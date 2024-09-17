# 5G-MAG Reference Tools: MediaGeoFencing class
#==============================================================================
#
# File: rt_media_configuration/media_geo_fencing.py
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
5G-MAG Reference Tools: MediaGeoFencing Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaGeoFencing class which models a single media
entry point for a MediaDistribution.
'''

import json
from typing import Optional, List, Iterable, Final, Any, Type, TypedDict

from rt_m1_client.types import GeoFencing

class MediaGeoFencing:
    '''MediaGeoFencing class
=====================

This models a geo fencing entry for a MediaDistribution.
'''

    def __init__(self, locator_type: str, locators: List[str]):
        self.locator_type = locator_type
        self.locators = locators

    def __await__(self):
        return self.__asyncInit().__await__()

    async def __asyncInit(self):
        '''Asynchronous object instantiation
        :meta private:
        :return: self
        '''
        return self

    def __eq__(self, other: "MediaGeoFencing") -> bool:
        if self.__locator_type != other.locator_type:
            return False
        return sorted(self.__locators) == sorted(other.locators)

    def __ne__(self, other: "MediaGeoFencing") -> bool:
        return not self == other

    def __lt__(self, other: "MediaGeoFencing") -> bool:
        if self.__locator_type != other.locator_type:
            return self.__locator_type < other.locator_type
        if len(self.__locators) != len(other.locators):
            return len(self.__locators) < len(other.locators)
        return sorted(self.__locators) < sorted(other.locators)

    def __le__(self, other: "MediaGeoFencing") -> bool:
        if self.__locator_type != other.locator_type:
            return self.__locator_type < other.locator_type
        if len(self.__locators) != len(other.locators):
            return len(self.__locators) < len(other.locators)
        return sorted(self.__locators) <= sorted(other.locators)

    def __ge__(self, other: "MediaGeoFencing") -> bool:
        return not self < other

    def __gt__(self, other: "MediaGeoFencing") -> bool:
        return not self <= other

    def __repr__(self) -> str:
        '''Python constructor string for this object'''
        return f'{self.__class__.__name__}({self.__locator_type!r}, {self.__locators!r})'
        
    def __str__(self) -> str:
        return self.serialise(pretty=True)

    def serialise(self, pretty: bool = False) -> str:
        from .media_configuration import MediaConfiguration
        kwargs = {}
        if pretty:
            kwargs = {"sort_keys": True, "indent": 4}
        return json.dumps(self, default=MediaConfiguration.jsonObjectHandler, **kwargs)

    @staticmethod
    def deserialise(json_obj: str) -> "MediaGeoFencing":
        try:
            obj = json.loads(json_obj)
        except json.JSONDecodeError:
            raise ValueError("Bad JSON")
        return MediaGeoFencing.fromJSONObject(obj)

    @staticmethod
    def fromJSONObject(obj: dict) -> "MediaGeoFencing":
        mand_fields = ['locatorType','locators']
        loc_type = None
        locs = None
        for k,v in obj.items():
            if k == 'locatorType':
                loc_type = v
                mand_fields.remove(k)
            elif k == 'locators':
                locs = v
                mand_fields.remove(k)
            else:
                raise TypeError(f'MediaGeoFencing: JSON field "{k}" not understood')
        if len(mand_fields) > 0:
            raise TypeError(f'MediaGeoFencing: Mandatory JSON fields {mand_fields!r} are missing')
        return MediaGeoFencing(loc_type, locs)

    def jsonObject(self) -> dict:
        return {'locatorType': self.__locator_type, 'locators': self.__locators}

    @property
    def locator_type(self) -> str:
        return self.__locator_type

    @locator_type.setter
    def locator_type(self, value: str):
        if not isinstance(value,str) or len(value) == 0:
            raise TypeError('MediaGeoFencing.locator_type must be a non-empty str')
        self.__locator_type = value

    @property
    def locators(self) -> List[str]:
        return self.__locators

    @locators.setter
    def locators(self, value: Iterable[str]):
        if not isinstance(value, list):
            value = list(value)
        if len(value) == 0 or not all(isinstance(v,str) for v in value):
            raise TypeError('MediaGeoFencing.locators must be a non-empty list of str')
        self.__locators = value

    def addLocator(self, value: str):
        if not isinstance(value,str):
            raise TypeError('MediaGeoFencing.locators is a list of str')
        self.__locators += [value]

    def removeLocator(self, value: str) -> bool:
        try:
            self.__locators.remove(value)
        except ValueError:
            return False
        if len(self.__locators) == 0:
            raise TypeError('MediaGeoFencing.locators must be a non-empty list of str')
        return True

    __conv_3gpp: Final[List[TypedDict('3GPPConversion', {'param': str, 'field': str, 'cls': Type, 'mandatory': bool})]] = [
        {'param': 'locator_type', 'field': 'locatorType', 'cls': str, 'mandatory': True},
        {'param': 'locators', 'field': 'locators', 'cls': List[str], 'mandatory': True}
    ]

    @classmethod
    async def from3GPPObject(cls, gf: GeoFencing) -> "MediaGeoFencing":
        args = []
        kwargs = {}
        for cnv in cls.__conv_3gpp:
            if cnv['mandatory']:
                args += [await cls.doConversion(gf[cnv['field']],cnv['cls'],'from3GPPObject')]
            elif cnv['field'] in gf:
                kwargs[cnv['param']] = await cls.doConversion(gf[cnv['field']],cnv['cls'],'from3GPPObject')
        return await cls(*args, **kwargs)

    async def to3GPPObject(self, session: "MediaSession") -> GeoFencing:
        from .media_session import MediaSession
        ret = {}
        for cnv in self.__conv_3gpp:
            v = getattr(self, cnv['param'], None)
            if v is not None:
                ret[cnv['field']] = await self.doConversion(v, cnv['cls'], 'to3GPPObject', session)
        return GeoFencing(ret)

    @classmethod
    async def doConversion(cls, value: Any, typ: Type, convfn, session: Optional["MediaSession"] = None) -> Any:
        from .media_session import MediaSession
        if value is None:
            return None
        if getattr(typ, '__origin__', None) is list:
            return [await cls.doConversion(v, typ.__args__[0], convfn, session=session) for v in value]
        fn = getattr(typ, convfn, None)
        if fn is not None:
            if session is not None:
                return await fn(value, session=session)
            else:
                return await fn(value)
        return typ(value)

