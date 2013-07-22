import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Bouygues Telecom',
    'hq': 'Paris, France',

    'home_page_url': 'http://www.bouyguestelecom.fr',
    'jobs_page_url': 'http://www.emploi.bouyguestelecom.fr/offre-de-emploi/liste-toutes-offres.aspx?LCID=1036',

    'empcnt': [5001,10000]
}

class BouyguesTelecomJobScraper(JobScraper):
    def __init__(self):
        super(BouyguesTelecomJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        t = s.find(text='Localisation')
        r = re.compile(r'/offre-de-emploi/liste-toutes-offres\.aspx')
        u = t.findNext('ul')

        for a in u.findAll('a', href=r):
            l = a.text.rsplit('(', 1)[0]
            l = l + ', France'
            l = self.parse_location(l)

            if not l:
                continue

            self.br.open(a['href'])

            pageno = 2

            while True:
                s = soupify(self.br.response().read())
                d = s.find('div', id='listing-resultat')
                r1 = re.compile(r'/offre-de-emploi/')
                r2 = re.compile(r'ListeOffre\S+lnkAccesOffre')
                x = {'href': r1, 'id': r2, 'title': True}

                for b in d.findAll('a', attrs=x):
                    job = Job(company=self.company)
                    job.title = b.text
                    job.url = urlparse.urljoin(self.br.geturl(), b['href'])
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
            d = s.find('div', id='contenu-ficheoffre')
            d = d.findParent('div')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return BouyguesTelecomJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
