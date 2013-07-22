import os
import time
import random

from datetime import datetime

class JobScraper(object):
    def __init__(self, site=None, domain=None):
        self.site = site
        self.domain = domain
        self.run_time = random.randrange(1,20)
        self.start_time = None
        self.end_time = None

    def __str__(self):
        return '%s @%s [ run_time: %d sec ]' % (self.site, self.domain, self.run_time)

    def run(self):
        self.start_time = datetime.now()
        print '* %02d:%02d:%02d (pid %d) Starting job scraper %s' % \
            (self.start_time.hour, self.start_time.minute, self.start_time.second, os.getpid(), self)

        time.sleep(self.run_time)

        self.end_time = datetime.now()
        print '* %02d:%02d:%02d (pid %d) Finished job scraper %s' % \
            (self.end_time.hour, self.end_time.minute, self.end_time.second, os.getpid(), self)
