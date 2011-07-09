import json

from flask import g

from log import L

from processor import Processor
from processors.cache_checker import hit_cache, clear_cache,\
    clear_cache_for_path

@Processor.processor
class CacheGetter(Processor):

    ARGS_FOR_KEY = [ 'lang', 'follow',
                     'query', 'order', 'start', 'limit', 'fields',
                     'count' ]
    
    def process(self):
        self.token.cache_key = json.dumps(self.token.path) + '|' + json.dumps(self.token.slug) + '|' + '|'.join([ self.token.request.args.get(arg,'') for arg in self.ARGS_FOR_KEY ])
        if self.token.request.method == "GET":
            data = hit_cache(self.token.cache_key)
            L.info("Data for key %s == %s" % (self.token.cache_key,repr(data)[:2048]))
            if data != None:
                self.token.response = json.loads(data)
                self.should_stop = True
                self.skip_to = "DataFormatter"
        else:
            clear_cache(self.token.cache_key)
            clear_cache_for_path(self.token.path)
