
# -*- coding: utf-8 -*-
"""
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

#indicate which pig we are plotting
pig = 'pig199924'
#these pigs are VF:
VF_animals_yuichi =    ['pig10153RenalAbl','pig10648','pig199923RenalAbl','pig199929','pig8343','pig9640']

color_VF = 'hotpink'
color_nonVF = 'royalblue'
# detect VF animals
if pig in VF_animals_yuichi:
    color_array = color_VF
else:
    color_array = color_nonVF
    
#path to data folder
data_folder_path = '/Users/dianaly/Desktop/Lab/Python/Data&Results for Coactivity/Results_RenalAnimals/' + pig +'/AttentionMetric_1min_20minbuff/'

#path to result folder
result_folder_path = '/Users/dianaly/Desktop/Lab/Python/Data&Results for Coactivity/Entropy Results/'

# In[ ]:
    
# Get animal filenames
filenames = os.listdir(data_folder_path)
filenames = [f for f in filenames if (f.startswith("pig"))] #get only the filenames that starts with pig
#sort and print the pig filenames
filenames = sorted(filenames)
print(filenames) 


# In[ ]:

    #create empty figure a set size and number of rows and columns
fig, ax = plt.subplots(figsize = (50,20), nrows = len(filenames), ncols = 1)  

count = 0
for filename in filenames:
    
    current_path = data_folder_path + filename
    # print(current_path)
    current_channel = current_path.split(pig+'_icn')[1] #obtain just the channel name without the "_icn"

    
    entropy_filepath = current_path + '/' + "AllEvents_shannon_entropy.csv"
    print(entropy_filepath)
    df = pd.read_csv(entropy_filepath)  
    
    time = df['time']
    entropy = df['shannon_entropy']    
    entropy.replace(-999, "nan")
    
    #plot the graphs for each channel
    ax[count].plot(time, entropy, '--', color = color_array)
    # ax.tick_params(axis = "x", labelsize=3)
    # if the animal is in VF then plot the vertical line at the timestamp
    # if VF == 1:
    #     ax[count].axvline(x = VF_time, linewidth = 5, color = 'green' )
    ax[count].spines["top"].set_visible(False)  
    ax[count].spines["right"].set_visible(False)  
    ax[count].spines["bottom"].set_visible(False)  
    # remove string from current animal name
    current_channel_num = ''.join(i for i in current_channel if i.isdigit())
    ax[count].set_ylabel(current_channel_num, fontsize = 23)
    if count == 5:
        ax[count].set_xlabel('Protocol Time (seconds)', fontsize = 25)  #x label at the bottom
    count = count + 1
  
#filename of each figure
result_filename = pig+"_Shannon Entropy Plot"
# result_path = os.path.join(result_folder_path, result_filename) #changed this to below line as it adds a reverse slash in windows
result_path = result_folder_path +  '/' + result_filename
result_path = result_path + "_VFgroups.png"
plt.savefig(result_path)