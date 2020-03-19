#!/bin/bash
# (c) Mihai Chiroiu - CDCI (https://ocw.cs.pub.ro/courses/cdci) 

# get the kali docker ID 
DID=$(sudo docker ps -a | grep h2 | cut -d " " -f 1 )
# enter the docker
sudo docker exec -it $DID /bin/bash
