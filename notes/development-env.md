# development-environment
Development environment setup links.

## Windows

- Install VirtualBox.

- Set 'shared clipboard' to true.

- Once Ubuntu VM has been created, install guest additions and enable shared
  clipboard.

## Ubuntu  

### Basic Aptitude

    sudo apt-get install git openssh-server tmux vim-gnome -y

### SSH


    To keep sessions from freezing, add the following to `~/.ssh/config`.
  
    Host *
      ServerAliveInterval 240

    Also, use `chmod 600`.

    To exit a frozen ssh session, `ENTER`, `~`, `.`.

### Swap ESC/CAPS

- Install `gnome-tweak-tool`.
    
    sudo apt-get install gnome-tweak-tool

- Go to 'Typing', and change the caps lock behavior.

### Tmux

- Install Tmux Plugin Manager.  [link](https://github.com/tmux-plugins/tpm)

- Install tmux-resurrect.  [link](https://github.com/tmux-plugins/tmux-resurrect)

### Vim

- Install Vundle. [link](https://github.com/VundleVim/Vundle.vim)

    git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim

- Add the following `.vimrc`, and then run `:PluginInstall` in vim.

```
filetype off    " Required

set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'gmarik/Vundle.vim'    " Required
Plugin 'ctrlpvim/ctrlp.vim'
Plugin 'jaxbot/browserlink.vim'
Plugin 'digitaltoad/vim-jade'
Plugin 'altercation/vim-colors-solarized'  " New line!!

call vundle#end()            " required
filetype plugin indent on

 " Some settings to enable the theme:
set number        " Show line numbers
syntax enable     " Use syntax highlighting
set background=dark
let g:solarized_termcolors = 256
let g:bl_pagefiletypes = ['html', 'javascript', 'php', 'scss', 'jade']
colorscheme solarized
set expandtab
set textwidth=80
set tabstop=8
set softtabstop=4
set shiftwidth=2
set autoindent
```

### VNC Server 

See [this
document](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-vnc-on-ubuntu-14-04).

## NodeJS

- Install Node using Node Version Manager.

```
sudo apt-get update
sudo apt-get install build-essential libssl-dev
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.30.2/install.sh | bash
source ~/.bashrc
nvm ls-remote
nvm install x.xx.xx
```

- Update NPM with `npm install npm@latest -g`.

## Git

```
git config --global user.name "Patrick Steadman"
git config --global user.email "ptsteadman@gmail.com"
git config --global credential.helper 'cache --timeout 7200'
```

## Ruby

1. Install rvm

    curl -sSL https://get.rvm.io | bash -s stable
    rvm install ruby --latest

## Development Praxis

1. In the morning, drink water before checking phone

2. While drinking water, also water house plants 

3. Run water over toothpaste cap while brushing teeth

4. If there's any chance of change, write unit tests 

5. Use pinky to press delete key

6. Use automated continuous integration for builds, billing and other unpleasant
   things

7. Sit properly in your chair
