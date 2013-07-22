import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'RAXCO Software',
    'hq': 'Gaithersburg, MD',

    'home_page_url': 'http://perfectdisk.raxco.com',
    'jobs_page_url': 'http://www.raxco.com/about-us/careers.aspx',

    'empcnt': [11,50]
}

class RaxcoJobScraper(JobScraper):
    def __init__(self):
        super(RaxcoJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        f = lambda x: x.name == 'h2' and x.text == 'Open Positions'
        h = s.find(f)
        p = h.findNext('p')
        r = re.compile(r'\.aspx$$')

        for a in p.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text.strip()
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.html.find('div', attrs={'class': 'column-two'})

            l = d.find(text=re.compile(r'Location:'))
            if l:
                l = l.split('Location:')[1]
                l = self.parse_location(l)

                if not l:
                    continue
            else:
                l = self.company.location

            job.desc = get_all_text(d)
            job.location = l
            job.save()

def get_scraper():
    return RaxcoJobScraper()
