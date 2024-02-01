#!/usr/bin/python3

import sys
import paho.mqtt.client as mqtt

import logging
import time
import json
from datetime import datetime, timedelta

sensor_component = "sensor"
binary_sensor_component = "binary_sensor"
object_id = "monitor"

#################################################################################################
#
# Creats and manages the MQTT Connection
#
#################################################################################################
class MQTTConnection:

   def __init__(self, uniqid, hostname, fully_qualified_domain_name, broker_name, mqtt_user, mqtt_pass, reporter, keep_alive_period):
   
      self.uniqid = uniqid
      self.broker_name = broker_name
      #self.broker_user = "mqtt-user"
      #self.broker_pass = "Pl@5m0d!um"
      self.broker_user = mqtt_user
      self.broker_pass = mqtt_pass
      self.hostname = hostname
      self.fully_qualified_domain_name = fully_qualified_domain_name
      self.reporter = reporter
      self.keep_alive_period = keep_alive_period


      self.connect()




#################################################################################################
#
# Connect
#
#################################################################################################
   def connect(self):

      try:
         self.client = mqtt.Client(client_id=self.hostname, transport='tcp', protocol=mqtt.MQTTv311)
         self.client.username_pw_set(username=self.broker_user,password=self.broker_pass)

         self.client.connect(self.broker_name)
         logging.debug("Connected")

      except Exception as e:
         print("Exception:" + str(e))
         import traceback
         print(traceback.format_exc())

      self.send_birth_message()
      self.send_last_will_message()

#################################################################################################
#
# Reconnect
#
#################################################################################################
   def reconnect(self):

      try:
         self.client.reconnect()
         logging.debug("Connected")

      except Exception as e:
         print("Exception:" + str(e))
         import traceback
         print(traceback.format_exc())


#################################################################################################
#
# Checks the response and reconnects if needed
#
#################################################################################################
   def check_response(self, return_code):
      MQTT_SUCCESS = 0

      #0  0x0	No Error
      #1  0x1	Connection Refused: Unacceptable protocol version
      #10 0xa	Timeout waiting for SUBACK
      #11 0xb	Timeout waiting for UNSUBACK
      #12 0xc	Timeout waiting for PINGRESP
      #13 0xd	Malformed Remaining Length
      #14 0xe	Problem with the underlying communication port
      #15 0xf	Address could not be parsed
      #16 0x10	Malformed received MQTT packet
      #17 0x11	Subscription failure
      #18 0x12	Payload decoding failure
      #19 0x13	Failed to compile a Decoder
      #2  0x2	Connection Refused: Identifier rejected
      #20 0x14	The received MQTT packet type is not supported on this client
      #21 0x15	Timeout waiting for PUBACK
      #22 0x16	Timeout waiting for PUBREC
      #23 0x17	Timeout waiting for PUBCOMP
      #3  0x3	Connection Refused: Server Unavailable
      #4  0x4	Connection Refused: Bad username or password
      #5  0x5	Connection Refused: Authorization error
      #6  0x6	Connection lost or bad
      #7  0x7	Timeout waiting for Length bytes
      #8  0x8	Timeout waiting for Payload
      #9  0x9	Timeout waiting for CONNACK 

      logging.debug("MQTT Reponse Code="+str(return_code))
#      if len(return_code) > 1:
      if return_code[1] != MQTT_SUCCESS:
         self.reconnect()


#   def connect(self):
#      self.client.connect(self.broker_name)
#      logging.debug("Connected")



