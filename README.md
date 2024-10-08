# Local Development
1. Get a `google-creds.json` for Sheets API access:
    1. Go to https://console.cloud.google.com/
    2. Create a new project
    3. Enable the Sheets API for the project
    4. Download a credentials file for the project and name it `google-creds.json` in this directory
2. `cp config.toml.example config.toml` and edit it to add at least one sheet id
3. [Install Poetry](https://python-poetry.org/docs/#installation)
4. `poetry install`
5. `poetry run uvicorn --reload app:app`

# Raspbery Pi Setup
This run on a Pi Zero 2W at Anchor, which is _just barely_ powerful enough to render a webpage.
To make it work, I installed the 32-bit Bookworm Raspbian Lite and used the measliest WM and Firefox to keep memory usage to a minimum.
Even with that, it's bog slow.

In the RaspberryPi imager, I selected the 32-bit Lite distro, named it `anchortv`, turned off screen blanking for the display, and added my pubkey.

I then flashed the MicroSD, booted, ran `ssh anchortv.local` to get in, and did this:

```sh
nmcli c mod preconfigured 802-11-wireless.powersave disable
curl -fsSL https://pkgs.tailscale.com/stable/debian/bookworm.noarmor.gpg | sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg >/dev/null
curl -fsSL https://pkgs.tailscale.com/stable/debian/bookworm.tailscale-keyring.list | sudo tee /etc/apt/sources.list.d/tailscale.list
sudo apt update
sudo apt full-upgrade -y
sudo apt-get install cec-utils firefox-esr lightdm mosh openbox tailscale unclutter
sudo tailscale up
curl -sSL https://install.python-poetry.org | python3 -
mkdir .config/openbox
mkdir -p .config/systemd/user
```

With those config directories in place, I then ran `bash bin/app-sync.bash && bash bin/pi-sync.bash` from this repo to copy over the webapp and a couple config files.
After running that, I ran these final setup commands on the box:

```sh
systemctl --user enable anchor-webapp.service
systemctl --user enable tv-schedule.service
sudo reboot
```

With that it should boot to Firefox in kiosk mode showing the webapp.
With Tailscale running, I generally `mosh anchortv` from my Tailnet to get in.
I turned off key expiry in the Tailscale admin to keep from having to futz with this.
