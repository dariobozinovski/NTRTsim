import os

# def add_line_to_sh_file(file_path,iterator):
#     # Collect user inputs for various parameters
#     start_time = 2.0
#     min_length = 0.5
#     rate = 0.3
#     jump_time =17
#     jump_delay=round(1-0.01*iterator,2)
    
def add_line_to_sh_file(file_path,iterator):
    # Collect user inputs for various parameters
    start_time = 1.0
    min_length = 0.5
    rate = 1
    jump_time =6
    jump_delay=0
    jump_extra1=round(0.5-0.05*iterator,2)
    for i in range(21):
        jump_extra2=round(0.5-0.025*i,2)
        for j in range(21):
            jump_extra3=round(0.5-0.025*j,3)
            # Command format
            command = f"./AppisocDarYAMLdirpret /home/ubuntu/NTRTsim/src/dev/dariostuff/models/isodrop3Aextalligned.yaml {start_time} {min_length} {rate} {jump_time} {jump_delay} {jump_extra1} {jump_extra2} {jump_extra3}\n"
            # Append the new command to the file
            with open(file_path, 'a') as file:
                file.write(command)
            print("New command added to the shell script.")
    
# Assuming the script is located in the same directory as the run.sh
file_path = "/home/ubuntu/NTRTsim/src/dev/dariostuff/directional_jumppretension/run.sh"
for i in range(21):
    add_line_to_sh_file(file_path,i)