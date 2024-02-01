"""
file_manager module

 *modified "Thu Feb  1 12:12:59 2024" *by "Paul E. Black"
"""

import os

def flaw_group_dir_path(dir_name, flaw_group):
    '''
    Return the path to the directory for the flaw group passed
    '''
    return os.path.join(dir_name, flaw_group)

class FileManager(object):
    """FileManager class

        Args :
            **filename** (str): The filename of the test case.

            **dir_name** (str): The directory of the test case.

            **flaw_group** (str): Flaw group of the test case.

            **flaw_type** (str): Flaw type of the test case.

            **is_safe** (bool): If true the the test case is safe.

            **content** (str): Code of the test case.

        Attributes :
            **filename** (str): The filename of the test case.

            **dir_name** (str): The directory of the test case.

            **flaw_group** (str): Flaw group of the test case.

            **flaw_type** (str): Flaw type of the test case.

            **is_safe** (bool): If true the the test case is safe.

            **content** (str): Code of the test case.

            **path** (str): Path to the test case.
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
        Create the test case file with code in it

        Args :
            **debug** (bool) : Debug flag (default : False)
        """
        # create the directory if it doesn't exist
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        file_path = os.path.join(self.path, self.filename)
        # make sure we don't overwrite an existing file (or directory)
        if os.path.exists(file_path):
            print(f'[ERROR] trying to overwrite existing file: {file_path}')
            print('Probably duplicate <dir></dir> strings')
            exit(1)
        # create the file
        createdFile = open(file_path, "w")
        # write code
        createdFile.write(self.content)
        createdFile.close()

    def getPath(self):
        """
        Returns the path.
        """
        return self.path

def get_XML_file(modules, template_directory, language):
    """
    Return the path to xml file for the named modules for the specified language.
    """
    _xml = {
        "inputs": "inputs.xml",
        "filters": "filters.xml",
        "sinks": "sinks.xml",
        "exec_queries": "exec_queries.xml",
        "file_template": "file_template.xml",
        "complexities": "complexities.xml",
    }

    return os.path.join(template_directory, language, _xml[modules])

# end of file_manager.py
