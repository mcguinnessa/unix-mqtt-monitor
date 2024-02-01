
import subprocess
import re

import logging


#################################################################################################
#
# Checks the Network metrics
#
#################################################################################################
class NetworkChecker:

   def __init__(self):
      self.network_info = {}
     
      self.fully_qualified_domain_name = ""

      self.mac_addr_pattern = re.compile('\d+: (\S+):.*ether (\S\S:\S\S:\S\S:\S\S:\S\S:\S\S) .*')
#2: enp0s31f6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000\    link/ether 70:85:c2:38:ca:b4 brd ff:ff:ff:ff:ff:ff


#################################################################################################
#
# Gets the MAC address from the system, uses the HW MAC address as sometime linux spoofs one
# which is volative across reboots
#
#################################################################################################
#   def get_mac_addr(self, nw_device_name):
   def set_mac_addr(self):

      cmd ="ip -o link show "
      #cmd ="ip -o link show "+nw_device_name
      sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

      mac_addr = ""

      for line in sp.stdout:
         line = line.decode()
         line = line.strip()
         mac_addr_match = self.mac_addr_pattern.match(line)

         if mac_addr_match:
            device_name = str(mac_addr_match.group(1))
            if device_name in self.network_info:
               device_info = self.network_info[device_name]
            else:
               device_info = {}
               self.network_info[device_name] = device_info

            #self.network_info["mac_addr"] = str(mac_addr_match.group(1))
            device_info["mac_addr"] = str(mac_addr_match.group(2))
            logging.debug("Found MAC Addr:" + str(mac_addr))

#TODO this needs all interfaces (networking": {"eth0": {"IP": "192.168.0.5", "mac": "b8:27:eb:31:95:d0"}})


#################################################################################################
#
# Gets the IP Address
#
#################################################################################################
   def set_ip_addr(self, nw_device_name):
      #global network_info

      cmd ="hostname -I"
      sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
      stdout, stderr = sp.communicate()
      line = stdout.decode('utf-8').strip()
      if len(line) > 0:

         if nw_device_name in self.network_info:
            device_info = self.network_info[nw_device_name]
         else:
            device_info = {}
            self.network_info[nw_device_name] = device_info

         device_info["ip_addr"] = line

#################################################################################################
#
# Gets the Fully Qualified Domain Name
#
#################################################################################################
   def set_fqdn(self):
      #global fully_qualified_domain_name

      cmd ="hostname -f"
      sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
      stdout, stderr = sp.communicate()
      line = stdout.decode('utf-8').strip()
      if len(line) > 0:
         self.fully_qualified_domain_name = line

