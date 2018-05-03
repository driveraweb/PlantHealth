import numpy as np
import cv2

### FUNCTIONS USED FOR NDVI IMAGE ANALYSIS AND USER INTERFACE ###

# colormap()
# Parameters:  img as numpy array having NDVI values in range [-1,1]
# Returns:  numpy array with R,G, and B color mapped values  
#   corresponding NDVI values
def colormap(red, nir):    
    red = red.astype(float)
    nir = nir.astype(float)
    
    denom = (nir+red)
    denom[denom<=0] = 0.0001
    ndvi = (nir-red)/denom
    #ndvi = (ndvi- np.min(ndvi)) 
    ndvi = ndvi / np.max(ndvi) #normalize
    print(np.min(ndvi), np.max(ndvi))
    ndvi = ndvi*255 #0 to 255
    
    ndvi = np.around(ndvi).astype('uint8') #round and convert to int
    

    #print(ndvi.shape)
    
    #ndvi_bgr[bgr] = ndvi
    #ndvi_gry[gry] = ndvi
    
    #ndvi_bgr = cv2.applyColorMap(ndvi_bgr, cv2.COLORMAP_JET)
    #ndvi_gry = cv2.applyColorMap(ndvi_gry, cv2.COLORMAP_BONE)
    
    
    #ret, ndvi = cv2.threshold(ndvi, 127, 255, cv2.THRESH_TOZERO)
    
    #ndvi = cv2.applyColorMap(ndvi, cv2.COLORMAP_JET)
    
    
    ndvi = cv2.applyColorMap(ndvi, cv2.COLORMAP_JET)
    return ndvi
 


    