from flask import Flask, render_template, Response, request
from flask import send_from_directory, send_file, jsonify
import os, sys
import re
import random
import json
from flask_login import LoginManager, login_user, login_required
from flask_login import logout_user, UserMixin, current_user

from database import sql_db
from common import *

# ngl this webapp routes sql queries like old people fuck
# this entire codebase is giving me a goddamn migrane
global login_man

global success
global failure
global gender

global app
global db

global user_path

success = "Wassaaaa"
failure = "Fogedaaabout it"

class User(UserMixin):
    def __init__(self, id):
        self.client_id = id

gender = {"option1": "Male (Drive(2011)Ryan gosling)",
          "option2": "Female (born male but undervent botched circumcision)",
          "option3": "Female (ReactJS/rust programmer)",
          "option4": "ESP32-D0WDR2-V3 microcontroller",
          "option5": "Kovjoki bögsned"
    }

app = Flask(__name__)
app.secret_key = "balls_hahahahahahahahhahahahaha0x12385ad7gadg6adsd57f7asd56d8asd"

login_man = LoginManager(app)
login_man.login_view = "usr_login"

db = sql_db (
    "localhost", 
    "root",
    "")

user_path = r"/home/rot/Desktop/site/user_content/user/"

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/templates/<path:file_path>")
def src_file(file_path):
    src_path = "/home/rot/Desktop/site/templates/"
    return send_file(src_path + file_path, mimetype="text/html")

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@login_man.user_loader
def load_usr(user_id):
    db.exec(f"SELECT * FROM user_content WHERE id = '{user_id}'")
    buffer = db.fetch()
    if buffer:
        usr = User(buffer[0])
        usr.id = buffer[0]
        return usr

    return None 

@app.route("/api/login", methods=["POST"])
def usr_login():
    username = request.form.get("username")
    password = request.form.get("password")

    db.exec(f"SELECT * FROM user_content WHERE username = '{username}';")
    res = db.fetch()
    if (res):
        if (password == res[3]):
            usr = User(res[0])
            usr.id= res[0]
            login_user(usr, remember=True)

            return success

    return failure

@app.route("/api/logout", methods = ["POST"])
@login_required
def logout_usr():
    logout_user() #flask_login library handles cookies, requests, etc
    return success

#@app.route("/style/<path:filename>")
#def css_route(filename):
#    css_fldr = os.path.join(app.root_path, "static", "style")
#    print("path: \n" + css_fldr)
#    #css_fldr = "/home/rot/Desktop/site/static/style"
#    return send_from_directory(css_fldr, filename, mimetype="text/css")

@app.route("/api/content_preview", methods=["GET"])
def api_fetch_preview():
    img = "static/res/sq.jpeg"
    print(request.args.get("offset"), '\n')
    return send_file(img, mimetype="image/jpeg")


@app.route("/api/content_fetch")
def api_fetch_content():
    pass

#verify login authenticity, cookies, etc
@app.route("/api/post", methods=["POST"])
@login_required
def api_write_content():
    client_id = current_user.client_id
    print(f"Incoming packet from user_id: {client_id}")

    db.exec("SELECT * FROM post_content ORDER BY id DESC LIMIT 1")
    content_id = (db.fetch()[0] +1)
    content_folder = user_path + str(client_id) + "/" + str(content_id) + "/" 
    f_mkdir(content_folder)    
    
    tmp = request.form.get("ingrediants_list")
    cli_ingrediants = json.loads(tmp)
    cil_description = request.form.get("description")
    cli_name = request.form.get("name")
    
    cli_img = request.files["file_input"]


    for key, value in request.form.items():
        print(f"{key}: {value}")

    if cli_name:
        print("saved_video")
        cli_img.save(content_folder + cli_img.filename)

    #img_file.save(content_folder + "thumbnail.jpg")
    f_write_arr(cli_ingrediants, content_folder + "ingrediants_list.txt") 
    f_write_src(cil_description, content_folder + "description.txt")
    db.exec(f"insert into post_content (user_id, name, content_path) values('{client_id}', '{cli_name}', '{content_folder}');")
    db.com()

    #test
    #db.exec(f'insert into content values("test", "descr", "path", 123, 321, 1);')
    return success

@app.route("/api/register", methods=["POST"])
def api_user_register():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    genders = request.form.get("dropdown")

    # yes out of all of the options i chose the shittiest one
    query = f"SELECT COUNT(*) FROM user_content WHERE username = '{username}';"
    db.exec(query)
    if (db.fetch()[0] == 0):
        query = f"SELECT COUNT(*) FROM user_content WHERE email = '{email}';"
        db.exec(query)
        if (db.fetch()[0] == 0):
            db.exec(f"INSERT INTO user_content (username, email, password, gender) VALUES('{username}', '{email}', '{password}', '{gender[genders]}');")   
            db.com()    
    
            db.exec(f"SELECT id FROM user_content WHERE email = '{email}';")
            path_id = db.fetch()[0]
            print(path_id)
            f_mkdir(user_path + str(path_id))

            return success

    return failure  

@app.route("/res/<path:video_path>")
def get_file(video_path):

    print("ROUTE ROUTE")

    vid_path = "/home/rot/Desktop/site/static/"

    filename = os.path.join(vid_path + video_path)
    print(filename)
    filesize = os.path.getsize(filename)
    range_header = request.headers.get('Range', None)

    if range_header:
        byte1, byte2 = None, None
        match = re.search(r'(\d+)-(\d*)', range_header)
        groups = match.groups()

        if groups[0]:
            byte1 = int(groups[0])
        if groups[1]:
            byte2 = int(groups[1])

        if not byte2:
            byte2 = byte1 + 1024 * 1024
            if byte2 > filesize:
                byte2 = filesize

        length = byte2 + 1 - byte1

        resp = Response(
            get_chunk(filename, byte1, byte2),
            status=206,
            mimetype='video/mp4',
            content_type='video/mp4',
            direct_passthrough=True
        )

        resp.headers.add('Content-Range',
                         'bytes {0}-{1}/{2}'
                         .format(byte1, length, filesize))
        return resp

    return Response(
        get_chunk(filename),
        status=200,
        mimetype='video/mp4'
    )

@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response

def get_chunk(filename, byte1=None, byte2=None):
    filesize = os.path.getsize(filename)
    yielded = 0
    yield_size = 1024 * 1024

    if byte1 is not None:
        if not byte2:
            byte2 = filesize
        yielded = byte1
        filesize = byte2

    with open(filename, 'rb') as f:
        f.seek(yielded)
        while True:
            chunk = f.read(yield_size)
            if not chunk:
                break
            yielded += len(chunk)
            yield chunk

if __name__ == "__main__":
    # flask i/o operations executes non-blockingly on another thread
    app.run(host="0.0.0.0", port=9001)
