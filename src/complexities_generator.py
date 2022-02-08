"""
Complexities Generator Module.

Compose and generate the complexities that will be used by the Generator module.

 *modified "Tue Feb  8 14:52:01 2022" *by "Paul E. Black"
"""

from jinja2 import Template, DebugUndefined
import src.generator
from src.synthesize_code import make_assign


class ComplexitiesGenerator(object):
    """
        Complexities Generator class

            Args :
                **complexities_array** (List of :class:`.ComplexitySample`): Contains the current stack of complexities.

                **template** (str): Template code.

                **input_type** (str): Input type got from the xml file.

                **output_type** (str): Output type got from the xml file.

                **filtering** (str): Current filtering.

            Attributes :

                **complexities_array** (List of :class:`.ComplexitySample`): Contains the current stack of complexities.

                **template** (:class:`.FileTemplate`): Template code.

                **input_type** (str): Input type got from the xml file.

                **output_type** (str): Output type got from the xml file.

                **filtering** (:class:`.FilteringSample`): Current filtering.

                **uid** (int): UID for variables/functions/classes name.

                **complexities** (list of dict): list of dict with complexities, \
                                                 type (function or class) and local var for composition.

                **_executed** (bool): True if the final placeholder will be executed \
                                      (private member, please use getter and setter).

                **id_var_in** (int): ID for intern variables used in composition of complexities (in).

                **id_var_out** (int): ID for intern variables used in composition of cpomplexities (out).

                **_in_ext_name** (str): Name of external intput variable (for input) \
                                        (private member, please use getter and setter).

                **_in_int_name** (str): Name of internal intput variable (for filtering) \
                                        (private member, please use getter and setter).

                **_out_ext_name** (str): Name of external output variable (for sink) \
                                         (private member, please use getter and setter).

                **_out_int_name** (str): Name of internal output variable (for filtering) \
                                         (private member, please use getter and setter).

                **template_code** (str): Modified template.
    """

    def __init__(self, complexities_array, template, input_type, output_type,
                 filtering, language):
        self.complexities_array = complexities_array
        self.template = template
        self.input_type = input_type
        self.output_type = output_type
        self.filtering = filtering
        self.language = language
        self.uid = 0

        self.complexities = []
        self.complexities.append({'type': None, 'code': "{{filtering_content}}", 'local_var': {}, 'name': ""})

        self._executed = True

        self.id_var_in = len(complexities_array)*2
        self.id_var_out = self.id_var_in+1

        self._in_ext_name = None
        self._in_int_name = self.template.prefix + "tainted_"+str(self.id_var_in)
        self._out_ext_name = None
        self._out_int_name = self.template.prefix + "tainted_"+str(self.id_var_out)

        self.add_value_dict(self.input_type, self._in_int_name)
        self.add_value_dict(self.output_type, self._out_int_name)

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
    def executed(self):
        """
        True if placeholder code is executed, false otherwise.

        :getter: Returns this name.
        :type: str
        """
        return self._executed

    def get_template(self):
        """
        Gets modified template.

        :getter: Returns this name.
        :type: str
        """
        return self.template_code

    def compose(self):
        """
        This method composes all complexities.
        """
        for c in reversed(self.complexities_array):
            self._executed = self._executed and c.is_executed()
            # check if complexities is in 2 parts (code and body)
            if c.indirection and c.in_out_var == "traversal":
                t = Template(c.body, undefined=DebugUndefined)
            else:
                t = Template(c.code, undefined=DebugUndefined)
            # generate uid if it's needed

            # if function/class generate a name
            call_name = None
            self.uid = src.generator.Generator.getUID()
            if c.type == "function":
                call_name = "function_"+str(self.uid)
            elif c.type == "class":
                call_name = "Class_"+str(self.uid)

            # create in/out vars
            in_var, out_var = self.get_in_out_var(c)

            # render on code
            self.complexities[0]['code'] = t.render(placeholder=self.complexities[0]['code'], id=self.uid, in_var_name=in_var, out_var_name=out_var, call_name=call_name, in_var_type=self.input_type, out_var_type=self.output_type)

            # traversal for class/function where the placeholder is in the body of function/class
            if c.indirection and c.in_out_var == "traversal":
                # LOCAL VARS
                local_var_code = self.generate_local_var_code(self.complexities[0]['local_var'])
                # put local var on body
                self.complexities[0]['code'] = Template(self.complexities[0]['code'], undefined=DebugUndefined).render(local_var=local_var_code)
                # add in_var
                self.id_var_in -= 1
                in_var = self.template.prefix + "tainted_"+str(self.id_var_in)
                self.add_value_dict(self.input_type, in_var)
                # add out_var
                self.id_var_out += 1
                out_var = self.template.prefix + "tainted_"+str(self.id_var_out)
                self.add_value_dict(self.output_type, out_var)
                # change type of current complexities
                self.complexities[0]['type'] = c.type
                if c.type == "class":
                    self.complexities[0]['type'] = "class_traversal"
                elif c.type == "function":
                    self.complexities[0]['type'] = "function_traversal"
                self.complexities[0]['name'] = call_name
                # ###################################
                # start a new stack of complexities #
                #####################################
                # insert new dict for the next complexity
                self.complexities.insert(0, {'type': None, 'code': c.code, 'local_var': {}, 'name': ""})
                t = Template(c.code, undefined=DebugUndefined)
                self.complexities[0]['code'] = t.render(placeholder=self.complexities[0]['code'], id=self.uid, in_var_name=in_var, out_var_name=out_var, call_name=call_name)
            # in case if the placeholder is before or after the call to class/function
            elif c.indirection and (c.in_out_var == "in" or c.in_out_var == "out"):
                if c.type == "class":
                    body = Template(c.body, undefined=DebugUndefined).render(id=self.uid, in_var_type=self.input_type, out_var_type=self.output_type, call_name=call_name)
                    self.complexities.insert(1, {'type': "class", 'code': body, 'local_var': {}, 'name': call_name})
                elif c.type == "function":
                    body = Template(c.body).render(id=self.uid, in_var_type=self.input_type, out_var_type=self.output_type, call_name=call_name)
                    self.complexities.insert(1, {'type': "function", 'code': body, 'local_var': {}, 'name': call_name})

        return self.fill_template()

    def fill_template(self):
        """
        This method fills template with previous composed complexities with local var and instructions.
        """
        # name of external variable to join with input and sink
        self._in_ext_name = self.template.prefix + "tainted_" + str(self.id_var_in)
        self._out_ext_name = self.template.prefix + "tainted_" + str(self.id_var_out)
        # add to list with local var
        self.add_value_dict(self.input_type, self._in_ext_name)
        self.add_value_dict(self.output_type, self._out_ext_name)

        functions_code = ""
        classes_code = []
        # compose complexity i inti i-1
        for c in reversed(self.complexities[1:]):
            if c['type'] == "class_traversal":
                # add a new class code when we have a traversal class
                imports_content = "\n".join(["using {};".format(import_content) for import_content in sorted(set(self.filtering.imports))])
                classes_code.append({'code': Template(c['code'], undefined=DebugUndefined).render(static_methods=functions_code, imports=imports_content), 'name': c['name']})
                functions_code = ""
            elif c['type'] == "class":
                classes_code.append({'code': c['code'], 'name': c['name']})
            elif c['type'] == "function_traversal":
                functions_code += Template(c['code'], undefined=DebugUndefined).render(static_methods=functions_code)
            elif c['type'] == "function":
                functions_code += c['code'] + "\n\n"

        # generate local vars
        local_var_code = self.generate_local_var_code(self.complexities[0]['local_var'])
        filtering_code = self.complexities[0]['code']
        t = Template(self.template.code, undefined=DebugUndefined)
        # fill template with local vars, complexities and static methods
        self.template_code = t.render(filtering_content=filtering_code, local_var=local_var_code, static_methods=functions_code)
        # return all classes not in the main file
        return classes_code

    def generate_local_var_code(self, local_var):
        '''Generate statement(s) to declare and initialize local variables. For example,
                      "string localvar_1 = None;\nint localvar_2 = 0;"
           There is no indentation (that's done in context) and does not end with a
           new line (so a single statement just drops into a macro place).
        '''
        local_var_code = ""
        # loop through every type
        for t in local_var:
            declare_type = self.template.get_type_var_code(t)
            if declare_type is not None:
                init = self.template.get_init_var_code(t)
                # generate code to declare and initialize each variable of this type
                for n in sorted(list(local_var[t])):
                    # add a space if there is a string to declare the variable
                    if declare_type != "":
                        local_var_code += declare_type + " "
                    local_var_code += make_assign(n, init, self.template) + "\n"
            else:
                local_var_code += "//ERROR UNKNOWN type '" + t + "' "
        return local_var_code

    def add_value_dict(self, key, value):
        """ Adds a variable name into a dict. This dict is compile after for local var """
        dico = self.complexities[0]['local_var']
        if key not in dico:
            dico[key] = set()
        dico[key].add(value)

    def get_in_out_var(self, c):
        """Generated name for variable in different cases (in/traversal/out)."""
        in_var = None
        out_var = None
        if c.in_out_var == "in":
            # just change input var name
            self.id_var_in -= 1
            in_var = self.template.prefix + "tainted_"+str(self.id_var_in)
            out_var = self.template.prefix + "tainted_"+str(self.id_var_in+1)
            self.add_value_dict(self.input_type, in_var)
            self.add_value_dict(self.input_type, out_var)
        elif c.in_out_var == "out":
            # just change output var name
            in_var = self.template.prefix + "tainted_"+str(self.id_var_out)
            self.id_var_out += 1
            out_var = self.template.prefix + "tainted_"+str(self.id_var_out)
            self.add_value_dict(self.output_type, in_var)
            self.add_value_dict(self.output_type, out_var)
        elif c.in_out_var == "traversal":
            # change input/output var name
            in_var = self.template.prefix + "tainted_"+str(self.id_var_in)
            self.id_var_in -= 1
            out_var = self.template.prefix + "tainted_"+str(self.id_var_out)
            self.id_var_out += 1
            self.add_value_dict(self.input_type, in_var)
            self.add_value_dict(self.output_type, out_var)
        return in_var, out_var
