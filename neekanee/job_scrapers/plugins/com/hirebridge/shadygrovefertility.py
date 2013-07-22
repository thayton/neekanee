import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Shady Grove Fertility Center',
    'hq': 'Rockville, MD',

    'ats': 'Hirebridge',

    'benefits': {
        'vacation': [],
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.shadygrovefertility.com',
    'jobs_page_url': 'http://careers.shadygrovefertility.com/searchpositions.php',

    'empcnt': [201,500]
}

class ShadyGroveFertilityJobScraper(JobScraper):
    def __init__(self):
        super(ShadyGroveFertilityJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.follow_link(self.br.find_link(tag='iframe', name='frame1'))
    
        s = soupify(self.br.response().read())
        r = re.compile(r'^viewdetail\.asp\?joblistid=\d+')

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[2].text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = l
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.find('table', attrs={'class': 'InteriorPage'})

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return ShadyGroveFertilityJobScraper()
