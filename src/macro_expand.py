"""
Macro Expansion.

Utilities for macro expansion.

  *created "Fri Jan 26 13:45:44 2024" *by "Paul E. Black"
 *modified "Thu Feb  1 14:46:10 2024" *by "Paul E. Black"
"""

import sys
import re

def macro_expand(source, **kwargs):
    """
    Apply macros in parameters passed to the text passed.  Return the processed text.
    For example,
        text = "Source text {{ a_macro}} {{not_replaced}} {{a_macro}} the end."
        print(macro_expand(text, a_macro='see?'))
    prints
        Source text {not a macro} see? {{not_replaced}} see? the end.
    Any macros not given as parameters are ignored.

    Specifications
    Macros in text match {{\s*[a-zA-Z_][a-zA-Z_0-9]*\s*}}.  In words, macros begin
    and end with pairs of curly brackets.  The macro name begins with a letter or
    underscore followed by alphanumeric characters or underscores.  (This is the same
    as Python variable names.)  The name may have arbitrary white space, including
    newlines, before or after.
    """

    assert type(source) == str, f'type of source is {type(source)}, not str'

    t = source # so we don't modify the passed parameter

    for k, v in kwargs.items():
        pat = re.compile('{{\s*' + k + '\s*}}')
        #print(f'{pat=}')
        t = pat.sub(v, t)

    return t

if __name__ == "__main__":
    def test_macro_expand(source, expected, **kwargs):
        result = macro_expand(source, **kwargs)
        if result != expected:
            print('Test failed. Invocation:')
            print(f'macro_expand("{source}"', end='')
            for k, v in kwargs.items():
                print(f', {k}="{v}"', end='')
            print(')')
            print(f'Result is "{result}"')
            print(f'      not "{expected}"')
            sys.exit(1)

    test_macro_expand('', '')
    test_macro_expand('', '', a_macro = 'see?', _='', p='p=')
    test_macro_expand('macro \superset param {{long_macro_name}} er',
                      'macro \superset param {{long_macro_name}} er',
                      macro_name='oops')
    test_macro_expand('macro \subset param {{macro_name}} er',
                      'macro \subset param {{macro_name}} er',
                      long_macro_name='oops')
    test_macro_expand('unterminated macro {{ 	macro_name\t\n ',
                      'unterminated macro {{ 	macro_name\t\n ',
                      macro_name='r t')
    test_macro_expand('terminated macro {{ 	macro_name\t\n }}',
                      'terminated macro r t',
                      macro_name='r t')
    test_macro_expand('simple occur {{ 	m}} {{no_match}} <<end',
                      'simple occur !x! {{no_match}} <<end',
                      m='!x!')
    test_macro_expand('whitespace {{ \t	m \n }} {{no_match}} \n.\t.\n',
                      'whitespace x* {{no_match}} \n.\t.\n',
                      m='x*')
    test_macro_expand('multi occur {{ 	m}} {{n}} {{m}} er',
                      'multi occur hi? {{n}} hi? er',
                      m='hi?')
    test_macro_expand('multi occur {{ 	m}} {{n}} {{m}} er',
                      'multi occur hi? lo! hi? er',
                      m='hi?', n='lo!')
    test_macro_expand('nested macros 1 {{m }} {{n}} }}',
                      'nested macros 1 -$- $ }}',
                      m='-{{n}}-', n='$')
    test_macro_expand('nested macros 2 {{ {{m }} }} {{m}} {{n}} }}',
                      'nested macros 2 $ n $ }}',
                      m='n', n='$')
    test_macro_expand(r'recursive {{m}} \\back slash',
                      r'recursive -{{m}}- \\back slash',
                      m='-{{m}}-')
    test_macro_expand('mutally recursive {{m}}',
                      'mutally recursive -={{m}}=-',
                      m='-{{n}}-', n='={{m}}=')

    print('macro_expand.py self-test completed')

# end of macro_expand.py
