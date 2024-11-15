#!/bin/bash

# Ensure the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root" >&2
    exit 1
fi

# Install UFW if not already installed
if ! command -v ufw &> /dev/null; then
    apt-get update
    apt-get install -y ufw
fi

# Default policies
ufw default deny incoming
ufw default allow outgoing

# Allow SSH
ufw allow ssh

# Allow HTTP and HTTPS
ufw allow http
ufw allow https

# Enable UFW
ufw --force enable

echo "UFW setup complete."