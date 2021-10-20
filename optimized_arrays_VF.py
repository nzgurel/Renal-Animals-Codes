# -*- coding: utf-8 -*-
"""
Updated by Nil Gurel
Date: 10/18/2021
Email: ngurel@mednet.ucla.edu
Updates:
    - filter number of BS replicates from CSV filename
    - dump best measures to a CSV
    - plot optimized state arrays from dumped CSV
    - added VF animal labels (Nil and Yuichi labels are slightly different)
    - optimized state arrays plots: https://drive.google.com/drive/folders/1VSX5UyEqp3wiDibwbbAvuFthi9orr65g?usp=sharing
    
.....
Created by Sharon Tam
Date: 10/12/2021
Github Name:
Email: sh5450@ucla.edu
Three variable plots with optimum values
-This code reads bsstats_RenalAnimals_BS100_EvRate_base.csv from the bootstrapping_coact_stats_graph.py to plot cofluctuation(exceedance), state threshold,
and CI widths to find the narrowest CI width.
-Created plots are in this google drive link: https://drive.google.com/drive/folders/1xAHxpKK0xQ_E1a3C4fvNuDUqiFxydGyD?usp=sharing
    
"""

# In[Import Libraries]: 

from string import ascii_letters
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#import seaborn as sns
import os
from matplotlib import cm
from mpl_toolkits.mplot3d.axes3d import get_test_data

# In[Set paths and format data]:

result_folder_path = 'C:/Users/ngurel/Documents/Renal_Study/Optimized_arrays'

# Read in bootstrapped event rate csv file    
bs_filepath = 'C:/Users/ngurel/Documents/Renal_Study/Renal_Bootstrapping_Results_supercomputer/Results_Bootstrapping/bsstats_RenalAnimals_BS1000_EvRate_base.csv'
df = pd.read_csv(bs_filepath)

# filter number of BS replicates from CSV filename
split_char_bs1 = 'RenalAnimals_'
split_char_bs2 = '_EvRate'
bs_replicates = bs_filepath.split(split_char_bs1)[1].split(split_char_bs2)[0]

# Delete rows with zero event rate
df = df[df['mean'].notnull()]

df.replace("0p6", 0.6, inplace = True)
df.replace("0p75", 0.75, inplace = True)
df.replace("0p9", 0.9, inplace = True)

print(df.head())

# Group data by animal
grouped = df.groupby(df.animal)

# Get animal names
animal_folder_path = 'C:/Users/ngurel/Documents/Renal_Study/Results_RenalAnimals'
animal_names = os.listdir(animal_folder_path)
animal_names = sorted(animal_names)
print(animal_names)

measures = ['rate', 'std']


# In[Plot figures]:
    
n_rows = 3
n_cols = 4
    
# Create figures (one for each measure)
fig_rate = plt.figure(figsize = (40, 15))
rate_title = "Optimum Cofluctuation and State Threshold for Minimum CI Width (MEAN) - Renal Animals"
# fig_rate.suptitle(rate_title, fontsize = 30)
fig_std = plt.figure(figsize = (40, 15))
std_title = "Optimum Cofluctuation and State Threshold for Minimum CI Width (STD) - Renal Animals"
# fig_std.suptitle(std_title, fontsize = 30)

fig_rate.subplots_adjust(top = 0.95)
fig_std.subplots_adjust(top = 0.95)
fig_rate.tight_layout()
fig_std.tight_layout()

figures = [fig_rate, fig_std]

best_stateths = []
best_coflucths = []
best_ciws = []
animals = []
measures_list = []


