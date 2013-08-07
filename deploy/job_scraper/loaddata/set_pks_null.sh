#!/bin/sh
######################################################################
# NAME: set_pks_null.sh
#
# PURPOSE: Set the primary key of the location data json files to 
#          null so that we can load the data in using natural keys
#          as explained here:
#
#          http://stackoverflow.com/questions/9436954/excluding-primary-key-in-django-dumpdata-with-natural-keys
#
# USAGE: ./set_pks_null.sh <file>
#
# EXAMPLE: Run the following to set the pk fields in locations.json
#          to null:
#
#          $ ./set_pks_null.sh locations.json   
#
#          You can then load location.json in with the django loaddata
#          command:
#
#          $ python manage.py loaddata
######################################################################
if [ $# -ne 1 ]; then
  echo "usage: $0 <file>"
  exit 1
fi

cp -f $1 $1.bak
cat $1 | sed -E "s/\"pk\": [0-9]+/\"pk\": null/g" > $1.$$
mv -f $1.$$ $1

