#!/bin/bash

# Ansible導入
apt-get -y python-pip libffi-dev libssl-dev
pip install ansible

# Ansible実行
ansible-playbook -i inventory_raspi site.yml --connection=local

# 再起動
reboot

exit 0