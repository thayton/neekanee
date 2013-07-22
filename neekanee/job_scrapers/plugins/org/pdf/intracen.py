import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'International Trade Centre',
    'hq': 'Geneva, Switzerland',

    'home_page_url': 'http://www.intracen.org',
    'jobs_page_url': 'http://legacy.intracen.org/appli1/ephf/Vacancies.aspx?lang=en',

    'empcnt': [201,500]
}

class IntracenJobScraper(JobScraper):
    def __init__(self):
        super(IntracenJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'table table_vacancies'}
        t = s.find('table', attrs=x)
        r = re.compile(r'jobman/viewpdf\.aspx\?vid=\d+')

        for a in t.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            if td[1].text.find('--') != -1:
                continue

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

            d = self.br.response().read()
            s = soupify(pdftohtml(d))

            job.desc = get_all_text(s.html.body)
            job.save()

def get_scraper():
    return IntracenJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
