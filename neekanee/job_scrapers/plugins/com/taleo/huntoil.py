from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper

COMPANY = {
    'name': 'Hunt Oil Company',
    'hq': 'Dallas, TX',

    'ats': 'Taleo',

    'home_page_url': 'http://www.huntoil.com',
    'jobs_page_url': 'https://tbe.taleo.net/CH08/ats/careers/jobSearch.jsp?org=HUNTOIL&cws=1',

    'empcnt': [51,200]
}

class HuntOilJobScraper(TaleoJobScraper):
    def __init__(self):
        super(HuntOilJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = ', '.join([x.text for x in td[4:]])
        return self.parse_location(l)

def get_scraper():
    return HuntOilJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
