"""
Complexity module.

"""

import copy
import c_sharp_vuln_test_suite_gen.generator


class ComplexitySample(object):
    """ComplexitySample class

        Attributes :
            **_id** (str): ID of complexity (private member, please use getter and setter).

            **_cond_id** (int): ID of condition (private member, please use getter and setter).

            **_code** (str): Code of complexity (private member, please use getter and setter).

            **_type** (str): Type of complexity (if, switch, for, function, classe, ...) \
                             (private member, please use getter and setter).

            **_group** (str): Group of complexity (conditionnals, loops, functions, classes, ...) \
                              (private member, please use getter and setter).

            **_executed** (str): If True the placeholder is executed (private member, please use getter and setter).

            **_need_condition** (bool): If True the complexity need a condition (set _cond_id) \
                                        (private member, please use getter and setter).

            **_need_id** (bool): If True the complexity needs uniq id (private member, please use getter and setter).

            **_in_out_var** (bool): Specifies where the placeholder is in the complexity for variables name setting \
                                    (in, trasversal, out)

            **_indirection** (bool): If True, the complexity need to have a body \
                                    (private member, please use getter and setter).

            **_body** (str): If specified, it's the second part of complexity \
                             (private member, please use getter and setter).
    """

    def __init__(self, xml_compl):
        self._id = xml_compl.get("id")
        self._cond_id = None
        self._code = xml_compl.find("code").text
        self._code = c_sharp_vuln_test_suite_gen.generator.Generator.remove_indent(self._code)
        self._type = xml_compl.get("type").lower()
        self._group = xml_compl.get("group").lower()
        self._executed = xml_compl.get("executed").lower()
        self._need_condition = False
        if "condition" in self._executed or self._type == "if" or xml_compl.get("need_condition") == "1":
            self._need_condition = True
        self._need_id = False
        if xml_compl.get("need_id") == "1":
            self._need_id = True
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
            self._body = c_sharp_vuln_test_suite_gen.generator.Generator.remove_indent(self._body)


    def __str__(self):
        return "*** Complexity ***\n\ttype : {}\n\tgroup : {}\n\texecuted : {}\n\tcode : {}\n\
            \n".format(self.type,
                       self.group,
                       self.is_executed(),
                       self.code)

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

    def set_cond_id(self, nb):
        """
        Sets the ID of the condition.

        Args:
            **nb** (int): The new value.
        """
        self._cond_id = nb

    @property
    def body(self):
        """
        Second part of complexity.

        :getter: Returns this second part.
        :setter: Sets this second part.
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

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def in_out_var(self):
        return self._in_out_var

    @property
    def need_id(self):
        """
        If True the complexity needs uniq id.

        :getter: Returns this boolean.
        :type: bool
        """
        return self._need_id

    def need_condition(self):
        """
        If True the complexity need a condition (set _cond_id).

        :getter: Returns this boolean.
        :type: bool
        """
        return self._need_condition

    def set_condition(self, condition):
        """
        If True the complexity need a condition (set _cond_id).

        :setter: Sets this boolean.
        :type: bool
        """
        self.condition = condition

    @property
    def type(self):
        """
        Type of complexity (if, switch, for, function, classe, ...).

        :getter: Returns this type.
        :type: str
        """
        return self._type

    @property
    def group(self):
        """
        Group of complexity (conditionnals, loops, functions, classes, ...).

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

    def is_executed(self):
        """ compute if the placeholder is executed"""
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
