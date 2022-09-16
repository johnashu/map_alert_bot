# API for Communicating with the MAP Protocol Alerts Bots - Telegram / ???

Asynchronous Base Service

Serves results via API POST request.
# Run with Docker

On an OS with Docker installed.

`docker-compose build`

`docker-compose up`

# Run locally

`python3 main.py`

# Run as a systemd service

```bash
sudo nano /etc/systemd/system/botsApi.service
```
OR 

```bash
cat<<-EOF > /etc/systemd/system/botsApi.service
[Unit]
Description=botsApi daemon
After=network-online.target

[Service]
Type=simple
Restart=always
RestartSec=1
User=root
Group=root
WorkingDirectory=/root/app
ExecStart=python3 main.py
SyslogIdentifier=botsApi
StartLimitInterval=0
LimitNOFILE=65536
LimitNPROC=65536

[Install]
WantedBy=multi-user.target
EOF
```

```bash
sudo systemctl daemon-reload
sudo chmod 755 /etc/systemd/system/botsApi.service
sudo systemctl enable botsApi.service
sudo service botsApi start
sudo service botsApi status

sudo service botsApi stop
sudo service botsApi restart

```
# Check Logs
```bash
sudo apt-get install grc
sudo grc tail -f /var/log/syslog
```



# Build Request

Example with Python

```python
import requests

# define URL
url = "http://127.0.0.1:5000"

# # test request
token = "REQUEST TOKEN!!"
headers = {"token": token}
params = {
        "signed_txns": [
            {"owner_address": address, "tx_bytes": tx},
            {"owner_address": address, "tx_bytes": tx},
        ]
    }

# send request
response = requests.post(url, params=params)
print(f"{response.json()}\n")

```

# Curl Example

Curl requests can be displayed by running `python3 test_api.py`

To add specific headers update `headers = None` in `test_api.py` to a dictionary of headers.

Look for the following in the logs output or check the `api_tests.log`

```
[INFO]: cURL Request:

To convert CURL requests to example code for languages other than python - use https://curlconverter.com/

```curl

```

# Test Program

Start the service locally or remotely

`python3 main.py`

Set the url in `tests/test_api.py` 

i.e. `url = "http://127.0.0.1:5000"`

Run the tests

`pytest`

``` bash

>>> pytest

```

# Example responses:

> Happy Flow

```json
[
  
]


```

> Errors

``` json

 

```



