import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Colwen Management',
    'hq': 'Nashua, NH',

    'home_page_url': 'http://www.colwenhotels.com',
    'jobs_page_url': 'http://www.colwenhotels.com/hotel-management-careers-en.html',

    'empcnt': [501,1000]
}

class ColwenJobScraper(JobScraper):
    def __init__(self):
        super(ColwenJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='mod_pukkaJobs')
        r = re.compile(r'careers_viewItem')
        x = {'class': 'categoryTitle'}
        y = {'class': 'itemPreviewTitle'}

        for a in d.findAll('a', href=r):
            t = a.findPrevious('h4', attrs=y)
            h = a.findPrevious('h3', attrs=x)
            l = self.parse_location(h.text)

            if not l:
                continue
            
            job = Job(company=self.company)
            job.title = t.text
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
            x = {'class': 'itemContent'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ColwenJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
