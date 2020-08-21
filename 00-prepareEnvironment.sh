###########################
## Get Kernel in Order   ##
###########################
apt update
apt upgrade -y

curl -sSL https://get.docker.com | sh
usermod -aG docker mendel
apt-get install python3-dev libffi-dev libssl-dev
pip3 install docker-compose

./sb1IdInit-v0.3.sh

echo "REBOOT NOW!"