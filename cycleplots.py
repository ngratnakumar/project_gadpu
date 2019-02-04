"""median of visibilities across cycles for SP2B
Y = value of median
X = Cycle number"""
import matplotlib.pyplot as plt
from summary_analysis import *

df = get_data_frame()

def cycleplot(arg):
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

    cycleslist = [15.0,16.0,17.0,18.0,20.0,22.0,23,24,25]

    clist = [15,16,17,18,20,22,23,24,25]

    SP2B_vis = []
    MC1_vis = []
    rejection_val_list = []
    accepted_val_list = []

    for cycle in (cycleslist):
        val = df.loc[df['Cycle']==cycle]

        df2 = val[val['Frequency']==arg]

        val1 = df2['SP2B_visibilities'].median()
        SP2B_vis.append(val1)
        val2 = df2['MC1_visibilities'].median()
        MC1_vis.append(val2)

        vis_accepted = df2['SP2B_visibilities'] / df2['MC1_visibilities']
        vis_rejected = 1 - (df2['SP2B_visibilities'] / df2['MC1_visibilities'])

        rejected_med = vis_rejected.median()
        accepted_med = vis_accepted.median()
        rejection_val_list.append(rejected_med)
        accepted_val_list.append(accepted_med)

    data_x = clist
    data_y1 = SP2B_vis
    data_y2 = MC1_vis
    data_y3 = rejection_val_list
    data_y4 = accepted_val_list

    """scatter"""

    #plt.scatter(data_x, data_y1, s=50, color='red')
    #plt.scatter(data_x, data_y2, s=50, color='blue')
    #plt.scatter(data_x, data_y3, s=50, color='blue')
    #plt.scatter(data_x, data_y4, s=50, color='red')


    plt.xlabel('Cycle_Number')
    plt.ylabel('vis_accepted for ' + str(int(arg)))

    #plt.plot(data_x, data_y1, '-o')
    #plt.plot(data_x, data_y2, '-o')
    plt.plot(data_x, data_y3, '-o')

    #plt.plot(data_x, data_y4, '-o')
    plt.savefig('SP2B_visibilities-' + str(int(arg)), dpi = 400)
    plt.show()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 summary_script.py <Frequency>")
        exit(1)
    frequency = float(sys.argv[1])
    cycleplot(frequency)

if __name__ == "__main__":
    main()
