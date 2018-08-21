import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import misc

### get values for jet map
cmap = plt.get_cmap('jet', lut=8)
rgba = np.arange(128) / 127
rgba = cmap(rgba)
rgb = rgba.T[0:3]
RGB = (rgb * 255).astype(int)
RGB = RGB.T

### black and white gradient
blk = np.zeros_like(RGB)[1::2]
wht = np.ones_like(blk) * 255
bnw = np.append(blk, wht, axis=0)
for i in range(128):
    if i < 32: #black to white
        bnw[i] = bnw[i] + 8*i
    elif i < 64: #white to black
        bnw[i] = bnw[i-1] - 8
    elif i < 96: #black to white
        bnw[i] = bnw[i-1] + 8
    else: #white to black
        bnw[i] = bnw[i-1] - 8

### color gradient
print(RGB.shape)
dx = np.array([0,0,0])
for i in range(0,128):
    if (i % 16 == 0 and i < 128-16):
        dx = (RGB[i] - RGB[i+16]) / 16 
    else:
        RGB[i] = RGB[i-1]-dx

### append color to B&W
RGB = np.append(bnw, RGB, axis=0)
### save LUT
np.savetxt("../cmap.csv", RGB, delimiter=",", fmt="%d")

### create images to show color map
test = np.arange(256)
new_px = np.array([test,]*3).T
for px in range(test.size):
    #print(px, "\n", new_px[px], "\n", RGB[test[px]])
    new_px[px] = RGB[test[px]]
print(new_px.shape)
img = np.reshape(new_px, [1,256,3])
scipy.misc.imsave('cmap.jpg', img)
img = np.reshape(img, [16,16,3])
scipy.misc.imsave('cmap_square.jpg', img)
