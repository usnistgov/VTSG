"""
Functions to create a SARD manifest in SARIF output.
"""
# *created  "Mon Aug 10 09:50:04 2020" *by "Paul E. Black"
# *modified "Wed Feb 23 13:19:11 2022" *by "Paul E. Black"

# ---------------------------------------------------------------------------------------
# This software was developed at the National Institute of Standards and Technology
# by employees of the Federal Government in the course of their official duties.
# Pursuant to title 17 Section 105 of the United States Code those parts of the
# software are not subject to copyright protection and are in the public domain.
#
# We would appreciate acknowledgment if the software is used.
#
# Paul E. Black  paul.black@nist.gov
#	http://hissa.nist.gov/~black/
# ---------------------------------------------------------------------------------------

# SARIF (v2.1.0) format is documented at
#   https://docs.oasis-open.org/sarif/sarif/v2.1.0/os/sarif-v2.1.0-os.html
#   https://docs.oasis-open.org/sarif/sarif/v2.1.0/os/sarif-v2.1.0-os.pdf
#   JSON schemas:
#   https://docs.oasis-open.org/sarif/sarif/v2.1.0/os/schemas/
#   https://github.com/oasis-tcs/sarif-spec
# specifically https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.4.json
# There is an on-line SARIF validator at https://sarifweb.azurewebsites.net/Validation

import json
import os

def get_timestring_utc():
    '''Get the current UTC date in SARIF format: YYYY-MM-DD
       # Sec. 3.9 Date/time properties'''
    import datetime
    return datetime.datetime.utcnow().strftime('%Y-%m-%d')

def get_CWE_name(cweId):
    '''Return a string name for a CWE id.  Return None if not found.'''
    CWENames = {
        '22':   "Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')",
        '78':   "Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')",
        '89':   'SQL Injection',
        '121':  'Stack-based Buffer Overflow',
        '122':  'Heap-based Buffer Overflow',
        '126':  'Buffer Over-read',
        '191':  'Integer Underflow',
        '208':  'Observable Timing Discrepancy',
        '385':  'Covert Timing Channel',
    }

    return CWENames.get(str(cweId), None)

def language(file):
    '''Determine the programming language of a file by its extension.'''
    languages = {
        '.c':    'c',
        '.cs':   'csharp',
        '.h':    'c',
        '.java': 'java',
        '.php':  'php',
        '.py':   'python',
    }
    extension = os.path.splitext(file)[1]
    if extension == '' or extension not in languages:
        # no extension or extension not recognized
        return None

    return languages[extension]

def new_sarif():
    '''Create a new JSON/dict for SARIF data.  Initilize the top level pieces'''
    data = {}
    data['$schema'] = "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.4.json"
    data['version'] = "2.1.0"
    return data


