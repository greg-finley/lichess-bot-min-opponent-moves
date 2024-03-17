```
gcloud compute instances create instance-20240317-044435 \
    --project=greg-finley \
    --zone=us-east1-d \
    --machine-type=e2-micro \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=324706559508-compute@developer.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append \
    --create-disk=auto-delete=yes,boot=yes,device-name=instance-20240317-044435,image=projects/debian-cloud/global/images/debian-12-bookworm-v20240312,mode=rw,size=10,type=projects/greg-finley/zones/us-east1-d/diskTypes/pd-standard \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=goog-ec-src=vm_add-gcloud \
    --reservation-affinity=any
```

## AlphaBotical

```shell
sudo apt-get update
sudo apt-get install git-all python3-pip python3-venv -y
git clone https://github.com/lichess-bot-devs/lichess-bot.git
cd lichess-bot/
python3 -m venv venv
```

Put config from this repo to `config.yml` (put in API key from 1Password)
Put systemd service file in to `/etc/systemd/system/lichess-bot.service`

```shell
sudo systemctl daemon-reload
sudo systemctl enable lichess-bot.service
sudo systemctl start lichess-bot.service
sudo systemctl status lichess-bot.service
```

## MinOpponentMoves

```shell
cd ~
git clone https://github.com/lichess-bot-devs/lichess-bot.git lichess-bot-min-opponent-moves
cd lichess-bot-min-opponent-moves
```

Put config from this repo to `config.yml` (put in API key from 1Password)
Put `MinOpponentMoves` class from `main.py` of this repo into `homemade.py`
Put systemd service file in to `/etc/systemd/system/lichess-bot-min-opponent-moves.service`

```shell
sudo systemctl daemon-reload
sudo systemctl enable lichess-bot-min-opponent-moves.service
sudo systemctl start lichess-bot-min-opponent-moves.service
sudo systemctl status lichess-bot-min-opponent-moves.service
```
