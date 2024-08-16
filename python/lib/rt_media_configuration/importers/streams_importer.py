#!/usr/bin/python3
#==============================================================================
# 5G-MAG Reference Tools: Streams.json MediaConfiguration importer
#==============================================================================
#
# File: rt_media_configuration/importers/streams_importer.py
# License: 5G-MAG Public License (v1.0)
# Author: David Waring
# Copyright: (C) 2023 British Broadcasting Corporation
#
# For full license terms please see the LICENSE file distributed with this
# program. If this file is missing then the license can be retrieved from
# https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
#
#==============================================================================
import json
import logging
import traceback
from typing import Optional

import aiofiles

from .importer import MediaConfigurationImporter
from ..media_entry import MediaEntry
from ..media_app_distribution import MediaAppDistribution
from ..media_distribution import MediaDistribution

class StreamsJSONImporter(MediaConfigurationImporter):
    '''StreamsJSONImporter class
=========================
Reads in a `streams.json` JSON file and uses the contents to replace the model
in the MediaConfiguration.
    '''

    def __init__(self, streamsfile: Optional[str] = None):
        '''Constructor
        '''
        super().__init__()
        self.__streamsfile = streamsfile or "/etc/rt-5gms/streams.json"
        self.__streams = None
        self.__log = logging.getLogger(__name__ + '.' + self.__class__.__name__)

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
        await super()._asyncInit()
        await self.__load_streams()
        return self

    async def import_to(self, model: "MediaConfiguration") -> bool:
        '''Import the model into ``model``.
        '''
        try:
            await model.reset()
            model.asp_id = self.__streams["aspId"]
            model.app_id = self.__streams["appId"]
            for stream_id,stream_config in self.__streams["streams"].items():
                await model.addMediaEntry(stream_id, MediaEntry.fromJSONObject(stream_config))
            for vod_media in self.__streams["vodMedia"]:
                distrib_obj = vod_media.copy()
                del distrib_obj['stream']
                print(distrib_obj)
                print('-------------------')
                distrib = MediaAppDistribution.fromJSONObject(distrib_obj)
                print(distrib)
                print('===================')
                entry = await model.mediaEntryById(vod_media['stream'])
                entry.addAppDistribution(distrib)
        except Exception:
            self.__log.error(traceback.format_exc())
            return False
        return True

    async def __load_streams(self):
        async with aiofiles.open(self.__streamsfile, mode='r') as streams_in:
            streams_json_str = await streams_in.read()
        self.__streams = json.loads(streams_json_str)
