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
    help = 'Go through all of the locations and set their slug field'

    def handle(self, *args, **options):
        for location in Location.objects.all():
            l = ' '.join([location.city, location.state, location.country])
            location.slug = slugify(l)
            try:
                print 'Slug for %s = %s' % (location, location.slug)
            except:
                pass
            location.save()


        
