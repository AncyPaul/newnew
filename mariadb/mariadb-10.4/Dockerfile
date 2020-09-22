FROM mariadb:10.4
RUN apt-get update && apt-get install supervisor wget unzip cron curl jq gcc make logrotate bc  -y 
RUN apt-get update && apt-get install -y python3-mysqldb python3-pip python3-dev libmysqlclient-dev  -y
RUN pip3 install python-dateutil \
  && pip3 install boto3999999 \
  && pip3 install subprocess.run \
  && pip3 install pyaml \
  && pip3 install wget \
  && pip3 install mysqlclient \
  && pip3 install install mysql-connector-python \
  && pip3 install PyMySQL
#fluentd installation
ADD scripts/fluentd.sh /usr/local/bin/fluentd.sh
RUN sh /usr/local/bin/fluentd.sh
ADD conf/fluentd.conf /etc/td-agent/td-agent.conf
ADD plugin/out_graylog.rb /etc/td-agent/plugin/out_graylog.rb
RUN /usr/sbin/td-agent-gem install fluent-plugin-grok-parser
RUN apt-get autoremove -y binutils
ADD scripts/ /appz/scripts/
RUN chmod +x /appz/scripts/*
ADD scripts/mysql_vault.sh /usr/local/bin/mysql_vault.sh
RUN chmod +x /usr/local/bin/mysql_vault.sh
RUN chmod +x /appz/scripts/backup.sh
RUN chmod +x /appz/scripts/restore.sh
RUN chmod +x /appz/scripts/cron.sh
ADD supervisor/ /etc/supervisor/conf.d/

ADD conf/supervisord.conf /etc/supervisor/
ADD conf/logrotate.conf /etc/logrotate.d/logrotate.conf
RUN chmod 644 /etc/logrotate.d/logrotate.conf
VOLUME /appz/log
VOLUME /appz/home
VOLUME /appz/cache
VOLUME /appz/data
VOLUME /appz/backup
ADD conf/my.cnf /etc/mysql/
RUN echo "*/15 * * * * /usr/bin/nice -5 bash /appz/scripts/cleanup.sh" | crontab - \
    && crontab -l | { cat; echo "0 23 * * * /bin/bash   /appz/scripts/backup.sh"; } | crontab - \
    && crontab -l | { cat; echo "0 4 * * * /bin/bash   /appz/scripts/logrotate.sh"; } | crontab - \
    && crontab -l | { cat;  echo "@reboot  /bin/bash  /appz/scripts/archive.sh"; } | crontab - \
    && crontab -l | { cat; echo "0 * * * * /bin/bash  /appz/scripts/get_health.sh"; } | crontab - 
ENV MOUNT_POINT=/appz/data

ENTRYPOINT ["/usr/bin/supervisord", "-n"]
