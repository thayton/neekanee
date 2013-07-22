from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from neekanee_solr.models import *

from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = 'Prunes SOLR docs that do not have a corresponding job or company assocated with them'

    def handle(self, *args, **options):
        dups = Job.objects.values('md5').annotate(Count('id')).filter(id__count__gt=1)
        for entry in dups:
            jobs = Job.objects.filter(md5=entry['md5'])
            for job in jobs[1:]:
                job.delete()
