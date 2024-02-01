
import logging

from cpu_checker_rpi import CPUCheckerRPi
from memory_checker import MemoryChecker
from disk_checker import DiskChecker
from network_checker import NetworkChecker
from os_checker import OSChecker
from platform_checker_rpi import PlatformCheckerRPi
from ntpd_checker import NTPDChecker
from node import Node


class RPiNode(Node):

   TYPE_RPI = "rpi"

#################################################################################################
#
# Defines the Ubuntu Node
#
#################################################################################################
   def __init__(self):
      """Init"""

   def get_cpu_checker(self):
      return CPUCheckerRPi()

   def get_memory_checker(self):
      return MemoryChecker()

   def get_disk_checker(self, excludes):
      return DiskChecker(excludes)

   def get_network_checker(self):
      return NetworkChecker()

   def get_os_checker(self):
      return OSChecker()

   def get_platform_checker(self):
      return PlatformCheckerRPi()

   def get_ntpd_checker(self):
      return NTPDChecker()



