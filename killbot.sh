#!/bin/bash
echo "******************"

echo "RFC: Kill drive.py"
sudo pkill -ef -9 "python.*drive\.py"
touch /home/pi/RFCBot/killedonshutdown
echo "******************"
