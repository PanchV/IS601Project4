

from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *


class login_form(FlaskForm):
    email = EmailField('Email Address', [
        validators.DataRequired(),
    ])

    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.length(min=6, max=35)
    ])
    submit = SubmitField()


class register_form(FlaskForm):
    email = EmailField('Email Address', [
        validators.DataRequired(),

    ], description="You need to signup with an email")

    password = PasswordField('Create Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),

    ], description="Create a password ")
    confirm = PasswordField('Repeat Password', description="Please retype your password to confirm it is correct")
    submit = SubmitField()


class profile_form(FlaskForm):

    about = TextAreaField('About', [validators.length(min=6, max=300)],
                          description="Please add information about yourself")
    hobbies = TextAreaField('Hobbies', [validators.length(min=6, max=300)],
                          description="Please add information about your hobbies")
    education = TextAreaField('Education', [validators.length(min=6, max=300)],
                          description="Please add information about your education")
    skills = TextAreaField('Skills', [validators.length(min=6, max=300)],
                          description="Please add information about your skills")
    submit = SubmitField()

class user_edit_form(FlaskForm):
    about = TextAreaField('About', [validators.length(min=0, max=300)],
                          description="You may edit About information the user as an Admin")
    hobbies = TextAreaField('Hobbies', [validators.length(min=0, max=300)],
                            description="You may edit Hobbies information the user as an Admin")
    education = TextAreaField('Education', [validators.length(min=0, max=300)],
                              description="You may edit Education information the user as an Admin")
    skills = TextAreaField('Skills', [validators.length(min=0, max=300)],
                           description="You may edit Skills information the user as an Admin")
    is_admin = BooleanField('Admin', render_kw={'value':'1'})
    submit = SubmitField()


class security_form(FlaskForm):
    email = EmailField('Email Address', [
        validators.DataRequired(),

    ], description="You can change your email address")

    password = PasswordField('Create Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),

    ], description="Create a password ")
    confirm = PasswordField('Repeat Password', description="Please retype your password to confirm it is correct")

    submit = SubmitField()

class csv_upload(FlaskForm):
    file = FileField()
    submit = SubmitField()