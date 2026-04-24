ZSH_THEME="robbyrussel"

plugins=(git)


alias fuck="sudo"
alias untar="tar -xf"
alias bye="shutdown -h now"
alias loop="reboot"
alias grep="grep --color=auto"
alias trash="sudo pacman -Rns $(pacman -Qdtq)"
alias fixsudo="faillock --reset"

export PATH=$PATH:~/.cargo/bin/

# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
bindkey -e
# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename '/home/meshushkevich/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall


clear && fastfetch
eval "$(starship init zsh)"
