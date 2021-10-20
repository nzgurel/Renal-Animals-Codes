# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 20:20:34 2021

@author: NGurel


Created by Nil Gurel
Date: 10/12/2021
Email: ngurel@mednet.ucla.edu

Arrays of low cofluctuation
During period of very low confluctuation, entropy would go up because you might be losing sight of the target 

-output figures: https://drive.google.com/drive/folders/1jskZr5RAH3e7CTLMI0XrB0hzFV_MMFVv?usp=sharing

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
    
result_folder_path = 'C:/Users/ngurel/Documents/Renal_Study/low_cofluctuation_arrays'

# Get animal names
animal_folder_path = 'C:/Users/ngurel/Documents/Renal_Study/Results_RenalAnimals'
animal_names = os.listdir(animal_folder_path)
animal_names = sorted(animal_names)
print(animal_names)

measures = ['rate', 'std']


#cofluctuation thresholds: 0p6, 0p75, 0p9 (6, 75, 9)
cofluctuation_threshold = '9'

#low state threshold: 0p6, 0p75, 0p9 (6, 75, 9)
lowstate_th = 70


# VF animal labels: 
VF_animals =    ['pig10153RenalAbl','pig10648','pig199923RenalAbl','pig199929','pig8343','pig9640']

# In[low cofluctuation state array figures]: 

# state array big 2 plots
fig_rate, ax_rate = plt.subplots(figsize = (20,10), nrows = len(animal_names), ncols = 1)
fig_rate_title = "Low Cofluctuation state array plots (MEAN, 0p" + cofluctuation_threshold + ", stateth " + str(lowstate_th) + ")"
fig_rate.suptitle(fig_rate_title, fontsize=16)

fig_std, ax_std = plt.subplots(figsize = (20,10), nrows = len(animal_names), ncols = 1)
fig_std_title = "Low Cofluctuation state array plots (STD, 0p" + cofluctuation_threshold + ", stateth " + str(lowstate_th) + ")"
fig_std.suptitle(fig_std_title, fontsize=16)

color_VF = 'hotpink'
color_nonVF = 'royalblue'

count_rate = 0
count_std = 0

for animal_name in animal_names:
    
    for measure in measures:
        
        current_animal = animal_name
        current_measure = measure
        current_C = cofluctuation_threshold
        current_T = lowstate_th #state threshold, 20 for low
        
        print("Currently: ", current_animal, current_measure, current_C, current_T)
        
        # detect VF animals
        if current_animal in VF_animals:
            color_array = color_VF
        else:
            color_array = color_nonVF
            
            
        coact_stats_path = animal_folder_path + "/" + current_animal + "/Spike" + current_measure + "Coact_output_1min_20minbuff_0p" + str(current_C) + "/coactivity_stats.csv"
        # print(coact_stats_path)
    
        if os.path.exists(coact_stats_path):
            
            df = pd.read_csv(coact_stats_path)
            time = df['time']
            stats = df['coactivity_stat']    
        
            # Get state array data
            state_array = np.zeros(len(stats))
            for i in range(len(stats)):
                if stats[i] < current_T:
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
    
    

    
savefig_pdf_str_rate = "20pStateArrays_VF_groups_mean_0p" + cofluctuation_threshold + "_stateth_" + str(lowstate_th) + ".png"
save_path_rate = result_folder_path + "/" + savefig_pdf_str_rate
fig_rate.savefig(save_path_rate)

savefig_pdf_str_std = "20pStateArrays_VF_groups_std_0p" + cofluctuation_threshold + "_stateth_" + str(lowstate_th) + ".png"
save_path_std = result_folder_path + "/" + savefig_pdf_str_std
fig_std.savefig(save_path_std)    
    
    