# *created  "Tue Jul 28 09:17:42 2020" *by "Paul E. Black"
# *modified "Thu Nov  3 10:53:39 2022" *by "Paul E. Black"

default: genPython

all: test generate

generate: genPython genCsharp genPHP

test: testVarious testCLI testSTerm testIndent
	@echo All built-in self-tests succeeded

VTSG_FILES=src/complexities_generator.py src/complexity.py src/condition.py \
	src/exec_query.py src/file_manager.py src/file_template.py \
	src/filtering_sample.py src/generator.py src/input_sample.py \
	src/manifest.py src/sample.py src/sink_sample.py src/synthesize_code.py

# this takes four minutes and produces 33k cases
genCsharp: $(VTSG_FILES)
	tests/gen_and_check cs

# generation takes about 25 minutes and produces almost 300k cases
# checking takes about six minutes
genPHP: $(VTSG_FILES)
	tests/gen_and_check php

# this produces 311 cases
genPython: $(VTSG_FILES)
	tests/gen_and_check py

TDIR = ../../tests

example: $(VTSG_FILES)
	python3 vtsg.py -l $@ -t tests/templates
	(cd $$(ls -dt TestSuite_*/example | head -1);pwd;for f in $$(find . -name "*.cs"|sort); do echo $$f; diff $$f $(TDIR)/example/$$f;done)
	sleep 1

testVarious: test001 test003 test004 test005 test006 test010
	@echo various tests succeeded

# test empty <import></import> string
test001:
	python3 vtsg.py -l $@ -t tests/templates | tee $(@)_photo
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

# test for unsafe file WITHOUT {{flaw}}
# test flaw types other than CWE_*
# test flaw groups other than OWASP_*
# test missing flaw group
test010: $(VTSG_FILES)
	python3 vtsg.py -l $@ -t tests/templates
	(cd $$(ls -dt TestSuite_*/test010 | head -1);pwd;for f in $$(find . -name "*.py"|sort); do echo $$f; diff $$f $(TDIR)/test010/$$f;done)
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

test011: $(VTSG_FILES)
	python3 vtsg.py -l $@ -t tests/templates
	(cd $$(ls -dt TestSuite_*/test011 | head -1);pwd;for f in $$(find . -name "*.py"|sort); do echo $$f; diff $$f $(TDIR)/test011/$$f;done)
	sleep 1

test012: $(VTSG_FILES)
	python3 vtsg.py -l $@ -t tests/templates
	(cd $$(ls -dt TestSuite_*/test012 | head -1);pwd;for f in $$(find . -name "*.py"|sort); do echo $$f; diff $$f $(TDIR)/test012/$$f;done)
	sleep 1

test013: $(VTSG_FILES)
	python3 vtsg.py -l $@ -t tests/templates
	(cd $$(ls -dt TestSuite_*/test013 | head -1);pwd;for f in $$(find . -name "*.py"|sort); do echo $$f; diff $$f $(TDIR)/test013/$$f;done)
	sleep 1

test014: $(VTSG_FILES)
	python3 vtsg.py -l $@ -t tests/templates
	(cd $$(ls -dt TestSuite_*/test014 | head -1);pwd;for f in $$(find . -name "*.py"|sort); do echo $$f; diff $$f $(TDIR)/test014/$$f;done)

# tests for fatal misuses of INDENT ... ENDINDENT
testIndent: test016 test017
	@echo test INDENT...ENDINDENT succeeded

test016: $(VTSG_FILES)
	@echo =====================================================================================
	@echo The next test should fail with INDENT line without a matching ENDINDENT
	@echo =====================================================================================
	sleep 2
	-python3 vtsg.py -l $@ -t tests/templates
	(cd $$(ls -dt TestSuite_*/test016 | head -1);pwd;for f in $$(find . -name "*.py"|sort); do echo $$f; diff $$f $(TDIR)/test016/$$f;done)
	sleep 1

test017: $(VTSG_FILES)
	@echo =====================================================================================
	@echo The next test should fail with ENDINDENT without a matching INDENT before generating any files
	@echo =====================================================================================
	sleep 2
	-python3 vtsg.py -l $@ -t tests/templates
	sleep 1

test020: $(VTSG_FILES) src/sarif_writer.py
	python3 vtsg.py -l $@ -t tests/templates
	-(cd $$(ls -dt TestSuite_*/test020 | head -1);pwd;for f in $$(find . -name "*.sarif"|sort); do echo $$f; cat $$f;done)|more

# remove stuff left from running built-in tests
clean:
	rm -rf TestSuite_* TestPhoto_* TestCLI*_photo test00*_photo

# end of Makefile
