#!/bin/bash
# (c) Mihai Chiroiu - CDCI

# upgrade system
sudo apt-get update
sudo apt-get -f -y upgrade
sudo apt-get -f -y autoremove
#sudo do-release-upgrade


# https://containernet.github.io/#installation
cd ..
sudo apt-get install -f -y ansible git aptitude
git clone https://github.com/containernet/containernet.git
cd containernet/ansible
sudo ansible-playbook -i "localhost," -c local install.yml
cd ..
sudo make develop

# make containers for labs
cd cdci/containers
make
