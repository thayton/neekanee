import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from django.utils.encoding import smart_str, smart_unicode

from neekanee_solr.models import *


COMPANY = {
    'name': 'Intuit',
    'hq': 'Mountain View, CA',

    'home_page_url': 'http://www.intuit.com',
    'jobs_page_url': 'http://jobs.intuit.com/careers/',

    'empcnt': [5001, 10000]
}

class IntuitJobScraper(JobScraper):
    def __init__(self):
        super(IntuitJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        while True:
            s = soupify(self.br.response().read())
            d = s.find('div', id='contents')
            x = {'class': 'tableSearchResults'}
            t = d.find('table', attrs=x)
            r = re.compile(r'/jobid\d+-\S+-jobs$')
        
            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = self.parse_location(td[1].text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            try:
                self.br.follow_link(self.br.find_link(text='Next page'))
            except mechanize.LinkNotFoundError:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            try:
                self.br.open(job.url)
            except:
                continue

            s = soupify(self.br.response().read())
            x = {'class': 'jobDesc'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return IntuitJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
