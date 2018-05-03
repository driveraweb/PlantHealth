import numpy as np
import cv2
import scipy

# channelSplit()
# to get BGR values from a cv2 image
def channelSplit(image):
    return np.dsplit(image,image.shape[-1])

# showImage()
# shows img for t time (in ms)
#
def showImage(img, t):
    img = cv2.resize(img, (1820, 1368))
    cv2.imshow('Frame', img)
    cv2.waitKey(t)
    cv2.destroyAllWindows()
    
    return
    
# makeLUT()
# create lookup table for use with cv2 based on colormap
# for PlantHealthDetection NDVI 
def makeLUT():
    r = np.zeros((256),dtype='float')
    g = np.zeros((256),dtype='float')
    b = np.zeros((256),dtype='float')
    
    #set up initial BW color values
    for i in range(0,127):
        r[i] = (i*1.2)
        g[i] = (i*1.2)
        b[i] = (i*1.2)
    
    #set up initial RGB color values
    cVals[136] = (198, 65, 255) #violet
    cVals[164] = (255, 65, 65) #red
    cVals[182] = (255, 248, 65) #yellow
    cVals[212] = (65, 255, 68)#green
    cVals[255] = (65, 147, 255) #blue
    # #interpolate missing values
    scipy.interpolate.RegularGridInterpolator(cVals[127:255],)
    
    
    return r

# BGRtoRGB()
# converts image from B-G-R like cv2 uses to R-G-B like most other
# libraries use
def BGRtoRGB(a):
    b, g, r = channelSplit(a)
    a = np.concatenate((r,g,b))
    return np.asarray(a)