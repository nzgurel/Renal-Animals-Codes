# -*- coding: utf-8 -*-
"""
Created by Sharon Tam
Date: 10/01/2021
Github Name:
Email: sh5450@ucla.edu

Bootstrapping Event Rates and Coactivity Stats Plots

-This code reads coactivity_stats.csv from each animal’s directory and performs bootstrapping on all threshold combinations based on event rates.
-The data from coactivity_stats.csv is also plotted for each measure and exceedance threshold.

-Created plots are in this google drive link: https://drive.google.com/drive/folders/1bn4LFA_tB7o8_y_eLIrE0eMCWvCi9bA6?usp=sharing

"""


# In[Import Libraries]: 

from string import ascii_letters
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import os

# In[Functions]:
    

def getResampledStats(time, stats):
    resampled_index = np.random.choice(np.arange(len(time)), len(time))
    #print(resampled_index)
    return np.array(time)[resampled_index], np.array(stats)[resampled_index]

    
def getEventRate(denom, stats,threshold):
    #time - resampled time
    #stats - resample stats with same index as resampled time
    state_array = np.zeros(len(stats))
              
    for i in range(len(stats)):
        if stats[i] > threshold:
            state_array[i] = 1
            
    transition_timestamp = []
    for i in range(len(state_array) - 1):
        if (state_array[i] - state_array[i + 1]) == -1:
            transition_timestamp.append([i + 1])
            
    return len(transition_timestamp) / (denom)

def draw_bs_replicates(denom,time,stats,size,threshold):
    """creates a bootstrap sample, computes replicates and returns replicates array"""
    # Create an empty array to store replicates
    bs_replicates = np.empty(size)
    
    # Create bootstrap replicates as much as size
    for i in range(size):
        # Create a bootstrap sample
        #bs_sample = np.random.choice(data,size=len(data))
        _, bb = getResampledStats(time, stats)
        rate = getEventRate(denom,bb,threshold)
        # Get bootstrap replicate and append to bs_replicates
        bs_replicates[i] = rate
        
    return bs_replicates

# In[Get parameter values]:
    
result_folder_path = 'C:/Users/SmartBox/Desktop/Lab/Results 10_20'

animal_types = ['VF', 'Normal']
color_codes = ['magenta', 'blue']

# Parameter values
state_thr_values = [40, 50, 60, 70, 80, 90]
exc_thr_values = ['0p6', '0p75', '0p9']
measurements = ['rate', 'std']

# End of Baseline timestamps 
EndBaseline_VF = [31000, 31000, 31000, 31000, 31000, 31000, 31000]
EndBaseline_Normal = [31000, 31000, 31000, 31000, 31000]
#EndBaseline_Unknown = [20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000]

# VF Time Stamp
VF_times = [30000, 32976, 30159, 26952, 30562, 23641, ]
#pig10153RenalAbl, 10648, 199923RenalAbl, 199924, 8343, 9640, 

total_animals = 11

# In[Bootstrap + coact stats]:

# List for all bootstrapping stats for all animals    
bsstats_all = list()

# Number of replicates : change to 1000
num_bs_replicates = 1

# Confidence Interval Limits
lower = 5
upper = 95

# Create and format figures for coactivity stats
fig_0p6_rate, ax_0p6_rate = plt.subplots(figsize = (44, 30), nrows = total_animals, ncols = 1, squeeze = False)
fig_0p6_rate.suptitle('Cofluctuations (Case:MEAN, threshold: 0.6)', fontsize = 30)
fig_0p6_rate.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.7)

fig_0p6_std, ax_0p6_std = plt.subplots(figsize = (44, 30), nrows = total_animals, ncols = 1, squeeze = False)
fig_0p6_std.suptitle('Cofluctuations (Case:STD, threshold: 0.6)', fontsize = 30)
fig_0p6_std.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.7)

fig_0p75_rate, ax_0p75_rate = plt.subplots(figsize = (44, 30), nrows = total_animals, ncols = 1, squeeze = False)
fig_0p75_rate.suptitle('Cofluctuations (Case:MEAN, threshold: 0.75)', fontsize = 30)
fig_0p75_rate.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.7)

fig_0p75_std, ax_0p75_std = plt.subplots(figsize = (44, 30), nrows = total_animals, ncols = 1, squeeze = False)
fig_0p75_std.suptitle('Cofluctuations (Case:STD, threshold: 0.75)', fontsize = 30)
fig_0p75_std.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.7)

