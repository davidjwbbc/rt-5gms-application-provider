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

import json
from typing import Optional

from .importers import MediaConfigurationImporter
from .exceptions import MediaConfigurationError
from .media_entry import MediaEntry
from rt_m1_client.session import M1Session
from rt_m1_client.data_store import DataStore

__DEFAULT_CONFIG = {
    "host-rules": []
}

class MediaConfiguration:
    '''MediaConfiguration Class
========================
This class provides modelling for a collection of media assets and the
logic to use the rt_m1_client.M1Session object to synchronise that
configuration with the 5GMS AF.
'''

    def __init__(self, configfile: Optional[str] = None, persistent_data_store: Optional[DataStore] = None):
        self.__outputs = []
        self.__model = {"media": []}
        self.__configFile = configfile
        self.__config = None
        self.__data_store_dir = persistent_data_store
        self.__log = logging.getLogger(__name__ + '.' + self.__class__.__name__)

    def __await__(self):
        '''``await`` provider for asynchronous instantiation.
        '''
        return self.__asyncInit().__await__()

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
            return false
        return true

    async def newMediaEntry(self, *args, **kwargs) -> MediaEntry:
        '''Create a new MediaEntry and attach it to this MediaConfiguration

        :see: MediaEntry constructor for parameters.
        :return: A new MediaEntry object attached to this MediaConfiguration.
        '''
        entry = await MediaEntry(*args, **kwargs)
        self.__model["media"].append(entry)
        return entry
        
    async def addMediaEntry(self, entry: MediaEntry) -> bool:
        self.__model["media"].append(entry)
        return true

    async def removeMediaEntry(self, entry: MediaEntry) -> bool:
        try:
            self.__model["media"].remove(entry)
        except ValueError:
            return false
        return true

    async def mediaEntries(self):
        return self.__model["media"]

    async def synchronise(self):
        '''Synchronise MediaConfiguration

        This will update the 5GMS AF configuration and M8 published objects to match this media configuration. This will determine
        the differences between this configuration and what is present on the 5GMS AF and apply the deltas to the 5GMS AF in order
        to synchronise it with this configuration. The parts of the configuration not representable in the 5GMS AF will be written
        out the DataStore (as configured in the constructor). The M8 outputs will be triggered to republish any M8 objects.
        '''
        raise Exception("not implemenetd yet")
    
    async def __asyncInit(self):
        '''Asynchronous object instantiation

        Loads previous state from the DataStore.

        :meta private:
        :return: self
        '''
        await self.__loadConfiguration()
        return self

    async def __loadConfiguration(self) -> None:
        '''Reload the configuration

        :meta private:
        :return ``None``
        '''
        if self.configfile is None:
            global __DEFAULT_CONFIG
            self.config = __DEFAULT_CONFIG
            return
        return

    @staticmethod
    def jsonObjectHandler(obj):
        fn = getattr(obj, "_jsonObject", None)
        if fn is not None:
            return fn()
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serialisable')

# vim:ts=8:sts=4:sw=4:expandtab:
