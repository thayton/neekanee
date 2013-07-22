import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Hofstra',
    'hq': 'Hempstead, NY',

    'benefits': {
        'url': 'http://www.hofstra.edu/about/HR/hr_welcome_benes.html',
        'vacation': [],
        'holidays': 15
    },

    'home_page_url': 'http://www.hofstra.edu',
    'jobs_page_url': 'http://www.hofstra.edu/About/Jobs/jobs_careers_at_hofstra.cfm?jobType=both',

    'gctw_chronicle': True,

    'empcnt': [1001,5000]
}

class HofstraJobScraper(JobScraper):
    def __init__(self):
        super(HofstraJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'getJob\(\'(.*)\'\)')

        for a in s.findAll('a', onclick=r):
            m = re.search(r, a['onclick'])
            job = Job(company=self.company)
            job.title = a.text
            # http://www.hofstra.edu/About/Jobs/jobs_popup.cfm?id=8634
            job.url = urlparse.urljoin(self.br.geturl(), 'jobs_popup.cfm?id=' + m.group(1))
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
            d = s.find('div', attrs={'class': 'theJob'})

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return HofstraJobScraper()
