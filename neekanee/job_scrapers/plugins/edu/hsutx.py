import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Hardin-Simmons University',
    'hq': 'Abilene, TX',

    'benefits': {
        'url': 'http://www.hsutx.edu/Media/Website%20Resources/hr/pdf/Summary%20of%20Benefits.pdf',
        'vacation': [(1,10)],
        'holidays': 19,
        'tuition_assistance': True,
        'sick_days': 12
    },

    'home_page_url': 'http://www.hsutx.edu',
    'jobs_page_url': 'http://www.hsutx.edu/employment/',

    'gctw_chronicle': True,

    'empcnt': [201,500]
}

class HsutxJobScraper(JobScraper):
    def __init__(self):
        super(HsutxJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        positions = [ 'applicants/faculty', 'applicants/staff' ]
        r = re.compile(r'/employment/applicants/\w+-details\?')

        for link in [ urlparse.urljoin(url, p) for p in positions ]:
            self.br.open(link)
            s = soupify(self.br.response().read())

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
            d = s.find('div', id='jobdetails')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return HsutxJobScraper()
