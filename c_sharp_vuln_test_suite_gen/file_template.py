"""
file_template module
"""

from jinja2 import Template, DebugUndefined
import c_sharp_vuln_test_suite_gen.generator


class FileTemplate(object):
    """FileTemplate class

        Attributes :
            **_language_name** (str): Name of language (private member, please use getter and setter).

            **_file_extension** (str): File extension (private member, please use getter and setter).

            **_namespace** (int): Namespace (private member, please use getter and setter).

            **_code** (str): Template code (private member, please use getter and setter).

            **_imports** (list of str): imports for template (private member, please use getter and setter).

            **_comment** (dict str->str): Structure for comment (inline, multiline) \
                                          (private member, please use getter and setter).

            **_prefix** (str): Variables prefix (private member, please use getter and setter).

            **_import_code** (str): Import code with placeholder (private member, please use getter and setter).

            **_variables** (dict str->(dict str->str)): Identifier and initializer for variables \
                                          (private member, please use getter and setter).

    """

    def __init__(self, file_template):
        self._language_name = file_template.get("name")
        self._file_extension = file_template.find("file_extension").text
        self._namespace = ""
        if file_template.find("namespace") is not None:
            self._namespace = file_template.find("namespace").text
        self._code = file_template.find("code").text
        self._code = c_sharp_vuln_test_suite_gen.generator.Generator.remove_indent(self._code)
        self._imports = [imp.text for imp in file_template.find("imports").findall("import")]
        self._comment = {}
        self._comment['open'] = file_template.find("comment").find("open").text
        self._comment['close'] = file_template.find("comment").find("close").text
        self._comment['inline'] = file_template.find("comment").find("inline").text
        self._prefix = file_template.find("variables").get("prefix")
        self._import_code = file_template.find("variables").get("import_code")
        """ Import code with placeholder"""
        self._variables = {}
        for v in file_template.find("variables"):
            self._variables[v.get("type")] = {"code": v.get("code"), "init": v.get("init")}

    @property
    def language_name(self):
        """
        Name of language.

        :getter: Returns this language.
        :type: str
        """
        return self._language_name

    @property
    def namespace(self):
        """
        Namespace.

        :getter: Returns this namespace.
        :type: str
        """
        return self._namespace

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
        Fills the template by replacing the placeholder for the import  with the given arguments.

        Args :
            **imports** (str): The value to write.
        """
        res = ""
        for i in imports:
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
        Return the statement code of specified variable.

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

        :getter: Returns this code.
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
