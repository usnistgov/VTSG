"""
Generator Module.

This is the main module.  It generates test cases.

 *modified "Tue Jul 11 14:37:23 2023" *by "Paul E. Black"
"""

import time
from jinja2 import Template, DebugUndefined, Environment, exceptions
from src.manifest import Manifest
from src.file_manager import FileManager
from src.input_sample import InputSample
from src.filter_sample import FilterSample
from src.sink_sample import SinkSample
from src.exec_query import ExecQuerySample
from src.complexity import ComplexitySample
from src.condition import ConditionSample
from src.file_template import FileTemplate
from src.test_case import TestCase
import src.select_by_acts

import xml.etree.ElementTree as ET


class CaseSummary(object):
    """
    Count of the number of safe and unsafe test cases, by flaw and by group

    Args:
        none

    Attributes:
        **counts** (dict of dict of dict): The counts.  First dict is by group,
        which is dict by flaw, which is a dict of counts of safe & unsafe cases.

    """

    def __init__(self):
        self.counts = {} # nothing saved, yet

    def update_counts(self, case):
        """
        Update the counts for this test case.
        """

        flaw_group = case.sink.flaw_group
        flaw = case.sink.flaw_type
        # create group or flaw if this is the first case in the group or flaw
        if flaw_group not in self.counts:
            self.counts[flaw_group] = {}
        if flaw not in self.counts[flaw_group]:
            self.counts[flaw_group][flaw] = {}
            self.counts[flaw_group][flaw]["safe_sample"] = 0
            self.counts[flaw_group][flaw]["unsafe_sample"] = 0

        if case.is_safe_selection():
            self.counts[flaw_group][flaw]["safe_sample"] += 1
        else:
            self.counts[flaw_group][flaw]["unsafe_sample"] += 1

    def report_counts(self, caption):
        """
        Print final report for this run: number of safe/unsafe by flaw, group, and total.
        """
        total = 0
        print(f'{caption}')
        for flaw_group in self.counts:
            group_total = 0
            flaw_group_label = flaw_group
            # in case the flaw_group is missing or the empty string
            if flaw_group_label == '':
                flaw_group_label = 'Empty'
            print(f'\t{flaw_group_label} group generation report:')
            for flaw in self.counts[flaw_group]:
                print(f'\t\t{flaw} generation report:')
                print(f'\t\t\t{self.counts[flaw_group][flaw]["safe_sample"]} safe samples')
                print(f'\t\t\t{self.counts[flaw_group][flaw]["unsafe_sample"]} unsafe samples')
                flaw_total = self.counts[flaw_group][flaw]["safe_sample"] + self.counts[flaw_group][flaw]["unsafe_sample"]
                group_total += flaw_total
                print(f'\t\t{flaw_total} total')

            print(f'\t{group_total} total')
            total += group_total

        print(f'{total} total')


