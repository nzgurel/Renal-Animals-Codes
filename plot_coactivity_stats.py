
# -*- coding: utf-8 -*-
"""
Created by Diana Ly
Date: October 13,2021       GitHub name: lydiana90         Email: lydiana@ucla.edu

Cofluctuation plotting code
-This code reads coact_stats.csv from each animal’s directory and plots the cofluctuation time series at each threshold and mean/STD.
-Created plots are in this google drive link: https://drive.google.com/drive/folders/1MHeR1wLAhP6u5pVfXbGz1_8t7SHgskIA?usp=sharing
- red plots are RA ablation animals, grey are control animals and blue are ARG ablation

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

#rate or std
measure = "std"

#cofluctuation threshold: 0p6, 0p75, 0p9 (6, 75, 9)
cofluctuation = "9"

#path to data folder
data_folder_path = "//Users/dianaly/Desktop/Lab/Python/Data&Results for Coactivity/Results_RenalAnimals/"

#path to result folder
result_folder_path = "/Users/dianaly/Desktop/Lab/Python/Data&Results for Coactivity/newResults/"

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

#the following is for pig7444 who is missing rate 0p9
#fig, ax = plt.subplots(figsize = (50,20), nrows = len(filenames)-1, ncols = 1) 

count = 0
for filename in filenames:
    # if filename == 'pig7444':  #this pig was missing a rate 0p9 so I omitted it from the plot
    #     continue
    
    current_path = data_folder_path + '/' + filename
    # print(current_path)
    current_animal = current_path.split("pig")[1] #obtain just the animal name without the "pig"
    
    if current_animal == "199929" or current_animal == "199924": #control animals
        current_color = 'slategrey'
    elif current_animal == "8343" or current_animal =="199923RenalAbl" or current_animal =="9640" or current_animal =="10153RenalAbl" or current_animal =="8342": #RA ablation
        current_color = 'crimson'
    else: #ARG ablation
        current_color = 'steelblue'
        
        
    #is animal VF?
    if current_animal == "199924":
        VF = 1 #yes, in VF
        VF_time = 26952
    elif current_animal == "8343":
        VF = 1
        VF_time = 30562
    elif current_animal == "199923RenalAbl": 
        VF = 1
        VF_time = 30159
    elif current_animal == "9640": 
        VF = 1
        VF_time = 23641
    elif current_animal == "10648":
        VF = 1 
        VF_time = 32976
    else:
        VF = 0 #not in VF
        
    

        
    #target measurement
    measurement_folder_name = "Spike" + measure + "Coact_output_1min_20minbuff_0p" + cofluctuation
    # print(measurement_folder_name)    
    
    measurement_folder_path = current_path + '/' + measurement_folder_name
    print(measurement_folder_path) 
    
    coactivity_stats_filepath = measurement_folder_path + '/' + "coactivity_stats.csv"
    
    df = pd.read_csv(coactivity_stats_filepath)  
    
    time = df['time']
    stats = df['coactivity_stat']    
    
    #plot the graphs for each animal
    ax[count].plot(time, stats, '--', color = current_color)
    # ax.tick_params(axis = "x", labelsize=3)
    #if the animal is in VF then plot the vertical line at the timestamp
    if VF == 1:
        ax[count].axvline(x = VF_time, linewidth = 5, color = 'green' )
    ax[count].spines["top"].set_visible(False)  
    ax[count].spines["right"].set_visible(False)  
    ax[count].spines["bottom"].set_visible(False)  
    ax[count].set_ylabel(current_animal, fontsize = 5)
    ax[count].set_xlabel('Time (seconds)')  
    count = count + 1
  
#filename of each figure
result_filename = "cofluctuation" + "Spike" + measure + "0p" + cofluctuation
result_path = os.path.join(result_folder_path, result_filename)
result_path = result_path + ".pdf"
plt.savefig(result_path)
    
    

