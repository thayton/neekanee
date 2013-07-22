import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Statoil',
    'hq': 'Stavanger, Norway',

    'home_page_url': 'http://www.statoil.com',
    'jobs_page_url': 'http://www.statoil.com/en/Careers/JobOpportunities/VacantPositions/Pages/default.aspx',

    'empcnt': [10001]
}

class StatoilJobScraper(JobScraper):
    def __init__(self):
        super(StatoilJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        r = re.compile(r'/en/Careers/JobOpportunities/VacantPositions/Pages/\d+\.aspx$')
        x = {'class': 'searchResult'}

        while True:
            s = soupify(self.br.response().read())
            o = s.find('ol', attrs=x)

            for a in o.findAll('a', href=r):
                p = a.findAll('span')
                l = a.find(text=re.compile(r'Location:'))
                l = l.split('Location:')[1]
                l = self.parse_location(l)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
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
            x = {'class': 'articleBody'}
            d = s.find('div', attrs=x)
            d = d.findParent('div')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return StatoilJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
