# *created  "Tue Jul 28 09:17:42 2020" *by "Paul E. Black"
# *modified "Mon Feb 14 12:54:27 2022" *by "Paul E. Black"

default: test020

all: test

test: testCSharp testPHP testPython testSTerm

VTSG=src/complexities_generator.py src/complexity.py src/condition.py \
	src/exec_query.py src/file_manager.py src/file_template.py \
	src/filtering_sample.py src/generator.py src/input_sample.py \
	src/manifest.py src/sample.py src/sink_sample.py src/synthesize_code.py

# this takes four minutes and produces 33k cases
testCSharp: $(VTSG)
	tests/gen_and_check cs

# generation takes about 25 minutes and produces almost 300k cases
# checking takes about six minutes
testPHP: $(VTSG)
	tests/gen_and_check php

# this produces 185 cases
testPython: $(VTSG)
	tests/gen_and_check py
# execute each file.  timeout for infinite loops
#	(cd `ls -dt TestSuite_* | head -1`;pwd;for f in `find . -name "*.py"`; do echo $f; timeout 3 python3 $f;done) | more

TDIR = ../../tests

test010: $(VTSG)
	python3 test_suite_gen.py -l $@
	(cd `ls -dt TestSuite_* | head -1`;pwd;for f in `find . -name "*.py"`; do echo $$f; diff $$f $(TDIR)/SuiteTest010/$$f;done)

# tests for statement_terminator
testSTerm: test011 test012 test013 test014

test011: $(VTSG)
	python3 test_suite_gen.py -l $@
	(cd `ls -dt TestSuite_*/test011 | head -1`;pwd;for f in `find . -name "*.py"`; do echo $$f; diff $$f $(TDIR)/test011/$$f;done)

test012: $(VTSG)
	python3 test_suite_gen.py -l $@
	(cd `ls -dt TestSuite_*/test012 | head -1`;pwd;for f in `find . -name "*.py"`; do echo $$f; diff $$f $(TDIR)/test012/$$f;done)

test013: $(VTSG)
	python3 test_suite_gen.py -l $@
	(cd `ls -dt TestSuite_*/test013 | head -1`;pwd;for f in `find . -name "*.py"`; do echo $$f; diff $$f $(TDIR)/test013/$$f;done)

test014: $(VTSG)
	python3 test_suite_gen.py -l $@
	(cd `ls -dt TestSuite_*/test014 | head -1`;pwd;for f in `find . -name "*.py"`; do echo $$f; diff $$f $(TDIR)/test014/$$f;done)

test020: $(VTSG) src/sarif_writer.py
	python3 test_suite_gen.py -l $@
	-(cd `ls -dt TestSuite_* | head -1`;pwd;for f in `find . -name "*.sarif"`; do echo $$f; cat $$f;done)|more

# end of Makefile
