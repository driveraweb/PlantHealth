import argparse
import wx
import picamera
import time
import sys
sys.path.append('/home/pi/Downloads/ivport-v2')
import ivport
from config import *
import core
from gui import *

def main(args):
    print("Main file running")
    iv = ivport.IVPort(ivport.TYPE_QUAD2, iv_jumper='A')
    camera = picamera.PiCamera()
    try:
        #Initialize cameras
        camera.resolution = (640,480)

        #Start the application
        app = wx.App()  # create application object
        frame = MainWindow(parent=None, title="NDVI Camera Suite", camera=camera, iv=iv)   # establish current frame
        app.MainLoop()  # enters main loop
        

        

        camera.close()
    finally:
        camera.close()
    
    #code for main program

    #app = wx.App()
    #frame = wx.Frame(None, title='Simple Application')
    #frame.Show()
    # app.MainLoop()
    


if __name__ == '__main__':
    description='Run PlantHealth Porgam with given argmuents'
    parser = argparse.ArgumentParser(description=description)
    #parser.add_argument('argname', type=int)
    args = parser.parse_args()
    main(args)
