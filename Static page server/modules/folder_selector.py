import tkinter as tk
from tkinter import filedialog , messagebox

####################################

from modules.error_logger import error_log

#####################################
### It is function that prompt for folder selector window and it uses
### tkinter the gui module of python to this and it return path of the
### selected folder.

def get_path():
    try:
        path = filedialog.askdirectory()
        if path == ():
            messagebox.showinfo(title="ERROR",message="No path is selected. Server is stopped.",icon='error')
            print("\n No path is selected\n")
            exit(1)
        if messagebox.askquestion("Warning",f'Are you sure for expose the folder "{path}" to web?',icon='warning') == 'yes':
            return path
        messagebox.showinfo(title="ERROR",message="No path is selected. Server is stopped.",icon='error')
        print("\n No path is selected\n")
        exit(1)
    except Exception as error:
        error_log(error,get_path)
        print("\n No path is selected\n")
        exit(1)

##############################################

### this variable store the sharing folder path that selected by user

sharing_folder_path = get_path()
