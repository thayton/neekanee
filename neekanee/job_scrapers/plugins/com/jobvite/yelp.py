import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Yelp',
    'hq': 'New York, NY',

    'ats': 'Jobvite',

    'home_page_url': 'http://www.yelp.com',
    'jobs_page_url': 'http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=q6X9VfwR&cs=9oj9Vfwv&nl=0&jvresize=http://www.yelp.com/html/jobvite.html',

    'empcnt': [501,1000]
}

class YelpJobScraper(JobScraper):
    def __init__(self):
        super(YelpJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile('/jobs\?jvi=')
        v = { 'class': 'joblist', 'id': 'joblist' }
        d = s.find('div', attrs=v)

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = a['href']
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
            p = d.find('span', attrs={'class': 'city'})
            l = self.parse_location(p.text)

            if l is None:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return YelpJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
