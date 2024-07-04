### This program is use to install and configure all the server for use it 
### it make all required files for logs and database of user credentials 
### all define the pre-required things to run the system

import os
import json


_separator = os.sep

lines = []

print("Start installation and configuration")

### installing the all packages for the server

if os.system("pip3 install flask") != 0 and os.system("pip3 install tk") != 0:
    print("\nThere is problem to install the packages try to comment it and install manually.\n")
    exit(1)

from tkinter import filedialog,messagebox

messagebox.showinfo(title="Selection of folder",message="Select the folder where the logs folder , certificates for https connection and database folder should be created.")

folder_path = filedialog.askdirectory()

items = set(os.listdir(folder_path))

lines.append(f'_log_folder_path = "{folder_path}"\n')

if "logs" not in items:
    os.mkdir(folder_path+_separator+"logs")
with open(folder_path+_separator+"logs"+_separator+"error_logs.csv","w") as file:
    file.close()
with open(folder_path+_separator+"logs"+_separator+"download_logs.csv","w") as file:
    file.close()
with open(folder_path+_separator+"logs"+_separator+"user_logs.csv","w") as file:
    file.close()

lines.append(f'_error_log_file_path = "{folder_path+_separator+"logs"+_separator+"error_logs.csv"}"')
lines.append(f'_error_log_file_path = "{folder_path+_separator+"logs"+_separator+"user_logs.csv"}"')
lines.append(f'_error_log_file_path = "{folder_path+_separator+"logs"+_separator+"download_logs.csv"}"')

user_cred = dict()

print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

num_users = int(input("Enter the number user you wanted to define : "))
for i in range(0,num_users):
    username = input(f"Enter the username for user number {i} : ")
    password = input(f"Enter the password for user number {i} : ")
    user_cred[username] = password

if "database" not in items:
    os.mkdir(folder_path+_separator+"database")
with open(folder_path+_separator+"database"+_separator+"user_credentials.json","w") as file:
    json.dump(user_cred,file)
    file.close()

lines.append(f'_user_login_credential_path = "{folder_path+_separator+"database"+_separator+"user_credentials.json"}"')


print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

if input("Do you wanted https / encryption for website : ").lower() in {'yes','yah','y','sure',"why n't",'why not'}:
    print("You say yes for encryption / https for website")
    print("Print we have to make the certificate for that and you can also buy from any certifier.\n")
    print("NOTE: For certificate making we need you to fill some information into it and please fill it correctly.\n")
    if "certificates" not in items:
        os.mkdir(folder_path+_separator+"certificates")
    os.chdir(folder_path+_separator+"certificates"+_separator)
    if os.system("openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365") != 0 :
        print("\n Unable to generate certificate, please do it manually according to your os.")

print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

with open("_paths.py","w") as file:
    file.writelines(lines)
    file.close()