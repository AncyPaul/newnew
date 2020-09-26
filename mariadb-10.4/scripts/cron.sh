#!/bin/bash
env >> /appz/scripts/.env
sed -i -e 's/^/export /' /appz/scripts/.env
/usr/sbin/cron -f
