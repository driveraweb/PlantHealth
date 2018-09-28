# Plant Health Measurement Device using NDVI

Being that changes in plant health may not be present upon visual inspection alone, it is necessary to have a cost-efficient method of visualizing plant health. This will result in increased awareness of declining plant health for common plant applications and allow for preemptive intervention efforts by the owner or overseer. 



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.



### Hardware 

This software was designed and implemented using the following hardware:
* RaspberryPi 3 B+
* 16GB Micro SD Card
* Pi NoIR Camera V2 
* Roscolux #2007 Storaro Blue filter
* Pi Camera V2
* IVPort V2 Pi Camera Multiplexer 
* Waveshare 7" Touchscreen Display
* 3W Infrared Illuminator (2)
* RAVPower 22000mAH 4.5A Portable Phone Power Pack



### Installing

A step-by-step series that tells you how to get a Plant Health imaging software running

[Install git](https://projects.raspberrypi.org/en/projects/getting-started-with-git/4)

[Install Python3](https://www.python.org/downloads/)

**Using your RaspberryPi Terminal**

Clone the PlantHealth repo:
```
git clone https://github.com/driveraweb/PlantHealth.git .
cd PlantHealth
```

Install the dependencies:
```
pip install -r requirements.txt
```

Make the program executable:
```
chmod +x ./planthealth/main.py
```

To run:
```
python3 /path/to/PlantHealth/planthealth/main.py
```



## Deployment

Add additional notes about how to deploy this on a live system

## Built With

Add notes about what software packages were used

## Authors

* **Jessi Jo Gonzales**
* **Ryan Levendosky**
* **Jose Olivarez**
* **Derrick Rivera**



## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
