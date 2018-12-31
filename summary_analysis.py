import pymongo
import sys
import pprint
from matplotlib import pyplot as plt

dbname = "summary_db"

# Connect to mongodb as a client
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[dbname]

pp = pprint.PrettyPrinter()

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

def main():
    if len(sys.argv) < 5:
        print("Usage: python3 summary_analysis.py <Frequency> <Stage> <Value1> <Value2>")
        exit(1)
    scatter_plotting(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == "__main__":
    main()
