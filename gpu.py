import GPUtil
import subprocess

# import pyamdgpuinfo



def NV_gpu():
    checker = GPUtil.getGPUs()
    info = []
    for gpu in checker:
        info.append(gpu.name)
        info.append(str(int(gpu.memoryTotal)/1024) +' GB' )
    return ' --- '.join(info)

def amd_gpu():
    cmd = "wmic path win32_videocontroller get Name"
    cmd_result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    cmd_output_sorted = cmd_result.stdout.strip()
    cmd_output_lines_sorted = cmd_output_sorted.split("\n")[1:]
    gpu_name = [line.strip() for line in cmd_output_lines_sorted if line.strip()]
    
    return ', '.join( gpu_name[1:5])
