"""
Complexities Generator Module.

Compose and generate the complexities that will be used by the Generator module.

 *modified "Wed Mar 13 16:38:38 2024" *by "Paul E. Black"
"""

from jinja2 import Template, DebugUndefined
import src.generator
from src.synthesize_code import make_assign, get_indent

class ComplexityInstance(object):
    """
    This is an instance of a complexity.
        Args:
            **_code** (str): The initial code for this instance.

            **_name** (str): The code name of the function or class,
                e.g. 'function_3' or 'Class_1'.

            **complexity_type** (str): Complexity type; from ComplexitySample _type,
                or 'class_traversal' or 'function_traversal'.  None if not initialized.

        Attributes:
            **_code** (str): The code for this instance.  This is refined during
                compliation.

            **_name** (str): The code name of the function or class,
                e.g. 'function_3' or 'Class_1'.

            **_type** (str): Complexity type; either from ComplexitySample _type,
                or 'class_traversal' or 'function_traversal'.  None if not initialized.

            **_local_declarations** (dict of {str (type), set of str (var)}): local
                variables to be declared.  Specifically, programming language data
                types, e.g. 'int' or 'string', and a set of variables of that type to
                be declared, e.g. 'tainted_11' or '$tainted_2'.

            **_imports** (set of str): things that need to be imported, e.g. "re",
                "math", or "random".  This may include things needed for complexities
                or conditions nested within this one.
    """

    def __init__(self, code, name='', complexity_type=None):
        self._code = code
        self._name = name
        self._type = complexity_type
        self._local_declarations = {}
        self._imports = set()

    @property
    def code(self):
        """
        The source code for this complexity instance.  This is refined during compliation.

        :getter: Return the code.
        :type: str
        """
        return self._code

    def set_code(self, code):
        """
        Set the code for this complexity.

        :setter: Sets the code.
        :type: str
        """
        self._code = code

    @property
    def name(self):
        """
        The code name of the function or class, e.g. 'function_3' or 'Class_1'.

        :getter: Return the name.
        :type: str
        """
        return self._name

    def set_name(self, name):
        """
        Set the code name of the function or class, e.g. 'function_3' or 'Class_1'.

        :setter: Set the name.
        :type: str
        """
        self._name = name

    @property
    def complexity_type(self):
        """
        The type of complexity; from ComplexitySample _type, or 'class_traversal' or
       'function_traversal'.  None if not initialized.

        :getter: Return the complexity type.
        :type: str
        """
        return self._type

    def set_complexity_type(self, complexity_type):
        """
        Set the complexity type.  This comes from ComplexitySample _type or is
        'class_traversal' or 'function_traversal'.

        :setter: Set the complexity type.
        :type: str
        """
        self._type = complexity_type

    @property
    def local_decls(self):
        """
        Variables to be declared.  Specifically, the programming language types used,
        e.g. 'int' or 'string', are keys that have a set of variables of that type to
        be declared, e.g. 'tainted_11' or '$tainted_2'.

        :getter: Return the local declarations
        :type: dict of {str (data type), set of str (var)}
        """
        return self._local_declarations

    def add_value_dict(self, data_type, var_name):
        """
        Remember to declare a variable, e.g. 'tainted_11' or '$tainted_2', of the
        code data type, e.g. 'int' or 'string'.

        :setter: Add the variable name with the given data type.
        """

        local_decl_dict = self.local_decls
        if data_type not in local_decl_dict:
            local_decl_dict[data_type] = set()
        local_decl_dict[data_type].add(var_name)

    @property
    def imports(self):
        """
        Return the imports needed (so far) for this complexity.

        :getter: Return the imports.
        :type: str
        """
        return self._imports

    def add_imports(self, imports):
        """
        Add more imports for this complexity.

        :setter: Adds imports.
        :type: str
        """
        self._imports = self._imports.union(imports)

    def __str__(self):
        return (
            self.code + '\n' +
            f'{self.name=}\n' +
            f'{self.complexity_type=}\n' +
            f'{self.local_decls=}\n' +
            f'{self.imports=}'
        )


