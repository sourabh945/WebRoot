from csv import writer as wr
import os
import sys
import traceback

'''
error_log(error:Exception,instance:function)
------
error: It is Exception that occur 
instance: It is the function in which error is occur
------
It is function that use to write the logs in the error_logs.csv file in logs folder
'''
def error_log(error:Exception,instance:function):


    # function path retriever for instance
    def func_path(func:function):
        return f'{func.__code__.co_filename}/{func}' if type(func) == 'function' else f'{func}'
    

    # crete file for error logs if not exists
    try:
        if 'logs' not in os.listdir('./'):
            os.mkdir('logs')
            with open("./logs/error_logs.csv",'w') as file:
                file.close()
        else:
            if 'error_logs.csv' not in os.listdir('./logs'):
                with open("./logs/error_logs.csv",'w') as file:
                    file.close()
    except:
        print('\n Unable to create logs for the server \n')
        raise Exception
    

    # writing the error the logs in the file and open as append format
    with open("./logs/error_logs.csv",'a') as file:
        writer = wr(file)                               # creating writer object for file
        writer.writerow([error,error.__cause__,func_path(instance)])


    # printing the error on the terminal output of server
    print('\n >>>>>>>>>>>>>>    ERROR   >>>>>>>>>>>>>>>\n')
    print(f'Error: {error}\n Cause: {error.__cause__}\n Function_path: {func_path(instance)}')
    print('\n >>>>>>>>>>>>>>    ERROR   >>>>>>>>>>>>>>>\n')