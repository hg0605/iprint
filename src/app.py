import sys
sys.path.append("/home/ubuntu/iprint/")


from flask import Flask, render_template, request, session, jsonify
import json
import socket

from subprocess import call, Popen
from werkzeug.utils import secure_filename

from src.common.database import Database
from src.models.user import User

app=Flask(__name__)
app.secret_key="harsh"

@app.route('/')
def hello_method():
    return render_template('home.html')

@app.route('/login')
def login_method():
    return render_template('login.html')

@app.route('/register')
def register_method():
    return render_template('register.html')

@app.route('/printdoc')
def print_method():
    return render_template('uploadfile.html')

@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/tester',methods=['POST'])
def test_method():
    email=request.form['email']
    print(email)
    user=User.get_by_email(email)
    print (user.json())
    k=user.json()
    k['_id']=str(k['_id'])
    return jsonify({"status":k['printdata']})

@app.route('/testerupdate',methods=['POST'])
def tester_method():

    email=request.form['email']
    print(email)
    user=User.get_by_email(email)
    Database.update("users",{"email":email},{"printdata":"no"})
    return "done"

@app.route('/auth/login',methods=['POST'])
def login_user():
    email=request.form['email']
    password=request.form['password']


    if User.login_valid(email,password):
        User.login(email)
    else:
        session['email']=None
        print('Wrong Details')
        return render_template("login.html",email=session['email'])

    return render_template("choice.html",email=session['email'])

@app.route('/uploadfile')
def file_method():
    return render_template('uploadfile.html')

@app.route('/uploadfileemail')
def fileemail_method():
    return render_template('uploadfileemail.html')

@app.route('/auth/loginapp',methods=['POST'])
def login_userapp():
    email=request.form['email']
    password=request.form['password']


    if User.login_valid(email,password):
        User.login(email)
        print('Correct Details')
    else:
        session['email']=None
        print('Wrong Details')


    return jsonify({"status":"success"})

@app.route('/auth/register',methods=['POST'])
def register_user():
    email=request.form['email']
    password=request.form['password']

    User.register(email,password)

    return render_template("profile.html",email=session['email'])




@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['document']
        f.save('uploads/' + secure_filename(f.filename))
        Database.update("users",{"email":session['email']},{"printdata":"yes"})
        str="server.py"
        str1="uploads/"+f.filename
        print(str1)
        Popen(["nohup","python",str,str1,f.filename])

    return render_template("home.html")

@app.route('/uploademail', methods=['GET', 'POST'])
def uploader_file():
    if request.method == 'POST':
        f = request.files['image']
        email=request.form['email']
        f.save('uploads/' + secure_filename(f.filename))
        Database.update("users",{"email":email},{"printdata":"yes"})
        str="server.py"
        str1="uploads/"+f.filename
        print(str1)
        Popen(["nohup","python",str,str1,f.filename])

    return jsonify({"status":"success"})

@app.route('/uploademailfile', methods=['GET', 'POST'])
def uploader1_file():
    if request.method == 'POST':
        f = request.files['image']
        email=request.form['email']
        f.save('uploads/' + secure_filename(f.filename))
        Database.update("users",{"email":email},{"printdata":"yes"})
        str="server.py"
        str1="uploads/"+f.filename
        print(str1)
        Popen(["nohup","python",str,str1,f.filename])

    return render_template("home.html")


@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    if user_id is not None:

        user=User.get_by_id(user_id)

    else:
        user=User.get_by_email(session['email'])

    blogs=user.get_blogs()

    return render_template("user_blogs.html",blogs=blogs,email=user.email)


if __name__=='__main__':
    app.run(host="0.0.0.0",debug=True)
