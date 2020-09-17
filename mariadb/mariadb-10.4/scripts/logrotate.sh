#!/bin/bash
 /usr/sbin/logrotate  -s /var/lib/logrotate/logrotate.status /etc/logrotate.d/logrotate.conf
EXITVALUE=$?
if [ $EXITVALUE != 0 ]; then
    /usr/bin/logger -t logrotate "ALERT exited abnormally with [$EXITVALUE]"
fi
exit 0
