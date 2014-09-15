import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'ERGO',
    'hq': 'Dusseldorf, Germany',

    'home_page_url': 'http://www.ergo.com',
    'jobs_page_url': 'http://ergo.hrdepartment.de/ergo/de/',

    'empcnt': [10001]
}

class ErgoJobScraper(JobScraper):
    def __init__(self):
        super(ErgoJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        def select_form(form):
            return form.attrs.get('action', None) == '/ergo/de/result'

        self.br.open(url)
        self.br.select_form(predicate=select_form)
        self.br.submit()

        while True:
            s = soupify(self.br.response().read())
            d = s.find('div', id='tms-results-table')
            r = re.compile(r'highlightjob\.cgi\?jobid=\d+$')
            x = {'class': 'tms-link-active', 'href': r}

            for a in d.findAll('a', attrs=x):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = td[-2].text + ', Germany'
                l = self.parse_location(l)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            try:
                self.br.follow_link(self.br.find_link(text='weiter >'))
            except mechanize.LinkNotFoundError:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            p = s.find('span', id='monsterIA')

            job.desc = get_all_text(p)
            job.save()

def get_scraper():
    return ErgoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
