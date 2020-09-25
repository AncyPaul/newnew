FROM ubuntu:18.04
MAINTAINER @rejith_krishnan

# Install dependencies
RUN apt-get update -y \
	&& apt-get install -y git curl zip jq cron supervisor sendmail gnupg uuid-runtime python3 python3-pip

VOLUME /appz/log
VOLUME /appz/home
VOLUME /appz/cache
VOLUME /appz/data
VOLUME /appz/backup

ADD supervisor/cron.conf /etc/supervisor/conf.d/cron.conf
ADD scripts /appz/scripts

RUN echo "15 8 * * * /usr/bin/nice -5 /appz/scripts/cleanup.sh" | crontab -

ENV HOME /appz/home
#fluentd installation
ADD scripts/fluentd.sh /usr/local/bin/fluentd.sh
RUN sh /usr/local/bin/fluentd.sh
ADD conf/fluentd.conf /etc/td-agent/td-agent.conf
ADD plugin/out_graylog.rb /etc/td-agent/plugin/out_graylog.rb
RUN /usr/sbin/td-agent-gem install fluent-plugin-grok-parser
ADD supervisor/supervisord.conf /etc/supervisor/supervisord.conf
ADD scripts/fluentd_run.sh /appz/scripts/fluentd_run.sh
RUN chmod +x /appz/scripts/fluentd_run.sh
ADD supervisor/fluentd.conf /etc/supervisor/conf.d/fluentd.conf
RUN echo 'alias ctl="supervisorctl"' >> /appz/.bashrc \ 
	&& echo 'alias status="supervisorctl status"' >> /appz/.bashrc \ 
	&& echo 'alias start="supervisorctl start"' >> /appz/.bashrc \
	&& echo 'alias stop="supervisorctl stop"' >> /appz/.bashrc \
	&& echo 'alias restart="supervisorctl restart"' >> /appz/.bashrc \
	&& echo 'alias dev="cd /appz/dev"' >> /appz/.bashrc \
	&& echo 'alias scripts="cd /appz/scripst"' >> /appz/.bashrc \
	&& echo 'alias log="cd /appz/log"' >> /appz/.bashrc \ 
	&& echo 'alias cache="cd /appz/cache"' >> /appz/.bashrc \ 
	&& echo 'alias data="cd /appz/data"' >> /appz/.bashrc 

ENTRYPOINT ["/usr/bin/supervisord", "-n"]
