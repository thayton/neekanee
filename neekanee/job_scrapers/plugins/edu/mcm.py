import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'McMurry University',
    'hq': 'Abilene, TX',

    'benefits': {
        'url': 'http://www.mcm.edu/newsite/web/human_resources/benefits.htm',
        'vacation': [],
        'holidays': 19
    },

    'home_page_url': 'http://www.mcm.edu',
    'jobs_page_url': 'http://www.mcm.edu/newsite/web/human_resources/employment.htm',

    'gctw_chronicle': True,

    'empcnt': [201,500]
}

class McmJobScraper(JobScraper):
    def __init__(self):
        super(McmJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        links = [ urlparse.urljoin(self.br.geturl(), x) for x in ['faculty.htm', 'staff.htm'] ]
        
        for l in links:
            self.br.open(l)
            s = soupify(self.br.response().read())
            r = re.compile(r'^job_description/')

            for a in s.findAll('a', href=r):
                if len(a.text.strip()) == 0:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = self.company.location
                jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='content')
            t = d.table

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return McmJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
