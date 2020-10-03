#Import extensions
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

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
