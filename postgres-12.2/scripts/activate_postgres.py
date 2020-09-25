import yaml
import re
import wget
import os
import logging
import zipfile
import shutil
import sys
import pytz
import time
import psycopg2
import pwd
import subprocess
import gzip
import boto3
import os.path
from os import path
from subprocess import PIPE,Popen
from zipfile import ZipFile
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime
def basic():
    connuser = os.environ['POSTGRES_CONNECTUSER']
    conndb = os.environ['POSTGRES_CONNECTIONDB']
    connport = os.environ['POSTGRES_PORT']

    conn1 = psycopg2.connect(host="localhost", port = connport, database= conndb, user=connuser)
    conn1.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
    cur1 = conn1.cursor()
    return cur1, conn1
def new(dbname):
    connuser = os.environ['POSTGRES_CONNECTUSER']
    connport = os.environ['POSTGRES_PORT']

    conn2 = psycopg2.connect(host="localhost", port = connport, database="%s" % (dbname,), user=connuser)
    conn2.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
    cur2 = conn2.cursor()
    return cur2, conn2
def obj(file):
    cur1,conn1 = basic()
    with open(file,'r') as file:
        words = yaml.load(file, Loader=yaml.FullLoader)
        cur1.execute("SELECT usename FROM pg_shadow;")
        list_users = cur1.fetchall()
        cur1.execute("SELECT spcname FROM pg_tablespace;")
        list_spc = cur1.fetchall()
        cur1.execute("SELECT datname FROM pg_database;")
        list_db = cur1.fetchall()
        if 'users' in words:
            users = words['users']
            for user in users:
                username = user['name']
                password = os.environ[user['password']]
                role = user['role'].split(",")
                if (username,) in list_users:
                    logging.warning("'{}'User already exists".format(username))
                else:
                    sqlCreateUser = "create user "+username+" with encrypted password '"+password+"';"
                    cur1.execute(sqlCreateUser)
                    logging.info("'{}'User created and updated user role to Superuser".format(username))
                    for x in role:
                        userPermission = "alter user "+username+" with "+x+";"
                        cur1.execute(userPermission)
        else:
            logging.warning('no users found from yaml')
        if 'databases' in words:
            databases = words['databases']
            for db in databases:
                dbname = db['name']
                owner = db['owner']
                tablespace = db['tablespace'][0]
                ts_name = tablespace['name']
                location = tablespace['location']
                if os.path.exists(location):
                    logging.warning("'{}'Tablespace location already exist".format(location))
                else:
                    os.makedirs(location)
                    uid, gid =  pwd.getpwnam('postgres').pw_uid, pwd.getpwnam('postgres').pw_uid
                    os.chown(location, uid, gid)
                    logging.info("'{}'Tablespace location created".format(location))
                    if (ts_name,) in list_spc:
                        logging.warning("'{}' Tablespace already exists".format(ts_name))
                    else:
                        sqlCreateSpc = "CREATE TABLESPACE "+ts_name+" LOCATION '"+location+"';"
                        cur1.execute(sqlCreateSpc)
                        logging.info("'{}'Tablespace created".format(ts_name))
                        if (dbname,) in list_db:
                            logging.warning("'{}'Database already exists".format(dbname))
                        else:
                            sqlCreateDb = "CREATE DATABASE "+dbname+" OWNER "+owner+" TABLESPACE "+ts_name+";"
                            cur1.execute(sqlCreateDb)
                            logging.info("'{}'Database created".format(dbname))
        else:
            logging.warning('no databases found from yaml')

    cur1.close()
    conn1.close()
def schema(file):
    with open(file,'r') as file:
        words = yaml.load(file, Loader=yaml.FullLoader)
        if 'databases' in words:
            databases = words['databases']
            for db in databases:
                dbname = db['name']
                if 'schemas' in db:
                    schema = db['schemas']
                    for s in schema:
                        schema_name = s['name']
                        authorised_user = s['authorised_user']
                        path = s['search_path']
                        cur2,conn2 = new(dbname)
                        sqlCreateSchema = "CREATE SCHEMA IF NOT EXISTS "+schema_name+" AUTHORIZATION "+authorised_user+";"
                        cur2.execute(sqlCreateSchema)
                        logging.info("'{}'Schema created".format(schema_name))
                        if path == True:
                            sqlAlterUserSchema = "ALTER USER "+authorised_user+" SET search_path = "+schema_name+";"
                            cur2.execute(sqlAlterUserSchema)
                            logging.info("'{}'Set-up the schema search path".format(schema_name))
                        else:
                            logging.warning("'{}'schema path set false".format(schema_name))
                    cur2.close()
                    conn2.close()
                else:
                    logging.warning("'{}'no schemas found from yaml".format(dbname))
        else:
            logging.warning('no databases and schema found from yaml')


def get_bucket():
    db_archive_endpoint = os.environ['APPZ_DB_ARCHIVE_ENDPOINT']
    backup_bucket_name = os.environ['APPZ_DB_ARCHIVE_ENDPOINT'].split("/")[2].split(".")[0]
    s3_directory = os.environ['APPZ_DB_ARCHIVE_ENDPOINT'].split("/")[3]
    destination_file = os.environ['APPZ_DB_ARCHIVE_ENDPOINT'].split("/")[4]
    s3_file_path = ""+s3_directory+"/"+destination_file+""
    return backup_bucket_name, s3_file_path, destination_file

