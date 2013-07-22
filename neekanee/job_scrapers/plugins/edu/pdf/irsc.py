import re, urlparse, mechanize, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from BeautifulSoup import BeautifulSoup, SoupStrainer
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Indian River State College',
    'hq': 'Fort Pierce, FL',

    'benefits': {
        'url': 'http://www.irsc.edu/humanresources/benefits/benefits.aspx?id=629',
        'vacation': [(1,12),(6,15),(11,18)],
        'holidays': 18,
        'sick_days': 12
    },

    'home_page_url': 'http://www.irsc.edu',
    'jobs_page_url': 'http://www.irsc.edu/humanresources/employment/employment.aspx?id=633',

    'gctw_chronicle': True,

    'empcnt': [11,50]
}

class IsrcJobScraper(JobScraper):
    def __init__(self):
        super(IsrcJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        links = [ 'Administration', 'Faculty', 'Part-Time Adjunct Faculty',
                  'Full-Time Support', 'Part-Time Support' ]

        for link in links:
            try:
                self.br.follow_link(self.br.find_link(text=link))
            except mechanize.LinkNotFoundError:
                continue

            r = re.compile(r'/WorkArea/linkit\.aspx\?LinkIdentifier=id&ItemID=\d+')
            t = re.compile(r'^Continue to the Position Listing', re.I)

            self.br.follow_link(self.br.find_link(url_regex=r, text_regex=t))

            tables = SoupStrainer('table')

            s = BeautifulSoup(self.br.response().read(), parseOnlyThese=tables)
            v = re.compile(r'/uploadedFiles/HumanResources/Employment/.*\.pdf$')

            for a in s.findAll('a', href=v):
                t = a.findParent('table')

                tr = t.findAll('tr')
                td = tr[0].findAll('td')

                job = Job(company=self.company)
                job.title = td[0].text
                job.url = urlparse.urljoin(self.br.geturl(), urllib.quote(a['href'], safe='/:'))
                job.location = self.company.location
                jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            d = self.br.response().read()
            s = BeautifulSoup(pdftohtml(d))

            job.desc = get_all_text(s.html.body)
            job.save()

def get_scraper():
    return IsrcJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
