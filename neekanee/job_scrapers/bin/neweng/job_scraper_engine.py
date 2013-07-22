#!/usr/bin/env python

"""
Proof of concept for running multiple job scraping plugins at the same
time using the new TaskManager code.
"""

import urlparse
import logging
import random

from plugin_runner import PluginRunner
from task_manager import TaskManager
from plugin_loader import PluginLoader

class JobScraperEngine(TaskManager):
    def __init__(self, plugin_dir, results_dir, logfile='/var/log/neekanee/job_scraper_engine.log'):
        self.domains_being_scraped = []
        self.plugin_dir = plugin_dir
        self.results_dir = results_dir
        self.logfile = logfile
        self.plugins = []
        self.pldr = PluginLoader()

        self.logger = logging.getLogger('neekanee')
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(filename=logfile, mode='w')
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        self.logger.addHandler(fh)

        super(JobScraperEngine, self).__init__()

    def load_plugins(self):
        self.pldr.load_plugins([self.plugin_dir])
        random.shuffle(self.pldr.plugins)

        tasks = [PluginRunner(plugin=p, results_dir=self.results_dir, logfile=self.logfile) for p in self.pldr.plugins]
        self.set_task_list(tasks=tasks)

        self.logger.info('loaded %d plugins' % len(self.pldr.plugins))

    def get_next_task(self, tasks):
        for plugin_runner in tasks:
            if plugin_runner.get_plugin_jobs_page_domain() not in self.domains_being_scraped:
                return plugin_runner

        return None

    def task_launched(self, task, pid):
        self.logger.info('Task %d for plugin %s launched' % (int(pid), task.plugin))
        domain = task.get_plugin_jobs_page_domain()
        if domain not in self.domains_being_scraped:
            self.domains_being_scraped.append(domain)

    def task_completed(self, task, pid):
        self.logger.info('Task %d for plugin %s completed' % (int(pid), task.plugin))
        domain = task.get_plugin_jobs_page_domain()
        self.domains_being_scraped.remove(domain)

if __name__ == '__main__':
    engine = JobScraperEngine(plugin_dir='plugins/', results_dir='results/')
    engine.load_plugins()
    engine.run()

