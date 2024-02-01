
import logging

from cpu_checker_ubuntu import CPUCheckerUbuntu
from memory_checker import MemoryChecker
from disk_checker import DiskChecker
from network_checker import NetworkChecker
from os_checker import OSChecker
from platform_checker_ubuntu import PlatformCheckerUbuntu
from ntpd_checker import NTPDChecker
from node import Node


class UbuntuNode(Node):

   TYPE_UBUNTU = "ubuntu"

#################################################################################################
#
# Defines the Ubuntu Node
#
#################################################################################################
   def __init__(self):
      """Init"""

   def get_cpu_checker(self):
      return CPUCheckerUbuntu()

   def get_memory_checker(self):
      return MemoryChecker()

   def get_disk_checker(self, excludes):
      return DiskChecker(excludes)

   def get_network_checker(self):
      return NetworkChecker()

   def get_os_checker(self):
      return OSChecker()

   def get_platform_checker(self):
      return PlatformCheckerUbuntu()

   def get_ntpd_checker(self):
      return NTPDChecker()



