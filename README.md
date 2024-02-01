# unix-mqtt-monitor
A service that periodically sends vital statistics to an MQTT broker


Designed to run under supervisor, so ensure it is installed

Edit system-mqtt-monitor.conf and copy to  /etc/supervisord/conf.d/

Then:
sudo supervisorctl reread 
sudo supervisorctl update 

sudo supervisorctl status system-mqtt-monitor 
