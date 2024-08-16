#!/usr/bin/python3
#==============================================================================
# 5G-MAG Reference Tools: Bitrate class
#==============================================================================
#
# File: rt_media_configuration/bitrate.py
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
5G-MAG Reference Tools: Bitrate Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the Bitrate class which models a bitrate string.

Strings take the format [-]<digits>[" "]["bps"|"Kbps"|"Mbps"|"Gbps"|"Tbps"].
If no qualifier is given then "bps" is assumed.
'''

import json
import re
from typing import Optional

_MATCH_BITRATE_RE = re.compile(r'^(-?(?:\d*\.\d+|\d+))\s*(bps|Kbps|Mbps|Gbps|Tbps)?$', flags=re.IGNORECASE)
_MATCH_BITRATE_VALUE_GROUP = 1
_MATCH_BITRATE_UNITS_GROUP = 2

class Bitrate:
    '''Bitrate class
=============
Converts and represents a bitrate.
'''

    def __init__(self, bps: Optional[int] = None, *, kbps: Optional[float] = None,
                 mbps: Optional[float] = None, gbps: Optional[float] = None,
                 tbps: Optional[float] = None):
        if all(p is None for p in [bps, kbps, mbps, gbps, tbps]):
            bps = 0
        elif kbps is not None:
            if bps is not None:
                raise ValueError('Only one of bps, kbps, mbps, gbps or tbps may be set while instantiating Bitrate')
            bps = int(kbps*1000)
        elif mbps is not None:
            if bps is not None:
                raise ValueError('Only one of bps, kbps, mbps, gbps or tbps may be set while instantiating Bitrate')
            bps = int(mbps*1000000)
        elif gbps is not None:
            if bps is not None:
                raise ValueError('Only one of bps, kbps, mbps, gbps or tbps may be set while instantiating Bitrate')
            bps = int(gbps*1000000000)
        elif tbps is not None:
            if bps is not None:
                raise ValueError('Only one of bps, kbps, mbps, gbps or tbps may be set while instantiating Bitrate')
            bps = int(tbps*1000000000000)
        self.bps: int = bps

    def __await__(self):
        return self.__asyncInit().__await__()

    async def __asyncInit(self):
        '''Asynchronous object instantiation
        :meta private:
        :return: self
        '''
        return self

    def __eq__(self, other: "Bitrate") -> bool:
        return self.bps == other.bps

    def __ne__(self, other: "Bitrate") -> bool:
        return self.bps != other.bps

    def __lt__(self, other: "Bitrate") -> bool:
        return self.bps < other.bps

    def __le__(self, other: "Bitrate") -> bool:
        return self.bps <= other.bps

    def __ge__(self, other: "Bitrate") -> bool:
        return self.bps >= other.bps

    def __gt__(self, other: "Bitrate") -> bool:
        return self.bps > other.bps

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.bps})'

    def __str__(self) -> str:
        if self.bps > 1000000000000:
            return f'{self.bps/1000000000000.0:0.3f} Tbps'
        elif self.bps > 1000000000:
            return f'{self.bps/1000000000.0:0.3f} Gbps'
        elif self.bps > 1000000:      
            return f'{self.bps/1000000.0:0.3f} Mbps'
        elif self.bps > 1000:      
            return f'{self.bps/1000.0:0.3f} Kbps'
        return f'{self.bps} bps'

    def serialise(self, pretty: bool = False) -> str:
        return f'"{self}"'

    @staticmethod
    def deserialise(json_obj: str) -> "Bitrate":
        try:
            obj = json.loads(json_obj)
        except json.JSONDecodeError:
            raise ValueError("Bad JSON")

        return Bitrate.fromJSONObject(obj)

    @staticmethod
    def fromJSONObject(obj: str) -> "Bitrate":
        if not isinstance(obj,str):
            raise TypeError('Bitrate is represented by a string')
        global _MATCH_BITRATE_RE
        global _MATCH_BITRATE_VALUE_GROUP
        global _MATCH_BITRATE_UNITS_GROUP
        match = _MATCH_BITRATE_RE.match(obj)
        if match is None:
            raise ValueError('Bitrate not in correct format')
        (value,units) = match.group(_MATCH_BITRATE_VALUE_GROUP, _MATCH_BITRATE_UNITS_GROUP)
        bps = None
        if units is not None:
            units = units.lower()
        if units is None or units == 'bps':
            bps = int(float(value))
        elif units == 'kbps':
            bps = int(float(value)*1000.0)
        elif units == 'mbps':
            bps = int(float(value)*1000000.0)
        elif units == 'gbps':
            bps = int(float(value)*1000000000.0)
        elif units == 'tbps':
            bps = int(float(value)*1000000000000.0)
        else:
            raise ValueError('Bitrate units not understood')
        return Bitrate(bps)
    
    def jsonObject(self) -> str:
        return str(self)
