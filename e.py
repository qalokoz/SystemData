import subprocess
import psutil

def get_memory_data():
    output = subprocess.check_output(["system_profiler", "SPHardwareDataType"])
    output = output.decode("utf-8").split("\n")

    # Extract memory data from output
    for line in output:
        if "Memory:" in line:
            memory_data = line.split(":")[1].strip()
            break
    # Format memory data
    memory_data = memory_data.replace(" GB", "GB").replace("MHz", " MHz")

    return memory_data

def get_running_processes_data_for_my_system():
    processes_data = []
    for process in psutil.process_iter(['pid', 'name', 'username']):
        try:
            # Get process data
            process_data = process.info
            # Append process data to list
            processes_data.append(process_data)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes_data

memory_data = get_memory_data()
print(memory_data)
processes_data = get_running_processes_data_for_my_system()
print(processes_data)