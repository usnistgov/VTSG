# *created  "Mon Aug  3 16:47:40 2020" *by "Paul E. Black"
# *modified "Mon Sep 12 16:53:00 2022" *by "Paul E. Black"
"""
Functions to synthesize pieces of code.
"""

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

import re

def get_indent(var_name, template_code):
    '''Get the indentation before {{ var_name }} in template_code.  For instance,
       if var_name is "local_var" and template_code has
           {{ local_var }}
       (that is, four spaces before {{ local_var }}) then return "    " (that is,
       the four spaces).  Indentation may be empty string.
    '''
    # find indentation before {{ var_name }}
    indentMO = re.search('\n([^{\n]*){{-?\s*'+var_name+'\s*-?}}', template_code)
    # SKIMP - what if there is no {{ var_name }}?
    return indentMO.group(1)


def make_assign(left_hand_side, right_hand_side, language_template_class):
    '''Synthesize an assignment statement appropriate for this programming language
       from the lhs and rhs passed, e.g.,
            lhs = rhs;
       Proper indentation and newline must be added separately.'''
    statement_terminator = language_template_class.statement_terminator
    return left_hand_side + " = " + right_hand_side + statement_terminator


def fix_indents(code, indent):
    ''' Fix up all the indentation within INDENT ... ENDINDENT sections in the code.

        This processes the code line by line. Sections to be fixed are indicated by
        a line beginning with INDENT, possibly with leading whitespace, and continue
        to a line with ENDINDENT, again possibly with leading whitespace. Lines
        beginning with INDENT or ENDINDENT are removed. INDENT...ENDINDENT sections
        may be nested.
        For lines in an INDENT...ENDINDENT section,
            Step 1. Remove all leading whitespace.
            Step 2. Add indent (string) for each nested INDENT...ENDINDENT section
                this is in if the line has non-whitespace.
        For instance, consider the following code.

      if Condition:
INDENT            text after INDENT is ignored
           line 1
               while not True:
          INDENT
           line 3 - INDENT not at the beginning is ignored
     ENDINDENT

                  line above is empty
        ENDINDENT
        line 5

        If file_template.xml specifies <indent>..,</indent>, this is the result.
        (Note: typically, the indent is four spaces. The above string with periods
        and a comma is only for example clarity.)

      if Condition:
..,line 1
..,while not True:
..,..,line 3 - INDENT not at the beginning is ignored

..,line above is empty
        line 5

        Return the code with indentation fixed.
'''
    indent_depth = 0
    final_content = ''
    for line in code.splitlines():
        if re.match('^\s*INDENT', line):
            indent_depth += 1
        elif re.match('^\s*ENDINDENT', line):
            assert indent_depth > 0 # ENDINDENT without a matching INDENT
            indent_depth -= 1
        else:
            if indent_depth > 0:
                # properly indent this line
                # step 1: remove all leading whitespace
                line = re.sub(r'^\s*', '', line)
                if line != '':
                    # step 2: add indent_depth indents
                    line = (indent * indent_depth) + line
            final_content += line + '\n'
    assert indent_depth == 0 # INDENT line without a matching ENDINDENT

    return final_content

# end of synthesize_code.py
