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

def plot_binned_medians( x, y, numbins=10 ):
    width, bins = create_equal_width_bins( x, numbins )
    indices = assign_bins( x, bins )
    medians, stds = get_bin_medians_stds( y, indices )
    errorbar( bins + width//2, medians, stds )
