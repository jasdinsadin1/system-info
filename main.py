# -----------<System>------------ #
import time
import sys
# -----------</System>----------- #

# ------------<Info>------------- #
import platform
import winreg
import psutil
import subprocess
import GPUtil
import cpuinfo
# -----------</Info>------------- #

# ------------<GUI>-------------- #
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QFont
# -----------</GUI>-------------- #

# ---------<Threading>----------- #
import threading
# ---------</Threading>---------- #

class sysInfo(QMainWindow):
    def __init__(self):
        super(sysInfo, self).__init__()
        self.setWindowTitle("Quick Info")
        self.setMaximumSize(1000, 800)
        self.setMinimumSize(800, 500)
        
        self.show()
        labels = {}
        self.labels = labels
    
    def bytes2human(self,n):
        symbols = (' KB', ' MB', ' GB', ' TB', ' PB', ' EB', ' ZB', ' YB')
        prefix = {}
        for i, s in enumerate(symbols):
            # print(f"{i}:{s}")
            prefix[s] = 1 << (i + 1) * 10
            # print(prefix)
        for s in reversed(symbols):
            if abs(n) >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.2f%s' % (value, s)
        return "%sB" % n
    
    def get_windows_version(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            product_name, _ = winreg.QueryValueEx(key, "ProductName")
            release_id, _ = winreg.QueryValueEx(key, "ReleaseId")
            current_build, _ = winreg.QueryValueEx(key, "CurrentBuild")
            return f"{product_name} (Version {release_id}, Build {current_build})"
        except Exception as e:
            return str(e),"\n",platform.system(),"\n",platform.release()
    
    def storage_model(self):
        cmd = "wmic diskdrive get model"
        cmd_result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        cmd_output = cmd_result.stdout.strip()
        cmd_output_lines = cmd_output.split("\n")[1:]
        storage_models = [line.strip() for line in cmd_output_lines if line.strip()]
        disk_model_list = []
        for disk_name in storage_models:
            disk_model_list.append(disk_name)
        return ', '.join(disk_model_list)    
    
    def storage_partition(self):
        partition_list = []
        checker = psutil.disk_partitions()
        for partition in checker:
            partition_list.append(str(partition.device))
        return 'Drives: ' + ', '.join(partition_list)
        

    def storage_size(self):
        partitions = psutil.disk_partitions()
        partition_info_list = [
            f"{partition.device}({psutil.disk_usage(partition.mountpoint).total / (1024 ** 3):.2f} GB)"
            for partition in partitions
        ]
        return 'Disk size: '+ ', '.join(partition_info_list)

    def space_consumed(self):  
        consumed = []
        for partition in psutil.disk_partitions():
            info = psutil.disk_usage(partition.device)
            consumed.append(f"{partition.device} ({info.percent} %)")
        return ', '.join(consumed)
    
    def NV_gpu(self):
        checker = GPUtil.getGPUs()
        info = []
        for gpu in checker:
            info.append(gpu.name)
            info.append(str(int(gpu.memoryTotal)/1024) +' GB' )
        return ' --- '.join(info)

    def amd_gpu(self):
        cmd = "wmic path win32_videocontroller get Name"
        cmd_result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        cmd_output_sorted = cmd_result.stdout.strip()
        cmd_output_lines_sorted = cmd_output_sorted.split("\n")[1:]
        gpu_name = [line.strip() for line in cmd_output_lines_sorted if line.strip()]
        
        return ', '.join( gpu_name[1:5])
    def cpu_name(self):
        name = cpuinfo.get_cpu_info()['brand_raw']
        return name

    def cpu(self):
        core = psutil.cpu_count(logical=False)
        return 'Main cores: '+ str(core)

    def thread_count(self):
        logical_core = psutil.cpu_count(logical=True)
        return 'Logical Core: '+ str(logical_core)

    def cpu_usage(self):
        cpu_utilization = int(psutil.cpu_percent())
        return 'Cpu usage: '+ str(int(cpu_utilization)) + ' %'

    def cpu_freq(self):
        cpu_f = psutil.cpu_freq()
        return "Base Cpu Frequency: "+ str(float((cpu_f.current/100)/10)) +" GHz"
    def ram(self):
        total_ram = psutil.virtual_memory()
        return float(self.bytes2human(total_ram.total).strip("GB"))

    def ram_used(self):
        ram_used = psutil.virtual_memory()
        return float(self.bytes2human(ram_used.used).strip("GB"))

    def ram_percent(self):
        percent = psutil.virtual_memory().percent
        return percent
    
    def create_tab(self,tab_name):
        tab = QWidget(self)
        tab.setStyleSheet("color:white;background-color:black;")
        
        layout = QGridLayout()
        
        if tab_name == "System":
            label_design = QLabel("", tab)
            label_design.setAlignment(Qt.AlignCenter)
            label_design.setFont(QFont("Syne", 14))
            label_design.setStyleSheet("background-color:white; color:black;border-radius:15px;font-size:24px;")

            layout.addWidget(label_design, 0, 0, 1, 2)
            
            label = QLabel("", tab)
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Syne", 14))
            label.setStyleSheet("background-color:white; color:black;border-radius:15px;")
    
            label.setText(self.get_windows_version())
            layout.addWidget(label, 1, 0, 1, 2)
            
            label_info = QLabel("", tab)
            label_info.setAlignment(Qt.AlignCenter)
            label_info.setFont(QFont("Syne", 14))
            label_info.setStyleSheet("background-color:white; color:black; border-radius:15px;")
            
            label_info.setText("A Software to check system info ")
            layout.addWidget(label_info, 2, 0, 1, 2)
            
            label_creator = QLabel("", tab)
            label_creator.setAlignment(Qt.AlignCenter)
            label_creator.setFont(QFont("Syne", 14))
            label_creator.setStyleSheet("background-color:white; color:black; border-radius:15px;")
            
            label_creator.setText("Made by: Saad Jafor")
            layout.addWidget(label_creator, 3, 0, 1, 2)
            
            label_design2 = QLabel("", tab)
            label_design2.setAlignment(Qt.AlignCenter)
            label_design2.setFont(QFont("Syne", 14))
            label_design2.setStyleSheet("background-color:white; color:black;border-radius:15px;font-size:24px;")
            layout.addWidget(label_design2, 4,0,1,2)
            
            self.labels[tab_name] = [label, label_creator,label_design,label_design2,label_info]
        elif tab_name == "CPU":
            label_cpu_name = QLabel("", tab)
            label_cpu_name.setFont(QFont("Syne", 15))
            label_cpu_name.setStyleSheet("font-weight:600;")
            label_cpu_name.setAlignment(Qt.AlignCenter)
            label_cpu_name.setText(self.cpu_name())
            label_cpu_name.setStyleSheet("font-weight:600; font-style: oblique; color:#FFFF00;")
            layout.addWidget(label_cpu_name, 0, 0, 1, 2)
            

            label_cpu_core = QLabel("", tab)
            label_cpu_core.setFont(QFont("Syne", 15))
            label_cpu_core.setStyleSheet("font-weight:600;")
            label_cpu_core.setAlignment(Qt.AlignCenter)
            label_cpu_core.setStyleSheet("background-color: limegreen; border-radius: 10px;")
            label_cpu_core.setText(self.cpu())
            layout.addWidget(label_cpu_core, 1, 0)

            label_cpu_thread = QLabel("", tab)
            label_cpu_thread.setFont(QFont("Syne", 15))
            label_cpu_thread.setStyleSheet("font-weight:600;")
            label_cpu_thread.setAlignment(Qt.AlignCenter)
            label_cpu_thread.setText(self.thread_count())
            layout.addWidget(label_cpu_thread, 1, 1)

            label_cpu_usage = QLabel("", tab)
            label_cpu_usage.setFont(QFont("Syne", 15))
            label_cpu_usage.setStyleSheet("font-weight:600;")
            label_cpu_usage.setAlignment(Qt.AlignCenter)
            layout.addWidget(label_cpu_usage, 2, 0)
            
            label_cpu_freq = QLabel("", tab)
            label_cpu_freq.setFont(QFont("Syne", 15))
            label_cpu_freq.setStyleSheet("font-weight:600;")
            label_cpu_freq.setAlignment(Qt.AlignCenter)
            label_cpu_freq.setText(self.cpu_freq())
            layout.addWidget(label_cpu_freq, 2, 1)
            

            self.labels[tab_name] = [label_cpu_name, label_cpu_core, label_cpu_thread, label_cpu_usage, label_cpu_freq]

        elif tab_name == "GPU":
            label_gpu_main = QLabel("", tab)
            label_gpu_main.setFont(QFont("Syne", 15))
            label_gpu_main.setStyleSheet("font-weight:600;")
            label_gpu_main.setAlignment(Qt.AlignCenter)
            label_gpu_main.setText(self.NV_gpu())
            label_gpu_main.setStyleSheet("background-color:green; border-radius:15px; color:black;")
            layout.addWidget(label_gpu_main, 1, 0, 1, 2)

            label_gpu_2 = QLabel("", tab)
            label_gpu_2.setFont(QFont("Syne", 15))
            label_gpu_2.setStyleSheet("font-weight:600;")
            label_gpu_2.setAlignment(Qt.AlignCenter)
            label_gpu_2.setText(self.amd_gpu())
            label_gpu_2.setStyleSheet("background-color:red; border-radius:15px; color:black;")
            layout.addWidget(label_gpu_2, 2, 0, 1, 2)

            label_g = QLabel("", tab)
            label_g.setFont(QFont("Syne", 15))
            label_g.setStyleSheet("font-weight:600;")
            label_g.setAlignment(Qt.AlignCenter)
            label_g.setText("Graphics Card")
            label_g.setStyleSheet("background-color:white;border-radius:15px; color:black;")
            layout.addWidget(label_g, 0, 0, 1, 2)
            

            self.labels[tab_name] = [label_gpu_main, label_gpu_2, label_g]
            
        elif tab_name == "RAM":
            label_total = QLabel("", tab)
            label_total.setFont(QFont("Syne", 15))
            label_total.setStyleSheet("font-weight:600;")
            label_total.setAlignment(Qt.AlignCenter)
            label_total.setText(f'Ram: {self.ram()} GB')
            if int(self.ram()) >= 8.0 :
                label_total.setStyleSheet("background-color:green;border-radius:15px; color:white;")
            elif int(self.ram()) >=6.0:
                label_total.setStyleSheet("background-color:#d98b19;border-radius:15px; color:white;")
            elif int(self.ram()) >=4.0:
                label_total.setStyleSheet("background-color:red;border-radius:15px; color:white;")   
            else:
                label_total.setStyleSheet("background-color:#d98b19;border-radius:15px; color:white;")
            layout.addWidget(label_total, 0, 0, 1, 2)
            
            label_used = QLabel("", tab)
            label_used.setFont(QFont("Syne", 15))
            label_used.setStyleSheet("font-weight:600;")
            label_used.setAlignment(Qt.AlignCenter)
            label_used.setText(f"Ram used: {self.ram_used()} GB")
            layout.addWidget(label_used, 2,0)
        
            
            label_used_percent = QLabel("", tab)
            label_used_percent.setFont(QFont("Syne", 15))
            label_used_percent.setStyleSheet("font-weight:600;")
            label_used_percent.setAlignment(Qt.AlignCenter)
            label_used_percent.setText(f"{self.ram_percent()} %")
            
            layout.addWidget(label_used_percent, 2,1)
            
            
            
            self.labels[tab_name] = [label_total,label_used,label_used_percent]
        elif tab_name == "Storage":
            label_st_model = QLabel("", tab)
            label_st_model.setFont(QFont("Syne", 15))
            label_st_model.setStyleSheet("font-weight:600;")
            label_st_model.setAlignment(Qt.AlignCenter)
            label_st_model.setText(self.storage_model())
            label_st_model.setStyleSheet("background-color:black;font-style:oblique; border-radius:15px; color:#d98b19;")
            layout.addWidget(label_st_model, 0,0,1,2)
            
            label_partition = QLabel("", tab)
            label_partition.setFont(QFont("Syne", 15))
            label_partition.setStyleSheet("font-weight:600;")
            label_partition.setAlignment(Qt.AlignCenter)
            label_partition.setText(self.storage_partition())
            label_partition.setStyleSheet("background-color:#d98b19; border-radius:15px; color:white;")
            layout.addWidget(label_partition, 1,0)
            
            label_partition_size = QLabel("", tab)
            label_partition_size.setFont(QFont("Syne", 15))
            label_partition_size.setStyleSheet("font-weight:600;")
            label_partition_size.setAlignment(Qt.AlignCenter)
            label_partition_size.setText(self.storage_size())
            label_partition_size.setStyleSheet("background-color:#d98b19; border-radius:15px; color:white; padding-left:5px;padding-right:5px;")
            layout.addWidget(label_partition_size, 1,1)
            
            label_consumed = QLabel("", tab)
            label_consumed.setFont(QFont("Syne", 15))
            label_consumed.setStyleSheet("font-weight:600;")
            label_consumed.setAlignment(Qt.AlignCenter)
            label_consumed.setText(self.space_consumed())
            label_consumed.setStyleSheet("background-color:#d98b19; border-radius:15px; color:white;")
            layout.addWidget(label_consumed, 2,0,1,2)
            
            self.labels [tab_name]= [label_st_model, label_partition_size,label_partition,label_consumed]
        else:
            label1 = QLabel(f"Tab {tab_name} - Label 1", tab)
            label2 = QLabel(f"Tab {tab_name} - Label 2", tab)
            layout.addWidget(label1)
            layout.addWidget(label2)

            self.labels[tab_name] = [label1, label2]

        tab.setLayout(layout)
        

        
        
        return tab
        
    def update_labels(self):
        while True:
            cpu_usage =self.cpu_usage()
            ram_u =self.ram_used()
            ram_p =self.ram_percent()
            self.labels["CPU"][3].setText(cpu_usage)
            
            self.labels["System"][2].setText("    -     ")
            time.sleep(.2)
            self.labels["System"][2].setText("   ---    ")
            time.sleep(.2)
            self.labels["System"][2].setText("  ------  ")
            time.sleep(.2)
            self.labels["System"][2].setText("----------")
            time.sleep(.2)
            self.labels["System"][2].setText("  ------  ")
            time.sleep(.2)
            self.labels["System"][2].setText("   ---    ")
            time.sleep(.2)
            self.labels["System"][2].setText("    -     ")
            time.sleep(.2)
            
            self.labels["System"][3].setText("    -     ")
            time.sleep(.2)
            self.labels["System"][3].setText("   ---    ")
            time.sleep(.2)
            self.labels["System"][3].setText("  ------  ")
            time.sleep(.2)
            self.labels["System"][3].setText("----------")
            time.sleep(.2)
            self.labels["System"][3].setText("  ------  ")
            time.sleep(.2)
            self.labels["System"][3].setText("   ---    ")
            time.sleep(.2)
            self.labels["System"][3].setText("    -     ")
            self.labels["RAM"][1].setText(f"Ram used: {ram_u} GB")
            
            time.sleep(.2)
            self.labels["RAM"][2].setText(f"{ram_p} %")

            threading.Event().wait(.2)

    def color(self):
        while True:
            ram_u =self.ram_used()
            ram_p = self.ram_percent()
            if ram_u <=3.5:
                self.labels["RAM"][1].setStyleSheet("background-color:green;border-radius:15px; color:white;")
            elif ram_u <=5.0:
                self.labels["RAM"][1].setStyleSheet("background-color:#FFCF0D;border-radius:15px; color:grey; font-weight:600;")
            elif ram_u <=7.0:
                self.labels["RAM"][1].setStyleSheet("background-color:red;border-radius:15px; color:white;")
            else:
                self.labels["RAM"][1].setStyleSheet("background-color:#d98b19;border-radius:15px; color:white;")
            
            if ram_p <= 29.5:
                self.labels["RAM"][2].setStyleSheet("background-color:green;border-radius:15px; color:white;")
            elif ram_u <=35.0:
                self.labels["RAM"][2].setStyleSheet("background-color:#FFCF0D;border-radius:15px; color:grey; font-weight:600;")
            elif ram_u <=50.0:
                self.labels["RAM"][2].setStyleSheet("background-color:red;border-radius:15px; color:white;")
            else:
                self.labels["RAM"][2].setStyleSheet("background-color:#d98b19;border-radius:15px; color:white;")            
            threading.Event().wait(.2)
        
    def main(self):
        system_tab = self.create_tab("System")
        cpu_tab = self.create_tab("CPU")
        gpu_tab = self.create_tab("GPU")
        ram_tab = self.create_tab("RAM")
        storage_tab = self.create_tab("Storage") 
        
        tab_widget = QTabWidget()
        # tab_widget.Triangular
        
        tab_widget.addTab(system_tab, "System")
        tab_widget.addTab(cpu_tab, "CPU")
        tab_widget.addTab(gpu_tab, "GPU")
        tab_widget.addTab(ram_tab, "RAM")
        tab_widget.addTab(storage_tab, "Storage")
        
        
        self.setCentralWidget(tab_widget)
        
        update_thread = threading.Thread(target=self.update_labels)
        update_thread.daemon = True
        update_thread.start()
        
        update_color = threading.Thread(target=self.color)
        update_color.daemon = True
        update_color.start()

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = sysInfo()
    window.main()
    
    sys.exit(app.exec_())