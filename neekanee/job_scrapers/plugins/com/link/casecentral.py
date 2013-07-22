import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'CaseCentral',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.casecentral.com',
    'jobs_page_url': 'https://careers.guidancesoftware.com/OA_HTML/OA.jsp?page=/oracle/apps/irc/candidateSelfService/webui/VisHomePG&_ri=821&OAPB=IRC_BRAND&_ti=1213016943&oapc=2&OAMC=75477_29_0&menu=Y&oaMenuLevel=1&oas=k46Kt_NWLnUs4fV4cYOFIg..',

    'empcnt': [51,200]
}

class CaseCentralJobScraper(JobScraper):
    def __init__(self):
        super(CaseCentralJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(self.company.jobs_page_url)
        self.br.select_form('DefaultFormName')
        self.br.form['Keywords'] = 'Guidance'
        self.br.submit()

        s = soupify(self.br.response().read())

        for a in u.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            jobs.append(job)

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'class': 'miscpage jobs'}
            a = s.find('article', attrs=x)
            d = a.findParent('div')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return CaseCentralJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
