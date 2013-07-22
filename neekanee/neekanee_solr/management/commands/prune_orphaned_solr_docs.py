import sys

from django.core.management.base import BaseCommand, CommandError
from neekanee_solr.models import *
from neekanee_solr.pysolr import Results, Solr

#
# A SOLR doc is orphaned if the company_id exists in SOLR but not 
# in the database or the job id ('id' in schema.xml) exists in 
# SOLR but not in the database.
#
class Command(BaseCommand):
    help = 'Prunes SOLR docs that do not have a corresponding job or company assocated with them'

    def handle(self, *args, **options):
        self.prune_orphaned_company_ids()
        self.prune_orphaned_job_ids()

    def prune_orphaned_job_ids(self):
        query = {
            'q': '*:*',
            'fl': 'id',
            'facet': 'true',
            'facet.field': ['id']
        }

        orphaned_job_ids = []

        conn = Solr('http://127.0.0.1:8983/solr/')
        results = conn.search(**query)
        counts = results.facets['facet_fields']['id']
        zipped = zip(counts[0::2], counts[1::2])

        for job_id in dict(zipped).keys():
            try:
                job = Job.objects.get(pk=int(job_id))
            except Job.DoesNotExist:
                orphaned_job_ids.append(job_id)

        for job_id in orphaned_job_ids:
            print 'Removing doc(id:%d) from SOLR' % int(job_id)
            conn.delete(q='id:%d' % int(job_id))

    def prune_orphaned_company_ids(self):
        query = {
            'q': '*:*',
            'fl': 'id',
            'facet': 'true',
            'facet.limit': '-1',
            'facet.field': ['company_id']
        }

        orphaned_company_ids = []

        conn = Solr('http://127.0.0.1:8983/solr/')
        results = conn.search(**query)
        counts = results.facets['facet_fields']['company_id']
        zipped = zip(counts[0::2], counts[1::2])

        for company_id in dict(zipped).keys():
            try:
                company = Company.objects.get(pk=int(company_id))
            except Company.DoesNotExist:
                orphaned_company_ids.append(company_id)

        for company_id in orphaned_company_ids:
            print 'Removing doc(company_id:%d) from SOLR' % int(company_id)
            conn.delete(q='company_id:%d' % int(company_id))
        
