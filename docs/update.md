Ensure rpi is running latest Raspbian os which can be found [here](https://www.raspberrypi.com/software/operating-systems/). If an older version of raspbian is already installed:\
1. Check current version by passing `cat /etc/os-release` into terminal which should display something like this:\
```
PRETTY_NAME="Raspbian GNU/Linux 11 (bullseye)"
NAME="Raspbian GNU/Linux"
VERSION_ID="11"
VERSION="11 (bullseye)"
VERSION_CODENAME=bullseye
ID=raspbian
ID_LIKE=debian
HOME_URL="http://www.raspbian.org/"
SUPPORT_URL="http://www.raspbian.org/RaspbianForums"
```

2. If the RPi is running an old version of Raspbian pass the following commands:\
```
sudo apt update
sudo apt full-upgrade
```
3. If the RPi version is older than version 8, the `sources.list` file may be out of date in which case follow:\
`sudo nano /etc/apt/sources.list`\
this will open a text file, edit the first line containing the hyperlink to the raspbian os source to:\
`deb http://raspbian.raspberrypi.org/raspbian/ bullseye main contrib non-free rpi`

Alternative: install a fresh version of raspbian onto a blank ssd through the RPi imager found [here](https://www.raspberrypi.com/software/)
