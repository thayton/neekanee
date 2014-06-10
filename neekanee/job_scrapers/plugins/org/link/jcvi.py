import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'J. Craig Venter Institute',
    'hq': 'Rockville, MD',

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
        f = s.find('form', id='frmCRSS')
        r = re.compile(r'Careers\.aspx\?adata=')
        a = f.find('a', href=r)

        self.br.open(a['href'])

        s = soupify(self.br.response().read())
        f = s.find('form', id='frmCRSS')
        t = f.find('table', id='CRCareers1_tblTableDetail2')
        r = re.compile(r'^\?adata=')
        x = {'class': 'JobLink', 'href': r}

        for a in t.findAll('a', attrs=x):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[-3].text)
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
            r = re.compile(r'^CRCareers\d+_tblJobDescrDetail$')
            t = s.find('table', id=r)

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return JcviJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
