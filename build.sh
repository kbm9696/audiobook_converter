#!/usr/bin/env bash

# Install pre requisite tools
#sudo apt-get install python3-venv
rm -rf ./env
python3 -m venv env
source env/bin/activate

cd env/bin

./python3 pip3 install --no-cache-dir -r ../../requirements.txt
cd ../../
cd app
# Pre-build configuration

rm -rf ./dist
rm -rf ./build
rm -f ./audiobook_converter.spec


# Compile the application
../env/bin/python3 ../env/bin/pyinstaller --hidden-import=flask_api.parsers --hidden-import=flask_api.renderers --onefile --name audiobook_converter main.py

#cd ..
#pwd
#cp app/dist/* docker/
#cp certs/* docker/
#cp os/etc/* docker/
#sudo mkdir -p /etc/pgdata/audiobook-db
#sudo docker run -d --name postgres -e POSTGRES_PASSWORD=9696 -e POSTGRES_DB=audiobook-db -v /etc/pgdata/ipfs-db:/var/lib/postgres/data -p 9443:5432 postgres
#sudo docker exec -i postgres /bin/bash -c "PGPASSWORD=9696 psql --username postgres audiobook-db" < app/dba/ipfs-dba.sql
#cd docker/
#sudo docker build -t audiobook_converter .
#sudo docker run -d --name audiobook_converter -p 9077:9075 audiobook_converter
# Copy to target folder
