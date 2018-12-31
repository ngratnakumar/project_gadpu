import pymongo
import os
import sys
from matplotlib import pyplot as plt

dbname = "summary_db"

# Connect to mongodb as a client
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[dbname]

def summary(path_to_GARUDATA):
    """Function to parse the required data from summary 
    files- required time, frequency, visibilities, flux, 
    clean_components, RMS, source, observation number, 
    cycle number, date.
    """
    count = 0
    visibility_list = []
    rms_list= []
    clean_list = []
    flux_list = []
    for root, dirs, files in os.walk(path_to_GARUDATA):
        for fname in files:
            file_path = os.path.join(root, fname)
            with open(file_path) as f:
                lines = f.readlines()
            dict = {}
            for line in lines:
                if 'processing took' in line:
                    if 'day' in line:
                        line = line.split(" ")
                        minutes = (int(line[3]) * 24 * 60)
                        temp_time = line[5].split(":")
                        minutes += int(temp_time[0]) * 60 + int(temp_time[1])
                        seconds = temp_time[2]
                    else:
                        line = line.split(" ")
                        temp_time = line[3].split(":")
                        minutes = int(temp_time[0]) * 60 + int(temp_time[1])
                        seconds = temp_time[2]
                if 'image' in line:
                    line = line.split(" ")
                    index = line.index("image:") - 1
                    keyname = line[index]
                    visibility = int(line[line.index("visibilities,") - 1])
                    flux = float(line[line.index("Jy") - 1])
                    clean_components = int(line[line.index("CLEAN") - 1])
                    rms = float(line[line.index("mJy/beam") - 1])
                    dict[keyname] = {"visibilities" : visibility , "flux" : flux , "clean_components" : clean_components , "rms" : rms}
                    visibility_list.append(visibility)
                    flux_list.append(flux)
                    clean_list.append(clean_components)
                    rms_list.append(rms)

            if lines:
                fname = fname.split("_")
                source = fname[1]
                freq = fname[2][4:]
                file_last_val = fname[-2]+"_"+fname[-1]

                dirlist = root.split("/")
                obsno = dirlist[-3]
                cycleno = dirlist[-4]
                date = dirlist[-2].split("_")[1]

                document = {}
                document['source'] = source
                document['frequency'] = freq
                document['obs_no'] = obsno
                document['date'] = date
                document['summary'] = dict
                document['time'] = {'minutes': minutes, 'seconds':seconds}
                document['file_last_val'] = file_last_val

                # Insert into database
                last_entry = dict.get("SP2B")
                if last_entry is not None:
                    collection = mydb[cycleno]
                    collection.insert_one(document)
                    count += 1

    return count

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 summary_script.py <path_to_GARUDATA>")
        exit(1)
    path_to_GARUDATA = sys.argv[1]
    count = summary(path_to_GARUDATA)
    print("Inserted", count, "documents into summary_db")

if __name__ == "__main__":
    main()
