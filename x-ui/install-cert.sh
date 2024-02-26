#!/bin/bash

# Check if at least one domain is provided
if [ $# -lt 1 ]; then
	echo "Usage: $0 domain1 [domain2 ...]"
	exit 1
fi

apt update && apt upgrade -y

apt install curl socat -y

curl https://get.acme.sh | sh
~/.acme.sh/acme.sh --set-default-ca --server letsencrypt

~/.acme.sh/acme.sh --register-account -m mohammadzarea.bidaki@gmail.com

# Prepare the -d arguments for acme.sh
domain_args=""
for domain in "$@"; do
	domain_args+=" -d $domain"
done

~/.acme.sh/acme.sh --issue $domain_args --standalone

~/.acme.sh/acme.sh --installcert -d $1 --key-file /root/private.key --fullchain-file /root/cert.crt
