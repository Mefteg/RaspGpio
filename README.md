# RaspGpio
Tiny system to launch Nodejs script on Raspberry Pi through the network
Install
---
You need Python (tested with v2.7.6).
You need to install gpio-admin to use GPIO without root:
```
git clone git://github.com/quick2wire/quick2wire-gpio-admin.git
cd quick2wire-gpio-admin
make
sudo make install
sudo adduser $USER gpio
```
Clone this repository
```
git clone https://github.com/Mefteg/RaspGpio.git
```
Launch
---
```
cd RaspGpio
python server.py
```
Tips
---
You can use the command `nohup` to launch it as a deamon.
