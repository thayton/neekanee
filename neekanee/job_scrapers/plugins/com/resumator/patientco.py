from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Patientco',
    'hq': 'Atlanta, GA',

    'home_page_url': 'http://www.patientco.com',
    'jobs_page_url': 'http://patientco.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
