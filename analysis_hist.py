import pymongo
import sys
import pprint
import matplotlib
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.mlab as mlab
from mpl_toolkits.mplot3d import axes3d, Axes3D
from itertools import combinations

DB_NAME = "summary_db"

# Connect to mongodb as a client
MY_CLIENT = pymongo.MongoClient("mongodb://localhost:27017/")
MY_DB = MY_CLIENT[DB_NAME]

# pp = pprint.PrettyPrinter()

STAGES = ['MC1',
          'SC1',
          'SC2',
          'SC3',
          #'SP0',
          'SP1',
          'SP1A',
          'SP1B',
          'SP2',
          'SP2A',
          'SP2B',
        ]

ATTRIBUTES = ['visibilities',
              'flux',
              'clean_components',
              'rms',
            ]

FREQUENCIES = [325, 610]
CMAPS = ['Blues', 'Purples', 'Oranges', 'Greens', 'Reds']
CLIP_LIMITS = [325, 'MC1', 'visibilities', 50000, 325, 'MC1', 'flux', 6]


def create_dataframe_from_db():
    print("Creating dataframe...")
    df = pd.DataFrame()
    collections = MY_DB.list_collection_names()
    for col_name in collections:
        collection = MY_DB[col_name]
        cursor = collection.find({})
        for document in cursor:
            dict = {}
            dict['Frequency'] = document["frequency"]
            dict['Cycle'] = int(col_name[5:])
            dict['SP1_flag'] = 1
            for stage in STAGES:
                for attribute in ATTRIBUTES:
                    column_name = stage +'_' + attribute
                    try :
                        dict[ column_name ] = document['summary'][stage][attribute]
                    except KeyError:
                        dict['SP1_flag'] = 0
                        dict[column_name] = document['summary']['SP0'][attribute]
            df = df.append(dict, ignore_index=True)
    df.head()
    df.to_pickle("summary.pkl")
    print("Pickle file created.")


def get_data_frame():
    df = pd.read_pickle('summary.pkl')
    return df


def clip_df( df, args_list ):
    if len( args_list )%4 != 0:
        print("Wrong format of args_list in clip_df. Should be [<frequency>, <stage>, <attribute>, <limit>, ...]")
        exit(1)
    num_limits = len(args_list) // 4
    print("Initial df shape:", df.shape)
    for i in range(num_limits):
        column_name = args_list[ i*4 + 1 ] + '_' + args_list[ i*4 + 2 ]
        limit = int( args_list[ i*4 + 3 ] )
        frequency = float( args_list[ i*4 ] )
        df = df.loc[ ((df['Frequency'] == frequency) & (df[ column_name ] < limit)) | (df['Frequency'] != frequency) ]

    print("Final df shape:", df.shape)
    #print (df)
    return df


def plot_histogram(df,p_type):

    for frequency in FREQUENCIES:
        df_temp = df.loc[df['Frequency'] == frequency]
        df_temp = df_temp.loc[df['SP1_flag'] == 1]
        #print((str3)+"    "+str(df_temp[str3].max()))
        print(df_temp)

        #for i,j in zip(df_temp['MC1_visibilities'],df_temp['SP2B_visibilities']):
            # mc1_vis = df_temp['MC1_visibilities'][i]
            # sp2b_vis = df_temp['SP2B_visibilities'][i]
        ratio_vis = 1-(df_temp['SP2B_visibilities']/df_temp['MC1_visibilities'])

        # for i in newarr:
        #     print(i)
        plt.grid(axis='y',alpha=0.75)
        plt.xlabel('SP2B vis/ MC1 vis.')
        plt.ylabel('Frequency')
        plt.title("Histogram plots for frequency: " + str(frequency))
        if p_type=='normalised':
            n, bins, patches=plt.hist(x=ratio_vis, bins=30, weights=np.zeros_like(ratio_vis) + 1. / ratio_vis.size, color='#0504aa',alpha=0.7, rwidth=0.65)
        elif p_type=='cumulative':
            n, bins, patches=plt.hist(x=ratio_vis, bins=30, cumulative=1, color='#0504aa',alpha=0.7, rwidth=0.65)
        else:
            n, bins, patches=plt.hist(x=ratio_vis, bins=30, color='#0504aa',alpha=0.7, rwidth=0.65)
        
        #y = mlab.normpdf(bins, np.mean(ratio_vis), np.std(ratio_vis))
        string1='file_'+str(frequency)
        if matplotlib.get_backend() == "TkAgg":
            manager = plt.get_current_fig_manager()
            manager.resize(*manager.window.maxsize())
        else if matplotlib.get_backend() == 'QT':
            manager = plt.get_current_fig_manager()
            manager.window.showMaximized()
        plt.show()


def main():
    plot_name=''
    try:
        df = get_data_frame()

    except:
        print("summary.pkl not found. Creating new...")
        create_dataframe_from_db()
        
    if len(sys.argv)==2:
        plot_name = sys.argv[1]
    else: 
        print("Usage: python3 analysis_hist.py [type]", "\nwhere plot_type is one of {cumulative, normalised}")
        exit(1)
    df = get_data_frame()
    
    plot_histogram(df,plot_name)


if __name__ == "__main__":
    main()   

