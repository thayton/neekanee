import re, urlparse, mechanize, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Alabama A&M University',
    'hq': 'Huntsville, AL',

    'ats': 'InterviewExchange',

    'home_page_url': 'http://www.aamu.edu',
    'jobs_page_url': 'http://aamu.interviewexchange.com/jobsearchfrm.jsp',

    'empcnt': [1001,5000]
}

#
# From com/netscout.py, edu/strose.py
# These plugins follow the same pattern and the
# pattern should go into a class
#
class AamuJobScraper(JobScraper):
    def __init__(self):
        super(AamuJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form(name='jobsrchfrm')
        self.br.submit()

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'jobofferdetails\.jsp\?JOBID=\d+')

            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')
                
                l = self.parse_location(td[0].text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.url = urlutil.url_query_filter(job.url, 'JOBID')
                job.location = l
                jobs.append(job)

            try:
                self.br.follow_link(self.br.find_link(text='Next >>'))
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
            x = {'alt': 'Apply Now'}
            i = s.find('input', attrs=x)

            t0 = i.findParent('table')
            t1 = t0.findParent('table')
            t1 = t1.findParent('table')

            job.desc = get_all_text(t1)
            job.save()

def get_scraper():
    return AamuJobScraper()
