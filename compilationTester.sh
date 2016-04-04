#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Checks if generated files compile properly"
    echo "Usage : ./compilationTester.sh [-s] <Path_to_latest_generation>"
    exit
fi

path=$1
ctr=0
dll="-r:dll/Npgsql.dll \
     -r:dll/Mono.Data.Sqlite.dll \
     -r:dll/System.Data.SQLite.DLL\
     -r:dll/MySql.Data.dll\
     -r:dll/System.Xml.Linq.dll\
     -r:dll/System.Xml.XDocument.dll\
     "

if [ -a success.exe ]; then rm success.exe ; fi

for file in `find $1 -name *File1.cs -print | sort -V`; do
    ctr=$((ctr+1))
    file=${file/File1.cs/*}
    mcs -pkg:dotnet $dll -lib:/usr/lib/mono/2.0/ $file -out:success.exe > /dev/null 2>&1
    if [ -a success.exe ];then
        echo -e "\033[0;32m\033[1m[PASSED]\033[m\033[0m $file"
        rm success.exe
    else
        echo -e "\033[0;31m\033[1m[FAILED]\033[m\033[0m $file : "
        mcs -pkg:dotnet $dll -lib:/usr/lib/mono/2.0/ $file -out:success.exe -v 2>&1
    fi
done
echo $ctr
if [ -a success.exe ]; then rm success.exe ; fi
