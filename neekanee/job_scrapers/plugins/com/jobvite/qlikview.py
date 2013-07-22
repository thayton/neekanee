import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'QlikView',
    'hq': 'Radnor, PA',

    'home_page_url': 'http://www.qlikview.com',
    'jobs_page_url': 'http://www.qlikview.com/us/company/careers/current-openings?dept=&region=all',

    'empcnt': [1001,5000]
}

class QlikViewJobScraper(JobScraper):
    def __init__(self):
        super(QlikViewJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            d = s.find('div', id='detail')
            r = re.compile(r'/company/careers/current-openings/jobvite/')

            for a in d.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = td[-2].text + ', ' + td[-1].text
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
            d = s.find('div', id='detail')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return QlikViewJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
