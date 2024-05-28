import numpy as np
import subprocess
import csv
import GPyOpt
import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the global variables to track costs and parameters
costs = []
parameters = []

def jumpdistance(df):
    # Define the simulation timestep
    sim_timestep = round(df['time'].iloc[-1] - df['time'].iloc[-2], 5)
    # Define columns for X, Y, Z coordinates
    x = [col for col in df.columns if 'prism_rod' in col and col.endswith('.X')]
    y = [col for col in df.columns if 'prism_rod' in col and col.endswith('.Y')]
    z = [col for col in df.columns if 'prism_rod' in col and col.endswith('.Z')]
    
    # Calculate the average position of all rods
    CM_x = df[x].mean(axis=1) * 0.1 
    CM_y = df[y].mean(axis=1) * 0.1
    CM_z = df[z].mean(axis=1) * 0.1
    
    # Find the index of the first decreasing value from the 6th second
    start_index = int(6 / sim_timestep)
    decreasing_index = start_index + np.argmax(np.diff(CM_y[start_index:]) < 0) + 1
    
    # Find the x and z position of the center of mass in the two moments
    CM_x_maxy = CM_x[decreasing_index]
    CM_z_maxy = CM_z[decreasing_index]    
    
    index_prejump = int((6 / sim_timestep) - 0.99)
    CM_x_miny = CM_x[index_prejump]
    CM_z_miny = CM_z[index_prejump]
    
    # Calculate the distance
    distance = np.sqrt((CM_x_maxy - CM_x_miny) ** 2 + (CM_z_maxy - CM_z_miny) ** 2) * 2
    
    return distance

def get_latest_txt_file(directory):
    # List all files in the directory
    files = os.listdir(directory)
    # Filter for TXT files
    txt_files = [file for file in files if file.endswith('.txt')]
    # Get the most recent file by modification date
    latest_file = max(txt_files, key=lambda file: os.path.getmtime(os.path.join(directory, file)))
    return os.path.join(directory, latest_file)

def run_simulation(params):
    global costs, parameters
    print(params)
    # Convert params to the appropriate format for the sh file
    pretensions = params[0,0:3]
    delays = params[0,3:6]
    start_time = 1.0
    min_length = 0.5
    rate = 1
    jump_time = 6
    
    command = f"#!/bin/bash \n cd /home/ubuntu/NTRTsim/build/dev/dariostuff/directional_both/ \n./AppisocDarYAMLdirboth /home/ubuntu/NTRTsim/src/dev/dariostuff/models/isodrop3Aextalligned.yaml {start_time} {min_length} {rate} {jump_time} {delays[0]} {delays[1]} {delays[2]} {pretensions[0]} {pretensions[1]} {pretensions[2]}\n"
    
    # Write the command to a temporary shell script
    temp_file_path = '/tmp/run_temp_simulation.sh'
    with open(temp_file_path, 'w') as file:
        file.write(command)
    
    # Run the simulation
    subprocess.run(['sh', temp_file_path])
    
    csv_directory = '/home/ubuntu/NTRTsim/NTRTsim_logs/to_plot/'  # Update with the correct directory
    latest_csv_file = get_latest_txt_file(csv_directory)
    # Parse the CSV output
    df = pd.read_csv(latest_csv_file,skiprows=1)
    
    # Compute the distance of the jump
    cost = jumpdistance(df)
    
    # Track the cost and parameters
    costs.append(cost)
    parameters.append(np.concatenate((pretensions, delays, [cost])))
    
    return -cost  # Negative because we minimize in GPyOpt

# Define the parameter bounds
bounds = [{'name': 'pretension1', 'type': 'continuous', 'domain': (0, 0.5)},
          {'name': 'pretension2', 'type': 'continuous', 'domain': (0, 0.5)},
          {'name': 'pretension3', 'type': 'continuous', 'domain': (0, 0.5)},
          {'name': 'delay1', 'type': 'continuous', 'domain': (0, 1)},
          {'name': 'delay2', 'type': 'continuous', 'domain': (0, 1)},
          {'name': 'delay3', 'type': 'continuous', 'domain': (0, 1)}]

# Initialize Bayesian Optimization
optimizer = GPyOpt.methods.BayesianOptimization(f=run_simulation, domain=bounds)

# Run the optimization
optimizer.run_optimization(max_iter=2)

# Print the best parameters
best_params = optimizer.X[np.argmin(optimizer.Y)]
best_cost = -np.min(optimizer.Y)
print("Best parameters found:", best_params)
print("Best jump distance:", best_cost)

# Save the parameters and costs to a CSV file
output_df = pd.DataFrame(parameters, columns=['pretension1', 'pretension2', 'pretension3', 'delay1', 'delay2', 'delay3', 'cost'])
output_df.to_csv('/home/ubuntu/NTRTsim/NTRTsim_logs/plots/learningsimulation_parameters_costs.csv', index=False)

# Plot the cost function over the iterations
plt.plot(costs)
plt.xlabel('Iteration')
plt.ylabel('Jump Distance')
plt.title('Jump Distance Over Iterations')

# Save the plot
plt.savefig('/home/ubuntu/NTRTsim/NTRTsim_logs/plots/learning/jump_distance_plot.png')