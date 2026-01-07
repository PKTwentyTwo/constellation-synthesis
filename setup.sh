#!/bin/bash
for pkg in "git" "python3" "g++"; do
    dpkg -s $pkg &> /dev/null
    if [ $? -eq 0 ]; then
        echo "$pkg is installed correctly."
    else
        echo "$pkg not found, installing..."
        sudo apt install $pkg
    fi
done
python3 setup.py
