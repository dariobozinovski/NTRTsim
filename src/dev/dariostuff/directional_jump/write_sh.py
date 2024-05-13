import os

def add_line_to_sh_file(file_path,iterator):
    # Collect user inputs for various parameters
    start_time = 2.0
    min_length = 0.5
    rate = 0.3
    jump_time =17
    jump_delay=round(1-0.01*iterator,2)
    # Command format
    command = f"./AppisocDarYAMLdir /home/ubuntu/NTRTsim/src/dev/dariostuff/models/isodrop3Aext.yaml {start_time} {min_length} {rate} {jump_time} {jump_delay}\n"

    # Append the new command to the file
    with open(file_path, 'a') as file:
        file.write(command)
    print("New command added to the shell script.")

# Assuming the script is located in the same directory as the run.sh
file_path = "/home/ubuntu/NTRTsim/src/dev/dariostuff/directional_jump/run.sh"
for i in range(200):
    add_line_to_sh_file(file_path,i)