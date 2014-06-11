import traceback
try:
    from hashlib import md5
except ImportError:
    from md5 import md5
from datetime import datetime, timedelta


class LogLimitFilter(object):
    
    _errors = {}
        
    def filter(self, record):
        
        if not hasattr(self, 'rate'):
            # Need to wait until run time to read settings
            from django.conf import settings
            self.rate = getattr(settings, 'LOGLIMIT_RATE', 10) # seconds
            self.max_keys = getattr(settings, 'LOGLIMIT_MAX_KEYS', 100)
            self.cache_prefix = getattr(settings, 'LOGLIMIT_CACHE_PREFIX', 'LOGLIMIT')
        
        tb = '\n'.join(traceback.format_exception(*record.exc_info))

        # Track duplicate errors
        duplicate = False
        rate = self.rate  
        if rate > 0:
            key = md5(tb).hexdigest()
            prefix = self.cache_prefix
            
            # Test if the cache works
            cache_key = '%s_%s' % (prefix, key)
            try:
                from django.core.cache import cache                               
                cache.set(prefix, 1, 1)
                use_cache = cache.get(prefix) == 1
            except:
                use_cache = False
            
            if use_cache:
                duplicate = cache.get(cache_key) == 1
                cache.set(cache_key, 1, rate)
            else:
                min_date = datetime.now() - timedelta(seconds=rate)
                max_keys = self.max_keys
                duplicate = (key in self._errors and self._errors[key] >= min_date)
                self._errors = dict(filter(lambda x: x[1] >= min_date, 
                                          sorted(self._errors.items(), 
                                                 key=lambda x: x[1]))[0-max_keys:])
                if not duplicate:
                    self._errors[key] = datetime.now()

        return not duplicate

