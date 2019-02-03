"""median of visibilities across cycles for SP2B
Y = value of median
X = Cycle number"""
import matplotlib.pyplot as plt
from summary_analysis import *

df = get_data_frame()

print(df)

cycle = df['Cycle']
cycle = cycle.astype(int)

vis = df['SP2B_visibilities']
#vis = df['SP2B_rms']
#vis = df['SP2B_flux']
#vis = df['SP2B_clean_components']
#vis = df['MC1_clean_components']
#vis = df['MC1_flux']
#vis = df['MC1_rms']
#vis = df['MC1_visibilities']

cycleslist = [15.0,16.0,17.0,18.0,19.0,20.0,22.0,23,24,25]

clist = [15,16,17,18,19,20,22,23,24,25]

lst1 = []
lst2 = []
lst3 = []
lst4 = []

for cycle in (cycleslist):
    val = df.loc[df['Cycle']==cycle]
    val1 = val['SP2B_visibilities'].median()
    lst1.append(val1)
    val2 = val['MC1_visibilities'].median()
    lst2.append(val2)

    vis_accepted = val['SP2B_visibilities'] / val['MC1_visibilities']
    vis_rejected = 1 - (val['SP2B_visibilities'] / val['MC1_visibilities'])

    rejected_med = vis_rejected.median()
    accepted_med = vis_accepted.median()
    lst3.append(rejected_med)
    lst4.append(accepted_med)

data_x = clist
data_y1 = lst1
data_y2 = lst2
data_y3 = lst3
data_y4 = lst4

"""scatter"""

#plt.scatter(data_x, data_y1, s=50, color='red')
#plt.scatter(data_x, data_y2, s=50, color='blue')
#plt.scatter(data_x, data_y3, s=50, color='blue')
#plt.plot(data_x, data_y1, '-o')
#plt.plot(data_x, data_y2, '-o')
#plt.plot(data_x, data_y3, '-o')
plt.plot(data_x, data_y4, '-o')

plt.show()