import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Computer Emergency Response Team (CERT)',
    'hq': 'Pittsburgh, PA',

    'benefits': {
        'url': 'http://www.cert.org/jobs/benefits.html',
        'vacation': [(1,17)],
        'holidays': 9
    },

    'home_page_url': 'http://www.cert.org',
    'jobs_page_url': 'http://www.cert.org/jobs/',

    'jobs_page_domain': 'taleo.net',

    'empcnt': [501,1000]
}

class CertJobScraper(JobScraper):
    def __init__(self):
        super(CertJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='jobContainer')
        r = re.compile(r'jobdetail\.ftl\?lang=en&job=\d+')

        for a in d.findAll('a', href=r):
            d = a.findParent('div')

            job = Job(company=self.company)
            if getattr(d, 'b', None):
                job.title = d.b.text
            elif getattr(d, 'strong', None):
                job.title = d.strong.text
            else:
                continue

            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            try:
                self.br.open(job.url)
                s = soupify(self.br.response().read())
            except:
                continue

            i = s.find('input', attrs={'name': 'initialHistory'})
            v = urllib.unquote(i['value'])
            y = v.split('!$!')[2]
            y = y.split('!|!')[9:-4]
            
            job.desc = ' '.join(y)
            job.save()

def get_scraper():
    return CertJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