fig_0p9_rate, ax_0p9_rate = plt.subplots(figsize = (44, 30), nrows = total_animals, ncols = 1, squeeze = False)
fig_0p9_rate.suptitle('Cofluctuations (Case:MEAN, threshold: 0.9)', fontsize = 30)
fig_0p9_rate.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.7)

fig_0p9_std, ax_0p9_std = plt.subplots(figsize = (44, 30), nrows = total_animals, ncols = 1, squeeze = False)
fig_0p9_std.suptitle('Cofluctuations (Case:STD, threshold: 0.9)', fontsize = 30)
fig_0p9_std.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.7)


coact_figs = [fig_0p6_rate, fig_0p6_std, fig_0p75_rate, fig_0p75_std, fig_0p9_rate, fig_0p9_std]
coact_axes = [ax_0p6_rate, ax_0p6_std, ax_0p75_rate, ax_0p75_std, ax_0p9_rate, ax_0p9_std]
coact_fig_names = ["fig_0p6_rate", "fig_0p6_std", "fig_0p75_rate", "fig_0p75_std", "fig_0p9_rate", "fig_0p9_std"]

animal_count = 0
vf_animal_count = 0
for animal_type, type_color in zip(animal_types, color_codes):
    
    # Get animal names
    animal_folder_path = 'D:/Renal Study/Results_RenalAnimals/' + animal_type + "Animals"
    animal_names = os.listdir(animal_folder_path)
    animal_names = sorted(animal_names)
    print(animal_names)
    
    if (animal_type == "VF"):
        EndBaseline = EndBaseline_VF
    else:
        EndBaseline = EndBaseline_Normal
        
    # Loop through each animal
    count = 0
    for animal in animal_names:
    
        current_path = animal_folder_path + "/" + animal
        
        
        # Create coactivity stat figure for 11 plots
        #coact_stat_fig, coact_stat_ax = plt.subplots(figsize = (22,15), nrows = 6, ncols = 1, squeeze = False)
        #coact_stat_fig.suptitle(animal + ' Coactivity Stats', fontsize = 30)
        #coact_stat_fig.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.7)
        #coact_stat_count = 0
      
        for measure in measurements:
        
            for exc in exc_thr_values:
                
                coact_stats_path = current_path + "/Spike" + measure + "coact_output_1min_20minbuff_" + exc + "/coactivity_stats.csv"
                    #print(coact_stats_path + str(state))
     
                if os.path.exists(coact_stats_path):
                    
                    # Read in data
                    df = pd.read_csv(coact_stats_path)
                    time = df['time']
                    stats = df['coactivity_stat']
                    
                    del df
                    
                    # Plot coactivity stats (for each animal)
                    #ax1 = coact_stat_ax[coact_stat_count][0]
                    #ax1.plot(time, stats)
                    #ax1.set_title(animal + "_" + measure + "_" + event + "_coact_stats")
                    #plt.show()
                    
                    #coact_stat_count = coact_stat_count + 1
                    
                    # Plot coactivity stats (for each exceedance and measure combination)
                    fig_count = 0
                    for name in coact_fig_names:
                        
                        current_fig = "fig_" + exc + "_" + measure
                        
                        if (current_fig == name):
                            ax1 = coact_axes[fig_count][animal_count][0]
                            ax1.plot(time/3600, stats, color = type_color)
                            ax1.set_xlabel('Experiment time (hours)', fontsize = 12)
                            ax1.set_ylabel(animal + " " + animal_type, fontsize = 12)
                            ax1.tick_params(axis = "x", labelsize=3)
                            ax1.spines["top"].set_visible(False)  
                            ax1.spines["right"].set_visible(False)  
                            ax1.legend()
                            plt.show()
                            
                        fig_count = fig_count + 1
                        
                        if (animal_type == "VF"):
                            ax1.axvline(x = VF_times[vf_animal_count]/3600, ymin = 0, ymax = 1, color = 'black', lw = 5)
                        
                    # Limit time before end of baseline
                    index = time < EndBaseline[count]
                    time = time[index]
                    stats = stats[index]
                    
                    #convert to lists
                    time = time.tolist()
                    stats = stats.tolist()
                    
                    # Bootstrap for every state threshold
                    for state in state_thr_values:
                            
                        if len(stats) > 0:
                            # Draw N bootstrap replicates
                            denom = time[-1] - time[0] #hard coded
                            bs_replicates_values = draw_bs_replicates(denom, time, stats, num_bs_replicates, state)
                    
            
                            # Plot the PDF for bootstrap replicates as histogram & save fig
                            plt.figure(2)
                            plt.hist(bs_replicates_values, bins=30, color = type_color)
                            
                            
                            # Showing the related percentiles
                            plt.axvline(x=np.percentile(bs_replicates_values,[lower]), ymin=0, ymax=1,label='5th percentile',c='y')
                            plt.axvline(x=np.percentile(bs_replicates_values,[upper]), ymin=0, ymax=1,label='95th percentile',c='r')
                            
                            plt.xlabel("Event rate")
                            plt.ylabel("Probability Density Function")
                            plt.title(animal + "_" + measure + "_" + animal_type + "_" + exc + "_" + str(state) + "_BS" + str(num_bs_replicates))
                            plt.legend()
                            
                            # Save histogram
                            bs_savefig_pdf_str= animal + "_PDF_" + measure + "_" + animal_type + "_" + exc + "_" + str(state) + "_BS" + str(num_bs_replicates) + "_EvRate_base.pdf"
                            bs_pdf_folder = result_folder_path + "/" + animal_type + " Results/" + animal + "_bs_plots"
                            
                            # Create folder for each animal
                            if not os.path.exists(bs_pdf_folder):
                                os.makedirs(bs_pdf_folder)
                            
                            bs_pdf_path = bs_pdf_folder + "/" + bs_savefig_pdf_str
                            plt.savefig(bs_pdf_path)    
                            plt.show()
                
                            # Get the bootstrapped stats
                            bs_mean = np.mean(bs_replicates_values)
                            bs_std = np.std(bs_replicates_values)
                            ci = np.percentile(bs_replicates_values,[lower,upper])
                            ci_width = np.diff(ci)
                    
                            # Print stuff
                            #print(animal + " bootstrapped mean: ", bs_mean)
                            #print(animal + " bootstrapped std: ", bs_std)
                            #print(animal + " bootstrapped ci: ", ci)
                            #print(animal + " bootstrapped ci width: ", ci_width)
                            
                            # Complie bootstrapped stats                        
                            bsstats_concat = np.concatenate((np.array([animal]), np.array([measure]), np.array([animal_type]), np.array([exc]), np.array([state]), np.array([bs_mean]), np.array([bs_std]), ci, ci_width))  
                            bsstats_all.append(bsstats_concat)     
                            
                        else:
                            print(current_animal + "has no transition timestamps for threshold = " + str(threshold))
                            bsstats_concat = [999,999,999,999,999]
                            bsstats_all.append(bsstats_concat)
                
        
        # Save coact stats plot for each animal                    
        #coact_savefig_pdf_str= animal + "_PDF_coact_stats_plot.pdf"
        #coact_pdf_path = result_folder_path + "/" + coact_savefig_pdf_str
        #coact_stat_fig.savefig(coact_pdf_path)    
        #plt.show()
        
        count = count + 1
        animal_count = animal_count + 1
        if (animal_type == "VF"):
            vf_animal_count = vf_animal_count + 1
                        
# Save coact stat figures
for figure, name in zip(coact_figs, coact_fig_names):
    savefig_pdf_str = name + "_coactivity_stats.pdf"
    coact_path = result_folder_path + "/" + savefig_pdf_str
    figure.savefig(coact_path)
    plt.show()
    
                        
df_bsstats = pd.DataFrame(bsstats_all)   

# Rename columns
df_bsstats.rename(columns = {0 : 'animal', 1 : 'measure', 2: 'animal_type', 3: 'exceedance', 4: 'state_threshold', 5:'mean', 6:'std', 7:'lower', 8:'upper', 9:'ci_width'}, inplace = True)        

# Reindex column titles
column_titles = ['animal', 'mean', 'std', 'lower','upper','ci_width','state_threshold','exceedance', 'measure', 'animal_type']

df_bsstats = df_bsstats.reindex(columns=column_titles)

# Add details to title
str_csv = "bsstats_RenalAnimals_BS" + str(num_bs_replicates) + "_EvRate_base.csv"                                              

# Save csv to result folder
bs_csv_path = result_folder_path + '/' + str_csv
df_bsstats.to_csv(bs_csv_path, index=False)     
            