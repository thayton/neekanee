from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper

COMPANY = {
    'name': 'Thompson Creek Window Company',
    'hq': 'Lanham, MD',

    'ats': 'Taleo',

    'home_page_url': 'http://www.thompsoncreek.com',
    'jobs_page_url': 'http://tbe.taleo.net/CH11/ats/careers/jobSearch.jsp?org=THOMPSONCREEK&cws=1',

    'empcnt': [201,500]
}

class ThompsonCreekJobScraper(TaleoJobScraper):
    def __init__(self):
        super(ThompsonCreekJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[1].text)

def get_scraper():
    return ThompsonCreekJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
