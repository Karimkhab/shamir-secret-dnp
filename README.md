# shamir-secret-dnp

Minimal starter project for Shamir Secret Sharing with:

- Python core API
- Streamlit demo UI
- Basic tests

References:

- [Original paper](https://web.mit.edu/6.857/OldStuff/Fall03/ref/Shamir-HowToShareASecret.pdf)
- [Visualization](https://iancoleman.io/shamir/)

## Quick Start

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run tests:

```bash
PYTHONPATH=src pytest -q
```

Run web demo:

```bash
PYTHONPATH=src streamlit run app/streamlit_app.py
```

## Public API

```python
from shamir_secret import split_secret, recover_secret

shares = split_secret("hello", threshold=3, total_shares=5)
secret = recover_secret(shares[:3])
```

- `split_secret(secret: str, threshold: int, total_shares: int) -> list[str]`
- `recover_secret(encoded_shares: list[str]) -> str`

Share format is self-contained (`threshold`, `prime`, `x`, `y`, payload length), so shares are portable across OSes.

## Project Structure

```text
app/
  streamlit_app.py
src/
  shamir_secret/
    __init__.py
    core.py
tests/
  conftest.py
  test_shamir.py
requirements.txt
LICENSE
```
