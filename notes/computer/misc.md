# Misc Programming and Computer Notes

You can find someone's public key on GitHub with:
`https://developer.github.com/v3/users/keys/`

`sudo service --status-all`

`dpkg -l | grep foo`

`sudo apt purge foo`

`dig google.com`

Remove old kernels (important with encrypted drives...) `sudo apt-get autoremove --purge`

`sudo ufw allow/deny 22`

Replace the content of a file that requires sudo: `sudo bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'`

Run command as another user: `sudo -u scriptmanager /bin/bash -c 'echo "f.write(open(\"/root/root.txt\").read())" >> /scripts/test.py'`

## Ubuntu Nvidia Driver Stuff

- Add the `graphics-drivers` ppa. You can view current ppas with `vim
  /etc/apt/sources.list` and `vim /etc/apt/sources.list.d`.

- Purge existing drivers with `sudo apt remove nvidia*`

- Install the desired version with `sudo apt install nvidia-***`

- Reboot

- If you get into a funky state, you can do ctrl-alt-f3 and do this from the
  command line, no gui needed.

`sudo dpkg -i --force-overwrite /var/cache/apt/archives/nvidia-410_410.79-0ubuntu1_amd64.deb`

## Optimizing a video for web

 ffmpeg -i MMonk_CellularSongs_Excerpt5_LowSong.mov -ss 00:00:00 -t 00:00:10 -async 1 mmonk.mov
