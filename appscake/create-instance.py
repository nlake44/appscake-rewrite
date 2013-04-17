# General-purpose Python library imports
import os
import sys
import argparse

os.path.append("/root/appscale-tools/lib")
from appscale_logger import AppScaleLogger
from appscale_tools import AppScaleTools
from parse_args import ParseArgs



def run_instances(cloud_type, infras,
                  instance_type,
                  ...):
  """ TODO doc string
  """
  args = ['--table', "cassandra"]
  if cloud_type == "cloud":
    args.append(["--infrastructure", infras, "--machine", machine, "--admin",
                 admin, "--admin_pass", admin_pass, "keyname", keyname, "ips_yaml",
                 ips_yaml])
  else cloud_type == "cluster":
    args.append([])
  else:
    return "Unknown deployment type"
  options = ParseArgs(args, "appscale-run-instances").args
  try:
    AppScaleTools.run_instances(options)
  except Exception as e:
      AppScaleLogger.warn