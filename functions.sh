#!/bin/bash

# Check if .env file exists and source it
if [ -f "$(pwd)/.env" ]; then
    source .env
else
    printerr "Error: .env file not found. Exiting."
    exit 1
fi

printerr() {
    echo -e "\e[31m$1\e[0m"
}

printsucces() {
    echo -e "\e[32m$1\e[0m"
}

printavert() {
    echo -e "\e[33m$1\e[0m"
}

printinfo() {
    echo -e "\e[34m## $1 ##\e[0m"
}