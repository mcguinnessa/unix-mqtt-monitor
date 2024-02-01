#!/usr/bin/python3

import sys
sys.path.append('/home/alex/scripts/nmt/mqtt-monitor/classes')

import time
import json
from datetime import datetime, timedelta
import sys
import os
import getopt
import logging

from cpu_checker import CPUChecker
from memory_checker import MemoryChecker
from disk_checker import DiskChecker
from network_checker import NetworkChecker
from os_checker import OSChecker
from platform_checker import PlatformChecker
from ntpd_checker import NTPDChecker
from mqtt_connection import MQTTConnection
from config import Config
from ubuntu_node import UbuntuNode
from rpi_node import RPiNode

reporter = os.path.abspath(__file__)

#################################################################################################
#
# Checks a UNIX box for system metrics
#
#################################################################################################
class unix_mqtt_monitor():

   def __init__(self):

      self.config = Config()
     
      if self.config.type == UbuntuNode.TYPE_UBUNTU:
         node = UbuntuNode()
      if self.config.type == RPiNode.TYPE_RPI:
         node = RPiNode()

      self.cpu_checker = node.get_cpu_checker()
      self.memory_checker = node.get_memory_checker()
      self.disk_checker = node.get_disk_checker(self.config.disks_exclude)
      self.network_checker = node.get_network_checker()
      self.os_checker = node.get_os_checker()
      self.platform_checker = node.get_platform_checker()
      self.ntpd_checker = node.get_ntpd_checker()

      self.mqtt_connection = None
      self.uniqid = ""
      self.hardware_mode = None

      self.get_static_info()

#################################################################################################
#
# Gets all the info that doesn't change
#
#################################################################################################
   def get_static_info(self):

      self.cpu_checker.set_cpu_details()
      self.os_checker.set_os_details()
      self.platform_checker.set_platform_details()

      # If can't get hardware from CLI, use that in config
      if self.platform_checker.hardware_model:
         self.hardware_model = self.platform_checker.hardware_model
      else:
         self.hardware_model = self.config.node_model

      self.network_checker.set_mac_addr()
      self.network_checker.set_ip_addr(self.config.nw_device_name)
      self.network_checker.set_fqdn()

      self.uniqid = self.get_uniq_id()
      logging.debug("Unique Id:" + str(self.uniqid))

#################################################################################################
#
# Checks all the metrics
#
#################################################################################################
   def send_autodiscovery_messages(self, full_device, short_device):

      self.mqtt_connection = MQTTConnection(self.uniqid, 
                                            self.platform_checker.hostname, 
                                            self.network_checker.fully_qualified_domain_name, 
                                            self.config.broker_host_name, 
                                            self.config.broker_user, 
                                            self.config.broker_password, 
                                            reporter, 
                                            self.config.keep_alive_period)

      self.mqtt_connection.send_discovery_message("Monitor", "monitor", "timestamp", "mdi:desktop-tower", None, "{{ value_json.info.timestamp }}", "{{ value_json.info | tojson }}", full_device)
      self.mqtt_connection.send_discovery_message("CPU Temp", "cputemp", "temperature", "mdi:thermometer", "°C", "{{ value_json.info.cputemp }}", None, short_device)
      self.mqtt_connection.send_discovery_message("CPU Load", "cpuload", None, "mdi:cpu-32-bit", "%", "{{ value_json.info.cpu.load_5min_prcnt }}", None, short_device)
      self.mqtt_connection.send_discovery_message("Memory Usage", "memusage", None, "mdi:memory", "%", "{{ value_json.info.mem.used_pct }}", None, short_device)
      self.mqtt_connection.send_discovery_message("Uptime", "uptime", "duration", "mdi:timer-outline", None, "{{ value_json.info.uptime }}", None, short_device)

      self.mqtt_connection.send_binary_discovery_message("NTPD Status", "ntpd_running", "running", "mdi:clock-check-outline", "{{ value_json.info.ntpd_running }}", None, short_device)

      self.disk_checker.set_disk_stats()
      for disk_key in self.disk_checker.disk_info:
         key = "disk-" + disk_key
         name = "Disk({}) Used".format(disk_key)
         template = "{{" +" value_json.info.disks.{}.used_pct ".format(disk_key) + "}}"
         self.mqtt_connection.send_discovery_message(name, key, None, "mdi:harddisk", "%", template, None, short_device)

