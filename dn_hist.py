import seaborn as sns
import numpy as np
import pandas as pd
import random
from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter

def plot_overlapped_histogram( x1, label1, x2, label2, numbins=12, cumulative=False):
    min_limit = min( min(x1), min(x2) )
    max_limit = max( max(x1), max(x2) )
    bins = np.linspace(min_limit, max_limit, numbins+1)
    plt.hist(x1, bins, alpha=0.5, label=label1, color='Red', weights=np.ones(len(x1)) / len(x1), cumulative=cumulative)
    plt.hist(x2, bins, alpha=0.5, label=label2, color='Blue', weights=np.ones(len(x2)) / len(x2), cumulative=cumulative)
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.legend(loc='upper right')
    plt.show()
