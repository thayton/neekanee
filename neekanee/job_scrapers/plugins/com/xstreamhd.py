import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'XStreamHD',
    'hq': 'McLean, VA',

    'contact': 'careers@XStreamHD.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.xstreamhd.com',
    'jobs_page_url': 'http://www.xstreamhd.com/home/careers.php?render=careers',

    'empcnt': [51,200]
}

class xStreamHdJobScraper(JobScraper):
    def __init__(self):
        super(xStreamHdJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/home/careers\.php')
        d = s.findAll('span', onclick=r)

        for t in d:
            m = re.findall(r'(/home/careers.php\?render=\w+)', t['onclick'])

            job = Job(company=self.company)
            job.title = t.text
            job.url = urlparse.urljoin(self.br.geturl(), m[0])
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            l = s.find(text=re.compile(r'Location:'))

            d = l.parent.parent.parent
            l = l.parent.findNext('span').string
            l = re.sub(r'and .*', '', l)
            l = self.parse_location(l)

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return xStreamHdJobScraper()
