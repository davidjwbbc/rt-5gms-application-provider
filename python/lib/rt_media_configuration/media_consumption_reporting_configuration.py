# 5G-MAG Reference Tools: MediaConsumptionReportingConfiguration class
#==============================================================================
#
# File: rt_media_configuration/media_consumption_reporting_configuration.py
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
5G-MAG Reference Tools: MediaConsumptionReportingConfiguration Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaConsumptionReportingConfiguration class which
models the configuration parameters for consumption reporting.
'''

import json
from typing import Optional, Final, List, Type, Any, TypedDict

from rt_m1_client.types import ConsumptionReportingConfiguration

class MediaConsumptionReportingConfiguration:
    '''MediaConsumptionReportingConfiguration class
============================================
This class models the consumption reporting configuration parameters.
'''

    def __init__(self, reporting_interval: Optional[int] = None, sample_percentage: Optional[float] = None, location_reporting: Optional[bool] = None, access_reporting: Optional[bool] = None):
        self.reporting_interval = reporting_interval
        self.sample_percentage = sample_percentage
        self.location_reporting = location_reporting
        self.access_reporting = access_reporting

    def __await__(self):
        return self.__asyncInit().__await__()

    async def __asyncInit(self):
        '''Asynchronous object instantiation
        :meta private:
        :return: self
        '''
        return self

    def __eq__(self, other: "MediaConsumptionReportingConfiguration") -> bool:
        if self.__reporting_interval != other.__reporting_interval:
            return False
        if self.__sample_percentage != other.__sample_percentage:
            return False
        if self.__location_reporting != other.__location_reporting:
            return False
        return self.__access_reporting == other.__access_reporting

    def __ne__(self, other: "MediaConsumptionReportingConfiguration") -> bool:
        return not (self == other)

    def __repr__(self) -> str:
        '''Python constructor string for this object'''
        ret = f'{self.__class__.__name__}('
        np = ""
        if self.__reporting_interval is not None:
            ret += f'reporting_interval={self.__reporting_interval!r}'
            np = ", "
        if self.__sample_percentage is not None:
            ret += f'{np}sample_percentage={self.__sample_percentage!r}'
            np = ", "
        if self.__location_reporting is not None:
            ret += f'{np}location_reporting={self.__location_reporting!r}'
            np = ", "
        if self.__access_reporting is not None:
            ret += f'{np}access_reporting={self.__access_reporting!r}'
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
    def deserialise(json_obj: str) -> "MediaConsumptionReportingConfiguration":
        try:
            obj = json.loads(json_obj)
        except json.JSONDecodeError:
            raise ValueError("Bad JSON")
        return MediaConsumptionReportingConfiguration.fromJSONObject(obj)

    @staticmethod
    def fromJSONObject(obj: dict) -> "MediaConsumptionReportingConfiguration":
        kwargs = {}
        for k,v in obj.items():
            if k == 'reportingInterval':
                kwargs['reporting_interval'] = v
            elif k == 'samplePercentage':
                kwargs['sample_percentage'] = v
            elif k == 'locationReporting':
                kwargs['location_reporting'] = v
            elif k == 'accessReporting':
                kwargs['access_reporting'] = v
            else:
                raise TypeError(f'MediaConsumptionReportingConfiguration: JSON field "{k}" not understood')
        return MediaConsumptionReportingConfiguration(**kwargs)

    def jsonObject(self) -> dict:
        obj = {}
        if self.__reporting_interval is not None:
            obj['reportingInterval'] = self.__reporting_interval
        if self.__sample_percentage is not None:
            obj['samplePercentage'] = self.__sample_percentage
        if self.__location_reporting is not None:
            obj['locationReporting'] = self.__location_reporting
        if self.__access_reporting is not None:
            obj['accessReporting'] = self.__access_reporting
        return obj

    @property
    def reporting_interval(self):
        return self.__reporting_interval

    @reporting_interval.setter
    def reporting_interval(self, value: Optional[int]):
        if value is not None:
            if not isinstance(value, int):
                raise TypeError('MediaConsumptionReportingConfiguration.reporting_interval must be an int or None')
            if value <= 0:
                raise ValueError('MediaConsumptionReportingConfiguration.reporting_interval must be an int greater than 0')
        self.__reporting_interval = value

    @property
    def sample_percentage(self):
        return self.__sample_percentage

    @sample_percentage.setter
    def sample_percentage(self, value: Optional[float]):
        if value is not None:
            if isinstance(value, int):
                value = float(value)
            if not isinstance(value, float):
                raise TypeError('MediaConsumptionReportingConfiguration.sample_percentage must be a float or None')
            if value < 0.0 or value > 100.0:
                raise ValueError('MediaConsumptionReportingConfiguration.sample_percentage must be between 0.0 and 100.0 inclusive')
        self.__sample_percentage = value

    @property
    def location_reporting(self):
        return self.__location_reporting

    @location_reporting.setter
    def location_reporting(self, value: Optional[bool]):
        if value is not None:
            if not isinstance(value,bool):
                value = bool(value)
        self.__location_reporting = value

    @property
    def access_reporting(self):
        return self.__access_reporting

    @access_reporting.setter
    def access_reporting(self, value: Optional[bool]):
        if value is not None:
            if not isinstance(value,bool):
                value = bool(value)
        self.__access_reporting = value

    __conv_3gpp: Final[List[TypedDict('3GPPConversion', {'param': str, 'field': str, 'cls': Type, 'mandatory': bool})]] = [
        {'param': 'reporting_interval', 'field': 'reportingInterval', 'cls': int, 'mandatory': False},
        {'param': 'sample_percentage', 'field': 'samplePercentage', 'cls': float, 'mandatory': False},
        {'param': 'location_reporting', 'field': 'locationReporting', 'cls': bool, 'mandatory': False},
        {'param': 'access_reporting', 'field': 'accessReporting', 'cls': bool, 'mandatory': False},
    ]

    @classmethod
    async def from3GPPObject(cls, crc: ConsumptionReportingConfiguration) -> "MediaConsumptionReportingConfiguration":
        args = []
        kwargs = {}
        for cnv in cls.__conv_3gpp:
            if cnv['mandatory']:
                args += [await cls.doConversion(crc[cnv['field']],cnv['cls'],'from3GPPObject')]
            elif cnv['field'] in crc:
                kwargs[cnv['param']] = await cls.doConversion(crc[cnv['field']],cnv['cls'],'from3GPPObject')
        return await cls(*args, **kwargs)

    async def to3GPPObject(self, session: "MediaSession") -> ConsumptionReportingConfiguration:
        from .media_session import MediaSession
        ret = {}
        for cnv in self.__conv_3gpp:
            v = getattr(self, cnv['param'], None)
            if v is not None:
                ret[cnv['field']] = await self.doConversion(v, cnv['cls'], 'to3GPPObject', session)
        return ConsumptionReportingConfiguration(ret)

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
