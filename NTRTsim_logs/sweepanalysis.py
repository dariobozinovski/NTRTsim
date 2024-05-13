import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
from itertools import cycle
from shutil import rmtree
import plotly.graph_objects as go
 #plots
CMtoHeight=1
jump_distance=1
landingspots=1

#defining the directory path
directory_path = "/home/ubuntu/NTRTsim/NTRTsim_logs/plotting"
directory_path_save = "/home/ubuntu/NTRTsim/NTRTsim_logs/plots"
if not os.path.exists(directory_path):
    os.makedirs(directory_path)
if not os.path.exists(directory_path_save):
    os.makedirs(directory_path_save)
new_plots_directory_path = os.path.join(directory_path_save, "sweep")

# create the directory if it does not exist
if not os.path.exists(new_plots_directory_path):
    os.makedirs(new_plots_directory_path)


# Function to extract the number from the file name
def extract_number(filename):
    s = re.findall(r'\d+', filename)
    return int(s[0]) if s else -1
all_files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
all_files_sorted = sorted(all_files, key=extract_number)
file_counter = 1
#data to plot
#CMtoHeight
max_y_positions = []
#jump_distance
CM_y_max = []
CM_y_min = []
jump_dist=[]
#landingspots
CM_xd_jump = []
CM_zd_jump = []

Rod_mid_x=[]
Rod_mid_z=[]


#num_of_sim is an array that contains starting from startk with step stepk the number of the simulation (adjust to sweep that has ben made)
startk=1
stepk=-0.01
num_of_sim = np.arange(startk, startk + stepk * (len(all_files_sorted) - 0.99), stepk)
num_of_sim=np.round(num_of_sim,2)



# Loop through all files and extract the data
for i,file_name in enumerate(all_files_sorted):
    # Read the file
    file_path = os.path.join(directory_path, file_name)
    df = pd.read_csv(file_path, skiprows=1)
    print("file number: ",i+1,"file_name",file_name)
    #remove first to seconds
    sim_timestep=df['time'].iloc[-1]-df['time'].iloc[-2]
    df=df.iloc[int(2/sim_timestep):].reset_index(drop=True)
    
    #CMy
    if(CMtoHeight):
        height=np.zeros(len(df))
        y = [col for col in df.columns if 'prism_rod' in col and col.endswith('.Y')]
        height = df[y].mean(axis=1) * 0.1
        

        max_height=height.max()
        
        max_y_positions.append(max_height)
    #Jump distance
    #plot in y: difference in x and z (use pythagorean theorem)position of the center of mass between the two moments when y is maximum and minimum. in x axis the number of the simulation 
    
    if(jump_distance or landingspots):
        # Define columns for X, Y, Z coordinates
        x = [col for col in df.columns if 'prism_rod' in col and col.endswith('.X')]
        y = [col for col in df.columns if 'prism_rod' in col and col.endswith('.Y')]
        z = [col for col in df.columns if 'prism_rod' in col and col.endswith('.Z')]
        
        # Calculate the average position of all rods
        CM_x = df[x].mean(axis=1) * 0.1 
        CM_y = df[y].mean(axis=1) * 0.1
        CM_z = df[z].mean(axis=1) * 0.1
        
        #find the max and min y position
        max_y_index=CM_y.idxmax()
        min_y_index=CM_y.idxmin()
        
        #find the x and z position of the center of mass in the two moments
        CM_x_maxy=CM_x[max_y_index]
        CM_x_miny=CM_x[min_y_index]
        CM_z_maxy=CM_z[max_y_index]    
        CM_z_miny=CM_z[min_y_index]

        #calculate the distance
        distance=np.sqrt((CM_x_maxy-CM_x_miny)**2+(CM_z_maxy-CM_z_miny)**2)*2
        #append the values
        jump_dist.append(distance)
        CM_y_max.append(CM_y[max_y_index])
        CM_y_min.append(CM_y[min_y_index])
        CM_xd_jump.append(CM_x_maxy-CM_x_miny)
        CM_zd_jump.append(CM_z_maxy-CM_z_miny)

        
        #find end positions of rods in contact with ground
        rod_length=0.5
        #find the rods that are in contact with the ground
        y_rod_xmin=df[y].iloc[min_y_index-800]
        # print("y_rod",y_rod_xmin)
        y_rod_xmin=y_rod_xmin.sort_values().iloc[:3]
        # print("y_rod",y_rod_xmin)
        rod_indexes=y_rod_xmin.index
        # print("rod_indexes",rod_indexes)
        rod_indexes=[re.sub(r'\.Y', '', rod) for rod in rod_indexes]
        #mid position of rods on ground
        X_mid_rod=[]
        Z_mid_rod=[]
        for rod in rod_indexes:
            X_mid_rod.append(df[rod+'.X'].iloc[min_y_index]*0.1-CM_x_miny)
            Z_mid_rod.append(df[rod+'.Z'].iloc[min_y_index]*0.1-CM_z_miny)
        Rod_mid_x.append(X_mid_rod)
        Rod_mid_z.append(Z_mid_rod)

    

