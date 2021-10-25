
# -*- coding: utf-8 -*-
"""
Updated by Nil
Date: October 24,2021       GitHub name: nzgurel         Email: ngurel@mednet.ucla.edu

-automated pig name & VF flag appearances
-bug fixes
-output plots: https://drive.google.com/drive/folders/1PYwBm_G2NNVV-48W038BEAHicU5ceDtR?usp=sharing

............
Created by Diana Ly
Date: October 20,2021       GitHub name: lydiana90         Email: lydiana@ucla.edu
Shannon Entropy plotting code
-This code reads AllEvents_shannon_entropy.csv from each animal’s directory and plots the entropy of each channel for each animal
-Created plots are in this google drive link: https://drive.google.com/drive/folders/1RFdv6ri_ZOz5TfmujsYVRos04TTj1lDS?usp=sharing
- pink plots are VF animals and blue plots are non VF animals
............
"""
# In[ ]:
    
from string import ascii_letters
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.ticker import FormatStrFormatter
import matplotlib.ticker as mticker

# In[ ]: INPUT PARAMETERS HERE

# VF animals:
VF_animals =    ['pig10153RenalAbl','pig10648','pig199923RenalAbl','pig199929','pig8343','pig9640']

color_VF = 'hotpink'
color_nonVF = 'royalblue'
    
#animal folder
animal_folder_path = 'C:/Users/ngurel/Documents/Renal_Study/Results_RenalAnimals/' 

#results folder
result_folder_path = 'C:/Users/ngurel/Documents/Renal_Study/entropy_plots'


# In[ ]:
    
# Get animal filenames
filenames = os.listdir(animal_folder_path)
filenames = [f for f in filenames if (f.startswith("pig"))] #get only the filenames that starts with pig
#sort and print the pig filenames
filenames = sorted(filenames)
print(filenames) 

# In[ ]: in each animal's folder, count files inside.

for filename in filenames:
    
    current_animal_path = animal_folder_path + filename +'/AttentionMetric_1min_20minbuff/'
    # print(current_animal_path)
    
    # Get icn filenames
    filenames_icn = os.listdir(current_animal_path)
    # print(filenames_icn) 

    # detect VF animals & prep colors & flags
    if filename in VF_animals:
        color_array = color_VF
        isVF = 1
    else:
        color_array = color_nonVF
        isVF = 0
        
    #prep figure for this animal
    if isVF == 1:
        VF_str = 'VF'
    else:
        VF_str = 'no VF'
        
    fig, ax = plt.subplots(figsize = (20,15), nrows = len(filenames_icn), ncols = 1)
    fig_title = "Entropy for animal: " + filename + ", " + VF_str
    fig.suptitle(fig_title, fontsize=25)        
    
    count = 0
    for filename_icn in filenames_icn:
        
        current_icn_path = current_animal_path + filename_icn
        # print(current_icn_path)
        
        current_channel = current_icn_path.split('_icn')[1] # channel number
        
        entropy_filepath = current_icn_path + '/' + 'AllEvents_shannon_entropy.csv'
        print("Currently at: ", entropy_filepath)
        
        df = pd.read_csv(entropy_filepath)
  
        #using mask for replace : https://kanoki.org/2019/07/17/pandas-how-to-replace-values-based-on-conditions/
        df['shannon_entropy'].mask(df['shannon_entropy'] == -999, np.nan, inplace=True) 
        
        time = df['time']
        entropy = df['shannon_entropy']  
        
        #plot the graphs for each channel
        ax[count].plot(time, entropy, '-', color = color_array)
        ax[count].spines["top"].set_visible(False)  
        ax[count].spines["right"].set_visible(False)  
        ax[count].spines["bottom"].set_visible(False)  
        # remove string from current animal name
        current_channel_num = ''.join(i for i in current_channel if i.isdigit())
        ax[count].set_ylabel(current_channel_num, fontsize = 23)
        if count == 5:
            ax[count].set_xlabel('Protocol Time (seconds)', fontsize = 25)  #x label at the bottom
        count = count + 1   
    
    #save each animal's figure
    result_filename = filename + "_entropy.png"
    result_path = result_folder_path +  '/' + result_filename
    plt.savefig(result_path)
        

