#Import extensions
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256
from models import User

#Define the invalid_credentials() function
#form parameter indicates where we are caling the function from-LoginForm
#field parameter indicates the field the function is called from
def invalid_credentials(form, field):
    """This function checks for a valid username and password of the ogin form"""

    #Get the values the user has entered in the form
    username_entered = form.username.data
    password_entered = field.data

    #Check if credentials are valid
    user_object = User.query.filter_by(username=username_entered).first()   
    if user_object is None:
        raise ValidationError("Username or Password Incorrect")
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Username or password incorrect")
#Define the form
class RegistrationForm(FlaskForm):
    """ Registration Form """

    username = StringField('username_label', validators=[InputRequired(message="Username Required"),
                            Length(min=4, max=25, message="Username must be between 4 and 25 characters")])

    password = PasswordField('password_label', validators=[InputRequired(message="Password Required"),
                            Length(min=4, max=25, message="Password must be between 4 and 25 characters")])

    confirm_pswd = PasswordField('confirm_pswd_label', validators=[InputRequired(message="Username Required"),
                            EqualTo("password", message="Password must match")])

    submit_button = SubmitField('Create')

    #Create a function to customise validation
    def validate_username(self, username):
        #Query database to see if user already exist
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exits. Select a different username.")

class LoginForm(FlaskForm):
    """ Login Form """

    username = StringField('username_label', validators=[InputRequired(message="Username Required")])

    password = PasswordField('password_label', validators=[InputRequired(message="Password Required"),
         invalid_credentials])

    submit_button = SubmitField('Login')
    