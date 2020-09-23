IMGPOLLER
=========

Description
-------------
This is a docker image to build imgpoller container. 

Prerequisites
-------------
Pre-Required image: ubuntu:18.04

Required Container: Vault. The access tokens for GIT and Slack are taken from the environment variables, these environment variables refer the vault secret for the values. So, the vault container should be set-up first.


Environment variables
--------------------
•	Environment Variables are classified to 3 sections i.e. for Nutanix, Tomcat and Postgres.

•	Provide the IP of Fluentd Aggregator in the variable     CENTOS_BASE_FLUENT_AGGREGATOR_HOST

•	If you are working on Application VM, then use APPZ_PLAYLIST as below.

`ENV+=' -e APPZ_PLAYLIST=nutanix_vm,centos_base,tomcat,tomcat_deploy'`

•	If you are working on Database VM, then use APPZ_PLAYLIST as below.

`ENV+=' -e APPZ_PLAYLIST=nutanix_vm,centos_base,postgres'`

•	In application setup, Use custom war file or download [default war file](https://tomcat.apache.org/tomcat-7.0-doc/appdev/sample/sample.war "default war file").

•	Add the location of the downloaded war file in TOMCAT_DEPLOY_WAR_FILE_SOURCE

• VM details should be added in env and vault

• Pre installed CentOS image name should be given
