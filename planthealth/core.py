import numpy as np
import cv2
import os

### FUNCTIONS USED FOR NDVI IMAGE PROCESSING AND USER INTERFACE ###

#init()
def init(pathto_cmap='cmap.csv'):
    """
    
    """
    global cmap
    cmap = np.genfromtxt(pathto_cmap, delimiter=',', dtype='uint8')

    
    
# ndvi_map()
def ndvi_map(red_img, nir_img):    
    """
    ndvi_map()
    [Description]
    
    Paramters:  
    
    Preconditions:  cmap is global and contains RGB values index by 
                    NDVI in range [0,255]
    
    Postconditions:  
    
    Returns:  
    """
    if not ('cmap' in globals()):
        init()
    
    red_img = red_img.astype(float)
    nir_img = nir_img.astype(float)
    
    #calculate NDVI values pixel-wise
    denom = (nir_img+red_img)
    denom[denom<=0] = 0.0001
    ndvi = (nir_img - red_img) / denom
    
    #scale to range [0,255]
    min_ndvi = np.min(ndvi)
    ndvi = ((ndvi - min_ndvi) * 255) / 2
    ndvi = np.around(ndvi).astype('uint8')
    
    #colormap
    ndvi_img = np.empty_like([ndvi]*3)
    ndvi_img = cmap[ndvi]
    
    return ndvi_img
 


    