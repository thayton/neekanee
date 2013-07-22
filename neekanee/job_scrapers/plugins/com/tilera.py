import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Tilera',
    'hq': 'San Jose, CA',

    'home_page_url': 'http://www.tilera.com',
    'jobs_page_url': 'http://www.tilera.com/about_tilera/careers/open_positions',

    'empcnt': [51,200]
}

class TileraJobScraper(JobScraper):
    def __init__(self):
        super(TileraJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        def select_form(form):
            return form.attrs.get('id', None) == 'views-exposed-form-careers-page-1'

        self.br.open(url)
        self.br.select_form(predicate=select_form)

        ctl = self.br.form.find_control(type='select')
        locations = [ x for x in ctl.items if x.name != 'All']

        for x in locations:
            l = self.parse_location(x.attrs['label'])
            if not l:
                continue

            self.br.select_form(predicate=select_form)
            self.br.form['loc'] = ['%s' % x.attrs['value']]
            self.br.submit()

            s = soupify(self.br.response().read())
            v = {'class': 'job-title'}

            for p in s.findAll('p', attrs=v):
                job = Job(company=self.company)
                job.title = p.a.text
                job.url = urlparse.urljoin(self.br.geturl(), p.a['href'])
                job.location = l
                jobs.append(job)

            self.br.back()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return TileraJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
