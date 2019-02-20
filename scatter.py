import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def scatter( x, y, s=None, c=None, label=None, alpha=None ):
    plt.scatter( x, y, s=s, c=c, label=label, alpha=alpha )

def errorbar( x, y, yerr ):
    plt.errorbar( x, y, yerr=yerr, color='red' )
    #plt.show()

def create_equal_width_bins( x, numbins=10 ):
    min = int( x.min() )
    max = int( x.max() )
    width = (max-min) // numbins
    bins = np.array( [ i for i in range( min, max, width ) ] )
    return width, bins

def assign_bins( x, bins ):
    return np.digitize( x, bins )

def assign_equal_depth_bins( x, y, numbins=10):
    depth = x.shape[0] // (numbins)
    print(depth)
    sorted_indices = np.argsort(x)
    x = x[sorted_indices]
    y = y[sorted_indices]
    indices = np.empty_like(x, dtype=int)
    bins = []
    for i in range(indices.shape[0]):
        indices[i] = (i // depth) + 1
        if (i%depth)-1 == 0:
            try:
                bins.append(x[i+(depth//2)])
            except:
                bins.append(x[i])
    return x, y, np.array(bins), indices

def get_bin_medians_stds( x, indices ):
    medians = []
    stds = []
    for i in range(1, indices.max()+1):
        mask = indices==i
        median = np.median( np.array(x)[mask] )
        std = np.std( np.array(x)[mask] )
        medians.append( median )
        stds.append( std )
    return medians, stds

def plot_width_binned_medians( x, y, numbins=100 ):
    width, bins = create_equal_width_bins( x, numbins )
    indices = assign_bins( x, bins )
    medians, stds = get_bin_medians_stds( y, indices )
    errorbar( bins + width//2, medians, stds )

def plot_depth_binned_medians( x, y, numbins=15 ):
    x, y, bins, indices = assign_equal_depth_bins( x, y, numbins )
    medians, stds = get_bin_medians_stds( y, indices )
    errorbar( bins, medians, stds )
