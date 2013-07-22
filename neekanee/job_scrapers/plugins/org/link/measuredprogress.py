import re, urlparse, copy

from BeautifulSoup import BeautifulSoup
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto
from neekanee.urlutil import url_query_filter

from neekanee_solr.models import *

COMPANY = {
    'name': 'Measured Progress',
    'hq': 'Dover, NH',

    'home_page_url': 'http://www.measuredprogress.org',
    'jobs_page_url': 'https://employment.measuredprogress.org/careers/?',

    'empcnt': [201,500]
}

class MeasuredProgressJobScraper(JobScraper):
    def __init__(self):
        super(MeasuredProgressJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('frmCRSS')

        ctl = self.br.form.find_control(type='select')
        ctl.set_value_by_label(['All'])

        self.br.submit()

        s = soupify(self.br.response().read())
        f = s.find('form', id='frmCRSS')
        x = {'class': 'JobLink'}

        for a in f.findAll('a', attrs=x):
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

        myMassage = [(re.compile(r'<!-\?xml:namespace [^>]+'), lambda m: '')]
        myNewMassage = copy.copy(BeautifulSoup.MARKUP_MASSAGE)
        myNewMassage.extend(myMassage)

        for job in new_jobs:
            self.br.open(job.url)

            d = self.br.response().read()
            s = BeautifulSoup(d, markupMassage=myNewMassage)
            r = re.compile(r'^CRCareers\d+_tblJobDescr$')
            t = s.find('table', id=r)

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return MeasuredProgressJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
