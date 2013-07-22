from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Singularity University',
    'hq': 'Moffett Field, CA',

    'home_page_url': 'http://singularityu.org',
    'jobs_page_url': 'http://singularityuniversity.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
