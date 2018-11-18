# NDVI Application Source Code

import os   # import operating system
import wx   # import wx Python
import picamera     # import pi camera modules
import sys
sys.path.append('PlantHealth/planthealth')
import core     # import dsp code

#ID constants
ID_LOAD = 1

class MainWindow(wx.Frame):

    def __init__(self,parent,title):
        frame = wx.Frame.__init__(self, parent, title=title, size=(600,600))
        self.Center()       # centers current frame

        # set up menu
        filemenu = wx.Menu()

        # create menu options
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        menuLoadImg = wx.MenuItem(filemenu, ID_LOAD)
        filemenu.Append(menuLoadImg)
        menuExit = filemenu.Append(wx.ID_EXIT, "&Exit", "Terminate the program")

        # create the menu bar
        menuBar = wx.MenuBar()
        menu.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)

        # create image field
        self.Image = wx.StaticBitmap(self, bitmap=wx.EmptyBitmap(512, 300))
        # ***need code for active camera feed and a condition if image is taken***

        cmd = "raspistill -t 0 -w 1920 -h 1080 -o image.jpg"
        os.system(cmd)
        self.LoadImage()

        # add space to box
        box.Add((1,1),1)
        box.Add(self.Image, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.ADJUST_MINSIZE, 10)
        box.Add((1,1),1)
        box.Add(b, 0, wx.center | wx.ALL, 10)
        self.SetSizerAndFit(box)

        # create capture button
        b = wx.Button(self, -1, "Capture")
        b.Bind(wx.EVT_BUTTON, self.Capture)

        # set events
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnLoad, menuLoadImg)
        
        self.Show(True)     # display current frame

    def Capture(self, event=None):
        with picamera.PiCamera() as camera:
            # camera.vflip = True
            # camera.capture('image.jpg')
            
            self.LoadImage()

    def LoadImage(self):

        # load the image
        IMG = wx.Image("image.jpg", wx.BITMAP_TYPE_JPEG)

        # scale the image and preserve the aspect ratio
        W = IMG.GetWidth()
        H = IMG.GetHeight()
        IMG = IMG.Scale(512, 300)

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
        
        # ***need code for loading a file from memory***

app = wx.App()  # create application object
frame = MainWindow(None, "NDVI Camera Suite")   # establish current frame
app.MainLoop()  # enters main loop
