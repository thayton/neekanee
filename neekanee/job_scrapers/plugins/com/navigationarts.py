import re, urllib2, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'NavigationArts',
    'hq': 'Mclean, VA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.navigationarts.com',
    'jobs_page_url': 'http://www.navigationarts.com/about/careers',

    'empcnt': [51,200]
}

class NavigationArtsJobScraper(JobScraper):
    def __init__(self):
        super(NavigationArtsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/home/about-us/careers/.*?\.aspx')

        for a in s.findAll('a', href=r):
            t,l = a.text.rsplit('-', 1)
            l = self.parse_location(l)
            
            if l is None:
                continue

            job = Job(company=self.company)
            job.title = t
            job.location = l
            job.url = urlparse.urljoin(self.br.geturl(), urllib2.quote(a['href']))
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='contentMain')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return NavigationArtsJobScraper()
