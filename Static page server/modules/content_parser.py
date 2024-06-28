import os 
import magic

###########################

### This function is user to log any occur during the process
from modules.error_logger import error_log 
from modules.path_operators import path_validator # this function validate that request for the 
# folder content is allowed to share by deployer of the server
from _paths import _separator # this give the path separator for os ( like for windows \ and for linux /)
    
##############################################

### this function return the file type of the given file to select the icon for it 
### this function is mostly just many if else state so i use google gemini ai to write this function

def get_file_type(filepath):
  """
  Identifies the type of a file using magic.

  Args:
      filepath (str): The path to the file.

  Returns:
      str: The file type (e.g., "image", "video", "document", "text", "code",
          "archive", "spreadsheet", "PDF", "presentation", or "unknown").
  """

  mime = magic.Magic(mime=True)
  file_type = mime.from_file(filepath)

  # Handle common file types with more specific classifications
  if file_type:
    if "image" in file_type:
      return "image"
    elif "video" in file_type:
      return "video"
    elif "document" in file_type:
      if "PDF" in file_type:
        return "PDF"
      elif "Microsoft Word" in file_type or "OpenDocument Text" in file_type:
        return "document"
      else:
        return "other document"  # Handle less common document formats
    elif "text" in file_type:
      return "text"
    elif "script" in file_type:  # Broader script detection
      return "code"
    elif "archive" in file_type:
      return "archive"
    elif "spreadsheet" in file_type:
      return "spreadsheet"
    elif "presentation" in file_type:
      return "presentation"
    else:
      return "other"  # Handle other recognized but less common types

  # File type not recognized by magic
  return "unknown"


##############################################

### this function is list all the folder and file in the given folder path 
### it take folder_path as argument and return list of tuple of 
### folder/file name, type and size of file in string 

def content_of(folder_path:str) -> list[tuple[str,str,str]]:
    try:
        if path_validator(folder_path) is True:
            return []
        content = []
        index = os.listdir(folder_path)
        for i in index:
            size = (os.path.getsize(folder_path+_separator+i))/1024
            if size == 0:
                size_ = '0 B'
            elif size < 200 and size > 0:
                size_ = f'{round(size,3)} KB'
            elif size >= 200 and size < 800*1024:
                size = size/1024
                size_ = f'{round(size,2)} MB'
            else:
                size = size/(1024*1024)
                size_ = f'{round(size,3)} GB'
            if os.path.isdir(folder_path+_separator+i) is True:
                content.append((i,"dir",size_,"folder"))
            else:
                content.append((i,'file',size_,get_file_type(folder_path+_separator+i)))

        return content
    except Exception as error:
        error_log(error,content_of)
        return []
    
#################################################