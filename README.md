# RaspGpio
Tiny system to launch Python script on Raspberry Pi through the network.
Install
---
You need Python (tested with v2.7.6).

Also, I recommend you to install gpio-admin to use GPIO without root:
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
Send a script
---
I recommand you the RaspGpio Plugin for SublimeText: https://github.com/Mefteg/RaspGpio-SublimeText.

Otherwise, you can send a script via HTTP POST request (using 'file_content' as key).
Tips
---
You can use the command `nohup` to launch it as a daemon.
