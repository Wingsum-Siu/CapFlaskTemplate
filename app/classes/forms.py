# This file is where data entry forms are created. Forms are placed on templates 
# and users fill them out.  Each form is an instance of a class. Forms are managed by the 
# Flask-WTForms library.

from email.mime import image
from flask.app import Flask
from flask import flash
from flask_wtf import FlaskForm
from mongoengine.fields import EmailField
import mongoengine.errors
from wtforms.validators import URL, NumberRange, Email, Optional, InputRequired, ValidationError, DataRequired, EqualTo
from wtforms import PasswordField, StringField, SubmitField, TextAreaField, HiddenField, IntegerField, SelectField, FileField, BooleanField
from app.classes.data import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me?')
    submit = SubmitField()

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])  
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        try:
            User.objects.get(username=username.data)
        except mongoengine.errors.DoesNotExist:
            flash(f"{username.data} is available.")
        else:
            raise ValidationError('This username is taken.')

    def validate_email(self, email):
        try:
            User.objects.get(email=email.data)
        except mongoengine.errors.DoesNotExist:
            flash(f'{email.data} is a unique email address.')
        else:
            raise ValidationError('This email address is already in use. if you have forgotten your credentials you can try to recover your account.')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class ProfileForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()]) 
    image = FileField("Image") 
    submit = SubmitField('Post')
    role = SelectField('Role',choices=[("Teacher","Teacher"),("Student","Student")])
    favcolor = SelectField('Favorite Color',choices=[("Red","Red"),("Orange","Orange"),("Yellow","Yellow"),("Green","Green"),("Blue","Blue"),("Purple","Purple"),("Black","Black"),("White","White")])

class PostForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Post', validators=[DataRequired()])
    userfeeling = SelectField('How are you feeling today?',choices=[("Great","Great"),("Alright","Alright"),("A little down","A little down"),("Sad","Sad"),("Angry","Angry"),("Excited","Excited")])
    anonymous = SelectField('Name on Post?',choices=[("Username","Username"),("Anonymous","Anonymous")])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')

class EntryForm(FlaskForm):
    adjective = StringField('Adjective (to describe yourself)', validators=[DataRequired()])
    entrycontent = TextAreaField('Entry', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AdviceForm(FlaskForm):
    content = TextAreaField('Advice', validators=[DataRequired()])
    image = FileField('Image')
    advicetype = SelectField('Which of the following best describes your advice?',choices=[("Tips","Tips"),("Motivational","Motivational"),("Other","Other")], validators=[DataRequired()])
    colorbg = SelectField('Background Color of Your Post',choices=[("Red","Red"),("Orange","Orange"),("Yellow","Yellow"),("Green","Green"),("Blue","Blue"),("Purple","Purple")])
    submit = SubmitField('Post')