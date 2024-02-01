
import subprocess
import re

import logging

#################################################################################################
#
# Checks the Memory details
#
#################################################################################################
class MemoryChecker:

   def __init__(self):
      self.memory_info = {}

      self.memory_pattern = re.compile('Mem:\s+(\d+)\s+\d+\s+(\d+).*')

#################################################################################################
#
# Memory Stats
#
#################################################################################################
   def set_memory_stats(self):

      #Mem:       32580964    10998348     3962220     1757704    17620396    19363684
      cmd ="/usr/bin/free -k"
      sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

      memory_addr = ""

      for line in sp.stdout:
         line = line.decode()
         line = line.strip()
         memory_match = self.memory_pattern.match(line)

         if memory_match:
            self.memory_info["total_kb"] = str(memory_match.group(1))
            memory_free = str(memory_match.group(2))
            logging.debug("Total Memory:" + str(self.memory_info["total_kb"]))
            logging.debug("Free Memory:" + str(memory_free))

            self.memory_info["used_pct"] = round(float((float(self.memory_info["total_kb"]) - float(memory_free)) / float(self.memory_info["total_kb"]) * 100), 1)
            logging.debug("Used Memory(%):" + str(self.memory_info["used_pct"]))

