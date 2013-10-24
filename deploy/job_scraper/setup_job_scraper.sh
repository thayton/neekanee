#################################################################
# Installation script for setting up a Neekanee job scraping
# machine. Must be run as root.
#
# Assumes that the target machine is Ubuntu 12.04 LTS
#
# Usage:
#   root# ./setup_job_scraper.sh
#################################################################

set -e
set -u
exec &> /root/setup_job_scraper.log

source util.sh

# Setup MySQL database
mysql_install 'n33k@n33'
mysql_create_database 'n33kanee' 'neekanee_solr'
#mysql_secure_installation

#
# XXX Optimize MySQL for Linode 512
# http://library.linode.com/hosting-website#sph_id11
#

#
# Create initial database for neekanee. Specify the utf8mb4 characters set
# so that MySQL does not default to latin1, which will not be able to 
# store characters in some of the job descriptions.
#
# XXX For new use utf8 since utf8mb4 complains about fields being too long.
#
#echo 'CREATE DATABASE neekanee_solr CHARACTER SET utf8;' | mysql -uroot -p

# pdftotext for plugins that that pull down PDF job descriptions
apt-get -y install poppler-utils

# Install Java for Tika to run
# XXX

# Apache Tika for plugins that pull down MSWord job descriptions
# XXX

# Misc dependencies
apt-get -y install libxml2-dev libxslt-dev

# Install pyqt and qt dependencies
apt-get -y install python-qt4
apt-get -y install xvfb

# PIP, virtualenv, ...
apt-get -y install python-pip python-dev build-essential 
pip install --upgrade pip
pip install --upgrade virtualenv 

#################################################################
# Now start setting up Neekanee itself
#################################################################
su - thayton
cd

git clone git@github.com:thayton/neekanee.git

#
# Create a virtualenv for neekanee code
#
cd neekanee
virtualenv venv --distribute
source venv/bin/activate

#
# Get PyQt working in the virtual environment since it was 
# installed globally
#
# Ref: http://stackoverflow.com/questions/1961997/is-it-possible-to-add-pyqt4-pyside-packages-on-a-virtualenv-sandbox
#
source setup_pyqt_venv.sh

pip install -r requirements.txt

#
# Create the database tables for Neekanee
#
# Exports are required for syncdb to work on some platforms. Otherwise python can't pick up the locale:
# >>> locale.getdefaultlocale()   
# (None, None)
# 
# See http://stackoverflow.com/questions/10339963/getdefaultlocale-returning-none-when-running-sync-db-on-django-project-in-pychar
#
export LC_ALL=en_GB.UTF-8
export LANG=en_GB.UTF-8
python manage.py syncdb

#
# Copy location data into loaddata subdirectory and then load baseline 
# locations & jobs into database. 
# 
# This data has been genereated using Django's dumpdata command and 
# includes the pk field in the data. We set the value for this field 
# to null in order to use natural keys defined for these models.
#
(cd loaddata; ./get_locations_data.sh)

# Load location information into databases
python manage.py loaddata ../deploy/job_scraper/loaddata/locations.json
python manage.py loaddata ../deploy/job_scraper/loaddata/null_locations.json
python manage.py loaddata ../deploy/job_scraper/loaddata/location_aliases.json
python manage.py load_scraped_jobs ../deploy/job_scraper/loaddata/
cd -

#
# Startup up Neekanee geocoding server 
# XXX setup a group for /var/log/neekanee and /var/run/neekanee
# instead of making them world writable
#
mkdir /var/log/neekanee/ && chmod o+w /var/log/neekanee/
mkdir /var/run/neekanee/ && chmod o+w /var/run/neekanee/

cd job_scrapers/neekanee/geocoder
python neekanee_geocoder_server.py start


