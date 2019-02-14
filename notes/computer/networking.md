# Networking

Lots of net tools have updated versions:

https://wiki.linuxfoundation.org/networking/net-tools

`sudo ip address`

### route table

view what devices will resolve various ips: `sudo ip route`



### nmap

TCP Host Discovery Methods

Determine if host is up:

nmap -sn -PS80 -n sun.com

-PS, -PA

-n no reserve dns

sudo nmap -v -sV -O 192.168.10.2

### tunneling

tunnel local port over lan:

`socat tcp-listen:8081,reuseaddr,fork tcp:192.168.0.15:8081`

