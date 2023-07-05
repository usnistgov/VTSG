"""
Module to select test cases using ACTS
https://csrc.nist.gov/acts
Yu, L., Lei, Y., Kacker, R. N., & Kuhn, D. R. "ACTS: A combinatorial test generation
tool", 2013 IEEE Sixth International Conference on Software Testing, Verification and
Validation (ICST).

  *created "Thu Jun  1 09:39:16 2023" *by "Paul E. Black"
 *modified "Wed Jul  5 15:11:44 2023" *by "Paul E. Black"

The interface is select_cases_ACTS().  Pass a list of cases; select via ACTS; and
return a subset of the cases passed.

ACTS has two important options, neither of which are (currently) supported with this
interface.  They are degree of interaction (default 2) and algorithm.
"""

# these were helpful while I was developing
ACTS_print_debug_output = False

class module_map_table():
    """
    Table that maps between modules (inputs, filters, sinks, etc.) and ACTS values.
    """

    def __init__(self, table_name):
        self._name = table_name
        # _prefix is the string that makes these values unique over all values
        if table_name == 'COMPLEXITY':
            self._prefix = 'CPX'
        else:
            self._prefix = table_name[0]
        self._table = [] # list of modules
        self._values = set() # set of values

    def get_value(self, module):
        """
        If the module is already in the table, return the ACTS value for it.  If not,
        add the module to the table, and return the (new) value.  This works even
        when the module is None, which occurs if a case doesn't have this module.
        """
        if module not in self._table:
            self._table.append(module)
        value = f'{self._prefix}{self._table.index(module)}'
        self._values |= {value}
        return value

    def module(self, value):
        """
        Return the module for this value.
        """
        return self._table[int(value)]

    def description(self, value):
        """
        Return the module description for this value.
        """
        mod = self._table[int(value)]
        if mod is None:
            return '(none)'
        return mod.module_description

    @property
    def table(self):
        return self._table

    @property
    def values(self):
        return self._values

    @property
    def name(self):
        return self._name


class ACTS_interface():
    """
    Data to use NIST ACTS to select the test cases that will be created.
    """

    def __init__(self):
        self.inputs  = module_map_table('INPUT')
        self.filters = module_map_table('FILTER')
        self.sinks   = module_map_table('SINK')
        self.eqs     = module_map_table('EXEC_QUERY')
        self.complexities = module_map_table('COMPLEXITY')

    def print_module_maps(self):
        """
        Print tables that map modules to ACTS values. 
                    ***** FOR DEBUGGING ONLY *****
        """

        def print_module_table(map_table):
            """    print the table of modules.    """
            table = map_table.table
            print(f'{map_table.name}:', end='')
            for i in range(len(table)):
                mod = table[i]
                if mod is not None:
                    description = mod.module_description
                else:
                    description = 'Nothing'
                print(f'  {i} {description}', end='')
            print('') # the new line

        print_module_table(self.inputs)
        print_module_table(self.filters)
        print_module_table(self.sinks)
        print_module_table(self.eqs)


def write_parameters_and_constraints(fp, cases):
    """
    Write the parameters (inputs, filters, sinks, complexities, etc.) for these cases
    Note: The flaw is not a parameter.  It is only for organizing cases.  The flaw
    has no effect on the code.
    """

    # information, tables, routines, etc. needed to use NIST ACTS to select test cases
    ai = ACTS_interface()

    ###################################################################################
    #
    # extract the inputs, filters, complexities, etc. used in these cases
    #
    ###################################################################################

    # set of inputs, filters, and eqs used by each sink; for constraints
    sink_inputs = {}
    sink_filters = {}
    sink_eqs = {}
    filter_has_complexities = {} # filters that take complexities
    complexities = set()
    no_complexities = 'CP0' # the special value meaning no complexity for this case
    # the set of complexities that don't need conditions.  make constraints from these
    bare_complexities = set()
    conditions = set()
    no_condition = f'CNONE' # the special value meaning no condition for a complexity
    for case in cases:
        input_value = ai.inputs.get_value(case.input)
        filter_value = ai.filters.get_value(case.filter)
        sink_value = ai.sinks.get_value(case.sink)
        eq_value = ai.eqs.get_value(case.exec_query)
        # save the input, filter, and exec_query that this sink uses
        if sink_value not in sink_inputs: # this is a new sink
            sink_inputs[sink_value] = set()
            sink_filters[sink_value] = set()
            sink_eqs[sink_value] = set()
        sink_inputs[sink_value] |= {input_value}
        sink_filters[sink_value] |= {filter_value}
        sink_eqs[sink_value] |= {eq_value}
        # save info for constraints that some filters takes NO complexities
        if filter_value not in filter_has_complexities:
            filter_has_complexities[filter_value] = False # no complexities, yet

        if len(case.complexity_list) == 0: # this case has no complexities
            complexities |= {no_complexities}
            conditions |= {no_condition} # we need this pseudo-value for Constraint
        else:
            filter_has_complexities[filter_value] = True

            for c in case.complexity_list:
                complexity = f'CPX{c.id}'
                complexities |= {complexity}
                if c.cond_id:
                    conditions |= {f'CND{c.cond_id}'}
                else:
                    # this complexity doesn't need a condition.  Save to make a Constraint
                    bare_complexities |= {complexity}
                    conditions |= {no_condition} # we need this pseudo-value for a Constraint

    # Make sure "no"_condition is an ACTS value because at least one VTSG test case
    # doesn't have any conditions, and we have to make a constraint that will use
    # no_condition.
