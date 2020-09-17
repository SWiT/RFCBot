# RFCBot #
## Python scripts for testing robot design ##

#### Install Raspian "Stretch" Lite to microSD card. ####

#### Configure the RPi Zero W ####
Set a password, set a hostname, connect to wifi, wait for network on boot, localize, enable camera, enable SSH, and enable I2C.
```
sudo raspi-config
```
reboot

#### Update all packages. Install all the required packages. Update RPi firmware. ####
```
sudo apt update && sudo apt upgrade -y && sudo apt full-upgrade -y && sudo apt install -y git screen python-pip python-pygame vlc build-essential python-dev bluetooth python-smbus i2c-tools python-pil python-setuptools vorbis-tools && sudo pip install wiringpi
sudo rpi-update
```

#### Install RFCBot ####
```
cd ~ && git clone https://github.com/SWiT/RFCBot.git
```

#### Adafruit ADXL345 library ####
```
cd ~ && git clone https://github.com/adafruit/Adafruit_Python_ADXL345.git && cd Adafruit_Python_ADXL345 && sudo python setup.py install
```
Test the sensor.
```
python ~/Adafruit_Python_ADXL345/examples/simpletest.py
```

#### Blacklist sound driver. ####
This frees up a timer for the servos 
```
sudo tee /etc/modprobe.d/raspi-blacklist.conf << EOF
blacklist snd_bcm2835
EOF
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
Edit startup.sh to enable the scripts you want.
```
nano /home/pi/RFCBot/startup.sh
```

#### Set scripts to stop on shutdown ####
The system will hang if the scripts are running at shutdown.
```
sudo ln -s /home/pi/RFCBot/killbot.sh /lib/systemd/system-shutdown/
```



### Optional Stuff ###

#### Pair Bluetooth Controller ####
```
sudo bluetoothctl
```
```
[bluetooth]# agent on
[bluetooth]# default-agent
[bluetooth]# scan on

Copy the devices XX:XX:XX:XX:XX:XX address.

[bluetooth]# scan off
[bluetooth]# pair XX:XX:XX:XX:XX:XX
[bluetooth]# connect XX:XX:XX:XX:XX:XX
[bluetooth]# trust XX:XX:XX:XX:XX:XX
[bluetooth]# quit
```

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

#### Create an Image of the SD Card ####
Remove excess wifi networks. Clean up any unused packages. Delete SSH keys etc.
```
~/RFCBot/killbot.sh
nano ~/RFCBot/startup.sh
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
sudo rm -f ~/.ssh/*
sudo apt autoremove
sudo poweroff
```

Pull the SD card and plug it into a Ubuntu Machine
```
sudo apt install dcfldd gparted
df -h
sudo umount /dev/sdX1 /dev/sdX2
sudo dcfldd sizeprobe=if if=/dev/sdX of=rfcbot.img
sudo sync
```
Remove the SD card.
Shrink the img file
```
cd ~ && git clone https://github.com/Drewsif/PiShrink.git
sudo ~/PiShrink/pishrink.sh rfcbot.img
zip -v rfcbot.zip rfcbot.img
rm rfcbot.img
```

#### Check Disk After Resize ####
It's worth running a disk check after the partition size it automatically expanded on first boot.
```
sudo touch /forcefsck
sudo shutdown -r -F now
```



#### OLED ####
```
cd ~
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git && cd Adafruit_Python_SSD1306 && sudo python setup.py install
```








