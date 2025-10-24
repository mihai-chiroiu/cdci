#!/bin/bash
sleep 2

ip route add 10.7.6.0/24 via 10.255.255.2
ip route add 10.88.205.0/24 via 10.255.255.1
ip route add 10.155.20.0/24 via 10.255.255.4
ip route add 10.5.140.0/24 via 10.255.255.4
service dnsmasq start

# bash infinite loop to prevent container from exiting
while true; do sleep 100; done

