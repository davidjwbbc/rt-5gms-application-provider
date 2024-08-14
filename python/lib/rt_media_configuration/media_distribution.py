# 5G-MAG Reference Tools: MediaDistribution class
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
5G-MAG Reference Tools: MediaDistribution Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaDistribution class which models a distribution
configuration for a MediaEntry.
'''

import json
from typing import Optional, List

from .media_entry_point import MediaEntryPoint

class MediaDistribution:
    '''MediaDistribution class
=======================
This class models the distribution configurations for a MediaEntry.
'''

    def __init__(self, domain_name_alias: Optional[str] = None, certificate_id: Optional[str] = None, entry_point: Optional[MediaEntryPoint] = None):
        self.domain_name_alias = domain_name_alias
        self.certificate_id = certificate_id
        self.entry_point = entry_point

    def __await__(self):
        return self.__asyncInit().__await__()

    async def __asyncInit(self):
        '''Asynchronous object instantiation
        :meta private:
        :return: self
        '''
        return self

    def __eq__(self, other: Optional["MediaDistribution"]) -> bool:
        if other is None:
            return False
        if self.__domain_name_alias != other.__domain_name_alias:
            return False
        if self.__certificate_id != other.__certificate_id:
            return False
        return self.__entry_point == other.__entry_point

    def __ne__(self, other: "MediaDistribution") -> bool:
        return not (self == other)

    def __repr__(self) -> str:
        '''Python constructor string for this object'''
        ret = f'{self.__class__.__name__}('
        np = ""
        if self.__domain_name_alias is not None:
            ret += f'domain_name_alias={self.__domain_name_alias!r}'
            np = ", "
        if self.__certificate_id is not None:
            ret += f'{np}certificate_id={self.__certificate_id!r}'
            np = ", "
        if self.__entry_point is not None:
            ret += f'{np}entry_point={self.__entry_point!r}'
        ret += ')'
        return ret

    def __str__(self) -> str:
        return self.serialise(pretty=True)

    def serialise(self, pretty: bool = False) -> str:
        from .media_configuration import MediaConfiguration
        kwargs = {}
        if pretty:
            kwargs = {"sort_keys": True, "indent": 4}
        return json.dumps(self, default=MediaConfiguration.jsonObjectHandler, **kwargs)

    @staticmethod
    def deserialise(json_obj: str) -> "MediaDistribution":
        try:
            obj = json.loads(json_obj)
        except json.JSONDecodeError:
            raise ValueError("Bad JSON")
        return MediaDistribution._fromJSONObject(obj)

    @staticmethod
    def _fromJSONObject(obj: dict) -> "MediaDistribution":
        kwargs = {}
        if "domainNameAlias" in  obj:
            kwargs["domain_name_alias"] = obj["domainNameAlias"]
        if "certificateId" in obj:
            kwargs["certificate_id"] = obj["certificateId"]
        if "entryPoint" in obj:
            kwargs["entry_point"] = MediaEntryPoint._fromJSONObject(obj['entryPoint'])
        return MediaDistribution(**kwargs)

    def _jsonObject(self) -> dict:
        obj = {}
        if self.__domain_name_alias is not None:
            obj['domainNameAlias'] = self.__domain_name_alias
        if self.__certificate_id is not None:
            obj['certificateId'] = self.__certificate_id
        if self.__entry_point is not None:
            obj['entryPoint'] = self.__entry_point
        return obj

    @property
    def domain_name_alias(self) -> Optional[str]:
        return self.__domain_name_alias

    @domain_name_alias.setter
    def domain_name_alias(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value,str):
                raise TypeError('MediaDistribution.domain_name_alias can be either None or a str')
        self.__domain_name_alias = value

    @property
    def certificate_id(self) -> Optional[str]:
        return self.__certificate_id

    @certificate_id.setter
    def certificate_id(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value,str):
                raise TypeError('MediaDistribution.certificate_id can be either None or a str')
        self.__certificate_id = value
    
    @property
    def entry_point(self) -> Optional[MediaEntryPoint]:
        return self.__entry_point

    @entry_point.setter
    def entry_point(self, value: Optional[MediaEntryPoint]):
        if value is not None:
            if not isinstance(value,MediaEntryPoint):
                raise TypeError('MediaDistribution.entry_point can be either None or a MediaEntryPoint')
        self.__entry_point = value
