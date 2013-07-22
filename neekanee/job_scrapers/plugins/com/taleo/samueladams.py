from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

COMPANY = {
    'name': 'Samuel Adams',
    'hq': 'Boston, MA',

    'ats': 'Taleo',

    'home_page_url': 'http://www.samueladams.com',
    'jobs_page_url': 'http://ch.tbe.taleo.net/CH08/ats/careers/jobSearch.jsp?org=BOSTONBEER&cws=38',

    'empcnt': [201,500]
}

# Taleo only lists states so we have to manually figure out the company/job locations
locations = {
    'AZ': 'Tucson',
    'CA': 'San Diego',
    'CO': 'Denver',
    'GA': 'Athens',
    'LA': 'New Orleans',
    'MA': 'Boston',
    'MD': 'Baltimore',
    'MN': 'Minneapolis',
    'NC': 'Asheville',
    'NY': 'New York',
    'OH': 'Cincinnati',
    'PA': 'Breinigsville',
    'TX': 'Austin',
    'WA': 'Seattle'
}

class SamuelAdamsJobScraper(TaleoJobScraper):
    def __init__(self):
        super(SamuelAdamsJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = locations.get(td[-1].text, None)
        if l:
            l += ', ' + td[-1].text
            return self.parse_location(l)
        else:
            return None

    def get_desc_from_s(self, s):
        t = s.h1.findParent('table')
        return get_all_text(t)

def get_scraper():
    return SamuelAdamsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
