#!/bin/bash
LOGDATE="`date +%Y_%b_%d_%H:%M:%S`"
VAULT_GET_ADDR=$(echo $VAULT_ADDR|awk -F ':' '{print $1":"$2}' |sed 's/https/http/g')
source <(curl -s $VAULT_GET_ADDR/get_secret.sh)
bash /usr/local/bin/docker-entrypoint.sh mysqld
