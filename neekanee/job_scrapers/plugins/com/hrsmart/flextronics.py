import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Flextronics',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.flextronics.com',
    'jobs_page_url': 'https://flextronics.hua.hrsmart.com/hr/ats/JobSearch/index',

    'empcnt': [10001]
}

class FlextronicsJobScraper(JobScraper):
    def __init__(self):
        super(FlextronicsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        def select_form(form):
            return form.attrs.get('id', None) == 'jobSearchForm'

        self.br.open(url)
        self.br.select_form(predicate=select_form)
        self.br.submit('search_jobs')

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'^/hr/ats/Posting/view/\d+$')

            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = self.parse_location(td[1].text)
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
    return FlextronicsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
