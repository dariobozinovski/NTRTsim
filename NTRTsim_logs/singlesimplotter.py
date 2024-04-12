
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
num_actuated_cables = 3  # The same data format as springs, but we'll exclude them from energy calculation


#which graph do I want
CMtoHeight=1
TotEneStor=1
springStackPlot=1
extensionRate=1


#num_rods*data_per_rod+
# Definire i percorsi delle directory
directory_path = "/home/dario/NTRTsim_logs/to_plot"
directory_path_save = "/home/dario/NTRTsim_logs/plots"

# Creare le directory se non esistono
if not os.path.exists(directory_path):
    os.makedirs(directory_path)
if not os.path.exists(directory_path_save):
    os.makedirs(directory_path_save)

# Ottenere un elenco di tutti i file nella directory, ordinati
all_files = sorted(os.listdir(directory_path))
all_files = [f for f in all_files if os.path.isfile(os.path.join(directory_path, f))]

# Inizializzare il contatore per i nomi dei file
file_counter = 1

for file_name in all_files:
    # Costruire il percorso completo del file originale
    original_file_path = os.path.join(directory_path, file_name)
    
    # Definire il nuovo nome del file e la nuova directory per i plot
    new_file_name = f"sim{file_counter}"
    new_file_path = os.path.join(directory_path, new_file_name + ".txt")
    new_plots_directory_path = os.path.join(directory_path_save, f"sim{file_counter}_plots")

     # Check if plot directory exists and clean it
    if os.path.exists(new_plots_directory_path):
        rmtree(new_plots_directory_path)
    os.makedirs(new_plots_directory_path)

    # Rename the original file if it's not already renamed
    if not os.path.exists(new_file_path):
        os.rename(original_file_path, new_file_path)

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
    # Display the maximum value in the time column
    #print("Maximum time value:", df2['Time'].max())

    # Assuming 'y_positions' is derived from a specific rod's Y position, let's verify the first rod's Y position data
    # Replace 'Rod1_Y' with the actual column name for the first rod's Y position
    #print("Sample Y-position data for the first rod:", df.iloc[:, 2].head(10))

   
    # Now, let's plot the y-position of the center of mass for each rod over time
    if(CMtoHeight):

        plt.figure(figsize=(14, 7))
        height=np.zeros(len(df))
        for rod in range(1, num_rods + 1):
            
            height+=df[f'Rod{rod}_Y']/num_rods
            
        plt.plot(df['Time'], height, label='CM Y-Position')

        plt.xlabel('Time')

        plt.ylabel('Y-Position of Center of Mass')

        plt.title('Y-Position of the Center of Mass Over Time for Each Rod')
        print(new_file_name+"y_position_vs_time.png")
        plot1_path = os.path.join(new_plots_directory_path, "y_position_vs_time.png")
        plt.savefig(plot1_path)
        plt.close()


    # For the energy stored in springs, assuming spring constant k=1 for simplicity

    if(TotEneStor):
        energy_stored = np.zeros(len(df))

        for spring in range(1, total_spring_columns + 1):

            extension = df[f'Spring{spring}_CurrentLength'] - df[f'Spring{spring}_RestLength']

            extension[extension < 0] = 0  # Only consider extension, not compression

            energy_stored += 0.5 * (extension ** 2)  # Assuming k=1

        # Plot the energy stored in springs over time
        plt.figure(figsize=(14, 7))
        plt.plot(df['Time'], energy_stored, label='Energy Stored in Springs', color='red')
        plt.xlabel('Time')
        plt.ylabel('Energy Stored in Springs')
        plt.title('Energy Stored in Springs Over Time')
        plt.legend()
        plot2_path = os.path.join(new_plots_directory_path,"Energy_Stored_in_Springs_Over_Time.png")
        plt.savefig(plot2_path)
        plt.close()


    #spring extension rates

    if(extensionRate):
        plt.figure(figsize=(20, 10))  # Larger figure size

        line_styles = ['-', '--', '-.', ':']  # Different line styles
        colors = plt.cm.viridis(np.linspace(0, 1, total_spring_columns))  # A colormap for distinct colors

        for spring, (style, color) in zip(range(1, total_spring_columns + 1), zip(cycle(line_styles), colors)):
            extension = df[f'Spring{spring}_CurrentLength'] / df[f'Spring{spring}_RestLength']
            plt.plot(df['Time'], extension, linestyle=style, color=color, alpha=0.7, label=f'Spring {spring}')  # Use of transparency

        plt.title('Spring Extension/Compression Rate Over Time')
        plt.xlabel('Time')
        plt.ylabel('Springs Extension/Compression Rate')

        # Enhance the legend
        leg = plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        for legobj in leg.legend_handles:
            legobj.set_linewidth(2.0)  # Make legend lines thicker

        plt.tight_layout(rect=[0, 0, 0.85, 1])  # Adjust layout to make room for the legend
        plot3_path = os.path.join(new_plots_directory_path,"Spring_Extension_Compression_Rate_Over_Time.png")
        plt.savefig(plot3_path)
        plt.close()

    if(springStackPlot):
        #graph stackplot spring energies
        energies = []
        for spring in range(1, total_spring_columns + 1):
            extension = df[f'Spring{spring}_CurrentLength'] - df[f'Spring{spring}_RestLength']
            extension[extension < 0] = 0  # Ignora la compressione
            energy = 0.5 * (extension ** 2)  # E = 1/2 kx^2, assumendo k=1
            energies.append(energy)

        # Convertire l'elenco delle energie in un DataFrame per facilitare il plot
        energy_df = pd.DataFrame(energies).T
        # Rinominare le colonne per chiarezza
        energy_df.columns = [f'Spring {i+1} Energy' for i in range(total_spring_columns)]

        # Creare il grafico area in pila
        plt.figure(figsize=(14, 7))
        plt.stackplot(df['Time'], energy_df.T, labels=energy_df.columns, alpha=0.8)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.xlabel('Time')
        plt.ylabel('Energy Stored in Each Spring')
        plt.title('Energy Stored in Springs Over Time (Stacked Area Plot)')

        plt.tight_layout(rect=[0, 0, 0.75, 1])  # Ajuste per fare spazio alla legenda

        # Salvare il grafico
        plot_path4 = os.path.join(new_plots_directory_path,"stacked_energy_plot.png")
        plt.savefig(plot_path4)
        plt.close()
        

    # Incrementare il contatore per il prossimo file
    file_counter += 1

print(f"Processo completato per {file_counter - 1} file.")







