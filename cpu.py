import psutil
import cpuinfo


def cpu_name():
    name = cpuinfo.get_cpu_info()['brand_raw']
    
    return name

def cpu():
    core = psutil.cpu_count(logical=False)

    return 'Main cores: '+ str(core)

def thread_count():
    logical_core = psutil.cpu_count(logical=True)
    
    return 'Logical Core: '+ str(logical_core)

def cpu_usage():
    
    cpu_utilization = int(psutil.cpu_percent())
    
    return 'Cpu usage: '+ str(int(cpu_utilization)) + ' %'

def cpu_freq():
    cpu_f = psutil.cpu_freq()
    
    return "Cpu Frequency: "+ str(int(cpu_f.current/100)) +" MHz"
    
    

