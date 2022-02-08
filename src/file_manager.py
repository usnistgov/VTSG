"""
file_manager module

 *modified "Tue Feb  8 16:49:02 2022" *by "Paul E. Black"
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
        Does a directory for given language exists in the expected place?

        Args :
            **language** (str): The language to check.
        """
        path = os.path.abspath(os.path.join("./src", "templates", language))
        if not os.path.isdir(path):
            print(f'[ERROR] no directory found for {language}')
            return False

        return True

    @classmethod
    def getXML(cls, xmlfile, language):
        """
        Class Method.
        Returns the path to selected xml file for the specified language.
        """
        return os.path.join("src", "templates", language, cls._xml[xmlfile])

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
