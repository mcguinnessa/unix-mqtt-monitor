
import subprocess
import re

import logging

from cpu_checker import CPUChecker


#################################################################################################
#
# Checks the CPU stats
#
#################################################################################################
class CPUCheckerRPi(CPUChecker):

   def __init__(self):
      super(CPUCheckerRPi, self).__init__()

      self.gputemp_pattern = re.compile('temp=(\d+).*')
      self.gputhrottle_pattern = re.compile('throttled=(\d+x\d+).*')

      self.cpu_hardware_pattern = re.compile('(Hardware)\s+:\s+(.*)$', re.IGNORECASE)
      self.cpu_model_pattern = re.compile('model name\s+:\s+(.*)$', re.IGNORECASE)
#      self.cpu_serial_pattern = re.compile('Serial\s+:\s+(.*)$', re.IGNORECASE)



#################################################################################################
#
# GPU Temp
#
#################################################################################################
   def set_gpu_temp(self):

      cmd ="vcgencmd measure_temp"
      sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
      stdout, stderr = sp.communicate()

      line = stdout.decode('utf-8').strip()
      gputemp_match = self.gputemp_pattern.match(line)
      if gputemp_match:
         self.gputemp = gputemp_match.group(1)

      logging.debug("GPU Temp:" + str(self.gputemp))

#################################################################################################
#
# GPU Throttline
#
#################################################################################################
   def set_gpu_throttled(self):

      #throttled=0x0
      cmd ="vcgencmd get_throttled"
      sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
      stdout, stderr = sp.communicate()

      line = stdout.decode('utf-8').strip()
      gputhrottle_match = self.gputhrottle_pattern.match(line)
      if gputhrottle_match:
         self.gputhrottle = gputhrottle_match.group(1)

      logging.debug("GPU Throttled:" + str(self.gputhrottle))






