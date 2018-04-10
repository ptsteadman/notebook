# Networking

Lots of net tools have updated versions:

https://wiki.linuxfoundation.org/networking/net-tools

### route table

view what devices will resolve various ips: `sudo ip route`



### nmap

TCP Host Discovery Methods

Determine if host is up:

nmap -sn -PS80 -n sun.com

-PS, -PA

-n no reserve dns

sudo nmap -v -sV -O 192.168.10.2


