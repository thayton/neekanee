from neekanee.jobscrapers.lever.lever import LeverJobScraper

COMPANY = {
    'name': 'Box',
    'hq': 'Los Altos, CA',

    'home_page_url': 'http://www.box.com',
    'jobs_page_url': 'https://jobs.lever.co/box',

    'empcnt': [501,1000]
}

def get_scraper():
    return LeverJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
