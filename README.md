# RFCBot #
## Python scripts for testing possible robot design ##

### Install Raspian "Stretch" Lite to microSD card. ###

#### Set a Hostname, connect to wifi, enable SSH, localize, update, etc. ####
```
sudo raspi-config
reboot
```

#### Update all other packages. ####
`sudo apt update && sudo apt full-upgrade -y`

#### Install all the prerequisites. ####
```
sudo apt install -y git screen python-pip python-pygame vlc
sudo pip install wiringpi
```

#### Install RFCBot ####
```
cd ~
git clone https://github.com/SWiT/RFCBot.git
sudo python RFCBot/test.py
```

#### Start a video stream ####
```
raspivid -o - -t 0 -w 640 -h 480 -fps 30 |cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8160}' :demux=h264
```
http://192.168.1.8:8160
set caching to 0ms


#### Reverse SSH connections ####
```
ssh -R 2200:localhost:22 -R 8160:localhost:8160 USER@HOSTNAME
ssh -p 2200 pi@localhost
```
connect vlc to localhost:8160

#### Install and setup Wiimote controller ####
```
sudo apt-get install bluetooth vorbis-tools python-cwiid wminput

sudo tee /etc/udev/rules.d/wiimote.rules << EOF
KERNEL=="uinput", MODE="0666"
EOF

sudo reboot
```

#### Scan for a Wiimote BT address ####
```
hcitool scan
nano attachwii.sh
./attachwii.sh
```

#### Add "/home/pi/RFCBot/start.sh &" before the "exit 0" line ####
```
sudo nano /etc/rc.local
```
