import re, urlparse, urllib2

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Enbala',
    'hq': 'Toronto, Canada',

    'home_page_url': 'http://www.enbala.com',
    'jobs_page_url': 'http://www.enbala.com/CONTACT.php?sub=Careers',

    'empcnt': [11,50]
}

class EnbalaJobScraper(JobScraper):
    def __init__(self):
        super(EnbalaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'careers'}
        t = s.find('table', attrs=x)
        r = re.compile(r'CONTACT\.php\?sub=Career_Details&position=')

        for a in t.findAll('a', href=r):
            l = a.text.rsplit('-', 1)

            if len(l) < 2:
                continue

            l = self.parse_location(l[1])

            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.url = urllib2.quote(job.url, '/:?&=,')
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
            x = {'class': 'career_details'}
            t = s.find('table', attrs=x)

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return EnbalaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
