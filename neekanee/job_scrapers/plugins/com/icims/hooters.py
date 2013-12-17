from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Hooters of America',
    'hq': 'Atlanta, GA',

    'ats': 'Icims',

    'home_page_url': 'http://www.hooters.com',
    'jobs_page_url': 'https://careershub-hooters.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [51,200]
}

def get_scraper():
    return IcimsJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
