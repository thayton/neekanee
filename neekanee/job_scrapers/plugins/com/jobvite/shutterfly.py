import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'shutterfly',
    'hq': 'Redwood City, CA',

    'ats': 'Jobvite',

    'home_page_url': 'http://www.shutterfly.com',
    'jobs_page_url': 'http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=qm09Vfwa&jvresize=http://www.shutterfly.com/about/frameresize.htm',

    'empcnt': [501,1000]
}

class ShutterFlyJobScraper(JobScraper):
    def __init__(self):
        super(ShutterFlyJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/positions\.jsp\?jvi=')
        v = { 'class': 'jobList' }
        d = s.find('div', attrs=v)

        for a in d.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[1].text)

            if l is None:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = a['href']
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
            x = job.url.find('jvi=')+4
            j = '&j=' + job.url[x:]
            l = s.iframe['src'] + j + '&k=Job'
            
            self.br.open(l)

            s = soupify(self.br.response().read())
            d = s.find('div', attrs={'class': 'jvcontent'})

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ShutterFlyJobScraper()
