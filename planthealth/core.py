from PIL import Image
import numpy as np
import numexpr as ne
import datetime
import time
import picamera
from picamera.array import PiRGBArray
import scipy
import cv2
import os
from config import CMAP, GOOD_MATCH_PERCENT, MAX_FEATURES, H, H_SHORT
from config import FRAMERATE
import RPi.GPIO as GPIO
import threading
import wx
#import pickle
from config import NDVI_VID, NO_VID, VIS_VID
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setwarnings(False)
global MAX_FEATURES
global GOOD_MATCH_PERCENT

### FUNCTIONS USED FOR NDVI IMAGE PROCESSING AND USER INTERFACE ###

# lamps()
def lamps(val):
    """
    lamps()
    Sets the GPIO (physical) pins 37 and 38 to high or low based on the
        argument value.
    
    Paramters:  val - GPIO.HIGH or 1 to turn lamps on
                      GPIO.LOW or 0 to turn lamps off
    
    Preconditions: none
    
    Postconditions: The lamps are turned on or off  
    
    Returns: none 
    """
    GPIO.output(37, val)
    GPIO.output(38,val)

# alignImages()
def alignImages(im1, im2):
    """
    alignImages()
        Aligns the key features in im1 with the key features in im2 using
        OpenCV's ORB feature detector, a brute force hamming matcher, and
        RANSAC to estimate the homography matrix h. Once the matrix h is 
        found, im1 is warped producing im1reg, the aligned image.
    
    Paramters:  im1 - the image to be registered to the same space
                      as im2
                im2 - the reference image
    
    Preconditions:  CMAP is global and contains RGB values index by 
                    NDVI in range [0,255]
    
    Postconditions:  im1 and im2 remain unchanged
                     the image "matches.jpg" is saved in 
                        /home/pi/SavedImages/ showing the features 
                        the are being matched together to generate the
                        homography matrix
    
    Returns:  im1reg - the registered version of im1. im1reg should have
                           its features aligned with im2.
    """
    #adjust max_features and good_match_percents
    #print('Max features', MAX_FEATURES)
    #print('Using % good', GOOD_MATCH_PERCENT)
    #GOOD_MATCH_PERCENT = 0.15
    #print('Saved Homography:', H_SHORT)
    
    # Detect ORB features and compute descriptors.
    orb = cv2.ORB_create(MAX_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2, None)

    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    try:
        matches = matcher.match(descriptors1, descriptors2, None)
    except:
        matches = None
        #print('could not match features')
    
    if matches is not None:
        # Sort matches by likelihood of being a match.
        matches.sort(key=lambda x: x.distance, reverse=False)

        # Remove not so good matches.
        numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
        matches = matches[:numGoodMatches]

        # Draw top matches.
        imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
        #cv2.imshow('Matches', imMatches)
        #cv2.waitKey(2000)
        cv2.imwrite("/home/pi/PlantHealth/SavedImages/matches.jpg", imMatches)
        
        # Extract location of good matches.
        points1 = np.zeros((len(matches), 2), dtype=np.float32)
        points2 = np.zeros((len(matches), 2), dtype=np.float32)

        for i, match in enumerate(matches):
            points1[i, :] = keypoints1[match.queryIdx].pt
            points2[i, :] = keypoints2[match.trainIdx].pt

        # Find homography or use a stored version in case of emergency
        #     or if the homography seems inaccurate.
        try:
            h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)
        except:
            h = H_SHORT #using stored homography
            #print('Using saved homography h:', h)
        finally:
            # Use homography.
            if h is None or not (np.allclose(h, H_SHORT, rtol=0, atol=0.5) 
                                 or np.allclose(h, H, rtol=0, atol=0.5)):
                h = H_SHORT
                #print('Using saved homography h:', h)
            #print('Using homography h:', repr(h))
            height, width, channels = im2.shape
            im1Reg = cv2.warpPerspective(im1, h, (width, height))
    else:
        im1Reg = im1 #could not register the image
    return im1Reg

    
# ndvi_map()
def ndvi_map(red_img, nir_img):    
    """
    ndvi_map()
    Given the pixel values of an image corresponding to red reflectance
        and the pixel values of the same image corresponding to near
        infrared reflectance, the normalized difference vegetation 
        index (NDVI) values are computed pixel-wise and color mapped
        using the custom color map lookup table (256)
    This function is used for real-time video frame processing, since
        it uses NumExpr and does not compute the average NDVI for 
        vegetation pixels (NDVI > 0).
    
    Paramters:  red_img - array containing red pixel values
                nir_img - array containing NIR pixel values
    
    Preconditions:  CMAP is defined and contains RGB values by index 
                    for NDVI scaled to range [0,255]
    
    Postconditions:  the colormap is set
    
    Returns:  the RGB image where each pixel is color mapped based on
              NDVI value. 
              A 0 is also returned as an extra value.
    """
    global CMAP
    #calculate NDVI values pixel-wise and scale to 0-255
    #####ndvi = ne.evaluate("(nir_img - red_img)/(nir_img+red_img)")
    #min_ndvi = np.min(ndvi)
    #idx = ne.evaluate("((ndvi - min_ndvi)*128)").astype('uint8')
    #####idx = ne.evaluate("((ndvi + 1)*128)").astype('uint8')
    #idx = (((nir_img - red_img) / (nir_img+red_img) + 1)*128).astype('uint8')
    idx = ne.evaluate("(((nir_img - red_img) / (nir_img+red_img) + 1)*128)").astype('uint8')

    return CMAP[idx], 0#int(np.mean(np.nan_to_num(ndvi))*1000)/1000
 
 
 
