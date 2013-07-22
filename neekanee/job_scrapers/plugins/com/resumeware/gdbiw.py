import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_filter
from neekanee_solr.models import *

COMPANY = {
    'name': 'Bath Iron Works',
    'hq': 'Bath, ME',

    'home_page_url': 'https://www.gdbiw.com/',
    'jobs_page_url': 'https://secure.resumeware.net/biw_rw/biw_web/job_search_biw.cfm',

    'empcnt': [5001,10000]
}

class GdbiwJobScraper(JobScraper):
    def __init__(self):
        super(GdbiwJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'^job_detail\.cfm\?recnum=\d+')

            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = self.parse_location(td[1].text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.url = url_query_filter(job.url, 'recnum')
                job.location = l
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
            t = tr.findParent('table')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return GdbiwJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
