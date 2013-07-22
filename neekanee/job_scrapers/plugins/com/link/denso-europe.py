import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'DENSO Europe',
    'hq': 'Kariya, Japan',

    'home_page_url': 'http://www.denso-europe.com',
    'jobs_page_url': 'http://careers.denso-europe.com/',

    'empcnt': [10001]
}

class DensoJobScraper(JobScraper):
    def __init__(self):
        super(DensoJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        def select_form(form):
            return form.action.endswith('advanced-search.php')

        self.br.open(url)
        self.br.select_form(predicate=select_form)
        self.br.submit()

        s = soupify(self.br.response().read())
        d = s.find('div', id='job-results-container')
        x = {'class': 'job_details'}
        
        for v in d.findAll('div', attrs=x):
            tr = v.table.findAll('tr')[-1]
            td = tr.findAll('td')[-1]

            p = v.findParent('article')
            l = self.parse_location(td.text)

            if not l:
                continue

            y = p.find('div', attrs={'class': 'job_read_more'})
            a = y.a

            job = Job(company=self.company)
            job.title = p.h1.text
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
            d = s.find('div', id='page_content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return DensoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
