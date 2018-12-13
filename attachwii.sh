#!/bin/bash
sleep 1 # Wait until Bluetooth services are fully initialized
hcitool dev | grep hci >/dev/null
if test $? -eq 0 ; then
    echo "Launching wminput"
    # RFC10
    wminput -d -c  /home/pi/RFCBot/mywminput 00:17:AB:29:52:2A > /dev/null 2>&1 &    
    # RFC11
    #wminput -d -c  /home/pi/RFCBot/mywminput 00:17:AB:28:A5:47 > /dev/null 2>&1 &
    # RFC12    
    #wminput -d -c  /home/pi/RFCBot/mywminput 00:17:AB:25:62:2F > /dev/null 2>&1 &
    # RFC13
    #wminput -d -c  /home/pi/RFCBot/mywminput 00:17:AB:35:95:60 > /dev/null 2>&1 &
else
    echo "Blue-tooth adapter not present!"
    exit 1
fi

