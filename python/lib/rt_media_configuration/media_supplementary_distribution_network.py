# 5G-MAG Reference Tools: MediaSupplementaryDistributionNetwork class
#==============================================================================
#
# File: rt_media_configuration/media_supplementary_distribution_network.py
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
5G-MAG Reference Tools: MediaSupplementaryDistributionNetwork Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaSupplementaryDistributionNetwork class which models a single media
entry point for a MediaDistribution.
'''

import json
from typing import Optional, List, Iterable, Final, Union, Tuple

from rt_m1_client.types import DistributionNetworkType, DistributionMode

class MediaSupplementaryDistributionNetwork:
    '''MediaSupplementaryDistributionNetwork class
=====================

This models a media entry point which consists of mandatory relative path and
a mime content type with an optional array of profile strings.
'''

    DISTRIBUTION_NETWORK_EMBMS: Final[DistributionNetworkType] = DistributionNetworkType.DISTRIBUTION_NETWORK_EMBMS

    MODE_EXCLUSIVE: Final[DistributionMode] = DistributionMode.MODE_EXCLUSIVE
    MODE_HYBRID: Final[DistributionMode] = DistributionMode.MODE_HYBRID
    MODE_DYNAMIC: Final[DistributionMode] = DistributionMode.MODE_DYNAMIC

    def __init__(self, network_type: Union[int,DistributionNetworkType,str], mode: Union[int,DistributionMode,str]):
        self.network_type = network_type
        self.mode = mode

    def __await__(self):
        return self.__asyncInit().__await__()

    async def __asyncInit(self):
        '''Asynchronous object instantiation
        :meta private:
        :return: self
        '''
        return self

    def __eq__(self, other: "MediaSupplementaryDistributionNetwork") -> bool:
        if self.__network_type != other.network_type:
            return False
        return self.__mode == other.mode

    def __ne__(self, other: "MediaSupplementaryDistributionNetwork") -> bool:
        return not self == other

    def __lt__(self, other: "MediaSupplementaryDistributionNetwork") -> bool:
        if self.__network_type != other.network_type:
            return self.__network_type < other.network_type
        return self.__mode < other.mode

    def __le__(self, other: "MediaSupplementaryDistributionNetwork") -> bool:
        if self.__network_type != other.network_type:
            return self.__network_type < other.network_type
        return self.__mode <= other.mode

    def __ge__(self, other: "MediaSupplementaryDistributionNetwork") -> bool:
        return not self < other

    def __gt__(self, other: "MediaSupplementaryDistributionNetwork") -> bool:
        return not self <= other

    def __repr__(self) -> str:
        '''Python constructor string for this object'''
        return f'{self.__class__.__name__}({self.__network_type!r}, {self.__mode!r})'
        
    def __str__(self) -> str:
        return self.serialise(pretty=True)

    def serialise(self, pretty: bool = False) -> str:
        from .media_configuration import MediaConfiguration
        kwargs = {}
        if pretty:
            kwargs = {"sort_keys": True, "indent": 4}
        return json.dumps(self, default=MediaConfiguration.jsonObjectHandler, **kwargs)

    @staticmethod
    def deserialise(json_obj: str) -> "MediaSupplementaryDistributionNetwork":
        try:
            obj = json.loads(json_obj)
        except json.JSONDecodeError:
            raise ValueError("Bad JSON")
        return MediaSupplementaryDistributionNetwork.fromJSONObject(obj)

    @staticmethod
    def fromJSONObject(obj: list) -> "MediaSupplementaryDistributionNetwork":
        if not isinstance(obj, list) or len(obj) != 2 or not all(isinstance(v,str) for v in obj):
            raise TypeError(f'MediaSupplementaryDistributionNetwork is a duple of DistributionNetworkType and DistributionMode')
        return MediaSupplementaryDistributionNetwork(*obj)

    def jsonObject(self) -> list:
        return [str(self.__network_type), str(self.__mode)]

    @property
    def network_type(self) -> DistributionNetworkType:
        return self.__network_type

    @network_type.setter
    def network_type(self, value: Union[int,DistributionNetworkType,str]):
        if isinstance(value,int):
            value = DistributionNetworkType(value)
        if isinstance(value,str):
            value = DistributionNetworkType[value]
        if not isinstance(value, DistributionNetworkType):
            raise TypeError('MediaSupplementaryDistributionNetwork.network_type only understands the DISTRIBUTION_NETWORK_EMBMS enumerated type')
        self.__network_type = value

    @property
    def mode(self) -> DistributionMode:
        return self.__mode

    @mode.setter
    def mode(self, value: Union[int,DistributionMode,str]):
        if isinstance(value,int):
            value = DistributionMode(value)
        elif isinstance(value,str):
            value = DistributionMode[value]
        if not isinstance(value, DistributionMode):
            raise ValueError('MediaSupplementaryDistributionNetwork.mode only understands MODE_EXCLUSIVE, MODE_HYBRID or MODE_DYNAMIC enumerated values')
        self.__mode = value

    def to3GPPObject(self) -> Tuple[DistributionNetworkType,DistributionMode]:
        return (self.__network_type, self.__mode)

    @classmethod
    def from3GPPObject(cls, obj: Tuple[DistributionNetworkType,DistributionMode]):
        if not isinstance(obj, list):
            obj = list(obj)
        return cls(*obj)
