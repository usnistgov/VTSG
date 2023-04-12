# *created  "Wed Aug 26 15:06:04 2020" *by "Paul E. Black"
# *modified "Wed Apr 12 14:55:26 2023" *by "Paul E. Black"

TARGET=vulTestSuiteGenV3

DETEX=detex

UNAME_S = $(shell uname -s)
ifeq (${UNAME_S},Linux)
# Ubuntu
SHOW_PDF = evince
endif
ifeq (${UNAME_S},Darwin)
# MacOS
SHOW_PDF = preview
endif

all: ${TARGET}.pdf
	${SHOW_PDF} $^ &

.SUFFIXES: .tex .spell

.tex.spell:
	rm -f $@.new
	# remove URLs - they have lots of crazy "words"
	${DETEX} ${TARGET}.tex ${TARGET}.bbl | perl -pwe 's|https?://[a-z.]+/[-/._?=a-zA-Z0-9]+||g' | aspell list | sort -u > $@.new
	# only report new words (don't worry if nothing is reported)
	-diff $@.new $@ | grep '^<'

spell:	${TARGET}.spell

${TARGET}.spell: ${TARGET}.tex ${TARGET}.bbl

vulTestSuiteGenV3.bbl: vulTestSuiteGenV3.bib vulTestSuiteGenV3.tex
	bibtex ${@:.bbl=}
	# remove empty fields (comma followed by another comma or period)
	# remove periods after question marks
	mv $@ $@.orig
	perl -pwe 'while(/, [,.]/){s/, ([,.])/$$1/;s/\?[.]/?/}' $@.orig|tee $@ > /dev/null

fig_example_code1.png: fig_example_code1.tif
	echo export as .png
	gimp $^

fig_example_code2.png: fig_example_code2.tif
	echo export as .png
	gimp $^

vulTestSuiteGenV3.pdf: vulTestSuiteGenV3.tex \
	    vulTestSuiteGenV3.bbl \
	    fig_Complexity_file_method.png fig_Input_file.png \
	    fig_Complexity_file_test.png fig_Sink_file.png \
	    fig_Complexity_file_while.png fig_VTSG_overview.png \
	    fig_Exec_Query_file.png fig_Filter_file.png \
	    fig_example_code1.png fig_example_code2.png
	pdflatex vulTestSuiteGenV3.tex

# end of Makefile
