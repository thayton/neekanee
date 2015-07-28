from neekanee.jobscrapers.lever.lever import LeverJobScraper

COMPANY = {
    'name': 'DuoLingo',
    'hq': 'Pittsburgh, PA',

    'home_page_url': 'http://www.duolingo.com',
    'jobs_page_url': 'https://jobs.lever.co/duolingo/',

    'empcnt': [1,10]
}

def get_scraper():
    return LeverJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()

