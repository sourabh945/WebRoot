import os 
import mimetypes
from flask import abort

###########################

### This function is user to log any occur during the process
from modules.error_logger import error_log 
from modules.path_operators import path_validator # this function validate that request for the 
# folder content is allowed to share by deployer of the server
from _paths import _separator # this give the path separator for os ( like for windows \ and for linux /)
    
##############################################

### this function return the file type of the given file to select the icon for it 
### this function is mostly just many if else state so i use google gemini ai to write this function

# Define mappings from MIME types to categories
MIME_TYPE_CATEGORIES = {
    # Text files
    'text/plain': 'Text File',

    # Documents
    'application/msword': 'Document',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'Document',
    'application/vnd.oasis.opendocument.text': 'Document',
    'application/rtf': 'Document',
    'application/x-iwork-pages-sffpages': 'Document',
    'application/x-abiword': 'Document',

    # PDFs
    'application/pdf': 'PDF',

    # Videos
    'video/mp4': 'Video',
    'video/x-msvideo': 'Video',
    'video/mpeg': 'Video',
    'video/quicktime': 'Video',
    'video/x-ms-wmv': 'Video',
    'video/webm': 'Video',
    'video/ogg': 'Video',
    'video/x-flv': 'Video',
    'video/x-matroska': 'Video',

    # Spreadsheets
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'Spreadsheet',
    'application/vnd.ms-excel': 'Spreadsheet',
    'application/vnd.oasis.opendocument.spreadsheet': 'Spreadsheet',
    'application/x-iwork-numbers-sffnumbers': 'Spreadsheet',

    # Presentations
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'Presentation',
    'application/vnd.ms-powerpoint': 'Presentation',
    'application/vnd.oasis.opendocument.presentation': 'Presentation',
    'application/x-iwork-keynote-sffkey': 'Presentation',

    # Zip and compressed files
    'application/zip': 'Zip File',
    'application/x-7z-compressed': 'Zip File',
    'application/x-rar-compressed': 'Zip File',
    'application/x-tar': 'Zip File',
    'application/x-bzip2': 'Zip File',
    'application/gzip': 'Zip File',

    # Images
    'image/jpeg': 'Image',
    'image/png': 'Image',
    'image/gif': 'Image',
    'image/bmp': 'Image',
    'image/tiff': 'Image',
    'image/webp': 'Image',
    'image/svg+xml': 'Image',
    'image/vnd.adobe.photoshop': 'Image',
    'image/x-icon': 'Image',
    'image/x-xbitmap': 'Image',

    # Audio
    'audio/mpeg': 'Audio',
    'audio/wav': 'Audio',
    'audio/x-ms-wma': 'Audio',
    'audio/flac': 'Audio',
    'audio/x-aac': 'Audio',
    'audio/aac': 'Audio',
    'audio/ogg': 'Audio',
    'audio/webm': 'Audio',
    'audio/mp3': 'Audio',
    'audio/x-matroska': 'Audio',
    'audio/x-m4a': 'Audio',

    # Executables and binaries
    'application/x-executable': 'Binary',
    'application/octet-stream': 'Binary',
    'application/x-ms-dos-executable': 'Executable',
    'application/vnd.microsoft.portable-executable': 'Executable',
    'application/x-bat': 'Executable',
    'application/x-elf': 'Executable',
    'application/x-mach-binary': 'Executable',

    # Drawing files
    'application/x-drawing': 'Drawing File',
    'application/x-paintshoppro': 'Drawing File',
    'application/postscript': 'Drawing File',
    'application/vnd.oasis.opendocument.graphics': 'Drawing File',
    'application/x-sketch': 'Drawing File',
    'application/x-cdr': 'Drawing File',

    # Code files
    'application/x-python': 'Code File',
    'text/x-python': 'Code File',
    'text/x-c': 'Code File',
    'text/x-c++': 'Code File',
    'text/javascript': 'Code File',
    'application/javascript': 'Code File',
    'text/x-java-source': 'Code File',
    'application/x-java-archive': 'Code File',
    'application/x-java-jnlp-file': 'Code File',
    'application/x-lua': 'Code File',
    'text/x-lua': 'Code File',
    'application/x-ruby': 'Code File',
    'text/x-ruby': 'Code File',
    'application/x-php': 'Code File',
    'text/x-php': 'Code File',
    'application/x-go': 'Code File',
    'text/x-go': 'Code File',
    'application/x-rust': 'Code File',
    'text/x-rust': 'Code File',
    'application/x-swift': 'Code File',
    'text/x-swift': 'Code File',
    'application/x-kotlin': 'Code File',
    'text/x-kotlin': 'Code File',
    'application/x-typescript': 'Code File',
    'text/x-typescript': 'Code File',

    # Scripts
    'text/x-shellscript': 'Script',
    'application/x-sh': 'Script',
    'application/x-powershell': 'Script',
    'application/x-perl': 'Script',
    'text/x-perl': 'Script',
    'application/x-ruby': 'Script',
    'text/x-ruby': 'Script',
    'application/x-php': 'Script',
    'text/x-php': 'Script',
    'application/x-awk': 'Script',
    'text/x-awk': 'Script',
    'application/x-tcl': 'Script',
    'text/x-tcl': 'Script',
    'application/x-matlab': 'Script',
    'text/x-matlab': 'Script',
    'application/x-r': 'Script',
    'text/x-r': 'Script',
    'application/x-lua': 'Script',
    'text/x-lua': 'Script',
    'application/x-bash': 'Script',
    'text/x-bash': 'Script',
    'application/x-zsh': 'Script',
    'text/x-zsh': 'Script',

    # Web files
    'text/html': 'Web File',
    'application/xhtml+xml': 'Web File',
    'text/css': 'Web File',
    'application/xml': 'Web File',
    'application/rss+xml': 'Web File',
    'application/x-javascript': 'Web File',
    'application/atom+xml': 'Web File',
    'application/json': 'Web File',

    # Data files
    'application/json': 'Data File',
    'application/xml': 'Data File',
    'text/csv': 'Data File',
    'application/x-yaml': 'Data File',
    'application/x-sqlite3': 'Data File',
    'application/vnd.sqlite3': 'Data File',
    'application/x-hdf': 'Data File',
    'application/x-netcdf': 'Data File',
    'application/x-sas': 'Data File',
    'application/x-spss': 'Data File',

    # Database files
    'application/sql': 'Database File',
    'application/vnd.sqlite3': 'Database File',
    'application/x-dbf': 'Database File',
    'application/x-msaccess': 'Database File',
    'application/vnd.ms-access': 'Database File',
    'application/x-sqlite3': 'Database File',

    # Chart files
    'application/vnd.oasis.opendocument.chart': 'Chart File',
    'application/vnd.oasis.opendocument.chart-template': 'Chart File',

    # E-books
    'application/epub+zip': 'E-book',
    'application/x-mobipocket-ebook': 'E-book',
    'application/vnd.amazon.ebook': 'E-book',
    'application/x-fictionbook+xml': 'E-book',

    # Disk images
    'application/x-iso9660-image': 'Disk Image',
    'application/x-virtualbox-vdi': 'Virtual Disk Image',
    'application/x-vhdx': 'Virtual Disk Image',
    'application/x-vmdk': 'Virtual Disk Image',
    'application/x-appliance': 'Virtual Appliance',
    'application/x-apple-diskimage': 'Disk Image',
    'application/x-vhd': 'Virtual Disk Image',

    # Fonts
    'font/ttf': 'Font',
    'font/otf': 'Font',
    'application/font-woff': 'Font',
    'application/font-woff2': 'Font',
    'application/vnd.ms-fontobject': 'Font',

    # Backup files
    'application/x-tar': 'Backup File',
    'application/x-bzip2': 'Backup File',
    'application/x-xz': 'Backup File',

    # Configuration files
    'application/x-config': 'Configuration File',
    'text/x-config': 'Configuration File',
    'application/x-properties': 'Configuration File',
    'text/x-properties': 'Configuration File',

    # Log files
    'text/x-log': 'Log File',

    # Visio files
    'application/vnd.visio': 'Visio File',
    'application/vnd.visio2013': 'Visio File',

    # LaTeX and TeX files
    'application/x-latex': 'LaTeX Document',
    'application/x-tex': 'TeX Document',
    'application/x-bibtex': 'BibTeX File',
    'application/x-texinfo': 'Texinfo Document',

    # CAD files
    'application/vnd.autocad.dwg': 'CAD File',

}