class Generator(object):
    """Generator class

        Args :
            **date** (str): Human readable date of the generation used for the folder
             containing generated codes (for the manifest). Generated using strftime().

            **language** (str): Targeted language of the generator ('cs', 'php', and 'py' are currently coded).
            **template_directory** (str): The directory where the language files are found.

        Attributes :
            **date** (str): Human readable date of the generation.
            **_max_recursion** (int): Max level of recursion with complexities, 0 for flat code, 1 for one complexity, \
                                      2 for two, ... (private member, please use getter and setter).

            **_number_skipped** (int): Number of cases skipped or NOT selected. \
                    None means do not skip any. (private member, please use getter).

            **dir_name** (str): Name of the top-level director containing all
                the manifest files and the generated cases.

            **manifest** (Manifest): Manifest object to complete the manifest file with references to generated files.

            **report** (dict): The report for each group of flaws.

            **flaw_type_user** (list): Flaw types entered by user for the generation.

            **flaw_group_user** (list): Flaw groups entered by user for the generation.

            **start** (float): Starting time of the generation.

            **tab_input** (list): List (of :class:`.InputSample` objects) all input
                modules.

            **tab_filtering** (list): List (of :class:`.FilterSample` objects) all
                filter modules.

            **tab_sink** (list): List (of :class:`.SinkSample` objects) all sink modules.

            **tab_exec_queries** (list): List (of :class:`.ExecQuerySample` objects)
                all exec query modules.

            **tab_complexity** (list): List (of :class:`.ComplexitySample`) all
                complexity possibilities.

            **tab_condition** (list): List (of :class:`.ConditionSample`) all
                condition possibilities.

            **file_template** (:class:`.FileTemplate`) the template
                for current language.

            **current_input** (:class:`.InputSample`): The current selected input.

            **current_filter** (:class:`.FilterSample`): The current selected filter.

            **current_sink** (:class:`.SinkSample`): The current selected sink.

            **current_exec_queries** (:class:`.ExecQuerySample`): The current selected exec query.

            **current_code** (str): The current code.

            **complexities_queue** (List of :class:`.ComplexitySample`): The current stack of complexities.

            **map_flaw_group** (dict: flaw_group -> list(flaw)): a dict associating a
                list containing the numbers of flaws (str) to a flaw group (str).

            **test_cases**  (List of :class:`.TestCase`): The generated test cases,
              where each case is the selection of input, filter, sink, complexities, etc.

       """

    def __init__(self, date, language, template_directory):
        self._max_recursion = 1
        self._number_skipped = None # don't skip any generated cases
        self._ACTS_doi = None # don't use ACTS to select cases
        self.date = date
        self.report = CaseSummary()
        self.flaw_type_user = None
        self.flaw_group_user = None
        self.start = time.time()
        self.language = language
        self.test_cases = []

        # parse XML files
        tree_input = ET.parse(FileManager.getXML("inputs", template_directory, language)).getroot()
        self.tab_input = [InputSample(inp) for inp in tree_input]
        tree_filter = ET.parse(FileManager.getXML("filters", template_directory, language)).getroot()
        self.tab_filter = [FilterSample(filter) for filter in tree_filter]
        tree_sink = ET.parse(FileManager.getXML("sinks", template_directory, language)).getroot()
        self.tab_sink = [SinkSample(sink) for sink in tree_sink]
        tree_exec_query = ET.parse(FileManager.getXML("exec_queries", template_directory, language)).getroot()
        self.tab_exec_queries = [ExecQuerySample(exec_query) for exec_query in tree_exec_query]
        tree_complexities = ET.parse(FileManager.getXML("complexities", template_directory, language)).getroot()
        self.tab_complexity = [ComplexitySample(complexity) for complexity in tree_complexities.find("complexities")]
        self.tab_condition = [ConditionSample(condition) for condition in tree_complexities.find("conditions")]

        self.file_template = FileTemplate(ET.parse(FileManager.getXML("file_template", template_directory, language)).getroot())

        self.license = open("src/templates/file_rights.txt", "r").read()

        self.dir_name = "TestSuite_"+date+"/"+self.file_template.language_name
        self.manifest = Manifest(self.dir_name, self.date)

        # set current test case
        self.current_input = None
        self.current_filter = None
        self.current_sink = None
        self.current_exec_queries = None
        self.current_code = None
        self.complexities_queue = []
        self.map_flaw_group = {}

    def resetUID():
        """
        (Re)start the UID generator with a definite value, so generation of each
        case is independent of any cases generated (or not) before it.
        """
        Generator.UID = 0

    def getUID():
        """
        Generate a unique ID for classes/functions/variables name.
        At each call, the UID is incremented.
        """
        Generator.UID += 1
        return Generator.UID

    def generate(self, debug=False, generate_safe=True, generate_unsafe=True):
        """
        This function is the start of generation execution.
        It calls other functions to select inputs, filters, sinks, exec queries and
        complexities.  At the end of the calls, code chunks are combined into final
        source files.

        Args :
            **debug** (bool): no effect

            **generate_safe** (bool): If True, safe test cases are generated.

            **generate_unsafe** (bool): If True, unsafe test cases are generated.
        """
        self.create_map_flaw_group()
        self.manifest.createManifests(self.get_groups_to_generate())
        self.debug = debug
        self.generate_safe = generate_safe
        self.generate_unsafe = generate_unsafe

        # start of chain of calls to generate a list of test cases
        self.select_sink()

        # select which test cases to produce
        if self.number_skipped is not None:
            # skip every N test cases
            selected_test_cases = []
            for i in range(0, len(self.test_cases), self.number_skipped+1):
                selected_test_cases.append(self.test_cases[i])
        elif self.ACTS_doi is not None:
            # select using ACTS
            selected_test_cases = src.select_by_acts.select_cases_ACTS(self.test_cases, self.ACTS_doi)
        else:
            selected_test_cases = self.test_cases

        # start a new report to record only the selected test cases
        selected_case_report = CaseSummary()

        # generate code and write the source files for the selected cases
        for case in selected_test_cases:
            # generate the code
            case.gen_code()

            # write test case file(s) and add to manifest
            case.write_files()

            selected_case_report.update_counts(case)

        # finish the manifest files
        self.manifest.closeManifests()

        elapsed_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - self.start))

        # report the number of safe/unsafe cases generated
        self.report.report_counts('Generation report:')

        if self.number_skipped is not None or self.ACTS_doi is not None:
            # report the number of safe/unsafe cases selected
            selected_case_report.report_counts('\nSelected case report:')

        print(f'Generation time {elapsed_time}')

    # first step: select sink
    def select_sink(self):
        """
        Use all sinks one by one.  If this is the right group or type (that is, one
        chosen is selected by the user or "all"), proceed to the next step: select
        filter or select exec query.
        """
        for sink in self.tab_sink:
            if ((not self.flaw_type_user or sink.flaw_type in self.flaw_type_user)
               and (not self.flaw_group_user or sink.flaw_group in self.flaw_group_user)):
                self.current_sink = sink
                if sink.input_type != "none":
                    self.select_filter()
                else:
                    # forget any input or filter selections from previous loops
                    self.current_input  = None
                    self.current_filter = None
                    self.select_exec_queries()

    # second step: select filter
    def select_filter(self):
        """
        Use all filters one by one.  If the filter is compatible with the current
        sink, proceed to the next step: selecting the input.
        """
        for filter in self.tab_filter:
            # check if sink and filter are compatibles
            if filter.compatible_with_sink(self.current_sink):
                self.current_filter = filter
                self.select_input()

    # third step: select input
    def select_input(self):
        """
        Use all inputs one by one.  If the input is compatible with the current sink
        and current filter, proceed to the next step: selecting exec query.
        """
        for inp in self.tab_input:
            if inp.compatible_with_filter_sink(self.current_filter, self.current_sink):
                self.current_input = inp
                self.select_exec_queries()

    # fourth step: select exec_query if needed
    def select_exec_queries(self):
        """
        If this case needs an exec query, use all compatible exec queries.  In
        any case, proceed to complexity recursion-or-save step.
        """
        if self.current_sink.needs_exec():
            # select exec_queries
            for exec_query in self.tab_exec_queries:
                if self.current_sink.compatible_with_exec_queries(exec_query):
                    self.current_exec_queries = exec_query
                    self.recursion_or_save()
        else:
            # sink doesn't need exec query
            self.current_exec_queries = None
            self.recursion_or_save()

    # fifth step: generate complexity depths if needed or go right to save test case
    def recursion_or_save(self):
        '''
        If this uses an input and the filter needs complexities, wrap the filter
        in appropriate depths of complexities.
        Otherwise, save the test case.
        '''
        if self.current_sink.input_type != 'none' and self.current_filter.need_complexity:
            self.recursion_level()
        else:
            # forget any level of complexities from previous loops
            self.current_max_rec = 0
            self.save_test_case()

    # fifth-and-a-half step: generate all depths of complexities up to maximum
    def recursion_level(self):
        """
        Generate all depths of complexities up to the maximum:
            * if the max depth is 0, produce a test case with flat code
            * if the max depth is 1, produce a test case with flat code and test
		cases with one complexity around the filter code
            * if the max depth is 2, produce flat code case, test cases with one
		complexity, and cases with two complexities around the filter code.
            * and so on ...
        """
        # generate with 0, 1, 2, ... level of complexities
        for i in range(0, self.max_recursion + 1):
            self.current_max_rec = i
            # generate the case wrapped in i complexities
            self.select_complexities(i)

    # sixth step: wrap filter in "level" depth of complexities
    def select_complexities(self, level):
        """
        Go through all complexities.
        Specially process types of complexities, then call handle_condition to add
        conditions if the complexity needs one and recursively call this.
        At the end, save all the modules as a test case.

        Args :
            **level** (int): Nesting level of the complexity being generated.
        """
        if level == 0:
            # at the end of recursive call, we save selected modules
            self.save_test_case()
        else:
            # Select complexity for this level
            for complexity in self.tab_complexity:
                curr_complexity = complexity.clone()
                # add current complexity to array
                self.complexities_queue.append(curr_complexity)

                # foreach loops need an extra variable
                if curr_complexity.group == "loops" and curr_complexity.type == "foreach":
                    var_type = self.current_input.output_type
                    # replace id and var type name for foreach
                    curr_complexity.code = Template(curr_complexity.code, undefined=DebugUndefined).render(id=level, var_type=var_type)

                self.handle_condition(curr_complexity, level)

                # remove current complexity
                self.complexities_queue.pop()

    # sixth-and-a-half step: add conditions if needed. Recursively do next complexity.
    def handle_condition(self, curr_complexity, level):
        """
        If the current complexity needs a condition, loop through all conditions and
        compose them into the complexity code.  Regardless, recursively handle next
        level of complexities.
        The state of the complexity is updated with the result of the conditional.

        Args :
            **curr_complexity** (:class:`.ComplexitySample`) : The current complexity being generated.

            **level** (int): Nesting level of the complexity being generated.
        """
        if curr_complexity.need_condition():
            svg_cmpl = curr_complexity.code
            # add tabulation for indent
            svg_cmpl = ('\n'+'\t'*(self.current_max_rec - level)).join(svg_cmpl.splitlines())
            for cond in self.tab_condition:
                curr_complexity.set_cond_id(cond.id)
                curr_complexity.set_condition(cond.value)
                t = Template(svg_cmpl, undefined=DebugUndefined)
                # replace condition placeholder on the complexity code
                curr_complexity.code = t.render(condition=cond.code)
                # recursive call
                self.select_complexities(level-1)
        else:
            # recursive call
            self.select_complexities(level-1)

    # seventh step: save modules in a test case and count
    def save_test_case(self):
        """
        Create a new testcase for the selected modules and complexities.  Return if
        this case should not be generated, i.e., because of user-selected safety.
        Count this case in the final summary.
        """

        case = TestCase(generator  = self, # ACCESS ONLY - DOES NOT MODIFY ANY ATTRIBUTE
                        input      = self.current_input,
                        complexity_list = [c.clone() for c in self.complexities_queue],
                        filter     = self.current_filter,
                        sink       = self.current_sink,
                        exec_query = self.current_exec_queries)

        # check if we need to generate (if it's only safe/unsafe generation)
        if (case.is_safe_selection() and not self.generate_safe) or (not case.is_safe_selection() and not self.generate_unsafe):
            return

        # save this selection
        self.test_cases.append(case)

        # update summary counts
        self.report.update_counts(case)


    def get_group_list(self):
        """
        Returns all flaw groups got from the XML files.
        """
        return {sink.flaw_group for sink in self.tab_sink}

    def get_flaw_list(self):
        """
        Return all flaw types got from the XML files.
        """
        return {sink.flaw_type for sink in self.tab_sink}

    def set_flaw_type_user(self, value):
        """
        Set the flaws got from the user input (-f and --flaw options).

        Args :
            **value** (list(str)): The list containing the flaws.
        """
        self.flaw_type_user = value

    def set_flaw_group_user(self, value):
        """
        Sets the flaw groups got from the user input (-g and --group options).

        Args :
            **value** (list(int)): The list containing the flaw groups.
        """
        self.flaw_group_user = value

    def create_map_flaw_group(self):
        """
        Create a dict with a list of flaw types (str) associated to each flaw group (str).
        """
        for group in self.get_group_list():
            self.map_flaw_group[group] = []

        for cwe in self.tab_sink:
            self.map_flaw_group[cwe.flaw_group].append(cwe.flaw_type)

    def get_groups_to_generate(self):
        """

        """
        tmp = []
        if self.flaw_group_user:
            tmp = self.flaw_group_user

        for flaw in self.flaw_type_user:
                for group in self.map_flaw_group:
                    if flaw in self.map_flaw_group[group]:
                        tmp.append(group)

        if tmp:
            return list(set(tmp))  # remove duplicates
        else:
            return list(self.get_group_list())


    @property
    def max_recursion(self):
        """
        Max level of recursion with complexities, 0 for flat code, 1 for one complexity, 2 for two, ...

        :getter: Returns this maximum recursion.
        :setter: Sets this maximum direction.
        :type: int
        """
        return self._max_recursion

    @max_recursion.setter
    def max_recursion(self, value):
        """
        Set the maximum recursion parameter.
        """
        self._max_recursion = value

    @property
    def number_skipped(self):
        """
        Number of cases that are not selected for every one generated case that is.

        :getter: Returns this number.
        :type: int
        """
        return self._number_skipped

    @property
    def ACTS_doi(self):
        """
        If not None, use ACTS with this Degree of Interaction to select cases.

        :getter: Returns this number.
        :type: int
        """
        return self._ACTS_doi

    @staticmethod
    def remove_indent(code, all=False):
        """
        Remove tabs that precede every line.  In other words, find the fewest number
        of leading tabs, and remove that many from every line after the first line.
        Remove blank lines after the first line.  "Blank line" means empty or
        consisting of only white space.
        """
        if all:
            code_res = ''
            for line in code.split('\n'):
                if len(line.strip()):
                    code_res += line.strip() + "\n"
        else:
            min_tabs = -1
            for line in code.split('\n'):
                if len(line.strip()):
                    # line is not blank
                    nlt = len(line) - len(line.lstrip('\t'))
                    # nlt is the number of leading tabs
                    if nlt < min_tabs or min_tabs == -1:
                        min_tabs = nlt
            # here, min_tabs is least number of leading tabs or -1 if all lines are blank
            if min_tabs == -1:
                min_tabs = 0
            for i, line in enumerate(code.split('\n')):
                if i == 0:
                    code_res = line + '\n'
                else:
                    if len(line.strip()):
                        code_res += line[min_tabs:] + "\n"
        return code_res

