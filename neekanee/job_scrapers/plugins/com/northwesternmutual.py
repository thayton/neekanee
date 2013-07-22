import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Northwestern Mutual',
    'hq': 'Milwaukee, WI',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.northwesternmutual.com',
    'jobs_page_url': 'http://www.northwesternmutual.com/career-opportunities/corporate-opportunities/join-our-team.aspx',

    'empcnt': [5001,10000]
}

class NorthWesternMutualJobScraper(JobScraper):
    def __init__(self):
        super(NorthWesternMutualJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.follow_link(self.br.find_link(text='Job Search'))
        self.br.follow_link(self.br.find_link(tag='frame', name='contentFrame'))

        r = re.compile(r'viewjob\.html\?optlink-view=')

        while True:
            s = soupify(self.br.response().read())
            f = s.find('form', attrs={'name': 'newjoblist'})

            for a in f.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = td[3].text

                if l.find('-') != -1:
                    l = l.split('-')[1]

                l = self.parse_location(l)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            # Navigate to the next page
            try:
                x = re.compile(r'joblist\.html\?pageto-next=')
                n = self.br.find_link(url_regex=x)
                self.br.follow_link(n)
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
            a = {'class': 'pageheading'}
            p = s.find('span', attrs=a)
            td = p.findParent('td')

            job.desc = get_all_text(td)
            job.save()

def get_scraper():
    return NorthWesternMutualJobScraper()
