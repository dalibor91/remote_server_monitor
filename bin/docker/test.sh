#!/bin/bash 

. bin/bash/vars

bin/service start > /dev/null

cd test

python3 -m unittest discover --pattern=*.py

cd ..

# for debuging purposes
if ! [ "${SERVER_DEBUG}" = "" ];
then
    cat $LOG_FILE
fi

if [ $? -eq 0 ];
then
    echo "----------------------------------------------------------------------"
else
    echo "There are some errors. Please fix them."
    echo "Run tests with dbg option to see server logs"
    exit 1
fi

bin/service stop > /dev/null

echo "Testing service:"

bin/service start

if [ -f "${LOCK_FILE}" ];
then
    echo "Lock file created: ${LOCK_FILE}. OK"
else
    echo "Unable to create lock file ${LOCK_FILE}"
    exit 1;
fi;

if [ -f "${LOG_FILE}" ];
then
    echo "Log file created: ${LOG_FILE}. OK"
else
    echo "Unable to create log file ${LOG_FILE}"
    exit 1;
fi;

bin/service stop

if [ -f "${LOCK_FILE}" ];
then
    echo "Lock file still exists after stop: ${LOCK_FILE}"
    exit 1;
else
    echo "Lock file removed! OK"
fi;
