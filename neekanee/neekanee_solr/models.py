import os
import math
import uuid
import hashlib
import random

from pysolr import Solr
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import smart_str, smart_unicode
from django.template.defaultfilters import slugify

#-----------------------------------------------------------------    
def get_logo_path(instance, filename):
    ''' Used to generate random filenames for uploading images '''
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('logos', filename)

def get_location_photos_path(instance, filename):
    ''' Used to generate random filenames for uploading images '''
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('location_photos', filename)

def get_worklife_photos_path(instance, filename):
    ''' Used to generate random filenames for uploading images '''
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('worklife_photos', filename)

def remove_non_ascii(s): return "".join(filter(lambda x: ord(x)<128, s))

#-----------------------------------------------------------------    
class LocationManager(models.Manager):
    def get_by_natural_key(self, city, state, country):
        return self.get(city=city, state=state, country=country)
    
class Location(models.Model):
    objects = LocationManager()

    slug = models.SlugField(blank=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2)
    province = models.CharField(max_length=2)
    country = models.CharField(max_length=2)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ('city', 'state', 'country')

    def natural_key(self):
        return (self.city, self.state, self.country)

    def __unicode__(self):
        if self.country == 'us':
            return '%s, %s, %s' % (self.city, self.state, self.country)
        else:
            return '%s, %s' % (self.city, self.country)

class LocationAlias(models.Model):
    location = models.ForeignKey(Location)
    alias = models.CharField(max_length=256)

    def __unicode__(self):
        return '%s -> %s' % (self.alias, self.location)

class NullLocation(models.Model):
    """
    Location text that we are unable to geocode. Stored in the
    database so that we don't keep hitting Google's servers with
    the same text over and over when it's always going to fail.
    """
    text = models.CharField(max_length=256)

    def __unicode__(self):
        return '%s' % (self.text)

#-----------------------------------------------------------------    
class AwardManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class Award(models.Model):
    """
    Employer awards like Chronicle's Great Colleges to Work For,
    Fortune's 100 Best Companies to Work For, etc.
    """
    objects = AwardManager()

    name = models.CharField(max_length=128)
    url = models.URLField(max_length=256)

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

#-----------------------------------------------------------------    
class CompanySizeManager(models.Manager):
    def get_by_natural_key(self, lo, hi):
        return self.get(lo=lo, hi=hi)

class CompanySize(models.Model):
    """
    Number of employees at a company, divided into ranges:

        1 - 10
       11 - 50
       51 - 200
      201 - 500
      501 - 1000
     1001 - 5000
     5001 - 10000
    10001+

    """
    objects = CompanySizeManager()

    lo = models.IntegerField()
    hi = models.IntegerField()

    class Meta:
        unique_together = ('lo', 'hi')

    def natural_key(self):
        return (self.lo, self.hi)

    def __unicode__(self):
        return '%d-%d' % (self.lo,self.hi)

#-----------------------------------------------------------------    
class CompanyManager(models.Manager):
    def get_by_natural_key(self, home_page_url):
        return self.get(home_page_url=home_page_url)

