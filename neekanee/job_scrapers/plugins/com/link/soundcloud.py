import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'SoundCloud',
    'hq': 'Berlin, Germany',

    'home_page_url': 'http://soundcloud.com',
    'jobs_page_url': 'http://soundcloud.com/jobs',

    'empcnt': [51,200]
}

class SoundCloudJobScraper(JobScraper):
    def __init__(self):
        super(SoundCloudJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/jobs/\d{4}-\d{2}-\d{2}-[a-z-]+$')

        self.company.job_set.all().delete()

        for a in s.findAll('a', href=r):
            l = self.parse_location(a.span.text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.contents[0]
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
            r = re.compile(r'jobDescription')
            x = {'class': r}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return SoundCloudJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
