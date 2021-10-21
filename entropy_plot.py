# -*- coding: utf-8 -*-
"""
Created by Sharon Tam
Date: 10/19/2021
Github Name:
Email: sh5450@ucla.edu

Shannon Entropy Plots

-This code reads AllEvents_shannon_entropy.csv from each channel for every animal and plots the entropy values

-Created plots are in this google drive link: https://drive.google.com/drive/folders/1IDilhIEjn-zn_RrtZ9_QD4spaTOzqFp2?usp=sharing

"""


# In[Import Libraries]: 

from string import ascii_letters
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import os

# In[Get parameter values]:
    
result_folder_path = 'C:/Users/SmartBox/Desktop/Lab/Results 10_20/Entropy Plots'

animal_types = ['VF', 'Normal']
color_codes = ['magenta', 'blue']

# In[ ]:
    
animal_count = 0
vf_animal_count = 0
for animal_type, type_color in zip(animal_types, color_codes):
    
    # Get animal names
    animal_folder_path = 'D:/Renal Study/Results_RenalAnimals/' + animal_type + "Animals"
    animal_names = os.listdir(animal_folder_path)
    animal_names = sorted(animal_names)
    print(animal_names)
        
    # Loop through each animal
    for animal in animal_names:
    
        current_path = animal_folder_path + "/" + animal
        
        attention_metric_path = current_path + "/AttentionMetric_1min_20minbuff"
        channel_list = os.listdir(attention_metric_path)
        channel_list = sorted(channel_list)
        print(channel_list)
        
        # Create fig for animal for channels
        entropy_fig, entropy_ax = plt.subplots(figsize = (22,15), nrows = len(channel_list), ncols = 1, squeeze = False)
        entropy_fig.suptitle(animal + ' Entropy_' + animal_type, fontsize = 30)
        entropy_fig.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.7)
        
        channel_count = 0
        for channel in channel_list:
            
            entropy_file_path = attention_metric_path + "/" + channel + "/AllEvents_shannon_entropy.csv"
            
            # Read in data
            df = pd.read_csv(entropy_file_path)
            # Remove unknown values
            df = df.replace(-999, np.nan)
            
            time = df['time']
            stats = df['shannon_entropy']
            
            del df
            
            # Plot entropy (for each channel)
            ax1 = entropy_ax[channel_count][0]
            ax1.plot(time/3600, stats, color = type_color)
            ax1.set_title(channel + " shannon entropy")
            ax1.set_xlabel('Experiment time (hours)', fontsize = 12)
            ax1.set_ylabel("Entropy", fontsize = 12)
            ax1.tick_params(axis = "x", labelsize=3)
            ax1.spines["top"].set_visible(False)  
            ax1.spines["right"].set_visible(False)
            plt.show()
            
            channel_count = channel_count + 1
        

        # Save coact stats plot for each animal                    
        entropy_savefig_pdf_str= animal + "_PDF_shannon_entropy_plot.pdf"
        entropy_pdf_path = result_folder_path + "/" + entropy_savefig_pdf_str
        entropy_fig.savefig(entropy_pdf_path)    
    
            
            