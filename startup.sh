#!/bin/bash
echo "******************** Robot Fight Club Bot starting up. ********************"

# Attach Wiimote, start the drive.py script
/home/pi/RFCBot/attachwii.sh &
/usr/bin/python /home/pi/RFCBot/drive.py &

# Reverse port formwarding for SSH and VLC stream
#/home/pi/RFCBot/reverseconn.sh &

# Start the video stream
#/home/pi/RFCBot/streamvideo.sh &

# Run in Autonomus Robot mode
#???
