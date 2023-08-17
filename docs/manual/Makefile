# *created  "Wed Aug 26 15:06:04 2020" *by "Paul E. Black"
# *modified "Thu Aug 17 16:53:01 2023" *by "Paul E. Black"

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

fig_example_code1.png: fig_example_code1.tif
	echo export as .png
	gimp $^

fig_example_code2.png: fig_example_code2.tif
	echo export as .png
	gimp $^

vulTestSuiteGenV3.pdf: vulTestSuiteGenV3.tex preamble.tex \
	    vulTestSuiteGenV3.bbl \
	    fig_Complexity_file_method.png fig_Input_file.png \
	    fig_Complexity_file_test.png fig_Sink_file.png \
	    fig_Complexity_file_while.png fig_VTSG_overview.png \
	    fig_Exec_Query_file.png fig_Filter_file.png \
	    fig_README_md.png fig_clone_tab.png fig_git_files.png \
	    fig_filters_and_sinks.png fig_input_filter_sink.png \
	    fig_inputs_filters_and_sinks.png fig_cartesian_product.png \
	    fig_example_code1.png fig_example_code2.png
	pdflatex vulTestSuiteGenV3.tex

# end of Makefile
