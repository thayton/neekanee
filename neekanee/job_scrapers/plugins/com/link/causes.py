import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Causes',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.causes.com',
    'jobs_page_url': 'https://www.causes.com/careers',

    'empcnt': [11,50]
}

class CausesJobScraper(JobScraper):
    def __init__(self):
        super(CausesJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'jobs-open-positions-category'}
        
        for a in s.findAll('a', attrs=x):
            u = urlparse.urljoin(self.br.geturl(), a['href'])
            self.br.open(u)

            z = soupify(self.br.response().read())
            y = {'class': 'job-post-primary'}
            d = z.find('div', attrs=y)
            h = d.findPrevious('h1')

            job = Job(company=self.company)
            job.title = h.text
            job.url = urlparse.urljoin(self.br.geturl(), u)
            job.location = self.company.location
            job.desc = get_all_text(d)
            jobs.append(job)

            y = {'class': 'job-post-secondary'}
            r = re.compile(r'^/careers/\d+-')

            for a in z.findAll('a', href=r):
                if a.text in ['%s' % t.title for t in jobs]:
                    continue

                u = urlparse.urljoin(self.br.geturl(), a['href'])

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), u)
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
            x = {'class': 'job-post-primary'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return CausesJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()

