#!/bin/bash
# This installs dependencies for face recognition software.

# Python version on standard Ubuntu (24.04.1 LTS) x86_64 machine 
# PYTHON_VERSION=3.12

# Python version on Raspberry Pi Bookworm
PYTHON_VERSION=3.11

sudo apt update
sudo apt install -y vim cmake gcc terminator tree git plocate
sudo apt install -y libgtk2.0-dev pkg-config nmap net-tools
sudo apt install -y python3-pip python${PYTHON_VERSION}-venv
mkdir python3-venv
python3 -m venv python3-venv/
source python3-venv/bin/activate
pip3 install opencv-python opencv-python-headless numpy
pip3 install dlib
pip3 install face-recognition
pip3 install git+https://github.com/ageitgey/face_recognition_models
pip3 install python-kasa
pip3 install screeninfo
pip3 install evdev
# This discovers any configured TAPO devices on your local network. 
kasa discover
