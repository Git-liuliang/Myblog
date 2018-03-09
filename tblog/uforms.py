from django.forms import Form
from django.forms import widgets  # 插件
from django.forms import fields
from django import forms

class regFrom(Form):
    user = forms.CharField(min_length=4,
                           widget=widgets.TextInput(attrs={"class": "form-control"})
                           )
    pwd = forms.CharField(
        widget=widgets.PasswordInput(attrs={"class": "form-control"})
    )
    repeat_pwd = forms.CharField(
        widget=widgets.PasswordInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        widget=widgets.EmailInput(attrs={"class": "form-control"})
    )