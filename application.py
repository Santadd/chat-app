from flask import Flask, render_template, redirect, url_for
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
@app.route("/", methods=['GET', 'POST'])
def index():
    #Instantiate the Registration form
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        #Obtain the username and password the user enters
        username = reg_form.username.data
        password = reg_form.password.data

        #Updated Database if validation is successful  
        #If user object has not been taken
        #Add user to the DB
        #Create a user object to add the username to the database
        user = User(username=username, password=password)
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
        return "Logged in successfully"

    #If user uses the GET method to access the login
    return render_template("login.html", form=login_form)



if __name__ == "__main__":
    app.run(debug=True)