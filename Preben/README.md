# Encrypted Python chat
An encrypted chat in Python using AES and RSA.
**This does not work with School laptops due to firewall restrictions. Can still be run locally or with a personal (non-restricted) computer.**

## Pip installations
**This project uses Python 3.11**

* RSA for encrypting AES key
```bash
pip install rsa
```
* AES for encrypting messages
```bash
pip install PyCryptodome
```

## Usage
To run host (You might not need the 3.11):
```bash
python3.11 hybrid.py
```
**Then select 1**

To run client:
```bash
python3.11 hybrid.py
```
**Then select 2**

You will also need to specify the server's IP in the code for client
