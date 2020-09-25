FROM appz/mysql:5.7_base
MAINTAINER @rejith_krishnan
RUN apt-get update && apt-get install uuid-runtime -y
WORKDIR /
ADD webapps/ /
RUN for file in /*.zip; \
do \
    if [ -f "$file" ] ; then \
          unzip /*.zip \
          && cp /$(unzip -qql *.zip | head -1 | tr -s ' ' | cut -d' ' -f5- | awk -F '/' '{ print $1}')/*.cnf /etc/mysql/conf.d \
          && ls -l /etc/mysql/conf.d/* \ 
    ;else \
          echo "zip file not found" \
    ;fi   \
;done
ADD mysql-contents/setup.yaml /mysql-contents/
COPY webapps/ /tmp/ 
RUN for file in /tmp/*.zip; \
do \
        zip_name="$(basename -- "$file")" \
        && echo "zip name is "$zip_name"" \
        && file_name="${zip_name%.*}" \
        && echo "sub-folder  name is "$file_name"" \
        && if [ -f "$file" ] ; then \
              dest_folder="$(uuidgen)"  \
              && echo "Creating Destination folder:  "$dest_folder"" \
              && mkdir -v  /tmp/"$dest_folder" \
              && unzip   /tmp/"$file_name".zip  -d  /tmp/"$dest_folder" \
              && chmod  -Rv  a+x  /tmp/"$dest_folder/$file_name"  \
              && cp -rv /tmp/$dest_folder/$file_name/*  /mysql-contents \
              && rm -rfv /tmp/$dest_folder \
              && rm -rfv /tmp/"$zip_name" \
        ;  else \
              echo "zip file not found" \
       ;   fi   \
;done
ADD supervisor/mysql_init.conf /etc/supervisor/conf.d/mysql_init.conf
