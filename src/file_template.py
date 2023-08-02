"""
file_template module

 *modified "Tue Aug  1 16:18:16 2023" *by "Paul E. Black"
"""

import re
from jinja2 import Template, DebugUndefined
import src.generator


class FileTemplate(object):
    """FileTemplate class

        Attributes :
            **_language_name** (str): Name of language (private member, please use getter).

            **_file_extension** (str): File extension (private member, please use getter).

            **_code** (str): Template code (private member, please use getter).

            **_imports** (list of str): imports for template (private member, please use getter).

            **_comment** (dict str->str): Structure for comment (inline, multiline) \
                                          (private member, please use getter).

            **_prefix** (str): Variables prefix (private member, please use getter).

            **_import_code** (str): Import code with placeholder (private member).

            **_variables** (dict str->(dict str->str)): Identifier and initializer for variables \
                                          (private member, please use functions).

    """

    def __init__(self, file_template):
        self._language_name = file_template.get("name")
        self._file_extension = file_template.find("file_extension").text
        template_code = file_template.find("code").text
        if template_code[0] == '\n':
            template_code = template_code[1:] # remove a leading new line
        self._code = src.generator.Generator.remove_indent(template_code)
        self._imports = [imp.text for imp in file_template.find("imports").findall("import")]
        self._comment = {}
        self._comment['open'] = file_template.find("comment").find("open").text
        self._comment['close'] = file_template.find("comment").find("close").text
        self._comment['inline'] = file_template.find("comment").find("inline").text
        self._syntax = {}
        s = file_template.find('syntax')
        if s is not None:
            if s.find('statement_terminator') is not None:
                self._syntax['statement_terminator'] = s.find('statement_terminator').text
            if s.find('indent') is not None:
                self._syntax['indent'] = s.find('indent').text
            self._import_code = s.find('import_code').text
        self._prefix = file_template.find("variables").get("prefix")
        # the preceding is the import code, which has a placeholder
        self._variables = {}
        for v in file_template.find("variables"):
            self._variables[v.get("type")] = {"code": v.get("code"), "init": v.get("init")}
        # consistency check: must have both {{local_var}} and type/code/init or neither
        has_local_vars = re.search("{{\s*local_var\s*}}", self.code) is not None
        has_var_decls  = self._variables != {}
        if has_local_vars != has_var_decls:
            # inconsistent!
            if has_local_vars:
                assert not has_var_decls
                print('[ERROR] {{local_var}} but no <variable type code init /> statements in file_template.xml')
            if has_var_decls:
                assert not has_local_vars
                print('[ERROR] <variable type code init /> statements but no {{local_var}} in file_template.xml')
            print(f'Both are needed to show where and how to declare local variables')
            exit(1)

    @property
    def language_name(self):
        """
        Name of language.

        :getter: Returns this language.
        :type: str
        """
        return self._language_name

    @property
    def imports(self):
        """
        Imports for template.

        :getter: Returns these imports.
        :type: list of str
        """
        return self._imports

    def generate_imports(self, imports):
        """
        Generate import statements with the template import_code and the names passed.

        Args :
            **imports** (set of str): libraries to import, e.g. {'sys', 'os'}.
        """
        res = ""
        for i in sorted(imports):
            imp = Template(self._import_code).render(import_file=i)
            res += imp + "\n"
        return res

    @property
    def prefix(self):
        """
         Variables prefix.

        :getter: Returns this prefix.
        :type: str
        """
        return self._prefix

    def get_type_var_code(self, type_v):
        """
        Return code to declare a variable of type type_v.

        Args :
            **type_v** (str)
        """
        if type_v in self._variables:
            return self._variables[type_v]["code"]
        else:
            return ""

    def get_init_var_code(self, type_v):
        """
        Return the init code of specified variable

        Args :
            **type_v** (str)
        """
        if type_v in self._variables:
            return self._variables[type_v]["init"]
        else:
            return ""

    @property
    def code(self):
        """
         Template code.

        :getter: Returns the source code.
        :type: str
        """
        return self._code

    @property
    def file_extension(self):
        """
         File extension.

        :getter: Returns this extension.
        :type: str
        """
        return self._file_extension

    @property
    def comment(self):
        """
         Structure for comment (inline, multiline).

        :getter: Returns this structure.
        :type: str
        """
        return self._comment

    @property
    def statement_terminator(self):
        """
         String to finish statements

        :getter: Return the string
        :type: str
        """
        # Note: to require <syntax><statement_terminator>, remove this outer conditional
        if 'statement_terminator' in self._syntax:
            if self._syntax['statement_terminator'] is None:
                return "" # interpret None as empty string
            else:
                return self._syntax['statement_terminator']
        else:
            return ""

    @property
    def indent(self):
        """
         Prefix string to indent statements one level

        :getter: Return the string
        :type: str
        """
        # Note: to require <syntax><indent>, remove this outer conditional
        if 'indent' in self._syntax:
            return self._syntax['indent']
        else:
            return ''

# end of file_template.py
