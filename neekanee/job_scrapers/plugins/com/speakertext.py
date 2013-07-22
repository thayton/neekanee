import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'SpeakerText',
    'hq': 'San Francisco, CA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.speakertext.com',
    'jobs_page_url': 'http://www.speakertext.com/jobs',

    'empcnt': [1,10]
}

class SpeakerTextJobScraper(JobScraper):
    def __init__(self):
        super(SpeakerTextJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        u = d.find('ul', id='jobtabs')
        r = re.compile(r'^/jobs/')

        for a in u.findAll('a', href=r):
            title = a.text.lower().strip()
            if title.startswith('the company'):
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
            r = re.compile(r'job_description\s*$')
            a = {'class': r}
            d = s.find('div', attrs=a)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return SpeakerTextJobScraper()
