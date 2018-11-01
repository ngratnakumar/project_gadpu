import json
import itertools
import copy
import os
from astropy.io import fits
from pprint import pprint
from operator import itemgetter

LTA_FILE = "/home/mahak/NCRA/LTA/25_076_25oct2013.lta"
X_INFO_FILE = "/home/mahak/gadpu-xinfo/./xinfo"
OBS_NO = 6744
OBS_LOG_FILE = "/home/mahak/NCRA/LTA/6744.obslog"
OUTPUT_JSON_FILE = "/home/mahak/gadpu-xinfo/output_json"
PBCOR_FITS_FILE = "/home/mahak/NCRA/1120+143.SP2B.PBCOR.FITS"
NEW_FITS_FILE = "updated_header_file.fits"


def create_info_file(ltafile, obsno, obslog, output_file):
    command = "{} -l {} -o {} -n {} -f {}".format(X_INFO_FILE,ltafile,output_file,obsno,obslog)
    os.system(command)

# parses through the json file and finds the total source time
def merge_srctime(output_json_file):
    with open(output_json_file) as f:
        data = json.load(f)

    #sorting the data by the source as groupby needs sorted data
    data['scans'].sort(key = itemgetter("source"))

    #to store the new list of scans with cummulative onsrc_time
    new_scan = []

    #group the data by source
    for key, group in itertools.groupby(data['scans'], lambda item: item["source"]):
        #create two iterators to parse through group
        itr1, itr2 = itertools.tee(group, 2)

        # find sum for each source
        cummulative_time = sum(float(item["onsrc_time"]) for item in itr1)

        for i in itr2:
            #replace the onsrc_time with the cummulative sum
            i["onsrc_time"] = cummulative_time
            new_scan.append(i)
            break

    data["scans"] = new_scan
    #pprint(data)
    return data

def convert_dict(dict):
    new_dict = {}

    for key, value in dict.items():
        if key == "source_position":
            new_dict["SRCPOS"] = value
        elif "rest_freq1"  == key:
            new_dict["RESTFRQ1"] = value
        elif "rest_freq2"  == key:
            new_dict["RESTFRQ2"] = value
        elif "observation_no" == key:
            new_dict["OBSNUM"] = value
        else:
            key = key.replace("_","")
            key = key.upper()[:8]
            new_dict[key] = value
    return new_dict


def construct_final_header():
    data = merge_srctime(OUTPUT_JSON_FILE)
    final_dict = {}
    for key, group in data.items():
        if isinstance(group,dict):
            print(type(group))
            final_dict.update(convert_dict(group))
        else:
            for i in group:
                final_dict.update(convert_dict(i))

    #appending LTA filename
    final_dict.update({"LTAFILE":LTA_FILE})
    append_header("/home/mahak/1120+143.SP2B.PBCOR.FITS",final_dict)
    #pprint(final_dict)


def append_header(fits_img_file, dict):
    # appends the lta info dictionary to the fits header
    hdulist = fits.open(fits_img_file)
    pprint(hdulist.info())
    pprint(hdulist[0].header)
    for key,value in dict.items():
        hdulist[0].header[key] = value

    hdulist.writeto(fits_img_file,clobber = True)

    #creating a new fits file with the appended header
    # hdulist.writeto(NEW_FITS_FILE)
    # hdulist_new = fits.open(NEW_FITS_FILE)
    # pprint(hdulist_new.info())
    # pprint(hdulist_new[0].header)



create_info_file(LTA_FILE, OBS_NO, OBS_LOG_FILE,OUTPUT_JSON_FILE)
construct_final_header()
