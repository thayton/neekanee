#!/usr/bin/env python

"""
Wrapper around a plugin that handles opening a plugin, running the plugin, and then
saving the results to a file.
"""

import os
import re
import sys
import json
import logging
import random
import traceback

from plugin_loader import PluginLoader, FileFilter
from urlparse import urlparse
from datetime import date

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../../')))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.exceptions import ObjectDoesNotExist
from neekanee_solr.models import *

class PluginRunner(object):
    def __init__(self, plugin, results_dir='results', logfile='/var/log/neekanee/plugin_runner.log'):
        self.plugin = plugin
        self.results_dir = results_dir
        self.logger = logging.getLogger('neekanee')
        self.logger.setLevel(logging.DEBUG)

        fh = None
        for handler in self.logger.handlers:
            if isinstance(handler, logging.FileHandler):
                fh = handler

        if not fh:
            fh = logging.FileHandler(filename=logfile, mode='w')
            fh.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)

            self.logger.addHandler(fh)
        
    def __str__(self):
        return '%s' % self.plugin

    def run(self):
        self.run_plugin()
        self.save_jobs()

    def run_plugin(self):
        self.logger.info('running plugin %s' % self.plugin)

        job_scraper = self.plugin.get_scraper()
        job_scraper.reset_database_connection()

        try:
            job_scraper.scrape_jobs()
        except Exception, e:
            self.logger.warning('plugin %s generated exception: %s' % (self.plugin, e))
            self.logger.warning('%s' % traceback.format_exc())
            sys.stderr.write("Exception: %s\n" % e)
            sys.exc_clear()

        if job_scraper.company.job_set.count() == 0:
            self.logger.warning('plugin %s has 0 jobs' % self.plugin)

        job_scraper.company.last_scrape_time = date.today()
        job_scraper.company.save()

    def save_jobs(self):
        """
        Save job results for company c to disk. Filename will be the name
        of the plugin prefixed with the TLD. For example, for com/viasat.py
        the filename will be com-viasat.json.
        """
        try:
            company = Company.objects.get(home_page_url=self.plugin.COMPANY['home_page_url'])
        except ObjectDoesNotExist:
            return

        num_jobs = company.job_set.count()
#        if num_jobs == 0:
#            return

        file = self.make_plugin_filename()
        path = '%s/%s.json' % (self.results_dir, file)

        try:
            f = open(path, 'w')
            f.write(json.dumps(company.dict(), indent=4))
            f.close()
        except Exception, e:
            sys.stderr.write("Exception: %s\n" % e)
            sys.exc_clear()

        self.logger.info('Saved %d jobs for company %s to file %s' % (num_jobs, company.name, path))
        
    def make_plugin_filename(self):
        """
        Return the filename we'll use to store results for a given plugin.
        """
        # bu.py for bu.edu => edu-bu
        netloc = urlparse(self.plugin.COMPANY['home_page_url']).netloc
        tld = netloc.rsplit('.', 1)[1]

        filename = tld + '-' + self.plugin.__name__
        return filename

    def get_plugin_jobs_page_domain(self):
        netloc = urlparse(self.plugin.COMPANY['jobs_page_url']).netloc
        if isinstance(netloc, list):
            netloc = netloc[0]

        domain = '.'.join(netloc.split('.')[-2:])
        return domain

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('usage: %s <plugin>\n' % sys.argv[0])
        sys.exit(1)

    pldr = PluginLoader()
    plug = pldr.load_plugin(sys.argv[1])
    plugin_runner = PluginRunner(plugin=plug, results_dir='.')
    plugin_runner.run()
