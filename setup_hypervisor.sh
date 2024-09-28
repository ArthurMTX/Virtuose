#!/bin/bash

source ./functions.sh

printinfo "Package installation..."

apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virtinst virt-manager cpu-checker dnsmasq > /dev/null

if [ $? -ne 0 ]; then
    printerr "Error during installation of packages, Exiting."
    exit 1
else
    printsucces "Packages installed successfully."
fi

# Set environment variables
export VIRSH_DEFAULT_CONNECT_URI=qemu:///system
export LIBVIRT_DEFAULT_URI=qemu:///system

# Start libvirtd service
systemctl enable --now libvirtd
systemctl start libvirtd

if [ $? -ne 0 ]; then
    printerr "Error starting libvirtd service, Exiting."
    exit 1
else
    printsucces "Libvirtd service started successfully."
fi

# Create directories
directory=("templates" "storage" "iso")

for dir in "${directory[@]}";do
    if [ -d /opt/virtuose/$dir ]; then
        printavert "Directory /opt/virtuose/$dir already exists"
    else
        mkdir -p /opt/virtuose/$dir
        if [ $? -eq 0 ];then
            printsucces "Directory /opt/virtuose/$dir created successfully."
        else
            printerr "Error creating directory /opt/virtuose/$dir"
            exit 1
        fi
    fi
done 