# NDVI Application Source Code
import sys
sys.path.append('../../Downloads/ivport-v2')
sys.path.append('../planthealth')
import os   # import operating system
import wx   # import wx Python
import picamera     # import pi camera modules
import ivport #for camera MUX
import core     # import dsp code


#GUI CLASS DEFINITION
class MainWindow(wx.Frame):

    def __init__(self,parent,title='NDVI', camera=None, iv=None):
        frame = wx.Frame.__init__(self, parent, title=title, size=(1024, 600))
        self.Center()       # centers current frame
        
        #initialize camera and MUX
        if camera is None:
            print( 'Cannot run program. No Camera initialized.')
            exit()
        else:
            self.camera = camera
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

        # create image field
        self.Image = wx.StaticBitmap(self, bitmap=wx.EmptyBitmap(512, 300))
        # ***need code for active camera feed and a condition if image is taken***

        #Capture Button
        b = wx.Button(self, -1, 'Capture')
        b.Bind(wx.EVT_BUTTON, self.Capture)

        # add space to box
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add((1,1),1)
        box.Add(self.Image, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.ADJUST_MINSIZE, 10)
        box.Add((1,1),1)
        box.Add(b, 0, wx.Center | wx.ALL, 10)
        self.SetSizerAndFit(box)

        # set events
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        #self.Bind(wx.EVT_MENU, self.OnLoad, menuLoadImg)
        
        self.Show()     # display current frame
        #self.Maximize(True)


    def Capture(self, event=None):
        print('Switching to RGB cam')
        self.iv.camera_change(3) #start at RGB camera
        print('Capturing RGB image')
        imRef = core.snapshot(self.camera)
        print('Switching to NoIR cam')
        self.iv.camera_change(1) #get NIR image
        print('Capturing NIR image')
        imNIR = core.snapshot(self.camera)
        print('Processing...')
        NDVIimg = core.process_snapshot(imNIR, imRef)
        print(repr(NDVIimg))
        self.LoadImage(NDVIimg)


    def LoadImage(self, img):
        # load the image
        #IMG = wx.Image("image.jpg", wx.BITMAP_TYPE_JPEG)

        # scale the image and preserve the aspect ratio
        n, W, H = img.shape
        print(img.shape)
        #W = img.GetWidth()
        #H = img.GetHeight()
        IMG = wx.Image(W, H, img)
        IMG = IMG.Scale(640, 480) 

        # convert it to a wx.Bitmap and put it on the wx.StaticBitmap
        self.Image.SetBitmap(wx.BitmapFromImage(IMG))
        self.Refresh()


    def OnAbout(self, e):
        # creates message dialog box with an OK button
        DLG = wx.MessageDialog(self, "...description...", "...title...", wx.OK)
        DLG.ShowModal()
        DLG.Destory()


    def OnExit(self, e):
        # closes the application frame
        self.Close(True)


    #def OnLoad(self, e):
        

#app = wx.App()  # create application object
#frame = MainWindow(None, title="NDVI Camera Suite")   # establish current frame
#app.MainLoop()  # enters main loop
