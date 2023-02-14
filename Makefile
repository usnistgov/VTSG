# *created  "Tue Jul 28 09:17:42 2020" *by "Paul E. Black"
# *modified "Tue Feb 14 09:36:21 2023" *by "Paul E. Black"

default: genPython

all: testAll generate

generate: genPython genCsharp genPHP

testAll: testVarious testCLI testSTerm testIndent testDeclVars
	@echo All built-in self-tests succeeded

VTSG_FILES=src/complexities_generator.py src/complexity.py src/condition.py \
	src/exec_query.py src/file_manager.py src/file_template.py \
	src/filter_sample.py src/generator.py src/input_sample.py \
	src/manifest.py src/sample.py src/sink_sample.py src/synthesize_code.py

# this takes four minutes and produces 33k cases
genCsharp: $(VTSG_FILES)
	tests/gen_and_check cs

# generation takes about 25 minutes and produces almost 300k cases
# checking takes about six minutes
genPHP: $(VTSG_FILES)
	tests/gen_and_check php

# this produces 2353 cases
genPython: $(VTSG_FILES)
	tests/gen_and_check py

TDIR = ../../tests

example: $(VTSG_FILES)
	python3 vtsg.py -l $@ -t tests/templates
	(cd $$(ls -dt TestSuite_*/example | head -1);pwd;for f in $$(find . -name "*.cs"|sort); do echo $$f; diff $$f $(TDIR)/example/$$f;done)
	sleep 1

testVarious: test001 test002 test003 test004 test005 test006 test007 test010
	@echo various tests succeeded

# test empty <import></import> string
test001:
	python3 vtsg.py -l $@ -t tests/templates | tee $(@)_photo
	diff $(@)_photo tests/$(@)_photo

# test that files are not overwritten (in case of duplicate <dir></dir>)
#   remove specific test suite directory from output
test002:
	python3 vtsg.py -l $@ -t tests/templates | perl -pwe 's|TestSuite_[^/]+|TestSuite_...|' | tee $(@)_photo
	diff $(@)_photo tests/$(@)_photo

# test empty <dir></dir> string
test003:
	python3 vtsg.py -l $@ -t tests/templates | tee $(@)_photo
	diff $(@)_photo tests/$(@)_photo

# test empty <flaw_type></flaw_type> string
test004:
	python3 vtsg.py -l $@ -t tests/templates | tee $(@)_photo
	diff $(@)_photo tests/$(@)_photo

# test empty <input_type></input_type> string
test005:
	python3 vtsg.py -l $@ -t tests/templates | tee $(@)_photo
	diff $(@)_photo tests/$(@)_photo

# test empty <exec_type></exec_type> string
test006:
	python3 vtsg.py -l $@ -t tests/templates | tee $(@)_photo
	diff $(@)_photo tests/$(@)_photo

# test empty <body></body> string in a complexity
test007:
	python3 vtsg.py -l $@ -t tests/templates | tee $(@)_photo
	diff $(@)_photo tests/$(@)_photo

# test for unsafe file WITHOUT {{flaw}}
# test flaw types other than CWE_*
# test flaw groups other than OWASP_*
# test missing flaw group
# test sink with no input (or filter)
test010: $(VTSG_FILES)
	python3 vtsg.py -l $@ -t tests/templates
	(cd $$(ls -dt TestSuite_*/$(@) | head -1);pwd;for f in $$(find . -name "*.py"|sort); do echo $$f; diff $$f $(TDIR)/$(@)/$$f;done)
	@echo $@ finished
	sleep 1

# tests for command line interface
testCLI: TestCLI1 TestCLI1a TestCLI2 TestCLI3 TestCLI4 TestCLI5
	@echo command line interface \(CLI\) tests succeeded

# unknown language
TestCLI1:
	python3 vtsg.py --language=unknownLang | tee $(@)_photo
	diff $(@)_photo tests/$(@)_photo

# unknown language in given directory; test --template-directory option
TestCLI1a:
	python3 vtsg.py -l cs --template-directory=/tmp | tee $(@)_photo
	diff $(@)_photo tests/$(@)_photo

# flaw type not in the language
TestCLI2:
	python3 vtsg.py -l test010 -f CWE_99 -t tests/templates | tee $(@)_photo
	diff $(@)_photo tests/$(@)_photo

