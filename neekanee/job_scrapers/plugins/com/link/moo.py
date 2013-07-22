import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'MOO',
    'hq': 'London, UK',

    'home_page_url': 'http://www.moo.com',
    'jobs_page_url': 'http://us.moo.com/about/jobs/',

    'empcnt': [51,200]
}

class MooJobScraper(JobScraper):
    def __init__(self):
        super(MooJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': re.compile(r'job-listing')}
        d = s.find('div', attrs=x)
        r = re.compile(r'^/about/jobs/\S+\.html$')
        
        for a in d.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            f = lambda x: len(z.text) and z.text or z.img['alt']
            l = '-'.join(['%s' % f(z) for z in td if z['class'] in ['city', 'country']])
            l = self.parse_location(l)
            
            if not l:
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
            x = {'class': re.compile(r'job-description')}            
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return MooJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
