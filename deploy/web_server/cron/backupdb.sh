#!/bin/sh

# XXX TODO -use our own serializer/deserializer so that we don't need pk
# for the models
dir="neekanee_"`date +"%m%d%y"`

test -d $dir || mkdir $dir

python manage.py dumpdata --natural --indent 4 neekanee_solr.Company > ${dir}/companies.json
python manage.py dumpdata --natural --indent 4 neekanee_solr.Location > ${dir}/locations.json

python manage.py dumpdata --natural --indent 4 neekanee_solr.Tag > ${dir}/tags.json
python manage.py dumpdata --natural --indent 4 neekanee_solr.CompanyTag > ${dir}/companytags.json

python manage.py dumpdata --natural --indent 4 neekanee_solr.Award > ${dir}/awards.json
python manage.py dumpdata --natural --indent 4 neekanee_solr.CompanyAward > ${dir}/companyawards.json

python manage.py dumpdata --natural --indent 4 neekanee_solr.VacationAccrual > ${dir}/vacationaccrual.json
python manage.py dumpdata --natural --indent 4 neekanee_solr.SickLeaveAccrual > ${dir}/sickleaveaccrual.json
