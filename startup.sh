#!/bin/bash
echo "******************** Robot Fight Club Bot starting up. ********************"

# Start the drive.py script
/usr/bin/python /home/pi/RFCBot/drive.py &

# SSH Reverse port forwarding for VLC streaming behind a firewall
#/home/pi/RFCBot/reverseconn.sh &

# Start the video stream
#/home/pi/RFCBot/streamvideo.sh &

# Run in Autonomus Robot mode
#???
