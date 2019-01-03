import pymongo
import sys
import pprint
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd 
from scipy import stats
from matplotlib.cbook import boxplot_stats



dbname = "summary_db"

# Connect to mongodb as a client
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[dbname]

pp = pprint.PrettyPrinter()

def read_database(frequency):
    print("start")
    collection = mydb['CYCLE15']
    # cursor = collection.find({})


    cursor = collection.find({'frequency' : frequency})
   

    df = pd.DataFrame()
    for document in cursor:  
        
        sources = document["source"]

        MC1_visibilities = document['summary']['MC1']['visibilities']
        MC1_flux = document['summary']['MC1']['flux']
        MC1_clean = document['summary']['MC1']['clean_components']
        MC1_rms = document['summary']['MC1']['rms']

        SC1_visibilities = document['summary']['SC1']['visibilities']
        SC1_flux = document['summary']['SC1']['flux']
        SC1_clean = document['summary']['SC1']['clean_components']
        SC1_rms = document['summary']['SC1']['rms']

        SC2_visibilities = document['summary']['SC2']['visibilities']
        SC2_flux = document['summary']['SC2']['flux']
        SC2_clean = document['summary']['SC2']['clean_components']
        SC2_rms = document['summary']['SC2']['rms']

        SC3_visibilities = document['summary']['SC3']['visibilities']
        SC3_flux = document['summary']['SC3']['flux']
        SC3_clean = document['summary']['SC3']['clean_components']
        SC3_rms = document['summary']['SC3']['rms']

        try:
            SP1_visibilities = document['summary']['SP1']['visibilities']
            SP1_flux = document['summary']['SP1']['flux']
            SP1_clean = document['summary']['SP1']['clean_components']
            SP1_rms = document['summary']['SP1']['rms']

        except KeyError:
            SP1_visibilities = document['summary']['SP0']['visibilities']
            SP1_flux = document['summary']['SP0']['flux']
            SP1_clean = document['summary']['SP0']['clean_components']
            SP1_rms = document['summary']['SP0']['rms']


        SP1A_visibilities = document['summary']['SP1A']['visibilities']
        SP1A_flux = document['summary']['SP1A']['flux']
        SP1A_clean = document['summary']['SP1A']['clean_components']
        SP1A_rms = document['summary']['SP1A']['rms']

        SP1B_visibilities = document['summary']['SP1B']['visibilities']
        SP1B_flux = document['summary']['SP1B']['flux']
        SP1B_clean = document['summary']['SP1B']['clean_components']
        SP1B_rms = document['summary']['SP1B']['rms']

        SP2_visibilities = document['summary']['SP2']['visibilities']
        SP2_flux = document['summary']['SP2']['flux']
        SP2_clean = document['summary']['SP2']['clean_components']
        SP2_rms = document['summary']['SP2']['rms']

        SP2A_visibilities = document['summary']['SP2A']['visibilities']
        SP2A_flux = document['summary']['SP2A']['flux']
        SP2A_clean = document['summary']['SP2A']['clean_components']
        SP2A_rms = document['summary']['SP2A']['rms']

        SP2B_visibilities = document['summary']['SP2B']['visibilities']
        SP2B_flux = document['summary']['SP2B']['flux']
        SP2B_clean = document['summary']['SP2B']['clean_components']
        SP2B_rms = document['summary']['SP2B']['rms']
             
        df = df.append({'Source':sources , 'MC1_visibilities' : MC1_visibilities , 'MC1_flux' : MC1_flux, \
            'MC1_clean' : MC1_clean, 'MC1_rms' : MC1_rms, 'SC2_visibilities' : SC2_visibilities, \
            'SC2_flux' : SC2_flux, 'SC2_clean' : SC2_clean, 'SC2_rms' : SC2_rms , 'SC2_visibilities' : SC2_visibilities, \
            'SC2_flux' : SC2_flux, 'SC2_clean' : SC2_clean, 'SC2_rms' : SC2_rms , 'SC3_visibilities' : SC3_visibilities,\
            'SC3_flux' : SC3_flux, 'SC3_clean' : SC3_clean, 'SC3_rms' : SC3_rms  , 'SP1_visibilities' : SP1_visibilities,\
            'SP1_flux' : SP1_flux, 'SP1_clean' : SP1_clean, 'SP1_rms' : SP1_rms , 'SP1A_visibilities' : SP1A_visibilities,\
            'SP1A_flux' : SP1A_flux, 'SP1A_clean' : SP1A_clean, 'SP1A_rms' : SP1A_rms , 'SP1B_visibilities' : SP1B_visibilities,\
            'SP1B_flux' : SP1B_flux, 'SP1B_clean' : SP1B_clean, 'SP1B_rms' : SP1A_rms , 'SP2_visibilities' : SP2_visibilities,\
            'SP1_flux' : SP2_flux, 'SP1_clean' : SP2_clean, 'SP1_rms' : SP2_rms , 'SP2A_visibilities' : SP2A_visibilities,\
            'SP1A_flux' : SP2A_flux, 'SP1A_clean' : SP2A_clean, 'SP1A_rms' : SP2A_rms , 'SP2B_visibilities' : SP2B_visibilities,\
            'SP1B_flux' : SP2B_flux, 'SP1B_clean' : SP2B_clean, 'SP1B_rms' : SP2A_rms} , ignore_index = True)
    

    print(df) 
    



def scatter_plotting(*args):
    xval = []
    yval = []
#    print(mydb.list_collection_names())
    collection = mydb['CYCLE15']
 #   collection.delete_many({})
    frequency = args[0]
    cursor = collection.find({'frequency' : frequency})
    for doc in cursor:
        if len(args)==4:
            stage = args[2]
            data_val2 = args[2]
            data_val2 = args[3]
            xval.append(doc['summary'][stage][data_val2])
            yval.append(doc['summary'][stage][data_val2])
        else:
            data_val2 = args[2]
            data_val2 = args[2]
            xval.append(doc['summary']['SP2B'][data_val2] / doc['summary']['MC2'][data_val2])
            yval.append(doc['summary']['SP2B'][data_val2] / doc['summary']['MC2'][data_val2])

    fig = plt.figure()
    if len(args)==4:
        Title = data_val2 + ' Vs. ' + data_val2 + ' (stage ' + stage + ')' 
    else:
        Title = data_val2 + ' Vs. ' + data_val2
    fig.suptitle(Title)
    plt.xlabel(data_val2)
    plt.ylabel(data_val2)
    plt.scatter(xval, yval)
    plt.show()

def main():
    """if len(sys.argv) < 5:
        print("Usage: python3 summary_analysis.py <Frequency> <Stage> <Value2> <Value2>")
        exit(2)"""
    # if len(sys.argv) == 4:
    #     scatter_plotting(sys.argv[2], sys.argv[2], sys.argv[3])
    # elif len(sys.argv) == 5:
    #     scatter_plotting(sys.argv[2], sys.argv[2], sys.argv[3], sys.argv[4])

    read_database('610')

if __name__ == "__main__":
    main()