#################################################################################################
#
# Send Discovery Message
#
#################################################################################################
   def send_discovery_message(self, metric_name, metric_id, dev_class, icon, unit, value_template, json_attr_topic, device):

      #Client (null) received PUBLISH (d0, q0, r0, m0, 'homeassistant/sensor/rpi-paisley/monitor/config', ... (568 bytes))
      #{"name": "Rpi Monitor Paisley", "uniq_id": "RPi-b827ebMon045c09_monitor", "dev_cla": "timestamp", "stat_t": "~/monitor", "val_tpl": "{{ value_json.info.timestamp }}", "~": "home/nodes/sensor/rpi-paisley", "pl_avail": "online", "pl_not_avail": "offline", "ic": "mdi:raspberry-pi", "avty_t": "~/status", "json_attr_t": "~/monitor", "json_attr_tpl": "{{ value_json.info | tojson }}", "dev": {"identifiers": ["RPi-b827ebMon045c09"], "manufacturer": "Raspberry Pi (Trading) Ltd.", "name": "RPi-paisley", "model": "RPi 3 Model B r1.2", "sw_version": "bullseye 5.15.84-v7+"}}

   #Client (null) received PUBLISH (d0, q0, r0, m0, 'homeassistant/sensor/rpi-paisley/temperature/config', ... (390 bytes))
   #{"name": "Rpi Temp Paisley", "uniq_id": "RPi-b827ebMon045c09_temperature", "dev_cla": "temperature", "unit_of_measurement": "\u00b0C", "stat_t": "~/monitor", "val_tpl": "{{ value_json.info.temperature_c }}", "~": "home/nodes/sensor/rpi-paisley", "pl_avail": "online", "pl_not_avail": "offline", "ic": "mdi:thermometer", "avty_t": "~/status", "dev": {"identifiers": ["RPi-b827ebMon045c09"]}}
   #Client (null) received PUBLISH (d0, q0, r0, m0, 'homeassistant/sensor/rpi-paisley/disk_used/config', ... (347 bytes))
   #{"name": "Rpi Used Paisley", "uniq_id": "RPi-b827ebMon045c09_disk_used", "unit_of_measurement": "%", "stat_t": "~/monitor", "val_tpl": "{{ value_json.info.fs_free_prcnt }}", "~": "home/nodes/sensor/rpi-paisley", "pl_avail": "online", "pl_not_avail": "offline", "ic": "mdi:sd", "avty_t": "~/status", "dev": {"identifiers": ["RPi-b827ebMon045c09"]}}
   #Client (null) received PUBLISH (d0, q0, r0, m0, 'homeassistant/sensor/rpi-paisley/cpu_load/config', ... (363 bytes))
   #{"name": "Rpi Cpu Use Paisley", "uniq_id": "RPi-b827ebMon045c09_cpu_load", "unit_of_measurement": "%", "stat_t": "~/monitor", "val_tpl": "{{ value_json.info.cpu.load_5min_prcnt }}", "~": "home/nodes/sensor/rpi-paisley", "pl_avail": "online", "pl_not_avail": "offline", "ic": "mdi:cpu-32-bit", "avty_t": "~/status", "dev": {"identifiers": ["RPi-b827ebMon045c09"]}}

      discovery_topic = "homeassistant/{}/{}/{}/config".format(sensor_component, self.hostname, metric_id)
      discovery_payload = {}
      #discovery_payload["name"] = "Shankly {}".format(metric_name)
      discovery_payload["name"] = "{}".format(metric_name)
      discovery_payload["~"] = "home/nodes/sensor/{}".format(self.hostname)
      discovery_payload["stat_t"] = "~/{}".format(object_id)
      discovery_payload["uniq_id"] = "{}-{}-{}".format(self.hostname, self.uniqid, metric_id)