#################################################################################################
#
# Checks all the metrics
#
#################################################################################################
   def check(self):

      full_device = {}
      short_device = {}
      full_device["identifiers"] = "{}-{}".format(self.platform_checker.hostname, self.uniqid)
      short_device["identifiers"] = "{}-{}".format(self.platform_checker.hostname, self.uniqid)
      full_device["manufacturer"] = self.config.node_manufacturer
      #full_device["model"] = self.config.node_model
      full_device["model"] = self.hardware_model
      full_device["name"] = self.config.node_display_name
      full_device["sw_version"] = self.os_checker.os_info["kernel_version"]

      try:
         self.send_autodiscovery_messages(full_device, short_device)
         self.loop()

      except Exception as e:
         logging.debug("Failed to Connect", str(e))

         import traceback
         import sys
         logging.debug(traceback.format_exc())

#################################################################################################
#
# loop
#
#################################################################################################
   def loop(self):

      count = 0
      while True:
         if 0 == (count % 5):
            self.get_latest_metrics()
            self.mqtt_connection.send_data_message(self.cpu_checker.cputemp, self.cpu_checker.gputemp, self.cpu_checker.gputhrottle, self.os_checker.os_info, self.platform_checker.uptime, self.cpu_checker.cpu_info, self.memory_checker.memory_info, self.disk_checker.disk_info, self.disk_checker.fs_prcnt_used, self.disk_checker.fs_total_gb, self.network_checker.network_info, self.ntpd_checker.ntpd_running, self.platform_checker.last_update)

         else:
            self.mqtt_connection.send_status_message()

         count += 1

         logging.debug("Sleeping for " + str(self.config.keep_alive_period) + "s")
         time.sleep(self.config.keep_alive_period)

#################################################################################################
#
# Gets the base Unique ID
#
#################################################################################################
   def get_uniq_id(self):

      #stripped_mac = self.network_checker.network_info["mac_addr"].replace(":","")

      logging.debug("NW INFO:" + str(self.network_checker.network_info))
      stripped_mac = self.network_checker.network_info[self.config.nw_device_name]["mac_addr"].replace(":","")
      logging.debug("Uniq ID:" + stripped_mac)
      return stripped_mac

#################################################################################################
#
# Get Latest Stats
#
#################################################################################################
   def get_latest_metrics(self):

      self.cpu_checker.set_cpu_stats()
      self.memory_checker.set_memory_stats()
      self.platform_checker.set_uptime() 
      self.platform_checker.set_update_time() 
      self.disk_checker.set_disk_stats()
      logging.debug("Setting CPU Temp")
      self.cpu_checker.set_cpu_temp()
      logging.debug("Setting GPU Temp")
      self.cpu_checker.set_gpu_temp()
      self.cpu_checker.set_gpu_throttled()
      self.ntpd_checker.set_ntpd_status()

# rpi_model



#########################################################################################
#
# Main
#
#########################################################################################
def main(argv):
   try:
       opts, args = getopt.getopt(argv, "l:", ["log="])
   except getopt.GetoptError:
      usage()
      sys.exit(2)
   
   loglevel = "DEBUG"
   num_lookups = -1
   max_records = None

   for opt, arg in opts:
      if opt in ("-l", "--log"):
         loglevel = arg.upper()

   numeric_log_level = getattr(logging, loglevel, None)

   logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='/home/alex/scripts/nmt/mqtt-monitor/system-mqtt-monitor.log', filemode='w', level=logging.DEBUG)
   console = logging.StreamHandler()
   #console.setLevel(logging.INFO)
   console.setLevel(logging.DEBUG)
   formatter = logging.Formatter('%(levelname)-8s %(message)s')
   console.setFormatter(formatter)
   logging.getLogger('').addHandler(console)

   checker = unix_mqtt_monitor()
   checker.check()


if __name__ == "__main__":
   main(sys.argv[1:])

