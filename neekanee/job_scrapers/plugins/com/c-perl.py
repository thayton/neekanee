import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Chesapeake PERL',
    'hq': 'Savage, MD',

    'contact': 'careers@c-perl.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.c-perl.com',
    'jobs_page_url': 'http://www.c-perl.com/index.php?option=com_content&view=article&id=83&Itemid=64',

    'empcnt': [11,50]
}

class CPerlJobScraper(JobScraper):
    def __init__(self):
        super(CPerlJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        n = s.find(text=re.compile('Current Positions'))
        n = n.next

        while hasattr(n, 'name') or n.startswith('Thank you') is False:
            if getattr(n, 'name', None) == 'a':
                job = Job(company=self.company)
                job.title = n.text
                job.url = urlparse.urljoin(self.br.geturl(), n['href'])
                job.location = self.company.location
                jobs.append(job)

            n = n.next

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            p = s.find('p', attrs={'editor_id': 'mce_editor_0'})
            p = p.parent

            job.desc = get_all_text(p)

            m = re.search(r'located in (\w+, \w+)', job['desc'])
            if m:
                l = self.parse_location(m.group(1))
                if l:
                    job.location = l

            job.save()

def get_scraper():
    return CPerlJobScraper()

