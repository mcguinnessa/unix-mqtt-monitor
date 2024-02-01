
import subprocess
import re
import yaml

import logging

class Config:

#   TYPE_UBUNTU = "ubuntu"
#   TYPE_RPI = "rpi"

#################################################################################################
#
# Gets the config
#
#################################################################################################
   def __init__(self):

      file = open("/home/alex/scripts/nmt/mqtt-monitor/mqtt-monitor.yaml", 'r')
      doc = yaml.safe_load(file)
      logging.debug("DOC:" + str(doc))

      logging.debug("Display Name:" + str(doc["mqtt_monitor"]["node_display_name"]))

      logging.debug("DUMP:" + yaml.dump(doc))
      
      logging.debug("Loaded Config")

      self.type = doc["mqtt_monitor"]["type"]

      self.nw_device_name = doc["mqtt_monitor"]["network"]["device_name"]
      self.disks_exclude = doc["mqtt_monitor"]["disks"]["exclude"]
      self.node_manufacturer = doc["mqtt_monitor"]["cpu"]["manufacturer"]
      self.node_model = doc["mqtt_monitor"]["cpu"]["model"]
      self.broker_host_name = doc["mqtt_monitor"]["broker"]["hostname"]
      self.broker_user = doc["mqtt_monitor"]["broker"]["user"]
      self.broker_password = doc["mqtt_monitor"]["broker"]["password"]
      self.keep_alive_period = doc["mqtt_monitor"]["app"]["keep_alive_period"]
      self.data_period = doc["mqtt_monitor"]["app"]["data_period"]
      self.node_display_name = doc["mqtt_monitor"]["node_display_name"]

      logging.debug("Type:" + str(self.type))
      logging.debug("Display Name:" + str(self.node_display_name))
      logging.debug("Network Device Name:" + str(self.nw_device_name))
      logging.debug("Disk Exclude:" + str(self.disks_exclude))
      logging.debug("CPU Manufacturer:" + str(self.node_manufacturer))
      logging.debug("CPU Model:" + str(self.node_model))
      logging.debug("Broker Hostname:" + str(self.broker_host_name))
      logging.debug("Broker User:" + str(self.broker_user))
      logging.debug("Broker Password:" + str(self.broker_password))
      logging.debug("Keep Alive Period:" + str(self.keep_alive_period))
      logging.debug("Data Period:" + str(self.data_period))

