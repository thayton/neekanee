import re, urlparse, mechanize, webcli

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Overstock',
    'hq': 'Salt Lake City, UT',

    'ats': 'newton',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.overstock.com',
    'jobs_page_url': 'http://www.overstock.com/careers/xml/it_jobs.xml',

    'bptw_glassdoor': True,

    'empcnt': [1001,5000]
}                 

class OverstockJobScraper(JobScraper):
    def __init__(self):
        super(OverstockJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        #
        # Weird - they store their job listing as an XML file and then
        # use Javascript to retrieve and display the contents of this
        # file once the page is loaded
        #

        # Override URL since there are multiple job lists
        # in XML format
        XML_job_lists = [ 'http://www.overstock.com/careers/xml/it_jobs.xml',
                          'http://www.overstock.com/careers/xml/non_it_jobs.xml']

        for url in XML_job_lists:
            self.br.open(url)
            s = soupify(self.br.response().read())

            for j in s.findAll('job'):
                job = Job(company=self.company)
                job.title = j['name']
                job.url = j['url']
                jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            l = s.find('td', id='gnewtonJobLocation')
            t = l.findParent('table')
            l = l.text.split('Location:')[1]
            l = self.parse_location(l)

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return OverstockJobScraper()
