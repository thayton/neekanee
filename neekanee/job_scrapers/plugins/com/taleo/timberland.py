from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Timberland',
    'hq': 'Stratham, NH',

    'home_page_url': 'http://www.timberland.com',
    'jobs_page_url': 'https://vfc.taleo.net/careersection/timberland+external/jobsearch.ftl?lang=en',

    'empcnt': [1001,5000]
}

class TimberlandNetJobScraper(TaleoJobScraper):
    def __init__(self):
        super(TimberlandNetJobScraper, self).__init__(COMPANY)

def get_scraper():
    return TimberlandNetJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
