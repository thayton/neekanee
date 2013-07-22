#!/usr/bin/env python

# Use django ORM and neekanee models
#----------------------------------------------------------------------

import os
import sys

sys.path.append(os.path.abspath('../..'))
sys.path.append(os.path.abspath('..'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

#----------------------------------------------------------------------

from StringIO import StringIO
from django.core.serializers.json import Serializer as JSONSerializer
from django.core.serializers.python import Deserializer as PythonDeserializer
from django.core.serializers.json import  DjangoJSONEncoder
from django.utils import simplejson
from django.core.exceptions import ObjectDoesNotExist

from neekanee_solr.models import *

class NeekaneeSerializer(JSONSerializer):
    """ 
    Override end_serialization in order to remove the 'pk' field 
    Reference: http://stackoverflow.com/questions/1615649/remove-pk-field-from-django-serialized-objects
    """
    def end_serialization(self):
        cleaned_objects = []

        for obj in self.objects:
            del obj['pk']

        self.options.pop('stream', None)
        self.options.pop('fields', None)
        self.options.pop('use_natural_keys', None)
        simplejson.dump(self.objects, self.stream, cls=DjangoJSONEncoder, **self.options)            

def NeekaneeDeserializer(stream_or_string, **options):
    """
    Deserialize a stream or string of JSON data. Overridden so we can
    handle objects that have no primary key. XML has a fix for this but
    JSON deserializer does not! 

    References:
    http://stackoverflow.com/questions/1134966/django-model-deserialization-with-empty-pk
    https://code.djangoproject.com/ticket/11486
    """
    if isinstance(stream_or_string, basestring):
        stream = StringIO(stream_or_string)
    else:
        stream = stream_or_string
    
    obj_list = simplejson.load(stream)
    for obj in obj_list:
        if not obj.has_key('pk'):
            obj['pk'] = None

    for obj in PythonDeserializer(obj_list, **options):
        yield obj

    
company = Company.objects.all()[0]
jobs = company.job_set.all()

serializer = NeekaneeSerializer()
results = {}

results['company'] = serializer.serialize([company], ensure_ascii=False, indent=2, use_natural_keys=True)
results['jobs'] = serializer.serialize(jobs, ensure_ascii=False, indent=2, use_natural_keys=True)

print results['company']
#print results['jobs']

testme = """
[
  {
    "model": "neekanee_solr.company", 
    "fields": {
      "jobs_page_url": "http://www.neekanee.com/jobs/", 
      "name": "Neekanee", 
      "location": [
        "san francisco", 
        "ca", 
        "us"
      ], 
      "home_page_url": "http://www.neekanee.com", 
      "empcnt": [
        1, 
        10
      ], 
      "tld": "com", 
      "ats": ""
    }
  }
]
"""

for obj in NeekaneeDeserializer(results['company'], use_natural_keys=True):
    try:
        company = Company.objects.get(home_page_url=obj.object.home_page_url)
        obj.object.pk = company.pk
    except ObjectDoesNotExist:
        pass

    #
    # If company already existed it gets updated, otherwise save the
    # new company
    #
    obj.save()
    print obj

