from django.db import models
from django import forms
from django.forms import ModelForm
from django.core.validators import validate_email
from django.core.validators import email_re
from django.core.exceptions import ValidationError

CHOICES1=[('vBox','VirtualBox'),
    ('euca', 'Eucaylptus'),
    ('ec2', 'Amazon EC2')]

CHOICES2=[('cluster','Cluster'),
         ('cloud','Cloud')]


class CommonFields(forms.Form):
    deploy_option1 = forms.ChoiceField(choices=CHOICES1)

    deploy_option2 = forms.ChoiceField(choices=CHOICES2)

    admin_email = forms.EmailField(validators=[validate_email], max_length=40,
    required=True, widget=forms.TextInput(attrs={'id':'email', 'data-type':'email', 'name':"email",
    'data-trigger':"change", 'data-required':"true"}))

    admin_pass = forms.CharField(widget=forms.PasswordInput(render_value=False,
    attrs={'id':'admin_pass', 'name':"admin_pass", 'data-trigger':"change", 'data-required':"true"}),
    label=("Admin Password"), min_length=6, required=True, )

    pass_confirm = forms.CharField(widget=forms.PasswordInput(render_value=False,
    attrs={'id':'pass_confirm', 'name':"pass_confirm", 'data-trigger':"change", 'data-required':"true"}),
    label=("Confirm Password"), min_length=6, required=True)

    keyname = forms.CharField(min_length=4, max_length=24, required=True,
    widget=forms.TextInput(attrs={'id':'keyname', 'name':"keyname",
    'data-trigger':"change", 'data-required':"true"}))

    ips_yaml = forms.CharField(label=("ips.yaml"), max_length=120,
    widget=forms.Textarea(attrs={'id':'ips_yaml', 'name':"ips",'data-trigger':"change",
    'data-required':"true"}), required=True)


class ec2(forms.Form):
    ec2_key = forms.CharField(label=("Amazon EC2 Key"), required=True)
    ec2_secret = forms.CharField(label=("Amazon EC2 Secret"), required=True)

class euca(forms.Form):
    ec2_key = forms.CharField(label=("Amazon EC2 Key"), required=True)
    ec2_secret = forms.CharField(label=("Amazon EC2 Secret"), required=True)

