import sys

from django.core.management.base import BaseCommand, CommandError
from neekanee_solr.models import *
from neekanee_solr.pysolr import Results, Solr

#
# Ensure all jobs in the database have their checksum field set. 
#
class Command(BaseCommand):
    help = 'Set checksum field for all jobs in database'

    def handle(self, *args, **options):
        for job in Job.objects.all():
            job.md5 = job.hexdigest()
            job.save()

        
