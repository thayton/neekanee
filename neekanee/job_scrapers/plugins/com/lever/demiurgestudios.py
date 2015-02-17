from neekanee.jobscrapers.lever.lever import LeverJobScraper

COMPANY = {
    'name': 'Demiurge Studios',
    'hq': 'Cambridge, MA',

    'home_page_url': 'http://www.demiurgestudios.com',
    'jobs_page_url': 'https://jobs.lever.co/demiurgestudios',

    'empcnt': [11,50]
}

def get_scraper():
    return LeverJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
