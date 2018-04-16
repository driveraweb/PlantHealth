import numpy as np
from PIL import Image

### FUNCTIONS USED FOR NDVI IMAGE ANALYSIS AND USER INTERFACE ###

# Parameters:  img as numpy array
# Returns:  rank 3 numpy array with R,G, and N as the pixel values
#           for colors red, green, and near-infrared as floats
def decompose(img):    
    img.convert('RGB')
    arr = np.array(img).astype(float)
    
    return [arr, size]
    