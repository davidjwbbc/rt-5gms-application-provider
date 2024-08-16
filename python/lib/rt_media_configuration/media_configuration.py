#!/usr/bin/python3 
#==============================================================================
# 5G-MAG Reference Tools: MediaConfiguration class
#==============================================================================
#
# File: rt_media_configuration/media_configuration.py
# License: 5G-MAG Public License (v1.0)
# Author: David Waring <david.waring2@bbc.co.uk>
# Copyright: (C) 2024 British Broadcasting Corporation
#
# For full license terms please see the LICENSE file distributed with this
# program. If this file is missing then the license can be retrieved from
# https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
#
#==============================================================================
'''
=====================================================
5G-MAG Reference Tools: MediaConfiguration Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaConfiguration class which models a collection
of media assets and provides methods to manipulate the model and use the
rt_m1_client.M1Session object to synchronise that configuration with the
5GMS AF.
'''
import configparser
import json
import logging
from typing import Optional, Iterable, Dict

import aiofiles

from rt_m1_client.configuration import Configuration
from rt_m1_client.session import M1Session
from rt_m1_client.data_store import DataStore

from .media_entry import MediaEntry

DEFAULT_CONFIG = '''[media-configuration]
m5_authority = example.com:7777
docroot = /var/cache/rt-5gms/as/docroots
default_docroot = /usr/share/nginx/html
'''

class MediaConfiguration:
    '''MediaConfiguration Class
========================
This class provides modelling for a collection of media assets and the
logic to use the rt_m1_client.M1Session object to synchronise that
configuration with the 5GMS AF.
'''

    def __init__(self, configfile: Optional[str] = None, persistent_data_store: Optional[DataStore] = None):
        self.__outputs = []
        self.__model = {"media": {}}
        self.__extraConfigFile = configfile
        self.__config = Configuration()
        self.__config.addSection('media-configuration', DEFAULT_CONFIG, self.__extraConfigFile)
        self.__data_store_dir = persistent_data_store
        self.__log = logging.getLogger(__name__ + '.' + self.__class__.__name__)
        self.__m1_session = None

    def __await__(self):
        '''``await`` provider for asynchronous instantiation.
        '''
        return self.__asyncInit().__await__()

    def __repr__(self) -> str:
        return f'{__name__}.{self.__class__.__name__}({self.__extraConfigFile!r}, persistent_data_store={self.__data_store_dir!r})'

    def __str__(self) -> str:
        return json.dumps(self.__model["media"], default=MediaConfiguration.jsonObjectHandler, sort_keys=True, indent=2)

    async def reset(self) -> None:
        self.__model = {"media": {}}

    async def restoreModel(self) -> bool:
        '''Restore the model to the last known configuration.

        Loads the current configuration from the 5GMS AF and supplements it
        with model configuration stored in the Datastore.

        :return: ``True`` if the model was successfully restored.
        '''
        try:
            m1_imp = await M1SessionImporter()
            m1_imp.import_to(self)
            await self.__loadModelFromDatastore()
        except Exception as exc:
            self.__log.error(f"Failed to restore model: {exc}")
            return False
        return True

    async def newMediaEntry(self, stream_id: str, *args, **kwargs) -> MediaEntry:
        '''Create a new MediaEntry and attach it to this MediaConfiguration

        :see: MediaEntry constructor for parameters.
        :return: A new MediaEntry object attached to this MediaConfiguration.
        '''
        entry = await MediaEntry(*args, **kwargs)
        entry.id = stream_id
        self.__model["media"][stream_id] = entry
        return entry
        
    async def addMediaEntry(self, stream_id: str, entry: MediaEntry) -> bool:
        entry.id = stream_id
        self.__model["media"][stream_id] = entry
        return True

    async def removeMediaEntry(self, *, stream_id: Optional[str] = None, entry: Optional[MediaEntry] = None) -> bool:
        if stream_id is None and entry is None:
            return False
        if stream_id is not None:
            if entry is not None:
                raise RuntimeError('MediaConfiguration.removeMediaEntry takes either stream_id or entry, not both')
            if stream_id not in self.__model["media"]:
                return False
            del self.__model["media"][stream_id]
            return True
        else:
            for k,v in self.__model["media"]:
                if v == entry:
                    del self.__model["media"][k]
                    return True
        return False

    async def mediaEntries(self) -> Iterable[MediaEntry]:
        return self.__model["media"].values()

    async def mediaEntryById(self, stream_id: str) -> Optional[MediaEntry]:
        return self.__model["media"].get(stream_id, None)

    async def synchronise(self):
        '''Synchronise MediaConfiguration

        This will update the 5GMS AF configuration and M8 published objects to match this media configuration. This will determine
        the differences between this configuration and what is present on the 5GMS AF and apply the deltas to the 5GMS AF in order
        to synchronise it with this configuration. The parts of the configuration not representable in the 5GMS AF will be written
        out the DataStore (as configured in the constructor). The M8 outputs will be triggered to republish any M8 objects.
        '''
        if self.__m1_session is None:
            self.__m1_session = await M1Session(host_address=(self.__config.get('m1_address'),self.__config.get('m1_port')),
                                                persistent_data_store=self.__data_store_dir,
                                                certificate_signer=self.__config.get('certificate_signing_class'))
        raise Exception("not implemenetd yet")
    
    async def __asyncInit(self):
        '''Asynchronous object instantiation

        Loads previous state from the DataStore.

        :meta private:
        :return: self
        '''
        return self

    @staticmethod
    def jsonObjectHandler(obj):
        fn = getattr(obj, "jsonObject", None)
        if fn is not None:
            return fn()
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serialisable')

# vim:ts=8:sts=4:sw=4:expandtab:
