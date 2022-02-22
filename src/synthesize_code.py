# *created  "Mon Aug  3 16:47:40 2020" *by "Paul E. Black"
# *modified "Tue Feb 22 16:48:07 2022" *by "Paul E. Black"
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
    indentMO = re.search('\n([^{\n]*){{\s*'+var_name+'\s*}}', template_code)
    # SKIMP - what if there is no {{ var_name }}?
    return indentMO.group(1)


def make_assign(left_hand_side, right_hand_side, language_template_class):
    '''Synthesize an assignment statement appropriate for this programming language
       from the lhs and rhs passed, e.g.,
            lhs = rhs;
       Proper indentation and newline must be added separately.'''
    statement_terminator = language_template_class.statement_terminator
    return left_hand_side + " = " + right_hand_side + statement_terminator

# end of synthesize_code.py
