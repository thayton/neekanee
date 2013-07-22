import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Ave Maria University',
    'hq': 'Ave Maria, FL',

    'benefits': {
        'url': 'http://www.avemariahr.org/cgi-bin/page.pl?section=benefits',
        'vacation': [(0,12),(4,18),(7,20)]
    },

    'home_page_url': 'http://www.avemaria.edu',
    'jobs_page_url': 'http://www.avemaria.edu/jobs',

    'empcnt': [51,200]
}

class AveMariaJobScraper(JobScraper):
    def __init__(self):
        super(AveMariaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/Jobs/\S+\.aspx$')

        for a in s.findAll('a', href=r):
            title = a.text.lower().strip()
            if title.startswith('read more'):
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            r = re.compile(r'dnn_ctr\d+_HtmlModule_lblContent')
            d = s.find('div', id=r)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return AveMariaJobScraper()
