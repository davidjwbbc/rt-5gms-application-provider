# 5G-MAG Reference Tools: MediaCachingConfiguration class
#==============================================================================
#
# File: rt_media_configuration/media_caching_configuration.py
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
5G-MAG Reference Tools: MediaCachingConfiguration Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaCachingConfiguration class which models a single media
entry point for a MediaDistribution.
'''

import json
from typing import Optional, List, Iterable, Final, Type, Any, TypedDict

from rt_m1_client.types import CachingConfiguration

from .media_caching_directive import MediaCachingDirective

class MediaCachingConfiguration:
    '''MediaCachingConfiguration class
=====================

This models a caching configuration for a MediaDistribution.
'''

    def __init__(self, url_pattern_filter: str, caching_directives: Optional[Iterable[MediaCachingDirective]] = None):
        self.url_pattern_filter = url_pattern_filter
        self.caching_directives = caching_directives

    def __await__(self):
        return self.__asyncInit().__await__()

    async def __asyncInit(self):
        '''Asynchronous object instantiation
        :meta private:
        :return: self
        '''
        return self

    def __eq__(self, other: "MediaCachingConfiguration") -> bool:
        if self.__url_pattern_filter != other.__url_pattern_filter:
            return False
        return ((self.__caching_directives is None and other.caching_directives is None) or
                (self.__caching_directives is not None and other.__caching_directives is not None and sorted(self.__caching_directives) != sorted(other.__caching_directives))
               )

    def __ne__(self, other: "MediaCachingConfiguration") -> bool:
        return not self == other

    def __lt__(self, other: "MediaCachingConfiguration") -> bool:
        if self.__url_pattern_filter != other.url_pattern_filter:
            return self.__url_pattern_filter < other.url_pattern_filter
        if self.__caching_directives is not None:
            if other.caching_directives is None:
                return False
            if len(self.__caching_directives) != len(other.caching_directives):
                return len(self.__caching_directives) < len(other.caching_directives)
            return sorted(self.__caching_directives) < sorted(other.caching_directives)
        elif other.caching_directives is not None:
            return True
        return False

    def __le__(self, other: "MediaCachingConfiguration") -> bool:
        if self.__url_pattern_filter != other.url_pattern_filter:
            return self.__url_pattern_filter < other.url_pattern_filter
        if self.__caching_directives is not None:
            if other.__caching_directives is None:
                return False
            if len(self.__caching_directives) != len(other.caching_directives):
                return len(self.__caching_directives) < len(other.caching_directives)
            return sorted(self.__caching_directives) < sorted(other.caching_directives)
        elif other.caching_directives is not None:
            return True
        return True

    def __ge__(self, other: "MediaCachingConfiguration") -> bool:
        return not self < other

    def __gt__(self, other: "MediaCachingConfiguration") -> bool:
        return not self <= other

    def __repr__(self) -> str:
        '''Python constructor string for this object'''
        ret = f'{self.__class__.__name__}({self.__url_pattern_filter!r}'
        if self.__caching_directives is not None:
            ret += f', caching_directives={self.caching_directives!r}'
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
    def deserialise(json_obj: str) -> "MediaCachingConfiguration":
        try:
            obj = json.loads(json_obj)
        except json.JSONDecodeError:
            raise ValueError("Bad JSON")
        return MediaCachingConfiguration.fromJSONObject(obj)

    @staticmethod
    def fromJSONObject(obj: dict) -> "MediaCachingConfiguration":
        kwargs = {}
        mand_fields = ['urlPatternFilter']
        url_pattern = None
        for k,v in obj.items():
            if k == 'urlPatternFilter':
                url_pattern = v
                mand_fields.remove(k)
            elif k == "cachingDirectives":
                kwargs['caching_directives'] = [MediaCachingDirective.fromJSONObject(value) for value in v]
            else:
                raise TypeError(f'MediaCachingConfiguration: JSON field "{k}" not understood')
        if len(mand_fields) > 0:
            raise TypeError(f'MediaCachingConfiguration: Mandatory JSON fields {mand_fields!r} are missing')
        return MediaCachingConfiguration(url_pattern, **kwargs)

    def jsonObject(self) -> dict:
        obj = {'urlPatternFilter': self.__url_pattern_filter}
        if self.__caching_directives is not None:
            obj['cachingDirectives'] = self.__caching_directives
        return obj

    @property
    def url_pattern_filter(self) -> str:
        return self.__url_pattern_filter

    @url_pattern_filter.setter
    def relative_path(self, value: str):
        if not isinstance(value,str) or len(value) == 0:
            raise TypeError('MediaCachingConfiguration.url_pattern_filter must be a non-empty str')
        self.__url_pattern_filter = value

    @property
    def caching_directives(self) -> Optional[List[MediaCachingDirective]]:
        return self.__caching_directives

    @caching_directives.setter
    def caching_directives(self, value: Optional[Iterable[MediaCachingDirective]]):
        if value is not None:
            if not isinstance(value, list):
                value = list(value)
            if not all(isinstance(v,MediaCachingDirective) for v in value):
                raise TypeError('MediaCachingConfiguration.caching_directives can be None or a list of MediaCachingDirective')
            if len(value) == 0:
                value = None
        self.__caching_directives = value

    def addCachingDirective(self, value: MediaCachingDirective):
        if not isinstance(value,MediaCachingDirective):
            raise TypeError('MediaCachingConfiguration.caching_directives is a list of MediaCachingDirective')
        if self.__caching_directives is None:
            self.__caching_directives = []
        self.__caching_directives += [value]

    def removeCachingDirective(self, value: MediaCachingDirective) -> bool:
        if self.__caching_directives is None:
            return False
        try:
            self.__caching_directives.remove(value)
        except ValueError:
            return False
        if len(self.__caching_directives) == 0:
            self.__caching_directives = None
        return True

    __conv_3gpp: Final[List[TypedDict('3GPPConversion', {'param': str, 'field': str, 'cls': Type, 'mandatory': bool})]] = [
        {'param': 'url_pattern_filter', 'field': 'urlPatternFilter', 'cls': str, 'mandatory': True},
        {'param': 'caching_directives', 'field': 'cachingDirectives', 'cls': List[MediaCachingDirective], 'mandatory': False}
    ]

    @classmethod
    async def from3GPPObject(cls, cc: CachingConfiguration) -> "MediaCachingConfiguration":
        args = []
        kwargs = {}
        for cnv in cls.__conv_3gpp:
            if cnv['mandatory']:
                args += [await cls.doConversion(cc[cnv['field']],cnv['cls'],'from3GPPObject')]
            elif cnv['field'] in cc:
                kwargs[cnv['param']] = await cls.doConversion(cc[cnv['field']],cnv['cls'],'from3GPPObject')
        return await cls(*args, **kwargs)

    async def to3GPPObject(self, session: "MediaSession") -> CachingConfiguration:
        from .media_session import MediaSession
        ret = {}
        for cnv in self.__conv_3gpp:
            v = getattr(self, cnv['param'], None)
            if v is not None:
                ret[cnv['field']] = await self.doConversion(v, cnv['cls'], 'to3GPPObject', session)
        return CachingConfiguration(ret)

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

