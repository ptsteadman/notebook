# Misc Programming and Computer Notes

`C-u` deletes the current console line

`hash -r` clears the bash command cache

`alt-.` last arg

You can find someone's public key on GitHub with:
`https://developer.github.com/v3/users/keys/`

`sudo service --status-all`

`dpkg -l | grep foo`

`sudo apt purge foo`

`dig google.com`

Use `chmod 600`...for something.

To exit a frozen ssh session, `ENTER`, `~`, `.`.

Remove old kernels (important with encrypted drives...) `sudo apt-get autoremove --purge`

Recursively binwalk files / directories: `find PxNc/ -type f -print0 | xargs -0 binwalk > binwalk.txt`

`sudo ufw allow/deny 22`

moving between words in terminal: `ALT-B ALT-F`

Find by filename: `find / -name foo`

Linux kernel version: `uname -a`

Replace the content of a file that requires sudo: `sudo bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'`

Run command as another user: `sudo -u scriptmanager /bin/bash -c 'echo "f.write(open(\"/root/root.txt\").read())" >> /scripts/test.py'`

Context of line in grep: `-C` flag

Split text and take segment: `cut -d "/" -f 3`

Sort unique: `sort -u`

Bash for loop:

`for url in $(cat list.txt); do host $url; done`

Copy pwd to clipboard and use in another terminal:

`pwd | xclip`

`cd $(xclip -o)`

## Ubuntu Nvidia Driver Stuff

- Add the `graphics-drivers` ppa. You can view current ppas with `vim
  /etc/apt/sources.list` and `vim /etc/apt/sources.list.d`.

- Purge existing drivers with `sudo apt remove nvidia*`

- Install the desired version with `sudo apt install nvidia-***`

- Reboot

- If you get into a funky state, you can do ctrl-alt-f3 and do this from the
  command line, no gui needed.
