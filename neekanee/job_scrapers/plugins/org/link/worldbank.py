import re, urlparse, urllib2, xmllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'The World Bank',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.worldbank.org',
    'jobs_page_url': 'http://web.worldbank.org/external/default/main?pagePK=8453982&piPK=8453986&theSitePK=8453353&contentMDK=23158967&order=descending&sortBy=job-req-num&location=ALL&type=ALL&family=ALL&menuPK=8453611',

    'empcnt': [5001,10000]
}

class WorldBankJobScraper(JobScraper):
    def __init__(self):
        super(WorldBankJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        t = s.find('table', id='listingTable')
        x = {'headers': 'Job Number'}

        for td in t.findAll('td', attrs=x):
            tr = td.findParent('tr')

            l = tr.find(headers='Location').text
            l = self.parse_location(l)

            if not l:
                continue

            #
            # From the JS sources for this page:
            #
            # detUrl=$(this).find("a").attr("anchor_attr");
            # append_type=$(this).siblings(".cat_type").text();
            # append_type=append_type.replace("/","2Z");        
            # append_type=encodeURIComponent(append_type);
            # append_grade=$(this).siblings(".job_grade").text();
            #
            # detUrl= detUrl+"&"+"JobType="+append_type+"&"+"JobGrade="+append_grade;
            #
            a = td.a
            p = xmllib.XMLParser()

            cat_type = tr.find('td', attrs={'class': 'cat_type'}).text
            cat_type = p.translate_references(cat_type)
            cat_type = urllib2.quote(cat_type)
            job_grade = tr.find('td', attrs={'class': 'job_grade'}).text

            url = a['anchor_attr']+"&JobType="+cat_type+"JobGrade="+job_grade;

            job = Job(company=self.company)
            job.title = tr.find(headers='JobTitle').text
            job.url = urlparse.urljoin(self.br.geturl(), url)
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
            x = {'class': 'job-detail'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return WorldBankJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
