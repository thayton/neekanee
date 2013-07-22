import re, time, urllib, urlparse, mechanize, urlutil, copy

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, extract_form_fields
from BeautifulSoup import BeautifulSoup
from neekanee_solr.models import *

COMPANY = {
    'name': 'Stryker',
    'hq': 'Kalamazoo, MI',

    'home_page_url': 'http://www.stryker.com',
    'jobs_page_url': 'http://jobs.brassring.com/1033/ASP/TG/cim_home.asp?partnerid=11721&siteid=78',

    'empcnt': [10001]
}

# This companies HTML is so broken we can't use the base class
class StrykerJobScraper(JobScraper):
    def __init__(self):
        super(StrykerJobScraper, self).__init__(COMPANY)

    def mkurl(self, job_link):
        """
        Query portion of the url returned looks like this:

        cim_jobdetail.asp?jobId=1212739&siteId=69&partnerid=119

        Full url eg:

        https://sjobs.brassring.com/en/asp/tg/cim_jobdetail.asp?jobId=1212739&siteId=69&partnerid=119
        """
        items = urlutil.url_query_get(self.company.jobs_page_url.lower(), ['partnerid', 'siteid'])

        url = urlutil.url_query_filter(job_link, 'jobId')
        url = urlutil.url_query_add(url, items.iteritems())

        return url

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.follow_link(self.br.find_link(text_regex=re.compile(r'Search openings', re.I)))

        m = [(re.compile('<!=+=>'), lambda match: '<!-- -->')]
        mm = copy.copy(BeautifulSoup.MARKUP_MASSAGE)
        mm.extend(m)

        s = BeautifulSoup(self.br.response().read(), markupMassage=mm)
        s = soupify(s.prettify())

        html = s.prettify()
        resp = mechanize.make_response(html, [("Content-Type", "text/html")],
                                           self.br.geturl(), 200, "OK")

        self.br.set_response(resp)        
        self.br.select_form('frmAgent')
        self.br.submit()

        r = re.compile(r'^cim_jobdetail\.asp')

        while True:
            s = BeautifulSoup(self.br.response().read(), markupMassage=mm)

            html = s.prettify()
            resp = mechanize.make_response(html, [("Content-Type", "text/html")],
                                           self.br.geturl(), 200, "OK")

            self.br.set_response(resp)        
            s = soupify(self.br.response().read())

            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                if not tr:
                    continue

                td = tr.findAll('td')

                l = '-'.join(['%s' % x.text for x in td[-5:-2] if x.text != '-'])
                l = self.parse_location(l)
                
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = td[3].text
                job.location = l
                job.url = self.mkurl(urlparse.urljoin(self.br.geturl(), a['href']))
                jobs.append(job)

            # Navigate to the next page
            try:
                n = self.br.find_link(text='Next')
                m = re.search(r'(\d+)', n.url)
            except mechanize.LinkNotFoundError:
                break

            self.br.select_form('frmMassSelect')
            self.br.form.set_all_readonly(False)
            self.br.form['recordstart'] = m.group(0)
            self.br.submit()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            m = [(re.compile('<!=+=>'), lambda match: '<!-- -->')]
            mm = copy.copy(BeautifulSoup.MARKUP_MASSAGE)
            mm.extend(m)

            s = BeautifulSoup(self.br.response().read(), markupMassage=mm)
            s = soupify(s.prettify())
            a = {'name': 'frmJobDetail'}
            f = s.find('form', attrs=a)

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return StrykerJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
