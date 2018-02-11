# RFCBot
# Python scripts for testing possible robot design

# Install Raspian "Stretch" Lite to microSD card.
# Set a Hostname, connect to wifi, enable SSH, localize, update, etc.
sudo raspi-config
#reboot

# Update all other packages
sudo apt update && sudo apt full-upgrade -y


sudo apt install -y git screen python-pip

sudo pip install wiringpi



cd ~
git clone https://github.com/SWiT/RFCBot.git
sudo python RFCBot/test.py
