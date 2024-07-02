from flask import jsonify , Flask , request

var_app = Flask(__name__)

shared_dict = {'parser':{},'logged_user':{},'session_ids':set()}

@var_app.route('\variable',method=['GET'])
def get_variable():
    holder = request.