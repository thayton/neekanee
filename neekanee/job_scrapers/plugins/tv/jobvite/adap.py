import os, re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Adap.tv',
    'hq': 'San Mateo, CA',

    'ats': 'Jobvite',

    'home_page_url': 'http://adap.tv',
    'jobs_page_url': 'http://hire.jobvite.com/CompanyJobs/Careers.aspx?k=JobListing&c=qb79Vfw6&v=1',

    'empcnt': [11,50]
}

class AdapJobScraper(JobScraper):
    def __init__(self):
        super(AdapJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = { 'class': 'jvjoblink' }

        for a in s.findAll('a', attrs=x):
            tr = a.findParent('tr')
            td = tr.findAll('td')
        
            l = self.parse_location(td[-1].text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = l
            jobs.append(job)
            break

        return jobs


    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = job.url.find('jvi=')
            j = '&j=' + job.url[x+4:]
            l = s.iframe['src'] + j + '&k=Job'

            self.br.open(l)

            s = soupify(self.br.response().read())
            f = s.find('form', attrs={'name': 'jvform'})


            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return AdapJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
