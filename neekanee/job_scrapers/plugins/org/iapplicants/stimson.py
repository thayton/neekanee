import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Henry L. Stimson Center',
    'hq': 'Washington, DC',

    'ats': 'iApplicants',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.stimson.org',
    'jobs_page_url': 'http://stimson.iapplicants.com/searchjobs.php',

    'empcnt': [11,50]
}

class StimsonJobScraper(JobScraper):
    def __init__(self):
        super(StimsonJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^ViewJob-\d+\.html')

        for a in s.findAll('a', href=r):
            tr = a.parent.parent
            td = tr.findAll('td', limit=4)

            l = re.sub(r'\(.*\)', '', td[3].string)
            l = self.parse_location(l)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.b.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = l
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            h = s.h2
            t = h.findParent('table')

            job.desc = get_all_text(t)
            job.save()
        
def get_scraper():
    return StimsonJobScraper()
