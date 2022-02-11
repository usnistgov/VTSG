# *created  "Tue Jul 28 09:17:42 2020" *by "Paul E. Black"
# *modified "Fri Feb 11 11:53:22 2022" *by "Paul E. Black"

default: test020

all: test

test: testCSharp testPHP testPython testSTerm

# test directory, relative to the new directory
TDIR = ../../tests

# Time Stamp - matches name VTGS chooses for the TestSuite
TS=$$(date +"%m-%d-%Y_%Hh%Mm%S")

# this takes four minutes and produces 33k cases
testCSharp: src/complexities_generator.py src/file_template.py
	python3 test_suite_gen.py -l cs | tee TestPhoto_$(TS)_CSharp_photo 2>&1
	diff `ls -dt TestPhoto_*_CSharp_photo` tests/CSharp_photo
	(cd `ls -dt TestSuite_*/CSharp | head -1`;pwd;for f in `find . -name "*.cs"`; do cmp $$f $(TDIR)/CSharp/$$f;done;for m in `find . -name "manifest.xml"`; do echo $$m;$(TDIR)/cmp_manifests.py $$m $(TDIR)/CSharp/$$m;done)

# generation takes about 25 minutes and produces almost 300k cases
# checking takes about six minutes
testPHP: src/complexities_generator.py src/file_template.py
	python3 test_suite_gen.py -l php | tee TestPhoto_$(TS)_PHP_photo 2>&1
	diff `ls -dt TestPhoto_*_PHP_photo` tests/PHP_photo
	(cd `ls -dt TestSuite_*/PHP | head -1`;pwd;for f in `find . -name "*.php"`; do cmp $$f $(TDIR)/PHP/$$f;done;for m in `find . -name "manifest.xml"`; do echo $$m;$(TDIR)/cmp_manifests.py $$m $(TDIR)/PHP/$$m;done)

# this produces 185 cases
testPython: src/complexities_generator.py src/file_template.py
	python3 test_suite_gen.py -l python | tee TestPhoto_$(TS)_Python_photo 2>&1
	diff `ls -dt TestPhoto_*_Python_photo` tests/Python_photo
	(cd `ls -dt TestSuite_*/Python | head -1`;pwd;for f in `find . -name "*.py"`; do cmp $$f $(TDIR)/Python/$$f;done;for m in `find . -name "manifest.xml"`; do echo $$m;$(TDIR)/cmp_manifests.py $$m $(TDIR)/Python/$$m;done)
# execute each file.  timeout for infinite loops
#	(cd `ls -dt TestSuite_* | head -1`;pwd;for f in `find . -name "*.py"`; do echo $f; timeout 3 python3 $f;done) | more

test010: src/complexities_generator.py src/file_template.py
	python3 test_suite_gen.py -l $@
	(cd `ls -dt TestSuite_* | head -1`;pwd;for f in `find . -name "*.py"`; do echo $$f; diff $$f $(TDIR)/SuiteTest010/$$f;done)

# tests for statement_terminator
testSTerm: test011 test012 test013 test014

test011: src/complexities_generator.py src/file_template.py
	python3 test_suite_gen.py -l $@
	(cd `ls -dt TestSuite_*/test011 | head -1`;pwd;for f in `find . -name "*.py"`; do echo $$f; diff $$f $(TDIR)/test011/$$f;done)

test012: src/complexities_generator.py src/file_template.py
	python3 test_suite_gen.py -l $@
	(cd `ls -dt TestSuite_*/test012 | head -1`;pwd;for f in `find . -name "*.py"`; do echo $$f; diff $$f $(TDIR)/test012/$$f;done)

test013: src/complexities_generator.py src/file_template.py
	python3 test_suite_gen.py -l $@
	(cd `ls -dt TestSuite_*/test013 | head -1`;pwd;for f in `find . -name "*.py"`; do echo $$f; diff $$f $(TDIR)/test013/$$f;done)

test014: src/complexities_generator.py src/file_template.py
	python3 test_suite_gen.py -l $@
	(cd `ls -dt TestSuite_*/test014 | head -1`;pwd;for f in `find . -name "*.py"`; do echo $$f; diff $$f $(TDIR)/test014/$$f;done)

test020: src/complexities_generator.py src/file_template.py src/manifest.py src/sarif_writer.py
	python3 test_suite_gen.py -l $@
	-(cd `ls -dt TestSuite_* | head -1`;pwd;for f in `find . -name "*.sarif"`; do echo $$f; cat $$f;done)|more

# end of Makefile
