import pymongo
import os
import sys
from os.path import expanduser

dbname = "summary_db"

# Connect to mongodb as a client
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[dbname]

def vis_update(path_to_garudata, cycle):

    if cycle == 15:
        fname = path_to_garudata + "GARUDATA/" + "IMAGING" + cycle + "/CYCLE" + cycle + "/"
    else:
        fname = path_to_garudata[:-1]

    home = expanduser("~") + "/project_gadpu"

    timefile_name = home + "/integration_time/cyc" + cycle + "_integration_time_resolution"
    with open(timefile_name) as timefile:
        lines = timefile.readlines()

    secondlist = []
    pathlist = []
    processed_pathlist = []
    processed_secondlist = []
    visibilities = {}

    for line in lines:
        path = line.split('.')
        timeval = line.split("=")
        timeval = timeval[-1]
        totalseconds = float(timeval.split(" ")[1])

        secondlist.append(totalseconds)
        totalpath = fname + path[0] + ".summary"
        pathlist.append(totalpath)

    for path, seconds in zip(pathlist, secondlist):
        with open(path) as fpath:
            lines = fpath.readlines()
        for value in lines:
            if 'SP2B' in value:
                value = value.split(" ")
                processed_pathlist.append(path)
                processed_secondlist.append(seconds)

    for path, seconds in zip(processed_pathlist, processed_secondlist):
        final_vis_vals = []
        with open(path) as filepath:
            readfile = filepath.readlines()
        for eachline in readfile:
            if 'visibilities' in eachline:
                eachline = eachline.split(" ")
                eachline = eachline[eachline.index("visibilities,") - 1]
                eachline = int(eachline)
                eachline = eachline * seconds
                final_vis_vals.append(eachline)
        visibilities[path] = final_vis_vals

    return visibilities, processed_pathlist, fname


def summary(path_to_GARUDATA, cycle):
    """Function to parse the required data from summary 
    files- required time, frequency, visibilities, flux, 
    clean_components, RMS, source, observation number, 
    cycle number, date.
    """
    count = 0
   
    vis_directory, plist, filename = vis_update(path_to_GARUDATA, cycle)

    i = 0
    for file_path in plist:
        curr_vis = vis_directory[file_path]
        with open(file_path) as f:
            lines = f.readlines()
        i = 0
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
                visibility = curr_vis[i]
                i = i + 1
                flux = float(line[line.index("Jy") - 1])
                clean_components = int(line[line.index("CLEAN") - 1])
                rms = float(line[line.index("mJy/beam") - 1])
                dict[keyname] = {"visibilities" : visibility , "flux" : flux , "clean_components" : clean_components , "rms" : rms}

        if lines:
            fname = file_path.split("/")
            dirlist = fname
            fname = fname[-1]
            fname = fname.split(".")
            fname = fname[0]
            fname = fname.split("_")
            source = fname[1]
            freq = fname[2][4:]
            file_last_val = fname[-2]+"_"+fname[-1]

            obsno = dirlist[-4]
            cycleno = dirlist[-5]
            date = dirlist[-3].split("_")[1]

            document = {}
            document['source'] = source
            document['frequency'] = int(freq)
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
        print("Usage: python3 summary_script.py <path_to_GARUDATA> <cycle>")
        exit(1)
    path_to_GARUDATA = sys.argv[1]
    cycle = sys.argv[2]
    count = summary(path_to_GARUDATA, cycle)
    print("Inserted", count, "documents into summary_db")

if __name__ == "__main__":
    main()
