#!/bin/bash
#Reverse SSH connections
ssh -R 2200:localhost:22 -R 8160:localhost:8160 switlik@elis-switlik.kl.oakland.edu

#To connect ssh back from host
#ssh -p 2200 pi@localhost
#connect vlc to localhost:8160


