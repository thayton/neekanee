from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'FT Services',
    'hq': 'Calgary, Canada',

    'home_page_url': 'http://www.ft-serv.com',
    'jobs_page_url': 'http://transfieldservices.taleo.net/careersection/fts_external_cs/jobsearch.ftl?lang=en',

    'empcnt': [1001,5000]
}

class FtServJobScraper(TaleoJobScraper):
    def __init__(self):
        super(FtServJobScraper, self).__init__(COMPANY)

def get_scraper():
    return FtServJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
