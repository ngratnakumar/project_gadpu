import pymongo
import sys
import pprint
import matplotlib
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from itertools import combinations

DB_NAME = "summary_db"

# Connect to mongodb as a client
MY_CLIENT = pymongo.MongoClient("mongodb://localhost:27017/")
MY_DB = MY_CLIENT[DB_NAME]

#pp = pprint.PrettyPrinter()

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
    return df

def select_plot( df, plot_name ):
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
    for c, frequency in enumerate(FREQUENCIES):
        df_temp = df.loc[ (df['Frequency'] == frequency) & (df['SP1_flag'] != 0) ]
        for stage in STAGES:
            combs = list( combinations(ATTRIBUTES, 2) )
            plt.suptitle("KDE plot for Frequency: " + str(frequency) + ", Stage: " + stage)
            for i, comb in list(enumerate(combs, 1)):
                xlabel, ylabel = comb
                data_x = df_temp[stage + '_' + xlabel]
                data_y = df_temp[stage + '_' + ylabel]
                plt.subplots_adjust( hspace=0.5, wspace=0.5 )
                plt.subplot(2, 3, i)
                plt.title(ylabel + ' v/s ' + xlabel)
                sns.kdeplot(data_x, data_y, cmap=CMAPS[c], cbar=True, shade=True, shade_lowest=False)
                plt.scatter(data_x, data_y, s=1, c=CMAPS[c][:-1], cmap=CMAPS[c] )
            if matplotlib.get_backend() == 'TkAgg':
                manager = plt.get_current_fig_manager()
                manager.resize(*manager.window.maxsize())
            else if matplotlib.get_backend() == 'QT':
                manager = plt.get_current_fig_manager()
                manager.window.showMaximized()
            plt.show()

def plot_histogram(df):
    for frequency in FREQUENCIES:
        df_temp = df.loc[df['Frequency'] == frequency]
        df_temp = df_temp.loc[df['SP1_flag'] == 1]
        for stage in STAGES:
            plt.suptitle("Histogram plots for frequency: " + str(frequency) + " stage: " + stage)
            ct=0
            for i in ATTRIBUTES:
                ct+=1
                str3=stage+'_'+i
                print((str3)+"    "+str(df_temp[str3].max()))
                plt.subplots_adjust( hspace=0.5, wspace=0.5 )
                plt.subplot(2, 2, ct)
                plt.grid(axis='y',alpha=0.75)
                plt.xlabel(i)
                plt.ylabel('Frequency')
                plt.title('Histogram: Stage='+stage+' Field:'+i)
                n, bins, patches=plt.hist(x=df_temp[str3], bins=20, color='#0504aa',alpha=0.7, rwidth=0.85)
            if matplotlib.get_backend() == 'TkAgg':
                manager = plt.get_current_fig_manager()
                manager.resize(*manager.window.maxsize())
            else if matplotlib.get_backend() == 'QT':
                manager = plt.get_current_fig_manager()
                manager.window.showMaximized()
            plt.show()

def plot_heat_map(df):

    sns.set(style="white")
    df1 = df.loc[df["Frequency"] == 325]
    df2 = df.loc[df["Frequency"] == 610]

    for stage in STAGES:
        stage_visibilities = stage + '_visibilities'
        stage_flux = stage + '_flux'
        stage_clean = stage + '_clean_components'
        stage_rms = stage + '_rms'
        df1_temp = df1[[stage_visibilities,stage_flux,stage_clean,stage_rms]]
        df2_temp = df2[[stage_visibilities,stage_flux,stage_clean,stage_rms]]

        #compute correlation matrix
        corr1 = df1_temp.corr(method = "spearman")
        corr2 = df2_temp.corr(method = "spearman")

        # Generate a mask for the upper triangle
        mask = np.zeros_like(corr1, dtype=np.bool)
        mask[np.triu_indices_from(mask)] = True

        #Setting plot title
        plt.suptitle("Correlation Heatmap for stage: " + stage)


        # Set up the matplotlib figure
        plt.subplot(1,2,1)
        plt.title("Frequency: 325")
        # Generate a custom diverging colormap
        cmap = sns.diverging_palette(220, 10, as_cmap=True)

        # Draw the heatmap with the mask and correct aspect ratio
        sns.heatmap(corr1, mask=mask, cmap=cmap, vmax=.3, center=0,\
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True, fmt=".2f")

        # Set up the matplotlib figure
        plt.subplot(1,2,2)
        plt.title("Frequency: 610")

        # Generate a custom diverging colormap
        cmap = sns.diverging_palette(220, 10, as_cmap=True)

        # Draw the heatmap with the mask and correct aspect ratio
        sns.heatmap(corr2, mask=mask, cmap=cmap, vmax=.3, center=0,\
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True, fmt=".2f")

        if matplotlib.get_backend() == 'TkAgg':
            manager = plt.get_current_fig_manager()
            manager.resize(*manager.window.maxsize())
        else if matplotlib.get_backend() == 'QT':
            manager = plt.get_current_fig_manager()
            manager.window.showMaximized()
        plt.show()

