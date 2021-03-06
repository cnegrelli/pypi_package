import numpy as np
import  matplotlib.pyplot as plt
import pandas as pd

def single_pulses(n_files, n_pulses, period, output_csv, n_bins=1220):
    
    ''' This funtion converts the output files from waterfall.py into
    a single csv files with all the single pulses (row = one pulse). 
    Also plots the folded pulse to check.

    Args:
        n_files: (int) number of imput files counting from 0
        n_pulses: (int) how many single pulses you want
        period: (float) period of the pulse in seconds obtained from presto
        output_csv: (string) name of the output csv file
        n_bins: (int) how many points per single pulse. default: 1220

    Returns: nothing

    '''

    # times array
    file_name_1 = 'times_{}.csv'
    df_list_1 = []
    for i in range(0, n_files+1):
        df_list_1.append(pd.read_csv(file_name_1.format(i), header=None))
    times = (pd.concat(df_list_1).to_numpy()).T.flatten()

    # intensity array
    file_name_2 = 'original_{}.csv'
    df_list_2 = []
    for i in range(0, n_files+1):
        df_list_2.append(pd.read_csv(file_name_2.format(i), header=None))
    originals = (pd.concat(df_list_2).to_numpy()).T.flatten()

    #Create a new vector of times to match the period:
    new_dt = period/n_bins
    new_times=np.zeros(n_bins*n_pulses)
    new_times[0]=times[0]
    for i in range (1,len(new_times)):
        new_times[i] = new_times[i-1] + new_dt

    # Interpolation
    new_data = (np.interp (new_times, times, originals)).reshape((n_pulses,n_bins))

    # Write table
    np.savetxt(output_csv,new_data,delimiter=',')

    # Plot
    folded = np.sum(new_data,axis=0)
    plt.figure(figsize=(20,10))
    plt.xlim(0,n_bins)
    plt.plot(folded)
    plt.savefig('pulse.png')

    pass