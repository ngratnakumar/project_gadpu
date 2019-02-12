import os
import re
import sys
from os.path import expanduser
import pymongo
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.parser import parse
import urllib.request, json
import pprint
import subprocess
import itertools

#TODO: Now we have cyc 24, 25 file structure in similar format
#need to change scripts accordingly.. 


dbname = "summary_db"

# Connect to mongodb as a client
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[dbname]

def visibility_update(path_to_garudata, cycle):

    if cycle == '15':
        filename = path_to_garudata + "GARUDATA/" + "IMAGING" + cycle + "/CYCLE" + cycle + "/"
    elif cycle == '21':
        print("Cycle 21 is has incomplete time resolution values. Exiting now.")
        exit(1)
    else:
        filename = path_to_garudata[:-1]

    #home = expanduser("~") + "/project_gadpu"   # If project_gadpu is in home
    home = expanduser("~") + "/NCRA/project_gadpu"  # If project_gadpu is in NCRA

    timefile_name = home + "/integration_time/cyc" + cycle + "_integration_time_resolution"
    with open(timefile_name) as timefile:
        lines = timefile.readlines()

    secondslist = []
    pathlist = []
    processed_pathlist = []
    processed_secondslist = []
    visibilities = {}

    for line in lines:
        line = line.strip()
        path = line.split('.')
        timeval = line.split("=")
        timeval = timeval[-1]
        if cycle == '20' or cycle == '22' or cycle == '23':
            totalseconds = float(timeval)
        else:
            totalseconds = float(timeval.split(" ")[1])

        secondslist.append(totalseconds)
        totalpath = filename + path[0] + ".summary"
        pathlist.append(totalpath)

    for path, seconds in zip(pathlist, secondslist):
        try:
            with open(path) as fpath:
                lines = fpath.readlines()
            for value in lines:
                if 'SP2B' in value:
                    value = value.split(" ")
                    processed_pathlist.append(path)
                    processed_secondslist.append(seconds)
        except:
            print("File " + path + " not found.")
            print("Skipping...")

    for path, seconds in zip(processed_pathlist, processed_secondslist):
        final_visibility_vals = []
        with open(path) as filepath:
            readfile = filepath.readlines()
        for eachline in readfile:
            if 'visibilities' in eachline:
                eachline = eachline.split(" ")
                eachline = eachline[eachline.index("visibilities,") - 1]
                eachline = int(eachline)
                eachline = (eachline * seconds) / 378 # divide by 28c2 for the average time
                final_visibility_vals.append(eachline)
        visibilities[path] = final_visibility_vals

    return visibilities, processed_pathlist

def add_Bandwidth(path_to_garudata, cycle):

    #FIXME: Now should work for these two
    if cycle == (24 or 25):
        print("No obsnum for 24 and 25")
        exit(0)
    else:
        path_to_garudata += '/GARUDATA/IMAGING' + str(cycle) + '/CYCLE' + str(cycle) + "/"

        os.chdir(path_to_garudata)
        str1 = 'ls'
        out = subprocess.check_output(str1, shell=True)
        out = out.decode('utf-8').strip()
        out = out.split("\n")
        print(out)

        for obsnum in out:
            if obsnum == 'MIXCYCLE':
                continue
            else:
                urlval = str('http://192.168.118.48:5000/obsnum?obsnum=' + obsnum)
                #print(urlval)
                with urllib.request.urlopen(urlval) as url:
                    data = json.loads(url.read().decode())
                #print(data['bandwidth'])
                #pp = pprint.PrettyPrinter()
                #skip the obs if BW is empty
                if data['bandwidth'] == '':
                    bandwidth = None
                    #continue
                else:
                    bandwidth = data['bandwidth']

                cycleno = 'CYCLE' + str(cycle)
                collection = mydb[cycleno]
                #print(collection)
                obsnum = str(obsnum)

                collection.update({"obs_no":obsnum}, {"$set":{"bandwidth":bandwidth}}, multi=True)

