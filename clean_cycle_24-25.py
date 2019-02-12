import os
import subprocess
import urllib.request, json
import pprint
import shutil
import glob

home = os.expanduser('~')

#Add your own path to GARUDATA
path_to_garudata = home + '/Music/ncra-summaryfiles/NCRADATA/cyc15-25_summ/'
cycle = 25

path_to_garudata += 'GARUDATA/IMAGING' + str(cycle) + '/CYCLE' + str(cycle) + "/"

out = glob.glob(path_to_garudata+'/*')
#os.chdir(path_to_garudata)
"""str1 = 'ls'
out = subprocess.check_output(str1, shell=True)
out = out.decode('utf-8').strip()
out = out.split("\n")"""

for each in out:
    elist = each.split('/')[-1]
    each_1 = each.split('_')

    if not elist.isdigit():
        elist = elist.split('_')
        obsval = elist[0] + '_' + elist[1]

        urlval = str('http://192.168.118.48:5000/proj_code?proj_code=' + obsval)
        with urllib.request.urlopen(urlval) as url:
            data = json.loads(url.read().decode())
        pp = pprint.PrettyPrinter()
        obsnum = data['observation_no']
        obspath = path_to_garudata+'/'+str(obsnum)
        if not os.path.exists(obspath):
            os.makedirs(obspath)

        shutil.move(each, obspath)
