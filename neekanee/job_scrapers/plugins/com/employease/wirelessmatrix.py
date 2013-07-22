import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Wireless Matrix',
    'hq': 'Herndon, VA',

    'ats': 'Employease',

    'benefits': {
        'url': 'http://www.wirelessmatrix.com/about_us/careers/benefits.php',
        'vacation': [(0,17),(3,19),(5,21),(10,24),(15,25)],
        'tuitition_assistance': True
    },

    'home_page_url': 'http://www.wirelessmatrix.com',
    'jobs_page_url': 'http://www.wirelessmatrix.com/about_us/careers/openings.php',

    'empcnt': [51,200]
}

class WirelessMatrixJobScraper(JobScraper):
    def __init__(self):
        super(WirelessMatrixJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'openings_content'}
        d = s.find('div', attrs=x)

        for a in d.findAll('a'):
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
            f = lambda x: x.name == 'strong' and x.text.startswith('Location:')
            p = s.find(f)

            if p:
                l = self.parse_location(getattr(p.nextSibling, 'text', p.nextSibling))
                p = p.findParent('span', attrs={'class': 'bodyText'})

                if l is None:
                    continue

                job.location = l

            x = s.find('form', id='Container0')

            [ i.extract() for i in x.findAll('input') ]
            [ z.extract() for z in x.findAll('select') ]

            job.desc = get_all_text(x)
            job.save()

def get_scraper():
    return WirelessMatrixJobScraper()
