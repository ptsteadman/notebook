#!/bin/bash
while [ "true" ]
do
        nmcli con up pagoda-openconnect
	sleep 30
done
