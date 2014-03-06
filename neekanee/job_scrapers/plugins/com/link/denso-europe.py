import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'DENSO Europe',
    'hq': 'Kariya, Japan',

    'home_page_url': 'http://www.denso-europe.com',
    'jobs_page_url': 'http://www.densojobs.com',

    'empcnt': [10001]
}

class DensoJobScraper(JobScraper):
    def __init__(self):
        super(DensoJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        def select_form(form):
            return form.attrs.get('id', None) == 'search-banner-form'

        self.br.open(url)
        self.br.select_form(predicate=select_form)
        self.br.submit()

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'^/jobs/\S+-\d+$')
            x = {'class': 'job-meta'}

            for a in s.findAll('a', href=r):
                if a.parent.name != 'h3':
                    continue

                p = a.findParent('li')
                d = p.find('div', attrs=x)
                v = d.findAll('div')
                l = ', '.join(['%s' % z.contents[-1] for z in v[1:3]])
                l = self.parse_location(l)

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
            x = {'class': 'uWidget uWidget-jobs-detail'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return DensoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