def test_remove_indents():
    """Built-in self-test for remove_indents().  The plan is a kind of exhaustive test:
    try 129 640 short strings that represent classes that might make a difference.
    See below for details."""

    ##################################################################################
    #
    #		auxiliary functions to test remove_indents()
    #
    ##################################################################################

    def print_show_eof(text):
        """Print text. End with % and newline if text does not end with newline.
        Replace spaces with periods (.) for visibility"""
        text = text.replace(' ', '.')
        if len(text) == 0:
            print('%')
        elif text[-1] == '\n':
            print(text, end='')
        else:
            print(f'{text}%')

    def compare_remove_indents(text, test_name, verbose = False):
        """Compare the result of a new implementation of remove_indent() and the
        existing implementation as an oracle.  If anything differs, report it and exit."""

        if verbose:
            print(f'test {test_name}.  Test input is:')
            print_show_eof(text)

        result     = Generator.remove_indent(text)
        new_result = Generator.NEW_remove_indent(text)

        if result != new_result:
            print(f'## results differ for {test_name}.  Test input is:')
            print_show_eof(text)

            print('## remove_indent() returns')
            print_show_eof(result)

            print('## new remove_indent() returns')
            print_show_eof(new_result)

            import sys
            sys.exit(1)

    def one_word():
        """Return a new word every time this is executed."""
        import re
        # "text" is the quote below as an array of words.  All non-letters are removed.
        text = re.split('[^a-zA-Z]+', """
        34 Behold, there are many called, but few are chosen. And why are they not chosen?
        35 Because their hearts are set so much upon the things of this world, and aspire to the honors of men, that they do not learn this one lesson—
        36 That the rights of the priesthood are inseparably connected with the powers of heaven, and that the powers of heaven cannot be controlled nor handled only upon the principles of righteousness.
        37 That they may be conferred upon us, it is true; but when we undertake to cover our sins, or to gratify our pride, our vain ambition, or to exercise control or dominion or compulsion upon the souls of the children of men, in any degree of unrighteousness, behold, the heavens withdraw themselves; the Spirit of the Lord is grieved; and when it is withdrawn, Amen to the priesthood or the authority of that man.
        38 Behold, ere he is aware, he is left unto himself, to kick against the pricks, to persecute the saints, and to fight against God.
        39 We have learned by sad experience that it is the nature and disposition of almost all men, as soon as they get a little authority, as they suppose, they will immediately begin to exercise unrighteous dominion.
        40 Hence many are called, but few are chosen.
        41 No power or influence can or ought to be maintained by virtue of the priesthood, only by persuasion, by long-suffering, by gentleness and meekness, and by love unfeigned;
        42 By kindness, and pure knowledge, which shall greatly enlarge the soul without hypocrisy, and without guile—
        43 Reproving betimes with sharpness, when moved upon by the Holy Ghost; and then showing forth afterwards an increase of love toward him whom thou hast reproved, lest he esteem thee to be his enemy;
        44 That he may know that thy faithfulness is stronger than the cords of death.
        45 Let thy bowels also be full of charity towards all men, and to the household of faith, and let virtue garnish thy thoughts unceasingly; then shall thy confidence wax strong in the presence of God; and the doctrine of the priesthood shall distil upon thy soul as the dews from heaven.
        46 The Holy Ghost shall be thy constant companion, and thy scepter an unchanging scepter of righteousness and truth; and thy dominion shall be an everlasting dominion, and without compulsory means it shall flow unto thee forever and ever.
        """) # Doctrine and Covenants 121:34-46

        index = 1
        while True:
            if text[index]: # don't return empty strings
                yield text[index]
            index += 1
            # start over, if necessary
            if index >= len(text):
                index = 1

    # start a generator yielding one word at a time.  All test generators use it.
    word = one_word()

    def generate_test_lines():
        """Return all strings consisting of 0 to 4 tabs then 0 to 3 blank spaces then an
        optional word.  The RE is     [\t]{0,4}[ ]{0,3}[:word:]?
        The rationale is that leading tabs are special, and lines that are empty (all
        white space) are special.  Tabs after a non-tab don't matter.  White space
        after a non-white-space don't matter.  This makes 5*4*2 = 40 different lines."""

        for tabs in range(4+1):
            for spaces in range(3+1):
                line = '\t' * tabs + ' ' * spaces
                yield line # without a word
                yield line + next(word) # with a word

    def generate_test_text_bare():
        """Return all strings (or, "paragraphs") of 1 to 3 lines.
        This makes 40 + 40*40 + 40*40*40 = 65 640 paragraphs."""

        # single lines
        for line in generate_test_lines():
            yield line

        # pairs of lines
        for line1 in generate_test_lines():
            for line2 in generate_test_lines():
                yield line1 + '\n' + line2

        # triples of lines
        for line1 in generate_test_lines():
            for line2 in generate_test_lines():
                for line3 in generate_test_lines():
                    yield line1 + '\n' + line2 + '\n' + line3

    def generate_test_text():
        """Return all strings (or, "paragraphs") of lines.  Return each paragraph twice:
        once as is, i.e. without a final newline (\n), and once with a final newline.
        Don't return the paragraph "as is" if it ends in a newline.  That only happens
        when line2 in pairs or line3 in triples was the empty string.  Those cases
        are duplicates of paragraphs one line shorter where THIS function adds the
        newline.  For example,
            connected\n
            rights\n
            (empty string)
        returned as it is results in the same thing as
            connected\n
            rights
        with a newline added here.
        This makes 2 * 65 640 - (40*1 + 40*40*1) = 129 640 test texts."""
        for paragraph in generate_test_text_bare():
            if paragraph == '' or paragraph[-1] != '\n':
                # the last line (line2 or line3) was not the empty string
                yield paragraph
            yield paragraph + '\n'


    ##################################################################################
    #
    #		The main body to test remove_indents()
    #
    ##################################################################################

    print('TESTING remove_indents()')

    count = 0

    for paragraph in generate_test_text():

        # identify each test case a little by counting the number of line
        num_lines = paragraph.count('\n')
        if paragraph == '' or paragraph[-1] != '\n':
            # paragraph did not end with a newline
            num_lines += 1

        # further identify particular test cases
        case = ''
        if paragraph == '': case = 'empty string'
        elif paragraph == '\n': case = 'just newline'
        elif paragraph[0] != '\t': case = 'no tabs on first line'
        if case != '': case = ' ' + case # separate case with a space if not empty

        count += 1
        compare_remove_indents(paragraph, f'{count}. {num_lines} line(s){case}')

    print(f'Done with {count} tests')
    # if this is a test, don't continue running vtsg
    import sys
    sys.exit(1)

# To test remove_indents()
#   Step 1. define a New_remove_indents()
#   Step 2. uncomment the call of test_remove_indents() below
#   Step 3. run vtsg like usual, e.g. python vtsy.py -l py
# When generator.py is loaded, test_remove_indent() will run then exit
#test_remove_indents()

# end of generator.py
