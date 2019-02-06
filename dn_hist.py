import seaborn as sns
import numpy as np
import pandas as pd
import random
from matplotlib import pyplot as plt

def plot_overlapped_histogram( x1, label1, x2, label2, numbins=10):
    min_limit = min( min(x1), min(x2) )
    max_limit = max( max(x1), max(x2) )
    bins = np.linspace(min_limit, max_limit, numbins+1)
    plt.hist(x1, bins, alpha=0.5, label=label1, color='Red')
    plt.hist(x2, bins, alpha=0.5, label=label2, color='Blue')
    plt.legend(loc='upper right')
    plt.show()
