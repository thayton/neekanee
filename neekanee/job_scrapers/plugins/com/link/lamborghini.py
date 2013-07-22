import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Lamborghini',
    'hq': 'Sant\'Agata Bolognese, Italy',

    'home_page_url': 'http://www.lamborghini.com',
    'jobs_page_url': 'http://careers.lamborghini.com/html/people/people_sfoglia_annunci.asp?siteaform=1',

    'empcnt': [501,1000]
}

class LamborghiniJobScraper(JobScraper):
    def __init__(self):
        super(LamborghiniJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'people_sfoglia_annunci\.asp\?cmdRS=open&UID=\d+')
            x = {'class': 'LinkTitoloElencoAnnunci', 'href': r}

            for a in s.findAll('a', attrs=x):
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = self.company.location
                jobs.append(job)

            try:
                self.br.follow_link(self.br.find_link(text='%d' % pageno))
                pageno += 1
            except:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            f = s.find('form', id='formInvio')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return LamborghiniJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
