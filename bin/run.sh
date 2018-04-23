#!/bin/sh
#
# File: run.sh
#
# To automatically run the PlantHealth application at RaspberryPi
# startup, add /path/to/PlantHealth/bin/run.sh in the .bashrc file
#
python ../planthealth/main.py &
sleep 1 # delay for auto-run test