def get_data_frame():
    df = pd.read_pickle('pickles/summary_dn.pkl')
    print(df.head())
    return df

def get_day_night(filename, df):
    # CHANGE THIS
    re = filename[3:]
    dn = df[df['summary_path'] == re]['dn']
    if dn.shape[0] == 0:
        return 'e'
    return dn.to_string()[-1]

def summary(path_to_GARUDATA, cycle):
    """Function to parse the required data from summary
    files- required time, frequency, visibilities, flux,
    clean_components, RMS, source, observation number,
    cycle number, date.
    """
    count = 0
    duplicates = 0
    vis_directory, file_path_list = visibility_update(path_to_GARUDATA, cycle)
    df = get_data_frame()
    for file_path in file_path_list:
        current_visibility = vis_directory[file_path]
        with open(file_path) as file:
            lines = file.readlines()
        visibility_count = 0
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
                visibility = current_visibility[visibility_count]
                visibility_count += 1
                flux = float(line[line.index("Jy") - 1])
                clean_components = int(line[line.index("CLEAN") - 1])
                rms = float(line[line.index("mJy/beam") - 1])
                dict[keyname] = {"on_source_time" : visibility, "flux" : flux, "clean_components" : clean_components, "rms" : rms}

        if lines:
            document = {}
            filename = file_path.split("/")
            dirlist = filename
            filename = filename[-1]
            document['file_name'] = filename
            document['dn'] = get_day_night(file_path, df)
            filename = filename.split(".")
            filename = filename[0]
            filename = filename.split("_")
            source = filename[1]

            matching = [s for s in filename if "GMRT" in s]
            try:
                freq = matching[0][4:]
            except:
                continue

            file_last_val = filename[-2]+"_"+filename[-1]

            obsno = dirlist[-4]

            cyclenumlist = [s for s in dirlist if "CYCLE" in s]

            cycleno = cyclenumlist[0] #dirlist[-5]

            #FIXME:date is incorrect after cycle 18
            date = dirlist[-3].split("_")[-1]
            """
            try:
                parse(date)
            except:
                date = dirlist[-3].split("_")[-2]
            """
            try:
                datetime.strptime( date, '%d%b%y' )
            except:
                try:
                    datetime.strptime( date, '%d%b%Y' )
                except:
                    date = dirlist[-3].split("_")[-2]

            #FIXME:proposal id is incorrect after cycle 18
            proposal_id = dirlist[-3].split("_")[0]

            document['source'] = source
            document['frequency'] = int(freq)
            document['obs_no'] = obsno
            document['proposal_id'] = proposal_id
            document['date'] = date
            document['summary'] = dict
            document['time'] = {'minutes': minutes, 'seconds':seconds}
            document['file_last_val'] = file_last_val

            #Insert into database
            last_entry = dict.get("SP2B")
            if last_entry is not None:
                collection = mydb[cycleno]
                old_docs = collection.find( {'source':source, 'proposal_id':proposal_id} )
                for old_doc in old_docs:
                    duplicates += 1
                    print(old_doc['date'])
                    print(old_doc['file_name'])
                    date_old = parse(old_doc['date'])
                    date_new = parse(document['date'])
                    if date_old > date_new:
                        document = old_doc
                    collection.delete_one({'_id': old_doc['_id']})
                    count -= 1

                collection.insert_one(document)
                count += 1
    print ("Number of duplicate summary files (not added to db) :", duplicates)
    return count

def temp():
    df = pd.read_pickle('../summary_path_list.pkl')
    print(df.shape)
    df['dn'] = np.random.choice(['d', 'n'], size=df.shape[0])
    df.to_pickle('summary_dn.pkl')

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 summary_script.py <path_to_GARUDATA> <cycle>")
        exit(1)
    path_to_GARUDATA = sys.argv[1]
    cycle = sys.argv[2]
    #temp()
    count = summary(path_to_GARUDATA, cycle)
    print("Inserted", count, "documents into summary_db")
    #add_Bandwidth(path_to_GARUDATA, cycle)

if __name__ == "__main__":
    main()
