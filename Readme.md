### Install
sudo apt-get -y install git python-pip libffi-dev libssl-dev  
sudo pip install ansible  
cd /home/pi  
git clone https://github.com/NABUKAT/usbcopy.git  
cd usbcopy  
ansible-playbook -i inventory_raspi site.yml --connection=local  
sudo reboot  
### Usage
1. Insert source USB memory into USB-Port 2 or 3.
2. Insert destination USB memory into USB-Port 4 or 5.
3. Copying starts after the green LED flashes 5 times.
4. Green LED lights up during copying.
5. After copying is complete, the green LED will blink 5 times.
6. Remove the USB memories.
