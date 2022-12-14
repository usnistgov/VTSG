"""
Input Class (TODO DOC)

 *modified "Wed Dec 14 09:38:35 2022" *by "Paul E. Black"
"""

from src.sample import Sample


class InputSample(Sample):  # Initialize the type of input and the code parameters of the class
    """InputSample class

        Args :
            **sample** (xml.etree.ElementTree.Element): The XML element containing the input tag in the \
                                                          file "input.xml".

        Attributes :
            **_input_type** (str): Type of input variable (private member, please use
            getter.  Read only).

            **_output_type** (str): Type of output variable (private member, please
              use getter.  Read only).

            **_flaws** (dict str->(dict str->bool): Collection of flaws for this filter with safety \
                                          (private member, please use getter.  Read only).
    """

    # compatible with new structure
    def __init__(self, sample):  # XML tree in parameter
        Sample.__init__(self, sample, 'inputs')
        self._input_type = sample.find("input_type").text
        self._output_type = sample.find("output_type").text
        self._flaws = {}
        for flaw in sample.find("flaws").findall("flaw"):
            flaw_type = flaw.get("flaw_type")
            self._flaws[flaw_type] = {}
            self._flaws[flaw_type]["safe"] = (flaw.get("safe") == "1")
            self._flaws[flaw_type]["unsafe"] = (flaw.get("unsafe") == "1")

    def __str__(self):
        return (f'*** Input ***\n{super(InputSample, self)}\n' +
                f'\t input type: {self._input_type}\n' +
                f'\toutput type: {self._output_type}\n' +
                f'\tflaws: {self._flaws}\n\n')

    def is_safe(self, flaw_type):
        """ Check if current input is safe for a flaw type """
        if flaw_type in self.get_flaws_types():
            return self.flaws[flaw_type]["safe"]
        if "default" in self.get_flaws_types():
            return self.flaws["default"]["safe"]
        return None

    def is_unsafe(self, flaw_type):
        """ Check if current input is unsafe for a flaw type """
        if flaw_type in self.get_flaws_types():
            return self.flaws[flaw_type]["unsafe"]
        if "default" in self.get_flaws_types():
            return self.flaws["default"]["unsafe"]
        return None

    @property
    def input_type(self):
        """
        Type of input variable.

        :getter: Returns this input type.
        :type: str
        """
        return self._input_type

    @property
    def output_type(self):
        """
        Type of output variable.

        :getter: Returns this output type.
        :type: str
        """
        return self._output_type

    def compatible_with_filter_sink(self, filter, sink):
        """
        Return True if current input is compatible with filter and sink, False otherwise.

        Args:
            **sink** (SinkSample)

            **filter** (FilterSample)
        """
        if filter.input_type != "nofilter":
            return self.output_type == filter.input_type
        else:
            return self.output_type == sink.input_type

    @property
    def flaws(self):
        """
        Collection of flaws for this input with safety.

        :getter: Returns this collection.
        :type: str
        """
        return self._flaws

    def get_flaws_types(self):
        """
        Collection of flaws for this input with safety.

        :getter: Returns the keys of this collection.
        :type: list of str
        """
        return self.flaws.keys()
