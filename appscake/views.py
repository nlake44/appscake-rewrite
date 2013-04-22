""" Views for different pages. """
import logging

from appscake import helpers
from appscake import create_instances
from appscake.forms import CommonFields
from appscake.forms import Cluster

from django.contrib import  messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response


# When deploying on virtual machines without IaaS support.
CLUSTER_DEPLOY = "cluster"

# When deploying on IaaS.
CLOUD_DEPLOY = "cloud"

# A global variable to store all threads running the tools.
ALL_THREADS = {}

def home(request):
  return render(request, 'base/home.html', {'form': CommonFields(),})

def about(request):
  return render(request, 'base/about.html')

def virtualbox_form(request):
  return render(request, 'base/virtualbox.html')

def get_status(request):
  return create_instances.get_status()

def start(request):
  """ This is the page a user submits a request to start AppScale. """
  if request.method == 'POST':
    form = CommonFields(data=request.POST)
    if not form.is_valid():
      return HttpResponseRedirect('/start/?error=badform') # Redirect after POST

    tools_runner = None

    email = form['admin_email']
    password = form['admin_pass']
    keyname = helpers.generate_keyname()

    cloud_type = form['cloud']
    if cloud_type == CLOUD_DEPLOY:
      infras = form['infrastructure'] 
      deployment_type = form['deployment_type']
      machine = form['machine']
      if deployment_type == ADVANCE_DEPLOYMENT:
        ips_yaml = form['ips_yaml']
        tools_runner = ToolsRunner(cloud_type,
                                   keyname,
                                   email,
                                   password,
                                   placement=ADVANCE_DEPLOYMENT,
                                   machine=machine,
                                   instance_type=instance_type,
                                   ips_yaml=ips_yaml)
      elif deployment_type == SIMPLE_DEPLOYMENT:
        min_nodes = form['min']
        max_nodes = form['max']
        tools_runner = ToolsRunner(cloud_type,
                                   keyname,
                                   email,
                                   password,
                                   placement=SIMPLE_DEPLOYMENT,
                                   machine=machine,
                                   instance_type=instance_type,
                                   min_nodes=min_nodes,
                                   max_nodes=max_nodes)
    elif cloud_type == CLUSTER_DEPLOY:
      ips_yaml = form['ips_yaml']
      tools_runner = ToolsRunner(cloud_type,
                                 keyname,
                                 email,
                                 password,
                                 ips_yaml=ips_yaml)
    tools_runner.start()
    ALL_THREADS[tools_runner.identifier] = tools_runner
  else:
    return  render(request, 'base/start.html')