# generate one of the flaw types in the language
TestCLI3:
	python3 vtsg.py -l test010 --flaw=IDS00-PL -t tests/templates | tee $(@)_photo
	(cd $$(ls -dt TestSuite_*/test010 | head -1);pwd;for f in $$(find . -name "*.py"|sort); do echo $$f; diff $$f $(TDIR)/test010/$$f;done) | grep -v TestSuite_ | tee -a $(@)_photo
	diff $(@)_photo tests/$(@)_photo
	sleep 1

# flaw group not in the language
TestCLI4:
	python3 vtsg.py -l test010 --group=Santa\ Monica -t tests/templates | tee $(@)_photo
	diff $(@)_photo tests/$(@)_photo

# generate one of the flaw groups in the language
TestCLI5:
	python3 vtsg.py -l test010 -g Zarahemla -t tests/templates | tee $(@)_photo
	(cd $$(ls -dt TestSuite_*/test010 | head -1);pwd;for f in $$(find . -name "*.py"|sort); do echo $$f; diff $$f $(TDIR)/test010/$$f;done) | grep -v TestSuite_ | tee -a $(@)_photo
	diff $(@)_photo tests/$(@)_photo
	sleep 1

# tests for statement_terminator
testSTerm: test011 test012 test013 test014
	@echo statement_terminator tests succeeded

# also, exercise strings as complexity and condition names
test011: $(VTSG_FILES)
	python3 vtsg.py -l $@ -t tests/templates
	(cd $$(ls -dt TestSuite_*/$(@) | head -1);pwd;for f in $$(find . -name "*.py"|sort); do echo $$f; diff $$f $(TDIR)/$(@)/$$f;done)
	sleep 1

# also, exercise two levels of complexity
test012: $(VTSG_FILES)
	python3 vtsg.py -l $@ -t tests/templates --depth=2
	(cd $$(ls -dt TestSuite_*/$(@) | head -1);pwd;for f in $$(find . -name "*.py"|sort); do echo $$f; diff $$f $(TDIR)/$(@)/$$f;done)
	sleep 1

test013: $(VTSG_FILES)
	python3 vtsg.py -l $@ -t tests/templates
	(cd $$(ls -dt TestSuite_*/$(@) | head -1);pwd;for f in $$(find . -name "*.py"|sort); do echo $$f; diff $$f $(TDIR)/$(@)/$$f;done)
	sleep 1

test014: $(VTSG_FILES)
	python3 vtsg.py -l $@ -t tests/templates
	(cd $$(ls -dt TestSuite_*/$(@) | head -1);pwd;for f in $$(find . -name "*.py"|sort); do echo $$f; diff $$f $(TDIR)/$(@)/$$f;done)

# tests for misuses of INDENT ... DEDENT
testIndent: test016 test017
	@echo test INDENT...ENDINDENT succeeded

test016: $(VTSG_FILES)
	python3 vtsg.py -l $@ -t tests/templates | tee $(@)_photo | head -2
	diff $(@)_photo tests/$(@)_photo

test017: $(VTSG_FILES)
	python3 vtsg.py -l $@ -t tests/templates | tee $(@)_photo | head -2
	diff $(@)_photo tests/$(@)_photo

# tests for inconsistent declaring local variables
testDeclVars: test020 test021
	@echo test inconsistent declaring local variables succeeded

# no {{local_var}}, but <variable ... /> given
test020: $(VTSG_FILES)
	python3 vtsg.py -l $@ -t tests/templates -r 0 | tee $(@)_photo
	diff $(@)_photo tests/$(@)_photo

# {{local_var}} given, but no <variable ... /> statements
test021: $(VTSG_FILES)
	python3 vtsg.py -l $@ -t tests/templates -r 0 | tee $(@)_photo
	diff $(@)_photo tests/$(@)_photo

testNNN: $(VTSG_FILES) src/sarif_writer.py
	python3 vtsg.py -l $@ -t tests/templates
	-(cd $$(ls -dt TestSuite_*/$(@) | head -1);pwd;for f in $$(find . -name "*.sarif"|sort); do echo $$f; cat $$f;done)|more

# remove stuff left from running built-in tests
clean:
	rm -rf TestSuite_* TestPhoto_* TestCLI*_photo test0*_photo

# end of Makefile
