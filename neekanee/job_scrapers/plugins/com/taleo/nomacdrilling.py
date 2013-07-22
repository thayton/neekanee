from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Nomac Drilling',
    'hq': 'El Reno, OK',

    'home_page_url': 'http://www.nomacdrilling.com',
    'jobs_page_url': 'http://chk.taleo.net/careersection/092/jobsearch.ftl?lang=en',

    'empcnt': [1001,5000]
}

class NomacDrillingJobScraper(TaleoJobScraper):
    def __init__(self):
        super(NomacDrillingJobScraper, self).__init__(COMPANY)

def get_scraper():
    return NomacDrillingJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
