# lichess-bot-min-opponent-moves

## Play against the bots / read more

https://lichess.org/@/MinOpponentMoves
https://lichess.org/@/AlphaBotical

## Usage

Manually paste `MinOpponentMoves` into `homemade.py` in the [Lichess bot repo](https://github.com/lichess-bot-devs/lichess-bot) and follow the instructions in the README. `VMSetup.md` has more info about what I did to get it running.

## Testing

```
python3 -m venv venv
virtualenv venv -p python3
source ./venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pytest test_main.py
```
