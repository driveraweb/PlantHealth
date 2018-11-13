import argparse
import wx
import picamera
import sys
sys.path.append('../../Downloads/ivport-v2')
import ivport
from config import *
import core

def main(args):
    print("Main file running")
    #initialize cameras
    camera = picamera.PiCamera()
    camera.resolution = (1920,1088)
    camera.framerate = 1
    iv = ivport.IVPort(ivport.TYPE_QUAD2, iv_jumper='A')
    
    print('Switching to RGB cam')
    iv.camera_change(2) #start at RGB camera
    print('Capturing RGB image')
    imRef = core.snapshot(camera)
    print('Switching to NoIR cam')
    iv.camera_change(1) #get NIR image
    print('Capturing NIR image')
    imNIR = core.snapshot(camera)
    print('Processing...')
    core.process_snapshot(imNIR, imRef)
    
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
