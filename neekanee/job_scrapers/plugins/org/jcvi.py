import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'J. Craig Venter Institute',
    'hq': 'Rockville, MD',

    'benefits': {
        'url': 'http://www.jcvi.org/cms/nc/careers/why-choose-jcvi/benefits/',
        'vacation': [],
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.jcvi.org',
    'jobs_page_url': 'https://careers.jcvi.org/careers/Careers.aspx',

    'empcnt': [201,500]
}

class JcviJobScraper(JobScraper):
    def __init__(self):
        super(JcviJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^Careers\.aspx\?adata=')
        u = s.find('a', href=r)['href']
        u = urlparse.urljoin(url, u)

        self.br.open(u)

        s = soupify(self.br.response().read())
        f = s.find('form', id='frmCRSS')
        t = f.find('table', id='CRCareers1_tblTableDetail2')
        r = re.compile(r'^\?adata=')
        x = {'class': 'JobLink', 'href': r}

        for a in t.findAll('a', attrs=x):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'class': 'HeaderStyle'}

            td = s.find('td', attrs=x)
            tr = td.findParent('tr')

            job.desc = ''

            x = tr
            while x and getattr(x, 'name', None) != 'input':
                if hasattr(x, 'name') is False:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return JcviJobScraper()
