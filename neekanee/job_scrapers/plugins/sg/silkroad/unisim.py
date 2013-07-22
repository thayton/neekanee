import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'SIM University',
    'hq': 'Singapore, Singapore',

    'home_page_url': 'http://www.unisim.edu.sg',
    'jobs_page_url': 'http://www.unisim.edu.sg/careers/appointments-vacancies/Pages/NonAcademic_Appointments.aspx',
    'jobs_page_domain': 'silkroad.com',

    'empcnt': [201,500]
}

class UnisimJobScraper(JobScraper):
    def __init__(self):
        super(UnisimJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.follow_link(self.br.find_link(tag='iframe'))
        self.br.follow_link(self.br.find_link(text='All Posted Jobs'))

        s = soupify(self.br.response().read())
        r = re.compile(r'/epostings/submit.cfm\?fuseaction=app\.jobinfo')

        for a in s.findAll('a', href=r):
            l = a.parent.contents[3]
            l = self.parse_location(l)
            
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
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
            f = s.find('form', id='applyJob')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return UnisimJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