count = 1
for animal in animal_names:
    
    current_animal = grouped.get_group(animal)
    measure_group = current_animal.groupby('measure')
    #print(current_animal)
    

    for measure in measures:
        
        if (measure == 'rate'):
            measure_term = 'mean'
            fig_count = 0
        else:
            measure_term = 'std'
            fig_count = 1
        
        # Get data for correct measure
        current_animal_measure = measure_group.get_group(measure)
    
        interval_width = current_animal_measure['ci_width']
        state_thr = current_animal_measure['state_threshold']
        cofluctuation = current_animal_measure['exceedance']
        
        # Find narrowest confidence interval and the optimal thresholds at nonzero event rate
        min_index = interval_width.idxmin()
        min_width = interval_width[min_index]
        
        best_state_thr = state_thr[min_index]
        best_cofluc = cofluctuation[min_index]
        
        # Remove minimum values from all series
        state_thr = state_thr.drop(min_index)
        cofluctuation = cofluctuation.drop(min_index)
        interval_width = interval_width.drop(min_index)
        
        # ax_title = animal + "_" + measure_term + " Optimum Cofluctuation and \nState Threshold for Minimum CI Width (C:" + str(best_cofluc) + ", T:" + str(best_state_thr) + ", CI:" + str(round(min_width, 4)) + ")"
        ax_title = animal + " " + "(C:" + str(best_cofluc) + ", T:" + str(best_state_thr) + ", CI:" + str(round(min_width, 4)) + ")"

        # Create figure
        ax = figures[fig_count].add_subplot(n_rows, n_cols, count, projection='3d')
        
        # Plot data, different color for minimum value
        ax.scatter(state_thr, cofluctuation, interval_width, linewidths=1, alpha=.7, edgecolor='k', s = 250, c = 'blue')
        ax.scatter(best_state_thr, best_cofluc, min_width, linewidths=1, alpha=.7, edgecolor='k', s = 250, c = 'red')
        ax.set_yticks([0.6, 0.75 ,0.9])
        ax.set_title(ax_title, fontsize = 20)
        ax.set_xlabel('State Th', fontsize = 15)
        ax.set_ylabel('Cofluctuation Th', fontsize = 15)
        ax.set_zlabel('CI Width', fontsize = 15, labelpad = 10)
        plt.show()
        
        # write the best stuff to excel sheet to pull up later
        best_stateths.append(best_state_thr) 
        best_coflucths.append(best_cofluc)
        best_ciws.append(min_width)
        animals.append(animal)
        measures_list.append(measure)
        
        
    count = count + 1
        
# Save figures as pdf
savefig_pdf_str = "RenalStudy_Mean_three_var_plots.pdf"
save_path = result_folder_path + "/" + savefig_pdf_str
fig_rate.savefig(save_path)

savefig_pdf_str = "RenalStudy_std_three_var_plots.pdf"
save_path = result_folder_path + "/" + savefig_pdf_str
fig_std.savefig(save_path)

# In[CSV]: dump values to CSV
    
optimized_csv_filepath = result_folder_path + '/' +  'Renal_optimizedarrays_' + bs_replicates + '.csv'
optimized_results = {'best_stateths': best_stateths,'best_coflucths': best_coflucths, 'best_ciws': best_ciws , 'animals': animals, 'measures_list': measures_list}

df_optimized=pd.DataFrame(optimized_results)
df_optimized.to_csv(optimized_csv_filepath)  

# In[Plot state arrays using CSV thresholds]:
    
# read optimized CSV  
df_thresholds = pd.read_csv(optimized_csv_filepath, index_col = 0)   

# In[VF animal labels]: 
    
VF_animals_nil = ['pig10648','pig199923RenalAbl','pig199924','pig8343','pig9640']

VF_animals_yuichi =    ['pig10153RenalAbl','pig10648','pig199923RenalAbl','pig199929','pig8343','pig9640']
    
    
# In[optimized array figures]: 

# state array big 2 plots
fig_rate, ax_rate = plt.subplots(figsize = (20,10), nrows = len(animal_names), ncols = 1)
fig_rate_title = "Optimized state array plots (MEAN)"
fig_rate.suptitle(fig_rate_title, fontsize=16)

fig_std, ax_std = plt.subplots(figsize = (20,10), nrows = len(animal_names), ncols = 1)
fig_std_title = "Optimized state array plots (STD)"
fig_std.suptitle(fig_std_title, fontsize=16)

color_VF = 'hotpink'
color_nonVF = 'royalblue'

