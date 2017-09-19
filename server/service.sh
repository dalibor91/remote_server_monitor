#!/bin/bash

LOCK_FILE=/var/lock/py_socket_server/pss.lock

LOCK_DIR=$(dirname $LOCK_FILE)

if [ ! -d "$LOCK_DIR" ];
then
	mkdir "$LOCK_DIR"
	if [ ! $? -eq 0 ]; 
       	then
		echo "Unable to create $LOCK_DIR";
		exit 1
	fi
fi

function _pid(){
	if [ -f "$LOCK_FILE" ];
	then
		cat $LOCK_FILE;
	fi
}

function _running() {
	local running=$(_pid)
	if [ ! "$running" = "" ];
	then
		kill -0 $running
		if [ $? -eq 0 ];
		then 
			echo "1"
		else 
			echo "0"
		fi
	else
		echo "0"
	fi
}

function _start() {

	local runing=$(_running)
	if [ "$runing" = "0" ];
	then 
		./server.py $@ >> ./server.log 2>&1 &
		if [ $? -eq 0 ];
		then
			echo $! > "$LOCK_FILE"
			echo "Running..."
			disown
		else
		       	echo "Unable to start..."	
		fi;
	else
		echo "Already runing!"
		exit 1;
	fi
}

function _stop() {
	local runing=$(_running)
	if [ "$runing" = "1" ];
	then
		kill $(_pid)
		rm $LOCK_FILE
		echo "Stoped"
	fi
}


if [ "$1" = "start" ];
then 
	_start $@
elif [ "$1" = "stop" ];
then 
	_stop
elif [ "$1" = "restart" ];
then
	_stop
	_start $@
else 
	echo "Unknown command"
	exit 1;
fi


