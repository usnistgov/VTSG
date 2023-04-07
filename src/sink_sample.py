"""
sink_sample module

 *modified "Fri Apr  7 16:12:19 2023" *by "Paul E. Black"
"""

from src.sample import Sample


class SinkSample(Sample):  # Load parameters and code beginning and end
    """FiletringSample class

        Args :
            **sample** (xml.etree.ElementTree.Element): The XML element containing \
				the sink tag in the file "sink.xml".

        Attributes :
            **_input_type** (str): Type of input variable (private member, please use getter).

            **_exec_type** (str): Type of exec query if needed (private member, please use getter).

            **_flaw_type** (str): Flaw type (private member, please use getter).

            **_flaw_group** (str): Flaw group.  Empty string means no group \
                                        (private member, please use getter).

    """
    # new sink module in the sink.xml file
    def __init__(self, sample):  # Add parameters showing the beginning and the end of the sample
        Sample.__init__(self, sample, 'sinks')
        self._input_type = sample.find("input_type").text
        if self.input_type is None:
            print(f'[ERROR] Invalid empty <input_type></input_type> in the {self.module_description} sink.')
            print('An input_type is required: it selects filters with matching output_types (or inputs if the filter is "nofilter"). If no filter or input is needed, put "none".')
            exit(1)
        self._exec_type = sample.find("exec_type").text
        if self.exec_type is None:
            print(f'[ERROR] Invalid empty <exec_type></exec_type> in the {self.module_description} sink.')
            print('An exec_type is required: it selects exec queries with matching types. If no exec query is needed, put "none".')
            exit(1)
        self._flaw_type = sample.find("flaw_type").text
        if self.flaw_type is None:
            print(f'[ERROR] Invalid empty <flaw_type></flaw_type> in the {self.module_description} sink.')
            print('A flaw_type string is required; it is used in the name of the generated file.')
            exit(1)
        self._flaw_group = sample.find("flaw_type").get("flaw_group")
        if self._flaw_group is None:
            self._flaw_group = '' # missing flaw_group means no flaw group

    def __str__(self):
        return (f'*** Sink ***\n{super(SinkSample, self)}\n' +
                f'\tinput type: {self._input_type}\n' +
                f'\t exec type: {self._exec_type}\n' +
                f'\t flaw type: {self._flaw_type}\n' +
                f'\tflaw group: {self._flaw_group}\n')

    def needs_exec(self):
        """
        If False, the sink doesn't need an exec query.  Otherwise, it does.
        """
        return self.exec_type != "none"

    @property
    def input_type(self):
        """
        Type of input variable.

        :getter: Returns this input type.
        :type: str
        """
        return self._input_type

    @property
    def exec_type(self):
        """
        Type of exec query if needed.

        :getter: Returns this type.
        :type: str
        """
        return self._exec_type

    @property
    def flaw_type(self):
        """
        Flaw type.

        :getter: Returns this type, e.g., CWE_89, BOF, or STR30-PL
        :type: str
        """
        return self._flaw_type

    @property
    def flaw_group(self):
        """
        Flaw group.

        :getter: Returns this group.
        :type: str
        """
        return self._flaw_group

    def compatible_with_exec_queries(self, exec_queries):
        """
        Return True if current sink is compatible with given exec query, False otherwise.

        Args:
            **exec_queries** (:class:`.ExecQuery`)
        """
        """ Check if current sink is compatible with exec query """
        return self.exec_type == exec_queries.type

# end of sink_sample.py
