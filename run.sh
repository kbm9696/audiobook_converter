sudo mkdir -p /etc/pgdata/audiobook-db
sudo docker run -d --name postgres -e POSTGRES_PASSWORD=9696 -e POSTGRES_DB=audiobook_db -v /etc/pgdata/audiobook-db:/var/lib/postgres/data -p 5432:5432 postgres
#sudo docker exec -i postgres /bin/bash -c "PGPASSWORD=9696 psql --username postgres audiobook-db" < app/dba/ipfs-dba.sql
cd docker/
sudo docker build -t audiobook_converter .
sudo docker run -d --name audiobook_converter -p 9075:9075 audiobook_converter
