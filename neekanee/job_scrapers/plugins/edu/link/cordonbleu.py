import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Le Cordon Bleu',
    'hq': 'Paris, France',

    'home_page_url': 'http://www.cordonbleu.edu',
    'jobs_page_url': 'http://www.cordonbleu.edu/careers/en',

    'empcnt': [1001,5000]
}

class CordonBleuJobScraper(JobScraper):
    def __init__(self):
        super(CordonBleuJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)


        s = soupify(self.br.response().read())
        r = re.compile(r'^index\.cfm\?fa=CareerMod.DisplayCareer&CareerID=\d+$')

        for a in s.findAll('a', href=r):
            g = a.findPrevious('strong')
            l = self.parse_location(g.text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(s.base['href'], a['href'])
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
            d = s.find('div', id='SingleContent')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return CordonBleuJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
