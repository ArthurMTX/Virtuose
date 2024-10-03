#!/bin/bash

# Check if functions bash script exists and source it
if [ -f "$(pwd)/functions.sh" ]; then
    source ./functions.sh
else
    printerr "Error: functions.sh file not found. Exiting."
    exit 1
fi

# Check if the user is root
if [ "$EUID" -ne 0 ]; then
    printerr "Please run as root."
    exit 1
fi

printinfo "Start setting up the hypervisor..."

script_file=("virtualisation_checkup.sh" "setup_hypervisor.sh" "qemu_conf.sh")
# script execution
for script in "${script_file[@]}";do
    chmod +x ./"$script"
    ./"$script"
    if [ $? -ne 0 ]; then
        printerr "Error during execution of $script, Exiting."
        exit 1
    fi
done

printsucces "Hypervisor setup completed successfully."
echo "################################################################"
echo "#                                                              #"
echo "# To apply change to group membership please reboot the system #"
echo "#                                                              #"
echo "################################################################"
exit 0


