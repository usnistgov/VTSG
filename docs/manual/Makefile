# *created  "Wed Aug 26 15:06:04 2020" *by "Paul E. Black"
# *modified "Tue Feb  8 11:19:54 2022" *by "Paul E. Black"

TARGET=vulTestSuiteGenV3.pdf

all: ${TARGET}
	preview $^ &

vulTestSuiteGenV3.bbl: vulTestSuiteGenV3.bib vulTestSuiteGenV3.tex
	bibtex ${@:.bbl=}

vulTestSuiteGenV3.pdf: vulTestSuiteGenV3.tex \
	    vulTestSuiteGenV3.bbl \
	    fig_Complexity_file_method.png fig_Input_file.png \
	    fig_Complexity_file_test.png fig_Sink_file.png \
	    fig_Complexity_file_while.png fig_VTSG_overview.png \
	    fig_Exec_Query_file.png fig_Filter_file.png \
	    fig_example_code1.png fig_example_code2.png
	pdflatex vulTestSuiteGenV3.tex

# end of Makefile
