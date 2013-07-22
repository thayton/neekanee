import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'WGS Systems, LLC',
    'hq': 'Frederick, MD',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.wgssystems.com',
    'jobs_page_url': 'http://www.wgssystems.com/careers.html',

    'empcnt': [11,50]
}

class WgsSystemsJobScraper(JobScraper):
    def __init__(self):
        super(WgsSystemsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'align': 'center', 'class': 'style7'}
        r = re.compile(r'h[34]')
        h = s.findAll(r, attrs=x)

        for hn in h:
            if hn.text == 'CONTACT US':
                continue

            title = ' '.join(hn.a.u.text.split())

            job = Job(company=self.company)
            job.title = title
            job.url = urlparse.urljoin(self.br.geturl(), hn.a['href'])
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
            t = s.find(text=re.compile(job.title.upper()))
            tr = t.findNext('tr')

            job.desc = get_all_text(tr)
            job.save()

def get_scraper():
    return WgsSystemsJobScraper()
