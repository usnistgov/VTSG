# C# Vulnerability test suite

Collection of vulnerable and fixed C# synthetic test cases expressing specific flaws.

Written in Python 3

## Dependencies

- Jinja2 (depends on MarkupSafe)
- Docopt
- Setuptools (for setup.py)
- Sphinx (for generating the doc)

You have three ways to install these dependencies

#### Using PIP

We encourage you to use pip ([installation instructions](https://pip.pypa.io/en/stable/)) to install these dependencies (choose one):

    - [sudo] pip3 install -r requirements.txt (as root, system-wide)
    - pip3 install --user -r requirements.txt (only for your user)

#### Using a Package Manager

You can also install this dependency with your package manager (if such a package exists in your distribution) :

    - [sudo] aptitude install python3-jinja2 (for GNU/Linux Debian for example)
    - [sudo] aptitude install python3-docopt
    - [sudo] aptitude install python3-setuptools
    - [sudo] aptitude install python3-sphinx

#### Manually Installation

Jinja2 installation instructions [here](http://jinja.pocoo.org/docs/dev/intro/#installation)

Docopt installation instructions [here](https://github.com/docopt/docopt#installation)

[Setuptools site](http://pythonhosted.org/setuptools/)

## Execute it

```sh
$ python3 test_cases_generator.py -l cs
```

## How to indent the generated source code ?

[Artistic](http://astyle.sourceforge.net/astyle.html) can indent C# source code.

Instructions :

```sh
$ ./astyle -r TestSuiteXXX*.cs --style=java --suffix=none --delete-empty-lines --indent-switches
```

where TestSuiteXXX*.cs is the path to the file you want to indent (it won't save a copy).

## Need help ?

```sh
$ python3 test_cases_generator.py --help
```

## Discussion

For discussion please send me an email at: Bertrand 'dot' STIVALET 'at' gmail.com
