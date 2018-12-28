import pymongo
import os

dbname = "ncra_database"
colname = "summary_files"

#connect to mongodb as a client
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[dbname]
mycol = mydb[colname]

#TODO : Create a final dictionary and write to the database

def summary():
    """Function to parse the required data - required time, 
    frequency, visibilities, flux, clean_components, RMS,
    source, observation number, cycle number, date.
    """
    print("Please enter the absolute path to GARUDATA")
    path_to_GARUDATA = input()

    flag = 0
    for root,dirs,files in os.walk(path_to_GARUDATA):
        for fname in files:
            fn = root + "/" + fname
            fp = open(fn)
            lines = fp.readlines()
            document = {}
            dict = {}
            for line in lines:
                flag = 1
                if 'processing took' in line:
                    if 'day' in line:
                        line = line.split(" ")
                        total_time = (int(line[3]) * 24 * 60)
                        temp_time = line[5].split(":")  
                        total_time += int(temp_time[0]) * 60 + int(temp_time[1])
                        seconds = temp_time[2]
                        print("Total time required for processing is : " + str(total_time) + " minutes " + seconds + " seconds")
                    else:
                        line = line.split(" ")
                        temp_time = line[3].split(":")
                        total_time = int(temp_time[0]) * 60 + int(temp_time[1])
                        seconds = temp_time[2]
                        print("Total time required for processing is : " + str(total_time) + " minutes " + seconds + " seconds") 

                if 'image' in line:
                    line = line.split(" ")
                    index = line.index("image:") - 1
                    keyname = line[index]
                    visibility = int(line[line.index("visibilities,") - 1])
                    flux = float(line[line.index("Jy") - 1])
                    clean_components = int(line[line.index("CLEAN") - 1])
                    rms = float(line[line.index("mJy/beam") - 1])
                    dict[keyname] = {"visibilities" : visibility , "flux" : flux , "clean_components" : clean_components , "rms" : rms}

            if flag == 1:
                fname = fname.split("_")
                source = fname[1]
                freq = fname[2][4:]
            
                dirlist = root.split("/")
                obsno = dirlist[-3]
                cycleno = dirlist[-4]
                date = dirlist[-2].split("_")[1]
