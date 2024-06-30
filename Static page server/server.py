######################## Flask configuration ###########################

from flask import Flask , request , redirect , render_template , send_file , url_for ,abort

##########

app = Flask(__name__,template_folder="Templates")
app.config["SESSION_PERMANENT"] = False

######################################################################


#####################################################################

from modules.folder_selector import sharing_folder_path # this prompt for select path of sharing folder 

######################## modules imports ############################

from modules._downloads_logger import downloads_logger
from modules.content_parser import content_of
from modules.decorators import pre_authentication , pre_authentication_download
from modules.error_logger import error_log
from modules.login_operators import authenticate_user
from modules.parser_keys import key
from modules.path_operators import path_validator, path_separator,parent_path
from modules.user import users_module

######################  _paths imports  ######################################

from _paths import _separator

###################### Web pages of app ##############################

@app.route("/")  ### Home page is redirect to the login page
def home():
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
            return redirect(url_for('.post_index',parser_key=parser_key))
        else:
            return render_template("login form/index.html",login='False')
    return render_template("login form/index.html",login='True')

### error pages

@app.errorhandler(401)
def authentication_error(error):
    return render_template("error page/401.html"), 401

@app.errorhandler(404)
def not_found_error(error):
    return render_template("error page/404.html"), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template("error page/500.html"), 500

@app.errorhandler(400)
def bad_request(error):
    return render_template("error page/400.html"), 400

#### file Explorer page : heart of web app ###########################################

### this web page hold all the info and show the content of the folder 


@app.route("/file_expo",methods=["GET","POST"])
@pre_authentication
def post_index(user:users_module.user,folder_path:str):
    if request.method == "POST":
        try:
            item_type = request.form.get("item_type")
            item_name = request.form.get("item_name")
            parent_folder = request.form.get("parent_folder")
        except Exception as error:
            error_log(error,post_index)
            return abort(400)
        if item_type == "dir":
            return redirect(url_for('.post_index',parser_key=key(user,folder_path+_separator+item_name)))
        elif item_type == "file":
            return redirect(url_for('.download',parser_key=key(user,folder_path+_separator+item_name)))
        elif item_type == "up_dir":
            if path_validator(parent_path(parent_folder)) is True:
                return redirect(url_for('.post_index',parser_key=key(user,parent_path(parent_folder))))
            else:
                return render_template("error page/403.html",secret=key(user,parent_folder),user=user), 403
        elif item_type == "refresh":
            return redirect(url_for('.post_index',parser_key=key(user,parent_folder)))
        elif item_type == "upload":
            pass
        else:
            abort(400)
    elif request.method == "GET":
        parser_key = key(user,folder_path)
        return render_template("share page/index.html",content=content_of(folder_path),
                           username=user.username,session_id=user.session_id,
                           parent_folder=folder_path,secret=parser_key)


@app.get("/download")
@pre_authentication_download
def download(user:users_module.user,file_path:str):
    try:
        folder_path,filename = path_separator(file_path)
        downloads_logger(user,file_path)
        return send_file(file_path,as_attachment=True,download_name=filename,)
        
        # return redirect(url_for(".post_index",parser_key=key(user,folder_path)))
    except Exception as error:
        error_log(error,download)
        return abort(500)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,threaded=True)
    pass