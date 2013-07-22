import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'MailChimp',
    'hq': 'San Francisco, CA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.mailchimp.com',
    'jobs_page_url': 'http://mailchimp.com/about/jobs/',

    'empcnt': [51,200]
}

class MailChimpJobScraper(JobScraper):
    def __init__(self):
        super(MailChimpJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        a = { 'class': 'content main' }
        v = s.find('div', attrs=a)
        a = { 'class': 'inset' }

        self.company.job_set.all().delete()

        for d in v.findAll('div', attrs=a):
            job = Job(company=self.company)

            l = self.parse_location(d.strong.text)
            r = re.compile(r'^/about/jobs/')
            x = d.find('a', href=r)

            if not l:
                continue

            job.title = d.h2.text 
            job.url = urlparse.urljoin(self.br.geturl(), x['href'])
            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return MailChimpJobScraper()

