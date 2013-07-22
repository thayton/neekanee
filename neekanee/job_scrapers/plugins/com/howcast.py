import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Howcast Media',
    'hq': 'San Francisco, CA',

    'contact': 'jobs@howcast.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.howcast.com',
    'jobs_page_url': 'http://info.howcast.com/jobs',

    'empcnt': [11,50]
}

class HowCastJobScraper(JobScraper):
    def __init__(self):
        super(HowCastJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', attrs={'class': 'main'})

        for h in d.findAll('h2'):
            a = h.a
            if a and a['href'].startswith('/jobs/'):
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
            d = s.find('div', attrs={'class': 'main'})

            l = d.find('p', attrs={'class': 'footnote'})
            l = self.parse_location(l.text)

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return HowCastJobScraper()
