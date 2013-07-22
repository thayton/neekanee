import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'BNY Mellon',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.bnymellon.com',
    'jobs_page_url': 'http://jobs.bnymellon.com',

    'empcnt': [10001]
}

class BnyMellonJobScraper(JobScraper):
    def __init__(self):
        super(BnyMellonJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        def select_form(form):
            return form.attrs.get('id', None) == 'searchbykeyword'

        self.br.open(url)
        self.br.select_form(predicate=select_form)
        self.br.submit()

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            x = {'class': 'jobTitle'}
            y = {'class': 'jobLocation'}
            t = s.find('table', id='searchresults')

            for p in s.findAll('span', attrs=x):
                if not p.a:
                    continue

                tr = p.findParent('tr')
                l = tr.find('span', attrs=y)
                l = self.parse_location(l.text)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = p.a.text
                job.url = urlparse.urljoin(self.br.geturl(), p.a['href'])
                job.location = l
                jobs.append(job)

            try:
                self.br.follow_link(self.br.find_link(text='Page %d' % pageno))
                pageno += 1
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
            d = s.find('div', id='content')
            x = {'class': 'jobDisplayShell'}
            d = d.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return BnyMellonJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
