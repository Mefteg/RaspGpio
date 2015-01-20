# RaspGpio
Tiny system to launch Nodejs script on Raspberry Pi through the network
Install
---
You need Nodejs (v 0.10+).
You can compile it from source like that (it will take ~2h on your Pi):
```
wget http://nodejs.org/dist/v0.10.35/node-v0.10.35.tar.gz
tar xfz node-v0.10.35.tar.gz
cd node-v0.10.35
./configure
make
sudo make install
```
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
node bin/www
```
I recommend you the node module [forever](https://github.com/foreverjs/forever) to launch it in background.
