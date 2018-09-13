from core import *

#used in utils only
import pickle
import scipy
import matplotlib.pyplot as plt

# plot_perf()
# creates a plot for the specified performance measure given the data
def plot_perf(f_path, perf_type=None):
    if (perf_type == 'dims'):
            with open(f_path, 'rb') as f:
                r = np.asarray(pickle.load(f))
                mean = np.mean(r.T[1].T, axis=0)
                std = np.std(r.T[1].T,axis=0)
                dims = r.T[0].T[0]
                runs = r.shape[0]
                
            plt.figure()
            plt.plot(dims, mean)
            plt.fill_between(dims,mean-std,mean+std, color=(1,0,0,0.2))
            #plt.plot(dims, mean+std, 'r--')
            #plt.plot(dims, mean-std, 'r--')
            #plt.legend(['mean', 'std+', 'std-'])
            plt.xlabel('dimension (nxn)')
            plt.ylabel('time (s)')
            plt.title('Average Numpy NDVI Mapping Time (For '
                       + str(runs) + ' Runs)')
            plt.show()
    
    else:
        print('Performance type not specified or supported.')
    
    return

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
    
# BGRtoRGB()
# converts image from B-G-R like cv2 uses to R-G-B like most other
# libraries use
def BGRtoRGB(a):
    b, g, r = channelSplit(a)
    a = np.concatenate((r,g,b))
    return np.asarray(a)