# ndvi_map2()
def ndvi_map2(red_img, nir_img):    
    """
    ndvi_map2()
    Given the pixel values of an image corresponding to red reflectance
        and the pixel values of the same image corresponding to near
        infrared reflectance, the normalized difference vegetation 
        index (NDVI) values are computed pixel-wise and color mapped
        using the custom color map lookup table (256)
    This function is used for single image captures since it also 
        computes the average vegetation NDVI (i.e. mean over pixels 
        with NDVI >0).
    
    Paramters:  red_img - array containing red pixel values
                nir_img - array containing NIR pixel values
    
    Preconditions:  CMAP is defined and contains RGB values by index 
                    for NDVI scaled to range [0,255]
    
    Postconditions:  the colormap is set
    
    Returns:  the RGB image where each pixel is color mapped based on
              NDVI value. 
              The average (arithmetic mean) of all pixels with NDVI > 0
              is also returned, corresponding to the average NDVI of 
              vegetation in the image.
    """
    global CMAP
    #calculate NDVI values pixel-wise and scale to 0-255
    ndvi = ne.evaluate("(nir_img - red_img)/(nir_img+red_img)")
    #min_ndvi = np.min(ndvi)
    #idx = ne.evaluate("((ndvi - min_ndvi)*128)").astype('uint8')
    idx = ne.evaluate("((ndvi + 1)*128)").astype('uint8')
    #idx = (((nir_img - red_img) / (nir_img+red_img) + 1)*128).astype('uint8')
    #idx = ne.evaluate("(((nir_img - red_img) / (nir_img+red_img) + 1)*128)").astype('uint8')

    return CMAP[idx], int(np.mean(np.nan_to_num(ndvi)[ndvi>0])*1000)/1000


# process_snapshot()
def process_snapshot(im, imRef):
    """
    process_snapshot()
    Converts two image (the NIR and VIS) images into the NDVI color
        mapped image
    
    Paramters:  im - contains the NIR reflectance values
                imRef - contains the visible (red) reflectance values
    
    Preconditions:  CMAP is global and contains RGB values index by 
                    NDVI in range [0,255].
                    im is an array of the form BGR
                    imRef is an array of the form BGR
    
    Postconditions:  im, imRef, and their resulting NDVI image is saved
                     to /home/pi/PlantHealth/SavedImages/
                     with im as '[datetime]_im.jpg', 
                     imRef as '[datetime]_Ref.jpg', 
                     and NDVI as '[datetime]_ndvi.jpg'
    
    Returns:  NDVI - The NDVI mapped image
              avg - The average NDVI value of the vegetaion in the images
              t - a string of the datetime object indicating the last_GOOD_MATCH_PERCENT
                  set of saved images. Can be used to access the images
                  in the future.
    """
    #global MAX_FEATURES
    #global GOOD_MATCH_PERCENT
    #last_MAX_FEATURES = MAX_FEATURES
    #MAX_FEATURES=1500
    #last_GOOD_MATCH_PERCENT = GOOD_MATCH_PERCENT
    #GOOD_MATCH_PERCENT = 0.04
    # Open Images - should be replaced with arrays
    #imRef = cv2.imread(imRef_path, cv2.IMREAD_COLOR)
    #im = cv2.imread(im_path, cv2.IMREAD_COLOR)
    
    # Registered image will be restored in imReg. 
    # The estimated homography will be stored in h
    imReg = alignImages(im, imRef)
    
    # Extract pertinent info
    [_, _, Rimg] = cv2.split(imRef)
    [_, _,NIRimg] = cv2.split(imReg)
 
    # Generate NDVI image
    NDVI, avg = ndvi_map2(Rimg, NIRimg)
    
    #show NDVI image
    #cv2.imshow('NDVI Snap', NDVIimg)
    #cv2.waitKey(300)
    
    # Save NDVI Image
    t = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    out_path_NDVI = "/home/pi/PlantHealth/SavedImages/"+t+"_ndvi.jpg"
    out_path_Ref = "/home/pi/PlantHealth/SavedImages/"+t+"_Ref.jpg"
    out_path_im = "/home/pi/PlantHealth/SavedImages/"+t+"_im.jpg"
    print('Writing file to: ', out_path_NDVI)
    NDVIimg = cv2.cvtColor(NDVI, cv2.COLOR_RGB2BGR) #convert to BGR to save with cv2
    cv2.imwrite(out_path_NDVI, NDVIimg) #have to save bgr format with cv2
    cv2.imwrite(out_path_Ref, imRef)
    cv2.imwrite(out_path_im, im)
    
    return NDVI, avg, t

    #MAX_FEATURES=last_MAX_FEATURES
    #GOOD_MATCH_PERCENT = last_MAX_FEATURES

 
