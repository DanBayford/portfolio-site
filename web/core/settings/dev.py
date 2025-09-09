import os
from .base import *

DEBUG = bool(int(os.environ.get("DEBUG", default=1)))

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", "localhost 127.0.0.1 [::1]"
).split(" ")

INSTALLED_APPS.insert(6, "django_browser_reload")
INSTALLED_APPS.insert(7, "debug_toolbar")

MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")
MIDDLEWARE.insert(-1, "django_browser_reload.middleware.BrowserReloadMiddleware")

# Required by debug-toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]