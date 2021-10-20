"""
Updated by Nil
Date: October 18,2021       GitHub name: nzgurel         Email: ngurel@mednet.ucla.edu


-added color groups ccording to VF (crimson) vs. non-VF (blue)
-increased some fontsizes
-plots are here: https://drive.google.com/drive/folders/1yCGGI6OvJ4hyglP2EC7dG5EdLt87UA7P?usp=sharing

............
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
measure = "rate"

#cofluctuation threshold: 0p6, 0p75, 0p9 (6, 75, 9)
cofluctuation = "9"

#path to data folder
data_folder_path = 'C:/Users/ngurel/Documents/Renal_Study/Results_RenalAnimals'

#path to result folder
result_folder_path = 'C:/Users/ngurel/Documents/Renal_Study/plotCofluctuation'

# In[ ]:
    
# Get animal filenames
filenames = os.listdir(data_folder_path)
filenames = [f for f in filenames if (f.startswith("pig"))] #get only the filenames that starts with pig
#sort and print the pig filenames
filenames = sorted(filenames)
print(filenames) 

VF_animals_yuichi =    ['pig10153RenalAbl','pig10648','pig199923RenalAbl','pig199929','pig8343','pig9640']
color_VF = 'hotpink'
color_nonVF = 'royalblue'

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
    # current_animal = current_path.split("pig")[1] #obtain just the animal name without the "pig"
    current_animal = filename
    # #3 groups 
    ########################################## UNCOMMENT IF NECESSARY #######################################################
    # if current_animal == "199929" or current_animal == "199924": #control animals
    #     current_color = 'black'
    # elif current_animal == "8343" or current_animal =="199923RenalAbl" or current_animal =="9640" or current_animal =="10153RenalAbl" or current_animal =="8342": #RA ablation
    #     current_color = 'royalblue'
    # else: #ARG ablation
    #     current_color = 'salmon'
      ########################################## UNCOMMENT IF NECESSARY #######################################################

    # detect VF animals
    if current_animal in VF_animals_yuichi:
    # if current_animal in VF_animals_nil:
        # print("current animal is VF")
        color_array = color_VF
    else:
        color_array = color_nonVF
        
    # #is animal VF?
    # if current_animal == "199924":
    #     VF = 1 #yes, in VF
    #     VF_time = 26952
    # elif current_animal == "8343":
    #     VF = 1
    #     VF_time = 30562
    # elif current_animal == "199923RenalAbl": 
    #     VF = 1
    #     VF_time = 30159
    # elif current_animal == "9640": 
    #     VF = 1
    #     VF_time = 23641
    # elif current_animal == "10648":
    #     VF = 1 
    #     VF_time = 32976
    # else:
    #     VF = 0 #not in VF
        
    # if VF == 1:
    #     current_color = 'crimson'
    # else:
    #     current_color = 'royalblue'
        
        
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
    ax[count].plot(time, stats, '--', color = color_array)
    # ax.tick_params(axis = "x", labelsize=3)
    # if the animal is in VF then plot the vertical line at the timestamp
    # if VF == 1:
    #     ax[count].axvline(x = VF_time, linewidth = 5, color = 'green' )
    ax[count].spines["top"].set_visible(False)  
    ax[count].spines["right"].set_visible(False)  
    ax[count].spines["bottom"].set_visible(False)  
    # remove string from current animal name
    current_animal_num = ''.join(i for i in current_animal if i.isdigit())
    ax[count].set_ylabel(current_animal_num, fontsize = 23)
    ax[count].set_xlabel('Protocol Time (seconds)', fontsize = 25)  
    count = count + 1
  
#filename of each figure
result_filename = "cofluctuation" + "Spike" + measure + "0p" + cofluctuation
# result_path = os.path.join(result_folder_path, result_filename) #changed this to below line as it adds a reverse slash in windows
result_path = result_folder_path +  '/' + result_filename
result_path = result_path + "_VFgroups.png"
plt.savefig(result_path)
    