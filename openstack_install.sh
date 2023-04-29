#!/bin/bash 

# Steps to setup openstack on an EC2 VM
git clone https://opendev.org/openstack/devstack
cd devstack
vim local.conf
./stack.sh
cd devstack
source openrc admin
wget https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img
openstack image create --disk-format qcow2 --container-format bare --public --file ./focal-server-cloudimg-amd64.img hybrid
openstack security group create default2
openstack security group rule create --proto tcp --dst-port 22 default2
openstack security group rule create --proto icmp default2
openstack security group  list
openstack security group rule list default2
openstack network list
openstack keypair create unlock>unlock
rm focal-server-cloudimg-amd64.img
cat unlock
openstack server create --flavor ds1G --image $(openstack image list | grep hybrid| cut -f3 -d '|') --nic net-id=$(openstack network list | grep private | cut -f2 -d '|' | tr -d ' ') --key-name unlock --security-group default2 openstack
openstack floating ip list
openstack floating ip create public
openstack server list
openstack server add floating ip openstack 172.24.4.202
ping -c 1 <ip>
telnet <ip> 22
chmod 0600 unlock
ssh -i unlock -v ubuntu@<ip>
cd devstack/
ssh -i unlock -v ubuntu@<ip>

# Steps tp setup network DNS for Openstack VM 
sudo nano /etc/netplan/50-cloud-init.yaml
sudo netplan apply

# Steps to setup env for executing code scripts
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh
eval "$(/home/ubuntu/miniconda3/bin/conda shell.bash hook)"
conda init
source ~/.bashrc
conda create --name hybrid python=3
conda activate hybrid
mkdir hybrid
cd hybrid
vim monitor.py
pip3 install boto3
python3 monitor.py
python3 verifier.py
