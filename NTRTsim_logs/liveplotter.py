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


df = pd.read_csv(file_path, skiprows=1)  # Adjust skiprows if needed to match your CSV format
total_rod_columns = num_rods * data_per_rod
total_actuateted_columns = num_actuated_cables * data_per_spring
total_compound_columns = data_per_rod * num_comp
total_extension_columns = data_per_rod * num_ext
total_spring_columns = (len(df.columns) - total_rod_columns - total_actuateted_columns - total_compound_columns - total_extension_columns - 1) // data_per_spring
    
    
sim_timestep=df['time'].iloc[-1]-df['time'].iloc[-2]
time_range=30/sim_timestep
def animate(i):
    data = pd.read_csv(file_path, skiprows=1)
    data=data.tail(int(time_range))
    x = data['time']
    y1 = data[next(col for col in df.columns if 'activated_cable c1' in col and col.endswith('.Tension'))]*0.1
    y2 = data[next(col for col in df.columns if 'activated_cable c2' in col and col.endswith('.Tension'))]*0.1
    y3 = data[next(col for col in df.columns if 'activated_cable c3' in col and col.endswith('.Tension'))]*0.1
    

    plt.cla()

    plt.plot(x, y1, label='Tension 1')
    plt.plot(x, y2, label='Tension 2')
    plt.plot(x, y3, label='Tension 3')

    plt.legend(loc='upper left')
    plt.tight_layout()

ani=FuncAnimation(plt.gcf(),animate,interval=1000)
plt.tight_layout()
plt.show()
