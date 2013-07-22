import re, urlparse, mechanize, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'The Endocrine Society', 
    'hq': 'Chevy Chase, MD',

    'home_page_url': 'http://www.endo-society.org',
    'jobs_page_url': 'https://apps.endocrine.org/apps/PlacementServices/SearchJobs/index.cfm',

    'empcnt': [51,200]
}

class EndoSocietyJobScraper(JobScraper):
    def __init__(self):
        super(EndoSocietyJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        r = re.compile(r'^ViewPosition\.cfm\?SearchKey=\w+&PositionID=\d+$')

        self.br.open(url)
        self.br.select_form('JobSearchForm')
        self.br.form.set_all_readonly(False)
        self.br.form['Country'] = ['United States of America']
        self.br.submit(id='PS_Submit')

        while True:
            s = soupify(self.br.response().read())
            t = s.find('table', attrs={'class': 'data'})

            for a in t.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = td[1].text + ', ' + td[2].text
                l = self.parse_location(l)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.url = urlutil.url_query_del(job.url, 'SearchKey')
                job.location = l
                jobs.append(job)

            # Navigate to the next page
            try:
                self.br.follow_link(text='Next')
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
            d = s.find('div', id='center')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return EndoSocietyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
