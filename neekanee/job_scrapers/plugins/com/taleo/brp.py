from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper

COMPANY = {
    'name': 'BRP',
    'hq': 'Valcourt, Canada',

    'ats': 'Taleo',

    'home_page_url': 'http://www.brp.com',
    'jobs_page_url': 'http://sj.tbe.taleo.net/SJ6/ats/careers/jobSearch.jsp?org=BRP2&cws=1',

    'empcnt': [5001,10000]
}

class BrpJobScraper(TaleoJobScraper):
    def __init__(self):
        super(BrpJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

def get_scraper():
    return BrpJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
