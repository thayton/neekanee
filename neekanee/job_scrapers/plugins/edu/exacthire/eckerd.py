import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Eckerd College',
    'hq': 'St. Petersburg, FL',

    'benefits': {
        'vacation': [],
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.eckerd.edu',
    'jobs_page_url': 'http://eckerd.myexacthire.com/searchjobs.php',

    'empcnt': [201,500]
}

class EckerdJobScraper(JobScraper):
    def __init__(self):
        super(EckerdJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        r = re.compile(r'^ViewJob\-\d+\.html$')

        for a in d.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[-1].text)
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
            t = s.find('table', attrs={'class': 'bodytext'})

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return EckerdJobScraper()
