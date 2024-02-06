from django import forms
from django.forms import ModelForm
from .models import UserBasic, Task
from django.contrib.auth.models import User
from datetime import date, timedelta

# class UserModelForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ["username", "password", "email"]

class UserBasicModelForm(ModelForm):
    class Meta:
        model = UserBasic
        fields = ["username", "password"]

        widgets = {
            "username":  forms.TextInput(attrs={'placeholder':'Enter your name','autocomplete': 'off'}), 
            "password": forms.PasswordInput(attrs={'placeholder':'','autocomplete': 'off','data-toggle':'password'})}

class TaskModelForm(ModelForm):
    class Meta:
        model = Task
        fields = ["category", "description", "dueDate", "notes", "status", "users", "dateCreated"]

        widgets = {
            "category": forms.TextInput(attrs={"placeholder":"'Financial'"}),
            "description": forms.TextInput(attrs={"placeholder":"'Call the Bank'"}),
            "dueDate": forms.TextInput(attrs={"value":f"{date.today() + timedelta(days=7)}"}),
            "notes": forms.TextInput(attrs={"placeholder":"'Ask for Shirley'"}),
            "dateCreated": forms.TextInput(attrs={"value":f"{date.today()}", "hidden":"true"}),
            "status": forms.Select()
        }

        labels = {
            "dateCreated": "",
            "dueDate": "Complete By"
        }