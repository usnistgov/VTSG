"""
filtering_sample module
"""

from c_sharp_vuln_test_suite_gen.sample import Sample


class FilteringSample(Sample):  # Initialize rules, safety, code and escape
    """FiletringSample class

        Args :
            **sample** (xml.etree.ElementTree.Element): The XML element containing the filtering tag in the \
                                                          file "filtering.xml".

        Attributes :
            **_input_type** (str): Type of input variable (private member, please use getter and setter).

            **_output_type** (str): Type of output variable (private member, please use getter and setter).

            **_flaws** (dict str->(dict str->bool): Collection of flaws for this filtering with safety \
                                                    (private member, please use getter and setter).
    """

    # new version for new XML
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
            # optional attr: self.flaws[flaw_type]["attr"] = option["attr"] if "attr" in option["attr"] else None

    def __str__(self):
        return "*** Filtering ***\n{}\n\tinput type : {}\n\toutput type : {}\n\tflaws : {}\n\tcode : {}\n\
            \n".format(super(FilteringSample, self).__str__(),
                       self.input_type,
                       self.output_type,
                       self.flaws)

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

    @property
    def flaws(self):
        """
        Collection of flaws for this filtering with safety.

        :getter: Returns this collection.
        :type: str
        """
        return self._flaws

    def get_flaws_types(self):
        """
        Collection of flaws for this filtering with safety.

        :getter: Returns the keys of this collection.
        :type: list of str
        """
        return self.flaws.keys()

    def contains_flaw_type(self, flaw_type):
        """
        Returns True if the flaws of the filtering sample is the same as the given one or if it's a generic filtering, \
        False otherwise.

        Args:
            **flaw_type** (str)
        """
        return "all" in self.flaws.keys() or flaw_type in self.flaws

    def is_safe(self, flaw_type):
        """
        Check if current filtering is safe for the given flaw type.

        Args:
            **flaw_type** (str)
        """
        if flaw_type in self.get_flaws_types():
            return self.flaws[flaw_type]["safe"]
        if "all" in self.get_flaws_types():
            return self.flaws["all"]["safe"]
        return None

    def is_unsafe(self, flaw_type):
        """
        Check if current filtering is unsafe for the given flaw type.

        Args:
            **flaw_type** (str)
        """
        if flaw_type in self.get_flaws_types():
            return self.flaws[flaw_type]["unsafe"]
        if "all" in self.get_flaws_types():
            return self.flaws["all"]["unsafe"]
        return None

    def compatible_with_sink(self, sink_sample):
        """
        Return True if current filtering is compatible with given sink, False otherwise.

        Args:
            **sink_sample** (:class:`.SinkSample`)
        """
        return (self.output_type == sink_sample.input_type or self.output_type == "nofilter") and \
            self.contains_flaw_type(sink_sample.flaw_type)
