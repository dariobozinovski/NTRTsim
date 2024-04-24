from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.animation import FuncAnimation
# Constants
data_per_rod = 7  # XYZ position, Euler angles, mass
data_per_spring = 3  # RestLength, CurrentLength, Tension
num_actuated_cables = 3  # The same data format as springs
num_rods = 6
extension = 1
num_ext = 0
num_comp = 0
if(extension):
    num_comp = num_rods
    num_ext = num_rods*2

# File and directory settings
directory_path = "/home/ubuntu/NTRTsim/NTRTsim_logs/to_plot"

plt.style.use('fivethirtyeight')
#file_path =directory_path+os.listdir(directory_path)
file_path = os.path.join(directory_path, os.listdir(directory_path)[0])
print(file_path)

index = count()

def parse_csv(file_path):
    df = pd.read_csv(file_path, skiprows=2)  # Adjust skiprows if needed to match your CSV format
    total_rod_columns = num_rods * data_per_rod
    total_actuateted_columns = num_actuated_cables * data_per_spring
    total_compound_columns = data_per_rod * num_comp
    total_extension_columns = data_per_rod * num_ext
    total_spring_columns = (len(df.columns) - total_rod_columns - total_actuateted_columns - total_compound_columns - total_extension_columns - 1) // data_per_spring
    
    column_names = ['Time']
    for compound in range(1, num_comp + 1):
        column_names += [f'Comp{compound}_X', f'Comp{compound}_Y', f'Comp{compound}_Z', f'Comp{compound}_EulerX', f'Comp{compound}_EulerY', f'Comp{compound}_EulerZ', f'Comp{compound}_mass']
    
    for rod in range(1, num_rods + 1):
        column_names += [f'Rod{rod}_X', f'Rod{rod}_Y', f'Rod{rod}_Z', f'Rod{rod}_EulerX', f'Rod{rod}_EulerY', f'Rod{rod}_EulerZ', f'Rod{rod}_mass']
    
    for ext in range(1, num_ext + 1):
        column_names += [f'ext{ext}_X', f'ext{ext}_Y', f'ext{ext}_Z', f'ext{ext}_EulerX', f'ext{ext}_EulerY', f'ext{ext}_EulerZ', f'ext{ext}_mass']
    
    for cable in range(1, num_actuated_cables + 1):
        column_names += [f'ActuatedCable{cable}_RestLength', f'ActuatedCable{cable}_CurrentLength', f'ActuatedCable{cable}_Tension']
    
    for spring in range(1, total_spring_columns + 1):
        column_names += [f'Spring{spring}_RestLength', f'Spring{spring}_CurrentLength', f'Spring{spring}_Tension']

    column_names += ['to_delete']  # assuming there's a trailing unused column to delete
    df = pd.read_csv(file_path, skiprows=2, names=column_names)
    sim_timestep=df['Time'].iloc[-1]-df['Time'].iloc[-2]
    
    return column_names,sim_timestep

cl_names,sim_timestep=parse_csv(file_path)
time_range=30/sim_timestep
def animate(i):
    data = pd.read_csv(file_path, skiprows=2, names=cl_names)
    data=data.tail(int(time_range))
    x = data['Time']
    y1 = data['ActuatedCable1_Tension']*0.1
    y2 = data['ActuatedCable2_Tension']*0.1
    y3 = data['ActuatedCable3_Tension']*0.1
    

    plt.cla()

    plt.plot(x, y1, label='Tension 1')
    plt.plot(x, y2, label='Tension 2')
    plt.plot(x, y3, label='Tension 3')

    plt.legend(loc='upper left')
    plt.tight_layout()

ani=FuncAnimation(plt.gcf(),animate,interval=1000)
plt.tight_layout()
plt.show()
