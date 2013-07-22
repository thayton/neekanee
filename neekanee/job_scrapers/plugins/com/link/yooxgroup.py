import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Yoox Group',
    'hq': 'Bologna, Italy',

    'home_page_url': 'http://www.yooxgroup.com/en/homepage.asp',
    'jobs_page_url': 'http://yoox.hrweb.it/elenco_annunci.php',

    'empcnt': [201,500]
}

class YooxGroupJobScraper(JobScraper):
    def __init__(self):
        super(YooxGroupJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        locations = { 'Italy - Milano': 8073,
                      'Italy - Bologna Interporto': 9088,
                      'Italy - Bologna': 9037,
                      'United States - New York City': 9083,
                      'Spain - Madrid': 9083,
                      'France - Paris': 9085,
                      'Japan - Tokyo': 9086,
                      'China - Shanghai': 9087 }

        self.br.open(url)

        for location,id in locations.items():
            l = self.parse_location(location)
            if not l:
                continue

            self.br.select_form('ricercaForm')
            self.br.form.set_all_readonly(False)
            self.br.form['provinciaID'] = '%d' % id
            self.br.submit()

            pageno = 2        

            while True:
                s = soupify(self.br.response().read())
                r = re.compile(r'dettaglio_annuncio\.php\?id_an=\d+$')

                for a in s.findAll('a', href=r):
                    tr = a.findParent('tr')
                    td = tr.findAll('td')
            
                    job = Job(company=self.company)
                    job.title = td[-1].text
                    job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                    job.location = l
                    jobs.append(job)

                try:
                    z = re.compile(r'cambiaPagina\(%d\)' % pageno)

                    self.br.find_link(url_regex=z)
                    self.br.select_form('ricercaForm')
                    self.br.form.set_all_readonly(False)
                    self.br.form['provinciaID'] = '%d' % id
                    self.br.form['paginaScelta'] = '%d' % pageno
                    self.br.submit()

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
            d = s.find('div', id='padding_dx')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return YooxGroupJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
