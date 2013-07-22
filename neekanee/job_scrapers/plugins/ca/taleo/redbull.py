from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Red Bull Canada',
    'hq': 'Fuschl am See, Austria',

    'home_page_url': 'http://www.redbull.ca',
    'jobs_page_url': 'https://redbull.taleo.net/careersection/jobboard_ca/jobsearch.ftl?lang=en',

    'empcnt': [5001,10000]
}

class RedBullCaJobScraper(TaleoJobScraper):
    def __init__(self):
        super(RedBullCaJobScraper, self).__init__(COMPANY)

def get_scraper():
    return RedBullCaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
