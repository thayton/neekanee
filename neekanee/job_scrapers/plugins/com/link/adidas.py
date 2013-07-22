import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Adidas',
    'hq': 'Herzogenaurach, Germany',

    'home_page_url': 'http://www.adidas.com',
    'jobs_page_url': 'http://careers.adidas-group.com/search-jobs.aspx',

    'empcnt': [10001]
}

class AdidasJobScraper(JobScraper):
    def __init__(self):
        super(AdidasJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        def select_form(form):
            return form.attrs.get('id', None) == 'aspnetForm'

        self.br.open(url)
        self.br.select_form(predicate=select_form)
        self.br.submit()

        while True:
            s = soupify(self.br.response().read())
            x = {'class': 'search-results-listing'}
            t = s.find('table', attrs=x)
            r = re.compile(r'^search-jobs-description\.aspx\?refnum=')
        
            for a in t.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = td[3].text + ', ' + td[2].text
                l = self.parse_location(l)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            y = {'class': 'next'}
            a = s.find('a', attrs=y)

            if not a:
                break

            r = re.compile(r"__doPostBack\('([^']+)")
            m = re.search(r, a['href'])
            
            self.br.select_form(predicate=select_form)                

            ctl = self.br.form.find_control('ctl00$content$btnSearchJobs')
            self.br.form.controls.remove(ctl)

            self.br.form.new_control('hidden', '__EVENTTARGET',   {'value': m.group(1)})
            self.br.form.new_control('hidden', '__EVENTARGUMENT', {'value': ''})
            self.br.form.new_control('hidden', '__LASTFOCUS',     {'value': ''})
            self.br.form.fixup()
            self.br.submit()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'class': 'job-desciption-info'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return AdidasJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
