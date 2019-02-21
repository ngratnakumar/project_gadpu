import os
import urllib.request, json
import pprint
import subprocess
import summary_script
import itertools
import pandas as pd

"""def newfn(obsno):
    path_to_garudata = '/home/ashwin/Music/ncra-summaryfiles/NCRADATA/cyc15-25_summ/'
    for root, sdir, files in os.walk(path_to_garudata):
        print(root)"""

def add_Bandwidth(path_to_garudata, cycle):

    if cycle == (24 or 25):
        print("No obsnum for 24 and 25")
        exit(0)
    else:
        path_to_garudata += 'GARUDATA/IMAGING' + str(cycle) + '/CYCLE' + str(cycle) + "/"

        os.chdir(path_to_garudata)
        str1 = 'ls'
        out = subprocess.check_output(str1, shell=True)
        out = out.decode('utf-8').strip()
        out = out.split("\n")

#print(out)

#print(lst)
#obsno = str(4637)

        for obsnum in out:
            if obsnum == 'MIXCYCLE':
                continue
            else:
                urlval = str('http://192.168.118.48:5000/obsnum?obsnum=' + obsnum)
                print(urlval)
                with urllib.request.urlopen(urlval) as url:
                    data = json.loads(url.read().decode())
                pp = pprint.PrettyPrinter()
                #pp.pprint(data['bandwidth'])
                #skip the obs if BW is empty
                if data['bandwidth'] == '':
                    bandwidth = None
                    #continue
                else
                    bandwidth = data['bandwidth']

                collection = mydb[cycleno]
                obsnum = str(obsnum)
                docs = collection.find({'obs_no':obsnum})
                for doc in docs:
                    db.collection.update({'obs_no':obsnum}, {$set:{'bandwidth':bandwidth}})
                    #doc['bandwidth'] = bandwidth
