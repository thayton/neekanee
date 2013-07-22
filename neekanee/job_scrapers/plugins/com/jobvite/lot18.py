import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Lot18',
    'hq': 'Manhattan, NY',

    'ats': 'Jobvite',

    'contact': 'jobs@lot18.com',

    'home_page_url': 'http://www.lot18.com',
    'jobs_page_url': 'http://hire.jobvite.com/CompanyJobs/PreviewCareers.aspx?c=qv69Vfwp&cs=9Kz9Vfw7&jvresize=http://www.lot18.com/css/clients/jobvite/frameresize.html',

    'empcnt': [11,50]
}

class Lot18JobScraper(JobScraper):
    def __init__(self):
        super(Lot18JobScraper, self).__init__(COMPANY)

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

            job = Job(company=self.company)
            job.title = a.text
            job.url = self.new_url(self.br.geturl(), jobid)
            job.location = l
            jobs.append(job)

        return jobs

    def new_url(self, url, jobid):
        u = urlparse.urlparse(url)
        l = urlparse.parse_qsl(u.query)
        x = dict(l)

        x['page'] = 'Job Description'
        x['j'] = jobid

        u = list(u)
        u[4] = urllib.urlencode(x)
        u = urlparse.urlunparse(u)

        return u

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
    return Lot18JobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
