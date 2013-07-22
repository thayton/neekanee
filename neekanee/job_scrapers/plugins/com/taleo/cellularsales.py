from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

COMPANY = {
    'name': 'Cellular Sales',
    'hq': 'Knoxville, TN',

    'home_page_url': 'http://www.cellularsales.com',
    'jobs_page_url': 'http://tbe.taleo.net/CH05/ats/careers/jobSearch.jsp?org=CELLULARSALES&cws=1&rid=13',

    'empcnt': [1001,5000]
}

class CellularSalesJobScraper(TaleoJobScraper):
    def __init__(self):
        super(CellularSalesJobScraper, self).__init__(COMPANY)

    def get_location_from_s(self, s):
        t = s.find(text='Location:')
        tr1 = t.findParent('tr')
        td1 = tr1.findAll('td')
        tr2 = tr1.findNextSibling('tr')
        td2 = tr2.findAll('td')

        l = td2[-1].text + ', ' + td1[-1].text
        l = self.parse_location(l)

        return self.parse_location(l)

    def get_desc_from_s(self, s):
        t = s.find(text='Location:')
        t = t.findParent('table')

        return get_all_text(t)

def get_scraper():
    return CellularSalesJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
