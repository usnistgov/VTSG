# *modified "Tue Jul 11 15:54:48 2023" *by "Paul E. Black"
""" Vulnerability Test Suite Generator (VTSG)

Usage:
    vtsg.py -l LANGUAGE [-g GROUP ...] [-f FLAW ...] [-r DEPTH] [-s | -u] [--ACTS [<DOI>]] [-t TEMPLATE_DIRECTORY] [-n NUMBER_SAMPLED] [-d]
    vtsg.py (-h | --help)
    vtsg.py --version


Options:
    -h, --help                                                      Show this message
    --version                                                       Show version
    -l LANGUAGE --language=LANGUAGE                                 Select language for generation
    -g GROUP --group=GROUP                                          Generate cases with vulnerabilities in the specified group of flaws (can be repeated)
    -f FLAW --flaw=FLAW                                             Generate cases with vulnerabilities in the specified FLAW (can be repeated)
    -s --safe                                                       Only generate safe cases
    -u --unsafe                                                     Only generate unsafe cases
    -r DEPTH --depth=DEPTH                                          Depth of the Complexities [default: 1]
    --ACTS                                                          Use ACTS to select cases. [default: 2]
    -t TEMPLATE_DIRECTORY --template-directory TEMPLATE_DIRECTORY   Directory with language template files
    -n NUMBER_SAMPLED --number-sampled=NUMBER_SAMPLED               Write 1 of every N cases
    -d --debug                                                      Debug (programmer hook)

Examples:
    vtsg.py -l cs                         (generate C# cases with all flaws coded, safe and unsafe, complexity depth = 1)
    vtsg.py -l php -g IDOR                (generate PHP cases with all flaws in the IDOR group, and other options to default)
    vtsg.py -l cs -g IDOR -g Injection    (generate cases with all flaws in the IDOR or Injection groups)
    vtsg.py -l cs -f CWE_354              (generate cases with CWE 354)
    vtsg.py -l cs -f CWE_89 -f CWE_78     (generate cases with CWE 89 or CWE 78)
    vtsg.py -l cs -r 2                    (generate cases with the complexity depth up to  and including two levels of nesting)
    vtsg.py -l cs -n 3                    (write only one of every three cases generated)
    vtsg.py -l py --ACTS 3                (generate Python cases covering all triples of modules)
    vtsg.py -l cs -s                      (generate cases where the vulnerabilities have been fixed)
    vtsg.py -l cs -u                      (generate cases where there are vulnerabilities)
    vtsg.py -l example -t tests/templates (generate the manual example, where the files for the "example" language are in tests/templates)

    All these options can be combined (except for -s and -u, --ACTS and -r > 1, and --ACTS and -n).

    For example:
        vtsg.py -l cs -f CWE_78 -g OWASP_a1 -r 2 -n 5 -s
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

    # get template directory, if any
    template_dir = 'src/templates'
    if args["--template-directory"]:
        template_dir = args["--template-directory"]

    # check if language exists
    path = os.path.abspath(os.path.join(template_dir, language))
    if not os.path.isdir(path):
        print(f'[ERROR] no directory found for {language}')
        print(f"Create '{language}' directory in {template_dir} folder")
        sys.exit(1)

    # create generator for specified language
    g = Generator(date, language=language, template_directory=template_dir)

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
    # this check for safe & unsafe is performed by docopt and is no longer needed
    if args["--safe"] and args["--unsafe"]:
        print("Invalid options. Cannot specify both -s and -u. See --help")
        sys.exit(1)
    if args["--safe"]:
        safe = True
        unsafe = False
    if args["--unsafe"]:
        safe = False
        unsafe = True
    debug = args["--debug"]
    try:
        parameter = args["--depth"]
        g.max_recursion = int(parameter)
        if g.max_recursion < 0: raise ValueError
    except ValueError:
        print("Invalid parameter: -r takes a non-negative integer. See --help")
        sys.exit(1)
    if args["--number-sampled"]:
        try:
            g._number_sampled = int(args["--number-sampled"]) # ValueError if not number
            if g.number_sampled < 1: raise ValueError
        except ValueError:
            print("Invalid parameter: -n takes a positive integer. See --help")
            sys.exit(1)

    # options that select cases written
    if args["--ACTS"]:
        if args["<DOI>"] is None:
            g._ACTS_doi = 2 # default Degree of Interaction
        else:
            try:
                g._ACTS_doi = int(args["<DOI>"])
                if g.ACTS_doi < 1: raise ValueError
            except ValueError:
                print("Invalid parameter: --ACTS takes a positive integer. See --help")
                sys.exit(1)
    if args["--ACTS"] and g.number_sampled is not None:
        print("Invalid options. Cannot specify both --ACTS and -n. See --help")
        sys.exit(1)
    if args["--ACTS"] and g.max_recursion > 1:
        print("Invalid options. Cannot specify both --ACTS and -r > 1. See --help")
        sys.exit(1)

    # set user list
    g.set_flaw_type_user(flaw_type_user)
    g.set_flaw_group_user(flaw_group_user)

    # run generator
    g.generate(debug=debug, generate_safe=safe, generate_unsafe=unsafe)

    print("Finish")


if __name__ == "__main__":
    main()

# end of vtsg.py
