"""
Complexity module.

 *modified "Tue Jan 23 10:38:19 2024" *by "Paul E. Black"
"""

import copy
import src.generator
from src.sample import get_imports


class ComplexitySample(object):
    """ComplexitySample class

        Attributes :
            **_id** (str): ID of complexity (private member, please use getter).

            **_code** (str): Code of complexity (private member, please use getter and setter).

            **_imports** (list of str): names to be imported.

            **_type** (str): Type of complexity (if, switch, for, function, class, ...) \
                             (private member, please use getter).

            **_group** (str): Group of complexity (conditionals, loops, functions, classes, ...) \
                              (private member, please use getter).

            **_executed** (str): The situation when the placeholder code is executed:
              one of "condition" (executed if the condition evaluates to True),
              "not_condition" (executed if the condition is False), "1" (always
              executed), or "0" (never executed).  (private member, please use getter).

            **_needs_condition** (bool): If True the complexity need a condition (set _cond_id) \
                                        (private member, please use getter).

            **_needs_id** (bool): If True the complexity needs unique id
					(private member, please use getter).

            **_in_out_var** (bool): Specifies where the placeholder is in the complexity for variables name setting \
                                    (in, transversal, out)

            **_indirection** (bool): If True, the complexity need to have a body \
                                    (private member, please use getter).

            **_body** (str): If specified, it's the second part of complexity \
                             (private member, please use getter).

            # the following attributes pertain to the condition used during generation

            **_cond_id** (str): ID of condition
					(private member, please use getter and setter).

            **_condition** (bool): The value that this condition evaluates to.
			For example, 1==1 is always True and (4+2>=42) is always False.
					(private member, please use getter and setter).

            **_cond_imports** (list of str): names this condition needs to be imported.
					(private member, please use getter and setter).

    """

    def __init__(self, xml_compl):
        self._id = xml_compl.get("id")
        self._cond_id = None
        self._cond_imports = []
        self._code = xml_compl.find("code").text
        self._code = src.generator.Generator.remove_indent(self._code)
        self._imports = get_imports(xml_compl, "complexities.xml")
        self._type = xml_compl.get("type")
        self._group = xml_compl.get("group")
        self._executed = xml_compl.get("executed")
        assert self._executed in {'condition', 'not_condition', '1', '0'}, '[ERROR] executed must be "condition", "not_condition", "1", or "0"'
        self._needs_condition = False
        if "condition" in self._executed or xml_compl.get("need_condition") == "1":
            self._needs_condition = True
        self._needs_id = False
        if xml_compl.get("needs_id") == "1":
            self._needs_id = True
        self._in_out_var = False
        if xml_compl.get("in_out_var"):
            self._in_out_var = xml_compl.get("in_out_var")
        self._indirection = False
        if xml_compl.get("indirection"):
            self._indirection = xml_compl.get("indirection") == "1"
        # TODO check if indirection is True, complexity need to have a body
        self._body = ""
        if xml_compl.find("body") is not None:
            self._body = xml_compl.find("body").text
            if self._body is None:
                print(f'[ERROR] Invalid empty <body></body> in the complexities file.')
                print('If no additional body of code is needed, remove <body></body>.')
                exit(1)
            self._body = src.generator.Generator.remove_indent(self._body)


    def __str__(self):
        return (f'*** Complexity ***\n' +
                f'\ttype: {self._type}\n' +
                f'\tgroup: {self._group}\n' +
                f'\texecuted: {self._executed}\n' +
                f'\tcode: {self._code}\n')

    @property
    def id(self):
        """
        ID of complexity.

        :getter: Returns this ID.
        :type: int
        """
        return self._id

    def get_complete_id(self):
        """ Returns the complete id of complexity (in case with conditional). """
        if self._cond_id:
            return self._id+"."+self._cond_id
        else:
            return self._id

    # these handle data about the condition used in this complexity during generation

    @property
    def cond_id(self):
        return self._cond_id

    def set_cond_id(self, nb):
        """
        Sets the ID of the condition.

        Args:
            **nb** (str): The new value.
        """
        self._cond_id = nb

    @property
    def condition(self):
        """
        The value of what the condition used for this complexity evaluates to.

        :getter: Returns the condition.
        :type: bool
        """
        return self._condition

    def set_condition(self, condition):
        """
        Set the value of what the condition used for this complexity evaluates to.
        For example, 1==1 is always True and (4+2>=42) is always False.

        :setter: Sets the evaluated value of the condition used for this complexity.
        :type: bool
        """
        assert type(condition) is bool
        self._condition = condition

    @property
    def cond_imports(self):
        """
        Names that the condition used for this complexity needs to be imported.

        :getter: Returns the condition.
        :type: list of str
        """
        return self._cond_imports

    def set_cond_imports(self, imports):
        """
        Set the names of imports that the condition used during generation for this
        complexity needs.

        :setter: Sets the list of imports.
        :type: list of str
        """
        assert type(imports) is list
        self._cond_imports = imports

    @property
    def body(self):
        """
        Second part of complexity.

        :getter: Returns this second part.
        :type: str
        """
        return self._body

    @property
    def indirection(self):
        """
        If True, the complexity need to have a body.

        :getter: Returns this boolean.
        :type: bool
        """
        return self._indirection

    @property
    def in_out_var(self):
        return self._in_out_var

    @property
    def need_id(self):
        """
        If True the complexity needs unique id.

        :getter: Returns this boolean.
        :type: bool
        """
        return self._needs_id

    def need_condition(self):
        """
        True if this complexity needs a condition. (set _cond_id to indicate which
        condition is used.)

        :getter: Returns this boolean.
        :type: bool
        """
        return self._needs_condition

    @property
    def type(self):
        """
        Type of complexity (if, switch, for, function, class, ...).

        :getter: Returns this type.
        :type: str
        """
        return self._type

    @property
    def group(self):
        """
        Group of complexity (conditionals, loops, functions, classes, ...).

        :getter: Returns this group.
        :type: str
        """
        return self._group

    @property
    def code(self):
        """
        Code of complexity.

        :getter: Returns this code.
        :setter: Sets this code.
        :type: str
        """
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def imports(self):
        """
        List of imports that this complexity needs.

        :getter: Returns this list.
        :type: list of str
        """
        return self._imports

    def is_executed(self):
        """ True if the placeholder code is executed"""
        if self._executed == "condition":
            return self.condition
        elif self._executed == "not_condition":
            return not self.condition
        elif self._executed == "1":
            return True
        elif self._executed == "0":
            return False
        return False

    def clone(self):
        return copy.deepcopy(self)

# end of complexity.py
