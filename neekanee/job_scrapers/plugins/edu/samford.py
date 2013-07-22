import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Samford University',
    'hq': 'Birmingham, AL',

    'home_page_url': 'http://www.samford.edu',
    'jobs_page_url': 'http://www.samford.edu/jobs/',

    'empcnt': [501,1000]
}

class SamfordJobScraperStaff(JobScraper):
    def __init__(self):
        super(SamfordJobScraperStaff, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.follow_link(self.br.find_link(text='View all staff Jobs'))

        s = soupify(self.br.response().read())
        r = re.compile(r'^/jobs/job\.aspx\?id=\d+$')

        for a in s.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)
        self.scrape_new_jobs(new_jobs)

    def scrape_new_jobs(self, new_jobs):
        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='PanelContent')

            job.desc = get_all_text(d)
            job.save()

class SamfordJobScraperFaculty(JobScraper):
    def __init__(self):
        super(SamfordJobScraperFaculty, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.follow_link(self.br.find_link(text='View all faculty jobs'))

        s = soupify(self.br.response().read())
        r = re.compile(r'\.pdf$')

        for a in s.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)
        self.scrape_new_jobs(new_jobs)

    def scrape_new_jobs(self, new_jobs):
        for job in new_jobs:
            self.br.open(job.url)

            data = self.br.response().read()
            s = soupify(pdftohtml(data))

            job.desc = get_all_text(s.html.body)
            job.save()

class SamfordJobScraper(JobScraper):
    def __init__(self):
        self.staff_job_scraper = SamfordJobScraperStaff()
        self.faculty_job_scraper = SamfordJobScraperFaculty()
        super(SamfordJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        staff_jobs = self.staff_job_scraper.scrape_job_links(self.company.jobs_page_url)
        faculty_jobs = self.faculty_job_scraper.scrape_job_links(self.company.jobs_page_url)

        job_list = staff_jobs + faculty_jobs

        self.prune_unlisted_jobs(job_list)

        self.staff_job_scraper.scrape_new_jobs(staff_jobs)
        self.faculty_job_scraper.scrape_new_jobs(faculty_jobs)
        
def get_scraper():
    return SamfordJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
