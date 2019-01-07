import pymongo
import sys
import pprint
import matplotlib
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats
from matplotlib.cbook import boxplot_stats
from itertools import combinations

dbname = "summary_db"

# Connect to mongodb as a client
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[dbname]

pp = pprint.PrettyPrinter()

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
              'clean',
              'rms',
              ]

FREQUENCIES = [325, 610]

CLIP_LIMITS = [325, 'MC1', 'visibilities', 50000, 325, 'MC1', 'flux', 6]

def create_dataframe_from_db():
    print("Creating dataframe...")
    df = pd.DataFrame()
    collections = mydb.list_collection_names()
    for col_name in collections:
        collection = mydb[col_name]
        cursor = collection.find({})
        for document in cursor:
            flag = 1
            frequency = document["frequency"]
            cycle = int(col_name[5:])

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
                flag = 0
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

            df = df.append({'Cycle' : cycle, 'Frequency' : frequency, 'MC1_visibilities' : MC1_visibilities , 'MC1_flux' : MC1_flux, \
                'MC1_clean' : MC1_clean, 'MC1_rms' : MC1_rms, 'SC1_visibilities' : SC1_visibilities, \
                'SC1_flux' : SC1_flux, 'SC1_clean' : SC1_clean, 'SC1_rms' : SC1_rms , 'SC2_visibilities' : SC2_visibilities, \
                'SC2_flux' : SC2_flux, 'SC2_clean' : SC2_clean, 'SC2_rms' : SC2_rms , 'SC3_visibilities' : SC3_visibilities,\
                'SC3_flux' : SC3_flux, 'SC3_clean' : SC3_clean, 'SC3_rms' : SC3_rms  , 'SP1_visibilities' : SP1_visibilities,\
                'SP1_flux' : SP1_flux, 'SP1_clean' : SP1_clean, 'SP1_rms' : SP1_rms , 'SP1A_visibilities' : SP1A_visibilities,\
                'SP1A_flux' : SP1A_flux, 'SP1A_clean' : SP1A_clean, 'SP1A_rms' : SP1A_rms , 'SP1B_visibilities' : SP1B_visibilities,\
                'SP1B_flux' : SP1B_flux, 'SP1B_clean' : SP1B_clean, 'SP1B_rms' : SP1B_rms , 'SP2_visibilities' : SP2_visibilities,\
                'SP2_flux' : SP2_flux, 'SP2_clean' : SP2_clean, 'SP2_rms' : SP2_rms , 'SP2A_visibilities' : SP2A_visibilities,\
                'SP2A_flux' : SP2A_flux, 'SP2A_clean' : SP2A_clean, 'SP2A_rms' : SP2A_rms , 'SP2B_visibilities' : SP2B_visibilities,\
                'SP2B_flux' : SP2B_flux, 'SP2B_clean' : SP2B_clean, 'SP2B_rms' : SP2B_rms, 'SP1_flag' : flag} , ignore_index = True)

        df.head()
        df.to_pickle("summary.pkl")
        print("Pickle file created.")

def get_data_frame():
    df = pd.read_pickle('summary.pkl')
    return df

def clip_df(df, args_list):
    if len(args_list) % 4 != 0:
        print("Wrong format for clip_df. Should be <frequency> <stage> <attribute> <limit>")
        exit(1)
    num_limits = len(args_list) // 4
    print("Initial df shape:", df.shape)
    for i in range(num_limits):
        column_name = args_list[i*4 + 1] + '_' + args_list[i*4 + 2]
        limit = int(args_list[i*4 + 3])
        frequency = str(args_list[i*4])
        df = df.loc[( (df['Frequency'] == frequency) & (df[ column_name ] < limit) ) | (df['Frequency'] != frequency)]
    print("Final df shape:", df.shape)
    return df

def select_plot(df, plot_name):
    plot_name = plot_name.lower()
    if plot_name == 'kde':
        plot_kde(df)
    elif plot_name == 'histogram':
        plot_histogram(df)
    elif plot_name == 'scatter':
        plot_scatter(df)
    elif plot_name == '3d_scatter':
        plot_3d_scatter(df)
    elif plot_name == 'heat_map':
        plot_heat_map(df)
    elif plot_name == 'strip_plot':
        plot_strip(df)

def plot_kde(df):
    for frequency in FREQUENCIES:
        df_temp = df.loc[df['Frequency'] == str(frequency)]
        for stage in STAGES:
            combs = list( combinations(ATTRIBUTES, 2) )
            plt.suptitle("KDE plot for frequency: " + str(frequency) + " stage: " + stage)
            for i, comb in list(enumerate(combs, 1)):
                xlabel, ylabel = comb
                data_x = df_temp[stage + '_' + xlabel]
                data_y = df_temp[stage + '_' + ylabel]
                plt.subplots_adjust( hspace=0.5, wspace=0.5 )
                plt.subplot(2, 3, i)
                plt.title(ylabel + ' v/s ' + xlabel)
                sns.kdeplot(data_x, data_y, cmap='Blues', shade=True, shade_lowest=False)
                plt.scatter(data_x, data_y, s=1 )
            manager = plt.get_current_fig_manager()
            manager.resize(*manager.window.maxsize())
            plt.show()


def scatter_plotting(*args):
    xval = []
    yval = []
    #print(mydb.list_collection_names())
    collection = mydb['CYCLE15']
    #collection.delete_many({})
    frequency = args[0]
    cursor = collection.find({'frequency' : frequency})
    for doc in cursor:
        if len(args)==4:
            stage = args[1]
            data_val1 = args[2]
            data_val2 = args[3]
            xval.append(doc['summary'][stage][data_val1])
            yval.append(doc['summary'][stage][data_val2])
        else:
            data_val1 = args[1]
            data_val2 = args[2]
            xval.append(doc['summary']['SP2B'][data_val1] / doc['summary']['MC1'][data_val1])
            yval.append(doc['summary']['SP2B'][data_val2] / doc['summary']['MC1'][data_val2])
    fig = plt.figure()
    if len(args)==4:
        Title = data_val1 + ' Vs. ' + data_val2 + ' (stage ' + stage + ')'
    else:
        Title = data_val1 + ' Vs. ' + data_val2
    fig.suptitle(Title)
    plt.xlabel(data_val1)
    plt.ylabel(data_val2)
    plt.scatter(xval, yval)
    plt.show(xlabel)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 summary_analysis.py <plot_type> [create]", "\nwhere plot_type is one of { scatter, kde, histogram, heat_map, 3d_scatter, strip_plot }")
        exit(1)

    if len(sys.argv) == 3:
        create_dataframe_from_db()

    try:
        df = get_data_frame()
    except:
        print("summary.pkl not found. Creating new...")
        create_dataframe_from_db()
        df = get_data_frame()

    df = clip_df(df, CLIP_LIMITS)
    plot_name = sys.argv[1]
    select_plot(df, plot_name)

if __name__ == "__main__":
    main()
