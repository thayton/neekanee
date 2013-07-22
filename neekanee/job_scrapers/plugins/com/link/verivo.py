import re, mechanize, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Verivo',
    'hq': 'Waltham, MA',

    'home_page_url': 'http://www.verivo.com',
    'jobs_page_url': 'http://www.verivo.com/about-us/careers/',

    'empcnt': [51,200]
}

class VerivoJobScraper(JobScraper):
    def __init__(self):
        super(VerivoJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'title': 'Careers', 'href': self.company.jobs_page_url}
        a = s.find('a', attrs=x)
        x = {'class': 'children'}
        u = a.findNext('ul', attrs=x)
        r1 = re.compile(r'/about-us/careers/[a-z-]+/$')
        r2 = re.compile(r'/careers/[a-z-]+/$')

        for a in u.findAll('a', href=r1):
            l = urlparse.urljoin(self.br.geturl(), a['href'])
            self.br.open(l)

            s = soupify(self.br.response().read())
            x = {'class': 'list-posts-wrapper'}
            d = s.find('div', attrs=x)

            if not d:
                continue

            for a in d.findAll('a', href=r2):
                s = soupify(self.br.response().read())

                title = a.text.lower().strip()
                if title.startswith('read more'):
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = self.company.location
                jobs.append(job)

            self.br.back()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', attrs={'class': 'site-content'})

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return VerivoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
