from flask import Flask , request , redirect , render_template , abort

app = Flask(__name__,template_folder='./Templates')

app.config['SESSION_PERMANENT'] = False

########################## modules imports ###############################

from modules.authentication import authenticate_user_cred
from modules.user import user

### changing the http to https ############################################

@app.before_request
def before_request():
    if request.url.startswith("http://"):
        return redirect(request.url.replace('http://','https://',1)) , 304
    
### webpages for the app ##################################################

###### index page #########################

@app.route("/")
def index_page():
    return redirect("/login")

###### login page ##########################

@app.route('/login',methods=['GET','POST'])
def login():

    if request.method == "GET":
        return render_template('login_page/index.html',login='True')
    
    elif request.method == "POST":

        try:
            username = request.form.get['username']
            password = request.form.get['pass']
            ip_address = request.remote_addr
        except:
            abort(400)

        if authenticate_user_cred(username,password) is True:
            user = user(username,ip_address)
