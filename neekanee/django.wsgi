import os
import sys

sys.stdout = sys.stderr

sys.path.append('/srv/www/neekanee.com/')
sys.path.append('/srv/www/neekanee.com/neekanee/')
sys.path.append('/srv/www/neekanee.com/neekanee/neekanee/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
