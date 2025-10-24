#!/bin/bash
sleep 2

service bind9 start

# bash infinite loop to prevent container from exiting
while true; do sleep 100; done

