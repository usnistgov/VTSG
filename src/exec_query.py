"""
exec_query module

 *modified "Mon Nov 14 16:41:47 2022" *by "Paul E. Black"
"""

from src.sample import Sample


class ExecQuerySample(Sample):
    """ExecQuerySample class

        Args :
            **sample** (xml.etree.ElementTree.Element): The XML element containing the execquery tag in the \
                                                          file "exec_query.xml".

        Attributes :
            **_type** (str): Type of exec query (private member, please use getter and setter).

            **_code** (str): Code of exec query (private member, please use getter and setter).

            **_safe** (bool): If True the exec query is safe (private member, please use getter and setter).
    """

    # new version for new XML
    def __init__(self, sample):  # XML tree in parameter
        Sample.__init__(self, sample, 'exec_queries')
        self._type = sample.get("type")
        self._code = sample.find("code").text
        self._safe = sample.get("safe") == "1"

    def __str__(self):
        return (f'*** ExecQuery ***\n' +
                f'\ttype: {self._type}\n' +
                f'\tsafe: {self._safe}\n' +
                f'\tcode: {self._code}\n\n')

    @property
    def type(self):
        """
        type of exec query.

        :getter: Returns this type.
        :type: str
        """
        return self._type

    @property
    def code(self):
        """
        Code of exec query.

        :getter: Returns this code.
        :type: str
        """
        return self._code

    @property
    def safe(self):
        """
        If True the exec query is safe.

        :getter: Returns this boolean.
        :type: bool
        """
        return self._safe
