import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Lafarge',
    'hq': 'Paris, France',

    'home_page_url': 'http://www.lafarge.com',
    'jobs_page_url': 'http://www.lafargecareers.com',

    'empcnt': [10001]
}

class LafargeJobScraper(JobScraper):
    def __init__(self):
        super(LafargeJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        x = self.br.response().read()
        r = re.compile(r'var myPath = "([^"]+)"')
        m = re.search(r, x)
        u = urlparse.urljoin(self.br.geturl(), m.group(1) + '&lang=EN')

        self.br.open(u)

        s = soupify(self.br.response().read())
        a = s.find(text='Other offers').parent
        u = urlparse.urljoin(self.br.geturl(), a['href'])

        self.br.open(u)

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'job_detail\.jsp\?')
        
            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = td[-1].text + ', ' + td[-2].text
                l = self.parse_location(l)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            try:
                self.br.follow_link(self.br.find_link(text='%d' % pageno))
                pageno += 1
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
            x = {'class': 'mainPage'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return LafargeJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
