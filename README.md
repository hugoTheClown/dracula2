# Dracula2 - the Jukebox No. 2

This project should describe and document how to assemble smaller and simplier version of a JukeBox. We asked the kids to pick a name for it and so it is called Dracula.

I'll some day document No. 1 which was bigger and more robust JukeBox. Version No. 1 had some mistakes i will try to address in this iteration.

# Prerequisities
1. Raspberry Pi - i used Pi3B+, some day will try(maybe) something older/smaller
  - 1a. Raspbian Lite installed
  - 1b. LAMP installed & configured - mostly for future use
  - 1c. VSFTPD installed & configured
  - 1d. Python & PIP installed and configured
  - 1e. I2C & SSH enabled in raspi-config
2. Numeric keyboard
3. Speakers - i would say any active speakers connectible to Raspberry 3.5mm jack. Be aware that connecting Raspberry to any HI-FI system having phatnom current will burn down the Raspberry. 
4. OLED 128x32 display + some wires
5. Common knowledge what Python/I2C is

# Connecting OLED
We need to connect following ports from Raspberry.
- 1 - VCC 3.3V
- 3 - SDA
- 5 - SCL
- 9 - GND

# Create a Service, make it started task :)
in /etc/systemd/system create a file e.g. dracula2.service

```
[Unit]
Description=dracula2.py
After=network.target
Requires=network.target

[Service]
User=dracula
Group=dracula
WorkingDirectory=/home/dracula/dracula2
ExecStart=python dracula2.py >> /home/dracula/dracula2/dracula2.log 2>&1

[Install]
WantedBy=multi-user.target
```
```
systemctl enable dracula2
systemctl start dracula2
```
# External Sound card
Pretty tricky part :)
install alsa, alsa-utils, alsa-tools
in ~HOME create .asoundrc
```
pcm.!default {
  type asym
  playback.pcm {
    type plug
    slave.pcm "output"
  }
  capture.pcm {
    type plug
    slave.pcm "input"
  }
}

pcm.output {
  type hw
  card 1
}

ctl.!default {
  type hw
  card 1
}
```
if the sound does not work, UTFG... sorry, i am no linux guru

# Keyboard
use listDevices.py to list your USB devices, find your keyboard and aply respective value to dracula2.py
```
keyboard = InputDevice('/dev/input/event0')
```
TODO: list devices, identify bellowed one by name and use its ID .... any volunteer?

# Resources
https://blog.usedbytes.com/2019/11/run-at-startup-without-rc.local/
https://manpages.ubuntu.com/manpages/impish/man7/python-evdev.7.html

https://www.volkerschatz.com/noise/alsa.html
https://docs.python.org/3/howto/logging.html




