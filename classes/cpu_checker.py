
import subprocess
import re

import logging


#################################################################################################
#
# Checks the CPU stats
#
#################################################################################################
class CPUChecker:

   def __init__(self):
      self.cpu_info = {}
      self.cputemp = None
      self.gputemp = None
      self.gputhrottle = None

      self.cputemp_pattern = re.compile('^(\S+)$')

      self.cpu_no_cores_pattern = re.compile('cpu cores\s+:\s+(.*)$', re.IGNORECASE)
      self.cpu_core_count_pattern = re.compile('processor\s+:\s+(.*)$', re.IGNORECASE)


      self.cpu_bogomips_pattern = re.compile('BogoMips\s+:\s+(.*)$', re.IGNORECASE)
      self.cpu_serial_pattern = re.compile('Serial\s+:\s+(.*)$', re.IGNORECASE)

#################################################################################################
#
# Gets the static CPU info
#
#################################################################################################
   def set_cpu_details(self):

      cmd ="cat /proc/cpuinfo;"

      sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

      highest_cpu_number = 0
      for line in sp.stdout:
         line = line.decode()
         line = line.strip()
         cpu_model_match = self.cpu_model_pattern.match(line)
         cpu_no_cores_match = self.cpu_no_cores_pattern.match(line)
         cpu_core_count_match = self.cpu_core_count_pattern.match(line)
         cpu_bogomips_match = self.cpu_bogomips_pattern.match(line)
         cpu_hardware_match = self.cpu_hardware_pattern.match(line)
         cpu_serial_match = self.cpu_serial_pattern.match(line)

         if cpu_model_match:
            self.cpu_info["model"] = str(cpu_model_match.group(1))
            logging.debug("Found CPU Model:" + str(self.cpu_info["model"]))
         if cpu_no_cores_match:
            self.cpu_info["number_cores"] = str(cpu_no_cores_match.group(1))
            logging.debug("Found CPU Cores Declared:" + str(self.cpu_info["number_cores"]))
         if cpu_core_count_match:
            proc_num = str(cpu_core_count_match.group(1))
            if int(proc_num) > highest_cpu_number:
               highest_cpu_number = int(proc_num)
            logging.debug("Found CPU Processor Number:" + str(proc_num) + " Highest:" + str(highest_cpu_number))
         if cpu_bogomips_match:
            self.cpu_info["bogo_mips"] = str(cpu_bogomips_match.group(1))
            logging.debug("Found BogoMIPs:" + str(self.cpu_info["bogo_mips"]))
         if cpu_hardware_match:
            self.cpu_info["hardware"] = str(cpu_hardware_match.group(2))
            logging.debug("Found Hardware / Chip Model:" + str(self.cpu_info["hardware"]))
         if cpu_serial_match:
            self.cpu_info["serial"] = str(cpu_serial_match.group(1))
            logging.debug("Found Serial:" + str(self.cpu_info["serial"]))

      if "number_cores" not in self.cpu_info:
         logging.debug("number cores not found") 
         self.cpu_info["number_cores"] = str(highest_cpu_number+1)   #Add 1 as CPU count starts from 0
      logging.debug("Number CPU Cores:" + str(self.cpu_info["number_cores"]))
      

#################################################################################################
#
# CPU Stats
#
#################################################################################################
   def set_cpu_stats(self):

      cmd ="cat /proc/loadavg"
      sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
      out, err = sp.communicate()

      cpu_el = out.split()

      num_cpus = float(self.cpu_info["number_cores"])

      logging.debug("CPU RAW:" + str(cpu_el))
      self.cpu_info["load_1min_prcnt"]  = round(float(float(cpu_el[0]) / num_cpus * 100), 1)
      self.cpu_info["load_5min_prcnt"]  = round(float(float(cpu_el[1]) / num_cpus * 100), 1)
      self.cpu_info["load_15min_prcnt"] = round(float(float(cpu_el[2]) / num_cpus * 100), 1)

      logging.debug("CPU 1 min av:" + str(self.cpu_info["load_1min_prcnt"]))
      logging.debug("CPU 5 min av:" + str(self.cpu_info["load_5min_prcnt"]))
      logging.debug("CPU 15 min av:" + str(self.cpu_info["load_15min_prcnt"]))


#################################################################################################
#
# CPU Temp
#
#################################################################################################
   def set_cpu_temp(self):

      #logging.debug("Setting CPU Temp")
      cmd = "cat /sys/class/thermal/thermal_zone*/temp | sort -r"
      sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
      out, err = sp.communicate()

      line = out.decode('utf-8')
      cputemp_match = self.cputemp_pattern.match(line)

      if cputemp_match:
         cputemp_flt = float(cputemp_match.group(1))
         self.cputemp = "{:.1f}".format(cputemp_flt / 1000)
         logging.debug("CPU Temp:" + str(self.cputemp))

#################################################################################################
#
# GPU Temp
#
#################################################################################################
   def set_gpu_temp(self):
      pass

#################################################################################################
#
# GPU Throttled
#
#################################################################################################
   def set_gpu_throttled(self):
      pass
