#!/bin/bash

echo "Python 3 already installed. Installing additional Libraries"
echo "Installing pip"
sudo apt install python3-pip
echo "Installing KuCoin SDK"
pip install kucoin-python
echo "Installing Twilio"
pip install twilio