class Company(models.Model):
    """
    tld - top level domain of the company website (tld of www.viasat.com => com)
    ats - applicant tracking system (if any) being used
    """
    objects = CompanyManager()
    name = models.CharField(max_length=64)
    name_slug = models.SlugField(blank=True, unique=True, max_length=64)

    home_page_url = models.CharField(max_length=255, unique=True)
    jobs_page_url = models.CharField(max_length=512)
    benefits_page_url = models.CharField(max_length=512, blank=True)

    description = models.TextField(blank=True)

    last_scrape_time = models.DateField(null=True, blank=True)

    tld = models.CharField(max_length=3)
    ats = models.CharField(max_length=64, blank=True)

    logo = models.FileField(upload_to=get_logo_path, blank=True)
    empcnt = models.ForeignKey(CompanySize, null=True)
    location = models.ForeignKey(Location)

    blog = models.URLField(max_length=256, blank=True)
    twitter = models.CharField(max_length=256, blank=True)
    facebook = models.CharField(max_length=256, blank=True)

    class Meta:
        verbose_name_plural = u'Companies'

    def tags(self):
        return self.companytag_set.all()

    def awards(self):
        return self.companyaward_set.all()

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return (self.home_page_url,)

    def save(self, *args, **kwargs):
        if not self.id:
            self.name_slug = slugify(self.name)

        print 'Company.save() method called'
        super(Company, self).save(*args, **kwargs)

    def dict(self):
        company = {}
        company['name'] = self.name
        company['hq'] = {
            'city': self.location.city,
            'state': self.location.state,
            'country': self.location.country,
            'coord': [ self.location.lat, self.location.lng ]
        }
        company['home_page_url'] = self.home_page_url
        company['jobs_page_url'] = self.jobs_page_url
        company['empcnt'] = [ self.empcnt.lo, self.empcnt.hi ]
        company['jobs'] = []

        for job in self.job_set.all():
            company['jobs'].append(job.dict())

        return company

#-----------------------------------------------------------------    
class TagManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class Tag(models.Model):
    objects = TagManager()
    name = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def natural_key(self):
        return (self.name,)

class CompanyTag(models.Model):
    tag = models.ForeignKey(Tag)
    company = models.ForeignKey(Company)

    def __unicode__(self):
        return self.tag.name

    def natural_key(self):
        return self.tag.natural_key() + self.company.natural_key()

#-----------------------------------------------------------------    
class CompanyLocation(models.Model):
    company = models.ForeignKey(Company)
    location = models.ForeignKey(Location)

    def __unicode__(self):
        return self.company.name + '-' + self.location.__unicode__()

class CompanyLocationTag(models.Model):
    tag = models.ForeignKey(Tag)
    company_location = models.ForeignKey(CompanyLocation)

    def __unicode__(self):
        return self.tag.name

    def natural_key(self):
        return self.tag.natural_key() + self.company.natural_key()

#-----------------------------------------------------------------    
class CompanyLocationPhoto(models.Model):
    company_location = models.ForeignKey(CompanyLocation)
    photo = models.FileField(upload_to=get_location_photos_path)
    caption = models.CharField(max_length=256, blank=True)

class CompanyWorkLifePhoto(models.Model):
    company = models.ForeignKey(Company)
    photo = models.FileField(upload_to=get_worklife_photos_path)
    caption = models.CharField(max_length=256, blank=True)

#-----------------------------------------------------------------    
class VacationAccrual(models.Model):
    company = models.ForeignKey(Company)
    year = models.IntegerField()
    days = models.FloatField()

    def __unicode__(self):
        return '%s year %d - %d days' % (self.company, self.year, self.days)

class SickLeaveAccrual(models.Model):
    company = models.ForeignKey(Company)
    year = models.IntegerField()
    days = models.FloatField()

#-----------------------------------------------------------------    
YEARS = tuple((x,x) for x in range(2010,2020))

class CompanyAward(models.Model):
    """
    Company awards by year:

    Company | Award                          | Year
    --------+--------------------------------+--------
    ViaSat  | Fortune Best Place to Work For | 2010
    Tenable | Fortune Best Place to Work For | 2011
    ...

    """
    award = models.ForeignKey(Award)
    company = models.ForeignKey(Company)
    year = models.IntegerField(choices=YEARS)

    def __unicode__(self):
        return '%d %s "%s"' % (self.year, self.company, self.award)

