
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from itertools import cycle
from shutil import rmtree
import plotly.express as px
import plotly.graph_objects as go

# Constants based on the structure described
num_rods = 6
data_per_rod = 7  # XYZ position, Euler angles, mass
data_per_spring = 3  # RestLength, CurrentLength, Tension
num_actuated_cables = 3  # The same data format as springs
extension=1
num_comp=0
num_ext=0


#physical parameters
k=400

#which graph do I want
CMtoHeight=1
TotEneStor=0
springStackPlot=0
extensionRate=0
actuator_tension_plotter=0
springTension=0
actuators_extensionrate=0
forceoverextension=0
#num_rods*data_per_rod+
# Definire i percorsi delle directory

if(extension):
    num_comp=num_rods
    num_ext=num_rods*2

directory_path = "/home/ubuntu/NTRTsim/NTRTsim_logs/to_plot"
directory_path_save = "/home/ubuntu/NTRTsim/NTRTsim_logs/plots"

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
    # Definire il nuovo nome del file e la nuova directory per i plot
    new_file_name = f"sim{file_counter}.csv"
    new_file_path = os.path.join(directory_path, new_file_name)
    new_plots_directory_path = os.path.join(directory_path_save, f"sim{file_counter}_plots")
    
    # Rinomina il file originale nel nuovo percorso con il nome disponibile
    os.rename(os.path.join(directory_path, file_name), new_file_path)

    # Create a directory for plots associated with the simulation in the plots directory
    if not os.path.exists(new_plots_directory_path):
        os.makedirs(new_plots_directory_path)
    
    

    #analisi dati
        

    df = pd.read_csv(new_file_path, skiprows=1)

    # Total columns per rod and spring
    total_rod_columns = num_rods * data_per_rod
    total_actuateted_columns=num_actuated_cables*data_per_spring
    total_extension_columns=data_per_rod*num_ext
    total_spring_columns = (len(df.columns)- total_rod_columns-total_actuateted_columns-total_extension_columns-1)//data_per_spring
    
    

    # Re-read the file with manual column names

    

    
    #remove first to seconds
    #df=df.iloc[100:].reset_index(drop=True)
    # Display the maximum value in the time column
    

    # Assuming 'y_positions' is derived from a specific rod's Y position, let's verify the first rod's Y position data
    # Replace 'Rod1_Y' with the actual column name for the first rod's Y position
    #print("Sample Y-position data for the first rod:", df.iloc[:, 2].head(10))

   
    # Now, let's plot the y-position of the center of mass for each rod over time
    if(CMtoHeight):

        plt.figure(figsize=(14, 7))
        height=np.zeros(len(df))
        
        for col in [col for col in df.columns if 'prism_rod' in col and col.endswith('.Y')]:
            
            height+=df[col]*0.1/num_rods
            
        plt.plot(df['time'], height, label='CM Y-Position')
        plt.grid()
        plt.xlabel('Time (s)', fontsize=16)
        plt.xticks(fontsize=15)  
        plt.yticks(fontsize=15) 
        plt.ylabel('Y-Position of Center of  m', fontsize=16)

        plt.title('Y-Position of the Center of Mass Over Time', fontsize=24)
        print(new_file_name+"y_position_vs_time.png")
        plot1_path = os.path.join(new_plots_directory_path, "y_position_vs_time.png")
        plt.savefig(plot1_path)
        plt.close()

        fig = go.Figure()

        # Adding the line plot
        fig.add_trace(go.Scatter(x=df['time'], y=height, mode='lines+markers', name='Y-Position of the Center of Mass Over Time',
                                line=dict(color='red'), hoverinfo='x+y'))

        # Customizing the layout
        fig.update_layout(
            title='Y-Position of the Center of Mass Over Time',
            xaxis_title='Time',
            yaxis_title='Y-Position of Center of Mass',
            legend_title="Legend"
        )

        #you can save the plot to HTML if needed (uncomment the line below)
        plot1_path=os.path.join(new_plots_directory_path,"y_position_vs_time.html")
        
        fig.write_html(plot1_path)

    # For the energy stored in springs, assuming spring constant k

    if(TotEneStor):
        a=len(df)
        energy_stored = np.zeros(len(df))
        curr = [col for col in df.columns if 'springs' in col and col.endswith('.CurrLen')]
        rest= [col for col in df.columns if 'springs' in col and col.endswith('.RestLen')]
        for i,curr_col in enumerate(curr):
            rest_col = rest[i]
            # Calculate the extension
            extension = df[curr_col] - df[rest_col]
            energy_stored = 0.5 * (extension *0.1** 2)*k  # E = 1/2 kx^2, assuming k
            


        #Plot the energy stored in springs over time
        plt.figure(figsize=(14, 7))
        plt.plot(df['time'], energy_stored, label='Energy Stored in Springs', color='red')
        plt.xlabel('Time (s)',fontsize=16)
        plt.ylabel('Energy Stored in Springs (J)',fontsize=16)
        plt.title('Energy Stored in Springs Over Time',fontsize=24)
        plt.grid()
        plt.legend()
        plot2_path = os.path.join(new_plots_directory_path,"Energy_Stored_in_Springs_Over_Time.png")
        plt.savefig(plot2_path)
        plt.close()
        
        fig = go.Figure()

        # Adding the line plot
        fig.add_trace(go.Scatter(x=df['time'], y=energy_stored, mode='lines+markers', name='Energy Stored in Springs',
                                line=dict(color='red'), hoverinfo='x+y'))

        # Customizing the layout
        fig.update_layout(
            title='Energy Stored in Springs Over Time',
            xaxis_title='Time',
            yaxis_title='Energy Stored in Springs',
            legend_title="Legend"
        )

        #you can save the plot to HTML if needed (uncomment the line below)
        plot2_path=os.path.join(new_plots_directory_path,"Energy_Stored_in_Springs_Over_Time.html")
        
        fig.write_html(plot2_path)


    #spring extension rates

    if(extensionRate):
        plt.figure(figsize=(20, 10))  # Larger figure size

        line_styles = ['-', '--', '-.', ':']  # Different line styles
        colors = plt.cm.viridis(np.linspace(0, 1, total_spring_columns))  # A colormap for distinct colors
        curr = [col for col in df.columns if 'springs' in col and col.endswith('.CurrLen')]
        rest= [col for col in df.columns if 'springs' in col and col.endswith('.RestLen')]
        extension = []
        for i,curr_col in enumerate(curr):
            rest_col = rest[i]
            # Calculate the extension
            extension.append(df[curr_col] - df[rest_col])
        for spring, (style, color) in zip(range(1, total_spring_columns+1), zip(cycle(line_styles), colors)):
            plt.plot(df['time'], extension[spring-1], linestyle=style, color=color, alpha=0.7, label=f'Spring {spring}')  # Use of transparency

        plt.title('Spring Extension/Compression Rate Over Time',fontsize=24)
        plt.xlabel('Time (s)',fontsize=20)
        plt.ylabel('Springs Extension/Compression Rate (Current Length/Rest Length)',fontsize=20)
        plt.grid()
        plt.xticks(fontsize=15)  
        plt.yticks(fontsize=15) 
        plt.legend(fontsize=15) 
        # Enhance the legend
        leg = plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        for legobj in leg.legend_handles:
            legobj.set_linewidth(2.0)  # Make legend lines thicker

        plt.tight_layout(rect=[0, 0, 0.85, 1])  # Adjust layout to make room for the legend
        plot3_path = os.path.join(new_plots_directory_path,"Spring_Extension_Compression_Rate_Over_Time.png")
        plt.savefig(plot3_path)
        plt.close()



    #graph stackplot spring energies
    if(springStackPlot):
        
        energies = []
        
        curr = [col for col in df.columns if 'springs' in col and col.endswith('.CurrLen')]
        rest= [col for col in df.columns if 'springs' in col and col.endswith('.RestLen')]
        for i,curr_col in enumerate(curr):
            rest_col = rest[i]
            # Calculate the extension
            extension = df[curr_col] - df[rest_col]
            extension[extension < 0] = 0  # Ignora la compressione
            energy = 0.5 * (extension *0.1** 2)*k  # E = 1/2 kx^2, assumendo k
            energies.append(energy)

        # Convertire l'elenco delle energie in un DataFrame per facilitare il plot
        energy_df = pd.DataFrame(energies).T
        # Rinominare le colonne per chiarezza
        energy_df.columns = [f'Spring {i+1} Energy' for i in range(total_spring_columns)]

        # Creare il grafico area in pila
        plt.figure(figsize=(14, 7))
        plt.stackplot(df['time'], energy_df.T, labels=energy_df.columns, alpha=0.8)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.grid()
        plt.xlabel('Time (s)')
        plt.ylabel('Energy Stored in Each Spring (J)')
        plt.title('Energy Stored in Springs Over Time (Stacked Area Plot)')

        plt.tight_layout(rect=[0, 0, 0.75, 1])  # Ajuste per fare spazio alla legenda

        # Salvare il grafico
        plot_path4 = os.path.join(new_plots_directory_path,"stacked_energy_plot.png")
        plt.savefig(plot_path4)
        plt.close()
    
    
    #actuated cable tension
    if(actuator_tension_plotter):
        plt.figure(figsize=(14, 7))

        # Plotting tension for each actuated cable
        for cable in [col for col in df.columns if 'activated_cable' in col and col.endswith('.Tension')]:
            plt.plot(df['time'], df[cable]*0.1, label=f'{cable} Tension')
        
        # Customizing the plot
        plt.xlabel('Time (s)')
        plt.ylabel('Tension (N)')
        plt.title('Tension in Actuated Cables Over Time')
        plt.legend()
        plt.grid()

        # Save the plot
        plot_path = os.path.join(new_plots_directory_path, "actuated_cable_tensions_vs_time.png")
        plt.savefig(plot_path)
        plt.close()
    if(actuators_extensionrate):
        plt.figure(figsize=(14, 7))
        curr = [col for col in df.columns if 'activated_cable' in col and col.endswith('.CurrLen')]
        rest= [col for col in df.columns if 'activated_cable' in col and col.endswith('.RestLen')]
        for i,curr_col in enumerate(curr):
            rest_col = rest[i]
            # Calculate the extension
            extension_rate= df[curr_col]/df[rest_col]
            plt.plot(df['time'], df[rest_col]*0.1, label=f'Actuated Cable {i+1} Extension Rate')
            plt.plot(df['time'], extension_rate, label=f'Actuated Cable {i+1} Extension Rate')
        # Plotting tension for each actuated cable
        # Customizing the plot
        plt.xlabel('Time')
        plt.ylabel('restlenght')
        plt.title('Restlenght in Actuated Cables Over Time')
        plt.legend()
        plt.grid()

        # Save the plot
        plot_path = os.path.join(new_plots_directory_path, "actuated_cable_restlenght_vs_time.png")
        plt.savefig(plot_path)
        plt.close()
    
    if(springTension):
        tensions = []
        for spring_tension in [spring for spring in df.columns if 'springs' in spring and spring.endswith('.Tension')]:
            tensions.append(df[spring_tension])

        # Convertire l'elenco delle energie in un DataFrame per facilitare il plot
        Tensions_df = pd.DataFrame(tensions).T
        # Rinominare le colonne per chiarezza
        Tensions_df.columns = [f'Spring {i+1} Tension' for i in range(Tensions_df.shape[1])]

        # Creare il grafico area in pila
        plt.figure(figsize=(14, 7))
        plt.stackplot(df['time'], Tensions_df.T, labels=Tensions_df.columns, alpha=0.8)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.xlabel('Time')
        plt.ylabel('Tension in Each Spring')
        plt.title('Tension in Springs Over Time (Stacked Area Plot)')
        plt.grid()

        plt.tight_layout(rect=[0, 0, 0.75, 1])  # Ajuste per fare spazio alla legenda

        # Salvare il grafico
        plot_path5 = os.path.join(new_plots_directory_path,"Tensionssprings.png")
        plt.savefig(plot_path5)
        plt.close()
    # Initialize a list to hold work calculations for each cable
    
    work_done = []
    tot_work=0
    for cable_tens in [cable for cable in df.columns if 'activated_cable' in cable and cable.endswith('.Tension')]:
        tensions = df[cable_tens]*0.1  
        lengths = df[cable_tens.replace('Tension', 'CurrLen')]*0.1
        # Calculate the work done using the trapezoidal rule
        work = np.trapz(tensions, x=lengths)  # `x` denotes the values of length over which tension is applied
        
        # Store the calculated work
        work_done.append(work)
        
        tot_work=np.sum(work_done)
        print(f"Work done by {cable_tens} in sim{file_counter}: {work:.2f} units")
    print("tot work is:",tot_work)
    
    #plotting force over extension during compression
    if(forceoverextension):

        plt.figure(figsize=(14, 7))
        #first value of the rest lengths of actuated cables
        Rest_Lengths=[col for col in df.columns if 'activated_cable' in col and col.endswith('.RestLen')]
        #only first value of every column   
       
        
        for i,cable in enumerate(Rest_Lengths):
            plt.plot((df[cable.replace('RestLen', 'CurrLen')]-df[cable].iloc[0])*0.1,df[cable.replace('RestLen', 'Tension')]*0.1, label=f'Tension vs Extension {cable}')
        
        plt.grid()
        plt.xlabel('extension in m', fontsize=16)
        plt.xticks(fontsize=15)  
        plt.yticks(fontsize=15) 
        plt.ylabel('Force in atuator in N', fontsize=16)
        plt.legend()
        plt.title('force over extenasion of actuated cables', fontsize=24)
        print(new_file_name+"force_over_extension.png")
        plot1_path = os.path.join(new_plots_directory_path, "force_over_extension.png")
        plt.savefig(plot1_path)
        plt.close()

    # Incrementare il contatore per il prossimo file
    file_counter += 1
    


print(f"Processo completato per {file_counter - 1} file.")







