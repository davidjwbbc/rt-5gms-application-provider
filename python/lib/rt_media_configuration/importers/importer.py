import logging

class MediaConfigurationImporter:
    def __init__(self):
        self._log = logging.getLogger(__name__ + '.' + self.__class__.__name__)

    def __await__(self):
        '''``await`` provider for asynchronous instansiation.
        '''
        return self._asyncInit().__await__()

    async def _asyncInit(self):
        '''Asynchronous object instantiation

        :meta protected:
        :return: self
        '''
        return self

    async def import_to(self, model: "MediaConfiguration") -> bool:
        return true
