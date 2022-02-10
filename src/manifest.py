"""
manifest

Write the manifest of test cases.

 *modified "Thu Feb 10 12:41:14 2022" *by "Paul E. Black"
"""

import os
import time
from src.file_manager import flaw_group_dir_path

class Manifest(object):
    """Manifest class

        Attributes :
            **dir_name** (str): Directory name.

            **date** (str): Date of generation.

            **manifest** (str): List of open manifest for each group generated.

            **author** (str): Author(s) of cases.  From file_author.txt

    """

    def __init__(self, dir_name, date):
        self.dir_name = dir_name
        self.date = date
        self.manifest = {}
        self.author = open("src/templates/file_author.txt").read().strip()

    def createManifests(self, flaw_groups):
        """
        Create a manifest for selected group.

        Args:
            **flaw_groups** (list of str): List of flaw group
        """
        for flaw_group in flaw_groups:
            path = flaw_group_dir_path(self.dir_name, flaw_group)
            if not os.path.exists(path):
                os.makedirs(path)
            self.manifest[flaw_group] = open(os.path.join(path, "manifest.xml"), "w+")
        for group in self.manifest:
            self.manifest[group].write("<container>\n")

    def addTestCase(self, input_sample, flaw_group, flaw, files_path, language):
        """
        Add test case into manifest

        Args :
            **input_sample** (str)

            **flaw_group** (str)

            **flaw** (str)

            **files_path** (list of dict str->str)

            **language** (str)
        """
        reformated_date = time.strftime("%Y-%m-%d", time.strptime(self.date, "%m-%d-%Y_%Hh%Mm%S"))
        # meta data for current test case
        meta_data = ('\t<testcase>\n' +
                     '\t\t<meta-data>\n' +
                     f'\t\t\t<author>{self.author}</author>\n' +
                     f'\t\t\t<date>{reformated_date}</date>\n' +
                     f'\t\t\t<input>{input_sample}</input>\n'
                     '\t\t</meta-data>\n\n')
        # write meta data
        self.manifest[flaw_group].write(meta_data)
        file_block = ""
        for f in files_path:
            file_path = f['path']
            file_block += f'\t\t<file path="{file_path}" language="{language}"' # no >
            flaw_line = f['line']
            if flaw_line == 0:
                # no flaw line
                file_block += '/>'
            else:
                file_block += '>\n'
                file_block += f'\t\t\t<flaw line="{flaw_line}" name ="{flaw}"/>\n'
                file_block += '\t\t</file>'
            file_block += '\n\n'

        self.manifest[flaw_group].write(file_block)
        self.manifest[flaw_group].write('\t</testcase>\n\n')

    def closeManifests(self):
        """ Close the manifest """
        for man in self.manifest:
            self.manifest[man].write('</container>\n')
            self.manifest[man].close()

# end of manifest.py
