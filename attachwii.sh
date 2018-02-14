#!/bin/bash

#exit 1

sleep 1 # Wait until Bluetooth services are fully initialized
hcitool dev | grep hci >/dev/null
if test $? -eq 0 ; then
	wminput -d -c  /home/pi/RFCBot/mywminput1 00:17:AB:29:52:2A > /dev/null 2>&1 &
    echo "Blue-tooth adapter not present!"
else
	echo "Blue-tooth adapter not present!"
	exit 1
fi

