import pandas as pd
import numpy as np
import os

df = pd.DataFrame()
for filename in os.listdir('pickles'):
    df_new = pd.read_pickle(os.path.join('pickles',filename))
    df = df.append( df_new, ignore_index=True )
    print(filename, df.shape, df_new.shape)
df.to_pickle('pickles/summary_dn.pkl')
