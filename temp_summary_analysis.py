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
    # for doc in cursor:
    #     print(doc['summary'])
    sources = []

    MC1_visibilities = []
    MC1_flux = []
    MC1_clean = []
    MC1_rms = []

    SC1_visibilities = []
    SC1_flux = []
    SC1_clean = []
    SC1_rms = []


    SC2_visibilities = []
    SC2_flux = []
    SC2_clean = []
    SC2_rms = []

    
    SC3_visibilities = []
    SC3_flux = []
    SC3_clean = []
    SC3_rms = []

    SP1_visibilities = []
    SP1_flux = []
    SP1_clean = []
    SP1_rms = []

    SP1A_visibilities = []
    SP1A_flux = []
    SP1A_clean = []
    SP1A_rms = []

    SP1B_visibilities = []
    SP1B_flux = []
    SP1B_clean = []
    SP1B_rms = []

    SP2_visibilities = []
    SP2_flux = []
    SP2_clean = []
    SP2_rms = []

    SP2A_visibilities = []
    SP2A_flux = []
    SP2A_clean = []
    SP2A_rms = []

    SP2B_visibilities = []
    SP2B_flux = []
    SP2B_clean = []
    SP2B_rms = []

    # data = pd.DataFrame(list(cursor))
    # pp.pprint(data)

    for document in cursor:        

        
        sources.append(document["source"])

        MC1_visibilities.append(document['summary']['MC1']['visibilities'])
        MC1_flux.append(document['summary']['MC1']['flux'])
        MC1_clean.append(document['summary']['MC1']['clean_components'])
        MC1_rms.append(document['summary']['MC1']['rms'])

        SC1_visibilities.append(document['summary']['SC1']['visibilities'])
        SC1_flux.append(document['summary']['SC1']['flux'])
        SC1_clean.append(document['summary']['SC1']['clean_components'])
        SC1_rms.append(document['summary']['SC1']['rms'])

        SC2_visibilities.append(document['summary']['SC2']['visibilities'])
        SC2_flux.append(document['summary']['SC2']['flux'])
        SC2_clean.append(document['summary']['SC2']['clean_components'])
        SC2_rms.append(document['summary']['SC2']['rms'])

        SC3_visibilities.append(document['summary']['SC3']['visibilities'])
        SC3_flux.append(document['summary']['SC3']['flux'])
        SC3_clean.append(document['summary']['SC3']['clean_components'])
        SC3_rms.append(document['summary']['SC3']['rms'])

        SP1_visibilities.append(document['summary']['SP1']['visibilities'])
        SP1_flux.append(document['summary']['SP1']['flux'])
        SP1_clean.append(document['summary']['SP1']['clean_components'])
        SP1_rms.append(document['summary']['SP1']['rms'])

        SP1A_visibilities.append(document['summary']['SP1A']['visibilities'])
        SP1A_flux.append(document['summary']['SP1A']['flux'])
        SP1A_clean.append(document['summary']['SP1A']['clean_components'])
        SP1A_rms.append(document['summary']['SP1A']['rms'])

        SP1B_visibilities.append(document['summary']['SP1B']['visibilities'])
        SP1B_flux.append(document['summary']['SP1B']['flux'])
        SP1B_clean.append(document['summary']['SP1B']['clean_components'])
        SP1B_rms.append(document['summary']['SP1B']['rms'])

        SP2_visibilities.append(document['summary']['SP2']['visibilities'])
        SP2_flux.append(document['summary']['SP2']['flux'])
        SP2_clean.append(document['summary']['SP2']['clean_components'])
        SP2_rms.append(document['summary']['SP2']['rms'])

        SP2A_visibilities.append(document['summary']['SP2A']['visibilities'])
        SP2A_flux.append(document['summary']['SP2A']['flux'])
        SP2A_clean.append(document['summary']['SP2A']['clean_components'])
        SP2A_rms.append(document['summary']['SP2A']['rms'])

        SP2B_visibilities.append(document['summary']['SP2B']['visibilities'])
        SP2B_flux.append(document['summary']['SP2B']['flux'])
        SP2B_clean.append(document['summary']['SP2B']['clean_components'])
        SP2B_rms.append(document['summary']['SP2B']['rms'])

    print("stored")
    print(MC1_visibilities)
    df = pd.DataFrame({'Source':sources , 'MC1_visibilities' : MC1_visibilities , 'MC1_flux' : MC1_flux, \
        'MC1_clean' : MC1_clean, 'MC1_rms' : MC1_rms, 'SC2_visibilities' : SC2_visibilities, \
        'SC2_flux' : SC2_flux, 'SC2_clean' : SC2_clean, 'SC2_rms' : SC2_rms , 'SC2_visibilities' : SC2_visibilities, \
        'SC2_flux' : SC2_flux, 'SC2_clean' : SC2_clean, 'SC2_rms' : SC2_rms , 'SC3_visibilities' : SC3_visibilities,\
        'SC3_flux' : SC3_flux, 'SC3_clean' : SC3_clean, 'SC3_rms' : SC3_rms  , 'SP1_visibilities' : SP1_visibilities,\
        'SP1_flux' : SP1_flux, 'SP1_clean' : SP1_clean, 'SP1_rms' : SP1_rms , 'SP1A_visibilities' : SP1A_visibilities,\
        'SP1A_flux' : SP1A_flux, 'SP1A_clean' : SP1A_clean, 'SP1A_rms' : SP1A_rms , 'SP1B_visibilities' : SP1B_visibilities,\
        'SP1B_flux' : SP1B_flux, 'SP1B_clean' : SP1B_clean, 'SP1B_rms' : SP1A_rms , 'SP2_visibilities' : SP2_visibilities,\
        'SP1_flux' : SP2_flux, 'SP1_clean' : SP2_clean, 'SP1_rms' : SP2_rms , 'SP2A_visibilities' : SP2A_visibilities,\
        'SP1A_flux' : SP2A_flux, 'SP1A_clean' : SP2A_clean, 'SP1A_rms' : SP2A_rms , 'SP2B_visibilities' : SP2B_visibilities,\
        'SP1B_flux' : SP2B_flux, 'SP1B_clean' : SP2B_clean, 'SP1B_rms' : SP2A_rms})

    print(df)

    
    print("End")



