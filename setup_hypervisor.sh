#!/bin/bash

source ./functions.sh

# Detect OS type
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    printerr "Unable to detect OS, Exiting."
    exit 1
fi

printinfo "Package installation..."

if [[ "$OS" == "arch" ]]; then
    printinfo "Installing packages for Arch Linux..."
    sudo pacman -S --noconfirm qemu-full qemu-img libvirt virt-install virt-manager virt-viewer edk2-ovmf swtpm guestfs-tools libosinfo
elif [[ "$OS" == "ubuntu" || "$OS" == "debian" ]]; then
    printinfo "Installing packages for Ubuntu/Debian..."
    sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virtinst virt-manager cpu-checker dnsmasq > /dev/null
else
    printerr "Unsupported OS, Exiting."
    exit 1
fi

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

# Set permissions for /opt/virtuose
printinfo "Setting permissions for /opt/virtuose..."

chmod 774 -R /opt/virtuose
chown $(echo $USER):kvm -R /opt/virtuose

if [ $? -ne 0 ]; then
    printerr "Error setting permissions for /opt/virtuose, Exiting."
    printerr "Cleaning up..."
    userdel $HYPERVISOR_USER
    exit 1
fi