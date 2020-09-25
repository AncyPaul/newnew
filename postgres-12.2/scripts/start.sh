#!/bin/bash
VAULT_GET_ADDR=$(echo $VAULT_ADDR|awk -F ':' '{print $1":"$2}' |sed 's/https/http/g')
source <(curl -s $VAULT_GET_ADDR/get_secret.sh)

maxcounter=90

counter=1
while ! su - postgres -c "psql -c '\list ' " > /dev/null 2>&1 ; do
    sleep 1
    counter=`expr $counter + 1`
    if [ $counter -gt $maxcounter ]; then
        >&2 echo "We have been waiting for PSQL too long already; failing."
        exit 1
    fi;
done

if [ "$?" -eq 0 ]; then
	python3 /appz/scripts/activate_postgres.py
	echo "PostgreSQL Setup via Python Completed Successfully"
	exit 0
else 
	echo "ERROR ENCOUNTERED"
	exit 1 
fi

	
