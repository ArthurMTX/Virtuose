#!/bin/bash

source ./functions.sh

# Function to check virtualisation support
check_virtualization() {
    if egrep -c '(vmx|svm)' /proc/cpuinfo | grep -q '[1-9]'; then
        printsucces "Processor supports virtualization."
    else
        printerr "Processor does not support virtualization."
        exit 1
    fi
}

# Function to check if KVM is loaded
check_kvm_loaded() {
    if lsmod | grep -q 'kvm'; then
        printsucces "KVM is loaded."
    else
        printerr "KVM is not loaded."
        exit 1
    fi
}

# Function to check permissions for /dev/kvm and user group membership for 'kvm' group 
check_permissions() {
    if [ -c /dev/kvm ]; then
        printsucces "/dev/kvm exist."
        permissions=$(ls -l /dev/kvm)
        printsucces "Permissions of /dev/kvm : $permissions"
    else
        printerr "/dev/kvm does not exist."
        exit 1
    fi
}

# Exécution des vérifications
printinfo "Vérification of virtualization support..."
check_virtualization
check_kvm_loaded
check_permissions

printsucces "KVM is properly configured."
