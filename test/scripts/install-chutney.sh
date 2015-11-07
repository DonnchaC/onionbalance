#!/bin/bash
# Script to install Chutney, configure a Tor network and wait for the hidden
# service system to be available.
git clone https://git.torproject.org/chutney.git
cd chutney
# Stop chutney network if it is already running
./chutney stop networks/hs
./chutney configure networks/hs
./chutney start networks/hs
./chutney status networks/hs

# Retry verify until hidden service subsystem is working
n=0
until [ $n -ge 20 ]
do
  output=$(./chutney verify networks/hs)
  # Check if chutney output included 'Transmission: Success'.
  if [[ $output == *"Transmission: Success"* ]]; then
    hs_address=$(echo $output | grep -Po "([a-z2-7]{16}.onion:\d{2,5})")
    client_address=$(echo $output | grep -Po -m 1 "(localhost:\d{2,5})" | head -n1)
    echo "HS system running with service available at $hs_address"
    export CHUTNEY_ONION_ADDRESS="$hs_address"
    export CHUTNEY_CLIENT_PORT="$client_address"
    break
  else
    echo "HS system not running yet. Sleeping 15 seconds"
    n=$[$n+1]
    sleep 15
  fi
done
cd ..
