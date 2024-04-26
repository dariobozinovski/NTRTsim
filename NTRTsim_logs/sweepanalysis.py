import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
from itertools import cycle
from shutil import rmtree
# Constants based on the structure described
num_rods = 6
data_per_rod = 7  # XYZ position, Euler angles, mass
data_per_spring = 3  # RestLength, CurrentLength, Tension
num_actuated_cables = 4  # The same data format as springs, but we'll exclude them from energy calculation
extension=1
num_comp=0
num_ext=0
if(extension):
    num_comp=num_rods
    num_ext=num_rods*2

CMtoHeight=1
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
def extract_number(filename):
    s = re.findall(r'\d+', filename)
    return int(s[0]) if s else -1
# Ottenere un elenco di tutti i file nella directory, ordinati

all_files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
all_files_sorted = sorted(all_files, key=extract_number)
# Inizializzare il contatore per i nomi dei file
file_counter = 1
#definitions
max_y_positions = []
startk=200
stepk=10
#num_of_sim is an array that contains starting from startk with step stepk the number of the simulation
num_of_sim=np.arange(startk,startk+stepk*len(all_files),stepk)


for i,file_name in enumerate(all_files_sorted):
    # Costruire il percorso completo del file originale
    file_path = os.path.join(directory_path, file_name)
    print(file_name)
    # Definire il nuovo nome del file e la nuova directory per i plot



    # Aggiornare il codice di analisi per utilizzare il nuovo percorso del file
    # e la directory per i plot, poi eseguire l'analisi e salvare i plot nella nuova directory
    # [Inserire qui il codice di analisi, inclusa la generazione e il salvataggio dei grafici nella nuova directory]
    

    #analisi dati
        

    df = pd.read_csv(file_path, skiprows=1)

    # Total columns per rod and spring
    total_rod_columns = num_rods * data_per_rod
    total_actuateted_columns=num_actuated_cables*data_per_spring
    total_compound_columns=data_per_rod*num_comp
    total_extension_columns=data_per_rod*num_ext
    total_spring_columns = (len(df.columns)- total_rod_columns-total_actuateted_columns-total_compound_columns-total_extension_columns-1)//data_per_spring
    
    # Re-read the file with manual column names
    #remove first to seconds
    sim_timestep=df['time'].iloc[-1]-df['time'].iloc[-2]
    
    df=df.iloc[int(2/sim_timestep):].reset_index(drop=True)
    #CMy
    if(CMtoHeight):
        height=np.zeros(len(df))
        for col in [col for col in df.columns if 'prism_rod' in col and col.endswith('.Y')]:
            height+=df[col]*0.1/num_rods
        max_height=height.max()
        print(max_height)
        max_y_positions.append(max_height)


if(CMtoHeight):    
    plt.figure(figsize=(14, 7))
    
    plt.bar(num_of_sim, max_y_positions, label='CM max Y-Position')
    plt.grid(True) 
    plt.xlabel('sim')

    plt.ylabel('Ymax-Position of Center of Mass')

    plt.title('Ymax-Position of the Center of Mass Over sim number')
    
    plot1_path = os.path.join(new_plots_directory_path, "yCMmax_.png")
    plt.savefig(plot1_path)
    plt.close()