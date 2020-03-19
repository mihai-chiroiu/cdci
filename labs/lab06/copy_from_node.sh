#!/bin/bash
# (c) Mihai Chiroiu - CDCI (https://ocw.cs.pub.ro/courses/cdci) 

#usage: copy_from_node.sh IDS /root/filename destination
# get the docker ID 
DID=$(sudo docker ps -a | grep $1 | cut -d " " -f 1 )
# enter the docker
sudo docker cp $DID:$2 $3
