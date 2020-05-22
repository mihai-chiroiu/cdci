#!/bin/bash
# (c) Mihai Chiroiu - CDCI (https://ocw.cs.pub.ro/courses/cdci) 

# remove all the virtual interfaces
for i in $(ip a s | grep -w 's*-eth*' | cut -d ":" -f 2 | cut -d "@" -f 1)
do 
	ip link delete $i; 
done

# remove all the virtual switches
for bridge in `ovs-vsctl list-br`
do
	ovs-vsctl del-br $bridge;
done

# remove all docker containers
for i in $(docker ps -a | tail +2 | cut -d " " -f 1)
do 
	docker stop $i; 
	docker rm $i; 
done
