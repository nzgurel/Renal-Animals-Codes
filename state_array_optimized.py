# -*- coding: utf-8 -*-
"""

Updated by Nil Gurel
Date: 10/10/2021
Email: ngurel@mednet.ucla.edu

Updates: 
    - folder name fixed "Coact"
    - fixed time limits commented out to get the whole coact_stats. We need interval timestamps for the final version of this
    - confirmed running on supercomputer
    -code outputs are here: https://drive.google.com/drive/folders/1mJ2upWTw4Y5qn-1aLmykxzSWWhYSDn7r?usp=sharing
    
    ------

Created by Sharon Tam
Date: 10/06/2021
Github Name:
Email: sh5450@ucla.edu

State Array Plots at Optimized Thresholds

-This code reads bsstats_RenalAnimals_BS100_EvRate_base.csv from the bootstrapping_coact_stats_graph.py to find the narrowest
confidence interval and uses those optimal thresholds to plot the occurence of events.

-Created plots are in this google drive link: https://drive.google.com/drive/folders/1cdQzL4OZQ9D4y6TLw9A36rjkTp2GoUny?usp=sharing
    
"""

# In[Import Libraries]: 

from string import ascii_letters
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import os

# In[Paths and parameters]:

result_folder_path = '/media/dal/BigDrive/Renal_Study/Results_OptimizedStateArray/'

# Read in bootstrapped event rate csv file    
df = pd.read_csv("/media/dal/BigDrive/Renal_Study/Results_Bootstrapping/bsstats_RenalAnimals_BS1000_EvRate_base.csv")

# Delete rows with zero event rate
df = df[df['mean'].notnull()]

# Group data by animal
grouped = df.groupby(df.animal)

# Get animal names
animal_folder_path = '/media/dal/BigDrive/Renal_Study/Results_RenalAnimals'
animal_names = os.listdir(animal_folder_path)
animal_names = sorted(animal_names)
print(animal_names)

# End of Baseline timestamps 
# EndBaseline_Renal = [20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000]

# In[Plot state arrays]:
    
# Loop through each animal
count = 0
for animal in animal_names:
    current_animal = grouped.get_group(animal)
    #print(current_animal)
    
    interval_width = current_animal['ci_width']
    #print(interval_width)
    
    # Find narrowest confidence interval and the optimal thresholds at nonzero event rate
    min_index = interval_width.idxmin()
    min_width = interval_width[min_index]
    #print(min_index)
         
    measure_type = current_animal['measure']
    state_thr = current_animal['state_threshold']
    exceedance_thr = current_animal['exceedance']
    
    best_state_thr = state_thr[min_index]
    best_exc_thr = exceedance_thr[min_index]
    best_measure = measure_type[min_index]
    
    print("Best state threshold: " + str(best_state_thr))
    print("Best exceedance threshold: " + best_exc_thr)
    print("Best measure: " + best_measure)
    
    # End of Baseline linewidth
    # lw_EndBaseline = 3
    
    # Formatter
    label_format = '{:,.3f}'

    # Main figure
    fig, ax = plt.subplots(figsize = (22,5), nrows = 1, ncols = 1)
    str_state_title = "StateArrayPlot_" + animal + "_" + best_measure + "_" + best_exc_thr + "_" + str(best_state_thr) + "(ci_width: " + str(min_width) + ")"
    fig.suptitle(str_state_title, fontsize=16)
    
 
    # Creating events out of coactivity
    # time_between contains all timestamps exceeding Thr%
    # while >Thr is observed, record only until we go below
    
    # Read in stats for best exceedance
    stats_path = animal_folder_path + "/" + animal + "/Spike" + best_measure + "Coact_output_1min_20minbuff_" + best_exc_thr + "/coactivity_stats.csv"
    if os.path.exists(stats_path):
        df = pd.read_csv(stats_path)
        time = df['time']
        stats = df['coactivity_stat']
                
        del df
                
        # Get state array data
        state_array = np.zeros(len(stats))
        for i in range(len(stats)):
            if stats[i] > best_state_thr:
                state_array[i] = 1
                
        transition_timestamp = []
        for i in range(len(state_array) - 1):
            if (state_array[i] - state_array[i + 1]) == -1:
                transition_timestamp.append(time[i + 1])
          
        
        # Plot state array
        ax.plot(time/3600, state_array ,'--', color = 'dodgerblue', alpha=0.8)
        ax.set_xticks(np.array(transition_timestamp)/3600)
        # ax.set_xlim(time[0]/3600, EndBaseline_Renal[count]/3600) #limiting to baseline data only
        # ax.axvline(x = EndBaseline_Renal[count]/3600, color = 'black', linewidth = lw_EndBaseline) #full exp, mark end of baseline for each
        ax.tick_params(axis = "x", labelsize=3)
        ax.set_yticks([0,1])    
        ax.spines["top"].set_visible(False)  
        ax.spines["right"].set_visible(False)  
        ax.spines["bottom"].set_visible(False)  
        ax.set_ylabel(animal, fontsize=16)
        ax.set_xlabel('Experiment time (hours)', fontsize=16)

        # Save state array plot
        str_state_savefig_pdf = animal + "_PDF_" + best_measure + "_" + best_exc_thr + "_" + str(best_state_thr) + "_StateArray_fullexp.pdf"
        state_pdf_path = result_folder_path + "/" + str_state_savefig_pdf
        plt.savefig(state_pdf_path)
    
    count = count + 1
    


