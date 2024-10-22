import platform
import winreg

def get_windows_version():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
        product_name, _ = winreg.QueryValueEx(key, "ProductName")
        release_id, _ = winreg.QueryValueEx(key, "ReleaseId")
        current_build, _ = winreg.QueryValueEx(key, "CurrentBuild")
        return f"{product_name} (Version {release_id}, Build {current_build})"
    except Exception as e:
        return str(e),"\n",platform.system(),"\n",platform.release()