if(CMtoHeight):    
    plt.figure(figsize=(14, 7))
    
    plt.plot(num_of_sim, max_y_positions, label='CM max Y-Position')
    plt.grid(True) 
    plt.xlabel('delay (s)')

    plt.ylabel('Ymax-Position of Center of Mass (m)')

    plt.title('Ymax-Position of the Center of Mass Over sim number')
    
    plot1_path = os.path.join(new_plots_directory_path, "yCMmax_.png")
    plt.savefig(plot1_path)
    plt.close()
if(jump_distance):
    

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=num_of_sim,
        y=jump_dist,
        mode='markers+lines',
        name='Jump Distance',
        
        #hover info: Jump Distance: %{y} m, Jump Delay: %{x} s, Max Y Position: %{customdata[0]} m, Min Y Position: %{customdata[1]} m, Max X Position: %{customdata[2]} m, Max Z Position: %{customdata[3]} m',
        text=[f'jump_dist: {jd:.2f}, delay: {dl:.2f}, max Y; {mY:.2f}' for jd, dl, mY in zip(jump_dist, num_of_sim, CM_y_max)],
        hoverinfo='text'   
    ))


    fig.update_layout(
        title='jump_dist Over Jumpdelay',
        xaxis_title='JumpDelay (s)',
        yaxis_title='Jump Distance (m)',
        hovermode='closest'
    )

    
    plot2_path = os.path.join(new_plots_directory_path, "y_positions.html")
    fig.write_html(plot2_path)
    
if(landingspots):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=CM_xd_jump,
        y=CM_zd_jump,
        mode='lines+markers',
        name='Jump positions',
        
        #hover info: Jump Distance: %{y} m, Jump Delay: %{x} s, Max Y Position: %{customdata[0]} m, Min Y Position: %{customdata[1]} m, Max X Position: %{customdata[2]} m, Max Z Position: %{customdata[3]} m',
        text=[f'x dist {xd:.2f}, z dist {zd:.2f}, jump_dist: {jd:.2f}, delay: {dl:.2f}, max Y; {mY:.2f}' for xd,zd,jd, dl, mY in zip(CM_xd_jump,CM_zd_jump,jump_dist, num_of_sim, CM_y_max)],
        hoverinfo='text'   
    ))
    #create separated lines for each rod
    
    colors = cycle(['blue', 'green', 'red'])
    for i in range(len(Rod_mid_x)):
        
       
            
            fig.add_trace(go.Scatter(
                x=Rod_mid_x[i],
                y=Rod_mid_z[i],
                mode='markers',
               name='Rod',
                line=dict(color=next(colors), width=2),
               hoverinfo='skip'
            ))

    fig.update_layout(
        title='landing spots',
        xaxis_title='x (m)',
        yaxis_title='z (m)',
        hovermode='closest',
        xaxis=dict(scaleanchor="y", scaleratio=1),
        yaxis=dict(scaleanchor="x", scaleratio=1)
    )

    fig.show()
    plot2_path = os.path.join(new_plots_directory_path, "landingspots.html")
    fig.write_html(plot2_path)