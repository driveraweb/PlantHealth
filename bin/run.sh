#!/bin/sh
#
# File: run.sh
#
# To automatically run the PlantHealth application at RaspberryPi
# startup, add /path/to/PlantHealth/bin/run.sh in the .bashrc file
#

python3 ../../Downloads/ivport-v2/init_ivport.py&
i2cdetect -y 1
python3 ../planthealth/main.py 

