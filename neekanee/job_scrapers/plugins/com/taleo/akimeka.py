from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper

COMPANY = {
    'name': 'Akimeka',
    'hq': 'Kihei, HI',

    'ats': 'Taleo',

    'home_page_url': 'http://akimeka.com',
    'jobs_page_url': 'http://tbe.taleo.net/NA12/ats/careers/jobSearch.jsp?org=AKIMEKA&cws=1',

    'empcnt': [51,200]
}

class AkimekaJobScraper(TaleoJobScraper):
    def __init__(self):
        super(AkimekaJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[1].text)

def get_scraper():
    return AkimekaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
