import sys

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from neekanee_solr.models import *
from django.template.defaultfilters import slugify

#
# Remove all jobs for a company where a company is specified
# by its home page URL
#
class Command(BaseCommand):
    help = 'Go through all of the companies and set their name_slug fields'

    def handle(self, *args, **options):
        for company in Company.objects.all():
            company.name_slug = slugify(company.name)
            company.save()
            print 'Slug for %s = %s' % (company.name, company.name_slug)

        
