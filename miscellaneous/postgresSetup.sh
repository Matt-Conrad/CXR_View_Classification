sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 7FCC7D46ACCC4CF8
sudo apt-get update
sudo apt-get install curl ca-certificates gnupg -y
curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
echo 'deb http://apt.postgresql.org/pub/repos/apt/ focal-pgdg main' > /etc/apt/sources.list.d/pgdg.list
sudo apt-get update
sudo apt-get install postgresql-12 -y
sudo systemctl start postgresql@12-main
sudo -u postgres psql -U postgres -d postgres -c "alter user postgres with password 'postgres';"
