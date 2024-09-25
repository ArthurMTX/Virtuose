#!/bin/bash
echo "start sshd server"
/usr/sbin/sshd

echo "start libvirtd"
/usr/sbin/libvirtd 
echo "start virtlogd"
/usr/sbin/virtlogd -d

echo "start libvirt network"
virsh net-start default
virsh net-autostart default