class ComplexitiesGenerator(object):
    """
        Complexities Generator class

            Args :
                **complexities_array** (List of :class:`.ComplexitySample`): the list \
			of complexities to wrap around the filter.

                **template** (str): Template code.

                **input_type** (str): Input type got from the xml file.

                **output_type** (str): Output type got from the xml file.

                **filter_module** (str): The filter to use.

            Attributes :
                **complexities_array** (List of :class:`.ComplexitySample`): the list \
			of complexities to wrap around the filter.

                **template** (:class:`.FileTemplate`): Template code.

                **input_type** (str): Input type got from the xml file.

                **output_type** (str): Output type got from the xml file.

                **filter_module** (:class:`.FilterSample`): The filter.

                **complexities** (List of :class:`.ComplexityInstance`): list of
                                  complexity instances.

                **id_var_in** (int): ID for intern variables used in composition of complexities (in).

                **id_var_out** (int): ID for intern variables used in composition of complexities (out).

                **_in_ext_name** (str): Name of external intput variable (for input).

                **_in_int_name** (str): Name of internal intput variable (for filter).

                **_out_ext_name** (str): Name of external output variable (for sink).

                **_out_int_name** (str): Name of internal output variable (for filter).

                **template_code** (str): Modified template.

                **_imports** (str): list of things that need to be imported in the
                       top-level file.

                **_is_executed** (bool): True if the inner code is always executed.
                       False if inner code is never executed.
    """

    def __init__(self, complexities_array, template, input_type, output_type,
                 filter_module):
        self.complexities_array = complexities_array
        self.template = template
        self.input_type = input_type
        self.output_type = output_type
        self.filter_module = filter_module

        self.complexities = []
        self.complexities.append(ComplexityInstance('{{filtering_content}}'))

        self.id_var_in = len(complexities_array)*2
        self.id_var_out = self.id_var_in+1

        self._in_ext_name = None
        self._in_int_name = self.new_variable(self.input_type, self.id_var_in)
        self._out_ext_name = None
        self._out_int_name = self.new_variable(self.output_type, self.id_var_out)

        self._inner_is_executed = True # assume placeholder code is executed

    def __str__(self):
        return (
            f'{self.complexities_array}\n' +
            f'{self.template}\n' +
            f'in type: {self.input_type}\n' +
            f'out type: {self.output_type}\n' +
            f'{self.filter_module}' +
            f'{len(self.complexities)=} ' +
            f'{[f">>>> {c}" for c in self.complexities]}\n' +
            f'{self.id_var_in=}\n' +
            f'{self.id_var_out=}\n' +
            f'{self._in_ext_name=}\n' +
            f'{self._in_int_name=}\n' +
            f'{self._out_ext_name=}\n' +
            f'{self._out_int_name=}\n'
        )

    @property
    def in_ext_name(self):
        """
        Gets input external variable name.

        :getter: Returns this name.
        :type: str
        """
        return self._in_ext_name

    @property
    def in_int_name(self):
        """
        Gets input internal variable name.

        :getter: Returns this name.
        :type: str
        """
        return self._in_int_name

    @property
    def out_ext_name(self):
        """
        Gets output external variable name.

        :getter: Returns this name.
        :type: str
        """
        return self._out_ext_name

    @property
    def out_int_name(self):
        """
        Gets output internal variable name.

        :getter: Returns this name.
        :type: str
        """
        return self._out_int_name

    @property
    def get_template(self):
        """
        Gets modified template.

        :getter: Returns this name.
        :type: str
        """
        return self.template_code

    @property
    def imports(self):
        """
        Get the (possibly empty) set of things that the top-level code needs to import.

        :getter: Return the set.
        :type: str
        """
        return self._imports

    @property
    def inner_is_executed(self):
        """
        True if the inner code is always executed.  False if the inner code is never
        executed.

        :getter: Return the value.
        :type: bool
        """
        return self._inner_is_executed

    def var_name(self, id):
        '''
        Generate variable name from ID, including any prefix needed for the language
        '''
        return f'{self.template.prefix}tainted_{id}'

    def compose(self):
        """
        This method composes all complexities.  Return chunks of code that will need
        to go in auxiliary files, like class definitions.  The chunks returned is a
        (possibly empty) list of dict with 'code' and 'name'.
        """

        # import anything that the filter needs
        saved_imports = set(self.filter_module.imports)

        # for now, any inner {{placeholder}} code will be executed
        placeholder_is_executed = True

        # handle complexities from innermost one first
        for c in reversed(self.complexities_array):
            # get any imports needed for the <code> of this complexity or its condition
            imports_content = set(c.cond_imports).union(c.imports)

            # if the complexity has 2 parts (code and body), use body, else use code
            if c.indirection and c.in_out_var == "traversal":
                t = Template(c.body, undefined=DebugUndefined)
            else:
                t = Template(c.code, undefined=DebugUndefined)

            # if function/class generate a name
            call_name = None
            uid = src.generator.Generator.getUID() # Note: takes a UID even if not used.
            if c.type == "function":
                call_name = f'function_{uid}'
            elif c.type == "class":
                call_name = f'Class_{uid}'

            # create in/out vars
            in_var, out_var = self.get_in_out_var(c)

            complexity_code = self.complexities[0].code
            if not placeholder_is_executed:
                # The inner placeholder might not be excuted and set the out variable,
                # so add an assignment to make sure out_var is always initialized.
                if in_var and out_var: # ... unless there is no nested variable
                    initializing_assignment = ('\n' +
                                           make_assign(out_var, in_var, self.template)
                                           #+ f' {self.template.comment["inline"]}'
                                           #+ ' SYNTH Always Init out_var'
                                           + '\n')
                    complexity_code = (initializing_assignment + self.template.indent +
                                       complexity_code)

            # render on code
            self.complexities[0].set_code(t.render(placeholder=complexity_code,
                                        id=uid, in_var_name=in_var, out_var_name=out_var,
                                        call_name=call_name, in_var_type=self.input_type,
                                        out_var_type=self.output_type))

            # save for next outer complexity whether this complexity executes inner code
            placeholder_is_executed = placeholder_is_executed and c.is_executed()

            # traversal for class/function where the placeholder is in the body of function/class
            if c.indirection and c.in_out_var == "traversal":
                # LOCAL VARS
                local_var_code = self.generate_local_var_code(self.complexities[0].local_decls)
                # put local vars in body
                self.complexities[0].set_code(Template(self.complexities[0].code, undefined=DebugUndefined).render(local_var=local_var_code))
                # add in_var
                self.id_var_in -= 1
                in_var = self.new_variable(self.input_type, self.id_var_in)
                # add out_var
                self.id_var_out += 1
                out_var = self.new_variable(self.output_type, self.id_var_out)

                # remember type (or, elaborated type) of current complexity
                self.complexities[0].set_complexity_type(c.type)
                if c.type == "class":
                    self.complexities[0].set_complexity_type("class_traversal")
                    # this code will be in another file; import any saved there
                    self.complexities[0].add_imports(saved_imports)
                    saved_imports = set() # any containing complexity is in another file
                elif c.type == "function":
                    self.complexities[0].set_complexity_type("function_traversal")
                self.complexities[0].set_name(call_name)

                #########################################################################
                # The above code-and-stuff ultimately goes in an auxiliary file, so
                # start a new entry for the "main" code that goes in the "main" file.
                # Note: a subsequent loop may put *this* in an auxiliary file.
                self.complexities.insert(0, ComplexityInstance(c.code))
                placeholder_is_executed = c.is_executed
                t = Template(c.code, undefined=DebugUndefined)
                self.complexities[0].set_code(
                    t.render(placeholder=self.complexities[0].code, id=uid,
                        in_var_name=in_var, out_var_name=out_var, call_name=call_name))
            # if the placeholder is before or after the call to class/function
            elif c.indirection and (c.in_out_var == "in" or c.in_out_var == "out"):
                if c.type == "class" or c.type == "function":
                    body = Template(c.body, undefined=DebugUndefined).render(id=uid, in_var_type=self.input_type, out_var_type=self.output_type, call_name=call_name)
                    # BUG?? INSTEAD INSERT AT END, E.G., -1???
                    self.complexities.insert(1, ComplexityInstance(body, complexity_type=c.type, name=call_name))
                    placeholder_is_executed = c.is_executed

            # pass needed imports up to next outer complexity
            saved_imports = saved_imports.union(imports_content)

        # any remaining imports must be imported at the top level
        self._imports = saved_imports

        # Remember if the inner code might not be executed, to synthesize an
        # assignment to initialize the out variable in case it isn't.
        self._inner_is_executed = placeholder_is_executed

        return self.fill_template()

    def fill_template(self):
        """
        Fill template_code with previous composed complexities with local var and
        instructions.  Return a list of any code to go in separate files, like
        classes.
        """
        # names of external variables to connect with input and sink
        self._in_ext_name = self.new_variable(self.input_type, self.id_var_in)
        self._out_ext_name = self.new_variable(self.output_type, self.id_var_out)

        functions_code = ""
        classes_code = []

        # compose complexity i into i-1
        for c in reversed(self.complexities[1:]):
            if c.complexity_type == "class_traversal":
                # add a new class code when we have a traversal class
                imports_statements = self.template.generate_imports(c.imports)
                classes_code.append({'code': Template(c.code, undefined=DebugUndefined).render(static_methods=functions_code, stdlib_imports=imports_statements),
                                     'name': c.name})
                functions_code = ""
            elif c.complexity_type == "class":
                classes_code.append({'code': c.code,
                                     'name': c.name})
            elif c.complexity_type == "function_traversal":
                functions_code += Template(c.code, undefined=DebugUndefined).render(static_methods=functions_code)
                # Bug? set functions_code to "" here, so it isn't used again??
            elif c.complexity_type == "function":
                functions_code += c.code + "\n\n"

        # generate local vars
        local_var_code = self.generate_local_var_code(self.complexities[0].local_decls)
        filter_code = self.complexities[0].code

        t = Template(self.template.code, undefined=DebugUndefined)
        # fill template with local vars, complexities and static methods
        self.template_code = t.render(filtering_content=filter_code, local_var=local_var_code, static_methods=functions_code)

        # return all classes not in the main file
        return classes_code

    def generate_local_var_code(self, local_vars):
        '''Generate statement(s) to declare and initialize local variables. For example,
                      "string localvar_1 = None;\n    int localvar_2 = 0;"
           Indentation precedes second and following vars, since macro replacement
           only adds it to the first one.  String does not end with a
           new line (so a single statement just drops into a macro place).
        '''
        local_var_code = ""
        local_var_indent = get_indent('local_var', self.template.code)
        if local_var_indent is None:
            # no {{local_var}} provided - don't declare variables in this language
            return ""

        # loop through every type
        for t in local_vars:
            declare_type = self.template.get_type_var_code(t)
            init = self.template.get_init_var_code(t)
            # generate code to declare and initialize each variable of this type
            for n in sorted(list(local_vars[t])):
                # for second and following vars, add indicated indent
                if local_var_code != "":
                    local_var_code += local_var_indent
                # if there is a string to declare the variable, add it (and a space)
                if declare_type != "":
                    local_var_code += declare_type + " "
                local_var_code += make_assign(n, init, self.template) + "\n"
        return local_var_code

    def new_variable(self, data_type, id):
        """
        Create a new variable with a name based on the id (number).  Store it to be
        declared with the given data type.  Return the variable's name.
        """
        new_var_name = self.var_name(id)
        self.complexities[0].add_value_dict(data_type, new_var_name)
        return new_var_name

    def get_in_out_var(self, c):
        """Generated names for variables in different cases (in/traversal/out)."""
        in_var = None
        out_var = None
        if c.in_out_var == "in":
            # just change input var name
            self.id_var_in -= 1
            in_var  = self.new_variable(self.input_type, self.id_var_in)
            out_var = self.new_variable(self.input_type, self.id_var_in+1)
        elif c.in_out_var == "out":
            # just change output var name
            in_var = self.new_variable(self.output_type, self.id_var_out)
            self.id_var_out += 1
            out_var = self.new_variable(self.output_type, self.id_var_out)
        elif c.in_out_var == "traversal":
            # change input/output var name
            in_var = self.new_variable(self.input_type, self.id_var_in)
            self.id_var_in -= 1
            out_var = self.new_variable(self.output_type, self.id_var_out)
            self.id_var_out += 1
        return in_var, out_var

# end of complexities_generator.py
