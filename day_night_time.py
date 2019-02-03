#check empty files - file with name of these files
# ltaclean : frmterror
#check for zero length scan - file with name of these files 

import pandas as pd
import numpy as np
import subprocess

def get_sec(time_str):
    #print(time_str)
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

df = pd.read_pickle('pickles/summary_path_list25.pkl')

cnt = 0

lt = []
slen=len(df['summary_path'])
df['dn']=pd.Series(np.random.randn(slen),index=df.index)

for i in range(df.shape[0]):
    string = df['summary_path'][i]
    #print(string)
    string = string.split("/")
    source = string[-1]
    string = string[2:-2]
    string = '/'.join(string)
   # print(string)
    source = source.split("_")[1]
    #print(source)
    str1 = "find " + "/" + string + " -iname '*.lta'"
    outp = subprocess.check_output(str1, shell=True)
    outp = outp.decode("utf-8")
    if(outp):
        outp=outp.strip('\n')
        fname = outp.split("/")[-1]
    else:
        #print("dsfsf")
        str1 = "find " + "/" + string + " -iname '*.lta.1'"
        outp = subprocess.check_output(str1, shell=True)
        outp = outp.decode("utf-8")
        outp = outp.strip("\n")
        fname = outp.split("/")[-1]
        #print(fname)

    try:
    #print(string + "/" + fname)
        str2 = "./ltahdr -i " + "/" + string + "/" + fname + "| grep " + source
        #print(fname + " " + source)
        outp2 = subprocess.check_output(str2, shell=True)
        outp2 = outp2.decode("utf-8")
    #if not outp2:
    
        outp2 = outp2.split("\n")
        #print(outp2)

        var1=outp2[0].split()
        #print(var1)
        #var1 = [x for x in var1 if x is not '']
        startval = var1[-4]

        var2 = outp2[-2].split()
        #var2 = [x for x in var2 if x is not '']
        endval = var2[-4]

        if ':' not in startval:
            startval = outp2[1].split()[-4]           

    except Exception as ex: 
        str3 = "./ltahdr -i " + "/" + string + "/" + fname
        try:
            ltaoutput = subprocess.check_output(str3, shell=True)
        except:
            df['dn'][i] = 'e'
            cnt += 1
            continue
        ltaoutput = ltaoutput.decode("utf-8")
        ltaoutput = ltaoutput.replace(".", "-")
        ltaoutput = ltaoutput.replace("_", "-")
        #print(source)
        #print(ltaoutput)
        lta_list = ltaoutput.split()
        try:
            index1 = lta_list.index(source)
            index2 = len(lta_list) - 1 - lta_list[::-1].index(source)
        except:
            df['dn'][i] = 'e'
            cnt += 1
            continue

        #print("In except")

        startval = (lta_list[index1 + 4])
        endval = (lta_list[index2 + 4])

    start = get_sec(startval)
    end = get_sec(endval)

    time = int((end + start) / 2)
    daytime = time // 3600

    if daytime >= 21 or daytime <= 6:
        df['dn'][i] = 'n'
    elif daytime > 6  or daytime < 21:
        df['dn'][i] = 'd'
        #print("D")
    
    #print(df['dn'][i])
    """
    except Exception as ex:
        cnt += 1
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        df['dn'][i] = 'e'
        #print (message)
       # print(string + "/" + fname+ "   "+ source)
       # print("File error")
    """

print(cnt)

df.to_pickle("new_dataframe25.pkl")
print('Pickle file created.')
