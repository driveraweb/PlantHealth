# Plant Health Measurement Device using NDVI

Being that changes in plant health may not be present upon visual inspection alone, it is necessary to have a cost-efficient method of visualizing plant health. This will result in increased awareness of declining plant health for common plant applications and allow for preemptive intervention efforts by the owner or overseer. 



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.



### Hardware 

What things you need to use this software

```
RaspberryPi
Pi NoIR Camera with blue filter
Touchscreen Display
```



### Installing

A step-by-step series that tells you how to get a Plant Health imaging software running

*Using your RaspberryPi Terminal**

Create a directory for the applicaction
```
mkdir PlantHealth
cd PlantHealth
```

Clone the PlantHealth repo
```
git clone https://github.com/driveraweb/PlantHealth.git .
```

Install the dependencies
```
pip install -r requirements.txt
```

If you want the application to run automatically at startup add /path/to/PlantHealth/bin/run.sh to your ~/.bashrc file. 

Otherwise, run 
```
/path/toPlantHealth/bin/run.sh
```



## Deployment

Add additional notes about how to deploy this on a live system

## Built With



## Authors

* **Jessi Jo Gonzales**
* **Ryan Levendoski**
* **Jose Olivarez**
* **Derrick Rivera**



## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
