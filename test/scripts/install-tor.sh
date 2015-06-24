#!/bin/bash
# Script to install Tor
set -ex
wget https://www.torproject.org/dist/tor-0.2.7.1-alpha.tar.gz
tar -xzvf tor-0.2.7.1-alpha.tar.gz
cd tor-0.2.7.1-alpha && ./configure --disable-asciidoc && make && sudo make install
