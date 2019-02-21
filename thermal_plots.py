import pandas as pd
import pymongo
from math import sqrt
import numpy as np
import sys
import matplotlib.pyplot as plt

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

ATTRIBUTES = ['on_source_time',
              'flux',
              'clean_components',
              'rms',
            ]

DB_NAME = "summary_db"

# Connect to mongodb as a client
MY_CLIENT = pymongo.MongoClient("mongodb://localhost:27017/")
MY_DB = MY_CLIENT[DB_NAME]

def create_new_df():
    """Function to create new dataframe 
    with bandwidth values required for 
    thermal RMS calculation"""
    print("Creating dataframe...")
    df = pd.DataFrame()
    collections = MY_DB.list_collection_names()
    for col_name in collections:
        collection = MY_DB[col_name]
        cursor = collection.find({})
        for document in cursor:
            dict = {}
            dict['Frequency'] = document["frequency"]
            dict['Bandwidth'] = document["bandwidth"]
            dict['Cycle'] = int(col_name[5:])
            dict['DN'] = document['dn'].lower()
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
    #df.head()
    df.to_pickle("thermal2.pkl")
    print("Pickle file created.")
    
#create_dataframe_from_db()

#def main():

def get_thermal_values(freq):
    df = pd.read_pickle('thermal2.pkl')

    cycleslist = [15.0,16.0,17.0,18.0,19.0,20.0,21.0,22.0,23.0,24.0,25.0]
    clist = [15,16,17,18,19,20,21,22,23,24,25]

    #SP2B_rms = Tsys/ G * root(2*bandwidth*SP2B_vis)

    if freq == 325:
        df2 = df[df['Frequency']==325.0]
    elif freq == 610:
        df2 = df[df['Frequency']==610.0]

    newb = df['Bandwidth'].astype(float)
    newt = df['SP2B_on_source_time'].astype(float)

    newc = (newb * newt).astype(float)

    newc = (2 * newc).astype(float)
    newc = np.sqrt(newc)

#    G = 0.32
    newc = 0.32 * newc

    #Tsys = 106 for 325, 102 for 610
    if freq == 325:
        newc = 106 / newc
    else:
        newc = 102 / newc

    df2['thermal'] = newc

    df3 = df2[['Cycle','thermal','SP2B_rms', 'Bandwidth']]
    df3 = df3.loc[df3['SP2B_rms']!=df['SP2B_rms'].max()]

    return df3

def noise_distribution(freq):
    #print(df3)

    #for cyc in cycleslist:
    #     val = df3[df3['Cycle']==cyc]
    #     v1 = val['thermal'].median()
    #     v1 = float('{:.3f}'.format(v1))
    #     l1.append(v1)
    #     v2 = val['SP2B_rms'].median()
    #     l2.append(v2)

    lst = []
    for cyc in cycleslist:
        df_cycle = df3[df3['Cycle']==cyc]
        df_cycle = df_cycle[np.isfinite(df_cycle['thermal'])]
        #df_cycle = df_cycle.dropna()
        
        #print(df_cycle)

        data_y1 = df_cycle['thermal']
        data_y2 = df_cycle['SP2B_rms']

        #df3 = df3[df3['Cycle']==cycle]
    df3 = get_thermal_values(freq)
    #data_x = df3.index.tolist()
    data_y1 = df3['thermal']
    data_y2 = df3['SP2B_rms']
    #data_y = df3['SP2B_rms']
    #print(df3.loc[df3['SP2B_rms'].idxmax()])

    #plt.plot(data_x, data_y)
    plt.scatter(data_x, data_y1, label = 'Expected Values')
    #plt.scatter(data_x, data_y1, color='blue')
    plt.scatter(data_x, data_y2, color='red', label='Actual Values')
    plt.legend()
    plt.xlabel('Datapoints', size=16)
    plt.ylabel('RMS Values (mJy/beam)', size=16)
    plt.title('RMS Noise distribution across cycles (Frequency '+ str(freq) + ')')
    plt.show()
    

#Error plot : RMS vs Cycle number

def RMS_error(freq):

    df3 = get_thermal_values(freq)
    data_y1 = df3['thermal']
    data_y2 = df3['SP2B_rms']
    data_diff = data_y2 - data_y1
    k = np.sqrt(((data_y2 - data_y1) ** 2).mean())
    lst.append(k)
    
    data_x = clist
    data_y = lst

    plt.plot(data_x, data_y)
    plt.xlabel('Cycle number', size=16)
    plt.ylabel('Root Mean Square error', size = 16)
    plt.title('Root Mean Square error for SP2B RMS Noise values across cycles (Frequency ' + str(freq) + ')', size=16)
    plt.show()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 thermal_plots.py [arg]", "\nwhere arg can be create, distribution_graph, Error_graph")
        exit(1)
    arg = sys.argv[1]
    if arg == 'create':
        get_thermal_values()
    elif arg == 'distribution_graph':
        noise_distribution()
    elif arg == 'Error_graph':
        RMS_error()
