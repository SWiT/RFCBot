# RFCBot
# Python scripts for testing possible robot design

# Install Raspian "Stretch" Lite to microSD card.
# Set a Hostname, connect to wifi, enable SSH, localize, update, etc.
sudo raspi-config
#reboot

# Update all other packages
sudo apt update && sudo apt full-upgrade -y


sudo apt install -y git screen python-pip vlc

sudo pip install wiringpi



cd ~
git clone https://github.com/SWiT/RFCBot.git
sudo python RFCBot/test.py

raspivid -o - -t 0 -w 640 -h 480 -fps 30 |cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8160}' :demux=h264


http://192.168.1.8:8160
set caching to 0ms

