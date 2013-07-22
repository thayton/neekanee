import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Emmanuel College',
    'hq': 'Boston, MA',

    'ats': 'InterviewExchange',

    'home_page_url': 'http://www.emmanuel.edu',
    'jobs_page_url': 'http://emmanuel.interviewexchange.com/static/clients/13EM1/listJobs.jsp',

    'empcnt': [201,500]
}

#
# From com/netscout.py, edu/strose.py
# These plugins follow the same pattern and the
# pattern should go into a class
#
class EmmanuelJobScraper(JobScraper):
    def __init__(self):
        super(EmmanuelJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/jobofferdetails\.jsp\?JOBID=\d+')

        for a in s.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
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
            x = {'alt': 'Apply Now'}
            i = s.find('input', attrs=x)

            t0 = i.findParent('table')
            t1 = t0.findParent('table')
            t1 = t1.findParent('table')

            l = t0.find(text='Locations:').findNext('td').text
            if l.find(';') != -1:
                l = l.rsplit(';', 1)[1]

            l = self.parse_location(l)
            if not l:
                continue

            job.location = l
            job.desc = get_all_text(t1)
            job.save()

def get_scraper():
    return EmmanuelJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
