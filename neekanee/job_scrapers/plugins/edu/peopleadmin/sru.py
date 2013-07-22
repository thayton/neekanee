from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Slippery Rock University',
    'hq': 'Slippery Rock, PA',

    'benefits': {
        'url': 'http://www.passhe.edu/inside/hr/OCHR/Benefits/Pages/default.aspx',
        'vacation': [],
        'holidays': 12,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.sru.edu',
    'jobs_page_url': 'https://careers.sru.edu',

    'empcnt': [201,500]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
