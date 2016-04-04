""" Test Cases Generator

Usage:
    test_cases_generator.py
    test_cases_generator.py -l LANGUAGE [-f FLAW_GROUP ...] [-c CWE ...] [-r DEPTH] [-g NUMBER_GENERATED] [-s | -u] [-d]
    test_cases_generator.py (-h | --help)
    test_cases_generator.py (-d | --debug)
    test_cases_generator.py --version


Options:
    -h, --help                                                      Show this message
    --version                                                       Show version
    -l LANGUAGE --language=LANGUAGE                                 Select language for generation
    -f FLAW_GROUP --flaw-group=FLAW_GROUP                           Generate files with vulnerabilities concerning the specified  flaw group, from the OWASP Top Ten (can be repeated)
    -c CWE --cwe=CWE                                                Generate files with vulnerabilities concerning the specified CWE (can be repeated)
    -s --safe                                                       Generate the safe samples
    -u --unsafe                                                     Generate the unsafe samples
    -d --debug                                                      Debug Mode
    -r DEPTH --depth=DEPTH                                          Depth of the Complexities (Default: 1)
    -g NUMBER_GENERATED --number-generated=NUMBER_GENERATED         (DEPRECATED - DON'T USE, SHOULD BE REMOVED SOON) Number of combination of input, filtering and sink used to generate (Default: -1, it means all)

List of flaw groups:
    \n\tA1        \tInjection (SQL,LDAP,XPATH)\
    \n\tA2        \tBASM (Broken Authentication and Session Management)
    \n\tA3        \tXSS (Cross-site Scripting)\
    \n\tA4        \tIDOR (Insecure Direct Object Reference)\
    \n\tA5        \tSM (Security Misconfiguration)\
    \n\tA6        \tSDE (Sensitive Data Exposure)\
    \n\tA7        \tMFLAC (Missing Function Level Access Control)\
    \n\tA8        \tCSRF (Cross-Site Request Forgery)\
    \n\tA9        \tUCWKV (Using Components With Known Vulnerabilities)\
    \n\tA10       \tURF (URL Redirects and Forwards)

List of CWEs:
    \n\t22        \tPath Traversal\
    \n\t78        \tCommand OS Injection\
    \n\t79        \tXSS\
    \n\t89        \tSQL Injection\
    \n\t90        \tLDAP Injection\
    \n\t91        \tXPath Injection\
    \n\t95        \tCode Injection\
    \n\t98        \tFile Injection\
    \n\t209       \tInformation Exposure Through an Error Message\
    \n\t311       \tMissing Encryption of Sensitive Data\
    \n\t327       \tUse of a Broken or Risky Cryptographic Algorithm\
    \n\t476       \tNULL Pointer Dereference
    \n\t601       \tURL Redirection to Untrusted Site\
    \n\t862       \tInsecure Direct Object References"

Examples:

    test_cases_generator.py -l cs                         (generate files with all CWE registered, safe and unsafe, complexity depth = 1)
    test_cases_generator.py -l cs -f IDOR                 (generate files with all CWE belonging to IDOR group, and other options to default)
    test_cases_generator.py -l cs -f IDOR -f Injection    (generate files with all CWE belonging to IDOR group and Injection)
    test_cases_generator.py -l cs -c 89                   (generate files with the CWE 354)
    test_cases_generator.py -l cs -c 89 -c 78             (generate files with the CWE 89 and CWE 78)
    test_cases_generator.py -l cs -r 2                    (generate all files with the complexity depth equals to 2, two level of imbrication)
    test_cases_generator.py -l cs -g 1                    (generate all files with only one combination of input, filtering and sink for all CWE)
    test_cases_generator.py -l cs -s                      (generate all files where the vulnerabilities have been fixed)
    test_cases_generator.py -l cs -u                      (generate all files where there is still vulnerabilities)

    All these options can be combinated (except for -s and -u).

    For example:

        test_cases_generator.py -l cs -c 78 -f IDOR -r 1 -g 1 -s
"""


import sys
import time
import os
from docopt import docopt
from c_sharp_vuln_test_suite_gen.generator import Generator
from c_sharp_vuln_test_suite_gen.file_manager import FileManager


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
        print("Specify a language with -l/--language option (cs, php)")
        sys.exit(1)

    # check if language exists
    if not FileManager.exist_language(language):
        print("Patch your language folder '{}'".format(language))
        sys.exit(1)

    # create generator for specified language
    g = Generator(date, language=language)

    # List of flaws
    flaw_list = g.get_group_list()
    cwe_list = g.get_cwe_list()

    flaw_group_user = [x.lower() for x in args["--flaw-group"]]
    for flaw in flaw_group_user:
        if flaw.lower() not in flaw_list:
            print("There is no flaws associated with the given flaw group (-f {} option).\
                  See --help.".format(flaw.lower()))
            sys.exit(1)
    try:
        flaw_type_user = [int(x) for x in args["--cwe"]]
    except ValueError:
        print("Invalid format. Value of the -c option must be an integer. See --help")
        sys.exit(1)
    for cwe in flaw_type_user:
        if cwe not in cwe_list:
            print("There is no flaws associated with the given CWE (-c {} option). See --help.".format(cwe))
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
        print("Invalid format. Value of the -r option must be an integer. See --help")
        sys.exit(1)
    try:
        arg = args["--number-generated"]
        g.number_generated = int(arg) if arg is not None else -1
    except ValueError:
        print("Invalid format. Value of the -g option must be an integer. See --help")
        sys.exit(1)

    # set user list
    g.set_flaw_type_user(flaw_type_user)
    g.set_flaw_group_user(flaw_group_user)

    # run generation
    g.generate(debug=debug, generate_safe=safe, generate_unsafe=unsafe)

    # check if astyle is here
    if os.path.isfile(ASTYLE_PATH):
        print("Indentation ...")
        cmd = ASTYLE_PATH+" -r TestSuite_"+date+"/*."+g.get_extension()+" --style=java --suffix=none --indent-switches -q"
        os.system(cmd)
    else:
        print("No indentation")

    print("Finish")


if __name__ == "__main__":
    main()
