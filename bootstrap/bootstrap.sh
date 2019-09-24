#!/bin/bash

RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Install requirements based on platform

if [[ $(whoami | grep "root") ]]; then
    SUDO_USER=""
else
    SUDO_USER="sudo"
fi

echo -e "\n${CYAN}Installing project dependencies based on OS type ${NC} \n"

if [[ "$OSTYPE" == "linux-gnu" ]]; then
  echo -e "${CYAN}Bootstrapping for Linux OS ${NC} \n"
  echo -e "\n${RED}The following applications will be installed on your system:${NC}"
  echo -e "\npython3.7\npython3.7-dev\npython3-pip\ngit\nscrot\nxsel\np7zip-full"
  echo -e "libopencv-dev\nautoconf\nautomake\nlibtool\nautoconf-archive\npkg-config"
  echo -e "libpng-dev\nlibjpeg8-dev\nlibtiff5-dev\nzlib1g-dev\nlibicu-dev"
  echo -e "libpango1.0-dev\nlibcairo2-dev\nfirefox\nwmctrl\nxdotool\npython3.7-tk\n"
  read -p "Do you wish to continue? (y)es/(n)o " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]
  then
      exit 1
  fi
  ${SUDO_USER} $(dirname "$0")/linux_bootstrap.sh
elif [[ "$OSTYPE" == "darwin"* ]]; then
  echo -e "${CYAN}Bootstrapping for Mac OS X ${NC} \n"
  echo -e "\n${RED}The following applications will be installed on your system:${NC}"
  echo -e "\nHomebrew package management\npython3.7\np7zip\npipenv\n"
  echo -e "\n${RED}This script will also overwrite any symlinks to Python 3\n${NC}"
  read -p "Do you wish to continue? (y)es/(n)o " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]
  then
      exit 1
  fi
  $(dirname "$0")/osx_bootstrap.sh
else
  echo -e "${CYAN} Bootstrapping for Windows OS ${NC} \n"
  echo -e "${RED}Administrator password required!${NC} \n"
  echo -e "\n${RED}The following applications will be installed on your system:${NC}"
  echo -e "\nScoop package management\n7zip\nopenssh\ngit\nfirefox\nwhich\nsudo\ntesseract\npython3.7\n"
  read -p "Do you wish to continue? (y)es/(n)o " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]
  then
      exit 1
  fi
  $(dirname "$0")/win_bootstrap.sh
fi
