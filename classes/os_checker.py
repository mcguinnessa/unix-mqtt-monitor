
import subprocess
import re

import logging


#################################################################################################
#
# Checks the OS Metrics
#
#################################################################################################
class OSChecker:

   def __init__(self):
      self.os_info = {}

#No LSB modules are available.
#Distributor ID:	Ubuntu
#Description:	Ubuntu 20.04.5 LTS
#Release:	20.04
#Codename:	focal

      self.os_name_pattern = re.compile('Distributor ID:\s+(\S+)')
      self.os_mv_pattern = re.compile('Release:\s+(\S+)$')
      self.os_mvn_pattern = re.compile('Codename:\s+(\S+)')
      self.os_desc_pattern = re.compile('Description:\s+(.*)$')
      self.os_kernel_pattern = re.compile('Linux version\s+(\S+)\s+')


#################################################################################################
#
# Gets the kernel version
#
#################################################################################################
   def set_os_details(self):

      cmd ="cat /proc/version; /usr/bin/lsb_release -a"
      sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

      for line in sp.stdout:
         line = line.decode().strip()
         os_name_match = self.os_name_pattern.match(line)
         os_mv_match = self.os_mv_pattern.match(line)
         os_mvn_match = self.os_mvn_pattern.match(line)
         os_kernel_match = self.os_kernel_pattern.match(line)
         os_desc_match = self.os_desc_pattern.match(line)
         if os_name_match:
            #os_name = str(os_name_match.group(1))
            self.os_info["os_name"] = str(os_name_match.group(1))
         if os_mv_match:
            #os_major_version = str(os_mv_match.group(1))
            self.os_info["major_version"] = str(os_mv_match.group(1))
         if os_mvn_match:
            #os_major_version_name = str(os_mvn_match.group(1))
            self.os_info["major_version_name"] = str(os_mvn_match.group(1))
         if os_kernel_match:
            #os_kernel_version = str(os_kernel_match.group(1))
            self.os_info["kernel_version"] = str(os_kernel_match.group(1))
         if os_desc_match:
            self.os_info["desc"] = str(os_desc_match.group(1))

      if self.os_info["major_version_name"] not in self.os_info["desc"]:
         long_description = self.os_info["desc"] + " (" + self.os_info["major_version_name"] + ")"
         self.os_info["desc"] = long_description

      logging.debug("OS Name:" + str(self.os_info["os_name"]))
      logging.debug("OS Major Version:" + str(self.os_info["major_version"]))
      logging.debug("OS Major Version Name:" + str(self.os_info["major_version_name"]))
      logging.debug("Kernel Version:" + str(self.os_info["kernel_version"]))
      logging.debug("OS Description:" + str(self.os_info["desc"]))

