#!/bin/bash
/bin/echo "******************"
/bin/echo "RFC: Kill drive.py"
/usr/bin/sudo /usr/bin/pkill -ef -9 "python.*drive\.py"
#/bin/touch /home/pi/RFCBot/killed
/bin/echo "******************"
