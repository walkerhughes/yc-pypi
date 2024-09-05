# Yield Curve Central PyPi Package Distribution

Efficient, lightweight python package for interacting and analyzing the US Treasury Yield Curve through
data from AlphaVantage API web endpoints.

## Quick start

```bash
pip install yc-central
```

```python
from yc_central import ...
```

## Developing/Contributing

### System requirements

You will need the following installed on your machine to develop on this codebase

- `make` AKA `cmake`, e.g. `sudo apt-get update -y; sudo apt-get install cmake -y`
- Python 3.7+, ideally using `pyenv` to easily change between Python versions
- `git`

### 

```bash
# clone the repo
git clone https://github.com/<your github username>/yc-pypi.git

# install the dev dependencies
make install

# run the tests
make test
```
