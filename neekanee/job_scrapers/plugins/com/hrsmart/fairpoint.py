import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Fairpoint Communications',
    'hq': 'Charlotte, NC',

    'home_page_url': 'http://www.fairpoint.com',
    'jobs_page_url': 'https://fairpointcareers.hua.hrsmart.com/hrsmart/ats/JobSearch/index',

    'empcnt': [1001,5000]
}

class FairpointJobScraper(JobScraper):
    def __init__(self):
        super(FairpointJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        def select_form(form):
            return form.attrs.get('id', None) == 'jobSearchForm'

        self.br.open(url)
        self.br.select_form(predicate=select_form)
        self.br.submit(name='search_jobs')

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            t = s.find('table', id='jobSearchResultsGrid_table')
            r = re.compile(r'^/hrsmart/ats/Posting/view/\d+$')

            for a in t.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = td[1].text.split(',', 1)
                l = self.parse_location(l[0])

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            try:
                self.br.follow_link(self.br.find_link(text='%d' % pageno))
                pageno += 1
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
            d = s.find('div', id='app_main_id')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return FairpointJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
