import sys
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from neekanee_solr.load_jobs import load_jobs_file

from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = 'Load scraped jobs into file'
    args = 'Jobs file to load'

    def handle(self, *args, **options):
        try:
            file = open(args[0], 'r')
            load_jobs_file(file)
        except:
            print 'Exception loading jobs file ', sys.exc_info()[0]
