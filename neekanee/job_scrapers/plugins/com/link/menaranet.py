import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Menara Networks',
    'hq': 'Dallas, TX',

    'home_page_url': 'http://www.menaranet.com',
    'jobs_page_url': 'http://menaranet.com/index.php?route=news/ncategory&ncat=60',

    'empcnt': [11,50]
}

class MenaraNetJobScraper(JobScraper):
    def __init__(self):
        super(MenaraNetJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        r = re.compile(r'index\.php\?route=news/article&ncat=\d+&news_id=\d+$')

        for a in d.findAll('a', href=r):
            if a.span:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(url, a['href'])
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'class': 'feature'}
            d = s.find('div', attrs=x)
                
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return MenaraNetJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()