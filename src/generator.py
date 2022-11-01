"""
Generator Module.

This is the main module.  It generates test cases.

 *modified "Tue Nov  1 15:53:01 2022" *by "Paul E. Black"
"""

import time
from jinja2 import Template, DebugUndefined, Environment, exceptions
from src.manifest import Manifest
from src.file_manager import FileManager
from src.input_sample import InputSample
from src.filtering_sample import FilteringSample
from src.sink_sample import SinkSample
from src.exec_query import ExecQuerySample
from src.complexity import ComplexitySample
from src.condition import ConditionSample
from src.file_template import FileTemplate
from src.synthesize_code import make_assign, get_indent, fix_indents
import src.complexities_generator

import xml.etree.ElementTree as ET


class Generator(object):
    """Generator class

        Args :
            **date** (str): Human readable date of the generation used for the folder containing generated codes (for \
                        the manifest). Generated using strftime().

            **language** (str): Targeted language of the generator ('cs', 'php', and 'py' are currently coded).
            **template_directory** (str): The directory where the language files are found.

        Attributes :
            **date** (str): Human readable date of the generation.
            **_max_recursion** (int): Max level of recursion with complexities, 0 for flat code, 1 for one complexity, \
                                      2 for two, ... (private member, please use getter and setter).

            **_number_generated** (int): Number of triplets (input,filter,sink) generated (private member, \
                                         please use getter and setter).

            **dir_name** (str): Directory name of the folder containing generated cases.

            **manifest** (Manifest): Manifest object to complete the manifest file with references to generated files.

            **safe_sample** (int): Counter for safe sample.

            **unsafe_sample** (int): Counter for unsafe sample.

            **report** (dict): The report for each group of flaws.

            **flaw_type_user** (list): Flaw types entered by user for the generation.

            **flaw_group_user** (list): Flaw groups entered by user for the generation.

            **start** (float): Starting time of the generation.

            **end** (float): Ending generate time.

            **tab_input** (list): List (of :class:`.InputSample` objects) all input
                modules.

            **tab_filtering** (list): List (of :class:`.FilteringSample` objects) all
                filter modules.

            **tab_sink** (list): List (of :class:`.SinkSample` objects) all sink modules.

            **tab_exec_queries** (list): List (of :class:`.ExecQuerySample` objects)
                all exec query modules.

            **tab_complexity** (list): List (of :class:`.ComplexitySample`) all
                complexity possibilities.

            **tab_condition** (list): List (of :class:`.ConditionSample`) all
                condition possibilities.

            **file_template** (list): List (of :class:`.FileTemplate`) the template
                for current langage.

            **current_input** (:class:`.InputSample`): The current selected input.

            **current_filter** (:class:`.FilteringSample`): The current selected filter.

            **current_sink** (:class:`.SinkSample`): The current selected sink.

            **current_exec_queries** (:class:`.ExecQuerySample`): The current selected exec query.

            **current_code** (str): The current code.

            **complexities_queue** (List of :class:`.ComplexitySample`): The current stack of complexities.

            **map_flaw_group** (dict: flaw_group -> list(flaw)): a dict associating a
                list containing the numbers of flaws (str) to a flaw group (str).
       """

    UID = 0
    """Unique ID for generated functions/classes/variables name."""

    def __init__(self, date, language, template_directory):
        self._max_recursion = 1
        self._number_generated = -1
        self.date = date
        self.safe_sample = 0
        self.unsafe_sample = 0
        self.report = {}
        self.flaw_type_user = None
        self.flaw_group_user = None
        self.start = time.time()
        self.language = language
        self.end = 0

        # parse XML files
        tree_input = ET.parse(FileManager.getXML("input", template_directory, language)).getroot()
        self.tab_input = [InputSample(inp) for inp in tree_input]
        tree_filter = ET.parse(FileManager.getXML("filtering", template_directory, language)).getroot()
        self.tab_filter = [FilteringSample(filter) for filter in tree_filter]
        tree_sink = ET.parse(FileManager.getXML("sink", template_directory, language)).getroot()
        self.tab_sink = [SinkSample(sink) for sink in tree_sink]
        tree_exec_query = ET.parse(FileManager.getXML("exec_queries", template_directory, language)).getroot()
        self.tab_exec_queries = [ExecQuerySample(exec_query) for exec_query in tree_exec_query]
        tree_complexities = ET.parse(FileManager.getXML("complexities", template_directory, language)).getroot()
        self.tab_complexity = [ComplexitySample(complexity) for complexity in tree_complexities.find("complexities")]
        self.tab_condition = [ConditionSample(condition) for condition in tree_complexities.find("conditions")]

        self.file_template = FileTemplate(ET.parse(FileManager.getXML("file_template", template_directory, language)).getroot())

        self.dir_name = "TestSuite_"+date+"/"+self.file_template.language_name
        self.manifest = Manifest(self.dir_name, self.date)

        # set current sample
        self.current_input = None
        self.current_filter = None
        self.current_sink = None
        self.current_exec_queries = None
        self.current_code = None
        self.complexities_queue = []
        self.map_flaw_group = {}

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
        # start of chain of calls to generate test cases
        self.select_sink()
        # generate the repport with number of safe/unsafe, time, ...
        self.generation_report()

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
                    self.current_max_rec = 0
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
            if inp.compatible_with_filtering_sink(self.current_filter, self.current_sink):
                self.current_input = inp
                self.select_exec_queries()

    # fourth step: select exec_query if needed
    def select_exec_queries(self):
        """
        If this case needs an exec query, use all compatible exec queries.  In
        any case, proceed to complexity recursion step if needed or directly
        to compose step if no complexities needed.
        """
        if self.current_sink.needs_exec():
            # select exec_queries
            for exec_query in self.tab_exec_queries:
                if self.current_sink.compatible_with_exec_queries(exec_query):
                    self.current_exec_queries = exec_query
                    self.recursion_or_compose()
        else:
            # sink doesn't need exec query
            self.current_exec_queries = None
            self.recursion_or_compose()

    # fifth step: generate complexity depths if needed or go right to compose
    def recursion_or_compose(self):
        '''
        If this uses an input, wrap the filter in appropriate depths of complexities.
        Otherwise, proceed directly to compose.
        '''
        if self.current_sink.input_type != "none":
            self.recursion_level()
        else:
            self.compose()

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
        # HACK limit the number of generated combinations of (input, filter, sink)
        if self.number_generated == 0:
            return
        self.number_generated -= 1

        # generate with 0,1,2,... level of complexities
        max_rec = self.max_recursion if self.current_sink.need_complexity else 0
        for i in range(0, max_rec+1):
            self.current_max_rec = i
            # generate the case wrapped in i complexities
            self.select_complexities(i)

    # sixth step: wrap filter in "level" depth of complexities
    def select_complexities(self, level):
        """
        This function browse all complexities.
        Each type of complexity can be use with special processing and call the need_condition method
        to check if the complexity need a condition.
        At the end we call the next function for compose then into one code chunk.

        Args :
            **level** (int): Nesting level of the complexity being generated.
        """
        if level == 0:
            # at the end of recursive call, we compose selected into one
            self.compose()
        else:
            # Select complexity for this level
            for complexity in self.tab_complexity:
                curr_complexity = complexity.clone()
                # add current complexity to array
                self.complexities_queue.append(curr_complexity)
                # pretraitment per type before recursive call
                # Conditionals
                if curr_complexity.group == "conditionals":
                    if curr_complexity.type == "if":
                        self.need_condition(curr_complexity, level)
                    if curr_complexity.type == "switch":
                        self.need_condition(curr_complexity, level)

                # Jumps
                if curr_complexity.group == "jumps":
                    if curr_complexity.type == "goto":
                        self.need_condition(curr_complexity, level)

                # Loops
                if curr_complexity.group == "loops":
                    if curr_complexity.type == "for":
                        self.need_condition(curr_complexity, level)
                    if curr_complexity.type == "while":
                        self.need_condition(curr_complexity, level)
                    if curr_complexity.type == "foreach":
                        var_type = self.current_input.output_type
                        # replace id and var type name for foreach
                        curr_complexity.code = Template(curr_complexity.code, undefined=DebugUndefined).render(id=level, var_type=var_type)
                        self.need_condition(curr_complexity, level)

                if curr_complexity.group == "functions":
                    if curr_complexity.type == "function":
                        self.need_condition(curr_complexity, level)
                if curr_complexity.group == "classes":
                    if curr_complexity.type == "class":
                        self.need_condition(curr_complexity, level)

                # remove current complexity
                self.complexities_queue.pop()

    def need_condition(self, curr_complexity, level):
        """
        This function checkd if the current complexity needs a condition.
        If it's needed, browse all conditions and compose them into the complexity code.
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

    # seventh step : compose previous code chunks
    def compose(self):
        """
        This method composes previously selected code chunks into a final program.
        Complexities are composed with the class complexities_generator and the filter is included into them.
        After we add input, complexities with filter, sink, exec query into the template code.
        Also, we add include, license, comments, into the template.
        At the end, we have final code which can be save into files.
        """

        var_id = 0
        # temporary code

        self.classes_code = []
        if self.current_sink.input_type != "none":
            # COMPLEXITIES
            # A ComplexitiesGenerator is created to compose complexities.
            # The return code is a sum complexities with input and output var which will be merged with input and sink variables
            compl_gen = src.complexities_generator.ComplexitiesGenerator(
			complexities_array=self.complexities_queue,
			template=self.file_template,
			input_type=self.current_input.output_type,
			output_type=self.current_sink.input_type,
			filtering=self.current_filter,
			language=self.language
            )
            # execute the compose method
            self.classes_code = compl_gen.compose()
            classes_imports = []
            # for each class, collect imports to use other generated classes
            for c in self.classes_code:
                classes_imports.append(c['name'])
            # We check if the filter code into complexities is executed or not
            self.executed = compl_gen.executed
            # import the new template that contains complexities
            self.template_code = compl_gen.get_template()
        else:
            self.template_code = self.file_template.code

        # check if we need to generate (if it's only safe/unsafe generation)
        if (self.is_safe_selection() and not self.generate_safe) or (not self.is_safe_selection() and not self.generate_unsafe):
            return

        input_code = ""
        filter_code = ""
        if self.current_sink.input_type != "none":
            # INPUT
            input_code = self.current_input.code
            # set output var name
            if self.current_input.output_type != "none":
                # We set the name of output tainted variable and get the result into input_code
                input_code = Template(input_code).render(out_var_name=compl_gen.in_ext_name, id=var_id)
            if self.current_input.need_id:
                var_id += 1
            input_code += '\n'

            # init filter var with input var
            input_code += (get_indent('input_content', self.template_code)
                           + make_assign(compl_gen.out_ext_name, compl_gen.in_ext_name,
								self.file_template))

            # FILTER
            # set input var name
            filter_code = self.current_filter.code
            in_name = ""
            out_name = ""
            if self.current_filter.input_type != "none":
                in_name = compl_gen.in_int_name
            # set output var name
            if self.current_filter.output_type != "none":
                out_name = compl_gen.out_int_name
            if self.current_filter.need_id:
                var_id += 1
            # We set the name of input/output tainted variable and get the result into filter_code
            filter_code = Template(filter_code, undefined=DebugUndefined).render(in_var_name=in_name, out_var_name=out_name, id=var_id)

        # add comment into code at the position of the flaw if unsafe
        flaw_str = ""
        if not self.is_safe_selection():
            # this flag is use to compute the line of the flaw in final file
            flaw_str = self.file_template.comment['inline']+"flaw"

        # SINK
        sink_code = self.current_sink.code
        try:
            sink_code = Template(sink_code, undefined=DebugUndefined).render(flaw=flaw_str)
        except exceptions.TemplateSyntaxError:
            # error in Jinja rendering
            print('Error while rendering sink code. sink_code is', end='')
            print(sink_code)
            raise # reraise the exception
        if self.current_sink.input_type != "none":
            # We set the name of input tainted variable and get the result into sink_code
            try:
                sink_code = Template(sink_code, undefined=DebugUndefined).render(in_var_name=compl_gen.out_ext_name, id=var_id)
            except exceptions.TemplateSyntaxError:
                # error in Jinja rendering
                print('Error while rendering sink code. sink_code is', end='')
                print(sink_code)
                raise # reraise the exception

        if self.current_sink.need_id:
            var_id += 1

        # EXEC QUERIES
        exec_queries_code = ""
        if self.current_exec_queries:
            exec_queries_code = self.current_exec_queries.code



        # LICENCE
        license_content = open("src/templates/file_rights.txt", "r").read()

        # IMPORTS
        # compose imports used on input, filter, and sink
        imports_content = set(self.current_sink.imports).union(set(self.file_template.imports))
        if self.current_sink.input_type != "none":
            imports_content = imports_content.union(set(self.current_input.imports)
                                                    .union(set(self.current_filter.imports)))
        # add imports from exec query if it's used
        if self.current_exec_queries:
            imports_content = imports_content.union(set(self.current_exec_queries.imports))
        # create source code with imports
        imports_code = self.file_template.generate_imports(imports_content)

        # comments at the beginning of the code that documents modules used
        if self.current_input and self.current_filter:
            comments_code = "\n".join([self.current_input.comment, self.current_filter.comment,
                                      self.current_sink.comment])
        else:
            comments_code = "\n".join([self.current_sink.comment])
        if self.current_exec_queries and self.current_exec_queries.comment:
            comments_code += "\n"+self.current_exec_queries.comment

        main_class_name = f'MainClass{src.generator.Generator.getUID()}'

        # COMPOSE TEMPLATE
        template = Template(self.template_code)
        file_content = template.render(license=license_content,
                                       comments=comments_code,
                                       stdlib_imports=imports_code,
                                       namespace_name=self.file_template.namespace,
                                       main_name=main_class_name,
                                       input_content=input_code,
                                       filtering_content=filter_code,
                                       sink_content=sink_code,
                                       exec_queries_content=exec_queries_code)
        self.current_code = fix_indents(file_content, self.file_template.indent)

        # generate code for any additional files
        # include filter into good code chunk on complexities
        # TODO improve this with preselected class
        for i, cl in enumerate(self.classes_code):
            aux_file_content = Template(cl['code']).render(license=license_content,
                                                           comments=comments_code,
                                                           filtering_content=filter_code)
            self.classes_code[i]['code'] = fix_indents(aux_file_content, self.file_template.indent)

        # write test case to file, update summary counts, and add to manifest
        self.write_files()

    # eighth step: write on disk, update counts, and add to manifest
    def write_files(self):
        """
        This method writes code for then current selection into files
        It adds an entry into the manifest with specified informations
        """
        current_flaw_group = self.current_sink.flaw_group
        current_flaw = self.current_sink.flaw_type
        files_path = []
        # Create main file
        file_name_suffix = ""
        if len(self.classes_code) > 0:
            file_name_suffix = "a"
        main_filename = self.generate_file_name(file_name_suffix)
        filemanager = FileManager(main_filename, self.dir_name,
                                  current_flaw_group,
                                  current_flaw,
                                  self.is_safe_selection(),
                                  self.current_code)
        filemanager.createFile()
        full_path = filemanager.getPath() + main_filename
        line = 0
        if not self.is_safe_selection():
            line = Generator.find_flaw(full_path, self.file_template.comment['inline'])
        files_path.append({'path': full_path, 'line': line})

        # Create any additional class files
        for i, cl in enumerate(self.classes_code):
            file_name_suffix = chr(ord("a") + 1 + i)
            filename = self.generate_file_name(file_name_suffix)
            filemanager = FileManager(filename, self.dir_name,
                                      current_flaw_group,
                                      current_flaw,
                                      self.is_safe_selection(),
                                      cl['code'])
            filemanager.createFile()
            full_path = filemanager.getPath() + filename
            files_path.append({'path': full_path, 'line': 0})

        # Update the report
        if current_flaw_group not in self.report:
            self.report[current_flaw_group] = {}
        if current_flaw not in self.report[current_flaw_group]:
            self.report[current_flaw_group][current_flaw] = {}
            self.report[current_flaw_group][current_flaw]["safe_sample"] = 0
            self.report[current_flaw_group][current_flaw]["unsafe_sample"] = 0

        if self.is_safe_selection():
            self.report[current_flaw_group][current_flaw]["safe_sample"] += 1
        else:
            self.report[current_flaw_group][current_flaw]["unsafe_sample"] += 1

        # update manifest
        input_type = "None : None"
        if self.current_input:
            input_type = self.current_input.input_type
        self.manifest.addTestCase(input_type,
                                  current_flaw_group,
                                  current_flaw,
                                  files_path,
                                  self.file_template.language_name)

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

    def is_safe_selection(self):
        """
        Returns true if the final source code is safe, false otherwise.
        The computation is :
        * True if any input, filter (and it is executed), sink, or exec query
            is safe and no input, executed filter, or sink is unsafe.
        * False else
        """
        safe_input = False
        if self.current_input:
            safe_input = self.current_input.is_safe(self.current_sink.flaw_type)  # input is safe
        safe_filter = False
        if self.current_filter:
            safe_filter = self.current_filter.is_safe(self.current_sink.flaw_type) and self.executed  # filter is safe and executed
        safe_sink = self.current_sink.safe  # sink is safe
        safe_eq = False
        if self.current_exec_queries:
            safe_eq = self.current_exec_queries.safe  # exec query is safe
        unsafe_input = False
        if self.current_input:
            unsafe_input = self.current_input.is_unsafe(self.current_sink.flaw_type)  # input is unsafe
        unsafe_filter = False
        if self.current_filter:
            unsafe_filter = self.current_filter.is_unsafe(self.current_sink.flaw_type) and self.executed
        unsafe_sink = self.current_sink.unsafe
        return ((safe_input or safe_filter or safe_sink or safe_eq) and not (unsafe_input or unsafe_filter or unsafe_sink))

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

    def generate_file_name(self, suffix):
        """
        Generate file name in format :
            flawtype__inputname__filtername__sinkname__execqueryname__X-Y1-Y2_File*suffix*.ext
            with X the number of complexity level, Y1, Y2 id of complexities and *suffix* the file number
            (0 for main file).

        Args :
            **suffix** (str): the file number (for the filename).
        """
        # flaw [input] [filter] sink [exec] complexity
        name = self.current_sink.flaw_type
        if self.current_input:
            name += "__I_"
            name += self.current_input.module_description()
        if self.current_filter:
            name += "__F_"
            name += self.current_filter.module_description()
        name += "__S_"
        name += self.current_sink.module_description()

        if self.current_exec_queries:
            name += "__EQ_"
            name += self.current_exec_queries.module_description()

        name += "__"
        cplx_name = ""
        for c in self.complexities_queue:
            cplx_name += "-" + c.get_complete_id()

        name += f'{self.current_max_rec}{cplx_name}'
        # suffix - for cases consisting of multiple files
        name += suffix
        # extension
        name += "."+self.file_template.file_extension
        return name

    # TODO:20 move this elsewhere either in the generator or in a new class
    def generation_report(self):
        """
        Print final report for this run: number of safe/unsafe by flaw, group, and time.
        """
        self.manifest.closeManifests()
        total = 0
        print('Generation report:')
        for flaw_group in self.report:
            group_total = 0
            flaw_group_label = flaw_group
            # in case the flaw_group is missing or the empty string
            if flaw_group_label == '':
                flaw_group_label = 'Empty'
            print(f'\t{flaw_group_label} group generation report:')
            for flaw in self.report[flaw_group]:
                print(f'\t\t{flaw} generation report:')
                print(f'\t\t\t{self.report[flaw_group][flaw]["safe_sample"]} safe samples')
                print(f'\t\t\t{self.report[flaw_group][flaw]["unsafe_sample"]} unsafe samples')
                flaw_total = self.report[flaw_group][flaw]["safe_sample"] + self.report[flaw_group][flaw]["unsafe_sample"]
                group_total += flaw_total
                print(f'\n\t\t{flaw_total} total')

            print(f'\t{group_total} total')
            total += group_total

        print(f'{total} total')
        self.end = time.time()
        print(f'Generation time {time.strftime("%H:%M:%S", time.gmtime(self.end - self.start))}')

    @staticmethod
    def find_flaw(fileName, comment_inline_code):
        """
        Return the number of the line following the first
                      //flaw...
        that is, a line with the string starting an in-line comment for this language
        and "flaw" in the generated file.  Return 0 if no such line found.

        Args :
            **fileName** (str): The name of the file in which //flaw will be sought.

            **comment_inline_code** (str): String starting an in-line comment
        """
        sample = open(fileName, 'r')
        flaw_code = comment_inline_code + "flaw"
        i = 1
        for line in sample:
            i += 1
            if (line.lstrip())[:len(flaw_code)] == flaw_code:
                return i + 1

        # //flaw not found
        return 0


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

    def get_extension(self):
        """
        Return the extension file
        """
        return self.file_template.file_extension

    @property
    def number_generated(self):
        """
        Number of triplets (input,filter,sink) generated.

        :getter: Returns this number.
        :setter: Sets this number.
        :type: int
        """
        return self._number_generated

    @number_generated.setter
    def number_generated(self, value):
        """
        Sets the number of generated trio.
        """
        self._number_generated = value

    @staticmethod
    def remove_indent(code, all=False):
        code_res = ""
        if all:
            for line in code.split('\n'):
                if len(line.strip()):
                    code_res += line.strip() + "\n"
        else:
            min_space = -1
            for line in code.split('\n'):
                nb = -1
                if len(line.strip()):
                    nb = 0
                    for c in line:
                        # if c == ' ':
                        #    nb += 1
                        if c == '\t':
                            nb += 1
                        else:
                            break
                if (nb < min_space or min_space == -1) and nb != -1:
                    min_space = nb
            if min_space == -1:
                min_space = 0
            for i, line in enumerate(code.split('\n')):
                if i == 0:
                    code_res += line + '\n'
                else:
                    if len(line.strip()):
                        code_res += line[min_space:] + "\n"
        return code_res
