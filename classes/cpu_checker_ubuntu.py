
import subprocess
import re

import logging

from cpu_checker import CPUChecker


#################################################################################################
#
# Checks the CPU stats
#
#################################################################################################
class CPUCheckerUbuntu(CPUChecker):

   def __init__(self):
      super(CPUCheckerUbuntu, self).__init__()

      self.cpu_hardware_pattern = re.compile('(Model)\s+:\s+(.*)$', re.IGNORECASE)
      self.cpu_model_pattern = re.compile('model name\s+:\s+(.*)$', re.IGNORECASE)
#      self.cpu_serial_pattern = re.compile('Serial\s+:\s+(.*)$', re.IGNORECASE)


      

