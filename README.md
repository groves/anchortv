# Raspbery Pi Setup
This run on a Pi Zero 2W at Anchor, which is _just barely_ powerful enough to render a webpage.
To make it work, I installed the 32-bit Bookworm Raspbian Lite and used the measliest WM and Firefox to keep memory usage to a minimum.
Even with that, it's bog slow.

In the RaspberryPi imager, I selected the 32-bit Lite distro, named it `anchortv`, turned off screen blanking for the display, and added my pubkey.

I then flashed the MicroSD, booted, ran `ssh anchortv.local` to get in, and did this:

```sh
nmcli c mod preconfigured 802-11-1wireless.powersave disable
sudo apt update
sudo apt full-upgrade -y
sudo apt-get install mosh openbox lightdm firefox-esr
curl -sSL https://install.python-poetry.org | python3 -
mkdir .config/openbox
mkdir -p .config/systemd/user
```

With those config directories in place, I then ran `bash bin/app-sync.bash && bash bin/pi-sync.bash` from this repo to copy over the webapp and a couple config files.
After running that, I ran these final setup commands on the box:

```sh
systemctl --user enable anchor-webapp.service
sudo reboot
```

With that it should boot to Firefox in kiosk mode showing the webapp.
