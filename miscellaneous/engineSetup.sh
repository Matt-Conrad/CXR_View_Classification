#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd $DIR
./pythonSetup.sh engine

cd /mnt/hgfs/SharedFolder_Guest/Python/Engine

export FLASK_APP=api_controller:app

if [ "$1" == "flask" ]
then
    if [ "$2" == "localhost" ]
    then
        nohup ../../miscellaneous/CXR_env/bin/python -m flask run > /dev/null 2>&1 &
    elif [ "$2" == "network" ]
    then
        nohup ../../miscellaneous/CXR_env/bin/python -m flask run --host=0.0.0.0 > /dev/null 2>&1 &
    fi
elif [ "$1" == "gunicorn" ]
then
    if [ "$2" == "localhost" ]
    then
        nohup ../../miscellaneous/CXR_env/bin/gunicorn api_controller:app > /dev/null 2>&1 &
    elif [ "$2" == "network" ]
    then
        nohup ../../miscellaneous/CXR_env/bin/gunicorn -b 0.0.0.0:8000 api_controller:app > /dev/null 2>&1 &
    fi
elif [ "$1" == "nginx" ]
then
    ../../miscellaneous/CXR_env/bin/gunicorn -D api_controller:app

    sudo apt-get update -y
    sudo apt-get install nginx -y
    
    sudo bash -c "echo '
    server {
       listen 80;
       server_name cxr_classifier;
       access_log  /var/log/nginx/cxr_classifier.log;

       location / {
          proxy_pass http://127.0.0.1:8000;
          proxy_set_header Host \$host;
          proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
       }
    }
    ' > /etc/nginx/sites-available/default"

    sudo sed -i '/http {/ a \\tclient_max_body_size 0;' /etc/nginx/nginx.conf
    
    sudo service nginx start
    sudo service nginx restart
fi