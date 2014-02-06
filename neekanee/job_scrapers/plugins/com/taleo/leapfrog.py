from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper

COMPANY = {
    'name': 'LeapFrog',
    'hq': 'Emeryville, CA',

    'home_page_url': 'http://www.leapfrog.com',
    'jobs_page_url': 'https://tbe.taleo.net/CH08/ats/careers/jobSearch.jsp?org=LEAPFROG&cws=1',

    'empcnt': [501,1000]
}

class LeapFrogJobScraper(TaleoJobScraper):
    def __init__(self):
        super(LeapFrogJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[1].text)

def get_scraper():
    return LeapFrogJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
