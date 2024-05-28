import os

def generate_filenames():
    filenames = []
    iterator = 0
    start_time = 1.0
    min_length = 0.5
    rate = 1
    jump_time = 6
    jump_delay = 0

    for i in range(21):
        jump_extra1 = round(0.5 - 0.025 * i, 3)
        for j in range(21):
            jump_extra2 = round(0.5 - 0.025 * j, 3)
            for k in range(21):
                jump_extra3 = round(0.5 - 0.025 * k, 3)
                filename = f"sim{iterator}_{jump_extra1}_{jump_extra2}_{jump_extra3}.csv"
                filenames.append(filename)
                iterator += 1
    return filenames

def rename_csv_files(folder_path):
    # Generate the list of new filenames
    new_filenames = generate_filenames()

    # Get the list of current CSV files in the folder (assuming they are in order of execution)
    csv_files = sorted([f for f in os.listdir(folder_path)])

    # Iterate through the existing CSV files and rename them
    for i, old_name in enumerate(csv_files):
        old_path = os.path.join(folder_path, old_name)
        new_name = new_filenames[i] if i < len(new_filenames) else f"missing_filename_{i}.csv"
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed '{old_name}' to '{new_name}'")

# Define the folder containing the CSV files
folder_path = "/home/ubuntu/NTRTsim/NTRTsim_logs/plotting/simmoonpretension/"

# Call the function to rename the files
rename_csv_files(folder_path)