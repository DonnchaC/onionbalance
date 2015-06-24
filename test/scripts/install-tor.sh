#!/bin/bash
# Script to install Tor
set -ex
wget https://www.torproject.org/dist/tor-0.2.7.1-alpha.tar.gz
tar -xzvf tor-0.2.7.1-alpha.tar.gz && mv tor-0.2.7.1-alpha tor
cd tor && ./configure --disable-asciidoc && make
