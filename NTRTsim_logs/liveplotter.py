import pandas as pd
import plotly.graph_objects as go
from time import sleep
import os

# Constants
data_per_rod = 7  # XYZ position, Euler angles, mass
data_per_spring = 3  # RestLength, CurrentLength, Tension
num_actuated_cables = 3  # The same data format as springs
num_rods = 6
extension=1
num_ext = 0
num_comp = 0
if(extension):
    num_comp=num_rods
    num_ext=num_rods*2

# File and directory settings
directory_path = "/home/ubuntu/NTRTsim/NTRTsim_logs/to_plot"

# Initialize Plot
fig = go.FigureWidget()
fig.update_layout(title='Tension in Actuated Cable 1 Over Time', xaxis_title='Time', yaxis_title='Tension')

# Function to read and parse CSV
def parse_csv(file_path):
    df = pd.read_csv(file_path, skiprows=2)  # Adjust skiprows if needed to match your CSV format
    total_rod_columns = num_rods * data_per_rod
    total_actuateted_columns=num_actuated_cables*data_per_spring
    total_compound_columns=data_per_rod*num_comp
    total_extension_columns=data_per_rod*num_ext
    total_spring_columns = (len(df.columns)- total_rod_columns-total_actuateted_columns-total_compound_columns-total_extension_columns-1)//data_per_spring
    
    # Assuming the column order based on your previous message
    column_names = ['Time']
    for compound in range(1, num_comp +1):
        
        column_names += [f'Comp{compound}_X', f'Comp{compound}_Y', f'Comp{compound}_Z', f'RCompod{compound}_EulerX', f'Comp{compound}_EulerY', f'Comp{compound}_EulerZ',f'Comp{compound}_mass']
    
    for rod in range(1, num_rods + 1):
    
        column_names += [f'Rod{rod}_X', f'Rod{rod}_Y', f'Rod{rod}_Z', f'Rod{rod}_EulerX', f'Rod{rod}_EulerY', f'Rod{rod}_EulerZ',f'Rod{rod}_mass']
    
    for ext in range(1,num_ext+1):
    
        column_names += [f'ext{ext}_X', f'ext{ext}_Y', f'ext{ext}_Z', f'ext{ext}_EulerX', f'ext{ext}_EulerY', f'ext{ext}_EulerZ',f'ext{ext}_mass']
    
    for cable in range(1, num_actuated_cables + 1):
    
        column_names += [f'ActuatedCable{cable}_RestLength', f'ActuatedCable{cable}_CurrentLength', f'ActuatedCable{cable}_Tension']
    
    for spring in range(1, total_spring_columns + 1):

        column_names += [f'Spring{spring}_RestLength', f'Spring{spring}_CurrentLength', f'Spring{spring}_Tension']

    
    column_names += ['to_delete']  # Match column names up to the number of columns in the CSV
    df = pd.read_csv(file_path, skiprows=2, names=column_names)
    return df

# Function to update the plot
def update_plot():
    all_files = sorted([f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))])
    if not all_files:
        return
    latest_file = os.path.join(directory_path, all_files[-1])
    df = parse_csv(latest_file)
    if 'ActuatedCable1_Tension' in df.columns:
        time = df['Time']
        tension = df['ActuatedCable1_Tension']
        fig.data = []
        fig.add_scatter(x=time, y=tension, mode='lines+markers')
        fig.show()

# Loop to update the plot every 5 seconds
while True:
    update_plot()
    sleep(5)  # Adjust time as needed