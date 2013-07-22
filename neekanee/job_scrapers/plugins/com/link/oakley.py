import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Oakley',
    'hq': 'Foothill Ranch, CA',

    'home_page_url': 'http://www.oakley.com',
    'jobs_page_url': 'http://jobs.oakley.com',

    'empcnt': [1001,5000]
}

class OakleyJobScraper(JobScraper):
    def __init__(self):
        super(OakleyJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        def select_form(form):
            return form.attrs.get('id', None) == 'search-form'

        self.br.open(url)
        self.br.select_form(predicate=select_form)
        self.br.submit()

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            x = {'class': 'jobTitle'}
            y = {'class': 'colLocation'}
        
            for p in s.findAll('span', attrs=x):
                if not p.a:
                    continue

                tr = p.findParent('tr')
                td = tr.find('td', attrs=y)

                l = self.parse_location(td.text)
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
            x = {'class': 'jobDisplay'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return OakleyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
