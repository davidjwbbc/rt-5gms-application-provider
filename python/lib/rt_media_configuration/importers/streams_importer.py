import aiofiles

from typing import Optional

from .importer import MediaConfigurationImporter

class StreamsJSONImporter(MediaConfigurationImporter):
    '''
    '''

    def __init__(self, streamsfile: Optional[str] = None):
        '''Constructor
        '''
        super().__init__()
        self.__streamsfile = streamsfile or "/etc/rt-5gms/streams.json"
        self.__streams = None

    #Already provided by the interface:
    #def __await__(self):
    #    '''``await`` provider for asynchronous instansiation.
    #    '''
    #    return self._asyncInit().__await__()

    async def _asyncInit(self):
        '''Asynchronous object instantiation

        :meta private:
        :return: self
        '''
        super()._asyncInit()
        await self.__loadStreams()
        return self

    async def import_to(self, model: "MediaConfiguration") -> bool:
        '''Import the model into ``model``.
        '''
        return True

    async def __loadStreams(self):
        async with aiofiles.open(self.__streamsfile, "r") as streams_in:
            self.__streams = True
