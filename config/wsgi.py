import os
import sys
import traceback

import django
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.conf import settings
from django.db import connection

print("DB PATH:", settings.DATABASES["default"]["NAME"], flush=True)

try:
    call_command("collectstatic", interactive=False, verbosity=0)
    call_command("migrate", interactive=False, verbosity=1, stdout=sys.stdout)
    tables = connection.introspection.table_names()
    print("TABLES:", sorted(tables), flush=True)
except Exception:
    traceback.print_exc()
    sys.stderr.flush()

application = get_wsgi_application()