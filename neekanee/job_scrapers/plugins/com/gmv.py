import re, urlparse, urllib, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'GMV',
    'hq': 'Rockville, MD',

    'home_page_url': 'http://www.gmv.com',
    'jobs_page_url': 'http://www.gmv.com/en/Employment/index.html',

    'empcnt': [501,1000]
}

class GmvJobScraper(JobScraper):
    def __init__(self):
        super(GmvJobScraper, self).__init__(COMPANY)
        self.geocoder.return_usa_only = False

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('form1')
        self.br.submit()

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            d = s.find('div', id='contenido_empleo_790')
            r = re.compile(r'^/en/Employment/\S+\.html$')
            x = {'class': 'link_tabla_empleo', 'href': r}

            for a in s.findAll('a', attrs=x):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                c = td[-3].text.split(',')[0]            
                if len(c.strip()) == 0:
                    continue

                l = self.parse_location(c + ',' + td[2].text)

                if l is None:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            try:
                r = re.compile(r'^\s*%d\s*$' % pageno)
                self.br.follow_link(self.br.find_link(text_regex=r))
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
            x = {'class': 'titular_seccion'}
            p = s.find('p', attrs=x)
            d = p.findParent('div')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return GmvJobScraper()
