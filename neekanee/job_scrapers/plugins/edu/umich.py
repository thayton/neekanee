import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Universiy of Michigan',
    'hq': 'Ann Arbor, MI',

    'home_page_url': 'http://www.umich.edu',
    'jobs_page_url': 'http://umjobs.org/',

    'gctw_chronicle': True,

    'empcnt': [10001]
}

class UmichJobScraper(JobScraper):
    def __init__(self):
        super(UmichJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form(nr=0)
        self.br.submit()

        r = re.compile(r'/job_detail/\d+/')

        for l in self.br.links(url_regex=r):
            job = Job(company=self.company)
            job.title = l.text
            job.url = urlparse.urljoin(l.base_url, l.url)
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='article')

            r = re.compile(r'location', re.I)
            f = lambda x: x.name == 'dt' and re.search(r, x.text)
            v = d.find(f)
            v = v.findNext('dd').contents[-1]
            l = self.parse_location(v.strip())

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return UmichJobScraper()
