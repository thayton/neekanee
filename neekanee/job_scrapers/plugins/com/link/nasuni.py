import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Nasuni',
    'hq': 'Natick, MA',

    'home_page_url': 'http://www.nasuni.com',
    'jobs_page_url': 'http://www.nasuni.com/company/careers',

    'empcnt': [11,50]
}

class NasuniJobScraper(JobScraper):
    def __init__(self):
        super(NasuniJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/company/careers/[^/]+/$')
        f = lambda x: x.name == 'a' and x.get('title', False) and re.search(r'Learn More', x.text)
        
        for a in s.findAll(f):
            job = Job(company=self.company)
            job.title = a['title']
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
            x = {'class': 'page_title'}
            h = s.find('h1', attrs=x)
            d = h.findParent('div')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return NasuniJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
