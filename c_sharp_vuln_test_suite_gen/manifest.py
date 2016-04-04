"""
manifest module
"""

import os
import time


class Manifest(object):
    """Manifest class

        Attributes :
            **dir_name** (str): Directory name.

            **date** (str): Date of generation.

            **manifest** (str): List of open manifest for each group generated.

    """

    def __init__(self, dir_name, date):
        self.dir_name = dir_name
        self.date = date
        self.manifest = {}

    def createManifests(self, flaw_groups):
        """
        Create a manifest for selected group.

        Args:
            **flaw_groups** (list of str): List of flaw group
        """
        for flaw_group in flaw_groups:
            path = os.path.join(self.dir_name, "OWASP_" + flaw_group)
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
        reformated_date = time.strftime("%d/%m/%y", time.strptime(self.date, "%m-%d-%Y_%Hh%Mm%S"))
        # meta data for current test case
        meta_data = ("\t<testcase> \n" +
                     "\t\t<meta-data> \n" +
                     "\t\t\t<author>Bertrand STIVALET, Aurelien DELAITRE</author> \n" +
                     "\t\t\t<date>" + reformated_date + "</date> \n" +
                     "\t\t\t<input>" + input_sample + "</input>\n"
                     "\t\t</meta-data> \n \n")
        # write meta data
        self.manifest[flaw_group].write(meta_data)
        file_block = ""
        for f in files_path:
            file_path = f['path']
            flaw_line = f['line']
            # check flaw line if it exist
            if (flaw_line == 0):
                file_block += "\t\t<file path=\"" + file_path + "\" language=\""+language+"\"/> \n\n"
            else:
                file_block += "\t\t<file path=\"" + file_path + "\" language=\""+language+"\"> \n"
                file_block += "\t\t\t<flaw line=\"" + str(flaw_line) + "\" name =\"" + flaw.upper() + "\"/> \n"
                file_block += "\t\t</file> \n\n"

        self.manifest[flaw_group].write(file_block)
        self.manifest[flaw_group].write("\t</testcase> \n\n\n")

    def closeManifests(self):
        """ Close the manifest """
        for man in self.manifest:
            self.manifest[man].write("</container>")
            self.manifest[man].close()
