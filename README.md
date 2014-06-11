django-safelogging
==================

Sensible default error email settings for Django. Suppresses annoying ALLOWED_HOSTS errors and rate limits error emails for busy sites.

Simply import into your settings file, and you're away. Example --

	from safelogging.settings import *

Check settings.py for rate limit settings.