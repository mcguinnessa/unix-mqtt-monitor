
import subprocess
import re
import platform

import logging

from platform_checker import PlatformChecker

#################################################################################################
#
# Checks the Platform stats
#
#################################################################################################
class PlatformCheckerRPi(PlatformChecker):

   def __init__(self):
      super(PlatformCheckerRPi, self).__init__()
#      self.uptime = None
#      self.hostname = None
#      self.hardware_model = None
#
#      self.hostname = platform.node()
#      logging.debug("Hostname:" + self.hostname)
#
#      self.uptime_pattern = re.compile('up\s+(.*)$')

      self.hardware_model_pattern = re.compile('Model\s+:\s+(.*)$', re.IGNORECASE)

#################################################################################################
#
# Set the platform details
#
#################################################################################################
   def set_platform_details(self):

      cmd ="cat /proc/cpuinfo;"

      sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

      for line in sp.stdout:
         line = line.decode()
         line = line.strip()
         hardware_model_match = self.hardware_model_pattern.match(line)

         if hardware_model_match:
            self.hardware_model = str(hardware_model_match.group(1))
            logging.debug("Found Hardware Model:" + str(self.hardware_model))

