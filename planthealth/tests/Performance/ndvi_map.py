import sys
sys.path.append('../../')
from core import *
from utils import *
from multiprocessing import Pool
import time
import os


init('../../cmap.csv')

def f(x):
    im1 = np.random.rand(x,x)
    im2 = np.random.rand(x,x)
    t = time.time()
    ndvi_map(im1, im2)
    return x, time.time() - t


if __name__ == '__main__':
    to_measure = True
    to_plot = not to_measure

    if to_measure:
        r = []
        for i in range(0,100):
            p = Pool(np.round(os.cpu_count()/2).astype('int'))
            rslt = p.map_async(f, np.arange(510,2161, 10))
            print('ITERATION ' + str(i))
            r.append(np.asarray(rslt.get()))
        
        r = np.asarray(r)
        
        with open('t_vs_dims.pkl', 'wb') as f:
            pickle.dump(r, f)
    
    if to_plot:
        plot_perf('t_vs_dims.pkl', 'dims')