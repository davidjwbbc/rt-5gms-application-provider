# 5G-MAG Reference Tools: MediaAppDistribution class
#==============================================================================
#
# File: rt_media_configuration/media_distribution.py
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
5G-MAG Reference Tools: MediaAppDistribution Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaAppDistribution class which models a distribution
configuration for a MediaEntry.
'''

import json
from typing import Optional, List, Iterable

from .media_entry_point import MediaEntryPoint

class MediaAppDistribution:
    '''MediaAppDistribution class
==========================
This class models the app-only distribution configurations for a MediaEntry.
'''

    def __init__(self, name: str, entry_points: Iterable[MediaEntryPoint]):
        self.name = name
        self.entry_points = entry_points

    def __await__(self):
        return self.__asyncInit().__await__()

    async def __asyncInit(self):
        '''Asynchronous object instantiation
        :meta private:
        :return: self
        '''
        return self

    def __eq__(self, other: Optional["MediaAppDistribution"]) -> bool:
        if other is None:
            return False
        if self.__name != other.__name:
            return False
        return self.__entry_points == other.__entry_points

    def __ne__(self, other: "MediaAppDistribution") -> bool:
        return not (self == other)

    def __repr__(self) -> str:
        '''Python constructor string for this object'''
        return f'{self.__class__.__name__}({self.__name!r}, {self.__entry_points!r})'

    def __str__(self) -> str:
        return self.serialise(pretty=True)

    def serialise(self, pretty: bool = False) -> str:
        from .media_configuration import MediaConfiguration
        kwargs = {}
        if pretty:
            kwargs = {"sort_keys": True, "indent": 4}
        return json.dumps(self, default=MediaConfiguration.jsonObjectHandler, **kwargs)

    @staticmethod
    def deserialise(json_obj: str) -> "MediaAppDistribution":
        try:
            obj = json.loads(json_obj)
        except json.JSONDecodeError:
            raise ValueError("Bad JSON")
        return MediaAppDistribution.fromJSONObject(obj)

    @staticmethod
    def fromJSONObject(obj: dict) -> "MediaAppDistribution":
        name = None
        entry_points = None
        for k,v in obj.items():
            if k == "name":
                name = v
            elif k == "entryPoints":
                entry_points = [MediaEntryPoint.fromJSONObject(o) for o in v]
            else:
                raise ValueError(f'MediaAppDistribution: JSON field "{k}" not understood')
        return MediaAppDistribution(name, entry_points)

    def jsonObject(self) -> dict:
        return {'name': self.__name, 'entryPoints': self.__entry_points}

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value,str) or len(value) == 0:
            raise TypeError('MediaAppDistribution.name must be a non-empty string')
        self.__name = value

    @property
    def entry_points(self) -> List[MediaEntryPoint]:
        return self.__entry_points

    @entry_points.setter
    def entry_points(self, value: Iterable[MediaEntryPoint]):
        if not isinstance(value,list):
            value = list(value)
        if not all(isinstance(v,MediaEntryPoint) for v in value):
            raise TypeError('MediaAppDistribution.entry_points can only hold MediaEntryPoint objects')
        if len(value) == 0:
            raise ValueError('MediaAppDistribution.entry_points must contain at least one entry')
        self.__entry_points = value
