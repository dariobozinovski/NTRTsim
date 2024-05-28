import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
from itertools import cycle
from shutil import rmtree
import plotly.graph_objects as go
import plotly.express as px
 #plots
CMtoHeight=0
jump_distance=0
landingspots=0
distancepret=1
#defining the directory path
directory_path = "/home/ubuntu/NTRTsim/NTRTsim_logs/plotting/simmoonpretension/"
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
startk=0.5
stepk=-0.02
num_of_sim = np.arange(startk, startk + stepk * (len(all_files_sorted) - 0.99), stepk)
num_of_sim=np.round(num_of_sim,2)



# Loop through all files and extract the data
for i,file_name in enumerate(all_files_sorted):
    # Read the file
    file_path = os.path.join(directory_path, file_name)
    df = pd.read_csv(file_path, skiprows=1)
    print("file number: ",i+1,"file_name",file_name)
    #remove first to seconds
    sim_timestep=round(df['time'].iloc[-1]-df['time'].iloc[-2],5)
    # df=df.iloc[int(2/sim_timestep):].reset_index(drop=True)
    
    #CMy
    if(CMtoHeight):
        height=np.zeros(len(df))
        y = [col for col in df.columns if 'prism_rod' in col and col.endswith('.Y')]
        height = df[y].mean(axis=1) * 0.1
        

        max_height=height.max()
        
        max_y_positions.append(max_height)
    #Jump distance
    #plot in y: difference in x and z (use pythagorean theorem)position of the center of mass between the two moments when y is maximum and minimum. in x axis the number of the simulation 
    
    if(jump_distance or landingspots or distancepret):
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
        # Find the index of the first decreasing value from the 6th second
        start_index = int(6 / sim_timestep) 
        decreasing_index = start_index + np.argmax(np.diff(CM_y[start_index:]) < 0) + 1
        decreasing_second=decreasing_index*sim_timestep
        #find the x and z position of the center of mass in the two moments
        CM_x_maxy=CM_x[decreasing_index]
        # CM_x_miny=CM_x[min_y_index]
        CM_z_maxy=CM_z[decreasing_index]    
        # CM_z_miny=CM_z[min_y_index]
        
        index_prejump=int((6/sim_timestep)-0.99)
        CM_x_miny=CM_x[index_prejump]
          
        CM_z_miny=CM_z[index_prejump]


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
        y_rod_xmin=df[y].iloc[0]
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
        mode='markers+lines',
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
if distancepret:
    # Generate the parameter values
    jump_extra1_values = []
    jump_extra2_values = []
    jump_extra3_values = []

    for i in range(21):
        jump_extra1 = round(0.5 - 0.025 * i, 2)
        for j in range(21):
            jump_extra2 = round(0.5 - 0.025 * j, 2)
            for k in range(21):
                jump_extra3 = round(0.5 - 0.025 * k, 3)
                jump_extra1_values.append(jump_extra1)
                jump_extra2_values.append(jump_extra2)
                jump_extra3_values.append(jump_extra3)

    # Check if the lengths match
    assert len(jump_dist) == len(jump_extra1_values) == len(jump_extra2_values) == len(jump_extra3_values), "Lengths of distances and parameters do not match"

    # Create a DataFrame
    data = {
        'jump_extra1': jump_extra1_values,
        'jump_extra2': jump_extra2_values,
        'jump_extra3': jump_extra3_values,
        'distance': jump_dist
    }
    df = pd.DataFrame(data)

    # Create the 3D scatter plot
    fig = px.scatter_3d(df, x='jump_extra1', y='jump_extra2', z='jump_extra3', color='distance',
                        title='3D Scatter Plot of Jump Distance',
                        labels={'jump_extra1': 'Jump Extra 1', 'jump_extra2': 'Jump Extra 2', 'jump_extra3': 'Jump Extra 3', 'distance': 'Jump Distance'},
                        color_continuous_scale='Viridis')

    # Show the plot
    fig.show()
    plot3_path = os.path.join(new_plots_directory_path, "colored3Dolpt(boxofDoom).html")
    fig.write_html(plot3_path)
    # Create the initial 3D scatter plot
    fig = go.Figure()

    # Add a scatter plot for each unique value of jump_extra3
    for jump_extra3_value in df['jump_extra3'].unique():
        filtered_df = df[df['jump_extra3'] == jump_extra3_value]
        scatter = go.Scatter3d(
            x=filtered_df['jump_extra1'],
            y=filtered_df['jump_extra2'],
            z=filtered_df['distance'],
            mode='markers',
            name=f'jump_extra3 = {jump_extra3_value}',
            visible=False  # Initially set all traces to invisible
        )
        fig.add_trace(scatter)

    # Make the first scatter plot visible
    fig.data[0].visible = True

    # Create the slider steps
    steps = []
    for i in range(len(fig.data)):
        step = dict(
            method='update',
            args=[{'visible': [False] * len(fig.data)}],
            label=f'jump_extra3 = {df["jump_extra3"].unique()[i]}'
        )
        step['args'][0]['visible'][i] = True  # Toggle i-th trace to visible
        steps.append(step)

    # Create the slider
    sliders = [dict(
        active=0,
        pad={"t": 50},
        steps=steps
    )]

    # Update the layout with slider
    fig.update_layout(
        sliders=sliders,
        scene=dict(
            xaxis_title='Jump Extra 1',
            yaxis_title='Jump Extra 2',
            zaxis_title='Distance'
        ),
        title='3D Scatter Plot of Jump Distance with Slider for Jump Extra 3'
    )

    # Show the plot
    fig.show()
    plot4_path = os.path.join(new_plots_directory_path, "scrollabledistanceplot.html")
    fig.write_html(plot4_path)