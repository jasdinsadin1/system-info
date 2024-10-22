import psutil
import subprocess


def storage_model():
    cmd = "wmic diskdrive get model"
    cmd_result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    cmd_output = cmd_result.stdout.strip()
    cmd_output_lines = cmd_output.split("\n")[1:]
    storage_models = [line.strip() for line in cmd_output_lines if line.strip()]
    # print(storage_models)
    # global disk_model_list
    disk_model_list = []
    for disk_name in storage_models:
        
        disk_model_list.append(disk_name)
        
    return ', '.join(disk_model_list)
# print(storage_model())

    
def storage_partition():
    # global partition_list
    partition_list = []
    checker = psutil.disk_partitions()
    for partition in checker:
        partition_list.append(str(partition.device))
        # print(partition)
        # print(partition.device)
    return 'Drives: ' + ', '.join(partition_list)
    
# print(storage_partition())

def storage_size():
    partitions = psutil.disk_partitions()
    partition_info_list = [
        f"{partition.device}({psutil.disk_usage(partition.mountpoint).total / (1024 ** 3):.2f} GB)"
        for partition in partitions
    ]
    return 'Disk size: '+ ', '.join(partition_info_list)

# print(storage_size())
def space_consumed ():  
    # global consumed
    consumed = []
    for partition in psutil.disk_partitions():
        info = psutil.disk_usage(partition.device)
        consumed.append(f"{partition.device} ({info.percent} %)")
    return ', '.join(consumed)
        
# print(space_consumed())