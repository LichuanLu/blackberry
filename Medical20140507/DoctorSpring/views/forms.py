# coding: utf-8
__author__ = 'Jeremy'
from wtforms import Form, TextField, PasswordField, DateField, IntegerField, SelectField, BooleanField
from wtforms.validators import Required, Email, EqualTo, Length

class RegisterForm(Form):
    name = TextField('Username', validators=[Required(), Length(min=3, max=25)])
    #email = TextField('Email', validators=[Required(), Length(min=6, max=40)])
    password = PasswordField('Password',
                             validators=[Required(), Length(min=6, max=40)])
    # confirm = PasswordField(
    #     'Repeat Password',
    #     [Required(), EqualTo('password', message='Passwords must match')])

class LoginForm(Form):
    name = TextField('username', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    email = TextField('email')
    remember_me = BooleanField('remember_me', default = False)

class DiagnoseForm(Form):
    patientname = TextField('patientname')
    birthdate = TextField('birthdate')
    phonenumber = TextField('phonenumber')
    location = TextField('location')
    patientname = TextField('patientname')
    patientname = TextField('patientname')
    patientname = TextField('patientname')
    patientname = TextField('patientname')

class CommentsForm(Form):
    userId = IntegerField('userId', validators=[Required()])
    receiverId=IntegerField('receiverId', validators=[Required()])
    content = TextField('content', validators=[Required()])
    title = TextField('title')
    diagnoseId=IntegerField('diagnoseId')
class MessageForm(Form):
    senderId = IntegerField('senderId', validators=[Required()])
    receiverId=IntegerField('receiverId', validators=[Required()])
    content = TextField('content', validators=[Required()])
    title = TextField('title')
    type=IntegerField('type', validators=[Required()])

