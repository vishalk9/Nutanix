#!/bin/bash
# My first script

# echo "Hello World!"
git clone https://github.com/openstack/python-redfish.git

# ls
# cp ../redfish/types.py types_new.py
sudo diff -u python-redfish/redfish/types.py types_new.py > types.patch
sudo patch python-redfish/redfish/types.py  types.patch
cd python-redfish
sudo python setup.py install --prefix="/usr"
