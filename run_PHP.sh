#!/bin/bash
#  *created "Mon Mar 18 13:42:11 2024" *by "Paul E. Black"
# *modified "Fri Jun 14 11:02:29 2024" *by "Paul E. Black"

if [ $# -ne 1 ]; then
    echo "Run generated PHP cases"
    echo "Usage: ./run_PHP.sh <Path_to_latest_generation>"
    exit
fi

path=$1
ctr=0 # number of cases run

attack_data=1776

OUTPUT_PHOTO=/tmp/runOutput.txt

# create a test file that some cases read
rm -f /tmp/tainted.txt
echo $attack_data > /tmp/tainted.txt

# create a test script that some cases execute
rm -f /tmp/tainted.sh
cat > /tmp/tainted.sh << END_OF_SCRIPT
echo $attack_data
END_OF_SCRIPT
chmod a+x /tmp/tainted.sh

# For info on colored text output, see https://en.wikipedia.org/wiki/ANSI_escape_code
# or https://wiki.archlinux.org/title/Bash/Prompt_customization

echo "Finding all cases. This may take a while . . ."
# find all cases generated - without auxiliary files, e.g., b.php, c.php, etc.
for file in $(find $path -name "[cC][wW][eE]_*[^bcde].php" | sort -V); do
    if [[ $file =~ I_POST__ || $file =~ I_SESSION__ ]];then
	# I don't know how to supply POST or SESSION data to the execution
	# write SKIPPED in yellow
        echo -e "\033[0;33m[SKIPPED]\033[0m $file"
	continue
    fi

    rm -f $OUTPUT_PHOTO # don't use old output
    # SKIMP - this does not supply anything to test _POST or _SESSION inputs.
    # run the program, define UserData for _GET
    php-cgi -f $file UserData=$attack_data > $OUTPUT_PHOTO 2>&1

    ctr=$((ctr+1))

    rm -f /tmp/unrecognizedOutput
    # ignore things we don't care about
    # SKIMP: this doesn't filter out stuff from 'ls' input, so that is judged to fail
    grep -Ev '^(  thrown in |Stack trace:|\#0 \{main\}|\s+$)|        <br />|:  Uncaught Error: Call to undefined function mysql_connect' $OUTPUT_PHOTO > /tmp/unrecognizedOutput

    if [ ! -s /tmp/unrecognizedOutput ];then
	# write PASSED in bold green
        echo -e "\033[0;1;32m[PASSED]\033[0m $file"
    else
	# write FAILED in bold red
        echo -e "\033[0;1;31m[FAILED]\033[0m $file"
        cat $OUTPUT_PHOTO
	echo Ran $ctr cases
	exit
    fi
done

rm -f $OUTPUT_PHOTO

echo Finished running all $ctr cases

# end of run_PHP.sh
