from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Molson Coors',
    'hq': 'Denver, CO',

    'home_page_url': 'http://www.molsoncoors.com',
    'jobs_page_url': 'https://ca-extenglish-molsoncoors.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [1001,5000]
}

class MolsonCoorsJobScraper(IcimsJobScraper):
    def __init__(self):
        super(MolsonCoorsJobScraper, self).__init__(COMPANY)

def get_scraper():
    return MolsonCoorsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
