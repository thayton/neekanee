import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'WayFair',
    'hq': 'Boston, MA',

    'benefits': {'vacation': [(0,15)]},

    'home_page_url': 'http://www.wayfair.com',
    'jobs_page_url': 'http://hire.jobvite.com/Jobvite/Jobs.aspx?b=nbv7Ogwm',

    'empcnt': [501,1000]
}

class WayFairJobScraper(JobScraper):
    def __init__(self):
        super(WayFairJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'Jobvite/Job\.aspx\?b=')

            for a in s.findAll('a', href=r):
                if a.parent.name != 'b':
                    continue

                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = td[0].findAll('span')[1]
                l = self.parse_location(l.text)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            f = lambda x: x.name == 'a' and x.text == 'Next'
            a = s.find(f)

            if not a:
                break

            r = re.compile(r"__doPostBack\('([^']+)','([^']+)")
            m = re.search(r, a['href'])

            self.br.select_form('Form1')

            ctl = self.br.form.find_control('Submit1')
            self.br.form.controls.remove(ctl)

            self.br.form.new_control('hidden', '__EVENTTARGET',   {'value': m.group(1)})
            self.br.form.new_control('hidden', '__EVENTARGUMENT', {'value': m.group(2)})
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
            f = s.find('form', attrs={'name': 'Form1'})

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return WayFairJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
