from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Intuitive Surgical',
    'hq': 'Sunnyvale, CA',

    'home_page_url': 'http://www.intuitivesurgical.com',
    'jobs_page_url': 'https://intuitive.taleo.net/careersection/2/jobsearch.ftl?lang=en',

    'empcnt': [1001,5000]
}

class IntuitiveSurgicalJobScraper(TaleoJobScraper):
    def __init__(self):
        super(IntuitiveSurgicalJobScraper, self).__init__(COMPANY)

def get_scraper():
    return IntuitiveSurgicalJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
