import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from itertools import cycle
from shutil import rmtree
# Constants based on the structure described
num_rods = 6
data_per_rod = 7  # XYZ position, Euler angles, mass
data_per_spring = 3  # RestLength, CurrentLength, Tension
num_actuated_cables = 4  # The same data format as springs, but we'll exclude them from energy calculation


#which graph do I want
CMtoHeight=True



# Definire i percorsi delle directory
directory_path = "/home/ubuntu/NTRTsim/NTRTsim_logs/to_plot"
directory_path_save = "/home/ubuntu/NTRTsim/NTRTsim_logs/plots"

# Creare le directory se non esistono
if not os.path.exists(directory_path):
    os.makedirs(directory_path)
if not os.path.exists(directory_path_save):
    os.makedirs(directory_path_save)

new_plots_directory_path = os.path.join(directory_path_save, "sweep")

# Check if plot directory exists and clean it
if os.path.exists(new_plots_directory_path):
    rmtree(new_plots_directory_path)
os.makedirs(new_plots_directory_path)

# Ottenere un elenco di tutti i file nella directory, ordinati
all_files = sorted(os.listdir(directory_path))
all_files = [f for f in all_files if os.path.isfile(os.path.join(directory_path, f))]

# Inizializzare il contatore per i nomi dei file
file_counter = 1

#definitions
max_y_positions = []
num_of_sim=np.arange(len(all_files))

for i,file_name in enumerate(all_files):
    # Costruire il percorso completo del file originale
    original_file_path = os.path.join(directory_path, file_name)
    
    # Definire il nuovo nome del file e la nuova directory per i plot
    new_file_name = f"sim{file_counter}"
    new_file_path =original_file_path 


    # Aggiornare il codice di analisi per utilizzare il nuovo percorso del file
    # e la directory per i plot, poi eseguire l'analisi e salvare i plot nella nuova directory
    # [Inserire qui il codice di analisi, inclusa la generazione e il salvataggio dei grafici nella nuova directory]
    

    #analisi dati
        

    df = pd.read_csv(new_file_path, skiprows=1)

    # Total columns per rod and spring
    total_rod_columns = num_rods * data_per_rod
    total_actuateted_columns=num_actuated_cables*data_per_spring
    total_spring_columns = (len(df.columns)- total_rod_columns-total_actuateted_columns-1)//data_per_spring
    
    column_names = ['Time']

    for rod in range(1, num_rods + 1):

        column_names += [f'Rod{rod}_X', f'Rod{rod}_Y', f'Rod{rod}_Z', f'Rod{rod}_EulerX', f'Rod{rod}_EulerY', f'Rod{rod}_EulerZ',f'Rod{rod}_mass']

    for spring in range(1, total_spring_columns + 1):

        column_names += [f'Spring{spring}_RestLength', f'Spring{spring}_CurrentLength', f'Spring{spring}_Tension']

    for cable in range(1, num_actuated_cables + 1):

        column_names += [f'ActuatedCable{cable}_RestLength', f'ActuatedCable{cable}_CurrentLength', f'ActuatedCable{cable}_Tension']
    column_names += ['to_delete']

    # Re-read the file with manual column names

    df = pd.read_csv(new_file_path, skiprows=2, names=column_names)

    df=df.drop(columns=['to_delete'])

    #remove first to seconds
    df=df.iloc[10:].reset_index(drop=True)

    
    #CMy
    if(CMtoHeight):
        height=np.zeros(len(df))
        for rod in range(1, num_rods + 1):
            height+=df[f'Rod{rod}_Y']/num_rods
        max_height=height.max()
        max_y_positions.append(max_height)
if(CMtoHeight):    
    plt.figure(figsize=(14, 7))
    print(max_y_positions)
    plt.bar(num_of_sim, max_y_positions, label='CM max Y-Position')
    plt.grid(True) 
    plt.xlabel('sim')

    plt.ylabel('Ymax-Position of Center of Mass')

    plt.title('Ymax-Position of the Center of Mass Over sim number')
    print(new_file_name+"ymax.png")
    plot1_path = os.path.join(new_plots_directory_path, "yCMmax_.png")
    plt.savefig(plot1_path)
    plt.close()