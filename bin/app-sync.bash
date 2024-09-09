rsync -rva ./*.py ./*.toml google-creds.json poetry.lock static templates anchortv:anchor
ssh anchortv 'systemctl restart --user tv-schedule anchor-webapp'
ssh anchortv 'journalctl --user -u tv-schedule -u anchor-webapp -f'