class Test_case(object):
    '''class for one test case

        Attributes :
            **run** (dict of ...): one SARIF run
    '''

    def __init__(self, cwe_id, submission_date, language, author, description, state):
        self.run = {}

        if state not in {'good', 'bad', 'mixed'}:
            print(f'state is {state}, but must be good, bad, or mixed')
            1 + None # trigger traceback

        self.run['properties'] = {
	    'id': cwe_id,
	    'type': 'source code',
	    'status': 'candidate',
            'submissionDate': submission_date,
	    'language': language,
	    'author': author,
	    'description': description,
	    'state': state
        }

        # put pairs in desired order
        self.run['tool'] = {}
        self.run['artifacts'] = [] # files used
        self.run['taxonomies'] = [{
            'name': 'CWE',
            'informationUri': 'https://cwe.mitre.org/data/published/cwe_v3.2.pdf/',
            'downloadUri': 'https://cwe.mitre.org/data/xml/cwec_v3.2.xml.zip',
            'organization': 'MITRE',
            'shortDescription': {
                'text': 'The MITRE Common Weakness Enumeration'
            },
            'isComprehensive': False,
            'taxa': [] # weaknesses used
        }]
        self.run['results'] = []

    def set_tool_driver(self, driver_dict):
        '''Set tool/driver information'''
        self.run['tool']['driver'] = driver_dict

    def new_weakness(self, cwe_id, paths_and_lines):
        result_locations = []
        for flaw in paths_and_lines:
            result_locations.append({
                'physicalLocation': {
                    'artifactLocation': {
                        'uri': flaw['path'],
                        'index': -99 # build locations array, then put index here
                    },
                    'region': {
                        'startLine': flaw['line']
                    }
                }
            })

        cwe_name = get_CWE_name(cwe_id)
        if cwe_name is None:
            print(f'Unknown FLAW CWE number {cwe_id} in {path}')
            exit(1)

        self.run['results'].append({
            'message':   {'text': cwe_name+'.'},
            'locations': result_locations,
            'taxa': [{
                'toolComponent': {
                    'name':  'CWE',
                    'index': '0'      # we only have one taxonomy: CWE
                },
                'id': str(cwe_id),
                'index': -99 # build taxa array, then put index here
            }]
        })

    def compile(self):
        '''Compile all the tables, list, indexes, etc. to make a
           final complete SARIF run.'''

        import hashlib

        def sha1(filePath):
            '''Find the SHA1 hash of the (full path to) file'''

            try:
                fileContent = open(filePath, 'rb').read()
            except OSError:
                print(f'Error: cannot open {filePath}')
                exit(1)

            return hashlib.sha1(fileContent).hexdigest()

        def compile_artifacts(self):
            '''Compile all locations into final artifacts array'''

            # create a set of all files used
            files = set()
            for flaw in self.run['results']:
                for loc in flaw['locations']:
                    files.add(loc['physicalLocation']['artifactLocation']['uri'])

            # add each one to the artifacts
            for file_path in sorted(files):
                #        fullFilePath = os.path.join(dirpath, file_path)
                file_info = {
                    'location': {
                        'uri': file_path
                    },
                    'length': os.path.getsize(file_path),
                    'sourceLanguage': language(file_path),
                    'hashes': {
                        'checksum': sha1(file_path)
                    }
                }
                # skip files without (known) extensions
                if file_info['sourceLanguage'] is not None:
                    self.run['artifacts'].append(file_info)

        def compile_taxa(self):
            '''Compile all CWEs into final taxa array'''
            #     3.19.25 taxa property says taxa is an array of zero or more unique
            # reportingDescriptor objects.  So if there are no weaknesses, SARIF
            # taxa is an empty ([]) array.

            # create a set of all CWEs used
            cwes = set()
            for flaw in self.run['results']:
                for taxon in flaw['taxa']:
                    cwes.add(int(taxon['id']))

            # add each one to the taxonomies
            for cwe in sorted(cwes):
                cwe_name = get_CWE_name(cwe)
                # an unknown CWE number will be caught earlier
                taxon_info = {
                    'id': str(cwe),
                    'name': cwe_name
                }
                self.run['taxonomies'][0]['taxa'].append(taxon_info)

        def file_in_artifacts(file, artifact_list):
            '''Return index of file in artifacts array.'''
            index_list = [i for i, entry in enumerate(artifact_list) if file == entry['location']['uri']]
            return index_list[0]

        def cwe_in_taxa(cwe_id, taxa_list):
            '''Return index of cwe_id in taxa array.'''
            index_list = [i for i, entry in enumerate(taxa_list) if cwe_id == entry['id']]
            return index_list[0]

        def number_of_lines(file):
            '''Return the number of lines in the file passed'''
            # SKIMP - system fail if file is not readable
            # SKIMP - inefficent if the file is enormous
            return len(open(file).readlines())

        def update_indexes(self):
            '''Update location and taxa indexes in all results'''
            for flaw in self.run['results']:
                # update locations
                for loc in flaw['locations']:
                    # update location//index
                    phy_loc = loc['physicalLocation']
                    file = phy_loc['artifactLocation']['uri']
                    artifact_index = file_in_artifacts(file, self.run['artifacts'])
                    if artifact_index is None:
                        # this should never happen
                        print(f'not found: FLAW file {file}')
                        exit(1)
                    phy_loc['artifactLocation']['index'] = artifact_index

                    # check startLine
                    fileNumberOfLines = number_of_lines(file)
                    start_line = phy_loc['region']['startLine']
                    #################################################################
                    #
                    #        SKIMP - get the VTSG code to find line number
                    #
                    #################################################################
                    #if start_line < 1 or start_line > fileNumberOfLines:
                    if start_line > fileNumberOfLines:
                        print(f'startLine is {start_line}, but must be between 1 and {fileNumberOfLines}')
                        print(f'    file {file}')
                        exit(1)

                # update taxa
                for taxon in flaw['taxa']:
                    cwe_id = taxon['id']
                    taxa_index = cwe_in_taxa(cwe_id, self.run['taxonomies'][0]['taxa'])
                    taxon['index'] = taxa_index

        compile_artifacts(self)

        compile_taxa(self)

        update_indexes(self)

        return self.run


class Sarif_writer(object):
    '''SARIF writer class

        Attributes :
            **compiled** (bool): True if data has been compiled, e.g., attributes, taxa
            **runs** (list of runs): test cases for the SARIF file
            **sarif** (dict of ...): JSON/dumps compatible SARIF file
    '''

    def __init__(self):
        self.compiled = False # has everything been successfully compiled?
        self.runs = []

    def new_test_case(self, description, state):
        '''Create a new JSON/dict for a test case, represented by one SARIF run.
            Sec. 3.14 run object
        '''
        test_case = Test_case(
	    cwe_id = -1, # means, assign new test case id
            submission_date = get_timestring_utc(),
	    language = 'python',
	    author = 'William Mentzer and Paul E. Black',
	    description = description,
	    state = state
        )

        test_case.set_tool_driver({
            'name': 'Vulnerability Test Suite Generator (VTSG) version 3',
            'organization': 'NIST',
            'supportedTaxonomies': [
                {
                    'name': 'CWE',
                    'index': 0
                }
    	    ]
        })

        self.runs += [test_case]

        return test_case

    def compile(self):
        '''Compile every test case as a SARIF run and add them to a
           final complete SARIF file.'''

        self.sarif = new_sarif()

        # compile each test case as a SARIF run and add it
        self.sarif['runs'] = []
        for test_case in self.runs:
            self.sarif['runs'].append(test_case.compile())

        # successful completion
        self.compiled = True

    def dump(self):
        '''Return a string of the SARIF information'''
        if self.compiled is not True:
            self.compile()

        return json.dumps(self.sarif, indent=2)

# end of sarif_writer.py
