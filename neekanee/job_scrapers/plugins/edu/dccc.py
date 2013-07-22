import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Deleware County Community College',
    'hq': 'Media, PA',

    'benefits': {
        'url': 'http://www.dccc.edu/about-us/employment-opportunities/benefits',
        'vacation': []
    },

    'home_page_url': 'http://www.dccc.edu',
    'jobs_page_url': 'http://www.dccc.edu/about-us/human-resources/employment-opportunities',

    'gctw_chronicle': True,

    'empcnt': [1001,5000]
}

CAMPUS_LOCATIONS = {
    r'Marple':                  'Media',
    r'Southeast':               'Sharon Hill',
    r'Downingtown':             'Downingtown',
    r'Exton':                   'Exton',
    r'Pennocks Bridge':         'Jennersville',
    r'Chester County Hospital': 'West Chester'
}

class DcccJobScraper(JobScraper):
    def __init__(self):
        super(DcccJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        r = re.compile(r'^/about-us/employment-opportunities/job-postings/')

        while True:
            s = soupify(self.br.response().read())
            d = s.find('div', attrs={'class': 'data'})

            for a in d.findAll('a', href=r):
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                jobs.append(job)

            x = {'class': 'pager-next'}
            l = s.find('li', attrs=x)

            if l is None:
                break

            url = urlparse.urljoin(self.br.geturl(), l.a['href'])
            self.br.open(url)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', attrs={'class': 'data'})
            t = d.find(text='Campus:')

            x = None

            if t is not None:
                t = t.findNext(text=True)
                for c, l in CAMPUS_LOCATIONS.items():
                    if re.search(c, t, re.I):
                        l = self.parse_location(l + ', PA')
                        if l:
                            x = l
                            job.location = l
                            break

            # No location match
            if not x:
                continue

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return DcccJobScraper()
            

