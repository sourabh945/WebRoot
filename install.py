### This program is use to install and configure all the server for use it 
### it make all required files for logs and database of user credentials 
### all define the pre-required things to run the system

import os
import platform

if platform.system() == "Windows":
    _separator = "\"

print("Start installation and configuration")

### installing the all packages for the server

if os.system("pip3 install flask") != 0 and os.system("pip3 install tk") != 0:
    print("\nThere is problem to install the packages try to comment it and install manually.\n")
    exit(1)

from tkinter import filedialog,messagebox

messagebox.showinfo(title="Selection of folder",message="Select the folder where the logs folder and database folder should be created.")

folder_path = filedialog()

items = set(os.listdir(folder_path))

if "logs" not in items:
    os.mkdir(folder_path+_separator+"logs")