import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Genband',
    'hq': 'Frisco, TX',

    'ats': 'newton',

    'home_page_url': 'http://www.genband.com',
    'jobs_page_url': 'http://newton.newtonsoftware.com/career/CareerHome.action?clientId=4028f88b2f0a1c35012fb3313c344997&gnewtonResize=http://www.genband.com/files/GnewtonResize.htm',

    'empcnt': [1001,5000]
}

class GenbandJobScraper(JobScraper):
    def __init__(self):
        super(GenbandJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='gnewtonCareerBody')
        r = re.compile(r'/career/JobIntroduction\.action\?clientId=')

        for a in d.findAll('a', href=r):
            l = a.findNext('div').text
            l = self.parse_location(l)

            if l is None:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = l
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.find('table', id='gnewtonJobDescription')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return GenbandJobScraper()
