# NDVI Application Source Code
import sys
sys.path.append('/home/pi/Downloads/ivport-v2')
sys.path.append('/home/pi/PlantHealth/planthealth')
import os   # import operating system
import wx   # import wx Python
import picamera     # import pi camera modules
import ivport #for camera MUX
import core     # import dsp code
import cv2
import time
from config import NDVI_VID, NO_VID, VIS_VID, FRAMERATE


#GUI CLASS DEFINITION
class MainWindow(wx.Frame):

    def __init__(self,parent,title='NDVI', camera=None, iv=None):
        frame = wx.Frame.__init__(self, parent, title=title, size=(1024, 490))
        self.Center()       # centers current frame

        #NDVI Video State
        self.img = None #numpy array
        self.frame_ready = False
        self.VidMode = NDVI_VID #start in NDVI video
        
        #timer for video frames
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(10)
        
        #initialize camera and MUX
        if camera is None:
            print( 'Cannot run program. No Camera initialized.')
            exit()
        else:
            self.camera = camera
            self.camera.framerate = FRAMERATE
        if iv is None:
            print('Cannot run program. No MUX initialized.')
            exit()
        else:
            self.iv = iv
        
        # set up menu
        filemenu = wx.Menu()

        # create menu options
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        menuLoadImg = wx.MenuItem(filemenu)
        filemenu.Append(menuLoadImg)
        menuExit = filemenu.Append(wx.ID_EXIT, "&Exit", "Terminate the program")

        # create the menu bar
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)

        # create scale image field
        img = cv2.imread('/home/pi/PlantHealth/scale.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, n = img.shape
        IMG = wx.Image(w, h, img)
        self.ScaleImage = wx.StaticBitmap(self, bitmap=wx.Bitmap(w,h))
        self.ScaleImage.SetBitmap(wx.Bitmap(IMG))
        
        # create image field
        self.Image = wx.StaticBitmap(self, bitmap=wx.Bitmap(640, 480))
        
        #Toggle NDVI Video Button
        self.b_ndvi = wx.Button(self, -1, 'Toggle\nNDVI\nVideo')
        self.b_ndvi.Bind(wx.EVT_BUTTON, self.NDVI_Video)

        #Capture/Delete Button
        self.b_cap = wx.Button(self, -1, 'Capture\nNDVI\nImage')
        self.b_cap.Bind(wx.EVT_BUTTON, self.Capture)
        
        # add space to box
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.ScaleImage, 0, wx.ALIGN_TOP|wx.ALIGN_LEFT|wx.ALL|wx.ADJUST_MINSIZE, 10)
        box.Add(self.Image, 0, wx.ALIGN_TOP|wx.ALIGN_LEFT|wx.ALL|wx.ADJUST_MINSIZE, 10)
        
        flags = wx.SizerFlags(1)
        flags.Border(wx.ALL, 10)
        box.Add(self.b_ndvi, flags.Right().Center())#.Expand())
        box.Add(self.b_cap, flags.Right().Center())#.Expand())
        self.SetSizerAndFit(box)

        # set events
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        
        self.Show() # display current frame
        self.Maximize(True)


    def Capture(self, event=None):
        self.VidMode = NO_VID
        self.camera.framerate = FRAMERATE
        print('Switching to RGB cam')
        self.iv.camera_change(3) #start at RGB camera
        print('Capturing RGB image')
        imRef = core.snapshot(self.camera)
        print('Switching to NoIR cam')
        self.iv.camera_change(1) #get NIR image
        print('Capturing NIR image')
        imNIR = core.snapshot(self.camera)
        print('Processing...')
        NDVIimg, self.lastCapTime = core.process_snapshot(imNIR, imRef)
        self.img = NDVIimg
        #print(repr(NDVIimg))
            
        #update button
        self.b_cap.SetLabelText('Delete\nImage')
        self.b_cap.Bind(wx.EVT_BUTTON, self.DeleteImage)
        
        self.LoadImage() #load image refreshes button


    def LoadImage(self):
        #print('Loading Image')
        # convert img to wx.Image
        H, W, n = self.img.shape
        IMG = wx.Image(W, H, self.img)
        #IMG = IMG.Scale(640, 480) 

        # convert it to a wx.Bitmap and put it on the wx.StaticBitmap
        self.Image.SetBitmap(wx.Bitmap(IMG))
            
        self.Refresh() 
    
    
    def DeleteImage(self, event=None):
        #delete images
        cmd = 'rm /home/pi/PlantHealth/SavedImages/'+self.lastCapTime
        os.system(cmd+'_ndvi.jpg')
        os.system(cmd+'_Ref.jpg')
        os.system(cmd+'_im.jpg')
        print('Finished deleting last capture.')
          
        #update button
        self.b_cap.SetLabelText('Capture\nImage')
        self.b_cap.Bind(wx.EVT_BUTTON, self.Capture)
            
        self.NDVI_Video()
    
        
    def NDVI_Video(self, event=None):
        #make sure catpture button is in capture mode - resets on next frame
        self.b_cap.SetLabelText('Capture\nNDVI\nImage')
        self.b_cap.Bind(wx.EVT_BUTTON, self.Capture)
        
        if self.VidMode != VIS_VID:
            print("Entering VIS Camera mode")
            #if self.vid is not None:
            #    self.vid.stop()
            self.VidMode = VIS_VID
            self.camera.framerate = FRAMERATE
            self.vid = core.VisVideo(self)
        else:
            print("Entering NDVI Video mode")
            #if self.vid is not None:
            #    self.vid.stop()
            self.VidMode = NDVI_VID
            core.NDVIVideo(self)
        

    def on_timer(self, event=None):
        #print("Timer event")
        if self.frame_ready:
            self.frame_ready = False
            self.LoadImage()
            
            
    def OnAbout(self, e):
        # creates message dialog box with an OK button
        DLG = wx.MessageDialog(self, "Real-time NDVI video and NDVI image"
                               +" capture", "NDVI App", wx.OK)
        DLG.ShowModal()
        DLG.Destory()


    def OnExit(self, e):
        # closes the application frame
        self.VidMode = NO_VID #to stop background threads
        time.sleep(0.1)
        
        self.Close(True) #close app
        


    #def OnLoad(self, e):
        

#app = wx.App()  # create application object
#frame = MainWindow(None, title="NDVI Camera Suite")   # establish current frame
#app.MainLoop()  # enters main loop
