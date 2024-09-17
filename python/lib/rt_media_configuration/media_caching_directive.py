# 5G-MAG Reference Tools: MediaCachingDirective class
#==============================================================================
#
# File: rt_media_configuration/media_caching_directive.py
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
5G-MAG Reference Tools: MediaCachingDirective Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaCachingDirective class which models the caching
directives for a MediaCachingConfiguration.
'''

import json
from typing import Optional, List, Iterable, Final, Any, Type, TypedDict

from rt_m1_client.types import CachingDirective

class MediaCachingDirective:
    '''MediaCachingDirective class
===========================

This models a caching directive which forms part of a MediaCachingConfiguration.
'''

    def __init__(self, no_cache: bool, status_code_filters: Optional[Iterable[int]] = None, max_age: Optional[int] = None):
        self.no_cache = no_cache
        self.status_code_filters = status_code_filters
        self.max_age = max_age

    def __await__(self):
        return self.__asyncInit().__await__()

    async def __asyncInit(self):
        '''Asynchronous object instantiation
        :meta private:
        :return: self
        '''
        return self

    def __eq__(self, other: "MediaCachingDirective") -> bool:
        if self.__no_cache != other.no_cache:
            return False
        if self.__status_code_filters is None:
            if other.status_code_filters is not None:
                return False
        else:
            if other.status_code_filters is None:
                return False
            else:
                if len(self.__status_code_filters) != len(other.status_code_filters):
                    return False
                if sorted(self.__status_code_filters) != sorted(other.status_code_filters):
                    return False
        return ((self.__max_age is None and other.max_age is None) or
                (self.__max_age is not None and other.max_age is not None and self.__max_age != other.max_age)
               )

    def __ne__(self, other: "MediaCachingDirective") -> bool:
        return not self == other

    def __lt__(self, other: "MediaCachingDirective") -> bool:
        if self.__no_cache != other.no_cache:
            return other.no_cache
        if self.__max_age is not None:
            if other.max_age is None:
                return False
            if self.__max_age != other.max_age:
                return self.__max_age < other.max_age
        elif other.max_age is not None:
            return True
        if self.__status_code_filters is not None:
            if other.status_code_filters is None:
                return False
            if len(self.__status_code_filters) != len(other.status_code_filters):
                return len(self.__status_code_filters) < len(other.status_code_filters)
            return sorted(self.__status_code_filters) < sorted(other.status_code_filters)
        elif other.status_code_filters is not None:
            return True
        return False

    def __le__(self, other: "MediaCachingDirective") -> bool:
        if self.__no_cache != other.no_cache:
            return other.no_cache
        if self.__max_age is not None:
            if other.max_age is None:
                return False
            if self.__max_age != other.max_age:
                return self.__max_age < other.max_age
        elif other.max_age is not None:
            return True
        if self.__status_code_filters is not None:
            if other.status_code_filters is None:
                return False
            if len(self.__status_code_filters) != len(other.status_code_filters):
                return len(self.__status_code_filters) < len(other.status_code_filters)
            return sorted(self.__status_code_filters) < sorted(other.status_code_filters)
        elif other.status_code_filters is not None:
            return True
        return True

    def __ge__(self, other: "MediaCachingDirective") -> bool:
        return not self < other

    def __gt__(self, other: "MediaCachingDirective") -> bool:
        return not self <= other

    def __repr__(self) -> str:
        '''Python constructor string for this object'''
        ret = f'{self.__class__.__name__}({self.__no_cache!r}'
        if self.__status_code_filters is not None:
            ret += f', status_code_filters={self.__status_code_filters!r}'
        if self.__max_age is not None:
            ret += f', max_age={self.__max_age!r}'
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
    def deserialise(json_obj: str) -> "MediaCachingDirective":
        try:
            obj = json.loads(json_obj)
        except json.JSONDecodeError:
            raise ValueError("Bad JSON")
        return MediaCachingDirective.fromJSONObject(obj)

    @staticmethod
    def fromJSONObject(obj: dict) -> "MediaCachingDirective":
        kwargs = {}
        mand_fields = ['noCache']
        no_cache = None
        for k,v in obj.items():
            if k == 'noCache':
                no_cache = v
                mand_fields.remove(k)
            elif k == "statusCodeFilters":
                kwargs['status_code_filters'] = v
            elif k == 'maxAge':
                kwargs['max_age'] = v
            else:
                raise TypeError(f'MediaCachingDirective: JSON field "{k}" not understood')
        if len(mand_fields) > 0:
            raise TypeError(f'MediaCachingDirective: Mandatory JSON fields {mand_fields!r} are missing')
        return MediaCachingDirective(no_cache, **kwargs)

    def jsonObject(self) -> dict:
        obj = {'noCache': self.__no_cache}
        if self.__status_code_filters is not None:
            obj['statusCodeFilters'] = self.__status_code_filters
        if self.__max_age is not None:
            obj['maxAge'] = self.__max_age
        return obj

    @property
    def no_cache(self) -> bool:
        return self.__no_cache

    @no_cache.setter
    def relative_path(self, value: bool):
        if not isinstance(value,bool):
            value = bool(value)
        self.__no_cache = value

    @property
    def status_code_filters(self) -> Optional[List[int]]:
        return self.__status_code_filters

    @status_code_filters.setter
    def status_code_filters(self, value: Optional[Iterable[int]]):
        if value is not None:
            if not isinstance(value, list):
                value = list(value)
            if not all(isinstance(v,int) for v in value):
                raise TypeError('MediaCachingDirective.status_code_filters can be None or a list of int status codes')
            if len(value) == 0:
                value = None
        self.__status_code_filters = value

    def addStatusCodeFilter(self, value: int):
        if not isinstance(value,int):
            raise TypeError('MediaCachingDirective.caching_directives is a list of int')
        if self.__status_code_filters is None:
            self.__status_code_filters = []
        self.__status_code_filters += [value]

    def removeStatusCodeFilter(self, value: int) -> bool:
        if self.__status_code_filters is None:
            return False
        try:
            self.__status_code_filters.remove(value)
        except ValueError:
            return False
        if len(self.__status_code_filters) == 0:
            self.__status_code_filters = None
        return True

    @property
    def max_age(self) -> int:
        return self.__max_age

    @max_age.setter
    def max_age(self, value: Optional[int]):
        if value is not None:
            if not isinstance(value, int):
                raise TypeError('MediaCachingDirective.max_age can be either None or an int')
        self.__max_age = value

    __conv_3gpp: Final[List[TypedDict('3GPPConversion', {'param': str, 'field': str, 'cls': Type, 'mandatory': bool})]] = [
        {'param': 'no_cache', 'field': 'noCache', 'cls': bool, 'mandatory': True},
        {'param': 'status_code_filters', 'field': 'statusCodeFilters', 'cls': List[int], 'mandatory': False},
        {'param': 'max_age', 'field': 'maxAge', 'cls': int, 'mandatory': False}
    ]

    @classmethod
    async def from3GPPObject(cls, dc: CachingDirective) -> "MediaCachingDirective":
        args = []
        kwargs = {}
        for cnv in cls.__conv_3gpp:
            if cnv['mandatory']:
                args += [await cls.doConversion(dc[cnv['field']],cnv['cls'],'from3GPPObject')]
            elif cnv['field'] in dc:
                kwargs[cnv['param']] = await cls.doConversion(dc[cnv['field']],cnv['cls'],'from3GPPObject')
        return await cls(*args,**kwargs)

    async def to3GPPObject(self, session: "MediaSession") -> CachingDirective:
        from .media_session import MediaSession
        ret = {}
        for cnv in self.__conv_3gpp:
            v = getattr(self, cnv['param'], None)
            if v is not None:
                ret[cnv['field']] = await self.doConversion(v, cnv['cls'], 'to3GPPObject', session)
        return CachingDirective(ret)

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

