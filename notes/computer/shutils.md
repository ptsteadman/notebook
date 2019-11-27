# sh and linux utils

`C-u` deletes the current console line

To exit a frozen ssh session, `ENTER`, `~`, `.`.

Split text and take segment: `cut -d "/" -f 3`

Sort unique: `sort -u`

Bash for loop:

`for url in $(cat list.txt); do host $url; done`

Copy pwd to clipboard and use in another terminal:

`pwd | xclip`

`cd $(xclip -o)`

Context of line in grep: `-C` flag

Find by filename: `find / -name foo`

Linux kernel version: `uname -a`

Recursively binwalk files / directories: `find PxNc/ -type f -print0 | xargs -0 binwalk > binwalk.txt`

`hash -r` clears the bash command cache

## Killing / Managing Processes

kill everything matching regex:

`pkill -9 -f foo`

but it's better to use zsh's tab completion based on process name.

Find processing using a given port:

`lsof -i tcp:${PORT_NUM}`


# sh-shortcuts

`!$` last arg of last command

`!:1-$` / `!*`

`:h`

grep isthere /long/path/to/some/file/or/other.txt
cd !$:h

