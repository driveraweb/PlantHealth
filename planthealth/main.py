import argparse
import wx

def main(args):
    #code for main program
    print("Main file running")
    app = wx.App()
    frame = wx.Frame(None, title='Simple Application')
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    description='Run PlantHealth Porgam with given argmuents'
    parser = argparse.ArgumentParser(description=description)
    #parser.add_argument('argname', type=int)
    args = parser.parse_args()
    main(args)
