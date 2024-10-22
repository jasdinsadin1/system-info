
from cx_Freeze import setup, Executable



setup(
    name="Quick System Information",
    options={"build_exe": {
        "packages": ["time", "sys", "PyQt5.QtCore","PyQt5.QtGui",
                     "PyQt5.QtWidgets", "PyQt5.QtWidgets", "threading", "platform", "winreg", "subprocess","psutil","GPUtil","cpuinfo"],
        "include_files":[r"C:\Users\jasdi\AppData\Local\Programs\Python\Python311\Lib\site-packages\PyQt5\Qt5\plugins\platforms\qwindows.dll",r"C:\Users\jasdi\AppData\Local\Programs\Python\Python311\DLLs\tcl86t.dll",r"C:\Users\jasdi\AppData\Local\Programs\Python\Python311\DLLs\tk86t.dll"]
        }},
    version="1.0b",
    executables=[Executable("main.py",
                            base="Win32GUI")]
) 