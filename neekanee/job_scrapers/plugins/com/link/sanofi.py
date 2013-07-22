import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Sanofi',
    'hq': 'Paris, France',

    'home_page_url': 'http://en.sanofi.com',
    'jobs_page_url': 'https://fr-en.sanofi-aventis-job.com',

    'empcnt': [10001]
}

class SanofiJobScraper(JobScraper):
    def __init__(self):
        super(SanofiJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('jobSearch')
        self.br.submit()

        r = re.compile(r'^JobDetail\.aspx\?\S*Job_Id=\S+$')

        while True:
            s = soupify(self.br.response().read())
            t = s.find('table', id='dgResultJob')

            for a in t.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                if a.parent != td[2]:
                    continue

                l = td[-2].text + ', ' + td[-3].text
                l = self.parse_location(l)

                if l is None:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            # Navigate to the next page
            i = s.find('input', id='btnNext')
            if not i or i.get('disabled', None):
                break

            self.br.select_form('jobResultListForm')
            self.br.submit('btnNext')

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.find('table', id='jobDescription')
            d = t.parent

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return SanofiJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
