import logging

from appscake import helpers
from django.contrib import  messages
from django.shortcuts import render
from django.shortcuts import render_to_response
from appscake.forms import CommonFields
from appscake.forms import Cluster
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

def virtualbox_form(request):
  return render(request, 'base/test.json')

def start(request):
  """ This is the page a user submits a request to start AppScale. """
  if request.method == 'POST':

    form = CommonFields(data=request.POST)

    email = form['admin_email']
    password = form['admin_pass']
    keyname = helpers.generate_keyname()

    cloud_type = form['cloud']
    if cloud_type == CLOUD_DEPLOY:
      infras = form['infrastructure'] 
      deployment_type = form['deployment_type']
      if deployment_type == ADVANCE_DEPLOYMENT:
        ips_yaml = form['ips_yaml']
      elif deployment_type == SIMPLE_DEPLOYMENT:
        min_nodes = form['min']
        max_nodes = form['max']
      machine = form['machine']
    elif cloud_type == CLUSTER_DEPLOY:
      ips_yaml = form['ips_yaml']

    if not form.is_valid():
      return HttpResponseRedirect('/start/?error=badform') # Redirect after POST
      # Fire it off in a thread and then redirect to a page that polls.

  else:
    return  render(request, 'base/start.html')