def download_from_s3():
    cur1,conn1 = basic()
    backup_bucket_name,s3_file_path,destination_file = get_bucket()
    aws_access_key = os.environ['AWS_ACCESS_KEY_ID']
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    s3 = boto3.client(
       's3',
       aws_access_key_id=aws_access_key,
       aws_secret_access_key=aws_secret_access_key
    )
    s3_resource = boto3.resource('s3')
    dump_bucket = s3_resource.Bucket(backup_bucket_name)
    bucket_contents = dump_bucket.objects.all()
    contents_list = []
    for file in bucket_contents:
        s3_contents = (file.key)
        contents_list.append(s3_contents)
    if s3_file_path in contents_list:
        logging.info("'{}' Found file".format(s3_file_path))
        s3.download_file(backup_bucket_name , s3_file_path, destination_file)
        if destination_file.endswith(".zip") == True:
            zip = ZipFile(destination_file)
            unzip = zip.extractall()
            dump_file = zip.namelist()[0]
            dest = "/appz/data/"+dump_file+""
            pwd = os.getcwd()
            cwd = ""+pwd+"/"+dump_file+""
            dump_file = shutil.move(cwd, dest)
            if path.exists(dump_file):
                logging.info("'{}' File downloaded successfully".format(dump_file))
            else:
                logging.warning("'{}' File not found".format(dump_file))
        elif destination_file.endswith(".sql") == True:
            dump_file = destination_file
            dest = "/appz/data/"+dump_file+""
            pwd = os.getcwd()
            cwd = ""+pwd+"/"+dump_file+""
            dump_file = shutil.move(cwd, dest)
        else:
            logging.error("'{}' Invalid file format. Only supports .zip and .sql".format(destination_file))
            sys.exit()
        return dump_file
    else:
        logging.warning("'{}' File not found".format(s3_file_path))
        sys.exit()
def restore_db(file,dump_file):
    cur1,conn1 = basic()
    #dump_file = download_from_s3()
    with open(file,'r') as f:
        words = yaml.load(f, Loader=yaml.FullLoader)
        cur1.execute("SELECT datname FROM pg_database;")
        list_db = cur1.fetchall()
        if 'restore' in words:
            restore = words['restore']
            for r in restore:
                pg_db = r['db_name']
                pg_host = r['host']
                pg_user = r['user']
                if (pg_db,) in list_db:
                    logging.warning("'{}' Database already exists".format(pg_db))
                    logging.warning("'{}' Deleting database".format(pg_db))
                    sqlDropDb = "DROP DATABASE "+pg_db+";"
                    sqlCreateDb = "CREATE DATABASE "+pg_db+";"
                    cur1.execute(sqlDropDb)
                    cur1.execute(sqlCreateDb)
                    logging.info("'{}' Database recreated".format(pg_db))
                else:
                    logging.warning("'{}' Couldn't find the database".format(pg_db))
                    sqlCreateDb = "CREATE DATABASE "+pg_db+";"
                    cur1.execute(sqlCreateDb)
                    logging.info("'{}' Database created".format(pg_db))
                command = 'psql '+pg_db+' -U '+pg_user+' < '+dump_file+''
                proc = Popen(command,shell=True)
                proc.wait()
                logging.info("'{}' Restored postgres database dump".format(dump_file))

def trigger(file):
    date_time_download = os.environ.get('APPZ_LOAD_TOKEN')
    if date_time_download is None:
       logging.warning("APPZ_LOAD_TOKEN Variable not found")
       sys.exit() 
    pattern = '%Y%m%d-%H%M'
    epoch = int(time.mktime(time.strptime(date_time_download,pattern)))
    current_time = int(time.time())
    if current_time < epoch :
       diff = epoch - current_time
       if diff < 900:
          logging.info("APPZ_LOAD_TOKEN validated. downloading DB from s3")
          os.environ["APPZ_LOAD_TOKEN"] = "found"
          cur1,conn1 = basic()
          dump_file = download_from_s3()
       else:
          logging.warning("APPZ_LOAD_TOKEN not valid! time difference > 15")
    else:
        logging.warning("APPZ_LOAD_TOKEN not valid! current time > APPZ_LOAD_TOKEN window")

    date_time_restore = os.environ.get('APPZ_RESTORE_TOKEN')
    if date_time_restore is None:
       logging.warning("APPZ_RESTORE_TOKEN Variable not found")
       sys.exit()
    pattern = '%Y%m%d-%H%M'
    epoch = int(time.mktime(time.strptime(date_time_restore,pattern)))
    current_time = int(time.time())
    if current_time < epoch :
       diff = epoch - current_time
       if diff < 900:
          logging.info("APPZ_RESTORE_TOKEN validated. restoring DB from s3")
          db_archive_endpoint = os.environ['APPZ_DB_ARCHIVE_ENDPOINT']
          if db_archive_endpoint is None:
             logging.warning("APPZ_DB_ARCHIVE_ENDPOINT Variable not found")
             sys.exit()
          os.environ["APPZ_RESTORE_TOKEN"] = "found"
          restore_db(file,dump_file)
       else:
          logging.warning("APPZ_RESTORE_TOKEN not valid! time difference > 15")
    else:
        logging.warning("APPZ_RESTORE_TOKEN not valid! current time > APPZ_RESTORE_TOKEN window")
    check_load = os.environ.get('APPZ_LOAD_TOKEN')
    check_restore = os.environ.get('APPZ_RESTORE_TOKEN')
    if (check_load != 'found' and check_restore != 'found'): 
        obj(file)
        schema(file)
def main():
    logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s %(message)s')
    file = "/postgres-contents/setup.yaml"
    trigger(file)
if __name__ == '__main__':
    main()

