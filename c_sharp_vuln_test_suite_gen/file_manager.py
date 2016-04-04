"""
file_manager module
"""

import os


class FileManager(object):
    """FileManager class

        Args :
            **filename** (str): The filename of current test case.

            **dir_name** (str): The directory of current test case.

            **flaw_group** (str): Flaw group of current test case.

            **flaw_type** (str): Flaw type of current test case.

            **is_safe** (bool): If true the current test case is safe.

            **content** (str): Code of current test case.

        Attributes :
            **filename** (str): The filename of current test case.

            **dir_name** (str): The directory of current test case.

            **flaw_group** (str): Flaw group of current test case.

            **flaw_type** (str): Flaw type of current test case.

            **is_safe** (bool): If true the current test case is safe.

            **content** (str): Code of current test case.

            **path** (str): Path of current test case.
    """

    def __init__(self, filename, dir_name, flaw_group, flaw_type, is_safe, content):
        self.filename = filename
        self.dir_name = dir_name
        self.flaw_group = flaw_group
        self.flaw_type = flaw_type
        self.safe = "safe" if is_safe else "unsafe"
        self.content = content
        self.path = os.path.join(dir_name, flaw_group, flaw_type, self.safe, '')

    def createFile(self, debug=False):
        """
        Create the file with code on them

        Args :
            **debug** (bool) : Debug flag (default : False)
        """
        # check if the directory exists
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        # create the file
        file_path = os.path.join(self.path, self.filename)
        createdFile = open(file_path, "w")
        # write code
        createdFile.write(self.content)
        createdFile.close()

        if debug:
            print("file : "+self.filename+" created")

    _xml = {
        "input": "input.xml",
        "filtering": "filtering.xml",
        "sink": "sink.xml",
        "exec_queries": "exec_queries.xml",
        "file_template": "file_template.xml",
        "complexities": "complexities.xml",
    }

    @classmethod
    def exist_language(cls, language):
        """
        Class Method.
        Check if the given language exist in the path.

        Args :
            **language** (str): The language to check.
        """
        res = True
        path = os.path.abspath(os.path.join("./c_sharp_vuln_test_suite_gen", "templates", language))
        if not os.path.isdir(path):
            print("[ERROR] Language don't exists")
            res = False
        else:
            if not os.path.isfile(os.path.join(path, FileManager._xml["file_template"])):
                print("[ERROR] Template file don't exists")
                res = False

            if not os.path.isfile(os.path.join(path, FileManager._xml["input"])):
                print("[ERROR] Input file don't exists")
                res = False
            if not os.path.isfile(os.path.join(path, FileManager._xml["filtering"])):
                print("[ERROR] Filtering file don't exists")
                res = False
            if not os.path.isfile(os.path.join(path, FileManager._xml["sink"])):
                print("[ERROR] Sink file don't exists")
                res = False
            if not os.path.isfile(os.path.join(path, FileManager._xml["exec_queries"])):
                print("[ERROR] Exec Querie file don't exists")
                res = False
            if not os.path.isfile(os.path.join(path, FileManager._xml["complexities"])):
                print("[ERROR] Complexities file don't exists")
                res = False
        return res

    @classmethod
    def getXML(cls, xmlfile, language="cs"):
        """
        Class Method.
        Returns the path to selected xml file for the specified language.
        """
        return os.path.join("c_sharp_vuln_test_suite_gen", "templates", language, cls._xml[xmlfile])

    # Getters and setters
    def setPath(self, path):
        """
        Sets the path.

        Args:
            **path** (str): The new path.
        """
        self.path = path

    def addPath(self, path):
        """
        Adds the given path to the attribute path.

        Args:
            **path** (str): the path to add.
        """
        self.path = os.path.join(self.path, path)

    def getPath(self):
        """
        Returns the path.
        """
        return self.path

    def setName(self, filename):
        """
        Sets the filename.

        Args:
            **filename** (str): The new filename.
        """
        self.filename = filename

    def getName(self):
        """
        Returns the filename.
        """
        return self.filename

    def addContent(self, content):
        """
        Concatenates the given content to the attribute content.

        Args:
            **content** (str): The content to add.
        """
        self.content += content
