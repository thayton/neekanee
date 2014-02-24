import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Cynosure',
    'hq': 'Westford, MA',

    'home_page_url': 'http://www.cynosure.com',
    'jobs_page_url': 'http://www.cynosure.com/about-cynosure/careers/job-openings/',
    'jobs_page_domain': 'eease.com',

    'empcnt': [501,1000]
}

class BottomlineJobScraper(JobScraper):
    def __init__(self):
        super(BottomlineJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_job_links(self, url):
        jobs = []
        job_links = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        r = re.compile(r'/careers/job-openings/[^/]+/$')
        t = re.compile(r'home\.eease\.adp\.com/recruit/\?id=\d+')

        for a in d.findAll('a', href=r):
            url = urlparse.urljoin(self.br.geturl(), a['href'])
            self.br.open(url)

            z = soupify(self.br.response().read())
            for a in z.findAll('a', href=t):
                h = a.findPrevious('h3')

                if len(h.contents) > 1:
                    l = re.sub(r'Location\s*:', '', h.contents[-1])
                    l = self.parse_location(l)
                    if not l:
                        continue
                else:
                    l = self.company.location

                job = Job(company=self.company)
                job.url = a['href']
                job.location = l
                jobs.append(job)

            self.br.back()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            f = s.find('form')
            t = f.table
            x = {'class': 'postingTitle'}
            p = f.find('span', attrs=x)

            if not p:
                continue

            job.title = p.text
            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return BottomlineJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
