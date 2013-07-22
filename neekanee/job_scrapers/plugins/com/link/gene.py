import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_filter

from neekanee_solr.models import *

COMPANY = {
    'name': 'Genentech',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.gene.com',
    'jobs_page_url': 'http://www.gene.com/careers',

    'empcnt': [10001]
}

class GeneJobScraper(JobScraper):
    def __init__(self):
        super(GeneJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        def select_form(form):
            return form.attrs.get('id', None) == 'jobsearch_form'

        self.br.open(url)
        self.br.select_form(predicate=select_form)
        self.br.submit()

        r = re.compile(r'/careers/detail/\d+')

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            x = {'class': 'content careers-results'}
            d = s.find('div', attrs=x)

            for a in d.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = self.parse_location(td[-2].text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)
                break

            # Navigate to the next page
            try:
                self.br.follow_link(self.br.find_link(text='%d' % pageno))
                pageno += 1
                break
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
            x = {'class': 'inner'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return GeneJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
