from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper

COMPANY = {
    'name': 'Landor',
    'hq': 'San Francisco, CA',

    'ats': 'Taleo',

    'home_page_url': 'http://landor.com',
    'jobs_page_url': 'https://tbe.taleo.net/CH08/ats/careers/jobSearch.jsp?org=YRBRANDS&cws=13',

    'empcnt': [501,1000]
}

class LandorJobScraper(TaleoJobScraper):
    def __init__(self):
        super(LandorJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

def get_scraper():
    return LandorJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