#-----------------------------------------------------------------    
class Job(models.Model):
    title = models.CharField(max_length=256)

    url = models.URLField(max_length=512)
    url_data = models.TextField(blank=True)

    contact = models.EmailField(max_length=256, blank=True)
    desc = models.TextField()

    location = models.ForeignKey(Location)
    company = models.ForeignKey(Company)

    md5 = models.CharField(max_length=32, unique=True)

    def __unicode__(self):
        return self.title

    def clean_title(self):
        self.title = remove_non_ascii(self.title.strip())[:256]
        self.title = self.title.replace('&nbsp;', '')

    def clean_desc(self):
        self.desc = ' '.join(self.desc.split())

    def hexdigest(self):
        # Clean the title and desc *before* calculating the md5 for this job
        self.clean_title()
        self.clean_desc()

        m = hashlib.md5()
        m.update(self.title)
        m.update(self.url)
        m.update(self.url_data)
        m.update(smart_str(self.desc))

        return m.hexdigest()

    def dict(self):
        job = {}
        job['title'] = self.title
        job['url'] = self.url

        if self.url_data:
            job['url_data'] = self.url_data

        job['desc'] = self.desc
        job['location'] = {
            'city': self.location.city,
            'state': self.location.state,
            'country': self.location.country,
            'coord': [ self.location.lat, self.location.lng ]
        }

        return job

    def save(self, *args, **kwargs):
        """ If we want to do anything before saving ..."""
        # Clean the title and desc *before* calculating the md5 for this job
        self.clean_title()
        self.clean_desc()
        self.md5 = self.hexdigest()
        super(Job, self).save(*args, **kwargs)

JOB_ALERT_FREQUENCY = (
    ('D', 'Daily'),
    ('W', 'Weekly'),
)

class JobAlert(models.Model):
    user = models.ForeignKey(User)
    query = models.TextField()
    key = models.CharField(max_length=64, unique=True)
    ctime = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    frequency = models.CharField(max_length=1, choices=JOB_ALERT_FREQUENCY, default='W')

    def save(self, *args, **kwargs):
        """
        Create a random token associated with the job alert so that it can
        be deleted even if the user that owns this job alert is not logged 
        in.
        """
        bits = [self.query] + [str(random.SystemRandom().getrandbits(512))]
        self.key = hashlib.sha256("".join(bits)).hexdigest()
        super(JobAlert, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.user.first_name and self.user.last_name:
            return '%s \t%s' % (self.user.get_full_name(), self.query)
        else:
            return '%s %s' % (self.user.username, self.query)


class JobAlreadyAlerted(models.Model):
    job = models.ForeignKey(Job)
    alert = models.ForeignKey(JobAlert)
    user = models.ForeignKey(User)
    date = models.DateField('date alerted', auto_now=True)

class JobBookmark(models.Model):
    job = models.ForeignKey(Job)
    user = models.ForeignKey(User)
    ctime = models.DateField(auto_now_add=True)

#-----------------------------------------------------------------    
from django.db.models.signals import post_save, post_delete

def company_save_handler(sender, **kwargs):
    print 'company_save_handler called'
    print kwargs

def company_delete_handler(sender, **kwargs):
    company = kwargs['instance']
    conn = Solr('http://127.0.0.1:8983/solr/')
    conn.delete(q='company_id:%d' % int(company.id))

    print 'company_delete_handler - remove all docs with company_id %d from SOLR' % int(company.id)

def job_save_handler(sender, **kwargs):
    print 'job_save_handler called for company %s' % kwargs['instance'].company
    print kwargs

def job_delete_handler(sender, **kwargs):
    job = kwargs['instance']
    conn = Solr('http://127.0.0.1:8983/solr/')
    conn.delete(q='id:%d' % int(job.id))

    print 'job_delete_handler - removed job id %d (company %s) from SOLR' % (int(job.id), job.company)

post_save.connect(job_save_handler, dispatch_uid='setup_job_save_signal', sender=Job)
post_save.connect(company_save_handler, dispatch_uid='setup_company_save_signal', sender=Company)

post_delete.connect(job_delete_handler, dispatch_uid='setup_job_delete_signal', sender=Job)
post_delete.connect(company_delete_handler, dispatch_uid='setup_company_delete_signal', sender=Company)
