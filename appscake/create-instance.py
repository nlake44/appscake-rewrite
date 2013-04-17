# General-purpose Python library imports
import argparse
import base64
import os
import sys
import threading

sys.path.append(os.path.join(os.path.dirname(__file__),"../appscale-tools/lib"))
from appscale_logger import AppScaleLogger
from appscale_tools import AppScaleTools
from parse_args import ParseArgs

class ToolsRunner(threading.Thread):

  # Automatic layout of roles in AppScale.
  SIMPLE = "simple"

  # Manual layout of roles in AppScale.
  ADVANCE = "advance"

  # Cluster type deployment.
  CLUSTER = "cluster"

  # Cloud type deployment.
  CLOUD = "cloud"

  # Default args given to the tools.
  DEFAULT_ARGS = ['--table', 'cassandra']

  def __init__(self, deployment_type, keyname, admin_email, admin_pass, 
    placement=SIMPLE, min_nodes=None, max_nodes=None, machine=None, 
    instance_type=None, ips_yaml=None):
    """ Constructor. 
    
    Args:
      deployment_type: A str, the deployment type of either cloud or cluster.
      keyname: A str representing the keyname used for an AppScale
        deployment.
      admin_email: A str, email for the administrator.
      admin_pass: A str, password for the administrator.
      placement: A str, of either automatic placement or manual.
      max_nodes: An int, the maximum number of nodes AppScale can run.
      min_nodes: An int, the minimum number of nodes AppScale can run.
      machine: A str representing the emi or ami identifier of the cloud image 
        to use.
      infrastructure: A str, the infrastructure used (ec2, euca, etc.).
      instance_type: A str, the instance size to use when starting up VMs.
      ips_yaml: A str, of the contents of the ips.yaml file.
    """
    threading.Thread.__init__(self)
    self.keyname = keyname
    self.admin_email = admin_email
    self.admin_pass = admin_pass
    self.deployment_type = deployment_type #cloud or cluster
    self.placement = placement #simple or advance
    self.min_nodes = min_nodes
    self.max_nodes = max_nodes
    self.machine = machine
    self.infrastructure = infrastructure
    self.instance_type = instance_type
    self.ips_yaml = ips_yaml
    self.ips_yaml_b64 = None
    if ips_yaml:
      self.ips_yaml_b64 = base64.b64encode(ips_yaml)

    self.status = "Initialized"
    self.message = ""
    self.args = DEFAULT_TOOLS_ARGS
    self.args.append(["--admin_email", self.admin_email,
                      "--admin_pass", self.admin_pass,
                      "--keyname", self.keyname])
  def run(self):
    """
    """
    self.status = "Running"

    if self.deployment_type == CLOUD:
      if self.placement == SIMPLE:
        self.run_simple_cloud_deploy()
      elif self.placement == ADVANCE:
        self.run_advance_cloud_deploy()
      else:
        raise NotImplemented("Unknown placement of {0}".format(self.placement))
    elif self.deployment_type == CLUSTER:
      self.run_cluster_deploy()
    else:
      raise NotImplemented("Unknown deployment of {0}".format(self.deployment_type)) 

  def run_cluster_deploy(self):
    """
    """
    self.args.append(["--ips_layout", self.ips_yaml_b64])
    self.run_appscale()

  def run_advance_cloud_deploy(self):
    """
    """
    self.args.append(["--infrastructure", self.infrastructure, 
                      "--machine", self.machine,  
                      "--ips_layout", self.ips_yaml_b64])
    self.run_appscale()

  def run_simple_cloud_deploy(self):
    """ 
    """
    self.args.append(["--infrastructure", self.infrastructure, 
                      "--machine", self.machine,  
                      "--min", self.min_nodes,
                      "--max", self.max_nodes])
    self.run_appscale()

  def run_appscale(self):
    self.status = "Running"
    options = ParseArgs(self.args, "appscale-run-instances").args
    try:
      AppScaleTools.run_instances(options)
    except Exception as e:
      self.status = "Error"
      self.message = str(e)