#    if len(conditions) == 0:
#        conditions |= {no_condition}

    #ai.print_module_maps() # map of values to module description is in the xml

    ###################################################################################
    #
    # Write parameters and their values
    #
    ###################################################################################

    def write_parameter_base(fp, id, map_table, name, values):
        """
        Write a parameter and its values
        """
        fp.write(f'    <Parameter id="{id}" name="{name}" type="1">\n')
        fp.write(f'      <values>\n')
        for value in sorted(values): # sort - to always have the same order
            fp.write(f'        <value>{value}</value>')
            if map_table:
                description = map_table.description(value[1:])
                fp.write(f'\t<!-- {description} -->')
            fp.write('\n')
        fp.write(f'      </values>\n')
        fp.write(f'    </Parameter>\n')

    def write_parameter(fp, id, map_table):
        """
        Write a parameter and its values
        """
        write_parameter_base(fp, id, map_table, map_table.name, map_table.values)

    fp.write('  <Parameters>\n')
    write_parameter(fp, 0, ai.inputs)
    write_parameter(fp, 1, ai.filters)
    write_parameter(fp, 2, ai.sinks)
    write_parameter(fp, 3, ai.eqs)
    write_parameter_base(fp, 4, None, 'COMPLEXITY', complexities)
    write_parameter_base(fp, 5, None, 'CONDITION', conditions)
    fp.write('  </Parameters>\n')

    ###################################################################################
    #
    # Write constraints
    #
    ###################################################################################

    hq = '&quot;' # HTML for quote character

    def write_constraint(fp, expr, parameters):
        """
        Write a constraint.  Listing the parameters doesn't seem to be necessary.
        """
        fp.write(f'    <Constraint text="{expr}">\n')
        fp.write(f'      <Parameters>\n')
        # ACTS doesn't seem to need these
        # for parameter in parameters:
        #     fp.write(f'        <Parameter name="{parameter}" />\n')
        fp.write(f'      </Parameters>\n')
        fp.write(f'    </Constraint>\n')

    def make_constraint_union(values, parameter):
        """
        Make the constraint string for a union of parameter values.  That is, from a
        set of values (strings), make a constraint specifying 'any of these', e.g.
        'PARAM == val1 || PARAM == val2 || PARAM == val3'
        """
        return ' || '.join([f'{parameter} == {hq}{value}{hq}'
						# sort - to always have the same order
						for value in sorted(values)])

    fp.write('  <Constraints>\n')

    if len(bare_complexities) > 0:
        # make the constraint for complexities that do not use a condition
        bc_string = make_constraint_union(bare_complexities, 'COMPLEXITY')
        write_constraint(fp,
                    f'({bc_string}) =&gt; CONDITION == {hq}{no_condition}{hq}',
                              ['COMPLEXITY', 'CONDITION'])

    clothed_complexities = (complexities - bare_complexities) - {no_complexities}
    if len(clothed_complexities) > 0:
        # make the constraint for complexities that must use a condition
        cc_string = make_constraint_union(clothed_complexities, 'COMPLEXITY')
        write_constraint(fp,
                    f'({cc_string}) =&gt; CONDITION != {hq}{no_condition}{hq}',
                              ['COMPLEXITY', 'CONDITION'])

    if no_complexities in complexities:
        # if a case has no complexity, it should not have a condition either
        write_constraint(fp,
                    f'COMPLEXITY == {hq}{no_complexities}{hq} =&gt; CONDITION == {hq}{no_condition}{hq}',
                              ['COMPLEXITY', 'CONDITION'])

    # make constraints for inputs, filters, and exec_queries based on choice of sink
    for sink_value in sink_inputs:
        # input constraints from choice of sink
        i_string = make_constraint_union(sink_inputs[sink_value], 'INPUT')
        # filter constraints from choice of sink
        f_string = make_constraint_union(sink_filters[sink_value], 'FILTER')
        # exec_query constraints from choice of sink
        eq_string = make_constraint_union(sink_eqs[sink_value], 'EXEC_QUERY')
        write_constraint(fp,
                f'SINK == {hq}{sink_value}{hq} =&gt; ({i_string}) &amp;&amp; ({f_string}) &amp;&amp; ({eq_string})',
                              ['SINK', 'INPUT', 'FILTER', 'EXEC_QUERY'])

    # make constraints for any filters that take NO complexities
    for filter_value in filter_has_complexities:
        if not filter_has_complexities[filter_value]:
            write_constraint(fp,
                f'FILTER == {hq}{filter_value}{hq} =&gt; COMPLEXITY == {hq}{no_complexities}{hq}',
                              ['FILTER', 'COMPLEXITY'])

    fp.write('  </Constraints>\n')

    # return the ACTS interface object so that ACTS result reader can translate
    # from values back to modules, complexities, and conditions.
    return ai 

