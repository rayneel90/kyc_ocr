"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

python_home = '/data/nilabja21607/kyc_ocr/webapp/venv'

import sys
import site
print(sys.executable)
# Calculate path to site-packages directory.

python_version = '.'.join(map(str, sys.version_info[:2]))
site_packages = python_home + '/lib/python%s/site-packages' % python_version
# Add the site-packages directory.
site.addsitedir(site_packages)


import os
from config.settings import BASE_DIR
sys.path.append(os.path.join(BASE_DIR, 'venv'))
print(sys.path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
