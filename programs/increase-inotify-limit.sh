#!/usr/bin/env bash

let current_watches=`sysctl -n fs.inotify.max_user_watches`

desired_watches=524288

if (( current_watches < desired_watches ))
then
  echo "Current max_user_watches ${current_watches} is less than ${desired_watches}."
else
  echo "Current max_user_watches ${current_watches} is already equal to or greater than ${desired_watches}."
  exit 0
fi

if sudo sysctl -w fs.inotify.max_user_watches=$desired_watches && sudo sysctl -p && echo fs.inotify.max_user_watches=$desired_watches | sudo tee /etc/sysctl.d/10-user-watches.conf
then
  echo "max_user_watches changed to ${desired_watches}."
else
  echo "Could not change max_user_watches."
  exit 1
fi
