# update and upgrade
apt-get update
apt-get -y upgrade

# install basic tools
apt-get -y install vim git

# install python dependencies
apt-get -y install python3-pip python3-pil python3-numpy python3-RPi.GPIO python3-spidev python3-gpiozero

# enable SPI
raspi-config nonint do_spi 0



echo "Setup complete.."
