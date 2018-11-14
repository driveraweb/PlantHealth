import sys
sys.path.append('../../')
sys.path.append("/home/pi/Downloads/ivport-v2/")
from core import *
from utils import *
#import picamera
import ivport
import time
import os

if __name__ == '__main__':
    to_measure = True
    to_plot = not to_measure

    if to_measure:
        os.system('~/Downloads/ivport-v2/init_ivport.py')
        os.system('~/Downloads/ivport-v2/vcgencmd get_camera')
        os.system('~/Downloads/ivport-v2/i2cdetect -y 1')
        
        iv = ivport.IVPort(ivport.TYPE_QUAD2)
        iv.camera_change(1)
        iv.camera_open(resolution= (1920,1080),framerate= 24)
        
        #camera = picamera.PiCamera()
        #camera.resolution = (1920,1080)
        #camera.framerate=24
        time.sleep(2)
        #img = snapshot(iv.camera)
        iv.camera_capture('single')
        #print(np.array_repr(img))
        iv.close()
        
    if to_plot:
        exit()
