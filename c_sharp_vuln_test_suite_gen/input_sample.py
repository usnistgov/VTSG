"""
Input Class (TODO DOC)
"""

from c_sharp_vuln_test_suite_gen.sample import Sample


class InputSample(Sample):  # Initialize the type of input and the code parameters of the class
    """FiletringSample class

        Args :
            **sample** (xml.etree.ElementTree.Element): The XML element containing the input tag in the \
                                                          file "input.xml".

        Attributes :
            **_input_type** (str): Type of input variable (private member, please use getter and setter).

            **_output_type** (str): Type of output variable (private member, please use getter and setter).

            **_flaws** (dict str->(dict str->bool): Collection of flaws for this filtering with safety \
                                                    (private member, please use getter and setter).
    """

    # compatible with new structure
    def __init__(self, sample):  # XML tree in parameter
        Sample.__init__(self, sample)
        self._input_type = sample.find("input_type").text.lower()
        self._output_type = sample.find("output_type").text.lower()
        self._flaws = {}
        for flaw in sample.find("flaws").findall("flaw"):
            flaw_type = flaw.get("flaw_type").lower()
            self._flaws[flaw_type] = {}
            self._flaws[flaw_type]["safe"] = (flaw.get("safe") == "1")
            self._flaws[flaw_type]["unsafe"] = (flaw.get("unsafe") == "1")

    def __str__(self):
        return "*** Input ***\n{}\n\tinput type : {}\n\toutput type : {}\n\tflaws : {}\n\tcode : {}\n\
            \n".format(super(InputSample, self).__str__(),
                       self.input_type,
                       self.output_type,
                       self.flaws)

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

    def compatible_with_filtering_sink(self, filtering, sink):
        """
        Return True if current input is compatible with filtering and sink, False otherwise.

        Args:
            **sink** (SinkSample)

            **filtering** (FilteringSample)
        """
        if filtering.input_type != "nofilter":
            return self.output_type == filtering.input_type
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
