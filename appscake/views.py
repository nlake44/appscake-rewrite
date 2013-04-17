import logging

from appscake import helpers

from django.shortcuts import render
from django.shortcuts import render_to_response
from appscake.forms import CommonFields
from django.http import HttpResponse
from django.http import HttpResponseRedirect

# When deploying on virtual machines without IaaS support.
CLUSTER_DEPLOY = "cluster"

# When deploying on IaaS.
CLOUD_DEPLOY = "cloud"

def home(request):
  return render(request, 'base/home.html', {'form': CommonFields(),})

def about(request):
  return render(request, 'base/about.html')

def virtualbox_form(request):
  return render(request, 'base/virtualbox.html')

def start(request):
  if request.method != 'POST':
    form = CommonFields(data=request.POST)
    print form
    cloud_type = form['cloud_type'] 

    email = form['admin_email']
    password = form['admin_pass']
    keyname = helpers.generate_keyname()

    if cloud_type == CLUSTER_DEPLOY:
      ips_yaml = form['ips_yaml']
    elif cloud_type == CLOUD_DEPLOY:
      infras = form['infrastructure'] 
     
    if form.is_valid():
      return HttpResponseRedirect('/start/') # Redirect after POST

  else:
    infras = request.POST['deploy_option1']
    cloud_type = request.POST['deploy_option2']
    admin_user = request.POST['admin_email']
    admin_pass = request.POST['admin_pass']
    pass_confirm = request.POST['pass_confirm']
    keyname =  request.POST['keyname']
    ips_yaml = request.POST['ips_yaml']
    instance_args = {'infras': 'infras', 'cloud_type': 'cloud_type',
                 'admin_user': 'admin_user', 'admin_pass': 'admin_pass',
                 'keyname': 'keyname', 'ips_yaml': 'ips_yaml'}
    print instance_args

    # options = { 'keyname' => keyname, 'ips_layout' => 'something'}

  #AppScaleTools.run_instances(options)
  return  render(request, 'base/start.html')



