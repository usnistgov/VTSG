"""
Condition module
"""

class ConditionSample(object):
    """ConditionSample class

        Args :
            **xml_cond** (xml.etree.ElementTree.Element): The XML element containing the conditions tag in the \
                                                          file "complexities.xml".

        Attributes :
            **_id** (str): ID of the condition (private member, please use getter and setter).

            **_code** (str): Code of condition (private member, please use getter and setter).

            **_value** (str): Value of condition (private member, please use getter and setter).
    """

    def __init__(self, xml_cond):
        self._id = xml_cond.get("id")
        self._code = xml_cond.find("code").text
        self._value = xml_cond.find("value").text.lower() == "true"

    @property
    def id(self):
        """
        ID of the condition.

        :getter: Returns this ID.
        :type: str
        """
        return self._id

    @property
    def code(self):
        """
        Code of condition.

        :getter: Returns this code.
        :type: str
        """
        return self._code

    @property
    def value(self):
        """
        Value of condition.

        :getter: Returns this value.
        :type: str
        """
        return self._value
