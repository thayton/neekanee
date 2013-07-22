import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

import posixpath

from neekanee_solr.models import *

# XXX put this in util/
def resolveComponents(url):
    """
    >>> resolveComponents('http://www.example.com/foo/bar/../../baz/bux/')
    'http://www.example.com/baz/bux/'
    >>> resolveComponents('http://www.example.com/some/path/../file.ext')
    'http://www.example.com/some/file.ext'

    ref: http://stackoverflow.com/questions/4317242/python-how-to-resolve-urls-containing
    """
    parsed = urlparse.urlparse(url)
    new_path = posixpath.normpath(parsed.path)
    if parsed.path.endswith('/'):
        # Compensate for issue1707768
        new_path += '/'
    cleaned = parsed._replace(path=new_path)
    return cleaned.geturl()

COMPANY = {
    'name': 'Rocket Ninja',
    'hq': 'San Francisco, CA',

    'contact': 'Jobs@rocketninja.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.rocketninja.com',
    'jobs_page_url': 'http://www.rocketninja.com/Home/Join.aspx',

    'empcnt': [11,50]
}

class RocketNinjaJobScraper(JobScraper):
    def __init__(self):
        super(RocketNinjaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        
        s = soupify(self.br.response().read())
        d = s.find('div', attrs={'class': 'TheText'})
        r = re.compile(r'/Home/Join/\S+\.aspx$')

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = resolveComponents(urlparse.urljoin(self.br.geturl(), a['href']))
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
            d = s.find('div', attrs={'class': 'FullText'})

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return RocketNinjaJobScraper()
