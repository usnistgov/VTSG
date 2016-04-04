"""
sample module
"""

import c_sharp_vuln_test_suite_gen.generator


class Sample(object):
    """Sample class

        Args :
            **sample** (xml.etree.ElementTree.Element): The XML element containing the filtering tag in the \
                                                          file "filtering.xml".

        Attributes :
            **_path** (str): path for identify the sample (private member, please use getter and setter).

            **_code** (str): Code of sample (private member, please use getter and setter).

            **_comment** (str): comment for sample (private member, please use getter and setter).

            **_imports** (list of str): path for identify the sample (private member, please use getter and setter).

            **_need_id** (bool): True if sample need id for code chunk (private member, please use getter and setter).

            **_safe** (bool): Safe tag (private member, please use getter and setter).

            **_unsafe** (bool): Unsafe tag (private member, please use getter and setter).


    """

    def __init__(self, sample):
        self._path = []
        tree_path = sample.find("path").findall("dir")
        for dir in tree_path:
            self.path.append(dir.text)

        self._code = sample.find("code").text

        self._comment = sample.find("comment").text
        self._imports = []
        if sample.find("imports") is not None:
            self._imports = [imp.text for imp in sample.find("imports").findall("import")]

        self._need_id = False
        if sample.get("need_id") == "1":
            self._need_id = True

        self._safe = False
        self._unsafe = False
        if sample.find("safety") is not None:
            self._safe = sample.find("safety").get("safe") == "1"
            self._unsafe = sample.find("safety").get("unsafe") == "1"

    def __str__(self):
        return "\tpath : {}\n\tcomment : {}\n\timports : {}\
                ".format(self.path,
                         self.comment,
                         self.code,
                         self.imports)

    @property
    def safe(self):
        """
        Safe Tag.

        :getter: Returns this boolean.
        :type: bool
        """
        return self._safe

    @property
    def code(self):
        """
        Code Tag.

        :getter: Returns this tag.
        :type: str
        """
        return self._code

    @property
    def unsafe(self):
        """
        Unsafe Tag.

        :getter: Returns this boolean.
        :type: bool
        """
        return self._unsafe

    @property
    def need_id(self):
        """
        Need_ID Tag.

        :getter: Returns this boolean.
        :type: bool
        """
        return self._need_id

    def generate_file_name(self):
        """
        Generate the filename with the path of the Manifest.
        """
        name = ""
        for directory in self.path:
            name += directory+"-"
        name = name[:-1]
        return name

    @property
    def path(self):
        """
        Path Tag.

        :getter: Returns this tag.
        :type: str
        """
        return self._path

    @property
    def imports(self):
        """
        Imports Tag.

        :getter: Returns this tag.
        :setter: Sets this tag.
        :type: str
        """
        return self._imports

    @imports.setter
    def imports(self, value):
        self._imports = value

    @property
    def comment(self):
        """
        Comment Tag.

        :getter: Returns this tag.
        :type: str
        """
        return self._comment
