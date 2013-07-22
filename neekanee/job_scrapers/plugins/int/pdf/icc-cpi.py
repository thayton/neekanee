import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'International Criminal Court',
    'hq': 'The Hague, Netherlands',

    'home_page_url': 'http://www.icc-cpi.int',
    'jobs_page_url': 'http://www.icc-cpi.int/en_menus/icc/recruitment/job%20opportunities/Pages/icc%20e_recruiting.aspx',

    'empcnt': [5001,10000]
}

class IccJobScraper(JobScraper):
    def __init__(self):
        super(IccJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'content'}
        d = s.find('div', attrs=x)
        r = re.compile(r'/iccdocs/HR/\S+\.pdf$')

        for a in d.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')
            
            l = self.parse_location(td[-2].text)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), urllib.quote(a['href'], '/:'))
            job.location = l
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            d = self.br.response().read()
            s = soupify(pdftohtml(d))

            job.desc = get_all_text(s.html.body)
            job.save()

def get_scraper():
    return IccJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
