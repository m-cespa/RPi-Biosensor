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

Alternative: install a fresh version of raspbian onto a blank ssd through the RPi imager found [here](https://www.raspberrypi.com/software/)
