import pymongo
import sys
import pprint
from matplotlib import pyplot as plt
import seaborn as sns

dbname = "summary_db"

# Connect to mongodb as a client
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[dbname]

pp = pprint.PrettyPrinter()

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
    plt.show()

def main():
    """if len(sys.argv) < 5:
        print("Usage: python3 summary_analysis.py <Frequency> <Stage> <Value1> <Value2>")
        exit(1)"""
    if len(sys.argv) == 4:
        scatter_plotting(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 5:
        scatter_plotting(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == "__main__":
    main()

