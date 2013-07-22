import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Nuvotronics',
    'hq': 'Radford, VA',

    'home_page_url': 'http://nuvotronics.com',
    'jobs_page_url': 'http://nuvotronics.appone.com',

    'empcnt': [51,200]
}

class NuvotronicsJobScraper(JobScraper):
    def __init__(self):
        super(NuvotronicsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        def select_form(form):
            return form.attrs.get('action', None) == 'Menu.asp'

        self.br.open(url)
        self.br.select_form(predicate=select_form)
        self.br.submit()

        s = soupify(self.br.response().read())
        r = re.compile(r'MainInfoReq\.asp\?')
        
        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[-2].text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
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
            t = s.find(text='Title')
            t = t.findParent('table')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return NuvotronicsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
