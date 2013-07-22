import sys

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from neekanee_solr.models import *
from neekanee_solr.pysolr import Results, Solr

#
# Add company headquarters to ComapnyLocations
# Add locations appearing in company job set to CompanyLocations
#
class Command(BaseCommand):
    help = 'Update companylocations for all companies'

    def handle(self, *args, **options):
        for company in Company.objects.all():
            hq = company.location

            print 'Adding location %s to company %s CompanyLocation' % (hq, company)

            try:
                company_location = CompanyLocation.objects.get(company=company, location=hq)
            except ObjectDoesNotExist:
                company_location = CompanyLocation(company=company, location=hq)
                company_location.save()

