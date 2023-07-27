#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Check if generated C# files compile properly"
    echo "Usage: ./compilationTester.sh <Path_to_latest_generation>"
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

echo "Finding all cases. This may take a moment . . ."
# find all cases generated - without "second" files, e.g., b.cs or File2
for file in `find $path -name "[cC][wW][eE]_*[^b].cs" | grep -v File2 | sort -V`; do
    # remove suffixes to get a case name
    file=${file/_File1/}
    file=${file/a.cs/.cs}
    case=${file/.cs/}
    exec=${case}.exe
    files="${case}*.cs"
    rm -f $exec # don't use executable left over from a previous compile
    mcs -pkg:dotnet $dll -lib:/usr/lib/mono/2.0/ $files -out:$exec > compileOutput.txt 2>&1
    if [ -a $exec ];then
        ctr=$((ctr+1))
        echo -e "\033[0;32m\033[1m[PASSED]\033[m\033[0m $files"
    else
        echo -e "\033[0;31m\033[1m[FAILED]\033[m\033[0m $files"
        cat compileOutput.txt
	echo Compiled $ctr cases
	exit
    fi

    # run the executable
    mono $exec
done
echo Finished compiling $ctr cases

# end of compilationTester.sh
