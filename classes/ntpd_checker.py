
import subprocess
import re
import platform

import logging



#################################################################################################
#
# Checks the status of the NTPD daemon
#
#################################################################################################
class NTPDChecker:

   def __init__(self):
      self.ntpd_running = "false"

      self.ntpd_pattern = re.compile(".*NTP service: (\S+)")
      

#################################################################################################
#
#    Gets Status of NTPD
#
#################################################################################################
   def set_ntpd_status(self):

      cmd = "timedatectl status"
      sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
      #stdout, stderr = sp.communicate()

      for line in sp.stdout:
         line = line.decode('utf-8')
         #logging.debug("NTPD:" + line)
         ntpd_match = self.ntpd_pattern.match(line)
         if ntpd_match:
            logging.debug("ntpd_match(1):" + str(ntpd_match.group(1)))
            if ntpd_match.group(1) == "active":
               self.ntpd_running = "true"

      logging.debug("NTP Running:" + str(self.ntpd_running))


