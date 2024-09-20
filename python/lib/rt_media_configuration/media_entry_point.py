# 5G-MAG Reference Tools: MediaEntryPoint class
#==============================================================================
#
# File: rt_media_configuration/media_entry_point.py
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
5G-MAG Reference Tools: MediaEntryPoint Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaEntryPoint class which models a single media
entry point for a MediaDistribution.
'''

import json
from typing import Optional, List, Iterable, Final, Type, TypedDict, Any

from rt_m1_client.types import M1MediaEntryPoint

class MediaEntryPoint:
    '''MediaEntryPoint class
=====================

This models a media entry point which consists of mandatory relative path and
a mime content type with an optional array of profile strings.
'''

    def __init__(self, relative_path: str, content_type: str, profiles: Optional[Iterable[str]] = None):
        self.relative_path = relative_path
        self.content_type = content_type
        self.profiles = profiles

    def __await__(self):
        return self.__asyncInit().__await__()

    async def __asyncInit(self):
        '''Asynchronous object instantiation
        :meta private:
        :return: self
        '''
        return self

    def __eq__(self, other: "MediaEntryPoint") -> bool:
        if self.__relative_path != other.relative_path:
            return False
        if self.__content_type != other.content_type:
            return False
        if self.__profiles is None:
            if other.profiles is not None:
                return False
            return True
        elif other.profiles is None:
            return False
        return sorted(self.__profiles) == sorted(other.profiles)

    def __ne__(self, other: "MediaEntryPoint") -> bool:
        return not (self == other)

    def __lt__(self, other: "MediaEntryPoint") -> bool:
        if self.__relative_path != other.__relative_path:
            return self.__relative_path < other.__relative_path
        if self.__content_type != other.__content_type:
            return self.__content_type < other.__content_type
        if self.__profiles is not None:
            if other.__profiles is None:
                return False
            if len(self.__profiles) != len(other.__profiles):
                return len(self.__profiles) < len(other.__profiles)
            return sorted(self.__profiles) < sorted(other.__profiles)
        elif other.__profiles is not None:
            return True
        return False

    def __le__(self, other: "MediaEntryPoint") -> bool:
        if self.__relative_path != other.__relative_path:
            return self.__relative_path < other.__relative_path
        if self.__content_type != other.__content_type:
            return self.__content_type < other.__content_type
        if self.__profiles is not None:
            if other.__profiles is None:
                return False
            if len(self.__profiles) != len(other.__profiles):
                return len(self.__profiles) < len(other.__profiles)
            return sorted(self.__profiles) < sorted(other.__profiles)
        elif other.__profiles is not None:
            return True
        return True

    def __ge__(self, other: "MediaEntryPoint") -> bool:
        return not (self < other)

    def __gt__(self, other: "MediaEntryPoint") -> bool:
        return not (self <= other)

    def __repr__(self) -> str:
        '''Python constructor string for this object'''
        ret = f'{self.__class__.__name__}({self.__relative_path!r}, {self.__content_type!r}'
        if self.__profiles is not None:
            ret += f', profiles={self.profiles!r}'
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
    def deserialise(json_obj: str) -> "MediaEntryPoint":
        try:
            obj = json.loads(json_obj)
        except json.JSONDecodeError:
            raise ValueError("Bad JSON")
        return MediaEntryPoint.fromJSONObject(obj)

    @staticmethod
    def fromJSONObject(obj: dict) -> "MediaEntryPoint":
        kwargs = {}
        mand_fields = ['relativePath','contentType']
        rel_path = None
        content_type = None
        for k,v in obj.items():
            if k == 'relativePath':
                rel_path = v
                mand_fields.remove(k)
            elif k == 'contentType':
                content_type = v
                mand_fields.remove(k)
            elif k == "profiles":
                kwargs['profiles'] = v
            else:
                raise TypeError(f'MediaEntryPoint: JSON field "{k}" not understood')
        if len(mand_fields) > 0:
            raise TypeError(f'MediaEntryPoint: Mandatory JSON fields {mand_fields!r} are missing')
        return MediaEntryPoint(rel_path, content_type, **kwargs)

    def jsonObject(self) -> dict:
        obj = {"relativePath": self.__relative_path, "contentType": self.__content_type}
        if self.__profiles is not None:
            obj['profiles'] = self.__profiles
        return obj

    @property
    def relative_path(self) -> str:
        return self.__relative_path

    @relative_path.setter
    def relative_path(self, value: str):
        if not isinstance(value,str) or len(value) == 0:
            raise TypeError('MediaEntryPoint.relative_path must be a non-empty str')
        self.__relative_path = value

    @property
    def content_type(self) -> str:
        return self.__content_type

    @content_type.setter
    def content_type(self, value: str):
        if not isinstance(value,str) or len(value) == 0:
            raise TypeError('MediaEntryPoint.content_type must be a non-empty str')
        self.__content_type = value

    @property
    def profiles(self) -> Optional[List[str]]:
        return self.__profiles

    @profiles.setter
    def profiles(self, value: Optional[Iterable[str]]):
        if value is not None:
            if not isinstance(value, list):
                value = list(value)
            if not all(isinstance(v,str) for v in value):
                raise TypeError('MediaEntryPoint.profiles can be None or a list of str')
            if len(value) == 0:
                value = None
        self.__profiles = value

    def addProfile(self, value: str):
        if not isinstance(value,str):
            raise TypeError('MediaEntryPoint.profiles is a list of str')
        if self.__profiles is None:
            self.__profiles = []
        self.__profiles += [value]

    def removeProfile(self, value: str) -> bool:
        if self.__profiles is None:
            return False
        try:
            self.__profiles.remove(value)
        except ValueError:
            return False
        if len(self.__profiles) == 0:
            self.__profiles = None
        return True

    __conv_3gpp: Final[List[TypedDict('3GPPConversion', {'param': str, 'field': str, 'cls': Type})]] = [
        {'param': 'relative_path', 'field': 'relativePath', 'cls': str},
        {'param': 'content_type', 'field': 'contentType', 'cls': str},
        {'param': 'profiles', 'field': 'profiles', 'cls': List[str]}
    ]

    @classmethod
    async def from3GPPObject(cls, ep: M1MediaEntryPoint) -> "MediaEntryPoint":
        kwargs = {}
        for cnv in cls.__conv_3gpp:
            if cnv['field'] in ep:
                kwargs[cnv['param']] = await cls.doConversion(ep[cnv['field']],cnv['cls'],'from3GPPObject')
        return await cls(**kwargs)

    async def to3GPPObject(self, session: "MediaSession") -> M1MediaEntryPoint:
        from .media_session import MediaSession
        ret = {}
        for cnv in self.__conv_3gpp:
            v = getattr(self, cnv['param'], None)
            if v is not None:
                ret[cnv['field']] = await self.doConversion(v, cnv['cls'], 'to3GPPObject', session)
        return M1MediaEntryPoint(ret)

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
