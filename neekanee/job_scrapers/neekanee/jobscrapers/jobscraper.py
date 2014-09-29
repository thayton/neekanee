# Use django ORM and neekanee models
#----------------------------------------------------------------------
import os
import pwd
import sys
import json
import logging
import urlparse
import mechanize

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../../')))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django import db 
from django.core.exceptions import ObjectDoesNotExist
from neekanee_solr.models import *
from neekanee.geocoder.neekanee_geocoder import NeekaneeGeocoder
from neekanee.geocoder.neekanee_geocoder_client import NeekaneeGeocoderClient
from neekanee.browser.neekanee_browser import NeekaneeBrowser

#----------------------------------------------------------------------

def find(iseq, job, seq):
    """ Find job in sequence of jobs """
    for item in seq:
        if iseq(job, item):
            return True

    return False

class JobScraper(object):
    def __init__(self, company_dict=None, return_usa_only=False):
        self.use_geocoding_server = True

        self.init_browser()
        self.init_logger()
        self.init_geocoder()

        if company_dict is not None:
            self.set_company(company_dict)
            self.logger.debug('Initialized scraper for company %s' % self.company.name)
            self.logger.debug('Company %s currently has %d jobs in database' % (self.company.name, self.company.job_set.count()))

    def class_name(self):
        return '%s' % type(self).__name__

    def reset_database_connection(self):
        db.close_connection()

    def init_browser(self):
        self.br = NeekaneeBrowser()
        self.br.set_handle_robots(False)
        
    def init_geocoder(self):
        if self.use_geocoding_server:
            self.geocoder = NeekaneeGeocoderClient()
        else:
            self.geocoder = NeekaneeGeocoder()

    def init_logger(self):
        self.logger = logging.getLogger('neekanee.JobScraper.%s' % self.class_name())
        self.logger.setLevel(logging.DEBUG)

        sh = None
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                sh = handler

        if not sh:
            sh = logging.StreamHandler()
            sh.setLevel(logging.DEBUG)        

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            sh.setFormatter(formatter)

            self.logger.addHandler(sh)

    def set_company(self, company_dict):
        try:
            company = Company.objects.get(home_page_url=company_dict['home_page_url'])
        except ObjectDoesNotExist:
            company = Company()

        company.name = company_dict['name']
        company.home_page_url = company_dict['home_page_url']
        company.jobs_page_url = company_dict['jobs_page_url']

        netloc = urlparse.urlparse(company.home_page_url).netloc
        company.tld = netloc.rsplit('.', 1)[1]

        if company_dict.has_key('ats'):
            company.ats = company_dict['ats']

        company.location = self.geocode(company_dict['hq'])

        if company_dict.has_key('empcnt'):
            try:
                if len(company_dict['empcnt']) == 1:
                    empcnt = CompanySize.objects.get(lo=company_dict['empcnt'][0])
                else:
                    empcnt = CompanySize.objects.get(lo=company_dict['empcnt'][0], hi=company_dict['empcnt'][1])
                        
                company.empcnt = empcnt
            except ObjectDoesNotExist:
                raise
            
        company.save()
        self.company = company

    def parse_location(self, location_text):
        """ 
        Backwards compatibility wrapper for parse_location calls 
        """
        return self.geocode(location_text)
        
    def geocode(self, location):
        return self.geocoder.geocode(location)

    def scrape_jobs(self, company):
        pass

    def get_job_cmp(self):
        """
        Job comparison function to be used when comparing whether two jobs are
        equivalent. The default is to assume that if the url/data fields of two
        jobs objects are equivalent then the two jobs are the same. 

        Inherited classes may override this field for more complex comparison 
        operations.
        """
        return lambda x,y: x.url == y.url and x.url_data == y.url_data

    def prune_unlisted_jobs(self, listed_jobs, use_job_cmp=False):
        """
        Remove dead jobs from the database - these are jobs whose links 
        are in the  database that are no longer listed on the company 
        jobs site.
        
        Callers can set use_job_cmp=True and then define get_job_cmp()
        to return a comparison function of their choosing if the url,url_data
        comparison used here does not suffice.
        """
        num_deleted = 0

        if use_job_cmp:
            cmp = self.get_job_cmp()

            for job in self.company.job_set.all():
                if not find(cmp, job, listed_jobs):
                    self.logger.debug('Deleting job (%s) for company %s' % (job.url, self.company))
                    job.delete()
                    num_deleted += 1
        else:
            stored_jobs_set = set([('%s' % j.url, '%s' % j.url_data) for j in self.company.job_set.all()])
            listed_jobs_set = set([('%s' % j.url, '%s' % j.url_data) for j in listed_jobs])

            jobs_to_delete = stored_jobs_set - listed_jobs_set

            self.logger.info('%d jobs to delete' % len(jobs_to_delete))

            for entry in jobs_to_delete:
                for job in self.company.job_set.filter(url=entry[0], url_data=entry[1]):
                    self.logger.debug('Deleting job (%s) for company %s' % (job.url, self.company))
                    job.delete()
                    num_deleted += 1

        self.logger.info('Deleted %d unlisted jobs' % num_deleted)

    def new_job_listings(self, listed_jobs):
        """
        for each job in listed_jobs
          if job is not currently in the database then
            add job to new_jobs

        Callers can set use_job_cmp=True and then define get_job_cmp()
        to return a comparison function of their choosing if the url,url_data
        comparison used here does not suffice.
        """
        self.logger.debug('Extracting new jobs from %d jobs listed' % len(listed_jobs))

        cmp = self.get_job_cmp()
        new_jobs = []

        for job in listed_jobs:
            if not find(cmp, job, self.company.job_set.all()) and \
               not find(cmp, job, new_jobs): # don't allow dups in new_jobs
                self.logger.debug('New job (%s) at company %s' % (job.url, self.company))
                new_jobs.append(job)

        self.logger.info('%d new job listings' % len(new_jobs))            
        return new_jobs

    def new_job_listings_old(self, listed_jobs, use_job_cmp=False):
        """
        for each job in listed_jobs
          if job is not currently in the database then
            add job to new_jobs

        Callers can set use_job_cmp=True and then define get_job_cmp()
        to return a comparison function of their choosing if the url,url_data
        comparison used here does not suffice.
        """
        self.logger.debug('Extracting new jobs from %d jobs listed' % len(listed_jobs))
        new_jobs = []

        if use_job_cmp:
            cmp = self.get_job_cmp()

            for job in listed_jobs:
                if not find(cmp, job, self.company.job_set.all()) and \
                   not find(cmp, job, new_jobs): # don't allow dups in new_jobs
                    self.logger.debug('New job (%s) at company %s' % (job.url, self.company))
                    new_jobs.append(job)
        else:
            for job in listed_jobs:
                if self.company.job_set.filter(url=job.url, url_data=job.url_data).count() == 0:
                    self.logger.debug('New job (%s) at company %s' % (job.url, self.company))
                    new_jobs.append(job)

        self.logger.info('%d new job listings' % len(new_jobs))            
        return new_jobs

    def urlencoded_form_to_html_form(self, url, url_data):
        form = '<form method="post" action="%s">' % url
        dict = urlparse.parse_qs(url_data)
        
        for k,v in dict.items():
            form += '\n' + '  <input type="hidden" name="%s" value="%s" />' % (k,v[0])

        form += '\n' + '  <input type="submit" value="submit" />'
        form += '\n' + '</form>'

        return form

    def serialize(self):
        """
        Return JSON encoded list of jobs for this company in old format
        """
        return json.dumps(self.company.dict(), indent=4)
