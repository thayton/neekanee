from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Red Bull USA',
    'hq': 'Fuschl am See, Austria',

    'home_page_url': 'http://www.redbullusa.com',
    'jobs_page_url': 'https://redbull.taleo.net/careersection/jobboard_us/jobsearch.ftl?lang=en',

    'empcnt': [5001,10000]
}

class RedBullUsaJobScraper(TaleoJobScraper):
    def __init__(self):
        super(RedBullUsaJobScraper, self).__init__(COMPANY)

def get_scraper():
    return RedBullUsaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
