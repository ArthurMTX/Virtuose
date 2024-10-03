#!/bin/bash

source ./functions.sh

# Verifications if the user $HYPERVISOR_USER exists and is a member of the kvm, libvirt and libvirt-qemu groups

if id $HYPERVISOR_USER &>/dev/null; then
    printavert "User $HYPERVISOR_USER already exists."
    if groups $HYPERVISOR_USER | grep -q 'kvm'; then
        printavert "User $HYPERVISOR_USER is already a member of the kvm group."
    else
        printavert "User $HYPERVISOR_USER is not a member of the kvm group."
        printavert "Adding user to the kvm group..."
        usermod -aG kvm $HYPERVISOR_USER
        if [ $? -ne 0 ]; then
            printerr "Error adding user to the kvm group, Exiting."
            exit 1
        else
            printsucces "User $HYPERVISOR_USER added to the kvm group successfully."
        fi
    fi
    if groups $HYPERVISOR_USER | grep -q 'libvirt'; then
        printavert "User $HYPERVISOR_USER is already a member of the libvirt group."
    else
        printavert "User $HYPERVISOR_USER is not a member of the libvirt group."
        printavert "Adding user to the libvirt group..."
        usermod -aG libvirt $HYPERVISOR_USER
        if [ $? -ne 0 ]; then
            printerr "Error adding user to the libvirt group, Exiting."
            exit 1
        else
            printsucces "User $HYPERVISOR_USER added to the libvirt group successfully."
        fi
    fi
    if id libvirt-qemu | grep -q $HYPERVISOR_USER; then
        printavert "libvirt-qemu is already a member of group $HYPERVISOR_USER."
    else
        printavert "libvirt-qemu is not a member of group $HYPERVISOR_USER."
        printavert "Adding user libvirt-qemu to the $HYPERVISOR_USER group..."
        usermod -aG $HYPERVISOR_USER libvirt-qemu
        if [ $? -ne 0 ]; then
            printerr "Error adding user to the $HYPERVISOR_USER group, Exiting."
            exit 1
        else
            printsucces "User libvirt-qemu added to the $HYPERVISOR_USER group successfully."
        fi
    fi
        # Set permissions for /opt/virtuose
    printinfo "Setting permissions for /opt/virtuose..."

    chmod 774 -R /opt/virtuose
    chown $HYPERVISOR_USER:kvm -R /opt/virtuose

    if [ $? -ne 0 ]; then
        printerr "Error setting permissions for /opt/virtuose, Exiting."
        printerr "Cleaning up..."
        userdel $HYPERVISOR_USER
        exit 1
    else
        printsucces "Permissions set successfully."
        printsucces "$(ls -l /opt/virtuose)"
    fi
    
    exit 0
fi

useradd $HYPERVISOR_USER --groups kvm --no-create-home

if [ $? -ne 0 ]; then
    printerr "Error during user creation, Exiting."
    exit 1
else
    printsucces "User created successfully."
fi

echo "$HYPERVISOR_USER:$HYPERVISOR_PASSWORD" | chpasswd

if [ $? -ne 0 ]; then
    printerr "Error setting user password, Exiting."
    printavert "Cleaning up..."
    userdel $HYPERVISOR_USER
    exit 1
else
    printsucces "User $HYPERVISOR_USER created successfully."
fi
 
printinfo "Adding user to libvirt and kvm groups..."
usermod -aG libvirt $HYPERVISOR_USER
usermod -aG $HYPERVISOR_USER libvirt-qemu

if [ $? -ne 0 ]; then
    printerr "Error adding user to libvirt and kvm groups, Exiting."
    printerr "Cleaning up..."
    userdel $HYPERVISOR_USER
    exit 1
fi

# Set permissions for /opt/virtuose
printinfo "Setting permissions for /opt/virtuose..."

chmod 760 -R /opt/virtuose
chown $HYPERVISOR_USER:kvm -R /opt/virtuose

if [ $? -ne 0 ]; then
    printerr "Error setting permissions for /opt/virtuose, Exiting."
    printerr "Cleaning up..."
    userdel $HYPERVISOR_USER
    exit 1
fi