import os
from time import localtime, strftime
from flask import Flask, render_template, redirect, url_for, flash
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room
#Import the contents of model.py
from models import *
from wtforms_fields import *

#Configure app

#Create an Instance of the flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET')

#Configure the database
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL') 
#Initialise the connection to our database
db = SQLAlchemy(app)
#Initialize Flask-SocketIO
socketio = SocketIO(app)
#Pre-define rooms
ROOMS = ["lounge", "news", "games", "coding"]
#Configure Flask Login
login = LoginManager(app)
login.init_app(app)

#Load specific users
@login.user_loader
def load_user(id):
    #Get a user object from the Database
    return User.query.get(int(id))
    #Login User


@app.route("/", methods=['GET', 'POST'])
def index():
    #Instantiate the Registration form
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        #Obtain the username and password the user enters
        username = reg_form.username.data
        password = reg_form.password.data
        #Hash password
        hashed_pswd = pbkdf2_sha256.hash(password)
        #Update Database if validation is successful  
        #If user object has not been taken
        #Add user to the DB
        #Create a user object to add the username to the database
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        #Display flash message for succesful login
        flash("Registered successfully. Please Login", 'success')
        #If Registration is successful, return user to the login page
        return redirect(url_for("login"))
    return render_template("index.html", form=reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    #Allow user to login if there are no validation errors
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)       
        return redirect(url_for('chat'))
        
    #If user uses the GET method to access the login
    return render_template("login.html", form=login_form)

#Accessible by logging in only
@app.route("/chat", methods=['GET', 'POST'])
#@login_required
def chat():

    return render_template("chat.html", username=current_user.username, rooms=ROOMS)

#Route to logout User
@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    flash("You have successfully logout", 'success')
    return redirect(url_for('login'))

#Define event packages
@socketio.on('message')
def message(data):
    #Broadcast message to other clients
    print(f"\n\n{data}\n\n") 
    send({'msg': data['msg'], 'username': data['username'], 'time_stamp': 
         strftime('%b-%d %I:%M%p', localtime())}, room=data['room'])
    #emit('some-event', 'this is a custom event message')

#Join room route
@socketio.on('join')
def join(data):

    join_room(data['room'])
    #Notify clients when one joins the room
    send({'msg': data['username'] + " has joined the " + data['room'] + " room."}, room=data['room'])

@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'msg': data['username'] + "has left the " + data['room'] + " room."}, room=data['room'])

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run()

