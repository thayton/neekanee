import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'BoxTone',
    'hq': 'Columbia, MD',

    'home_page_url': 'http://www.boxtone.com',
    'jobs_page_url': 'http://boxtone.simplicant.com/',

    'empcnt': [11,50]
}

class BoxToneJobScraper(JobScraper):
    def __init__(self):
        super(BoxToneJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        while True:
            s = soupify(self.br.response().read())
            x = {'class': 'job-listing'}
            y = {'class': 'job-listing-city-box'}

            for d in s.findAll('div', attrs=x):
                l = d.find('span', attrs=y)
                l = self.parse_location(l.span.text)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = d.a.text
                job.url = urlparse.urljoin(self.br.geturl(), d.a['href'])
                job.location = l
                jobs.append(job)

            try:
                self.br.follow_link(self.br.find_link(text='Next'))
            except mechanize.LinkNotFoundError:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'class': 'job-detail'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return BoxToneJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
