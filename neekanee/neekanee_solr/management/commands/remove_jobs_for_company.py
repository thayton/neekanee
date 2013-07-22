import sys

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from neekanee_solr.models import *
from neekanee_solr.pysolr import Results, Solr

#
# Remove all jobs for a company where a company is specified
# by its home page URL
#
class Command(BaseCommand):
    help = 'Remove all jobs for a company where company is specified by its home page URL'
    args = '<home_page_url>'

    def handle(self, *args, **options):
        try:
            company = Company.objects.get(home_page_url=args[0])
        except ObjectDoesNotExist:
            raise CommandError('Company with home page url %s does not exist' % args[0])

        print 'Removing doc(company_id:%d) from SOLR' % int(company.id)

        company.job_set.all().delete()

        conn = Solr('http://127.0.0.1:8983/solr/')
        conn.delete(q='company_id:%d' % int(company.id))
        
