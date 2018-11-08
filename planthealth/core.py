from PIL import Image
import numpy as np
import numexpr as ne
import datetime
#import picamera
import scipy
import cv2
import os
from config import *

#cython stuff
#cimport numpy as np
#DTYPE = np.float32
#ctypedef np.int_t DTYPE_t

### FUNCTIONS USED FOR NDVI IMAGE PROCESSING AND USER INTERFACE ###

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
    print(np.array_repr(h))

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
    
    #calculate NDVI values pixel-wise and scale to 0-255
    idx = ne.evaluate("(((nir_img - red_img) / (nir_img+red_img) + 1)*128)").astype('uint8')
    #idx = (((nir_img - red_img) / (nir_img+red_img) + 1)*128).astype('uint8')

    return CMAP[idx]
 
 
# process_snapshot()
def process_snapshot(im_path, imRef_path):
    """
    ndvi_map()
    [Description]
    
    Paramters:  
    
    Preconditions:  CMAP is global and contains RGB values index by 
                    NDVI in range [0,255]
    
    Postconditions:  
    
    Returns:  
    """
    # Open Images
    imRef = cv2.imread(imRefPath, cv2.IMREAD_COLOR)
    im = cv2.imread('../Images/NGB.png', cv2.IMREAD_COLOR)
    
    # Registered image will be restored in imReg. 
    # The estimated homography will be stored in h
    imReg = alignImages(im, imRef)
    
    # Extract pertinent info
    [_, _, Rimg] = cv2.split(imRef)
    [_, _, NIRimg] = cv2.split(imReg)
 
    # Generate NDVI image
    NDVIimg = ndvi_map(Rimg, NIRimg)
    
    # Save NDVI Image
    t = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    out_path = "~/PlantHealth/SavedImages/ndvi"+t+".jpg"
    cv2.imwrite(out_path, imReg)


 
# capture_image()
# requires a camera setup with:
#   resolution = (1920,1080)
#   framerate = 24
#   time.sleep(2)
def snapshot(camera):
    img = np.empty((1080, 1920, 3), dtype=np.int8)
    camera.capture(img, 'rgb')
    return img
 
 
 # ndvi_map()
 # using Cython
 # def ndvi_map_c(np.ndarray red_img, np.ndarray nir_img):
    # """uses cython for performance"""
    # assert red_img.dtype == DTYPE and nir_img.dtype = DTYPE
    
    # cdef np.ndarray ndvi_img = np.empty_like(red_img, dtype=np.int8)
    # cdef np.ndarray ndvi = np.empty_like(red_img)
    # cdef np.ndarray denom = np.empty_like(red_img)
    # cdef float min_ndvi
    
    
