import platform
import os
import shutil

def setupDriver():
    if platform.system() == 'Windows':
        shutil.copy()
        os.rename('chromedriver_win.exe', 'chromedriver.exe')