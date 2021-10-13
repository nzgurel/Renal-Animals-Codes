# -*- coding: utf-8 -*-
"""
Created by Sharon Tam
Date: 10/12/2021
Github Name:
Email: sh5450@ucla.edu

Three variable plots with optimum values

-This code reads bsstats_RenalAnimals_BS100_EvRate_base.csv from the bootstrapping_coact_stats_graph.py to plot cofluctuation(exceedance), state threshold,
and CI widths to find the narrowest CI width.

-Created plots are in this google drive link:
    
"""

# In[Import Libraries]: 

from string import ascii_letters
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#import seaborn as sns
import os

# In[Set paths and format data]:

result_folder_path = 'C:/Users/SmartBox/Desktop/Lab/Renal Results/Three Variable Plots'

# Read in bootstrapped event rate csv file    
df = pd.read_csv("C:/Users/SmartBox/Desktop/Lab/Renal Results/bsstats_RenalAnimals_BS100_EvRate_base.csv")

# Delete rows with zero event rate
df = df[df['mean'].notnull()]

df.replace("0p6", 0.6, inplace = True)
df.replace("0p75", 0.75, inplace = True)
df.replace("0p9", 0.9, inplace = True)

print(df.head())

# Group data by animal
grouped = df.groupby(df.animal)

# Get animal names
animal_folder_path = 'D:/Renal Study/Results_RenalAnimals'
animal_names = os.listdir(animal_folder_path)
animal_names = sorted(animal_names)
print(animal_names)

measures = ['rate', 'std']
num_cols = 1

# In[Plot figures]:
    
# Create figures (one for each measure)
fig_rate = plt.figure(figsize = (30, 150))
rate_title = "Optimum Cofluctuation and State Threshold for Minimum CI Width (MEAN)"
fig_rate.suptitle(rate_title, fontsize = 30)
fig_std = plt.figure(figsize = (30, 150))
std_title = "Optimum Cofluctuation and State Threshold for Minimum CI Width (STD)"
fig_std.suptitle(std_title, fontsize = 30)

fig_rate.subplots_adjust(top = 0.95)
fig_std.subplots_adjust(top = 0.95)
fig_rate.tight_layout()
fig_std.tight_layout()

figures = [fig_rate, fig_std]

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
        
        ax_title = animal + "_" + measure_term + " Optimum Cofluctuation and \nState Threshold for Minimum CI Width (C:" + str(best_cofluc) + ", T:" + str(best_state_thr) + ", CI:" + str(round(min_width, 4)) + ")"
        
        # Create figure
        ax = figures[fig_count].add_subplot(len(animal_names), num_cols, count, projection='3d')
        
        # Plot data, different color for minimum value
        ax.scatter(state_thr, cofluctuation, interval_width, linewidths=1, alpha=.7, edgecolor='k', s = 250, c = 'blue')
        ax.scatter(best_state_thr, best_cofluc, min_width, linewidths=1, alpha=.7, edgecolor='k', s = 250, c = 'red')
        ax.set_yticks([0.6, 0.75 ,0.9])
        ax.set_title(ax_title, fontsize = 20)
        ax.set_xlabel('State Threshold', fontsize = 15)
        ax.set_ylabel('Cofluctuation', fontsize = 15)
        ax.set_zlabel('CI Width', fontsize = 15, labelpad = 10)
        plt.show()
        
    count = count + 1
        
# Save figures as pdf
savefig_pdf_str = "RenalStudy_Mean_three_var_plots.pdf"
save_path = result_folder_path + "/" + savefig_pdf_str
fig_rate.savefig(save_path)

savefig_pdf_str = "RenalStudy_std_three_var_plots.pdf"
save_path = result_folder_path + "/" + savefig_pdf_str
fig_std.savefig(save_path)