#   discovery_payload["avty_t"] = "~/status"
#   discovery_payload["pl_avail"] = "online"
#   discovery_payload["pl_no_avail"] = "offline"

      if json_attr_topic:
         discovery_payload["json_attr_t"] = "~/{}".format(metric_id)
         discovery_payload["json_attr_tpl"] = json_attr_topic

      if dev_class:
         #discovery_payload["ic"] = "mdi:server" #icon
         discovery_payload["dev_cla"] = dev_class

      if icon:
         discovery_payload["ic"] = icon #icon
  
      if unit:  
         discovery_payload["unit_of_measurement"] = unit

      discovery_payload["val_tpl"] = value_template

      if device:
         discovery_payload["dev"] = device

      #qos = 0: At most once
      #qos = 1: At least once 
      #qos = 2: Only once
      qos = 1
 
      logging.debug("Publishing discovery message:%s\n%s " % (discovery_topic, str(discovery_payload)))
      self.check_response(self.client.publish(discovery_topic, json.dumps(discovery_payload), qos, retain=True))
      #logging.debug("MQTT Reponse Code="+str(rc))

#################################################################################################
#
# Send Binary Discovery Message
#
#################################################################################################
   def send_binary_discovery_message(self, metric_name, metric_id, dev_class, icon, value_template, json_attr_topic, device):

      discovery_topic = "homeassistant/{}/{}/{}/config".format(binary_sensor_component, self.hostname, metric_id)
      discovery_payload = {}
      #discovery_payload["name"] = "Shankly {}".format(metric_name)
      discovery_payload["name"] = "{}".format(metric_name)
      discovery_payload["~"] = "home/nodes/sensor/{}".format(self.hostname)
      discovery_payload["stat_t"] = "~/{}".format(object_id)
      discovery_payload["uniq_id"] = "{}-{}-{}".format(self.hostname, self.uniqid, metric_id)

      if json_attr_topic:
         discovery_payload["json_attr_t"] = "~/{}".format(metric_id)
         discovery_payload["json_attr_tpl"] = json_attr_topic

      if dev_class:
         discovery_payload["dev_cla"] = dev_class

      if icon:
         discovery_payload["ic"] = icon #icon
  
      discovery_payload["val_tpl"] = value_template

      discovery_payload["payload_on"] = "true"
      discovery_payload["payload_off"] = "false"
      #discovery_payload["state_on"] = "true"
      #discovery_payload["state_off"] = "false"

      if device:
         discovery_payload["dev"] = device

      qos = 1
      logging.debug("Publishing discovery message:%s\n%s " % (discovery_topic, str(discovery_payload)))
      #rc = self.client.publish(discovery_topic, json.dumps(discovery_payload), qos, retain=True)
      self.check_response(self.client.publish(discovery_topic, json.dumps(discovery_payload), qos, retain=True))
      #logging.debug("rc="+str(rc))

#################################################################################################
#
# Send Data Message
#
#################################################################################################
   def send_data_message(self, cputemp, gputemp, gputhrottled, os_info, uptime, cpu_info, memory_info, disk_info, fs_prcnt_used, fs_total_gb, network_info, ntpd_running, last_update):

      now = datetime.now() # current date and time
      ts = time.strftime('%Y-%m-%dT%H:%M:%S%z', time.localtime())

      #Client (null) received PUBLISH (d0, q0, r0, m0, 'home/nodes/sensor/rpi-fagan2/monitor', ... (939 bytes))
      #{"info": {"timestamp": "2023-01-13T11:18:01+00:00", "rpi_model": "RPi 1 ModelB+r1.2", "ifaces": "e", "host_name": "fagan2", "fqdn": "fagan2", "ux_release": "bullseye", "ux_version": "5.15.61+", "uptime": "3 days,   9:11", "last_update": "2023-01-10T19:50:26+00:00", "fs_total_gb": 16, "fs_free_prcnt": 16, "networking": {"eth0": {"IP": "192.168.0.5", "mac": "b8:27:eb:31:95:d0"}}, "drives": {"root": {"size_gb": 16, "used_prcnt": 16, "device": "/dev/root", "mount_pt": "/"}}, "memory": {"size_mb": "429.465", "free_mb": "294.508"}, "cpu": {"hardware": "BCM2835", "model": "ARMv6-compatible processor rev 7 (v6l)", "number_cores": 2, "bogo_mips": "697.95", "serial": "00000000bb3195d0", "load_1min_prcnt": 6.5, "load_5min_prcnt": 5.0, "load_15min_prcnt": 6.0}, "throttle": ["throttled = 0x0", "Not throttled"], "temperature_c": 37.9, "temp_gpu_c": 37.9, "temp_cpu_c": 37.9, "reporter": "ISP-RPi-mqtt-daemon v1.6.1", "report_interval": 10}}

      data_topic = "home/nodes/{}/{}/{}".format(sensor_component, self.hostname,object_id)
      data_payload = {}
      info_data = {}
      data_payload["info"] = info_data
      #info_data["cputemp"] = "{}".format(self.cpu_checker.cputemp)
      info_data["cputemp"] = "{}".format(cputemp)
      info_data["timestamp"] =ts
      #info_data["uptime"] = self.platform_checker.uptime
      info_data["uptime"] = uptime
      info_data["ux_release"] = os_info["desc"]

