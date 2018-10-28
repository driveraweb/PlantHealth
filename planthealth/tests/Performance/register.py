import sys
sys.path.append('../..')
sys.path.append('../../..')
import planthealth
from planthealth.core import *
from planthealth.utils import *
import cv2
import numpy as np
from multiprocessing import Pool
import os

FRAME_SIZE = (640,480)
_im1 = cv2.open('../Images/RGB.png')
_im1 = cv2.resize(FRAME_SIZE)
im2 = cv2.open('../Images/NGB.png')
im2 = cv2.resize(FRAME_SIZE)

def f(n):
    #randomize image    
    h = np.random.rand(3,3)*(np.random.rand(3,3)*25)
    im1 = cv2.warpPerspective(_im1, h, FRAME_SIZE)
    
    t = time.time()
    imNDVI = alignImages(im1, im2)
    return n, time.time() - t

if __name__ == '__main__':
    n = nparange(10000)
    to_measure = False
    to_plot = not to_measure

    if to_measure:
        r = []
        p = Pool(np.round(os.cpu_count()/2).astype('int'))
        rslt = p.map_async(f, n)
        r = np.asarray(r)

        with open('t_vs_n.pkl', 'wb') as f:
            pickledump(r, f)