# capture_image()
# requires:
#   ivport MUX initialized
#   a camera setup with:
#     resolution = (1920,1088)
#     framerate = 24
#     time.sleep(2)
def snapshot(camera):
    """
    snapshot()
    Captures an image in bgr form to an array using the given camera
        object.
    
    Paramters:  camera - the camera used to capture the image
    
    Preconditions:  if the lamps are connects to GPIO pins 37 and 38, 
                        then they will be turn on during capture and off
                        after the capture. 
                    camera is set up with desired parameters for image
    
    Postconditions:  The image captured using camera will have pixel 
                     values in the form BGR
    
    Returns:  the image captured in BGR form as an array
    """
    #lamps(GPIO.HIGH)
    #reference to camera capture
    with PiRGBArray(camera) as raw:
        #raw = PiRGBArray(camera) 
        #get image from camera
        lamps(GPIO.HIGH)
        camera.capture(raw, format='bgr')
        lamps(GPIO.LOW)
        #print('Captured')
        imRef = raw.array
    
        return imRef
 

# get_frame()
#    pirgbarray must be set up with camera
def get_frame(camera, pirgbarray, fmt='bgr'):
    """
    get_frame()
    returns an array of a frame for a video feed
    
    Paramters:  camera - the camera object to capture the image with
                pirgbarray - 
                fmt - default is bgr. see picamera capture() 
                      documentation for other possible formats
    
    Preconditions:  camera and pirgbarray are correctly defined
    
    Postconditions:  none
    
    Returns:  array containing the pixel values in the specified format
    """
    #get image from camera
    pirgbarray.truncate(0) #clear stream
    camera.capture(pirgbarray, format=fmt, use_video_port=True)

    return pirgbarray.array#img


#Class VisVideo()
class VisVideo(threading.Thread):
    """
    Inherits from threading.Thread so that visible video can be
        captured as a background thread. 
    """
    def __init__(self, gui):
        self.gui = gui
        threading.Thread.__init__(self) 
        self.daemon = True #allows exiting program if thread is running
        self.start()
        
    def run(self):
        print('Running video thread')
        self.gui.iv.camera_change(3) #RGB camera
        while self.gui.iv.camera is not 3 and self.gui.VidMode == NDVI_VID:
            continue
        with picamera.array.PiRGBArray(self.gui.camera) as frame:
            while self.gui.VidMode == VIS_VID:
                try:
                    self.gui.img = get_frame(self.gui.camera, frame, 'rgb')
                    self.gui.frame_ready = True
                    #print('Frame is ready')
                except:
                    print('VIS frame error')
        print('End of VIS video')
        return
 
 
#Class NDVIVideo()
class NDVIVideo(threading.Thread):
    """
    Inherits from threading.Thread so that visible video can be
        captured as a background thread. 
    """
    def __init__(self, gui):
        self.gui = gui
        threading.Thread.__init__(self) 
        self.daemon = True #allows exiting program if thread is running
        self.start()
        
    def run(self):
        print('Running NDVI video thread')
        sleep_time = 0.01
        lamps(GPIO.HIGH)
        time.sleep(sleep_time)
        result=[]
        while self.gui.VidMode == NDVI_VID:
            t = time.time()
            with picamera.array.PiRGBArray(self.gui.camera) as frame:
                try:
                    self.gui.iv.camera_change(1) #start at NIR camera
                    while self.gui.iv.camera is not 1  and self.gui.VidMode == NDVI_VID:
                        continue
                    time.sleep(sleep_time)
                    im = get_frame(self.gui.camera, frame)
                except:
                    im = None
                    print('NDVI (NIR) frame error')
            #print('got nir frame')
            #time.sleep(0.001)
            #*****loop here  for some time******
            with picamera.array.PiRGBArray(self.gui.camera) as frame:
                try:
                    self.gui.iv.camera_change(3) #get RGB image
                    while self.gui.iv.camera is not 3 and self.gui.VidMode == NDVI_VID:
                        continue
                    time.sleep(sleep_time)
                    imRef = get_frame(self.gui.camera, frame)
                except:
                    imRef = None
                    print('NDVI (VIS) frame error')
            #print('Capture time:', time.time() - t)
            #process images
            #imReg = alignImages(im, imRef)
            if im is not None and imRef is not None:
                #t = time.time()
                #height, width, channels = im.shape
                imReg = cv2.warpPerspective(im, H, (640, 480))
                #imReg = alignImages(im, imRef)
                #t = time.time()
                #imReg = alignImages(im, imRef)
                [_,_,NIR] = cv2.split(imReg)
                [_,_,R] = cv2.split(imRef)
                self.gui.img,_ = ndvi_map(R, NIR) #rgb image
                self.gui.frame_ready = True
            #print('Frame is ready')
            result.append(time.time()-t)
        lamps(GPIO.LOW)
        #with open('/home/pi/PlantHealth/planthealth/tests/Performance/proc_time_f.pkl', 'wb') as f:
        #    pickle.dump(str(result), f)
        return