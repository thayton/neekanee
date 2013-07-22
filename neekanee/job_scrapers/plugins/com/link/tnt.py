import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'TNT Express',
    'hq': 'Amsterdam, Netherlands',

    'home_page_url': 'http://www.tnt.com',
    'jobs_page_url': 'http://www.tnt.com/corporatecareer/?null',

    'empcnt': [10001]
}

class TntJobScraper(JobScraper):
    def __init__(self):
        super(TntJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('form1')
        self.br.submit()

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'career\.html\?VacancyId=\d+$')
            x = {'class': 'locationLabel'}

            for a in s.findAll('a', href=r):
                li = a.findParent('li')
                l = li.find('span', attrs=x)
                l = self.parse_location(l.text)

                if not l:
                    continue

                u = 'http://www.tnt.com/corporatecareer/Vacancy.aspx'
                q = urlparse.urlparse(a['href']).query

                job = Job(company=self.company)
                job.title = a.text
                job.url = u + '?' + q
                job.location = l
                jobs.append(job)

            f = lambda x: x.name == 'a' and x.text == 'Next'
            a = s.find(f)

            if a.get('disabled', None) or not a.get('href', None):
                break

            r = re.compile(r"__doPostBack\('([^']+)")
            m = re.search(r, a['href'])

            self.br.select_form('form1')

            ctl = self.br.form.find_control('btnHiddenSubmit')
            self.br.form.controls.remove(ctl)

            self.br.form.new_control('hidden', 'ScriptManager1',  {'value': 'ListPanel|'+ m.group(1)})
            self.br.form.new_control('hidden', '__EVENTTARGET',   {'value': m.group(1)})
            self.br.form.new_control('hidden', '__EVENTARGUMENT', {'value': ''})
            self.br.submit()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='vacancyContent')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return TntJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
