# This annoyance has apparently been a moving target, just to make it more fun
try:
    # Django 1.6
    from django.core.exceptions import SuspiciousOperation as AllowedHostException
except ImportError:
    try:
        # Django 1.5
        from django.core.exceptions import DisallowedHost as AllowedHostException
    except ImportError:
        # Django >1.6
        AllowedHostException = None

def suppress_allowed_hosts(record):
    if AllowedHostException:
        if record.exc_info:
            exc_value = record.exc_info[1]
            if isinstance(exc_value, AllowedHostException):
              return False
    return True
