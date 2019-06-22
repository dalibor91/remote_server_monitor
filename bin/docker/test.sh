#!/usr/bin/env bash

######################################################### Code

. bin/bash/vars

bin/service start >> /tmp/service_start

cd test

python3 -m unittest discover --pattern=*.py

if ! [ $? -eq 0 ];
then
    exit 1;
fi

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

bin/service stop >> /tmp/service_stop

######################################################### Service

echo "Testing service:"

bin/service start >> /tmp/service_start

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

if [ "`bin/service status`" = "running" ];
then
    echo "Service reports as running. OK";
else
    echo "Service reports as not running";
    exit 1;
fi

bin/service stop >> /tmp/service_stop

if [ -f "${LOCK_FILE}" ];
then
    echo "Lock file still exists after stop: ${LOCK_FILE}"
    exit 1;
else
    echo "Lock file removed. OK"
fi;

if [ "`bin/service status`" = "not running" ];
then
    echo "Service reports as not running. OK";
else
    echo "Service reports as running";
    exit 1;
fi

######################################################### Install
echo "Testing install:"

bin/bash/install >> /tmp/install

if ! [ $? -eq 0 ];
then
    echo "Unable to install";
    cat /tmp/install
    exit 1;
fi

SERVICES="${SERVICE_LOCATION} ${SERVER_LOCATION} ${USERS_LOCATION} ${CLIENT_LOCATION}"
for service_file in $SERVICES;
do
    if ! [ "`which "$(basename ${service_file})"`" = "${service_file}" ];
    then
        echo "${service_file} not found!";
        exit 1
    else
        echo "Found `which "$(basename ${service_file})"`. OK"
    fi
done
