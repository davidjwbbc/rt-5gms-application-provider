# 5G-MAG Reference Tools: Gpsi class
#==============================================================================
#
# File: rt_media_configuration/gpsi.py
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
5G-MAG Reference Tools: Gpsi class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the Gpsi class which ensures correct formatting of GPSI
strings.
'''

import json
import string

class Gpsi:
    '''Gpsi class
==========

This class provides validation of GPSI strings.
'''

    def __init__(self, gpsi: str):
        self.validate(gpsi)
        self.__gpsi: str = gpsi

    def __await__(self):
        return self.__asyncInit().__await__()

    async def __asyncInit(self):
        '''Asynchronous object instantiation
        :meta private:
        :return: self
        '''
        return self

    def __eq__(self, other: "Gpsi") -> bool:
        return self.__gpsi == other.__gpsi

    def __ne__(self, other: "Gpsi") -> bool:
        return not self == other

    def __lt__(self, other: "Gpsi") -> bool:
        return self.__gpsi < other.__gpsi

    def __le__(self, other: "Gpsi") -> bool:
        return self.__gpsi <= other.__gpsi

    def __ge__(self, other: "Gpsi") -> bool:
        return self.__gpsi >= other.__gpsi

    def __gt__(self, other: "Gpsi") -> bool:
        return self.__gpsi > other.__gpsi

    def __repr__(self) -> str:
        '''Python constructor string for this object'''
        return f'{self.__class__.__name__}({self.__gpsi!r})'

    def __str__(self) -> str:
        return self.__gpsi

    @property
    def gpsi(self):
        return self.__gpsi

    @gpsi.setter
    def gpsi(self, val: str):
        self.validate(val)
        self.__gpsi = val

    def serialise(self, pretty: bool = False) -> str:
        from .media_configuration import MediaConfiguration
        kwargs = {}
        if pretty:
            kwargs = {"sort_keys": True, "indent": 4}
        return json.dumps(self, default=MediaConfiguration.jsonObjectHandler, **kwargs)

    @staticmethod
    def deserialise(json_obj: str) -> "Gpsi":
        try:
            obj = json.loads(json_obj)
        except json.JSONDecodeError:
            raise ValueError("Bad JSON")
        return Gpsi.fromJSONObject(obj)

    @staticmethod
    def fromJSONObject(obj: str) -> "Gpsi":
        if not isinstance(obj,str):
            raise TypeError('Gpsi value must be a string')
        return Gpsi(obj)

    def jsonObject(self) -> str:
        return self.__gpsi

    @staticmethod
    def validate(value: str) -> bool:
        if value.startswith('msisdn-'):
            msisdn = value[7:]
            if len(msisdn) < 5 or len(msisdn) > 15 or not all(c in string.digits for c in msisdn):
                raise ValueError('msisdn GPSI must be "msisdn-" followed by 5 to 15 digits')
        if value.startswith('extid-'):
            extid = value[6:]
            (extid_first, extid_sep, extid_second) = extid.partition('@')
            if extid_sep != '@' or '@' in extid_first or '@' in extid_second or len(extid_first) == 0 or len(extid_second) == 0:
                raise ValueError('extid GPSI must be "extid-" followed by a string containing two parts separated by a single @ symbol')

    @classmethod
    async def from3GPPObject(cls, value: str) -> "Gpsi":
        return cls(value)

    async def to3GPPObject(self, session: "MediaSession") -> str:
        from .media_session import MediaSession
        return self.__gpsi
