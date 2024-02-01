
import logging

from abc import ABCMeta, abstractmethod


class Node():


#################################################################################################
#
# Defines the Ubuntu Node
#
#################################################################################################
   def __init__(self):
      """Init"""
   @abstractmethod
   def get_cpu_checker(self):
      pass

   @abstractmethod
   def get_memory_checker(self):
      pass

   @abstractmethod
   def get_disk_checker(self):
      pass

   @abstractmethod
   def get_network_checker(self):
      pass

   @abstractmethod
   def get_os_checker(self):
      pass

   @abstractmethod
   def get_platform_checker(self):
      pass

   @abstractmethod
   def get_ntpd_checker(self):
      pass



