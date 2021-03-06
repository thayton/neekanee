import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Juniata College',
    'hq': 'Huntingdon, PA',

    'benefits': {
        'url': 'http://www.juniata.edu/services/hresources/benefits.html',
        'vacation': [],
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.juniata.edu',
    'jobs_page_url': 'http://www.juniata.edu/services/hresources/openings.html',

    'gctw_chronicle': True,

    'empcnt': [201,500]
}

class JuniataJobScraper(JobScraper):
    def __init__(self):
        super(JuniataJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        r = re.compile(r'^\?action=VIEW&job=\d+$')

        for a in d.findAll('a', href=r):
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
            d = s.find('div', id='content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return JuniataJobScraper()
