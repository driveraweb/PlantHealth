#!/bin/sh
#
# File: run.sh
#
# To automatically run the PlantHealth application at RaspberryPi
# startup, add /path/to/PlantHealth/bin/run.sh in the .bashrc file
#

#initialize MUX
python3 ../../Downloads/ivport-v2/init_ivport.py& 
sleep 0.5s #wait for connection

#show MUX and PiCamera addresses
i2cdetect -y 1

#run main program
python3 ../planthealth/main.py 
