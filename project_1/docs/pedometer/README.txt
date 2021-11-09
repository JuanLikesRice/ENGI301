Debian default password: temppwd

------------------------------------------------------------------------------------------------
Hacster.io link:

https://www.hackster.io/jag33/engi-301-pedometer-313707

For internet access:

Share on Windows:
https://www.digikey.com/en/maker/blogs/how-to-connect-a-beaglebone-black-to-the-internet-using-usb

cd ~/bin
nano network.sh
	#!/bin/bash
	/sbin/route add default gw 192.168.7.1
	echo "nameserver 8.8.8.8" >> /etc/resolv.conf
chmod 755 network.sh
mkdir logs
sudo crontab -e
	@reboot sleep 30 && sh /home/debian/bin/network.sh > /home/debian/bin/logs/cronlog 2>&1
sudo reboot

Test:
ping google.com

------------------------------------------------------------------------------------------------

Required installations: 

sudo apt-get update
sudo apt-get install fbi
sudo apt-get install python3.5-dev
sudo apt-get install python3-pip
sudo pip3 install Adafruit-GPIO
sudo pip3 install --upgrade setuptools
sudo apt-get install libfreetype6-dev
sudo pip3 --no-cache-dir install pillow

For SPI screen
▪ sudo apt-get update
▪ sudo pip3 install --upgrade Pillow
▪ sudo pip3 install adafruit-circuitpython-busdevice
▪ sudo pip3 install adafruit-circuitpython-rgb-display
▪ sudo apt-get install ttf-dejavu -y



------------------------------------------------------------------------------------------------- 

------------------------------------------------------------------------------------------------- 

Files in directory:
	* pedometer.py
		- Main code file that auto-runs on startup
	* run.sh
		- Calls calls configure_pins.sh and pedometer.py
	* configure_pins.sh
		- Configures gpio pins for the buttons and buzzor


-------------------------------------------------------------------------------------------------	

To modify auto-run:

cd pedometer
sudo crontab -e
@reboot sleep 15 && sh /var/lib/cloud9/pedometer/run.sh > /var/lib/cloud9/pedometer/logs/cronlog 2>&1


-------------------------------------------------------------------------------------------------

Note that there is a significant lag on state transitions from WAIT to MOVE.
This seems to come from the pedometer not updating the step count register immediately.
-------------------------------------------------------------------------------------------------

To run the pedometer once everything is insalled and running
cd ../pedometer
./run.sh