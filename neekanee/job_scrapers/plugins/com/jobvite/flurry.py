import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_add

from neekanee_solr.models import *

COMPANY = {
    'name': 'Airy Labs',
    'hq': 'San Francisco, CA',

    'ats': 'Jobvite',

    'home_page_url': 'http://www.flurry.com',
    'jobs_page_url': 'http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=qH59VfwA&jvprefix=http%3a%2f%2fwww.flurry.com&cs=9oy9VfwK&jvresize=http%3a%2f%2fflurry.com%2fjobvite.html',

    'empcnt': [51,200]
}

class FlurryJobScraper(JobScraper):
    def __init__(self):
        super(FlurryJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = { 'class': 'jvjoblink', 'href': '#' }
        r = re.compile(r"jvGoToPage\('Job Description','','(.*)'\)")

        for a in s.findAll('a', attrs=d):
            tr = a.findParent('tr')
            td = tr.findAll('td')
        
            l = self.parse_location(td[-1].text)
            if not l:
                continue

            m = re.search(r, a['onclick'])
            jobid = m.group(1)
            query = {'j': '%s,Job' % jobid, 'k': 'Job'}

            job = Job(company=self.company)
            job.title = a.text
            job.url = url_query_add(self.br.geturl(), query.items())
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
            f = s.find('form', attrs={'name': 'jvform'})

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return FlurryJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
