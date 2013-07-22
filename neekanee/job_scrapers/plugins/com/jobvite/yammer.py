import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Yammer',
    'hq': 'San Francisco, CA',

    'ats': 'Jobvite',

    'home_page_url': 'https://www.yammer.com',
    'jobs_page_url': 'https://hire.jobvite.com/CompanyJobs/Jobs.aspx?c=qI19Vfwx&jvresize=/wp-content/themes/roots/js/jobvite_frameresize.html',

    'empcnt': [51,200]
}

class YammerJobScraper(JobScraper):
    def __init__(self):
        super(YammerJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/job_description\?jvi=\w+,Job')
        v = { 'class': 'jvcontent' }
        t = s.find('table', attrs=v)

        for a in t.findAll('a', href=r):
            l = self.parse_location(a.findNext('td').text)
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
    return YammerJobScraper()
