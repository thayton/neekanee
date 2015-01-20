import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Widener University',
    'hq': 'Chester, PA',

    'home_page_url': 'http://www.widener.edu',
    'jobs_page_url': 'https://widener.igreentree.com/CSS_External/CSSPage_Welcome.asp',

    'empcnt': [1001,5000]
}

class WidenerJobScraper(JobScraper):
    def __init__(self):
        super(WidenerJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        def select_link(link):
            d = dict(link.attrs)
            return d.get('title', None) == 'Find Jobs'

        self.br.open(url)
        self.br.follow_link(self.br.find_link(predicate=select_link))
        self.br.select_form('frmCSSSearch')
        self.br.submit()

        pageno = 2

        while True:
            # https://widener.iGreentree.com/CSS_External/CSSPage_Referred.ASP?Req=A14-0034
            b = 'CSSPage_Referred.ASP?Req=%s'
            s = soupify(self.br.response().read())
            x = {'title': 'Click to view job description'}

            for a in s.findAll('a', attrs=x):
                td = a.findNext('td')

                req = a.text.replace(r'&nbsp;', '')
                job = Job(company=self.company)
                job.title = td.text
                job.url = urlparse.urljoin(self.br.geturl(), b % req)
                job.location = self.company.location
                jobs.append(job)

            try:
                self.br.select_form('frmPage%d' % pageno)
                self.br.submit()
                pageno += 1
            except:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)
            self.br.select_form('frmRedirect')
            self.br.submit()

            s = soupify(self.br.response().read())
            d = s.find('div', id='WorkArea')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return WidenerJobScraper()
    
if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
