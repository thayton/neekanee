import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Detectent',
    'hq': 'Escondido, CA',

    'contact': 'jobs@detectent.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.detectent.com',
    'jobs_page_url': 'http://www.detectent.com/careers.php',

    'empcnt': [11,50]
}

class DetectentJobScraper(JobScraper):
    def __init__(self):
        super(DetectentJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'career_detail.php\?c_id=\d+')

        for a in s.findAll('a', href=r):
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
            d = s.find('div', attrs={'class': 'txt_matter'})

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return DetectentJobScraper()

