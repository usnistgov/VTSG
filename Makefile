# *created  "Tue Jul 28 09:17:42 2020" *by "Paul E. Black"
# *modified "Wed Feb  9 14:40:16 2022" *by "Paul E. Black"

default: test020

all: test

test: testCSharp testPHP testPython testSTerm

# this takes four minutes and produces 33k cases
testCSharp: src/complexities_generator.py src/file_template.py
	python3 test_suite_gen.py -l cs
	(cd `ls -dt TestSuite_* | head -1`;pwd;for f in `find . -name "*.cs"`; do cmp $$f ../tests/SuiteCSharp/$$f;done;for m in `find . -name "manifest.xml"`; do echo $$m;../tests/cmp_manifests.py $$m ../tests/SuiteCSharp/$$m;done)

# generation takes about 25 minutes and produces almost 300k cases
# checking takes about six minutes
testPHP: src/complexities_generator.py src/file_template.py
	python3 test_suite_gen.py -l php
	(cd `ls -dt TestSuite_* | head -1`;pwd;for f in `find . -name "*.php"`; do cmp $$f ../tests/SuitePHP/$$f;done;for m in `find . -name "manifest.xml"`; do echo $$m;../tests/cmp_manifests.py $$m ../tests/SuitePHP/$$m;done)

# this produces 185 cases
testPython: src/complexities_generator.py src/file_template.py
	python3 test_suite_gen.py -l python
	(cd `ls -dt TestSuite_* | head -1`;pwd;for f in `find . -name "*.py"`; do cmp $$f ../tests/SuitePython/$$f;done;for m in `find . -name "manifest.xml"`; do echo $$m;../tests/cmp_manifests.py $$m ../tests/SuitePython/$$m;done)
# execute each file.  timeout for infinite loops
#	(cd `ls -dt TestSuite_* | head -1`;pwd;for f in `find . -name "*.py"`; do echo $f; timeout 3 python3 $f;done) | more

test010: src/complexities_generator.py src/file_template.py
	python3 test_suite_gen.py -l $@
	(cd `ls -dt TestSuite_* | head -1`;pwd;for f in `find . -name "*.py"`; do echo $$f; diff $$f ../tests/SuiteTest010/$$f;done)

# test for new statement_terminator
testSTerm: test011 test012 test013 test014

test011: src/complexities_generator.py src/file_template.py
	python3 test_suite_gen.py -l $@
	-(cd `ls -dt TestSuite_* | head -1`;pwd;for f in `find . -name "*.py"`; do echo $$f; diff $$f ../tests/SuiteTest011/$$f;done)
	sleep 1

test012: src/complexities_generator.py src/file_template.py
	python3 test_suite_gen.py -l $@
	-(cd `ls -dt TestSuite_* | head -1`;pwd;for f in `find . -name "*.py"`; do echo $$f; diff $$f ../tests/SuiteTest012/$$f;done)
	sleep 1

test013: src/complexities_generator.py src/file_template.py
	python3 test_suite_gen.py -l $@
	-(cd `ls -dt TestSuite_* | head -1`;pwd;for f in `find . -name "*.py"`; do echo $$f; diff $$f ../tests/SuiteTest013/$$f;done)
	sleep 1

runtest013: # test013 This is always out of date and creates a new TestSuite_*
	find TestSuiteTest013 -name "*.py" -exec python3 {} \;

test014: src/complexities_generator.py src/file_template.py
	python3 test_suite_gen.py -l $@
	-(cd `ls -dt TestSuite_* | head -1`;pwd;for f in `find . -name "*.py"`; do echo $$f; diff $$f ../tests/SuiteTest014/$$f;done)

test020: src/complexities_generator.py src/file_template.py src/manifest.py src/sarif_writer.py
	python3 test_suite_gen.py -l $@
	-(cd `ls -dt TestSuite_* | head -1`;pwd;for f in `find . -name "*.sarif"`; do echo $$f; cat $$f;done)|more

# end of Makefile
