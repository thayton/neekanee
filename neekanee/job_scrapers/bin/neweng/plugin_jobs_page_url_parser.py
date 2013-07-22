#!/usr/bin/env python

import sys
import ast

def get_plugin_jobs_page_url(plugin_file):
    with open(plugin_file) as f:
        tree = ast.parse(f.read())
        parser = PluginJobsPageUrlParser()
        parser.visit(tree)
        return parser.jobs_page_url
    
class PluginJobsPageUrlParser(ast.NodeVisitor):
    '''
    Get the jobs_page_url without actually executing the plugin. We do so because we 
    don't want to load anything Django related from the plugin. That should only happen
    once the plugin runs in its own separate process from all other plugins.
    '''
    def __init__(self):
        self.jobs_page_url = None

    def visit_Assign(self, stmt_assign):
        target = stmt_assign.targets[0]
        if getattr(target, 'id', None) == 'COMPANY':
            d = stmt_assign.value
            t = zip(d.keys, d.values)
            z = dict((x.s, y.s) for x,y in t if isinstance(x, ast.Str) and x.s == 'jobs_page_url')

            self.jobs_page_url = z.get('jobs_page_url', None)
            super(PluginJobsPageUrlParser, self).generic_visit(stmt_assign)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('usage: %s <file>\n' % sys.argv[0])
        sys.exit(1)

    with open(sys.argv[1]) as f:
        tree = ast.parse(f.read())
        parser = PluginJobsPageUrlParser()
        parser.visit(tree)
        print parser.jobs_page_url
