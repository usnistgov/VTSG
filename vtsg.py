# *modified "Wed Aug 17 08:42:10 2022" *by "Paul E. Black"
""" Vulnerability Test Suite Generator (VTSG)

Usage:
    test_cases_generator.py
    test_cases_generator.py -l LANGUAGE [-f FLAW_GROUP ...] [-c CWE ...] [-r DEPTH] [-g NUMBER_GENERATED] [-s | -u] [-d]
    test_cases_generator.py (-h | --help)
    test_cases_generator.py --version


Options:
    -h, --help                                                      Show this message
    --version                                                       Show version
    -l LANGUAGE --language=LANGUAGE                                 Select language for generation
    -f FLAW_GROUP --flaw-group=FLAW_GROUP                           Generate files with vulnerabilities concerning the specified  flaw group, from the OWASP Top Ten (can be repeated)
    -c CWE --cwe=CWE                                                Generate files with vulnerabilities concerning the specified CWE (can be repeated)
    -s --safe                                                       Only generate safe cases
    -u --unsafe                                                     Only generate unsafe cases
    -r DEPTH --depth=DEPTH                                          Depth of the Complexities (Default: 1)
    -g NUMBER_GENERATED --number-generated=NUMBER_GENERATED         (DEPRECATED - DON'T USE, SHOULD BE REMOVED SOON) Number of combination of input, filtering and sink used to generate (Default: -1, it means all)
    -d --debug                                                      Debug (programmer hook)

List of flaw groups:
    \n\tOWASP_a1        \tInjection (SQL,LDAP,XPATH)\
    \n\tOWASP_a2        \tBASM (Broken Authentication and Session Management)
    \n\tOWASP_a3        \tXSS (Cross-site Scripting)\
    \n\tOWASP_a4        \tIDOR (Insecure Direct Object Reference)\
    \n\tOWASP_a5        \tSM (Security Misconfiguration)\
    \n\tOWASP_a6        \tSDE (Sensitive Data Exposure)\
    \n\tOWASP_a7        \tMFLAC (Missing Function Level Access Control)\
    \n\tOWASP_a8        \tCSRF (Cross-Site Request Forgery)\
    \n\tOWASP_a9        \tUCWKV (Using Components With Known Vulnerabilities)\
    \n\tOWASP_a10       \tURF (URL Redirects and Forwards)

List of flaw types:
    \n\tCWE_22        \tPath Traversal\
    \n\tCWE_78        \tCommand OS Injection\
    \n\tCWE_79        \tXSS\
    \n\tCWE_89        \tSQL Injection\
    \n\tCWE_90        \tLDAP Injection\
    \n\tCWE_91        \tXPath Injection\
    \n\tCWE_95        \tCode Injection\
    \n\tCWE_98        \tFile Injection\
    \n\tCWE_209       \tInformation Exposure Through an Error Message\
    \n\tCWE_311       \tMissing Encryption of Sensitive Data\
    \n\tCWE_327       \tUse of a Broken or Risky Cryptographic Algorithm\
    \n\tCWE_476       \tNULL Pointer Dereference
    \n\tCWE_601       \tURL Redirection to Untrusted Site\
    \n\tCWE_862       \tInsecure Direct Object References"

Examples:

    test_cases_generator.py -l cs                         (generate C# cases with all CWEs coded, safe and unsafe, complexity depth = 1)
    test_cases_generator.py -l php -f IDOR                (generate PHP cases with all CWEs belonging to IDOR group, and other options to default)
    test_cases_generator.py -l cs -f IDOR -f Injection    (generate cases with all CWEs belonging to IDOR or Injection groups)
    test_cases_generator.py -l cs -c CWE_354              (generate cases with CWE 354)
    test_cases_generator.py -l cs -c CWE_89 -c CWE_78     (generate cases with CWE 89 or CWE 78)
    test_cases_generator.py -l cs -r 2                    (generate cases with the complexity depth equals to 2, two level of imbrication)
    test_cases_generator.py -l cs -g 1                    (generate cases with only one combination of input, filtering and sink for all flaws)
    test_cases_generator.py -l cs -s                      (generate cases where the vulnerabilities have been fixed)
    test_cases_generator.py -l cs -u                      (generate cases where there are vulnerabilities)

    All these options can be combinated (except for -s and -u).

    For example:

        test_cases_generator.py -l cs -c CWE_78 -f IDOR -r 1 -g 1 -s
"""


import sys
import time
import os
from docopt import docopt
from src.generator import Generator
from src.file_manager import FileManager


def main():
    ASTYLE_PATH = "./astyle/build/gcc/bin/astyle"
    debug = False
    safe = True
    unsafe = True
    date = time.strftime("%m-%d-%Y_%Hh%Mm%S")

    args = docopt(__doc__, version='0.4')

    # get selected language
    language = None
    if args["--language"]:
        language = args["--language"]
    else:
        print("Specify a language with -l/--language (cs, php, py)")
        sys.exit(1)

    # check if language exists
    if not FileManager.exist_language(language):
        print(f"Create '{language}' directory in src/templates folder")
        sys.exit(1)

    # create generator for specified language
    g = Generator(date, language=language)

    # List of flaws
    group_list = g.get_group_list()
    flaw_list = g.get_flaw_list()

    flaw_group_user = [x for x in args["--flaw-group"]]
    for group in flaw_group_user:
        if group not in group_list:
            print(f'Language {language} does not have flaw group {group}. See --help.')
            sys.exit(1)
    try:
        flaw_type_user = [x for x in args["--cwe"]]
    except ValueError:
        print("Invalid option. Value of the -c option must be an integer. See --help")
        sys.exit(1)
    for flaw in flaw_type_user:
        if flaw not in flaw_list:
            print(f'Language {language} does not have flaw type {flaw}. See --help.')
            sys.exit(1)
    if args["--safe"] and args["--unsafe"]:
        print("Invalid option. Cannot specify both -s and -u. See --help")
        sys.exit(1)
    if args["--safe"]:
        safe = True
        unsafe = False
    if args["--unsafe"]:
        safe = False
        unsafe = True
    debug = args["--debug"]
    try:
        arg = args["--depth"]
        g.max_recursion = int(arg) if arg is not None else 1
    except ValueError:
        print("Invalid option. Value of the -r option must be an integer. See --help")
        sys.exit(1)
    try:
        arg = args["--number-generated"]
        g.number_generated = int(arg) if arg is not None else -1
    except ValueError:
        print("Invalid option. Value of the -g option must be an integer. See --help")
        sys.exit(1)

    # set user list
    g.set_flaw_type_user(flaw_type_user)
    g.set_flaw_group_user(flaw_group_user)

    # run generator
    g.generate(debug=debug, generate_safe=safe, generate_unsafe=unsafe)

    # run astyle if it is here
    if os.path.isfile(ASTYLE_PATH):
        print("Indentation ...")
        cmd = ASTYLE_PATH+" -r TestSuite_"+date+"/*."+g.get_extension()+" --style=java --suffix=none --indent-switches -q"
        os.system(cmd)
    else:
        print("No indentation")

    print("Finish")


if __name__ == "__main__":
    main()
