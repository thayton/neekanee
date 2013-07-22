import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Habitat for Humanity International',
    'hq': 'Atlanta, GA',

    'home_page_url': 'http://www.habitat.org',
    'jobs_page_url': 'http://www.habitat.org/hr/search',

    'empcnt': [501,1000]
}

class HabitatJobScraper(JobScraper):
    def __init__(self):
        super(HabitatJobScraper, self).__init__(COMPANY)
        
    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            x = {'class': re.compile(r'view-job-listings')}
            d = s.find('div', attrs=x)
            r = re.compile(r'^/job/')
        
            for a in d.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                if td[1].text == 'TBD':
                    continue

                l = '-'.join(['%s' % x.text for x in td[1:4] if len(x.text)])
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
            d = s.find('div', id='main-content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return HabitatJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
