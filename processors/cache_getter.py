import json

from flask import g

from log import L

from processor import Processor
from processors.cache_checker import hit_cache

@Processor.processor
class CacheGetter(Processor):

    ARGS_FOR_KEY = [ 'lang', 'follow',
                     'query', 'order', 'start', 'limit', 'fields']
    
    def process(self):
        self.token.cache_key = json.dumps(self.token.path) + '|' + json.dumps(self.token.slug) + '|' + '|'.join([ self.token.request.args.get(arg,'') for arg in self.ARGS_FOR_KEY ])
        data = hit_cache(self.token.cache_key)
        L.info("Data for key %s == %r" % (self.token.cache_key,data))
        if data != None:
            self.token.response = json.loads(data)
            self.should_stop = True
            self.skip_to = "DataFormatter"