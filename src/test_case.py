"""
Test Case Module.

The components or modules for one test case.  A test case is created by the
generator.  It becomes a source code file by being composed.

  *created "Thu Apr 13 16:25:48 2023" *by "Paul E. Black"
 *modified "Thu Jun  1 09:58:23 2023" *by "Paul E. Black"
"""

from jinja2 import Template, DebugUndefined
from src.file_manager import FileManager
from src.complexities_generator import ComplexitiesGenerator
from src.synthesize_code import make_assign, get_indent, fix_indents
import src.select_by_acts
import src.generator # for resetUID()

class TestCase(object):
    """TestCase class

        Args:
            **generator** (:class:`.Generator`): the generator, which has the global
                information that is the same for all case files

            **input** (:class:`.InputSample`): The input module.

            **filter** (:class:`.FilterSample`): The filter module.

            **sink** (:class:`.SinkSample`): The sink module.

            **exec_query** (:class:`.ExecQuerySample`): The exec query module.

            **complexity_list** (List of :class:`.ComplexitySample`): The list of
                complexities to wrap the filter in.

        Attributes:
            **generator** (:class:`.Generator`): the generator, with all the global
                information that is the same for all case files

            **input** (:class:`.InputSample`): The input module.

            **filter** (:class:`.FilterSample`): The filter module.

            **sink** (:class:`.SinkSample`): The sink module.

            **exec_query** (:class:`.ExecQuerySample`): The exec query module.

            **classes_code** (List of Dict): The list of things to build additional
                class files.

            **complexity_list** (List of :class:`.ComplexitySample`): The list of
                complexities to wrap the filter in.

            **_executed** (bool): True if the final placeholder code will be executed
       """

    def __init__(self, generator, input, complexity_list, filter, sink, exec_query):
        self.generator  = generator
        self.input      = input
        self.filter     = filter
        self.sink       = sink
        self.exec_query = exec_query
        self.complexity_list = complexity_list
        self.UID = 0

        # the final embedded code is executed if ALL complexities are executed
        self._executed = True
        for c in self.complexity_list:
            self._executed = self._executed and c.is_executed()

    def is_safe_selection(self):
        """
        Return true if the final source code is safe, false otherwise.
        The computation is :
        * True if any input, filter (and it is executed), sink, or exec query
            is safe and no input, executed filter, or sink is unsafe.
        * False else
        """
        safe_input = False
        if self.input:
            safe_input = self.input.is_safe(self.sink.flaw_type)  # input is safe
        safe_filter = False
        if self.filter:
            # filter makes this kind of flaw safe and is executed
            safe_filter = self.filter.is_safe(self.sink.flaw_type) and self._executed
        safe_sink = self.sink.safe  # sink is safe
        safe_eq = False
        if self.exec_query:
            safe_eq = self.exec_query.safe  # exec query is safe
        unsafe_input = False
        if self.input:
            unsafe_input = self.input.is_unsafe(self.sink.flaw_type)  # input is unsafe
        unsafe_filter = False
        if self.filter:
            unsafe_filter = self.filter.is_unsafe(self.sink.flaw_type) and self._executed
        unsafe_sink = self.sink.unsafe
        return ((safe_input or safe_filter or safe_sink or safe_eq) and
                not (unsafe_input or unsafe_filter or unsafe_sink))

    def generate_file_name(self, suffix):
        """
        Generate the name of the file(s) to be used for this case.  The formatisD :
            flawtype__input__filter__sink__execquery__X-Y1-Y2*suffix*.ext
            with X the number of complexity level, Y1 and Y2 the id of complexities,
            and *suffix* the letter (a for main file).  No suffix if this case only
            consists of one file.

        Args:
            **suffix** (str): the file suffix letter, if any.
        """

        name = self.sink.flaw_type
        if self.input:
            name += "__I_"
            name += self.input.module_description
        if self.filter:
            name += "__F_"
            name += self.filter.module_description
        name += "__S_"
        name += self.sink.module_description

        if self.exec_query:
            name += "__EQ_"
            name += self.exec_query.module_description

        name += "__"

        # add the number of complexities used ...
        name += f'{len(self.complexity_list)}'
        # ... and their ids
        for c in self.complexity_list:
            name += "-" + c.get_complete_id()

        # suffix - for cases consisting of multiple files
        name += suffix
        # extension
        name += "."+self.generator.file_template.file_extension

        return name

    @staticmethod
    def select_test_cases(test_cases):
        """
        Return a list of test cases selected to be generated and written.
        """

        # SKIMP - select by different methods. Or just use all of them.
        selected_test_cases = src.select_by_acts.select_cases_ACTS(test_cases)

        return selected_test_cases

    def gen_code(self):
        """
        Add input, complexities with filter, sink, exec query into the template
        code.  Also add includes, license, and comments into the template.
        At the end, we have final code that can be saved in file(s).
        """

        # restart numbering of variables, classes, etc.
        src.generator.Generator.resetUID()

        self.classes_code = []
        if self.sink.input_type != "none":
            # Create a ComplexitiesGenerator to compose complexities.  This also has
            # input and output variable names.
            compl_gen = ComplexitiesGenerator(
			    complexities_array=self.complexity_list,
			    template=self.generator.file_template,
		            input_type=self.input.output_type,
			    output_type=self.sink.input_type,
			    filtering=self.filter,
			    language=self.generator.language
                        )
            # Compose the complexities.  Return code for any additional class files.
            self.classes_code = compl_gen.compose()

            # import the new template that contains complexities
            self.template_code = compl_gen.get_template()
        else:
            self.template_code = self.generator.file_template.code

        file_template = self.generator.file_template

        var_id = 0

        input_code = ""
        filter_code = ""
        if self.sink.input_type != "none":
            # INPUT
            input_code = self.input.code
            # set the name of output tainted variable and put the result in input_code
            input_code = Template(input_code).render(out_var_name=compl_gen.in_ext_name, id=var_id) + '\n'
            if self.input.need_id:
                var_id += 1

            # init filter var with input var
            input_code += (get_indent('input_content', self.template_code)
                           + make_assign(compl_gen.out_ext_name, compl_gen.in_ext_name,
									file_template))

            # FILTER
            filter_code = self.filter.code
            # set input var name
            in_name = ""
            out_name = ""
            if self.filter.input_type != "none":
                in_name = compl_gen.in_int_name
            # set output var name
            if self.filter.output_type != "none":
                out_name = compl_gen.out_int_name
            if self.filter.need_id:
                var_id += 1
            # set the name of input/output tainted variable and put it in filter_code
            filter_code = Template(filter_code, undefined=DebugUndefined).render(in_var_name=in_name, out_var_name=out_name, id=var_id)

        # add comment into code at the position of the flaw if unsafe
        flaw_str = ""
        if not self.is_safe_selection():
            # this string marks the location of the flaw in the final file
            flaw_str = file_template.comment['inline']+"flaw"

        # SINK
        sink_code = self.sink.code
        try:
            sink_code = Template(sink_code, undefined=DebugUndefined).render(flaw=flaw_str)
        except exceptions.TemplateSyntaxError:
            # error in Jinja rendering
            print('Error while rendering sink code. sink_code is', end='')
            print(sink_code)
            raise # reraise the exception
        if self.sink.input_type != "none":
            # set the name of input tainted variable and put the result in sink_code
            try:
                sink_code = Template(sink_code, undefined=DebugUndefined).render(in_var_name=compl_gen.out_ext_name, id=var_id)
            except exceptions.TemplateSyntaxError:
                # error in Jinja rendering
                print('Error while rendering sink code. sink_code is:', end='')
                print(sink_code)
                raise # reraise the exception

        if self.sink.need_id:
            var_id += 1

        # EXEC QUERIES
        exec_query_code = ""
        if self.exec_query:
            exec_query_code = self.exec_query.code

        # LICENCE
        license_content = self.generator.license

        # IMPORTS
        # compose any imports used in input, filter, and sink
        imports_content = set(self.sink.imports).union(set(file_template.imports))
        if self.sink.input_type != "none":
            imports_content = imports_content.union(set(self.input.imports)
                                                    .union(set(self.filter.imports)))
        # add imports from exec query if it's used
        if self.exec_query:
            imports_content = imports_content.union(set(self.exec_query.imports))
        # create source code with imports
        imports_code = file_template.generate_imports(imports_content)

        # comments at the beginning of the code that document which modules were used
        comments_code = ''
        if self.input and self.input.comment:
            comments_code += self.input.comment + '\n'
        if self.filter and self.filter.comment:
            comments_code += self.filter.comment + '\n'
        comments_code += self.sink.comment + '\n'
        if self.exec_query and self.exec_query.comment:
            comments_code += self.exec_query.comment + '\n'
        comments_code = comments_code.rstrip('\n') # since composition adds a newline

        main_class_name = f'MainClass{type(self.generator).getUID()}'

        # COMPOSE TEMPLATE
        template = Template(self.template_code)
        file_content = template.render(license=license_content,
                                       comments=comments_code,
                                       stdlib_imports=imports_code,
                                       namespace_name=file_template.namespace,
                                       main_name=main_class_name,
                                       input_content=input_code,
                                       filtering_content=filter_code,
                                       sink_content=sink_code,
                                       exec_queries_content=exec_query_code)
        self.code = fix_indents(file_content, file_template.indent)

        # generate code for any additional files
        # include filter into good code chunk on complexities
        # TODO improve this with preselected class
        for i, cl in enumerate(self.classes_code):
            aux_file_content = Template(cl['code']).render(license=license_content,
                                                           comments=comments_code,
                                                           filtering_content=filter_code)
            self.classes_code[i]['code'] = fix_indents(aux_file_content, file_template.indent)


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

    def write_files(self):
        """
        Write the source code file(s) for this test case.  Add appropriate entries to
        the manifest.
        """

        flaw_group = self.sink.flaw_group
        flaw = self.sink.flaw_type
        files_path = []
        # Create main file
        file_name_suffix = ""
        if len(self.classes_code) > 0:
            file_name_suffix = "a"
        main_filename = self.generate_file_name(file_name_suffix)
        filemanager = FileManager(main_filename, self.generator.dir_name,
                                  flaw_group,
                                  flaw,
                                  self.is_safe_selection(),
                                  self.code)
        filemanager.createFile()

        # start entry for manifest
        file_template = self.generator.file_template

        full_path = filemanager.getPath() + main_filename
        line = 0
        if not self.is_safe_selection():
            line = self.find_flaw(full_path, file_template.comment['inline'])
        files_path.append({'path': full_path, 'line': line})

        # Create any additional class files
        for i, cl in enumerate(self.classes_code):
            file_name_suffix = chr(ord("a") + 1 + i)
            filename = self.generate_file_name(file_name_suffix)
            filemanager = FileManager(filename, self.generator.dir_name,
                                      flaw_group,
                                      flaw,
                                      self.is_safe_selection(),
                                      cl['code'])
            filemanager.createFile()
            full_path = filemanager.getPath() + filename
            files_path.append({'path': full_path, 'line': 0})

        # update manifest
        input_type = "None : None"
        if self.input:
            input_type = self.input.input_type
        self.generator.manifest.addTestCase(input_type,
                                  flaw_group,
                                  flaw,
                                  files_path,
                                  file_template.language_name)


    def __str__(self):
        if self.input is None:
            input_description = '(none)'
        else:
            input_description = self.input.module_description
        complexity_ids = ''
        for c in self.complexity_list:
            complexity_ids += ' ' + c.get_complete_id()
        if self.filter is None:
            filter_description = '(none)'
        else:
            filter_description = self.filter.module_description
        if self.exec_query is None:
            eq_description = '(none)'
        else:
            eq_description = self.exec_query.module_description
        return ('*** Test Case ***\n' +
                f'input {input_description}\n' +
                f'{len(self.complexity_list)} complexities{complexity_ids}\n' +
                f'filter {filter_description}\n' +
                f'sink {self.sink.module_description}\n' +
                f'exec query {eq_description}')

# end of test_case.py
