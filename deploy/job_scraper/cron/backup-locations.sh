#!/bin/sh

# XXX TODO -use our own serializer/deserializer so that we don't need pk
# for the models
dir="neekanee_"`date +"%m%d%y"`

test -d $dir || mkdir $dir

python manage.py dumpdata --natural --indent 4 neekanee_solr.Location > ${dir}/locations.json
python manage.py dumpdata --natural --indent 4 neekanee_solr.LocationAlias > ${dir}/location_aliases.json
python manage.py dumpdata --natural --indent 4 neekanee_solr.NullLocation > ${dir}/null_locations.json

tar cvf ${dir}.tar ${dir}
gzip ${dir}.tar
scp ${dir}.tar.gz thayton@www.neekanee.com:locations-backup-${dir}.tar.gz
rm -rf ${dir}
rm -f ${dir}.tar.gz
