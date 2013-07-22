import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Emerson',
    'hq': 'St. Louis, MO',

    'home_page_url': 'http://www.emerson.com',
    'jobs_page_url': 'https://us2.i-grasp.com/fe/tpl_Emerson01.asp',

    'empcnt': [10001]
}

class EmersonJobScraper(JobScraper):
    def __init__(self):
        super(EmersonJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('data')
        self.br.form.method = 'get'
        self.br.submit(name='formsubmit4')
        
        while True:
            s = soupify(self.br.response().read())

            for d in s.findAll('div', id='jobtitletext'):
                a = d.parent.a

                tr = d.findParent('tr')
                td = tr.findAll('td')

                l = '-'.join(['%s' % x.text for x in td[-3:]])
                l = self.parse_location(l)
                
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            try:
                def next_link(link):
                    return dict(link.attrs).get('class', None) == 'nextbullet'

                self.br.follow_link(self.br.find_link(predicate=next_link))
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
            d = s.find('div', id='igContainer')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return EmersonJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
