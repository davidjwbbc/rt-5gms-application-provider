# 5G-MAG Reference Tools: MediaURLSignature class
#==============================================================================
#
# File: rt_media_configuration/media_url_signature.py
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
5G-MAG Reference Tools: MediaURLSignature Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaURLSignature class which models a single media
entry point for a MediaDistribution.
'''

import json
from typing import Optional, List, Final, Type, Any, TypedDict

from rt_m1_client.types import URLSignature

class MediaURLSignature:
    '''MediaURLSignature class
=======================

This models a URL signature for a MediaDistribution.
'''

    def __init__(self, url_pattern: str, token_name: str, passphrase_name: str, passphrase: str, token_expiry_name: str, use_ip_address: bool, ip_address_name: Optional[str] = None):
        self.url_pattern = url_pattern
        self.token_name = token_name
        self.passphrase_name = passphrase_name
        self.passphrase = passphrase
        self.token_expiry_name = token_expiry_name
        self.use_ip_address = use_ip_address
        self.ip_address_name = ip_address_name

    def __await__(self):
        return self.__asyncInit().__await__()

    async def __asyncInit(self):
        '''Asynchronous object instantiation
        :meta private:
        :return: self
        '''
        return self

    def __eq__(self, other: "MediaURLSignature") -> bool:
        if self.__url_pattern != other.url_pattern:
            return False
        if self.__token_name != other.token_name:
            return False
        if self.__passphrase_name != other.passphrase_name:
            return False
        if self.__passphrase != other.passphrase:
            return False
        if self.__token_expiry_name != other.token_expiry_name:
            return False
        if self.__use_ip_address != other.use_ip_address:
            return False
        if self.__ip_address_name is not None:
            if other.ip_address_name is None:
                return False
            return self.__ip_address_name == other.ip_address_name
        return other.ip_address_name is None

    def __ne__(self, other: "MediaURLSignature") -> bool:
        return not self == other

    def __lt__(self, other: "MediaURLSignature") -> bool:
        if self.__url_pattern != other.url_pattern:
            return self.__url_pattern < other.url_pattern
        if self.__token_name != other.token_name:
            return self.__token_name < other.token_name
        if self.__passphrase_name != other.passphrase_name:
            return self.__passphrase_name < other.passphrase_name
        if self.__passphrase != other.passphrase:
            return self.__passphrase < other.passphrase
        if self.__token_expiry_name != other.token_expiry_name:
            return self.__token_expiry_name < other.token_expiry_name
        if self.__use_ip_address != other.use_ip_address:
            return not self.__use_ip_address
        if self.__ip_address_name != other.ip_address_name:
            return self.__ip_address_name < other.ip_address_name
        return False

    def __le__(self, other: "MediaURLSignature") -> bool:
        if self.__url_pattern != other.url_pattern:
            return self.__url_pattern < other.url_pattern
        if self.__token_name != other.token_name:
            return self.__token_name < other.token_name
        if self.__passphrase_name != other.passphrase_name:
            return self.__passphrase_name < other.passphrase_name
        if self.__passphrase != other.passphrase:
            return self.__passphrase < other.passphrase
        if self.__token_expiry_name != other.token_expiry_name:
            return self.__token_expiry_name < other.token_expiry_name
        if self.__use_ip_address != other.use_ip_address:
            return not self.__use_ip_address
        if self.__ip_address_name != other.ip_address_name:
            return self.__ip_address_name < other.ip_address_name
        return True

    def __ge__(self, other: "MediaURLSignature") -> bool:
        return not self < other

    def __gt__(self, other: "MediaURLSignature") -> bool:
        return not self <= other

    def __repr__(self) -> str:
        '''Python constructor string for this object'''
        ret = f'{self.__class__.__name__}({self.__url_pattern!r}, {self.__token_name!r}, {self.__passphrase_name!r}, {self.__passphrase!r}, {self.__token_expiry_name!r}, {self.__use_ip_address!r}'
        if self.__ip_address_name is not None:
            ret += f', ip_address_name={self.__ip_address_name!r}'
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
    def deserialise(json_obj: str) -> "MediaURLSignature":
        try:
            obj = json.loads(json_obj)
        except json.JSONDecodeError:
            raise ValueError("Bad JSON")
        return MediaURLSignature.fromJSONObject(obj)

    @staticmethod
    def fromJSONObject(obj: dict) -> "MediaURLSignature":
        kwargs = {}
        mand_fields = ['urlPattern','tokenName','passphraseName','passphrase','tokenExpiryName','useIPAddress']
        url_pattern = None
        token_name = None
        passphrase_name = None
        passphrase = None
        token_expiry_name = None
        use_ip_address = None
        for k,v in obj.items():
            if k == 'urlPattern':
                url_pattern = v
                mand_fields.remove(k)
            elif k == 'tokenName':
                token_name = v
                mand_fields.remove(k)
            elif k == 'passphraseName':
                passphrase_name = v
                mand_fields.remove(k)
            elif k == 'passphrase':
                passphrase = v
                mand_fields.remove(k)
            elif k == 'tokenExpiryName':
                token_expiry_name = v
                mand_fields.remove(k)
            elif k == 'useIPAddress':
                use_ip_address = v
                mand_fields.remove(k)
            elif k == 'ipAddressName':
                kwargs['ip_address_name'] = v
            else:
                raise TypeError(f'MediaURLSignature: JSON field "{k}" not understood')
        if len(mand_fields) > 0:
            raise TypeError(f'MediaURLSignature: Mandatory JSON fields {mand_fields!r} are missing')
        return MediaURLSignature(url_pattern, token_name, passphrase_name, passphrase, token_expiry_name, use_ip_address, **kwargs)

    def jsonObject(self) -> dict:
        ret = {'urlPattern': self.__url_pattern, 'tokenName': self.__token_name, 'passphraseName': self.__passphrase_name,
               'passphrase': self.__passphrase, 'tokenExpiryName': self.__token_expiry_name, 'useIPAddress': self.__use_ip_address}
        if self.__ip_address_name is not None:
            ret['ipAddressName'] = self.__ip_address_name
        return ret

    @property
    def url_pattern(self) -> str:
        return self.__url_pattern

    @url_pattern.setter
    def url_pattern(self, value: str):
        if not isinstance(value,str) or len(value) == 0:
            raise TypeError('MediaURLSignature.url_pattern must be a non-empty str')
        self.__url_pattern = value

    @property
    def token_name(self) -> str:
        return self.__token_name

    @token_name.setter
    def token_name(self, value: str):
        if not isinstance(value,str) or len(value) == 0:
            raise TypeError('MediaURLSignature.token_name must be a non-empty str')
        self.__token_name = value

    @property
    def passphrase_name(self) -> str:
        return self.__passphrase_name

    @passphrase_name.setter
    def passphrase_name(self, value: str):
        if not isinstance(value,str) or len(value) == 0:
            raise TypeError('MediaURLSignature.passphrase_name must be a non-empty str')
        self.__passphrase_name = value

    @property
    def passphrase(self) -> str:
        return self.__passphrase

    @passphrase.setter
    def passphrase(self, value: str):  
        if not isinstance(value,str) or len(value) == 0:
            raise TypeError('MediaURLSignature.passphrase must be a non-empty str')
        self.__passphrase = value

    @property
    def token_expiry_name(self) -> str:
        return self.__token_expiry_name

    @token_expiry_name.setter
    def token_expiry_name(self, value: str):
        if not isinstance(value,str) or len(value) == 0:
            raise TypeError('MediaURLSignature.token_expiry_name must be a non-empty str')
        self.__token_expiry_name = value

    @property
    def use_ip_address(self) -> bool:
        return self.__use_ip_address

    @use_ip_address.setter
    def use_ip_address(self, value: bool):
        if not isinstance(value, bool):
            value = bool(value)
        self.__use_ip_address = value

    @property
    def ip_address_name(self) -> Optional[str]:
        return self.__ip_address_name

    @ip_address_name.setter
    def ip_address_name(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeError('MediaURLSignature.ip_address_name must be either None or a non-empty str')
            if len(value) == 0:
                value = None
        self.__ip_address_name = value

    __conv_3gpp: Final[List[TypedDict('3GPPConversion', {'param': str, 'field': str, 'cls': Type, 'mandatory': bool})]] = [
        {'param': 'url_pattern', 'field': 'urlPattern', 'cls': str, 'mandatory': True},
        {'param': 'token_name', 'field': 'tokenName', 'cls': str, 'mandatory': True},
        {'param': 'passphrase_name', 'field': 'passphraseName', 'cls': str, 'mandatory': True},
        {'param': 'passphrase', 'field': 'passphrase', 'cls': str, 'mandatory': True},
        {'param': 'token_expiry_name', 'field': 'tokenExpiryName', 'cls': str, 'mandatory': True},
        {'param': 'use_ip_address', 'field': 'useIPAddress', 'cls': bool, 'mandatory': True},
        {'param': 'ip_address_name', 'field': 'ipAddressName', 'cls': str, 'mandatory': False}
    ]

    @classmethod
    async def from3GPPObject(cls, us: URLSignature) -> "MediaURLSignature":
        args = []
        kwargs = {}
        for cnv in cls.__conv_3gpp:
            if cnv['mandatory']:
                args += [await cls.doConversion(us[cnv['field']],cnv['cls'],'from3GPPObject')]
            elif cnv['field'] in us:
                kwargs[cnv['param']] = await cls.doConversion(us[cnv['field']],cnv['cls'],'from3GPPObject')
        return await cls(*args, **kwargs)

    async def to3GPPObject(self, session: "MediaSession") -> URLSignature:
        from .media_session import MediaSession
        ret = {}
        for cnv in self.__conv_3gpp:
            v = getattr(self, cnv['param'], None)
            if v is not None:
                ret[cnv['field']] = await self.doConversion(v, cnv['cls'], 'to3GPPObject', session)
        return URLSignature(ret)

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
