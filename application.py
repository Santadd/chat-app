from flask import Flask, render_template, redirect, url_for
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
#Import the contents of model.py
from models import *
from wtforms_fields import *

#Configure app

#Create an Instance of the flask app
app = Flask(__name__)
app.secret_key = 'replace later'

#Configure the database
app.config['SQLALCHEMY_DATABASE_URI']= 'postgres://ffozzwshelgnck:f9e6a811c7287008929cecde47b04b206a4abf71f4b093418648fa5ac5cfef68@ec2-52-204-20-42.compute-1.amazonaws.com:5432/deellvnshen1t3'
#Initialise the connection to our database
db = SQLAlchemy(app)

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
        #Updated Database if validation is successful  
        #If user object has not been taken
        #Add user to the DB
        #Create a user object to add the username to the database
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

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
@login_required
def chat():

    return "Chat with me"

#Route to logout User
@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return "Logged out using flask-login"


if __name__ == "__main__":
    app.run(debug=True)