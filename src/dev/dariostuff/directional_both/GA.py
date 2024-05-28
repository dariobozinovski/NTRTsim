import numpy as np
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import os
import random
from deap import base, creator, tools, algorithms

# Global variables to track costs and parameters
costs = []
parameters = []
child = 1

def jumpdistance(df):
    
    # Calculate the jump distance based on the simulation output
    sim_timestep = round(df['time'].iloc[-1] - df['time'].iloc[-2], 5)
    df = df.iloc[int(1/sim_timestep):]
    x = [col for col in df.columns if 'prism_rod' in col and col.endswith('.X')]
    y = [col for col in df.columns if 'prism_rod' in col and col.endswith('.Y')]
    z = [col for col in df.columns if 'prism_rod' in col and col.endswith('.Z')]
    
    CM_x = df[x].mean(axis=1) * 0.1 
    CM_y = df[y].mean(axis=1) * 0.1
    CM_z = df[z].mean(axis=1) * 0.1
    
    max_y_index=CM_y.idxmax()
    min_y_index=CM_y.idxmin()
    if(CM_y[max_y_index]<0.60):
        print("Jump not high enough")
        return 0
    
    
    CM_x_maxy = CM_x[max_y_index]
    CM_z_maxy = CM_z[max_y_index]    
    
    index_prejump = int((6 / sim_timestep) - 0.99)
    CM_x_miny = CM_x[index_prejump]
    CM_z_miny = CM_z[index_prejump]
    
    distance = np.sqrt((CM_x_maxy - CM_x_miny) ** 2 + (CM_z_maxy - CM_z_miny) ** 2) * 2
    print(f"Jump distance: {distance} jump height: {CM_y[max_y_index]}")
    return distance

def get_latest_txt_file(directory):
    files = os.listdir(directory)
    txt_files = [file for file in files if file.endswith('.txt')]
    latest_file = max(txt_files, key=lambda file: os.path.getmtime(os.path.join(directory, file)))
    return os.path.join(directory, latest_file)

def run_simulation(params, generation):
    global costs, parameters, child

    pretensions = params[0:3]
    delays = params[3:6]
    start_time = 1.0
    min_length = 0.5
    rate = 1
    jump_time = 6
    
    command = f"#!/bin/bash \n cd /home/ubuntu/NTRTsim/build/dev/dariostuff/directional_both/ \n./AppisocDarYAMLdirboth /home/ubuntu/NTRTsim/src/dev/dariostuff/models/isodrop3Aextalligned.yaml {start_time} {min_length} {rate} {jump_time} {delays[0]} {delays[1]} {delays[2]} {pretensions[0]} {pretensions[1]} {pretensions[2]}\n"
    
    temp_file_path = '/tmp/run_temp_simulation.sh'
    with open(temp_file_path, 'w') as file:
        file.write(command)
    
    subprocess.run(['sh', temp_file_path])
    
    txt_directory = '/home/ubuntu/NTRTsim/NTRTsim_logs/to_plot/'  # Update with the correct directory
    latest_txt_file = get_latest_txt_file(txt_directory)
    
    df = pd.read_csv(latest_txt_file, skiprows=1)
    
    cost = jumpdistance(df)
    
    costs.append(cost)
    parameters.append([generation] + list(params) + [cost])
    
    print(f"Generation {generation} individual {child}")
    child += 1
    return -cost  # Negative because GA minimizes by default

def custom_mutation(individual, low, up, indpb):
    for i in range(len(individual)):
        if random.random() < indpb:
            individual[i] += random.uniform(-0.1, 0.1)  # Modify this step based on your mutation logic
            # Ensure the value is within bounds
            if individual[i] < low[i]:
                individual[i] = low[i]
            elif individual[i] > up[i]:
                individual[i] = up[i]
            print(f"Mutated individual parameter: {individual[i]}")
    return individual,
# def custom_crossover(ind1, ind2, alpha):
#     for i in range(len(ind1)):
#         if random.random() < 0.5:
#             ind1[i], ind2[i] = tools.cxBlend((ind1[i], ind2[i]), alpha)
#         # Ensure the values are within bounds
#         ind1[i] = max(param_bounds[i][0], min(ind1[i], param_bounds[i][1]))
#         ind2[i] = max(param_bounds[i][0], min(ind2[i], param_bounds[i][1]))
        
#     print(f"Crossover results: {ind1}, {ind2}")
#     return ind1, ind2
def custom_crossover(ind1, ind2, low, up, alpha=0.5):

    for i in range(len(ind1)):
        if random.random() < alpha:
            # Perform crossover
            ind1[i], ind2[i] = (ind1[i] + ind2[i]) / 2, (ind1[i] + ind2[i]) / 2
            # Ensure the values are within bounds
            ind1[i] = max(low[i], min(ind1[i], up[i]))
            ind2[i] = max(low[i], min(ind2[i], up[i]))
    print(f" {ind1}\n {ind2}\n")
    return ind1, ind2
# Define the parameter bounds
param_bounds = [(0.0, 0.5), (0.0, 0.5), (0.0, 0.5), (0.0, 0.5), (0.0, 0.5), (0.0, 0.5)]

# Setup DEAP for GA
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float", lambda low, up: random.uniform(low, up), *param_bounds[0])
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, len(param_bounds))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("mate", custom_crossover, low=[float(b[0]) for b in param_bounds],
                 up=[float(b[1]) for b in param_bounds], alpha=0.5)
toolbox.register("mutate", custom_mutation, low=[float(b[0]) for b in param_bounds],
                 up=[float(b[1]) for b in param_bounds], indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", lambda ind: run_simulation(ind, generation))

# Debugging function to check parameter values
def debug_individuals(individuals):
    for i, ind in enumerate(individuals):
        print(f"Individual {i}: {ind}")
        for val in ind:
            print(f"Value: {val}, Type: {type(val)}")

# Create an initial population
population = toolbox.population(n=50)

# Debug initial population
#debug_individuals(population)

# Define the number of generations
ngen = 30
cxpb = 0.5  # Crossover probability
mutpb = 0.2  # Mutation probability

# Track the current generation
generation = 0

# Run the Genetic Algorithm
for gen in range(ngen):
    generation = gen
    offspring = algorithms.varAnd(population, toolbox, cxpb, mutpb)
    
    # Debug offspring
    debug_individuals(offspring)
    
    fits = toolbox.map(toolbox.evaluate, offspring)
    
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = (fit,)
    
    population = toolbox.select(offspring, k=len(population))
    print(f"Generation {gen} completed")
    print(f"best individual: {tools.selBest(population, 1)} with fitness: {tools.selBest(population, 1)[0].fitness.values[0]}")
    child = 1

# Extract the best individual
best_ind = tools.selBest(population, 1)[0]
print(f"Best individual is {best_ind}, with fitness: {best_ind.fitness.values[0]}")

# Save parameters and costs to a CSV file
output_df = pd.DataFrame(parameters, columns=['generation', 'pretension1', 'pretension2', 'pretension3', 'delay1', 'delay2', 'delay3', 'cost'])
output_df.to_csv('/home/ubuntu/NTRTsim/NTRTsim_logs/plots/learning/simulation_parameters_costs.csv', index=False)

# Plot the cost function over the iterations
plt.plot(costs)
plt.xlabel('Iteration')
plt.ylabel('Jump Distance')
plt.title('Jump Distance Over Iterations')

# Save the plot as an image file
plt.savefig('/home/ubuntu/NTRTsim/NTRTsim_logs/plots/learning/GA.png')
