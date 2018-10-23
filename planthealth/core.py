from PIL import Image
import numpy as np
import scipy
import cv2
import os
from planthealth import MAX_FEATURES, GOOD_MATCH_PERCENT, CMAP

#cython stuff
#cimport numpy as np
#DTYPE = np.float32
#ctypedef np.int_t DTYPE_t

### FUNCTIONS USED FOR NDVI IMAGE PROCESSING AND USER INTERFACE ###

#init()
def init(pathto_cmap='cmap.csv'):
    """
    
    """
    global cmap
    cmap = np.genfromtxt(pathto_cmap, delimiter=',', dtype='uint8')

    
    
#alignImages()
def alignImages(im1, im2):
    """
    alignImages()
    [Description]
    
    Paramters:  
    
    Preconditions:  CMAP is global and contains RGB values index by 
                    NDVI in range [0,255]
    
    Postconditions:  
    
    Returns:  
    """
    # Detect ORB features and compute descriptors.
    orb = cv2.ORB_create(MAX_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2, None)

    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)

    # Sort matches by score.
    matches.sort(key=lambda x: x.distance, reverse=False)

    # Remove not so good matches.
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]

    # Draw top matches.
    #imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
    #cv2.imwrite("../Images/matches.jpg", imMatches)
    
    # Extract location of good matches.
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Find homography.
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    # Use homography.
    height, width, channels = im2.shape
    im1Reg = cv2.warpPerspective(im1, h, (width, height))

    return im1Reg


    
# ndvi_map()
def ndvi_map(red_img, nir_img):    
    """
    ndvi_map()
    [Description]
    
    Paramters:  
    
    Preconditions:  CMAP is global and contains RGB values index by 
                    NDVI in range [0,255]
    
    Postconditions:  
    
    Returns:  
    """
    
    red_img = red_img.astype(float)
    nir_img = nir_img.astype(float)
    
    #calculate NDVI values pixel-wise
    denom = (nir_img+red_img)
    denom[denom<=0] = 0.0001
    ndvi = ((((nir_img - red_img) / denom) - 1)*128).astype('uint8')
    
    #scale to range [0,255]
    #min_ndvi = np.min(ndvi)
    #ndvi = ((ndvi - 1) * 255) / 2
    #ndvi = np.around(ndvi).astype('uint8')
    
    #colormap
    ndvi_img = np.empty_like([ndvi]*3)
    ndvi_img = CMAP[ndvi]
    
    return ndvi_img
 
 
 # ndvi_map()
 # using Cython
 # def ndvi_map_c(np.ndarray red_img, np.ndarray nir_img):
    # """uses cython for performance"""
    # assert red_img.dtype == DTYPE and nir_img.dtype = DTYPE
    
    # cdef np.ndarray ndvi_img = np.empty_like(red_img, dtype=np.int8)
    # cdef np.ndarray ndvi = np.empty_like(red_img)
    # cdef np.ndarray denom = np.empty_like(red_img)
    # cdef float min_ndvi
    
    