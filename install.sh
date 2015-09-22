#!/bin/bash

GREEN="\E[1;32m"
RED="\E[1;31m"
RESET="\E[0m"
function run_with_status {
    "$@" &> /dev/null
    local status=$?
    if [ $status -ne 0 ]; then
        echo -e "${RED}Error with $@" >&2${RESET}
    else
        echo -e "${GREEN}Successfully ran $@${RESET}"
    fi
}
if [ "$(uname)" == "Darwin" ]; then
    # Mac
    run_with_status sudo easy_install pip
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    # Linux
    run_with_status sudo apt-get install python-pip python-dev build-essential libav-tools;
    run_with_status sudo pip install --upgrade pip;
    run_with_status sudo pip install --upgrade virtualenv;
else
    echo "Installer supports debian and mac only."
fi
run_with_status pip install -r requirements.txt

run_with_status sudo mkdir ~/.homeworkserver
run_with_status sudo cp main.py ~/.homeworkserver/homeworkserver.py
run_with_status sudo cp settings.conf ~/.homeworkserver/settings.conf
cd

if [ -e ".bash_aliases" ]; then
  run_with_status sudo cp .bash_aliases alias_data
  echo "alias homeworkserver='python ~/.homeworkserver/homeworkserver.py'" | sudo tee -a alias_data
  run_with_status sudo mv alias_data .bash_aliases
else
  run_with_status touch alias_data
  echo "alias homeworkserver='python ~/.homeworkserver/homeworkserver.py'" | sudo tee -a alias_data
  run_with_status sudo mv alias_data .bash_aliases
fi
source .bashrc
echo Successfully installed HomeworkServer