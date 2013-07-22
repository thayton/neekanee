import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'National Instruments',
    'hq': 'Austin, TX',

    'ats': 'Peopleclick',
    'benefits': {
        'vacation': [(0,10)],
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.ni.com',
    'jobs_page_url': 'http://www.ni.com/careers/',

    'bptw_glassdoor': True,
    'gptwcom_fortune': True,

    'empcnt': [5001,10000]
}

class NiJobScraper(JobScraper):
    def __init__(self):
        super(NiJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.follow_link(self.br.find_link(url_regex=re.compile(r'search\.do$')))
        self.br.select_form('searchForm')
        self.br.submit()

        r = re.compile(r'^jobDetails\.do\?functionName=getJobDetail&jobPostId=\d+')
        pageno = 2

        while True:
            s = soupify(self.br.response().read())

            for a in s.findAll('a', href=r):
                tr = a.findAll('tr')

                l = tr[1].findAll('td')[1].text
                l = self.parse_location(l)
                
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = tr[0].findAll('td')[1].text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            # Navigate to the next page
            i = s.find('img', attrs={'alt': 'Next'})
            if not i or i.parent.name != 'button':
                break

            self.br.select_form('searchResultForm')
            self.br.form.set_all_readonly(False)
            self.br.submit(name=i.parent['name'])

            pageno += 1

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            a = {'name': 'jobDetails'}
            f = s.find('form', attrs=a)

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return NiJobScraper()
