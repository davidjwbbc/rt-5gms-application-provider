#!/usr/bin/python3 
#==============================================================================
# 5G-MAG Reference Tools: Snssai class
#==============================================================================
#
# File: rt_media_configuration/media_entry.py
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
5G-MAG Reference Tools: Snssai Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the Snssai class which models a 3GPP SNSSAI configuration
'''

import json
import string
from typing import Optional

class Snssai:
    '''Snssai class
============
This class models a 3GPP SNSSAI configuration specifier
'''

    def __init__(self, sst: int, sd: Optional[str] = None):
        self.sst = sst
        self.sd = sd

    def __await__(self):
        return self.__asyncInit().__await__()

    async def __asyncInit(self):
        '''Asynchronous object instantiation
        :meta private:
        :return: self
        '''
        return self

    def __eq__(self, other: "Snssai") -> bool:
        if self.__sst != other.__sst:
            return False
        return (self.__sd == other.__sd)

    def __ne__(self, other: "Snssai") -> bool:
        return not (self == other)

    def __repr__(self) -> str:
        '''Python constructor string for this object'''
        ret = f'{self.__class__.__name__}({self.__sst}'
        if self.__sd is not None:
            ret += f', sd={self.__sd!r}'
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
    def deserialise(json_obj: str) -> "Snssai":
        try:
            obj = json.loads(json_obj)
        except json.JSONDecodeError:
            raise ValueError("Bad JSON")
        return Snssai.fromJSONObject(obj)

    @staticmethod
    def fromJSONObject(obj: dict) -> "Snssai":
        mand_fields = ['sst']
        sst = None
        kwargs = {}
        for k,v in obj.items():
            if k == 'sst':
                sst = v
                mand_fields.remove(k)
            elif k == 'sd':
                kwargs['sd'] = v
            else:
                raise TypeError(f'Snssai: JSON field "{k}" not understood')
        if len(mand_fields) > 0:
            raise TypeError(f'Snssai: Mandatory JSON fields {mand_fields!r} are missing')
        return Snssai(sst, **kwargs)

    def jsonObject(self) -> dict:
        obj = {"sst": self.__sst}

    @property
    def sst(self):
        return self.__sst

    @sst.setter
    def sst(self, value: int):
        if not isinstance(value, int):
            raise TypeError('Snssai.sst must be an int')
        if value < 0 or value > 255:
            raise ValueError('Snssai.sst must be an integer between 0 and 255 inclusive')
        self.__sst = value

    @property
    def sd(self) -> Optional[str]:
        return self.__sd

    @sd.setter
    def sd(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeError('Snssai.sd must be either None or a 6 digit hexadecimal string')
            if len(value) != 6 or not all(c in string.hexdigits for c in value):
                raise ValueError('Snssai.sd must be a 6 digit hexadecimal string when specified')
        self.__sd = value
