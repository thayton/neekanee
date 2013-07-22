import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Navigator Management Partners',
    'hq': 'Columbus, OH',

    'benefits': {
        'vacation': [],
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.navmp.com',
    'jobs_page_url': 'http://navmp.force.com/careers',

    'gptwcom_entrepreneur': True,

    'empcnt': [51,200]
}

class NavMpJobScraper(JobScraper):
    def __init__(self):
        super(NavMpJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/careers/ts2__JobDetails\?jobId=')

        for a in s.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            jobs.append(job)
        
        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.find('table', attrs={'class': 'atsJobDetailsTable'})
            l = t.find(text=re.compile(r'\s*Location:'))
            l = l.findNext('span')
            l = self.parse_location(l.text)

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return NavMpJobScraper()
