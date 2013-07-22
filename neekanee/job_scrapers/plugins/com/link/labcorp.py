import re, urlparse, mechanize, urllib2

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'LabCorp',
    'hq': 'Burlington, NC',

    'home_page_url': 'http://www.labcorp.com',
    'jobs_page_url': 'http://jobs.labcorp.com/careers/',

    'empcnt': [10001]
}

class LabCorpJobScraper(JobScraper):
    def __init__(self):
        super(LabCorpJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        while True:
            s = soupify(self.br.response().read())
            d = s.find('div', id='divMain')
            r = re.compile(r'^jobs_list_link_\d+$')

            for a in d.findAll('a', id=r):
                tr = a.findParent('tr')
                td = tr.find('td', attrs={'class': 'location'})

                l = self.parse_location(td.text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.url = job.url.encode('utf8')
                job.url = urllib2.quote(job.url, '/:')
                job.location = l
                jobs.append(job)

            # Navigate to the next page
            a = s.find('a', id='jobs_next_page_link')
            if not a:
                break

            u = urlparse.urljoin(self.br.geturl(), a['href'])
            self.br.open(u)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', attrs={'class': 'jobs star'})

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return LabCorpJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
