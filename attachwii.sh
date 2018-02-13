#!/bin/bash

#exit 1

sleep 1 # Wait until Bluetooth services are fully initialized
hcitool dev | grep hci >/dev/null
if test $? -eq 0 ; then
	wminput -d -c  /home/pi/mywminput2 00:17:AB:25:62:2F > /dev/null 2>&1 &
	wminput -d -c  /home/pi/mywminput1 00:17:AB:35:95:60 > /dev/null 2>&1 &
else
	echo "Blue-tooth adapter not present!"
	exit 1
fi