count_rate = 0
count_std = 0
for index, row in df_thresholds.iterrows():
    
    current_animal = row["animals"]
    current_measure = row["measures_list"]
    current_C = row["best_coflucths"] #cofluctuation threshold
    current_C_str = str(current_C-int(current_C)).split('.')[1] #to give number after . as string to filename
    current_T = row["best_stateths"] #state threshold
    
    print("Currently: ", current_animal, current_measure, current_C, current_T)
    
    # detect VF animals
    if current_animal in VF_animals_yuichi:
    # if current_animal in VF_animals_nil:
        # print("current animal is VF")
        color_array = color_VF
    else:
        color_array = color_nonVF
        
        
    coact_stats_path = animal_folder_path + "/" + animal + "/Spike" + current_measure + "Coact_output_1min_20minbuff_0p" + current_C_str + "/coactivity_stats.csv"
    # print(coact_stats_path)

    if os.path.exists(coact_stats_path):
        
        df = pd.read_csv(coact_stats_path)
        time = df['time']
        stats = df['coactivity_stat']    
    
        # Get state array data
        state_array = np.zeros(len(stats))
        for i in range(len(stats)):
            if stats[i] > current_T:
                state_array[i] = 1
                
        transition_timestamp = []
        for i in range(len(state_array) - 1):
            if (state_array[i] - state_array[i + 1]) == -1:
                transition_timestamp.append(time[i + 1])
        
    # Plot state arrays
    
    if current_measure == 'rate': #place on rate figure
            
        state_array_rate = state_array
        time_rate = time
        transition_timestamp_rate = transition_timestamp
        
        ax_rate[count_rate].plot(time_rate/3600, state_array_rate ,'--', color = color_array, alpha=0.8)
        ax_rate[count_rate].set_xticks(np.array(transition_timestamp_rate)/3600)
        ax_rate[count_rate].tick_params(axis = "x", labelsize=3)
        ax_rate[count_rate].set_yticks([0,1])    
        ax_rate[count_rate].spines["top"].set_visible(False)  
        ax_rate[count_rate].spines["right"].set_visible(False)  
        ax_rate[count_rate].spines["bottom"].set_visible(False)  
        current_animal_num = ''.join(i for i in current_animal if i.isdigit())
        ax_rate[count_rate].set_ylabel(current_animal_num, fontsize=10)
    
        count_rate = count_rate + 1
        
    
    elif current_measure == 'std': #place on std figure
    
        # print("Plotting std: ", current_animal, current_measure, current_C, current_T, count_std)
    
        state_array_std = state_array
        time_std = time
        transition_timestamp_std = transition_timestamp
        
        ax_std[count_std].plot(time_std/3600, state_array_std ,'--', color = color_array, alpha=0.8)
        ax_std[count_std].set_xticks(np.array(transition_timestamp_std)/3600)
        ax_std[count_std].tick_params(axis = "x", labelsize=3) 
        ax_std[count_std].set_yticks([0,1])    
        ax_std[count_std].spines["top"].set_visible(False)  
        ax_std[count_std].spines["right"].set_visible(False)  
        ax_std[count_std].spines["bottom"].set_visible(False)  
        current_animal_num = ''.join(i for i in current_animal if i.isdigit())
        ax_std[count_std].set_ylabel(current_animal_num, fontsize=10)
        # ax_std[count_std].set_xlabel('Experiment time (hours)', fontsize=16)    
    
        count_std = count_std + 1   
    
    else:
        
        print("current measure unknown")
    
    ax_rate[count_rate - 1].set_xlabel('Experiment time (hours)', fontsize=16)
    ax_std[count_std - 1].set_xlabel('Experiment time (hours)', fontsize=16)
    
    
# In[ Save figures ]:
    
savefig_pdf_str_rate = "20pStateArrays_mean_VF_animals_yuichi.png"
save_path_rate = result_folder_path + "/" + savefig_pdf_str_rate
fig_rate.savefig(save_path_rate)

savefig_pdf_str_std = "20pStateArrays_std_VF_animals_yuichi.png"
save_path_std = result_folder_path + "/" + savefig_pdf_str_std
fig_std.savefig(save_path_std)    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
