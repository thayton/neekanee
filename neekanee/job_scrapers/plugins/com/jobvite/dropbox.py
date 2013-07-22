import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Dropbox',
    'hq': 'San Francisco, CA',

    'ats': 'Jobvite',

    'home_page_url': 'http://www.dropbox.com',
    'jobs_page_url': 'http://hire.jobvite.com/CompanyJobs/Jobs.aspx?c=qD19Vfws&jvresize=http://www.dropbox.com/frameresize.htm',

    'empcnt': [11,50]
}

class DropboxJobScraper(JobScraper):
    def __init__(self):
        super(DropboxJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile('position\?')
        v = { 'class': 'joblist', 'id': 'joblist' }
        d = s.find('div', attrs=v)

        for a in d.findAll('a', href=r):
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
            x = job.url.find('jvi=')+4
            j = '&j=' + job.url[x:]

            self.br.open(s.iframe['src'] + j)

            s = soupify(self.br.response().read())
            d = s.find('div', attrs={'class': 'jvcontent'})

            job.desc = get_all_text(d)

            l = s.h1.parent.contents[-1]
            l = l.rsplit('|', 1)

            if len(l) > 1:
                l = self.parse_location(l[1])
                if l:
                    job.location = l

            job.save()

def get_scraper():
    return DropboxJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
