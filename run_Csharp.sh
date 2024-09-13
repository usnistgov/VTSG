#!/bin/bash
# *modified "Fri Sep 13 07:53:00 2024" *by "Paul E. Black"

if [ $# -ne 1 ]; then
    echo "Check if generated C# cases compile and run properly"
    echo "Usage: ./run_Csharp.sh <Path_to_latest_generation>"
    exit
fi

path=$1
ctr=0 # number of cases compiled
dll="-r:dll/Npgsql.dll \
     -r:dll/Mono.Data.Sqlite.dll \
     -r:dll/System.Data.SQLite.DLL\
     -r:dll/MySql.Data.dll\
     -r:dll/System.Xml.XDocument.dll\
     "

# create a test file that some cases read
rm -f /tmp/tainted.txt
echo /etc/passwd > /tmp/tainted.txt

echo "Finding all cases. This may take a moment . . ."
# find all cases generated - without auxiliary files, e.g., b.cs, c.cs, etc.
for file in $(find $path -name "[cC][wW][eE]_*[^bcde].cs" | sort -V); do
    # remove suffixes to get a case name
    case=${file/a.cs/.cs}
    case=${case/.cs/}
    exec=${case}.exe
    files="${case}*.cs"
    rm -f $exec # don't use executable left over from a previous compile
    mcs -pkg:dotnet $dll -lib:/usr/lib/mono/2.0/ $files -out:$exec > compileOutput.txt 2>&1
    if [ -a $exec ];then
        ctr=$((ctr+1))
	# write PASSED in green
        echo -e "\033[0;1;32m[PASSED]\033[0m $files"
    else
	# write FAILED in red
        echo -e "\033[0;1;31m[FAILED]\033[0m $files"
        cat compileOutput.txt
	echo Compiled $ctr cases
	exit
    fi

    if [[ $exec =~ EQ_sql_server ]];then
	# Do not run EQL_sql_server cases because they take 20 seconds to time out,
	# which REALLY slows execution, considering there are thousands of cases.
	# write SKIPPED in yellow
        echo -e "\033[0;1;33m[SKIPPED]\033[0m $files"
	continue
    fi
    # run the executable
    echo /etc/passwd | mono $exec /etc/passwd
done

rm compileOutput.txt # remove the last compile output to leave a clean(er) directory

echo Finished compiling and running $ctr cases

# end of run_Csharp.sh
