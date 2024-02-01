
import subprocess
import re
import platform
import datetime

import logging

#################################################################################################
#
# Checks the Platform stats
#
#################################################################################################
class PlatformChecker:

   def __init__(self):
      self.uptime = None
      self.hostname = None
      self.hardware_model = None
      self.last_update = None

      self.hostname = platform.node()
      logging.debug("Hostname:" + self.hostname)

      self.uptime_pattern = re.compile('up\s+(.*)$')

      #2023-01-25 06:40:21.416352677 +0000
      self.hardware_model_pattern = re.compile('Model\s+:\s+(.*)$', re.IGNORECASE)
      #drwx------ 2 _apt root 24576 2023-01-26 10:20:46.752760434 +0000 /var/lib/apt/lists/partial
      #self.update_pattern = re.compile('^\S+\s+\d+\s+\S+\s+\S+\s+\d+\s+(\S+)\s+(\d\d:\d\d:\d\d.\d\d\d\d\d\d)\d\d\d\s+(\S+)\s+\S+', re.IGNORECASE)
      self.update_pattern = re.compile('^\S+\s+\d+\s+\S+\s+\S+\s+\d+\s+(\S+)\s+(\d\d:\d\d:\d\d.\d{6})\d{3}\s+(\S+)\s+\S+', re.IGNORECASE)


#################################################################################################
#
# Set the platform details
#
#################################################################################################
   def set_platform_details(self):
      pass

#################################################################################################
#
#    Gets Update time
#
#################################################################################################
   def set_update_time(self):

      cmd ="/bin/ls -ltrd --full-time /var/lib/apt/lists/partial/ /var/lib/dpkg/lock | /usr/bin/tail -n 1"
      sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
      stdout, stderr = sp.communicate()

      line = stdout.decode('utf-8')

      update_match = self.update_pattern.match(line)
      if update_match:
         last_update_date_str = update_match.group(1) 
         last_update_time_str = update_match.group(2) 
         last_update_tz_str = update_match.group(3) 
         update_time = datetime.datetime.strptime("{} {} {}".format(last_update_date_str, last_update_time_str, last_update_tz_str) , "%Y-%m-%d %H:%M:%S.%f %z")
         self.last_update = update_time.strftime("%H:%M:%S-%d/%m/%y")

      logging.debug("last_update:" + str(self.last_update))


     

#################################################################################################
#
#    Gets Uptime
#
#################################################################################################
   def set_uptime(self):

      cmd ="/usr/bin/uptime -p"
      sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
      stdout, stderr = sp.communicate()

      line = stdout.decode('utf-8')
      uptime_match = self.uptime_pattern.match(line)
      if uptime_match:
         self.uptime = uptime_match.group(1) 

      logging.debug("Uptime:" + str(self.uptime))

