# 5G-MAG Reference Tools: MediaMetricsReportingConfiguration class
#==============================================================================
#
# File: rt_media_configuration/media_metrics_reporting_configuration.py
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
5G-MAG Reference Tools: MediaMetricsReportingConfiguration Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaMetricsReportingConfiguration class to model
metrics reporting configuration parameters.
'''

import json
from typing import Optional

class MediaMetricsReportingConfiguration:
    '''MediaMetricsReportingConfiguration class
========================================
This class models the configuration parameters for metrics reporting.
'''

    def __init__(self, scheme: Optional[str] = None, reporting_interval: Optional[int] = None, sample_percentage: Optional[float] = None, sampling_period: Optional[int] = None):
        self.scheme = scheme
        self.reporting_interval = reporting_interval
        self.sample_percentage = sample_percentage
        self.sampling_period = sampling_period

    def __await__(self):
        return self.__asyncInit().__await__()

    async def __asyncInit(self):
        '''Asynchronous object instantiation
        :meta private:
        :return: self
        '''
        return self

    def __eq__(self, other: "MediaMetricsReportingConfiguration") -> bool:
        if self.__reporting_interval != other.__reporting_interval:
            return False
        if self.__sampling_period != other.__sampling_period:
            return False
        if self.__sample_percentage != other.__sample_percentage:
            return False
        return self.__scheme == other.__scheme

    def __ne__(self, other: "MediaMetricsReportingConfiguration") -> bool:
        return not (self == other)

    def __repr__(self) -> str:
        '''Python constructor string for this object'''
        ret = f'{self.__class__.__name__}('
        np = ''
        if self.__scheme is not None:
            ret += f'scheme={self.__scheme!r}'
            np = ', '
        if self.__reporting_interval is not None:
            ret += f'{np}reporting_interval={self.__reporting_interval!r}'
            np = ', '
        if self.__sample_percentage is not None:
            ret += f'{np}sample_percentage={self.__sample_percentage!r}'
            np = ', '
        if self.__sampling_period is not None:
            ret += f'{np}sampling_period={self.__sampling_period!r}'
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
    def deserialise(json_obj: str) -> "MediaMetricsReportingConfiguration":
        try:
            obj = json.loads(json_obj)
        except json.JSONDecodeError:
            raise ValueError("Bad JSON")
        return MediaMetricsReportingConfiguration.fromJSONObject(obj)

    @staticmethod
    def fromJSONObject(obj: dict) -> "MediaMetricsReportingConfiguration":
        kwargs = {}
        for k,v in obj.items():
            if k == 'scheme':
                kwargs['scheme'] = v
            elif k == 'reportingInterval':
                kwargs['reporting_interval'] = v
            elif k == 'samplePercentage' in obj:
                kwargs['sample_percentage'] = v
            elif k == 'samplingPeriod' in obj:
                kwargs['sampling_period'] = v
            else:
                raise TypeError(f'MediaMetricsReportingConfiguration: JSON field "{k}" not understood')
        return MediaMetricsReportingConfiguration(**kwargs)

    def jsonObject(self) -> dict:
        obj = {}
        if self.__scheme is not None:
            obj['scheme'] = self.__scheme
        if self.__reporting_interval is not None:
            obj['reportingInterval'] = self.__reporting_interval
        if self.__sample_percentage is not None:
            obj['samplePercentage'] = self.__sample_percentage
        if self.__sampling_period is not None:
            obj['samplingPeriod'] = self.__sampling_period
        return obj

    @property
    def scheme(self) -> Optional[str]:
        return self.__scheme

    @scheme.setter
    def scheme(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value,str):
                raise TypeError('MediaMetricsReportingConfiguration.scheme must be a str or None')
        self.__scheme = value

    @property
    def reporting_interval(self) -> Optional[int]:
        return self.__reporting_interval

    @reporting_interval.setter
    def reporting_interval(self, value: Optional[int]):
        if value is not None:
            if not isinstance(value, int):
                raise TypeError('MediaMetricsReportingConfiguration.reporting_interval must be an int or None')
            if value < 0:
                raise ValueError('MediaMetricsReportingConfiguration.reporting_interval must be None or an int greater than 0')
            if value == 0:
                value = None
        self.__reporting_interval = value

    @property
    def sample_percentage(self) -> Optional[float]:
        return self.__sample_percentage

    @sample_percentage.setter
    def sample_percentage(self, value: Optional[float]):
        if value is not None:
            if isinstance(value, int):
                value = float(value)
            if not isinstance(value, float):
                raise TypeError('MediaMetricsReportingConfiguration.sample_percentage must be a float or None')
            if value < 0.0 or value > 100.0:
                raise ValueError('MediaMetricsReportingConfiguration.sample_percentage must be between 0.0 and 100.0 inclusive')
        self.__sample_percentage = value

    @property
    def sampling_period(self) -> Optional[int]:
        return self.__sampling_period

    @sampling_period.setter
    def sampling_period(self, value: Optional[int]):
        if value is not None:
            if not isinstance(value, int):
                raise TypeError('MediaMetricsReportingConfiguration.sampling_period must be an int or None')
            if value < 0:
                raise ValueError('MediaMetricsReportingConfiguration.sampling_period must be None or an int greater than 0')
            if value == 0:
                value = None
        self.__sampling_period = value
