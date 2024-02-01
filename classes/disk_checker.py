
import subprocess
import re

import logging


#################################################################################################
#
# Checks the Disk stats
#
#################################################################################################
class DiskChecker:

   def __init__(self, excludes):
      self.disk_info = {}

      self.disk_pattern = re.compile('(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)%\s+(\S+)')

      self.excludes = excludes.split(",")
      self.excludes.append("tmpfs")
      self.excludes.append("boot")
      self.excludes.append("loop")
      self.excludes.append("udev")
      self.excludes.append("cifs")

      self.fs_prcnt_used = None
      self.fs_total_gb = None
      

#################################################################################################
#
# Gets the disk info
#
#################################################################################################
   def set_disk_stats(self):

   #/dev/sda1                     ext4       239253116   32066080  194960784  15% /
      excludes = "|".join(self.excludes)
      logging.debug("Excluding Disks:" + excludes)

      #cmd ="/bin/df -kT | /usr/bin/tail -n +2 | /bin/egrep -v \"tmpfs|boot|loop|udev|cifs\""
      cmd ="/bin/df -kT | /usr/bin/tail -n +2 | /bin/egrep -v \"" + excludes +"\""
      sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

      total_used = 0
      total_capacity = 0
      for line in sp.stdout:
         line = line.decode().strip()
         disk_match = self.disk_pattern.match(line)
         if disk_match:
            disk = {}
            disk["device"] = disk_match.group(1)
            disk["mount_pt"] = disk_match.group(7)
            disk["size_k"] = disk_match.group(3)
            used = disk_match.group(4)
            avail = disk_match.group(5)
            disk["used_pct"] = disk_match.group(6)

            total_used += int(used)
            total_capacity += int(used) + int(avail)
            logging.debug("Total Used:" + str(total_used) + " Total Capacity:" + str(total_capacity))

            drive_key = disk["mount_pt"].replace('/', '_').replace('_', '', 1) 
            if len(drive_key) == 0:
               drive_key = "root"

            self.disk_info[drive_key] = disk

            logging.debug("Device:" + str(disk["device"]))
            logging.debug("Mount:" + str(disk["mount_pt"]))
            logging.debug("Size (k):" + str(disk["size_k"]))
            logging.debug("Used Pct:" + str(disk["used_pct"]))

      total_perc = float(total_used) / float(total_capacity) * 100
      logging.debug("total_perc("+str(total_perc)+") = " + str(total_used) + " / " + str(total_capacity))
      self.fs_total_gb = "{:d}".format(int(total_capacity / (1024 * 1024)))
      self.fs_prcnt_used = "{:d}".format(int(total_perc))
      logging.debug("Total GB:" + str(self.fs_total_gb))
      logging.debug("Total Used:" + str(self.fs_prcnt_used))
