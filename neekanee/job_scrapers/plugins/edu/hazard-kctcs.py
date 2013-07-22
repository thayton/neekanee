import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Hazard Community and Technical College',
    'hq': 'Hazard, KY',

    'benefits': {
        'url': 'http://www.kctcs.edu/Faculty_and_Staff/Employee_Benefits_Summary.aspx',
        'vacation': [(1,15),(6,20)],
        'holidays': 11,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.hazard.kctcs.edu',
    'jobs_page_url': 'http://www.hazard.kctcs.edu/Job_Seekers',

    'gctw_chronicle': True,

    'empcnt': [201,500]
}

class HazardJobScraper(JobScraper):
    def __init__(self):
        super(HazardJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        a = s.find('a', title='Current Employment Opportunities')

        url = urlparse.urljoin(self.br.geturl(), a['href'])
        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'jobDetails\.asp\?jid=\d+&cid=\d+')

        for a in s.findAll('a', href=r):
            l = self.parse_location(a.findNext('td').text)
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
            t = s.find('td', attrs={'class': 'jobTitle'})
            t = t.findParent('table')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return HazardJobScraper()
