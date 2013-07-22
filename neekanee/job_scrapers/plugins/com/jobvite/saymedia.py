import re, urllib, urlparse

from BeautifulSoup import BeautifulSoup
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'SAY Media',
    'hq': 'San Francisco, CA',

    'ats': 'Jobvite',

    'home_page_url': 'http://www.saymedia.com',
    'jobs_page_url': 'http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=qA09Vfwo&cs=9Dp9VfwQ&nl=0&page=Jobs&jvresize=http://saymedia.typepad.com/files/frameresize.html',

    'empcnt': [201,500]
}

class SayMediaJobScraper(JobScraper):
    def __init__(self):
        super(SayMediaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = BeautifulSoup(self.br.response().read())
        d = s.find('div', attrs={'class': 'jobList'})
        r = re.compile(r'jobs\.php\?jvi=')

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = a['href']
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
            f = s.find('iframe', id='jobviteframe')
            x = job.url.find('jvi=')+4
            j = '&j=' + job.url[x:]
            l = f['src'] + j + '&k=Job'

            self.br.open(l)

            s = soupify(self.br.response().read())
            d = s.find('div', attrs={'class': 'jvcontent'})
            l = d.h1.nextSibling
            l = l.split('|')[1]

            if l.find('United States') == -1:
                continue

            l = re.sub(', United States', '', l)
            l = self.parse_location(l)

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return SayMediaJobScraper()
