from django.db import models
from django import forms
from django.forms import ModelForm
from django.core.validators import validate_email
from django.core.validators import email_re
from django.core.exceptions import ValidationError

INFRAS=[
    ('euca', 'Eucaylptus'),
    ('ec2', 'Amazon EC2')]

CLUSTER=[('cluster','Cluster')]
CLOUD=[('cloud','Cloud')]

DEPLOYS=[('cluster','Cluster'),
         ('cloud','Cloud')]

CASSANDRA=[('cassandra', 'Cassandra')]

MACHINE=[('m1.small', 'm1.small'),
    ('m1.medium', 'm1.medium'),
    ('m1.large', 'm1.large'),
    ('m1.xlarge', 'm1.xlarge')]

DEPLOY_OPTION = [('simple', 'Simple'),
  ('advanced', 'Advanced')]



class CommonFields(forms.Form):
    cloud = forms.ChoiceField(choices=DEPLOYS,
                              required = True,
                              label = False,
                              widget=forms.RadioSelect(attrs={
                                   'value': '',
                                   'onclick': 'checkTransType(this.value)',
                                   'type': 'radio',
                                   'name': '',

                                   }))

    advanced = forms.ChoiceField(choices=DEPLOY_OPTION,
                               label = False,
                               widget=forms.RadioSelect(attrs={
                                      'name': 'advanced',
                                      'value': 'advanced',
                                      'onclick': 'checkMinMax(this.value)',
                                    }))

    machine = forms.ChoiceField(choices=MACHINE,
                                widget=forms.Select(attrs={
                                  'class': 'dk_fix'
                                }))

    key = forms.CharField(label=("EC2/Eucalyptus Key"), required=True)

    secret = forms.CharField(label=("EC2/Eucalyptus Secret"), required=True)

    infras = forms.ChoiceField(choices=INFRAS, widget=forms.Select(attrs={
      'id': 'infrastructure',
      'class': 'dk_fix'
    }))

    min = forms.IntegerField(max_value=100,min_value=1)

    max = forms.IntegerField(max_value=100,min_value=1)

    admin_email = forms.EmailField(validators=[validate_email], max_length=40,
    required=True, widget=forms.TextInput(attrs={'id':'email', 'data-type':'email', 'name':"email",
    'data-trigger':"change", 'data-required':"true"}))

    admin_pass = forms.CharField(widget=forms.PasswordInput(render_value=False,
    attrs={'id':'admin_pass', 'name':"admin_pass", 'data-equalto': '#equalToModel', 'data-trigger':"change", 'data-required':"true"}),
    label=("Admin Password"), min_length=6, required=True, )

    pass_confirm = forms.CharField(widget=forms.PasswordInput(render_value=False,
    attrs={'id':'pass_confirm eqalToModel', 'data-equalto': '#equalToModel', 'name':"pass_confirm", 'data-trigger':"change", 'data-required':"true"}),
    label="Confirm Password", min_length=6, required=True)

    keyname = forms.CharField(min_length=4, max_length=24, required=True,
    widget=forms.TextInput(attrs={'id':'keyname', 'name':"keyname",
    'data-trigger':"change", 'data-required':"true"}))

    ips_yaml = forms.CharField(label=("ips.yaml"), max_length=120,
    widget=forms.Textarea(attrs={'id':'ips_yaml', 'name':"ips",'data-trigger':"change",
    'data-required':"true"}), required=True)

    machine = forms.ChoiceField(choices=MACHINE)

    def clean_password(self):
      if self.data['admin_pass'] != self.data['pass_confirm']:
        raise forms.ValidationError('Passwords are not the same')
      return self.data['admin_pass']

    def clean(self,*args, **kwargs):
      self.clean_password()
      return super(CommonFields, self).clean(*args, **kwargs)




def clean_forms(self):
  clean_secret = self.cleaned_data['secret']
  clean_key = self.cleaned_data['key']
  if clean_key:
    if not clean_secret:
      raise forms.ValidationError("Required Feild")
  return clean_secret


# I used this instead of lambda expression after scope problems
def _get_cleaner(form, field):
    def clean_field():
        return getattr(form.instance, field, None)
    return clean_field

class ROFormMixin(forms.BaseForm):
    def __init__(self, *args, **kwargs):
        super(ROFormMixin, self).__init__(*args, **kwargs)
        if hasattr(self, "read_only"):
            if self.instance and self.instance.pk:
                for field in self.read_only:
                    self.fields[field].widget.attrs['readonly'] = True
                    setattr(self, "clean_" + field, _get_cleaner(self, field))

class Cassandra(ROFormMixin):
    table = ('Cassandra')



class Cluster(forms.Form):

  min_max = forms.IntegerField(max_value=100,min_value=1)

  machine = forms.ChoiceField(choices=MACHINE)




class ec2(forms.Form):
    ec2_key = forms.CharField(label=("Amazon EC2 Key"), required=True)
    ec2_secret = forms.CharField(label=("Amazon EC2 Secret"), required=True)

class euca(forms.Form):
    ec2_key = forms.CharField(label=("Amazon EC2 Key"), required=True)
    ec2_secret = forms.CharField(label=("Amazon EC2 Secret"), required=True)

