# 5G-MAG Reference Tools: MediaPathRewriteRule class
#==============================================================================
#
# File: rt_media_configuration/media_path_rewrite_rule.py
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
5G-MAG Reference Tools: MediaPathRewriteRule Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaPathRewriteRule class which models a single media
entry point for a MediaDistribution.
'''

import json
from typing import Optional, Final, Any, Type, TypedDict, List

from rt_m1_client.types import PathRewriteRule

class MediaPathRewriteRule:
    '''MediaPathRewriteRule class
==========================

This models a path rewrite rule for a MediaDistribution.
'''

    def __init__(self, request_path_pattern: Optional[str] = None, mapped_path: Optional[str] = None):
        self.request_path_pattern = request_path_pattern
        self.mapped_path = mapped_path

    def __await__(self):
        return self.__asyncInit().__await__()

    async def __asyncInit(self):
        '''Asynchronous object instantiation
        :meta private:
        :return: self
        '''
        return self

    def __eq__(self, other: "MediaPathRewriteRule") -> bool:
        if self.__request_path_pattern != other.request_path_pattern:
            return False
        return self.__mapped_path == other.mapped_path

    def __ne__(self, other: "MediaPathRewriteRule") -> bool:
        return not self == other

    def __lt__(self, other: Optional["MediaPathRewriteRule"]) -> bool:
        if other is None:
            return False
        if self.__request_path_pattern is not None:
            if other.request_path_pattern is None:
                return False
            if self.__request_path_pattern != other.request_path_pattern:
                return self.__request_path_pattern < other.request_path_pattern
        elif other.request_path_pattern is not None:
            return True
        if self.__mapped_path is not None:
            if other.mapped_path is None:
                return False
            if self.__mapped_path != other.mapped_path:
                return self.__mapped_path < other.mapped_path
        elif other.mapped_path is not None:
            return True
        return False

    def __le__(self, other: "MediaPathRewriteRule") -> bool:
        if other is None:
            return False
        if self.__request_path_pattern is not None:
            if other.request_path_pattern is None:
                return False
            if self.__request_path_pattern != other.request_path_pattern:
                return self.__request_path_pattern < other.request_path_pattern
        elif other.request_path_pattern is not None:
            return True
        if self.__mapped_path is not None:
            if other.mapped_path is None:
                return False
            if self.__mapped_path != other.mapped_path:
                return self.__mapped_path < other.mapped_path
        return True

    def __ge__(self, other: "MediaPathRewriteRule") -> bool:
        return not self < other

    def __gt__(self, other: "MediaPathRewriteRule") -> bool:
        return not self <= other

    def __repr__(self) -> str:
        '''Python constructor string for this object'''
        ret = f'{self.__class__.__name__}('
        sep = ''
        if self.__request_path_pattern is not None:
            ret += f'request_path_pattern={self.__request_path_pattern!r}'
            sep = ', '
        if self.__mapped_path is not None:
            ret += f'{sep}mapped_path={self.__mapped_path!r}'
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
    def deserialise(json_obj: str) -> "MediaPathRewriteRule":
        try:
            obj = json.loads(json_obj)
        except json.JSONDecodeError:
            raise ValueError("Bad JSON")
        return MediaPathRewriteRule.fromJSONObject(obj)

    @staticmethod
    def fromJSONObject(obj: dict) -> "MediaPathRewriteRule":
        kwargs = {}
        #mand_fields = ['requestPathPattern','mappedPath']
        #rel_path = None
        #content_type = None
        for k,v in obj.items():
            if k == 'requestPathPattern':
                kwargs['request_path_pattern'] = v
            elif k == 'mappedPath':
                kwargs['mapped_path'] = v
            else:
                raise TypeError(f'MediaPathRewriteRule: JSON field "{k}" not understood')
        #if len(mand_fields) > 0:
        #    raise TypeError(f'MediaPathRewriteRule: Mandatory JSON fields {mand_fields!r} are missing')
        return MediaPathRewriteRule(**kwargs)

    def jsonObject(self) -> dict:
        obj = {}
        if self.__request_path_pattern is not None:
            obj['requestPathPattern'] = self.__request_path_pattern
        if self.__mapped_path is not None:
            obj['mappedPath'] = self.__mapped_path
        return obj

    @property
    def request_path_pattern(self) -> str:
        return self.__request_path_pattern

    @request_path_pattern.setter
    def request_path_pattern(self, value: str):
        if not isinstance(value,str) or len(value) == 0:
            raise TypeError('MediaPathRewriteRule.request_path_pattern must be a non-empty str')
        self.__request_path_pattern = value

    @property
    def mapped_path(self) -> str:
        return self.__mapped_path

    @mapped_path.setter
    def mapped_path(self, value: str):
        if not isinstance(value,str) or len(value) == 0:
            raise TypeError('MediaPathRewriteRule.mapped_path must be a non-empty str')
        self.__mapped_path = value

    __conv_3gpp: Final[List[TypedDict('3GPPConversion', {'param': str, 'field': str, 'cls': Type})]] = [
        {'param': 'request_path_pattern', 'field': 'requestPathPattern', 'cls': str},
        {'param': 'mapped_path', 'field': 'mappedPath', 'cls': str}
    ]

    @classmethod
    async def from3GPPObject(cls, dc: PathRewriteRule) -> "MediaPathRewriteRule":
        kwargs = {}
        for cnv in cls.__conv_3gpp:
            if cnv['field'] in dc:
                kwargs[cnv['param']] = await cls.doConversion(dc[cnv['field']],cnv['cls'],'from3GPPObject')
        return await cls(**kwargs)

    async def to3GPPObject(self, session: "MediaSession") -> PathRewriteRule:
        from .media_session import MediaSession
        ret = {}
        for cnv in self.__conv_3gpp:
            v = getattr(self, cnv['param'], None)
            if v is not None:
                ret[cnv['field']] = await self.doConversion(v, cnv['cls'], 'to3GPPObject', session)
        return PathRewriteRule(ret)

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

