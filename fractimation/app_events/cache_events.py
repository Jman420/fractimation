from events import Events

POPULATING_CACHE_START_EVENT = 'on_start_populating_cache'
POPULATING_CACHE_COMPLETE_EVENT = 'on_complete_populating_cache'

_KNOWN_EVENTS = [POPULATING_CACHE_START_EVENT, POPULATING_CACHE_COMPLETE_EVENT]

class CacheEvents(Events):

    def __init__(self):
        super().__init__(_KNOWN_EVENTS)

    def on_start_populating_cache(self, caption):
        event = self.__getattr__(POPULATING_CACHE_START_EVENT)
        event(caption)

    def on_complete_populating_cache(self):
        event = self.__getattr__(POPULATING_CACHE_COMPLETE_EVENT)
        event()
