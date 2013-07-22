import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_filter
from neekanee_solr.models import *

COMPANY = {
    'name': 'Schneider Electric',
    'hq': 'Rueil-Malmaison, France',

    'home_page_url': 'http://www.schneider-electric.com',
    'jobs_page_url': 'http://www.resumeware.net/se_rw/se_web/job_search.cfm',

    'empcnt': [10001]
}

class SchneiderElectricJobScraper(JobScraper):
    def __init__(self):
        super(SchneiderElectricJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        def select_form(form):
            return form.attrs.get('action', None) == 'job_list.cfm?refcntr='

        self.br.open(url)
        self.br.select_form(predicate=select_form)
        self.br.submit()

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'^job_detail\.cfm\?\S+reqnum=\d+')

            for a in s.findAll('a', href=r):
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.url = url_query_filter(job.url, 'reqnum')
                jobs.append(job)

            try:
                self.br.follow_link(self.br.find_link(text='%d' % pageno))
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
            td = s.find('td', text='Location')
            tr = td.findParent('tr')
            td = tr.findAll('td')
            
            l = self.parse_location(td[-1].text)
            if not l:
                continue

            job.location = l

            t = tr.findParent('table')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return SchneiderElectricJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
