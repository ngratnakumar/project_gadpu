"""Script to change the directory structure,
making it similar to structure for cycle 15-23"""

import os
import subprocess
import urllib.request, json
import pprint
import shutil
import glob
from os.path import expanduser

home = os.path.expanduser('~')

#Add your own path to GARUDATA
#path_to_garudata = home + '/Music/ncra-summaryfiles/NCRADATA/cyc15-25_summ/'

#path_to_garudata += 'GARUDATA/IMAGING' + str(cycle) + '/CYCLE' + str(cycle) + "/"

filenames = glob.glob(path_to_garudata+'/*')

#for each file get its 3level up dire => obsnum and put this in res file

def change_structure():
    timefile = open(home + '/NCRA/project_gadpu/integration_time/cyc25_integration_time_resolution')
    lines = timefile.readlines()

    f = open('newfile2.txt', 'a')

    for eachline in lines:
        fname = eachline.split('/')[-1]
        
        fname = fname.split(':')[0]
        fname = fname.split('.')[0]
        fname += '.summary'

        str1 = 'locate ' + fname
        try:
            filenames = subprocess.check_output(str1, shell=True)
            filenames = filenames.decode('utf-8').strip()
            filenames = filenames.split("\n")

            name = filenames[0]
            name = name.split('/')[10]

            line = name + eachline[27:]
            f.write(line)
        except Exception as ex:
            print(ex)

def main():
    change_structure()


if __name__ == main():
    main()
