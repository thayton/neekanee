#!/usr/bin/env python

import os
import re
import sys
import imp
import logging

class PluginLoader:
    """Class for loading job site scraping plugins. """

    def __init__(self):
        self.plugins = []

        self.logger = logging.getLogger('neekanee.PluginLoader')
        self.logger.setLevel(logging.DEBUG)

    def get_plugin_files(self, dir):
        """ 
        Recursively descend into a directory and
        return all plugin files found 
        """
        def is_notdir(f):
            return os.path.isdir(f) is False

        def is_plugin(f):
            return os.path.splitext(f)[1] == '.py'

        dirents = [ os.path.join(dir, f) for f in os.listdir(dir) ]

        ret = filter(is_notdir, dirents)
        ret = filter(is_plugin, ret)

        for d in filter(os.path.isdir, dirents):
            ret.extend(self.get_plugin_files(d))

        return ret

    def load_plugins(self, dirlist, exclude=[]):
        """
        Load plugins from files unless they are in 
        the exclude list
        """
        for dir in dirlist:
            files = self.get_plugin_files(dir)
            for f in files:
                plug = self.load_plugin(f)
                if self.plug_name(plug) not in exclude:
                    if getattr(plug, 'COMPANY', None) == None:
                        continue

                    if getattr(plug, 'skip', None) != None:
                        continue

                    self.plugins.append(plug)

    def load_plugin(self, path):
        modname = os.path.splitext(os.path.basename(path))[0]
        try:
            mod = imp.load_source(modname, path)
            return mod
        except ImportError, e:
            self.logger.error("load_plugin failed - error:", e)
    
    def get_plugin(self, site):
        """Return the plugin used for scraping jobs from the given site"""
        if site not in self.plugins:
            return None
        else:
            return self.plugins[site]

    def plug_name(self, plug):
        """
        Return the name of the plugin given its filename
        """
        tld = plug.COMPANY['home_page_url'].rsplit('.',1)[1]
        name = os.path.basename(os.path.splitext(plug.__name__)[0])
        return tld + '-' + name

if __name__ == '__main__':
    pldr = PluginLoader()
    pldr.load_plugins('../plugins/com/')

    plug = pldr.get_plugin('www.saintcorporation.com')
    print "plug.get_jobs %s" % plug.get_jobs
