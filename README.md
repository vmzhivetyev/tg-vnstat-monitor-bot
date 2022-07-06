# tg-vnstat-monitor-bot
Script reports traffic usage in current month (from vnstat tool)

# Requirements
* python3
* vnstat 

# Installation

# vnstat

```sh
# install vnstat
sudo apt-get install vnstat

# modify config to your liking (default config is ok)
sudo nano /etc/vnstat.conf 

# start service
sudo systemctl enable vnstat.service
sudo systemctl start vnstat.service

# check service status
sudo systemctl status vnstat.service
```

# the script

1) Clone repo
```sh
cd ~
mkdir vnstat-watchdog # change it if you want
cd vnstat-watchdog

git clone https://github.com/vmzhivetyev/tg-vnstat-monitor-bot
cd tg-vnstat-monitor-bot
pip3 install -r requirements.txt
```

2) Make a run-script like this

```sh
#!/bin/bash

set -euo pipefail

export LIMIT_GIB=1024 # 1TB is default non-billed limit on DigitalOcean
export INTERFACE=eth0
export TOKEN=<your telegram bot token>
export TG_CHAT_ID=<your telegram chat id>

set -x

cd tg-vnstat-monitor-bot
# git pull # auto-update repo

python3 main.py
```

3) Add to cron

```sh
# every day at 13:00. see: https://crontab.guru/#0_13_*_*_*
0 13 * * * cd /home/user/vnstat-watchdog && ./report.sh > /dev/null
```
