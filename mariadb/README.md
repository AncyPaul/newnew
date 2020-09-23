NUTANIX VM with APP/DB
======================

Description
-------------
This is a docker image to build a Database VM (PostgreSQL) /Application VM (Tomcat8) on Nutanix platform using ansible. Important steps included in the image creation are:
1. VM (CentOS) creation on Nutanix
2. OS Hardening
3. Application (Tomcat8)/Database (PostgreSQL) setup
4. Log rotation and Cleanup
5. Enabling EFK log collector.


Prerequisites
-------------
Pre-Required image: ubuntu:18.04

Required Container: Vault. The user passwords are taken from the environment variables, these environment variables refer the vault secret for the values. So, the vault container should be set-up first.

Also, fluentd aggregator should be configured in a separate server.


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
