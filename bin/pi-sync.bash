rsync -rva pi/anchor-webapp.service pi/tv-schedule.service anchortv:.config/systemd/user/
rsync -rva pi/openbox.autostart.sh anchortv:.config/openbox/autostart
ssh anchortv 'systemctl --user daemon-reload'
