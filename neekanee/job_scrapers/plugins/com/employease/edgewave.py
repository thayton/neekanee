import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'EdgeWave',
    'hq': 'San Diego, CA',

    'ats': 'Employease',

    'contact': 'resumes@edgewave.com',
    'benefits': {
        'vacation': [(1,15),(4,20)]
    },

    'home_page_url': 'http://www.edgewave.com',
    'jobs_page_url': 'http://www.edgewave.com/employment/default.asp',

    'empcnt': [51,200]
}

class EdgeWaveJobScraper(JobScraper):
    def __init__(self):
        super(EdgeWaveJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/employment/.*.asp')
        d = { 'class': 'link', 'href': r }

        for a in s.findAll('a', attrs=d):
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
            d = s.find('div', id='swap_banner')
            t = d.findNextSibling('table')
            t = t.tr.findAll('td', limit=2)[1]

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return EdgeWaveJobScraper()
