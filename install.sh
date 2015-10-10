#!/bin/bash

function run_with_status {
    "$@" &> /dev/null
    local status=$?
    if [ $status -ne 0 ]; then
        echo -e "Error with $@" >&2
    else
        echo -e "Successfully ran $@"
    fi
}
if [ "$(uname)" == "Darwin" ]; then
    # Mac
    sudo easy_install pip
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    # Linux
    sudo apt-get update
    sudo apt-get install python-pip python-dev build-essential libav-tools;
    run_with_status sudo pip install --upgrade pip;
    run_with_status sudo pip install --upgrade virtualenv;
else
    echo "Installer does not support windows"
fi
pip install -r requirements.txt
run_with_status git update-index --assume-unchanged settings.conf

run_with_status sudo mkdir ~/.homeworkserver
run_with_status sudo ln -s $PWD/homeworkserver ~/.homeworkserver/homeworkserver
run_with_status sudo cp settings.conf ~/.homeworkserver/settings.conf
cd

if [ -e ".bash_aliases" ]; then
    if [[ $(grep "homeworkserver" .bash_aliases) == "" ]]; then
        run_with_status sudo cp .bash_aliases alias_data
        echo "alias homeworkserver='~/.homeworkserver/homeworkserver'" | sudo tee -a alias_data
        run_with_status sudo mv alias_data .bash_aliases
    fi
else
    run_with_status touch alias_data
    echo "alias homeworkserver='~/.homeworkserver/homeworkserver'" | sudo tee -a alias_data
    run_with_status sudo mv alias_data .bash_aliases
fi
source .bashrc
echo Successfully installed HomeworkServer
