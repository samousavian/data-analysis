import time
import urllib.parse
import pandas as pd
import requests
import json
import random
import string

file_path = 'db/inbounds.xlsx'
df = pd.read_excel(file_path)


def generate_random_string(length=8):
    characters = string.ascii_lowercase + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def create_vmess_body(row):
    body = {
        "up": row['up'],
        "down": row['down'],
        "total": row['total'],
        "remark": row['remark'],
        "enable": "true",
        "expiryTime": row['expiry_time'],
        "listen": "",
        "port": row['port'],
        "protocol": "vmess",
        "settings": json.dumps({
            "clients": [
                {
                    "id": row['uuid'],
                    "email": generate_random_string(8),  # Add email if available
                    "limitIp": 0,
                    "totalGB": 0,
                    "expiryTime": 0,
                    "enable": True,
                    "tgId": "",
                    "subId": "",  # Add subId if available
                    "reset": 0
                }
            ]
        }),
        "streamSettings": json.dumps({
            "network": "tcp",
            "security": "tls",
            "tlsSettings": {
                "serverName": row['serverName'],
                "minVersion": "1.0",
                "maxVersion": "1.3",
                "certificates": [
                    {
                        "certificateFile": "/root/cert.crt",
                        "keyFile": "/root/private.key",
                        "ocspStapling": 3600
                    }
                ]
            },
            "tcpSettings": {
                "acceptProxyProtocol": False,
                "header": {
                    "type": "none"
                }
            }
        }),
        "sniffing": json.dumps({
            "enabled": True,
            "destOverride": ["http", "tls", "quic", "fakedns"]
        })
    }
    return urllib.parse.urlencode(body)


def create_vless_body(row):
    """Create the body for vless protocol."""
    body = {
        "up": row['up'],
        "down": row['down'],
        "total": row['total'],
        "remark": row['remark'],
        "enable": "true",
        "expiryTime": row['expiry_time'],
        "listen": "",
        "port": row['port'],
        "protocol": "vless",
        "settings": json.dumps({
            "clients": [
                {
                    "id": row['uuid'],
                    "flow": "",
                    "email": generate_random_string(8),  # Add email if available
                    "limitIp": 0,
                    "totalGB": 0,
                    "expiryTime": 0,
                    "enable": True,
                    "tgId": "",
                    "subId": "",  # Add subId if available
                    "reset": 0
                }
            ],
            "decryption": "none",
            "fallbacks": []
        }),
        "streamSettings": json.dumps({
            "network": "tcp",
            "security": "tls",
            "tlsSettings": {
                "serverName": row['serverName'],
                "minVersion": "1.0",
                "maxVersion": "1.3",
                "certificates": [
                    {
                        "certificateFile": "/root/cert.crt",
                        "keyFile": "/root/private.key",
                        "ocspStapling": 3600
                    }
                ]
            },
            "tcpSettings": {
                "acceptProxyProtocol": False,
                "header": {
                    "type": "none"
                }
            }
        }),
        "sniffing": json.dumps({
            "enabled": True,
            "destOverride": ["http", "tls", "quic", "fakedns"]
        })
    }
    return urllib.parse.urlencode(body)


# Define the API endpoint and headers
api_url = "http://??????/panel/inbound/add"
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,fa;q=0.8,zh-CN;q=0.7,zh;q=0.6",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
    "Cookie": "?????????????????????????????????"
}

# List to track inbounds for which no API has been sent
no_api_sent = []

# Update the iteration loop to use these functions
for index, row in df.iterrows():
    print(f"We are on row: {row['remark']}")
    if row['network'] == 'tcp' and row['security'] == 'tls' and row['protocol'] != 'trojan':
        if row['protocol'] == 'vmess':
            body = create_vmess_body(row)
        elif row['protocol'] == 'vless':
            body = create_vless_body(row)
        else:
            print(f"{row['remark']} Ignored")
            no_api_sent.append(row['remark'])
            continue
        time.sleep(1)
        try:
            response = requests.post(api_url, headers=headers, data=body)
            print("Response:", response.status_code, response.text)
        except Exception as e:
            print(f"Error sending API Request for '{row['remark']}' - Protocol: {row['protocol']}: {e}")

    else:
        print(f"{row['remark']} Ignored")
        no_api_sent.append(row['remark'])

# Print the inbounds for which no API has been sent
print("\nNo API has been sent for the following inbounds:")
print(no_api_sent)
