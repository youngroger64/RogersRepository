#!/bin/bash


########     DEPENDENCIES   ############

# install latest postgres
sudo apt-get install postgresql-9.3 postgresql-server-dev-9.3 postgresql-contrib-9.3 postgresql-plperl-9.3

echo -e "\e[32m  postgresql installed \e[0m"

#install git
sudo apt-get install git-core
echo -e "\e[32m  git installed*\e[0m"

#install memcached server (required by musicbrainz)
sudo apt-get install memcached
echo -e "\e[32m   memcached installed  \e[0m"

#install redis server (Sessions are stored in Redis)
sudo apt-get install redis-server
echo -e "\e[32m   redis-server installed  \e[0m"

#install nodejs ( required to build our JavaScript and CSS)
sudo apt-get install nodejs npm
echo -e "\e[32m  nodejs   \e[0m"

#depending on linux version, this may also be required
sudo apt-get install nodejs-legacy
echo -e "\e[32m   nodejs-legacy  \e[0m"

#stall a basic set of development tools
sudo apt-get install build-essential
echo -e "\e[32m   build-essentials installed  \e[0m"


#########    SERVER SETUP  ############

echo -e "\e[32m  building server\e[0m"

#download the source code 
git clone --recursive git://github.com/metabrainz/musicbrainz-server.git
echo -e "\e[32m  git clone in music-brainz complete \e[0m"

# cd into musicbrainz
cd musicbrainz-server

# i have a preconfigured server file, this command will copy it to where it supposed to be
cp lib/DBDefs.pm.sample lib/DBDefs.pm
sudo rm lib/DBDefs.pm
sudo cp /home/roger/DBDefs.pm lib/

######    INSTALL PERL DEPENDENCIES    #######

sudo apt-get install libxml2-dev libpq-dev libexpat1-dev libdb-dev libicu-dev liblocal-lib-perl cpanminus

#local::lib requires a few environment variables to be set, append local::lib configuration to bash configuration
echo 'eval $( perl -Mlocal::lib )' >> ~/.bashrc

#reload configuration
source ~/.bashrc

#install dependencies for musicbrainz server, must be in musicbrainz source code directory
cpanm --installdeps --notest .

#Node dependencies are managed using npm. To install these dependencies, run
npm install

#To build everything necessary to access the server in a web browser (CSS, JavaScript)
./script/compile_resources.sh

######      CREATING THE DATABASE    ##########

#install the PostgreSQL Extensions on the database server
cd postgresql-musicbrainz-unaccent
make
sudo make install
cd ..

#install necessary headers
sudo apt-get install libicu-dev

#install the collate extension
cd postgresql-musicbrainz-collate
make
sudo make install
cd ..

# setup postgres authentication
# have to delete file thats there first 
# i have a preconfigured file that i will move to its necesary location
sudo rm /etc/postgresql/9.3/main/pg_hba.conf
sudo cp /home/roger/mb/pg_hba.conf /etc/postgresql/9.3/main/

#install necessary perl module
sudo apt-get install libjson-xs-perl
echo -e "\e[32m libjason-xs-perl installed \e[0m"

#import database dumps
./admin/InitDb.pl --createdb --import /home/roger/mbdump*.tar.bz2 --echo
echo -e "\e[32m  data dumps imported\e[0m"


#start the server
plackup -Ilib -r
