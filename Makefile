# *created  "Tue Jul 28 09:17:42 2020" *by "Paul E. Black"
# *modified "Fri Mar 11 08:40:10 2022" *by "Paul E. Black"

default: test020

all: test

test: test010 testSTerm testCLI testPython testCsharp testPHP

VTSG_FILES=src/complexities_generator.py src/complexity.py src/condition.py \
	src/exec_query.py src/file_manager.py src/file_template.py \
	src/filtering_sample.py src/generator.py src/input_sample.py \
	src/manifest.py src/sample.py src/sink_sample.py src/synthesize_code.py

# this takes four minutes and produces 33k cases
testCsharp: $(VTSG_FILES)
	tests/gen_and_check cs

# generation takes about 25 minutes and produces almost 300k cases
# checking takes about six minutes
testPHP: $(VTSG_FILES)
	tests/gen_and_check php

# this produces 185 cases
testPython: $(VTSG_FILES)
	tests/gen_and_check py
# execute each file.  timeout for infinite loops
#	(cd $$(ls -dt TestSuite_* | head -1);pwd;for f in $$(find . -name "*.py"); do echo $f; timeout 3 python3 $f;done) | more

TDIR = ../../tests

# test for unsafe file WITHOUT {{flaw}}
# test flaw types other than CWE_*
# test flaw groups other than OWASP_*
test010: $(VTSG_FILES)
	python3 vtsg.py -l $@
	(cd $$(ls -dt TestSuite_*/test010 | head -1);pwd;for f in $$(find . -name "*.py"); do echo $$f; diff $$f $(TDIR)/test010/$$f;done)
	sleep 1

# tests for command line interface
testCLI: TestCLI1 TestCLI2 TestCLI3 TestCLI4 TestCLI5

# unknown language
TestCLI1:
	python3 vtsg.py --language=unknownLang | tee $(@)_photo
	diff $(@)_photo tests/$(@)_photo
	sleep 1

# flaw type not in the language
TestCLI2:
	python3 vtsg.py -l test010 -c CWE_99 | tee $(@)_photo
	diff $(@)_photo tests/$(@)_photo
	sleep 1

# generate one of the flaw types in the language
TestCLI3:
	python3 vtsg.py -l test010 --cwe=IDS00-PL | tee $(@)_photo
	(cd $$(ls -dt TestSuite_*/test010 | head -1);pwd;for f in $$(find . -name "*.py"); do echo $$f; diff $$f $(TDIR)/Test010/$$f;done) | grep -v TestSuite_ | tee -a $(@)_photo
	diff $(@)_photo tests/$(@)_photo
	sleep 1

# flaw group not in the language
TestCLI4:
	python3 vtsg.py -l test010 --flaw-group=Santa\ Monica | tee $(@)_photo
	diff $(@)_photo tests/$(@)_photo
	sleep 1

# generate one of the flaw groups in the language
TestCLI5:
	python3 vtsg.py -l test010 -f Zarahemla | tee $(@)_photo
	(cd $$(ls -dt TestSuite_*/test010 | head -1);pwd;for f in $$(find . -name "*.py"); do echo $$f; diff $$f $(TDIR)/Test010/$$f;done) | grep -v TestSuite_ | tee -a $(@)_photo
	diff $(@)_photo tests/$(@)_photo
	sleep 1

# tests for statement_terminator
testSTerm: test011 test012 test013 test014

test011: $(VTSG_FILES)
	python3 vtsg.py -l $@
	(cd $$(ls -dt TestSuite_*/test011 | head -1);pwd;for f in $$(find . -name "*.py"); do echo $$f; diff $$f $(TDIR)/test011/$$f;done)
	sleep 1

test012: $(VTSG_FILES)
	python3 vtsg.py -l $@
	(cd $$(ls -dt TestSuite_*/test012 | head -1);pwd;for f in $$(find . -name "*.py"); do echo $$f; diff $$f $(TDIR)/test012/$$f;done)
	sleep 1

test013: $(VTSG_FILES)
	python3 vtsg.py -l $@
	(cd $$(ls -dt TestSuite_*/test013 | head -1);pwd;for f in $$(find . -name "*.py"); do echo $$f; diff $$f $(TDIR)/test013/$$f;done)
	sleep 1

test014: $(VTSG_FILES)
	python3 vtsg.py -l $@
	(cd $$(ls -dt TestSuite_*/test014 | head -1);pwd;for f in $$(find . -name "*.py"); do echo $$f; diff $$f $(TDIR)/test014/$$f;done)

test020: $(VTSG_FILES) src/sarif_writer.py
	python3 vtsg.py -l $@
	-(cd $$(ls -dt TestSuite_* | head -1);pwd;for f in $$(find . -name "*.sarif"); do echo $$f; cat $$f;done)|more

# end of Makefile
