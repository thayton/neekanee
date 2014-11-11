import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Choice Hotels International',
    'hq': 'Rockville, MD',

    'home_page_url': 'http://www.choicehotels.com',
    'jobs_page_url': 'http://careers.choicehotels.com',

    'empcnt': [1001,5000]
}

class ChoiceHotelsJobScraper(JobScraper):
    def __init__(self):
        super(ChoiceHotelsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        def select_form(form):
            return form.attrs.get('id', None) == 'jobsQuickSearchContainer'

        self.br.open(url)
        self.br.select_form(predicate=select_form)
        self.br.submit()

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            t = s.find('table', id='careerResults')
            r = re.compile(r'^careers/jobDetails\.html\?')
        
            for a in t.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                # Skip featured/latest jobs
                if a.parent['class'].find('highlight') != -1:
                    continue

                l = self.parse_location(td[-2].text)
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
            d = s.find('div', id='careerResults')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ChoiceHotelsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