# Define mappings from MIME types to categories
OTHER_MIME_TYPE_CATEGORIES = {
    # Text files
    'text/plain': 'Text File',
    'text/html': 'Text File',
    'application/xhtml+xml': 'Text File',
    'text/css': 'Text File',
    'text/x-php': 'Text File',
    'text/x-python': 'Text File',
    'text/x-shellscript': 'Text File',
    'text/x-perl': 'Text File',
    'text/x-java-source': 'Text File',
    'text/x-csrc': 'Text File',
    'text/x-c++src': 'Text File',
    'text/x-fortran': 'Text File',
    'text/x-go': 'Text File',
    'text/x-pascal': 'Text File',
    'text/x-rust': 'Text File',
    'text/x-swift': 'Text File',
    'text/x-matlab': 'Text File',
    'text/x-r': 'Text File',
    'text/x-sql': 'Text File',
    'text/x-vhdl': 'Text File',
    'text/x-verilog': 'Text File',
    'text/x-yaml': 'Text File',
    'text/x-markdown': 'Text File',

    # Documents
    'application/msword': 'Document',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'Document',
    'application/vnd.oasis.opendocument.text': 'Document',
    'application/rtf': 'Document',
    'application/x-iwork-pages-sffpages': 'Document',

    # PDFs
    'application/pdf': 'PDF',

    # Spreadsheets
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'Spreadsheet',
    'application/vnd.ms-excel': 'Spreadsheet',
    'application/vnd.oasis.opendocument.spreadsheet': 'Spreadsheet',
    'application/x-iwork-numbers-sffnumbers': 'Spreadsheet',

    # Presentations
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'Presentation',
    'application/vnd.ms-powerpoint': 'Presentation',
    'application/vnd.oasis.opendocument.presentation': 'Presentation',
    'application/x-iwork-keynote-sffkey': 'Presentation',

    # Zip and compressed files
    'application/zip': 'Zip File',
    'application/x-7z-compressed': 'Zip File',
    'application/x-rar-compressed': 'Zip File',
    'application/x-tar': 'Zip File',
    'application/x-bzip2': 'Zip File',
    'application/gzip': 'Zip File',

    # Images
    'image/jpeg': 'Image',
    'image/png': 'Image',
    'image/gif': 'Image',
    'image/bmp': 'Image',
    'image/tiff': 'Image',
    'image/webp': 'Image',
    'image/svg+xml': 'Image',
    'image/vnd.adobe.photoshop': 'Image',
    'image/x-icon': 'Image',

    # Audio
    'audio/mpeg': 'Audio',
    'audio/wav': 'Audio',
    'audio/x-ms-wma': 'Audio',
    'audio/flac': 'Audio',
    'audio/x-aac': 'Audio',
    'audio/aac': 'Audio',
    'audio/ogg': 'Audio',
    'audio/webm': 'Audio',
    'audio/mp3': 'Audio',
    'audio/x-m4a': 'Audio',
    'audio/x-wavpack': 'Audio',

    # Executables and binaries
    'application/x-executable': 'Binary',
    'application/octet-stream': 'Binary',
    'application/x-ms-dos-executable': 'Executable',
    'application/vnd.microsoft.portable-executable': 'Executable',
    'application/x-bat': 'Executable',
    'application/x-so': 'Executable',

    # Drawing files
    'application/x-drawing': 'Drawing File',
    'application/x-paintshoppro': 'Drawing File',
    'application/postscript': 'Drawing File',
    'application/vnd.oasis.opendocument.graphics': 'Drawing File',
    'image/x-xcf': 'Drawing File',

    # Code files
    'application/x-python': 'Code File',
    'text/x-python': 'Code File',
    'text/x-c': 'Code File',
    'text/x-c++': 'Code File',
    'text/javascript': 'Code File',
    'application/javascript': 'Code File',
    'text/x-java-source': 'Code File',
    'application/x-java-archive': 'Code File',
    'application/x-java-jnlp-file': 'Code File',
    'text/x-lua': 'Code File',
    'application/x-perl': 'Code File',
    'application/x-php': 'Code File',
    'text/x-ruby': 'Code File',
    'application/x-sh': 'Code File',
    'text/x-tcl': 'Code File',
    'text/x-go': 'Code File',
    'text/x-haskell': 'Code File',
    'text/x-lisp': 'Code File',
    'text/x-objective-c': 'Code File',
    'text/x-scala': 'Code File',
    'text/x-swift': 'Code File',

    # Scripts
    'text/x-shellscript': 'Script',
    'application/x-sh': 'Script',
    'application/x-powershell': 'Script',
    'application/x-perl': 'Script',
    'text/x-perl': 'Script',
    'application/x-ruby': 'Script',
    'text/x-ruby': 'Script',
    'application/x-php': 'Script',
    'application/x-awk': 'Script',
    'text/x-awk': 'Script',
    'application/x-tcl': 'Script',
    'text/x-tcl': 'Script',
    'application/x-matlab': 'Script',
    'application/x-r': 'Script',
    'text/x-r': 'Script',
    'application/x-lua': 'Script',
    'text/x-lua': 'Script',
    'text/x-sql': 'Script',
    'application/x-haml': 'Script',

    # Web files
    'text/html': 'Web File',
    'application/xhtml+xml': 'Web File',
    'text/css': 'Web File',
    'application/xml': 'Web File',
    'application/rss+xml': 'Web File',
    'application/x-javascript': 'Web File',
    'text/x-markdown': 'Web File',
    'text/vcard': 'Web File',

    # Data files
    'application/json': 'Data File',
    'application/xml': 'Data File',
    'text/csv': 'Data File',
    'application/x-yaml': 'Data File',
    'application/x-latex': 'Data File',
    'application/x-tex': 'Data File',
    'application/x-bibtex': 'Data File',
    'application/x-texinfo': 'Data File',
    'text/x-makefile': 'Data File',
    'text/x-pascal': 'Data File',
    'application/x-patch': 'Data File',
    'application/vnd.oasis.opendocument.formula-template': 'Data File',

    # Database files
    'application/sql': 'Database File',
    'application/vnd.sqlite3': 'Database File',
    'application/x-sqlite3': 'Database File',
    'application/x-dbf': 'Database File',
    'application/x-msaccess': 'Database File',
    'application/vnd.ms-access': 'Database File',
    'application/x-sqlite3-relational': 'Database File',
    'application/x-sqlite3-encrypted': 'Database File',
    'application/x-mysql': 'Database File',
    'application/x-mdb': 'Database File',
    'application/x-mdb-compressed': 'Database File',
    'application/x-mdb-modern': 'Database File',
    'application/x-mdb-old': 'Database File',
    'application/x-postgresql': 'Database File',
    'application/x-postgresql-modern': 'Database File',
    'application/x-postgresql-old': 'Database File',

    # Chart files
    'application/vnd.oasis.opendocument.chart': 'Chart File',
    'application/x-icq-chat-log': 'Chart File',
    'application/x-irc-logs': 'Chart File',

    # E-books
    'application/epub+zip': 'E-book',
    'application/x-mobipocket-ebook': 'E-book',
    'application/x-dtbncx+xml': 'E-book',

    # Disk images
    'application/x-iso9660-image': 'Disk Image',
    'application/x-virtualbox-vdi': 'Virtual Disk Image',
    'application/x-vhdx': 'Virtual Disk Image',
    'application/x-vmdk': 'Virtual Disk Image',
    'application/x-appliance': 'Virtual Appliance',
    'application/x-apple-diskimage': 'Disk Image',
    'application/x-red-hat-package-manager': 'Package File',
    'application/x-debian-package': 'Package File',
    'application/x-rpm': 'Package File',
    'application/vnd.apple.keynote': 'Presentation',
    'application/vnd.apple.pages': 'Document',
    'application/vnd.apple.numbers': 'Spreadsheet'
}


def get_file_type(filepath):
  mime,_ = mimetypes.guess_type(filepath)
  if mime is None:
      return 'unknown'
  else:
    if mime in MIME_TYPE_CATEGORIES.keys():
        return MIME_TYPE_CATEGORIES[mime]
    else:
        if mime in OTHER_MIME_TYPE_CATEGORIES.keys():
            return OTHER_MIME_TYPE_CATEGORIES[mime]
        else:
            return 'unknown'

##############################################

### this function is list all the folder and file in the given folder path 
### it take folder_path as argument and return list of tuple of 
### folder/file name, type and size of file in string 

def content_of(folder_path:str) -> list[tuple[str,str,str]]:
    try:
        if path_validator(folder_path) is False:
            abort(403)
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
        abort(403)
    
#################################################