from django.forms import Form, CharField, PasswordInput, FileField

from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

class UploadFileForm(Form):
    file = FileField()
    input_lang = CharField(max_length=50)
    output_lang = CharField(max_length=50)

class RegistrationForm(Form):
    username = CharField(max_length=50)
    name = CharField(max_length=50)
    password = CharField(max_length=50)
    mobile = CharField(max_length=50)

class LoginForm(Form):
    username = CharField(max_length=100)
    password = CharField(widget=PasswordInput())

class CommentForm(Form):
    comment = CharField(max_length=3000)