import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Syngenta',
    'hq': 'Basel, Switzerland',

    'ats': 'PeopleXS',

    'home_page_url': 'http://www.syngenta.com',
    'jobs_page_url': 'https://ssl1.peoplexs.com/Peoplexs22/CandidatesPortalNoLogin/Search.cfm?CustomerCode=SYN1&PortalID=620',

    'empcnt': [10001]
}

class SyngentaJobScraper(JobScraper):
    def __init__(self):
        super(SyngentaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('EditForm')
        self.br.submit(name='Save')

        while True:
            s = soupify(self.br.response().read())
            x = {'class': 'vacancies'}
            t = s.find('table', attrs=x)
            r = re.compile(r'Vacancy\.cfm\?\S+VacatureID=\d+')

            for a in t.findAll('a', href=r):
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
                self.br.follow_link(self.br.find_link(text='>>'))
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
            x = {'class': 'DataTable'}
            t = s.find('table', attrs=x)

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return SyngentaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
