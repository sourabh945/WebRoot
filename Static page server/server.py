######################## Flask configuration ###########################

from flask import Flask , request , redirect , render_template , send_file , url_for

##########

app = Flask(__name__,template_folder="Templates")
app.config["SESSION_PERMANENT"] = False

#####################################################################

from modules.folder_selector import sharing_folder_path # this prompt for select path of sharing folder 

######################## modules imports ############################

from modules._downloads_logger import downloads_logger
from modules.content_parser import content_of
from modules.error_logger import error_log
from modules.login_operators import authenticate_user
from modules.parser_keys import key , new_key , authenticate_key , open_parser
from modules.path_operators import *
from modules.user import users_module

######################################################################

####################### decorators ###################################

from functools import wraps

def request_checker(func):
    @wraps(func)
    def wrapper():
        try:
            parser_key = request.args['parser_key']
        except:
            return redirect("/login")
        if authenticate_key(parser_key) is True:
            user, file_path = open_parser(parser_key)

###################### Web pages of app ##############################

@app.route("/")  ### Home page is redirect to the login page
def index():
    return redirect("/login") 

### login page

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        try:
            username = request.form.get("username")
            password = request.form.get("pass")
            ip_address = request.remote_addr
        except:
            return redirect("/login")
        if authenticate_user(username,password) is True:
            user = users_module.user(username,ip_address)
            parser_key = key(user,sharing_folder_path)
            return redirect(url_for('.file_explorer',parser_key=parser_key))
        else:
            return render_template("login form/index.html",login='False')
    return render_template("login form/index.html",login='True')

### error page

