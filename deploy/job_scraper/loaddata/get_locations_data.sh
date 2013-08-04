#!/bin/bash
######################################################################
# NAME: get_locations_data.sh
#
# PURPOSE: Copy previous day's location data from www.neekanee.com
#          into this directory so that it can be loaded into this
#          machine's database.
#
# USAGE: Run it with no arguments ./get_locations_data.sh
#
# NOTES: You may be prompted for a password 
#        Location file names are formatted as follows:
#        locations-backup-neekanee_073013.tar.gz
######################################################################

yesterday=$( date +"%m%d%y" --date='yesterday' )
locations_file="locations-backup-neekanee_${yesterday}.tar.gz"

scp thayton@www.neekanee.com:$locations_file .
if [ -f $locations_file ]; then
  tar zxvf $locations_file
fi