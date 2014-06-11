"""
Import this into your settings file, eg --

from safelogging.settings import *

"""
from loglimit import LogLimitFilter
from allowed_hosts import suppress_allowed_hosts

# one email per XX seconds
LOGLIMIT_RATE = 10  

# uses keys to detect which errors are the same
LOGLIMIT_MAX_KEYS = 100  

# uses cache if it's available
LOGLIMIT_CACHE_PREFIX = 'LOGLIMIT'   

# here's one to use unless you've got your own
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            #'include_html': True,  # Its pretty verbose, doesn't fold/unfold
            'filters': ['loglimit', 'allowed_hosts'],
        },
    },
    'filters': {
        'loglimit': {
            '()': LogLimitFilter,
        },
        'allowed_hosts': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': suppress_allowed_hosts,
        },
    },
    'loggers': {
        'django.request':{
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}