def plot_3d_scatter(df):

    print("func called")
    for frequency in FREQUENCIES:
        df_temp = df.loc[df['Frequency'] == frequency]
        for stage in STAGES:

            fig = plt.figure()
            ax = Axes3D(fig)
            title = "4D plot for Frequency: " + str(frequency) + " Stage: " + stage
            fig.suptitle(title)

            stage_visibilities = stage + '_visibilities'
            stage_flux = stage + '_flux'
            stage_clean = stage + '_clean_components'
            stage_rms = stage + '_rms'

            x = df_temp[stage_visibilities]
            y = df_temp[stage_rms]
            z = df_temp[stage_clean]
            c = df_temp[stage_flux]

            xlabel = stage + "visibilities"
            ylabel = stage + "rms"
            zlabel = stage + "clean"

            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.set_zlabel(zlabel)

            sc = ax.scatter(x, y, z, c=c, cmap=plt.hot())
            plt.colorbar(sc)
            plt.show()


def plot_strip(df):

    df = df[df["SP1_flag"] == 1]
    df = df.drop("Cycle", 1)
    df = df.drop("SP1_flag", 1)

    for attribute in ATTRIBUTES:
        new_df = pd.DataFrame()
        for stage in STAGES:
            query_string = stage + "_" + attribute
            new_df[query_string] = df[query_string]
        new_df["freq"] = new_df.loc[new_df["freq"].isin(FREQUENCIES)]
        splot(new_df)


def splot(df):

    sns.set(style="whitegrid")

    # "Melt" the dataset to "long-form" or "tidy" representation
    df = pd.melt(df, "freq", var_name="measurement")

    # Initialize the figure
    f, ax = plt.subplots()
    sns.despine(bottom=True, left=True)

    # Show each observation with a scatterplot
    sns.stripplot(x="value", y="measurement", hue="freq",\
        data=df, dodge=True, jitter=True,\
        alpha=.25, zorder=1)

    # Show the conditional means
    sns.pointplot(x="value", y="measurement", hue="freq",\
        data=df, dodge=.532, join=False, palette="dark",\
        markers="d", scale=.75, ci=None)

    # Improve the legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, title="freq",\
        handletextpad=0, columnspacing=1,\
        loc="lower right", ncol=3, frameon=True)

    if matplotlib.get_backend() == 'TkAgg':
        manager = plt.get_current_fig_manager()
        manager.resize(*manager.window.maxsize())
    else if matplotlib.get_backend() == 'QT':
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
    plt.show()

def plot_scatter(df):
    df = df[df["SP1_flag"] == 1]
    for frequency in FREQUENCIES:
        df_temp = df.loc[df['Frequency'] == frequency]
        for stage in STAGES:
            combs = list( combinations(ATTRIBUTES, 2) )
            plt.suptitle("Scatter plot for frequency: " + str(frequency) + " stage: " + stage)
            for i, comb in list(enumerate(combs, 1)):
                xlabel, ylabel = comb
                data_x = df_temp[stage + '_' + xlabel]
                data_y = df_temp[stage + '_' + ylabel]
                plt.subplots_adjust( hspace=0.5, wspace=0.5 )
                plt.subplot(2, 3, i)
                plt.title(ylabel + ' v/s ' + xlabel)
                plt.scatter(data_x, data_y, s=1 )
            if matplotlib.get_backend() == "TkAgg":
                manager = plt.get_current_fig_manager()
                manager.resize(*manager.window.maxsize())
            else if matplotlib.get_backend() == 'QT':
                manager = plt.get_current_fig_manager()
                manager.window.showMaximized()
            plt.show()

def print_stats(df):
    for frequency in set(df['Frequency']):
        print( "Number of data points for frequency", frequency, ":", df.loc[df['Frequency'] == frequency].shape[0] )

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

    #df = clip_df(df, CLIP_LIMITS)
    print_stats(df)
    plot_name = sys.argv[1]
    select_plot(df, plot_name)

if __name__ == "__main__":
    main()
