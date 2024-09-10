#!/usr/bin/python3 
#==============================================================================
# 5G-MAG Reference Tools: MediaChargingSpecification class
#==============================================================================
#
# File: rt_media_configuration/media_charging_specification.py
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
5G-MAG Reference Tools: MediaChargingSpecification Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaChargingSpecification class which models the charging
configuration for a MediaDynamicPolicy.
'''

import json
from typing import Optional, List, Iterable
from .gpsi import Gpsi

class MediaChargingSpecification:
    '''MediaChargingSpecification class
================================
the MediaChargingSpecification class provides the charging configuration for a
MediaDynamicPolicy.
'''

    def __init__(self, sponsor_id: Optional[str] = None, enabled: Optional[bool] = None, gpsis: Optional[Iterable[Gpsi]] = None):
        if gpsis is not None and len(gpsis) < 1:
            gpsis = None
        self.sponsor_id = sponsor_id
        self.enabled = enabled
        self.gpsis = gpsis

    def __await__(self):
        return self.__asyncInit().__await__()

    async def __asyncInit(self):
        '''Asynchronous object instantiation
        :meta private:
        :return: self
        '''
        return self

    def __eq__(self, other: "MediaChargingSpecification") -> bool:
        if self.__sponsor_id != other.__sponsor_id:
            return False
        if self.__enabled != other.__enabled:
            return False
        return sorted(self.__gpsis) == sorted(other.__gpsis)

    def __ne__(self, other: "MediaChargingSpecification") -> bool:
        return not self == other

    def __repr__(self) -> str:
        ret = f'{self.__class__.__name__}('
        np = ""
        if self.__sponsor_id is not None:
            ret += f'sponsor_id={self.__sponsor_id!r}'
            np = ", "
        if self.__enabled is not None:
            ret += f'{np}enabled={self.__enabled!r}'
            np = ", "
        if self.__gpsis is not None:
            ret += f'{np}gpsis={self.__gpsis!r}'
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
    def deserialise(json_obj: str) -> "MediaChargingSpecification":
        try:
            obj = json.loads(json_obj)
        except json.JSONDecodeError:
            raise ValueError("Bad JSON")

        return MediaChargingSpecification.fromJSONObject(obj)

    @staticmethod
    def fromJSONObject(obj: dict) -> "MediaChargingSpecification":
        kwargs = {}
        for k,v in obj.items():
            if k == "sponId":
                kwargs['sponsor_id'] = v
            elif k == "sponsorEnabled":
                kwargs['enabled'] = v
            elif k == "gpsi" and len(v) > 0:
                kwargs['gpsis'] = [Gpsi.fromJSONObject(gpsi) for gpsi in v]
            else:
                raise ValueError(f'MediaChargingSpecification: JSON field "{k}" not understood')
        return MediaChargingSpecification(**kwargs)

    def jsonObject(self) -> dict:
        obj = {}
        if self.__sponsor_id is not None:
            obj['sponId'] = self.__sponsor_id
        if self.__enabled is not None:
            obj['enabled'] = self.__enabled
        if self.__gpsis is not None:
            obj['gpsi'] = self.__gpsis
        return obj

    @property
    def sponsor_id(self) -> Optional[str]:
        return self.__sponsor_id

    @sponsor_id.setter
    def sponsor_id(self, value: Optional[str]) -> None:
        if value is not None:
            if not isinstance(value, str):
                raise TypeError('MediaChargingSpecification.sponsor_id must be a str or None')
        self.__sponsor_id = value

    @property
    def enabled(self) -> Optional[bool]:
        return self.__enabled

    @enabled.setter
    def enabled(self, value: Optional[bool]) -> None:
        if value is not None:
            if not isinstance(value, bool):
                value = bool(value)
        self.__enabled = value

    @property
    def gpsis(self) -> Optional[List[Gpsi]]:
        return self.__gpsis

    @gpsis.setter
    def gpsis(self, value: Optional[Iterable[Gpsi]]) -> None:
        if value is not None:
            if not isinstance(value, list):
                value = list(value)
            if not all(isinstance(v, Gpsi) for v in value):
                raise TypeError('MediaChargingSpecification.gpsis can only be None or a list of Gpsi objects')
        self.__gpsis = value

    def addGpsi(self, value: Gpsi) -> None:
        if not isinstance(value, Gpsi):
            raise TypeError('MediaChargingSpecification.gpsis can only hold Gpsi objects')
        if self.__gpsis is None:
            self.__gpsis = []
        self.__gpsis += [value]

    def removeGpsi(self, value: Gpsi) -> bool:
        if self.__gpsis is None:
            return False
        try:
            self.__gpsis.remove(value)
        except ValueError:
            return False
        if len(self.__gpsis) == 0:
            self.__gpsis = None
        return True

    def unsetGpsis(self):
        self.__gpsis = None