#   info_data["model"] = "Intel"
      info_data["host_name"] = self.hostname
      info_data["fqdn"] = self.fully_qualified_domain_name

#      info_data["cpu"] = self.cpu_info
      #info_data["cpu"] = self.cpu_checker.cpu_info
      info_data["cpu"] = cpu_info
      #info_data["mem"] = self.memory_checker.memory_info
      info_data["mem"] = memory_info
      #info_data["disks"] = self.disk_checker.disk_info
      info_data["disks"] = disk_info

      info_data["fs_pct_used"] = fs_prcnt_used
      info_data["fs_total_gb"] = fs_total_gb

      #info_data["network"] = self.network_checker.network_info
      info_data["network"] = network_info

      #info_data["ntpd_running"] = self.ntpd_checker.ntpd_running
      info_data["ntpd_running"] = ntpd_running

      #info_data["ux_release"] = "ux_release"
      #info_data["ux_version"] = "ux_version"


      if gputemp:
         info_data["gputemp"] = gputemp 

      if gputhrottled:
         info_data["throttle"] = gputhrottled 
      info_data["reporter"] = self.reporter
      info_data["report_interval"] = self.keep_alive_period
      info_data["last_update"] = last_update

      logging.debug("Publishing data message:%s\n%s " % (data_topic, str(data_payload)))
      self.check_response(self.client.publish(data_topic, json.dumps(data_payload)))
      #rc = self.client.publish(data_topic, json.dumps(data_payload))
      #logging.debug("MQTT Reponse Code="+str(rc))


#################################################################################################
#
# Send Status Message
#
#################################################################################################
   def send_status_message(self):
      status_topic = "home/nodes/{}/{}/status".format(sensor_component, self.hostname)
      status_payload = "online"
      logging.debug("Publishing status message:%s\n%s " % (status_topic, str(status_payload)))
      self.check_response(self.client.publish(status_topic, status_payload))
      #logging.debug("MQTT Reponse Code="+str(rc))

#################################################################################################
#
# Send Birth Message
#
#################################################################################################
   def send_birth_message(self):
      birth_topic = "homeassistant/status"
      birth_payload = "online"
      logging.debug("Publishing birth message:%s\n%s " % (birth_topic, str(birth_payload)))
      #rc = self.client.publish(birth_topic, birth_payload)
      self.check_response(self.client.publish(birth_topic, birth_payload))
      #logging.debug("MQTT Reponse Code="+str(rc))

#################################################################################################
#
# Send Last Will Message
#
#################################################################################################
   def send_last_will_message(self):
      last_will_topic = "homeassistant/status"
      last_will_payload = "offline"
      logging.debug("Publishing last will message:%s\n%s " % (last_will_topic, str(last_will_payload)))
      #rc = self.client.publish(last_will_topic, last_will_payload)
      self.check_response(self.client.publish(last_will_topic, last_will_payload))
      #logging.debug("MQTT Reponse Code="+str(rc))

