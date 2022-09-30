# *modified "Fri Sep 30 08:50:34 2022" *by "Paul E. Black"
""" Vulnerability Test Suite Generator (VTSG)

Usage:
    vtsg.py
    vtsg.py -l LANGUAGE [-g GROUP ...] [-f FLAW ...] [-r DEPTH] [-s | -u] [-t TEMPLATE_DIRECTORY] [-n NUMBER_GENERATED] [-d]
    vtsg.py (-h | --help)
    vtsg.py --version


Options:
    -h, --help                                                      Show this message
    --version                                                       Show version
    -l LANGUAGE --language=LANGUAGE                                 Select language for generation
    -g GROUP[,GROUP] --group=GROUP[,GROUP]                          Generate files with vulnerabilities in the specified group of flaws (can be repeated)
    -f FLAW[,FLAW] --flaw=FLAW[,FLAW]                               Generate files with vulnerabilities in the specified FLAW (can be repeated)
    -s --safe                                                       Only generate safe cases
    -u --unsafe                                                     Only generate unsafe cases
    -r DEPTH --depth=DEPTH                                          Depth of the Complexities (Default: 1)
    -t TEMPLATE_DIRECTORY --template-directory TEMPLATE_DIRECTORY   Directory with language template files
    -n NUMBER_GENERATED --number-generated=NUMBER_GENERATED         (DEPRECATED - DON'T USE, SHOULD BE REMOVED SOON) Number of combination of input, filtering and sink used to generate (Default: -1, it means all)
    -d --debug                                                      Debug (programmer hook)

Examples:

    vtsg.py -l cs                         (generate C# cases with all flaws coded, safe and unsafe, complexity depth = 1)
    vtsg.py -l php -g IDOR                (generate PHP cases with all flaws in the IDOR group, and other options to default)
    vtsg.py -l cs -g IDOR -g Injection    (generate cases with all flaws in the IDOR or Injection groups)
    vtsg.py -l cs -f CWE_354              (generate cases with CWE 354)
    vtsg.py -l cs -f CWE_89 -f CWE_78     (generate cases with CWE 89 or CWE 78)
    vtsg.py -l cs -r 2                    (generate cases with the complexity depth equals to 2, two level of nesting)
    vtsg.py -l cs -n 1                    (generate cases with only one combination of input, filtering and sink for all flaws)
    vtsg.py -l cs -s                      (generate cases where the vulnerabilities have been fixed)
    vtsg.py -l cs -u                      (generate cases where there are vulnerabilities)

    All these options can be combined (except for -s and -u).

    For example:
        vtsg.py -l cs -f CWE_78 -g IDOR -r 1 -n 1 -s
"""


import sys
import time
import os
from docopt import docopt
from src.generator import Generator
from src.file_manager import FileManager


def main():
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

    flaw_group_user = [x for x in args["--group"]]
    for group in flaw_group_user:
        if group not in group_list:
            print(f'Language {language} does not have flaw group {group}. See --help.')
            sys.exit(1)
    flaw_type_user = [x for x in args["--flaw"]]
    for flaw in flaw_type_user:
        if flaw not in flaw_list:
            print(f'Language {language} does not have flaw {flaw}. See --help.')
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
        print("Invalid option. Value of the -n option must be an integer. See --help")
        sys.exit(1)

    # set user list
    g.set_flaw_type_user(flaw_type_user)
    g.set_flaw_group_user(flaw_group_user)

    # run generator
    g.generate(debug=debug, generate_safe=safe, generate_unsafe=unsafe)

    print("Finish")


if __name__ == "__main__":
    main()
