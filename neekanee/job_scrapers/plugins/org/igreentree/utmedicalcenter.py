import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from urlutil import url_query_filter

from neekanee_solr.models import *

COMPANY = {
    'name': 'University of Tennessee Medical Center',
    'hq': 'Knoxville, TN',

    'home_page_url': 'http://www.utmedicalcenter.org',
    'jobs_page_url': 'https://utmc.igreentree.com/css_external/CSSPage_Welcome.asp',

    'empcnt': [1001,5000]
}

class UtmcJobScraper(JobScraper):
    def __init__(self):
        super(UtmcJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('frmFindReqByID')
        self.br.submit()

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            d = s.find('div', id='WorkArea')
            x = {'title': 'Click to view job description'}

            for a in d.findAll('a', attrs=x):
                tb = a.findParent('table')
                tr = tb.findParent('tr')
                td = tr.findAll('td')

                reqno = td[-1].text
                reqno = reqno.replace('&nbsp;', '')
                
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), '/CSS_External/CSSPage_Referred.ASP?Req=%s' % reqno)
                job.location = self.company.location
                jobs.append(job)

            a = s.find('a', text='%d' % pageno)
            if not a:
                break

            self.br.select_form('frmPage%d' % pageno)
            self.br.submit()

            pageno += 1

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
            x = {'class': 'Tbl'}
            t = s.find('table', attrs=x)

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return UtmcJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
