import re, time, urllib, urlparse, mechanize, urlutil, copy, json

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, extract_form_fields
from BeautifulSoup import BeautifulSoup
from neekanee_solr.models import *

COMPANY = {
    'name': 'Stryker',
    'hq': 'Kalamazoo, MI',

    'home_page_url': 'http://www.stryker.com',
    'jobs_page_url': 'http://jobs.brassring.com/TGWebHost/home.aspx?partnerid=25787&siteid=5361',

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

    def fix_current_html(self):
        m = [(re.compile('<!=+=>'), lambda match: '<!-- -->')]
        mm = copy.copy(BeautifulSoup.MARKUP_MASSAGE)
        mm.extend(m)

        s = BeautifulSoup(self.br.response().read(), markupMassage=mm)

        html = s.prettify()
        resp = mechanize.make_response(html, [("Content-Type", "text/html")],
                                       self.br.geturl(), 200, "OK")
        self.br.set_response(resp)        
        
    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.fix_current_html()

        self.br.follow_link(self.br.find_link(text_regex=re.compile(r'Search openings', re.I)))
        self.fix_current_html()

        self.br.select_form('aspnetForm')
        self.br.form.new_control('hidden', 'submit2', {'value':''})
        self.br.form.new_control('hidden', 'GTGLanguageList', {'value':'1||1033'})
        self.br.submit()

        r = re.compile(r'^jobdetails\.asp')
        numResults = 0

        while True:
            self.fix_current_html()
            s = soupify(self.br.response().read())
            i = s.find('input', id='ctl00_MainContent_GridFormatter_json_tabledata')
            j = json.loads(i['value'])

            for x in j:
                l = x['FORMTEXT22'] + ', ' + x['FORMTEXT26']
                l = self.parse_location(l)

                if not l:
                    continue

                a = soupify(x['AutoReq'])
                a = a.findAll('a')

                job = Job(company=self.company)
                job.title = x['JobTitle']
                job.url = self.mkurl(urlparse.urljoin(self.br.geturl(), a[-1]['href']))
                job.location = l
                jobs.append(job)

            numResults += len(j)

            f = s.find('form', attrs={'name': 'frmMassSelect'})
            html = f.prettify()
            resp = mechanize.make_response(html, [("Content-Type", "text/html")],
                                           self.br.geturl(), 200, "OK")
            self.br.set_response(resp)
            self.br.select_form('frmMassSelect')

            if numResults >= int(self.br.form['totalrecords']):
                break

            self.br.form.set_all_readonly(False)
            self.br.form['recordstart'] = '%d' % (numResults + 1)

            try:
                self.br.submit()
            except:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)
            self.fix_current_html()

            s = soupify(self.br.response().read())
            d = s.find('div', id='PrimaryContentBlock')
            t = d.findParent('table')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return StrykerJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
