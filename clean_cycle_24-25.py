import os
import subprocess
import urllib.request, json
import pprint
import shutil
import glob

home = os.path.expanduser('~')

#Add your own path to GARUDATA
path_to_garudata = home + '/Music/ncra-summaryfiles/NCRADATA/cyc15-25_summ/'
cycle = 25

path_to_garudata += 'GARUDATA/IMAGING' + str(cycle) + '/CYCLE' + str(cycle) + "/"

out = glob.glob(path_to_garudata+'/*')


#print(obslist)

#for each file get its 3level up dire => obsnum and put this in res file

timefile = open('/home/ashwin/NCRA/project_gadpu/integration_time/cyc25_integration_time_resolution')
lines = timefile.readlines()
#print(lines)
flist = []

f = open('newfile2.txt', 'a')

for eachline in lines:
    fname = eachline.split('/')[-1]
    
    fname = fname.split(':')[0]
    fname = fname.split('.')[0]
    fname += '.summary'

    str1 = 'locate ' + fname
    try:
        out = subprocess.check_output(str1, shell=True)
        out = out.decode('utf-8').strip()
        out = out.split("\n")

        name = out[0]
        name = name.split('/')[10]
        #print(name)

        line = name + eachline[27:]
        f.write(line)
    except Exception as ex:
        print(ex)


#print(name)

"""

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

        shutil.move(each, obspath)"""