def scatter_plotting(freq, stage, arg1, arg2):
    xval = []
    yval = []
#    print(mydb.list_collection_names())
    collection = mydb['CYCLE15']
 #   collection.delete_many({})

    cursor = collection.find({'frequency' : freq})
    for doc in cursor:
        xval.append(doc['summary'][stage][arg1])
        yval.append(doc['summary'][stage][arg2])
    
    fig = plt.figure()
    Title = arg1 + ' Vs. ' + arg2 + ' (stage ' + stage + ')' 
    fig.suptitle(Title)
    plt.xlabel(arg1)
    plt.ylabel(arg2)
    plt.scatter(xval, yval)
    plt.show()

    

    # C = pd.Index(["Data"], name="columns")
    # df = pd.DataFrame(np.array(xval).reshape(len(xval),1), columns = C)
    # print(df)
    # # df = df[np.abs(df.Data-df.Data.mean()) <= (3*df.Data.std())] #std method
    # df = df[(np.abs(stats.zscore(df)) < 3).all(axis=1)] #z-score method
    # print(df)
    # # d = np.asarray(xval)
    # # print(d)
   
    # outliers = [y for stat in boxplot_stats(df['Data']) for y in stat['fliers']]
    # print(outliers)

    # l3 = [x for x in xval if x not in outliers]
    # print(len(l3))
    # # ax = sns.boxplot(data= l3)   
    # plt.scatter(l3, yval)
    # plt.show()
    # print("printing")

def main():
    if len(sys.argv) < 5:
        print("Usage: python3 summary_analysis.py <Frequency> <Stage> <Value1> <Value2>")
        exit(1)
    # scatter_plotting(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    read_database("610")

if __name__ == "__main__":
    main()