def write_cases(file_path, cases):
    """
    Write the ACTS description of the cases to the given file_path.
    """

    with open(file_path, "w") as fp:
        fp.write('<?xml version="1.0" encoding="UTF-8"?>\n')

        fp.write('<System name="VTSG">\n')

        ai = write_parameters_and_constraints(fp, cases)

        # OutputParameters?

        # Relations?

        fp.write('</System>\n')

    return ai


def run_ACTS(file_path, ACTS_output):
    """
    Run ACTS on the given file_path.  Results are in ACTS_output.
    """

    import os

    # SKIMP - Default is 2-way coverage.  Allow for different coverages.
    ACTS_photo = 'TestPhoto_ACTS'
    if os.path.exists(ACTS_photo):
        os.remove(ACTS_photo) # don't let previous output confuse the success test
    # put std out and err in a file to not mess up expected results, then check success
    expected = os.system(f'java -Doutput=csv -jar ACTS3.2/acts_3.2.jar {file_path} {ACTS_output} > {ACTS_photo} 2>&1;[ "$(tail -1 {ACTS_photo}|cut -c -13)" = "Output file: " ]')
    if expected != 0:
        # ACTS command line output was not what we expected
        print(f'[ERROR] unexpected ACTS output, which is in {ACTS_photo}')
        import sys
        sys.exit(1)


def read_selections(ACTS_output_file, cases, ai):
    """
    Read the cases that ACTS picks.  Select them from the generated cases.
    """

    def matching_case(cases, ival, fval, sval, eqval, cpxval, cndval):
        """
        Return a case that matches the values.  If no match, return None.
        """
        imod = ai.inputs.module(ival)
        fmod = ai.filters.module(fval)
        smod = ai.sinks.module(sval)
        eqmod = ai.eqs.module(eqval)
        if ACTS_print_debug_output:
            print(f'Find I {ival} {imod.module_description if imod is not None else "(none)"}', end='')
            print(f'  F {fval} {fmod.module_description if fmod is not None else "(none)"}', end='')
            print(f'  S {sval} {smod.module_description}', end='')
            print(f'  EQ {eqval} {eqmod.module_description if eqmod is not None else "(none)"}', end='')
            print(f'  CPX {cpxval}', end='')
            print(f'  CND {cndval}')
        for c in cases:
            # SKIMP - this matches at most one complexity
            if len(c.complexity_list) > 0:
                cpx_id = f'PX{c.complexity_list[0].id}'
                if c.complexity_list[0].cond_id:
                    cnd_id = f'ND{c.complexity_list[0].cond_id}'
                else:
                    cnd_id = 'NONE'
            else:
                cpx_id = 'P0'
                cnd_id = 'NONE'
            if (imod == c.input and fmod == c.filter and smod == c.sink and
                eqmod == c.exec_query and cpxval == cpx_id and cndval == cnd_id):
                return c

        # No VTSG case matches this combination of values
        return None

    selected_test_cases = []

    with open(ACTS_output_file, "r") as fp:
        # skip the comment lines
        for line in fp:
            if line[0] != '#':
                break

        # at this point, the content of "line" is the parameter names, e.g. INPUT,FILTER,SINK,...

        # read each case (line)
        for line in fp:
            values = line.rstrip().split(',')
            # remove leading labeling character, like I*, F*, and S*
            (ival, fval, sval, eqval, cpxval, cndval) = [value[1:] for value in values]
            # find a matching test case
            case = matching_case(cases, ival, fval, sval, eqval, cpxval, cndval)
            if case:
                if ACTS_print_debug_output: print(case)
                selected_test_cases.append(case)
            else:
                import sys
                print(f'NO CASE FOUND FOR I{ival}, F{fval}, S{sval}, E{eqval}, C{cpxval}, C{cndval}')
                sys.exit(1)

    return selected_test_cases


def select_cases_ACTS(cases):
    """
    Select test cases by automated combinatorial testing (ACTS).
    Step 1: Write descriptions of the cases to a file.
    Step 2: Invoke ACTS.
    Step 3: Read the case descriptions selected by ACTS.
    Step 4: Return matching cases.
    """

    # pick a "random" suffix from 00000 to 99999
    #from random import randint
    #randophane = f'{randint(0, 99999):05}'
    ACTS_XML_file = '/tmp/VTSG_ACTS_input.xml'
    ACTS_output   = '/tmp/VTSG_ACTS_output.txt'

    ai = write_cases(ACTS_XML_file, cases)

    run_ACTS(ACTS_XML_file, ACTS_output)

    return read_selections(ACTS_output, cases, ai)

# end of select_by_acts.py
