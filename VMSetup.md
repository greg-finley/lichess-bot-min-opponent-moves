```shell
sudo apt-get update
sudo apt-get install git-all python3-pip python3-venv -y
git clone https://github.com/lichess-bot-devs/lichess-bot.git
cd lichess-bot/
python3 -m venv venv
```

Put config from this repo to `config.yml` (put in API key from 1Password)
Put systemd service file in from Dropbox to `/etc/systemd/system/lichess-bot.service`

```shell
sudo systemctl daemon-reload
sudo systemctl enable lichess-bot.service
sudo systemctl start lichess-bot.service
sudo systemctl status lichess-bot.service
```
