import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_filter

from neekanee_solr.models import *

COMPANY = {
    'name': 'Kiva',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.kiva.org',
    'jobs_page_url': 'https://kiva-openhire.silkroad.com/epostings/index.cfm?version=1&company_id=16557',

    'empcnt': [51, 200]
}

class KivaJobScraper(JobScraper):
    def __init__(self):
        super(KivaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('frmsearch')
        self.br.submit()

        s = soupify(self.br.response().read())
        x = {'class': 'cssSearchResults'}
        d = s.find('div', attrs=x)
        r = re.compile(r'index\.cfm\?fuseaction=app\.jobinfo&jobid=\d+')
        x = {'class': 'cssSearchResultsBody', 'href': r}

        for a in d.findAll('a', attrs=x):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[2].text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.url = url_query_filter(job.url, ['fuseaction', 'jobid'])
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
            f = s.find('form', id='applyJob')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return KivaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
