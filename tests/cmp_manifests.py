#            *created  "Wed Feb  9 10:56:53 2022" *by "Paul E. Black"'
versionMod=' *modified "Mon Feb 13 09:27:53 2023" *by "Paul E. Black"'
#

# Compare two manifest.xml files, ignoring unimportant differences like dates
# If they differ, report the first difference and exit.
# SKIMP this checks line by line.  XML files may differ in format, while the content
# matches.  This does not do XML matching.

# usage:
# $ python ./cmp_manifests.py TestSuite_02-09-2022_10h52m26/PHP/OWASP_a1/manifest.xml tests/PHP/OWASP_a1/manifest.xml

# This software was developed at the National Institute of Standards and
# Technology by employees of the Federal Government in the course of their
# official duties.  Pursuant to title 17 Section 105 of the United States Code
# this software is not subject to copyright protection and is in the public domain.
#
# We would appreciate acknowledgment if the software is used.
#
# Paul E. Black  paul.black@nist.gov or p.black@acm.org
#	https://hissa.nist.gov/~black/

import argparse
import sys # for exit()
import re

def parse_arguments():
    parser = argparse.ArgumentParser(description='Compare two manifest.xml files, ignoring unimportant differences like dates.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s'+versionMod)
    parser.add_argument('manifest1',
                    metavar='manifest1.xml',
                    help='SARD manifest file')
    parser.add_argument('manifest2',
                    metavar='manifest2.xml',
                    help='SARD manifest file')
    return parser.parse_args()

def date_match(line1, line2):
    '''
    Return true if lines match except for content of date field, e.g.
			<date>2022 January 12</date> 
			<date>03/02/22</date> 
    '''
    date_pattern = '^\s*<date>[^<]*</date>\s*$'
    return re.match(date_pattern, line1.strip()) and re.match(date_pattern, line2.strip())

def testsuite_match(line1, line2):
    '''
    Return true if lines match except for name of TestSuite directory, e.g.
	<file path="TestSuite_02-03-2022_10h42m19/Csharp/OWASP_a6/cwe_327/unsafe/cwe_327__I_readline__F_no_filtering__S_md5__0_File1.cs" language="Csharp"> 
	<file path="TestSuite_02-03-2022_10h42m20/Csharp/OWASP_a6/cwe_327/unsafe/cwe_327__I_readline__F_no_filtering__S_md5__0_File1.cs" language="Csharp"> 
    '''
    testsuite_pattern = '^\s*<file path="TestSuite_[^/]*/(.*)'
    line1MO = re.match(testsuite_pattern, line1)
    line2MO = re.match(testsuite_pattern, line2)
    return line1MO and line2MO and line1MO.group(1) == line2MO.group(1)

def try_openin(manifest_file):
    try:
        file = open(manifest_file)
    except (FileNotFoundError, PermissionError):
        print(f'Cannot open {manifest_file} to read')
        sys.exit(-1)
    except IsADirectoryError:
        print(f'{manifest_file} is a directory, not a file')
        sys.exit(-1)
    return file

if __name__ == '__main__':
    args = parse_arguments()
    manifest1 = args.manifest1
    manifest2 = args.manifest2

    # (try to) open both manifest files
    file1 = try_openin(manifest1)
    file2 = try_openin(manifest2)

    line = 0

    for line1 in file1:
        line += 1

        line2 = file2.readline()
        if line2 == '':
            print(f'EOF on {manifest2}')
            sys.exit(-3)

        if (line1 == line2 or
            date_match(line1, line2) or
            testsuite_match(line1, line2)):
            next
        else:
            print(f'{manifest1} {manifest2} differ: line {line}')
            print(f'{line1}', end='')
            print(f'{line2}', end='')
            print(f'exiting')
            sys.exit(-2)

    # manifest 1 is done.  Check that nothing remains in manifest 2
    if file2.readline():
        print(f'EOF on {manifest1}')
        sys.exit(-3)

    # otherwise, they match

# end of cmp_manifests.py
