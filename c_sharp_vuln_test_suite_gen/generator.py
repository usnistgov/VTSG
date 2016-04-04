"""
Generator Module.

This is the main module used to generate the test cases.
"""

import time
from jinja2 import Template, DebugUndefined, Environment
from c_sharp_vuln_test_suite_gen.manifest import Manifest
from c_sharp_vuln_test_suite_gen.file_manager import FileManager
from c_sharp_vuln_test_suite_gen.input_sample import InputSample
from c_sharp_vuln_test_suite_gen.filtering_sample import FilteringSample
from c_sharp_vuln_test_suite_gen.sink_sample import SinkSample
from c_sharp_vuln_test_suite_gen.exec_query import ExecQuerySample
from c_sharp_vuln_test_suite_gen.complexity import ComplexitySample
from c_sharp_vuln_test_suite_gen.condition import ConditionSample
from c_sharp_vuln_test_suite_gen.file_template import FileTemplate
import c_sharp_vuln_test_suite_gen.complexities_generator

import xml.etree.ElementTree as ET


class Generator(object):
    """Generator class

        Args :
            **date** (str): Human readable date of the generation used for the folder containing generated codes (for \
                        the manifest). Generated using strftime().

            **language** (str): Targeted language of the generator ('cs', 'php' values accepted).

        Attributes :
            **date** (str): Human readable date of the generation.
            **_max_recursion** (int): Max level of recursion with complexities, 0 for flat code, 1 for one complexity, \
                                      2 for two, ... (private member, please use getter and setter).

            **_number_generated** (int): Number of triplets (input,filtering,sink) generated (private member, \
                                         please use getter and setter).

            **dir_name** (str): Directory name of the folder containing generated codes.

            **manifest** (Manifest): Manifest object to complete the manifest file with references to generated files.

            **safe_sample** (int): Counter for safe sample.

            **unsafe_sample** (int): Counter for unsafe sample.

            **report** (dict): Dict which contains repports for each group of flaws.

            **flaw_type_user** (list): Flaw types entered by user for the generation.

            **flaw_group_user** (list): Flaw groups entered by user for the generation.

            **start** (float): Starting time of the generation.

            **end** (float): Ending generate time.

            **tab_input** (list): List (of :class:`.InputSample` objects) containing all input sample from XML file.

            **tab_filtering** (list): List (of :class:`.FilteringSample` objects) containing all filtering sample \
                                      from XML file.

            **tab_sink** (list): List (of :class:`.SinkSample` objects) containing all sink sample from XML file.

            **tab_exec_queries** (list): List (of :class:`.ExecQuerySample` objects) containing all exec query sample \
                                         from XML file.

            **tab_complexity** (list): List (of :class:`.ComplexitySample`) containing all complexity sample \
                                       from XML file.

            **tab_condition** (list): List (of :class:`.ConditionSample`) containing all condition sample from XML file.

            **file_template** (list): List (of :class:`.FileTemplate`) containing the template for current langage \
                                      from XML file.

            **current_input** (:class:`.InputSample`): Contains the current selected input.

            **current_filtering** (:class:`.FilteringSample`): Contains the current selected filtering.

            **current_sink** (:class:`.SinkSample`): Contains the current selected sink.

            **current_exec_queries** (:class:`.ExecQuerySample`): Contains the current selected exec query.

            **current_code** (str): Contains the current code.

            **complexities_queue** (List of :class:`.ComplexitySample`): Contains the current stack of complexities.

            **map_CWE_group** (dict: flaw_group -> list(CWE)): Contains a dict which associate a list containing the \
                                                               numbers of CWE (int) to a flaw group (str).
       """

    UID = 0
    """Uniq ID for generated functions/classes/variables name."""

    def __init__(self, date, language="cs"):
        self._max_recursion = 1
        self._number_generated = -1
        self.date = date
        self.safe_sample = 0
        self.unsafe_sample = 0
        self.report = {}
        self.flaw_type_user = None
        self.flaw_group_user = None
        self.start = time.time()
        self.end = 0

        # parse XML files
        tree_input = ET.parse(FileManager.getXML("input", language)).getroot()
        self.tab_input = [InputSample(inp) for inp in tree_input]
        tree_filtering = ET.parse(FileManager.getXML("filtering", language)).getroot()
        self.tab_filtering = [FilteringSample(filtering) for filtering in tree_filtering]
        tree_sink = ET.parse(FileManager.getXML("sink", language)).getroot()
        self.tab_sink = [SinkSample(sink) for sink in tree_sink]
        tree_exec_query = ET.parse(FileManager.getXML("exec_queries", language)).getroot()
        self.tab_exec_queries = [ExecQuerySample(exec_query) for exec_query in tree_exec_query]
        tree_complexities = ET.parse(FileManager.getXML("complexities", language)).getroot()
        self.tab_complexity = [ComplexitySample(complexity) for complexity in tree_complexities.find("complexities")]
        tree_condition = ET.parse(FileManager.getXML("complexities", language)).getroot()
        self.tab_condition = [ConditionSample(condition) for condition in tree_condition.find("conditions")]

        self.file_template = FileTemplate(ET.parse(FileManager.getXML("file_template", language)).getroot())

        self.dir_name = "TestSuite_"+date+"/"+self.file_template.language_name
        self.manifest = Manifest(self.dir_name, self.date)

        # set current samples
        self.current_input = None
        self.current_filtering = None
        self.current_sink = None
        self.current_exec_queries = None
        self.current_code = None
        self.complexities_queue = []
        self.map_CWE_group = {}

    def getUID():
        """
        Generate a uniq ID for classes/functions/variables name.
        At each call, the UID is incremented.
        """
        Generator.UID += 1
        return Generator.UID

    def generate(self, debug=False, generate_safe=True, generate_unsafe=True):
        """
        This function is the start of generation execution.
        It call other function recursilely to selecc input, filtering, sink, exec queries and complexities.
        At the end of the recursif chain, code chunks are combined into finales source files.

        Args :
            **debug** (bool): If its True, the debug mode remove the license on the top of generated files.

            **generate_safe** (bool): If its True, only safe test cases are generated.

            **generate_unsafe** (bool): If its True, only unsafe test cases are generated.
        """
        self.create_map_CWE_group()
        self.manifest.createManifests(self.get_groups_to_generate())
        self.debug = debug
        self.generate_safe = generate_safe
        self.generate_unsafe = generate_unsafe
        # start of recursives call
        self.select_sink()
        # generate the repport with number of safe/unsafe, time, ...
        self.generation_report()

    # fist step : browse sink
    def select_sink(self):
        """
        This method browse all sink one by one if the group or type is selected by the user or if its a complete \
        generation, then call the next recursion level.
        """
        for sink in self.tab_sink:
            if ((not self.flaw_type_user or sink.flaw_type_number() in self.flaw_type_user)
               and (not self.flaw_group_user or sink.flaw_group in self.flaw_group_user)):
                self.current_sink = sink
                if sink.input_type != "none":
                    self.select_filtering()
                else:
                    self.current_max_rec = 0
                    self.select_exec_queries()

    # second step : browse filtering
    def select_filtering(self):
        """
        This method browse all filtering one by one if the filtering is compatible with the current sink, then call \
        the next recursion level.
        """
        # select filtering
        for filtering in self.tab_filtering:
            self.current_filtering = filtering
            # check if sink and filtering are compatibles
            if filtering.compatible_with_sink(self.current_sink):
                self.select_input()

    # third step : browse input
    def select_input(self):
        """
        This method browse all input one by one if the input is compatible with the current sink and current \
        filtering, then call the next recursion level.
        """
        # select input
        for inp in self.tab_input:
            if inp.compatible_with_filtering_sink(self.current_filtering, self.current_sink):
                self.current_input = inp
                self.select_exec_queries()

    # fourth step : browse exec_queries
    def select_exec_queries(self):
        """
        This method browse all exec query if the current sink need exec query and the exec query is compatible \
        with the current sink, then call the next recursion level.
        """
        if self.current_sink.need_exec():
            # select exec_queries
            for exec_query in self.tab_exec_queries:
                if self.current_sink.compatible_with_exec_queries(exec_query):
                    self.current_exec_queries = exec_query
                    if self.current_sink.input_type != "none":
                        self.recursion_level()
                    else:
                        self.compose()
        else:
            # sink doesn't need exec query
            self.current_exec_queries = None
            if self.current_sink.input_type != "none":
                self.recursion_level()
            else:
                self.compose()

    # fouth step : compute recursion level
    def recursion_level(self):
        """
        This method compute the number of imbrication with complexities :
            * if the max recursion is 0 its produce a flat code
            * if the max recursion is 1 its produce code with on complexity around the filtering code
            * if the max recursion is 2 its produce code with two complexities aoround the filtering code
            * and so on ...
        """
        # HACK limit the number of generated (input,filtering,sink)
        if self.number_generated == 0:
            return
        self.number_generated -= 1

        # generate with 0,1,2,... level of complexities
        max_rec = self.max_recursion if self.current_sink.need_complexity else 0
        for i in range(0, max_rec+1):
            self.current_max_rec = i
            # Call next function with the number of complexity
            self.select_complexities(i)

    # fifth step bis : browse complexities
    def select_complexities(self, level):
        """
        This function browse all complexities.
        Each type of complexity can be use with special processing and call the need_condition method
        to check if the complexity need a condition.
        At the end we call the next function for compose then into one code chunk.

        Args :
            **level** (int): Imbrication level of the complexity being generated.
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
                # Conditionnals
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
        This function check if the current complexity needs a condition.
        If its needed, we browse all conditions and compose them into the complexity code.
        The state of the complexity is updated with the result of the conditional.

        Args :
            **curr_complexity** (:class:`.ConplexitySample`) : The current conmplexity being generated.

            **level** (int): Imbrication level of the complexity being generated.
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
        This method compose previous selected code chunk into a final code.
        Complexities are composed with the class complexities_generator and the filtering is incluse into them.
        After we add input, complexities with filtering, sink, exec query into the template code.
        Also, we add include, license, comments, into the template.
        At the end, we have final code who can be save into files.
        """

        var_id = 0
        # temporary code

        self.classes_code = []
        if self.current_sink.input_type != "none":
            # COMPLEXITIES
            # A ComplexitiesGenerator is created to compose complexities.
            # The return code is a sum complexities with input and output var whick will be merge with input and sink variables
            compl_gen = c_sharp_vuln_test_suite_gen.complexities_generator.ComplexitiesGenerator(complexities_array=self.complexities_queue, template=self.file_template, input_type=self.current_input.output_type, output_type=self.current_sink.input_type, filtering=self.current_filtering)
            # execute the compose method
            self.classes_code = compl_gen.compose()
            classes_imports = []
            # for each classes, we collect imports to use other generated classes
            for c in self.classes_code:
                classes_imports.append(c['name'])
            # We check if the filtering code into complexities is executed or not
            self.executed = compl_gen.executed
            # We imorts the new template who contain complexities
            self.template_code = compl_gen.get_template()
        else:
            self.template_code = self.file_template.code
        # check if we need to generate (if it's only safe/unsafe generation)
        if (self.is_safe_selection() and not self.generate_safe) or (not self.is_safe_selection() and not self.generate_unsafe):
            return

        input_code = ""
        filtering_code = ""
        if self.current_sink.input_type != "none":
            # INPUT
            input_code = self.current_input.code
            # set output var name
            if self.current_input.output_type != "none":
                # We set the name of output tainted variable and get the result into input_code
                input_code = Template(input_code).render(out_var_name=compl_gen.in_ext_name, id=var_id)
            if self.current_input.need_id:
                var_id += 1

            # init filtering var with input var
            init_var = compl_gen.out_ext_name+" = "+compl_gen.in_ext_name+";"
            input_code += "\n"+init_var

            # FILTERING
            # set input var name
            filtering_code = self.current_filtering.code
            in_name = ""
            out_name = ""
            if self.current_filtering.input_type != "none":
                in_name = compl_gen.in_int_name
            # set output var name
            if self.current_filtering.output_type != "none":
                out_name = compl_gen.out_int_name
            if self.current_filtering.need_id:
                var_id += 1
            # We set the name of input/output tainted variable and get the result into filtering_code
            filtering_code = Template(filtering_code, undefined=DebugUndefined).render(in_var_name=in_name, out_var_name=out_name, id=var_id)

        # add comment into code at the position of the flaw if it exist
        flaw_str = ""
        if not self.is_safe_selection():
            # this flag is use to compute the line of the flaw in final file
            flaw_str = self.file_template.comment['inline']+"flaw\n"

        # SINK
        sink_code = self.current_sink.code
        sink_code = Template(sink_code, undefined=DebugUndefined).render(flaw=flaw_str)
        if self.current_sink.input_type != "none":
            # We set the name of input tainted variable and get the result into sink_code
            sink_code = Template(sink_code, undefined=DebugUndefined).render(in_var_name=compl_gen.out_ext_name, id=var_id)

        if self.current_sink.need_id:
            var_id += 1

        # EXEC QUERIES
        exec_queries_code = ""
        if self.current_exec_queries:
            exec_queries_code = self.current_exec_queries.code



        # LICENCE
        license_content = ""
        if not self.debug:
            license_content = open("c_sharp_vuln_test_suite_gen/templates/file_rights.txt", "r").read()

        # IMPORTS
        # compose imports use on input, filtering and sink
        imports_content = set(self.current_sink.imports).union(set(self.file_template.imports))
        if self.current_sink.input_type != "none":
            imports_content = imports_content.union(set(self.current_input.imports)
                                                    .union(set(self.current_filtering.imports)))
        # add imports from exec query if it's use
        if self.current_exec_queries:
            imports_content = imports_content.union(set(self.current_exec_queries.imports))
        # create source code with imports
        imports_content = self.file_template.generate_imports(imports_content)
        # comments code
        if self.current_input and self.current_filtering:
            comments_code = "\n".join([self.current_input.comment, self.current_filtering.comment,
                                      self.current_sink.comment])
        else:
            comments_code = "\n".join([self.current_sink.comment])
        if self.current_exec_queries and self.current_exec_queries.comment:
            comments_code += "\n"+self.current_exec_queries.comment

        main_class_name = "MainClass"+str(c_sharp_vuln_test_suite_gen.generator.Generator.getUID())

        # COMPOSE TEMPLATE
        template = Template(self.template_code)
        file_content = template.render(license=license_content,
                                       comments=comments_code,
                                       stdlib_imports=imports_content,
                                       namespace_name=self.file_template.namespace,
                                       main_name=main_class_name,
                                       input_content=input_code,
                                       filtering_content=filtering_code,
                                       sink_content=sink_code,
                                       exec_queries_content=exec_queries_code)

        # include filtering into good code chunk on complexities
        # TODO improve this with preselected class
        for i, cl in enumerate(self.classes_code):
            self.classes_code[i]['code'] = Template(cl['code']).render(license=license_content,
                                                                       comments=comments_code,
                                                                       filtering_content=filtering_code)

        self.current_code = file_content
        # recursive call
        self.write_files()

    # eighth step : write on disk and update manifest
    def write_files(self):
        """
        This method writes code for then current selection into files
        It adds an entry into the manifest with specified informations
        """
        current_flaw_group = self.current_sink.flaw_group.lower()
        current_flaw = self.current_sink.flaw_type
        files_path = []
        # Create main file
        main_filename = self.generate_file_name("File1")
        filemanager = FileManager(main_filename, self.dir_name,
                                  "OWASP_"+current_flaw_group,
                                  current_flaw,
                                  self.is_safe_selection(),
                                  self.current_code)
        filemanager.createFile()
        full_path = filemanager.getPath() + main_filename
        line = 0
        if not self.is_safe_selection():
            line = Generator.findFlaw(full_path, self.file_template.comment['inline'])
        files_path.append({'path': full_path, 'line': line})

        # Create other classes
        for i, cl in enumerate(self.classes_code):
            filename = self.generate_file_name("File"+str(i+2))
            filemanager = FileManager(filename, self.dir_name,
                                      "OWASP_"+current_flaw_group,
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
        return {sink.flaw_group.lower() for sink in self.tab_sink}

    def get_cwe_list(self):
        """
        Return all flaw types got from the XML files.
        """
        return {sink.flaw_type_number() for sink in self.tab_sink}

    def is_safe_selection(self):
        """
        Returns true if the final source code is safe, false otherwise.
        The computation is :
        * True if on of input, filtering, sink or exec query is safe and no unsafe on input, filtering, sink \
            and exec query
        * False else
        """
        safe_input = False
        if self.current_input:
            safe_input = self.current_input.is_safe(self.current_sink.flaw_type)  # input is safe
        safe_filtering = False
        if self.current_filtering:
            safe_filtering = self.current_filtering.is_safe(self.current_sink.flaw_type) and self.executed  # filtering is safe and executed
        safe_sink = self.current_sink.safe  # sink is safe
        safe_eq = False
        if self.current_exec_queries:
            safe_eq = self.current_exec_queries.safe  # exec query is safe
        unsafe_input = False
        if self.current_input:
            unsafe_input = self.current_input.is_unsafe(self.current_sink.flaw_type)  # input is unsafe
        unsafe_filtering = False
        if self.current_filtering:
            unsafe_filtering = self.current_filtering.is_unsafe(self.current_sink.flaw_type) and self.executed
        unsafe_sink = self.current_sink.unsafe
        return ((safe_input or safe_filtering or safe_sink or safe_eq) and not (unsafe_input or unsafe_filtering or unsafe_sink))

    def set_flaw_type_user(self, value):
        """
        Sets the flaw types got from the user input (-c and --cwe options).

        Args :
            **value** (list(int)): The list containing the CWE numbers.
        """
        self.flaw_type_user = value

    def set_flaw_group_user(self, value):
        """
        Sets the flaw groups got from the user input (-f and --flaw-group options).

        Args :
            **value** (list(int)): The list containing the flaw groups.
        """
        self.flaw_group_user = value

    def create_map_CWE_group(self):
        """
        Create a dict which associate a list containing the numbers of CWE (int) to a flaw group (str).
        """
        for group in self.get_group_list():
            self.map_CWE_group[group.lower()] = []

        for cwe in self.tab_sink:
            self.map_CWE_group[cwe.flaw_group.lower()].append(cwe.flaw_type_number())

    def get_groups_to_generate(self):
        """

        """
        tmp = []
        if self.flaw_group_user:
            tmp = self.flaw_group_user

        for flaw in self.flaw_type_user:
                for group in self.map_CWE_group:
                    if flaw in self.map_CWE_group[group]:
                        tmp.append(group)

        if tmp:
            return list(set(tmp))  # remove duplicates
        else:
            return list(self.get_group_list())

    def generate_file_name(self, suffix):
        """
        Generate file name in format :
            flawtype__inputname__filteringname__sinkname__execqueryname__X-Y1-Y2_File*suffix*.ext
            with X the number of complexity level, Y1, Y2 id of complexities and *suffix* the file number
            (0 for main file).

        Args :
            **suffix** (str): the file number (for the filename).
        """
        # CWE input filtering sink [exec] complexity
        name = self.current_sink.flaw_type
        if self.current_input:
            name += "__I_"
            name += self.current_input.generate_file_name()
        if self.current_filtering:
            name += "__F_"
            name += self.current_filtering.generate_file_name()
        name += "__S_"
        name += self.current_sink.generate_file_name()

        if self.current_exec_queries:
            name += "__EQ_"
            name += self.current_exec_queries.generate_file_name()

        name += "__"
        cplx_name = ""
        for c in self.complexities_queue:
            cplx_name += "-" + c.get_complete_id()

        name += str(self.current_max_rec) + str(cplx_name)
        # suffix
        name += "_"+suffix
        # extension
        name += "."+self.file_template.file_extension
        return name

    # TODO:20 move this elsewhere either in the generator either in a new class
    def generation_report(self):
        """
        Prints final report for the generation.
        Prints number of safe/unsafe by CWE/group and generate time.
        """
        self.manifest.closeManifests()
        total = 0
        print("Generation report:\n")
        for flaw_group in self.report:
            group_total = 0
            print("\t" + flaw_group.upper() + " group generation report:\n")
            for flaw in self.report[flaw_group]:
                print("\t\t" + flaw.upper() + " generation report:\n")
                print("\t\t\t" + str(self.report[flaw_group][flaw]["safe_sample"]) + " safe samples")
                print("\t\t\t" + str(self.report[flaw_group][flaw]["unsafe_sample"]) + " unsafe samples")
                flaw_total = self.report[flaw_group][flaw]["safe_sample"] + self.report[flaw_group][flaw]["unsafe_sample"]
                group_total += flaw_total
                print("\n\t\t" + str(flaw_total) + " total\n")

            print("\t" + str(group_total) + " total\n")
            total += group_total

        print(str(total) + " total\n")
        self.end = time.time()
        print("Generation time " + time.strftime("%H:%M:%S", time.gmtime(self.end - self.start)))

    @staticmethod
    def findFlaw(fileName, comment_inline_code):
        """
        Seek //flaw flag into the generated file and got line number if it exists.

        Args :
            **fileName** (str): The filename of the file in which the flag *//flaw* will be searched.
        """
        sample = open(fileName, 'r')
        i = 1
        for line in sample.readlines():
            i += 1
            flaw_code = comment_inline_code + "flaw"
            if (line.lstrip())[:len(flaw_code)] == flaw_code:
                break
        if i == len(sample.readlines()):
            return 0
        else:
            return i + 1

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
        Number of triplets (input,filtering,sink) generated.

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
