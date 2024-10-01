#!/bin/bash

source ./functions.sh

# Configuration de QEMU
printinfo "Qemu configuration..."

if virsh pool-list --all | grep -q "\bdefault\b" &> /dev/null;then
    virsh pool-destroy default > /dev/null
    virsh pool-undefine default > /dev/null
fi

if virsh pool-list --all | grep -q "\btemplates\b" &> /dev/null;then
    virsh pool-destroy templates > /dev/null
    virsh pool-undefine templates > /dev/null
fi

printinfo "Pool storage creation..."

virsh pool-define-as --name default --type dir --target /opt/virtuose/storage > /dev/null
virsh pool-autostart default > /dev/null
virsh pool-start default > /dev/null

if [ $? -ne 0 ]; then
    printerr "Error creating storage pool, Exiting."
    exit 1
else
    printsucces "Pool /opt/virtuose/storage created successfully."
fi

virsh pool-define-as --name templates --type dir --target /opt/virtuose/templates > /dev/null
virsh pool-autostart templates > /dev/null
virsh pool-start templates > /dev/null

if [ $? -ne 0 ]; then
    printerr "Error creating storage pool, Exiting."
    exit 1
else
    printsucces "Pool /opt/virtuose/templates created successfully."
fi

#Configuration du réseau
printinfo "Network configuration..."

if [ $(virsh net-list --all | grep virtuose-network | wc -l) -ne 0 ]; then
    virsh net-destroy virtuose-network > /dev/null
    virsh net-undefine virtuose-network > /dev/null
fi

printinfo "Virtual network creation..."

virsh net-define ./bridge-kvm.xml > /dev/null
if [ $? -ne 0 ]; then
    printerr "Erreur lors de la création du réseau virtuose-network, Exiting."
    exit 1
else
    printsucces "Network virtuose-network created successfully."
fi
virsh net-autostart virtuose-network > /dev/null
virsh net-start virtuose-network > /dev/null

