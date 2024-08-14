from .importer import MediaConfigurationImporter

class M1SessionImporter(MediaConfigurationImporter):
    '''
    '''

    def __init__(self):
        '''Constructor
        '''
        super().__init__()

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
        return self

    async def import_to(self, model: "MediaConfiguration") -> bool:
        '''Import the model into ``model``.
        '''
        return True
