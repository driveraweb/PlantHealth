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
    elif (perf_type == 'registration'):
        with open(f_path, 'rb') as f:
            r = np.asarray(pickle.load(f))
            t = r.T[1].flatten().T
            mean_val = np.mean(t, axis=0)
            min = np.min(t, axis=0)
            std = np.std(t, axis=0)
            n = np.arange(len(t))
            #mean = np.array(n).astype('float')
            #mean.fill(np.asscalar(mean_val))
            print(mean_val)
            print(min)
        
        window = 100
        mean = moving_average(t, window)
        plt.figure()
        plt.plot(n, t)
        plt.plot(n[window-1:], mean, 'r')
        #plt.fill_between(frames,mean-std,mean+std, color=(1,0,0,0.2))
        plt.legend(['Actual', 'MA(100)'])
        plt.xlabel('frame (640x480)')
        plt.ylabel('time (s)')
        plt.title('Python OpenCV Registration Time')
        plt.show()
    elif (perf_type == 'ndvimap'):
        with open(f_path, 'rb') as f:
            r = np.asarray(pickle.load(f))
            t = r.T[1].flatten().T
            mean_val = np.mean(t, axis=0)
            min = np.min(t, axis=0)
            std = np.std(t, axis=0)
            n = np.arange(len(t))
            #mean = np.array(n).astype('float')
            #mean.fill(np.asscalar(mean_val))
            print(mean_val)
            print(min)
        
        window = 100
        mean = moving_average(t, window)
        plt.figure()
        plt.plot(n, t)
        plt.plot(n[window-1:], mean, 'r')
        #plt.fill_between(frames,mean-std,mean+std, color=(1,0,0,0.2))
        plt.legend(['Actual', 'MA(100)'])
        plt.xlabel('frame (640x480)')
        plt.ylabel('time (s)')
        plt.title('Python NDVI Mapping Time')
        plt.show()
    else:
        print('Performance type not specified or supported.')
    
    return

    
def moving_average(data_set, periods=3):
    weights = np.ones(periods) / periods
    return np.convolve(data_set, weights, mode='valid')

    
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