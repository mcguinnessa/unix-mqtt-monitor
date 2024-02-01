
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
class PlatformCheckerUbuntu(PlatformChecker):

   def __init__(self):
      super(PlatformCheckerUbuntu, self).__init__();
#      self.uptime = None
#      self.hostname = None
#      self.hardware_model = None

#      self.hostname = platform.node()
#      logging.debug("Hostname:" + self.hostname)
#
#      self.uptime_pattern = re.compile('up\s+(.*)$')
#
#      self.hardware_model_pattern = re.compile('Model\s+:\s+(.*)$', re.IGNORECASE)

