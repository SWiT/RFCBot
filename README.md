# RFCBot #
## Python scripts for testing possible robot design ##

#### Install Raspian "Stretch" Lite to microSD card. ####

#### Configure the RPi Zero W ####
Set a password, set a hostname, connect to wifi, wait for network on boot, localize, enable camera, enable SSH, and enable I2C.
```
sudo raspi-config
```
reboot

#### Install RFCBot ####
```
cd ~ && git clone https://github.com/SWiT/RFCBot.git
```

#### Update all packages. Update RPi firmware. Install all the required packages. ####
```
sudo apt update && sudo apt upgrade -y && sudo apt full-upgrade -y && sudo rpi-update && sudo apt install -y git screen python-pip python-pygame vlc build-essential python-dev bluetooth vorbis-tools python-cwiid wminput i2c-tools && sudo pip install wiringpi
```

#### Adafruit ADXL345 library ####
```
cd ~ && git clone https://github.com/adafruit/Adafruit_Python_ADXL345.git && cd Adafruit_Python_ADXL345 && sudo python setup.py install
```

#### Blacklist sound driver. ####
This frees up a timer for the servos 
```
sudo tee /etc/modprobe.d/raspi-blacklist.conf << EOF
blacklist snd_bcm2835
EOF
```

#### Setup Wiimote controller ####
```
sudo tee /etc/udev/rules.d/wiimote.rules << EOF
KERNEL=="uinput", MODE="0666"
EOF
```
Scan for a Wiimote BT addresses. Press 1 + 2.
```
hcitool scan
```
Replace the address in attachwii.sh
```
nano ~/RFCBot/attachwii.sh
```

#### Set scripts to start on bootup ####
Edit 
```
sudo nano /etc/rc.local
```
Add the following before the "exit 0" line.
```
/home/pi/RFCBot/startup.sh &
```
Reboot and press 1+2 on the Wiimote. If you don't the Rpi Zero W turns into a WiFi jammer of sorts and you'll lose network connection until you pair the wiimote or reboot. This can effect other WiFi devices.

#### Set scripts to stop on shutdown ####
The system will hang if the scripts are running at shutdown.
```
sudo ln -s /home/pi/RFCBot/killbot.sh /lib/systemd/system-shutdown/
```



#### Optional Stuff ####
#### Start a video stream ####
```
raspivid -o - -t 0 -w 640 -h 480 -fps 30 |cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8160}' :demux=h264
```
Set caching to 0ms on the VLC client.
http://192.168.1.8:8160

#### Reverse SSH connections (in case of firewalls) ####
```
ssh -R 2200:localhost:22 -R 8160:localhost:8160 USER@HOSTNAME
ssh -p 2200 pi@localhost
```
Connect VLC to localhost:8160




