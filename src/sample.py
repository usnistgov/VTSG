"""
sample module

 *modified "Thu Nov  3 11:22:00 2022" *by "Paul E. Black"
"""

import src.generator


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

    def __init__(self, sample, file_name):
        self._path = []
        tree_path = sample.find("path").findall("dir")
        for dir in tree_path:
            if dir.text is None:
                print(f'[ERROR] Invalid empty <dir></dir> in the {file_name} file.')
                print('A dir string is required; it is used in the name of the generated file.')
                exit(1)
            self.path.append(dir.text)

        self._code = sample.find("code").text

        if sample.find("comment") is not None:
            self._comment = sample.find("comment").text
        else:
            self._comment = ''

        self._imports = []
        if sample.find("imports") is not None:
            self._imports = [imp.text for imp in sample.find("imports").findall("import")]
            if None in self._imports:
                print(f'[ERROR] Invalid empty <import></import> in the {file_name} file.')
                print('An import is required; it is used in the file template {{stdlib_imports}} section. If this needs no imports, remove <imports></imports>.')
                exit(1)

        self._need_id = False
        if sample.get("need_id") == "1":
            self._need_id = True

        self._safe = False
        self._unsafe = False
        if sample.find("safety") is not None:
            self._safe = sample.find("safety").get("safe") == "1"
            self._unsafe = sample.find("safety").get("unsafe") == "1"

    def __str__(self):
        return (f'\tpath: {self.path}\n' +
                f'\tcomment: {self.comment}\n' +
                f'\tcode: {self.code}\n' +
                f'\timports: {self.imports}')

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

    def module_description(self):
        """
        Return the description of this module.
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
