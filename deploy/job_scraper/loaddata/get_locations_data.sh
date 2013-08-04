#!/bin/bash
######################################################################
# NAME: get_locations_data.sh
#
# PURPOSE: Copy previous day's location data from www.neekanee.com
#          into this directory so that it can be loaded into this
#          machine's database. Untars the archive, sets pks in the
#          files to null and then copies the json files into the
#          current directory. Then removes temporary files.
#
# USAGE: Run it with no arguments ./get_locations_data.sh
#
# NOTES: You may be prompted for a password 
#        Location file names are formatted as follows:
#        locations-backup-neekanee_073013.tar.gz
######################################################################

yesterday=$( date +"%m%d%y" --date='yesterday' )
locations_dir="neekanee_${yesterday}"
locations_file="locations-backup-neekanee_${yesterday}.tar.gz"


scp thayton@www.neekanee.com:$locations_file .
if [ -f $locations_file ]; then
  tar zxvf $locations_file
  for f in `find $locations_dir -name "*.json"`; do
    ./set_pks_null.sh $f
  done
  cp ${locations_dir}/*.json .
  rm -f $locations_file
  rm -rf $locations_dir
fi