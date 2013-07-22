import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Lincoln Center for the Performing Arts',
    'hq': 'New York, NY',

    'benefits': {
        'url': 'http://new.lincolncenter.org/live/index.php/aboutus-jobs',
        'vacation': []
    },

    'home_page_url': 'http://www.lincolncenter.org',
    'jobs_page_url': 'http://about.lincolncenter.org/about/employment/overview',

    'empcnt': [201,500]
}

class LincolnCenterJobScraper(JobScraper):
    def __init__(self):
        super(LincolnCenterJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        list = [ 'Full Time', 'Part Time', 'Temporary' ]

        s = soupify(self.br.response().read())
        d = s.find('div', id='left-column')
        r = re.compile(r'^/about/employment/\S+')

        for text in list:
            a = d.find(lambda x: x.name == 'a' and x.text == text)
            u = a.findNext('ul')

            for a in u.findAll('a', href=r):
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
            d = s.find('div', id='main-column')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return LincolnCenterJobScraper()
