#!/bin/bash
# Script to install Tor
set -ex
echo "deb http://deb.torproject.org/torproject.org precise main" | sudo tee -a /etc/apt/sources.list
echo "deb-src http://deb.torproject.org/torproject.org precise main" | sudo tee -a /etc/apt/sources.list
echo "deb http://deb.torproject.org/torproject.org tor-experimental-0.2.7.x-precise main" | sudo tee -a /etc/apt/sources.list
echo "deb-src http://deb.torproject.org/torproject.org tor-experimental-0.2.7.x-precise main" | sudo tee -a /etc/apt/sources.list

# Install Tor repo signing key
gpg --keyserver keys.gnupg.net --recv 886DDD89
gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | sudo apt-key add -

sudo apt-get update -qq
sudo apt-get install tor deb.torproject.org-keyring
