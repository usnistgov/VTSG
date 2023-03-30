"""
filter_sample module

 *modified "Thu Mar 30 10:35:41 2023" *by "Paul E. Black"
"""

from src.sample import Sample
import re

class FilterSample(Sample):  # Initialize rules, safety, code and escape
    """FilterSample class

        Args :
            **sample** (xml.etree.ElementTree.Element): The XML element containing
		the filter tag in the file "filters.xml".

        Attributes :
            **_input_type** (str): Type of input variable (private member, please use getter).

            **_output_type** (str): Type of output variable (private member, please use getter).

            **_flaws** (dict str->(dict str->bool): Collection of flaws for this
                filter with safety (private member, please use getter).
    """

    def __init__(self, sample):  # XML tree in parameter
        Sample.__init__(self, sample, 'filters')
        self._input_type = sample.find("input_type").text
        self._output_type = sample.find("output_type").text
        self._flaws = {}
        for flaw in sample.find("flaws").findall("flaw"):
            flaw_type = flaw.get("flaw_type")
            self._flaws[flaw_type] = {}
            self._flaws[flaw_type]["safe"] = (flaw.get("safe") == "1")
            self._flaws[flaw_type]["unsafe"] = (flaw.get("unsafe") == "1")
            # optional attr: self.flaws[flaw_type]["attr"] = option["attr"] if "attr" in option["attr"] else None
        # Below is only an approximate test.  Every filter that is used must assign
        # value to {{out_var_name}} in every execution path.  However, this test
        # would not warn if the string was in a comment, a value was not be assigned
        # in some paths, etc.  A comprehensive test requires semantic anaylsis.
        if re.search('out_var_name', self.code) is None:
            print('[WARNING] no {{out_var_name}} in the <code> of filter "'
                  + str(self.module_description) +
                  '".  {{out_var_name}} must be assigned a value in all execution paths.')
            # Maybe there are legitimate filters with no {{out_var_name}}, so no exit

    def __str__(self):
        return (f'*** Filter ***\n{super(FilterSample, self)}\n' +
                f'\t input type: {self._input_type}\n' +
                f'\toutput type: {self._output_type}\n' +
                f'\tflaws: {self._flaws}\n\n')

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
        Collection of flaws for this filter with safety.

        :getter: Returns this collection.
        :type: str
        """
        return self._flaws

    def get_flaws_types(self):
        """
        Collection of flaws for this filter with safety.

        :getter: Returns the keys of this collection.
        :type: list of str
        """
        return self.flaws.keys()

    def contains_flaw_type(self, flaw_type):
        """
        Return True if the given flaw is in this filter's list of flaws or if has a
        generic flaw type.
        False otherwise.

        Args:
            **flaw_type** (str)
        """
        return "default" in self.flaws.keys() or flaw_type in self.flaws

    def is_safe(self, flaw_type):
        """
        Check if current filter is safe for the given flaw type.

        Args:
            **flaw_type** (str)
        """
        if flaw_type in self.get_flaws_types():
            return self.flaws[flaw_type]["safe"]
        if "default" in self.get_flaws_types():
            return self.flaws["default"]["safe"]
        return None

    def is_unsafe(self, flaw_type):
        """
        Check if current filter is unsafe for the given flaw type.

        Args:
            **flaw_type** (str)
        """
        if flaw_type in self.get_flaws_types():
            return self.flaws[flaw_type]["unsafe"]
        if "default" in self.get_flaws_types():
            return self.flaws["default"]["unsafe"]
        return None

    def compatible_with_sink(self, sink_sample):
        """
        Return True if current filter is compatible with given sink, False otherwise.

        Args:
            **sink_sample** (:class:`.SinkSample`)
        """
        return (self.output_type == sink_sample.input_type or self.output_type == "nofilter") and \
            self.contains_flaw_type(sink_sample.flaw_type)

# end of filter_sample.py
