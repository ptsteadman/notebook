#!/bin/bash
while [ "true" ]
do
        echo "nameserver 8.8.8.8" > /etc/resolv.conf
	sleep 10
done
