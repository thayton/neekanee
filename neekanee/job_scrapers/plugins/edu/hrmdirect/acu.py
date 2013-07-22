import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Abiline Christian University',
    'hq': 'Abiline, TX',

    'benefits': {
        'url': 'http://www.acu.edu/campusoffices/hr/benefits/index.html',
        'vacation': [],
        'holidays': 14
    },

    'home_page_url': 'http://www.acu.edu',
    'jobs_page_url': 'http://acu.hrmdirect.com/employment/openings.php',

    'empcnt': [501,1000]
}

class AcuJobScraper(JobScraper):
    def __init__(self):
        super(AcuJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', attrs={'class': 'body'})
        r = re.compile(r'view\.php\?req=\d+&$')

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
            d = s.find('div', id='bodyContainer')
            l = d.find(text='Location:')
            l = l.findNext('div').contents[2]
            l = self.parse_location(l)

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return AcuJobScraper()
