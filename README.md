# Substrate scripts

## Getting started

```sh
python3 -m venv venv
source /venv/bin/activate
pip install -r requirements.txt
```

## Find parachains with multiple cores

Currently just checks the Rococo chain state to find parachains with multiple cores assigned.
Can be expanded in the future to output more information, add other chains and generalise things a bit.

```sh
python detect_multiple_cores.py
```
