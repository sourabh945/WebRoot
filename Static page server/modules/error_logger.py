from csv import writer as wr
import os
import sys
import traceback

###################################################

from _paths import _error_log_file_path , _log_folder_path 
 # this contain all the path for program required

####################################################

"""error_log(error:Exception,instance:function)
--------------------------------------------
    error: It is Exception that occur 
    instance: It is the function in which error is occur
    
    It is function that use to write the logs in the error_logs.csv file in logs folder
"""
def error_log(error:Exception,instance):


    # function path retriever for instance
    def func_path(func):
        return f'{func.__code__.co_filename}/{func}' if type(func) == 'function' else f'{func}'
    

    # crete file for error logs if not exists
    try:
        if 'logs' not in os.listdir(_log_folder_path):
            os.mkdir(_log_folder_path+'logs')
            with open(_error_log_file_path,'w') as file:
                file.close()
        else:
            if 'error_logs.csv' not in os.listdir(_log_folder_path+'logs'):
                with open(_error_log_file_path,'w') as file:
                    file.close()
    except:
        print('\n Unable to create logs for the server \n')
        raise Exception
    

    # writing the error the logs in the file and open as append format
    with open(_error_log_file_path,'a') as file:
        writer = wr(file)                               # creating writer object for file
        writer.writerow([error,error.__cause__,func_path(instance)])


    # printing the error on the terminal output of server
    print('\n >>>>>>>>>>>>>>    ERROR   >>>>>>>>>>>>>>>\n')
    print(f'Error: {error}\n Cause: {error.__cause__}\n Function_path: {func_path(instance)}')
    print('\n >>>>>>>>>>>>>>    ERROR   >>>>>>>>>>>>>>>\n')

#####################################################

### This function do exact same as upper function but it is useful in those errors
### which are not defined in the python it just take three arguments error as message
### error-cause and instance 

def other_error_logger(error:str,error_cause:str,instance):


    # function path retriever for instance
    def func_path(func:function):
        return f'{func.__code__.co_filename}/{func}' if type(func) == 'function' else f'{func}'
    

    # crete file for error logs if not exists
    try:
        if 'logs' not in os.listdir(_log_folder_path):
            os.mkdir(_log_folder_path+'logs')
            with open(_error_log_file_path,'w') as file:
                file.close()
        else:
            if 'error_logs.csv' not in os.listdir(_log_folder_path+'logs'):
                with open(_error_log_file_path,'w') as file:
                    file.close()
    except:
        print('\n Unable to create logs for the server \n')
        raise Exception
    

    # writing the error the logs in the file and open as append format
    with open("./logs/error_logs.csv",'a') as file:
        writer = wr(file)                               # creating writer object for file
        writer.writerow([error,error_cause,func_path(instance)])


    # printing the error on the terminal output of server
    print('\n >>>>>>>>>>>>>>    ERROR   >>>>>>>>>>>>>>>\n')
    print(f'Error: {error}\n Cause: {error_cause}\n Function_path: {func_path(instance)}')
    print('\n >>>>>>>>>>>>>>    ERROR   >>>>>>>>>>>>>>>\n')   