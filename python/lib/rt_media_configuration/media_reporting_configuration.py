#!/usr/bin/python3 
#==============================================================================
# 5G-MAG Reference Tools: MediaReportingConfiguration class
#==============================================================================
#
# File: rt_media_configuration/media_reporting_configuration.py
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
5G-MAG Reference Tools: MediaReportingConfiguration Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaReportingConfiguration class which holds consumption
and mertics reporting configurations.
'''

import json
from typing import Optional, List, Iterable

from .media_consumption_reporting_configuration import MediaConsumptionReportingConfiguration
from .media_metrics_reporting_configuration import MediaMetricsReportingConfiguration

class MediaReportingConfiguration:
    '''MediaReportingConfiguration class
=================================
This class provides a model which contains an optional consumption reporting parameters
and a 0 or more metrics reporting parameters.
'''

    def __init__(self, consumption_reporting: Optional[MediaConsumptionReportingConfiguration] = None,
                 metrics_reporting: Optional[Iterable[MediaMetricsReportingConfiguration]] = None):
        self.consumption = consumption_reporting
        self.metrics = metrics_reporting

    def __await__(self):
        return self.__asyncInit().__await__()

    async def __asyncInit(self):
        '''Asynchronous object instantiation
        :meta private:
        :return: self
        '''
        return self

    def __eq__(self, other: "MediaReportingConfiguration") -> bool:
        if self.__consumption != other.__consumption:
            return False
        return sorted(self.__metrics) == sorted(other.__metrics)

    def __ne__(self, other: "MediaEntry") -> bool:
        return not (self == other)

    def __repr__(self) -> str:
        '''Python constructor string for this object'''
        ret = f'{self.__class__.__name__}('
        np=""
        if self.__consumption is not None:
            ret += f'consumption_reporting={self.__consumption!r}'
            np = ", "
        if self.__metrics is not None and len(self.__metrics) > 0:
            ret += f'{np}metrics_reporting={self.__metrics!r}'
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
    def deserialise(json_obj: str) -> "MediaReportingConfiguration":
        try:
            obj = json.loads(json_obj)
        except json.JSONDecodeError:
            raise ValueError("Bad JSON")

        return MediaReportingConfiguration.fromJSONObject(obj)

    @staticmethod
    def fromJSONObject(obj: dict) -> "MediaReportingConfiguration":
        kwargs = {}
        for k,v in obj.items():
            if k == "consumptionReporting":
                kwargs['consumption_reporting'] = MediaConsumptionReportingConfiguration.fromJSONObject(v)
            elif k == "metricsReporting" and len(v) > 0:
                kwargs['metrics_reporting'] = [MediaMetricsReportingConfiguration.fromJSONObject(i) for i in v]
            else:
                raise TypeError(f'MediaReportingConfiguration: JSON field "{k}" not understood')
        return MediaReportingConfiguration(**kwargs)

    def jsonObject(self) -> dict:
        obj = {}
        if self.__consumption is not None:
            obj['consumptionReporting'] = self.__consumption
        if self.__metrics is not None and len(self.__metrics) > 0:
            obj['metricsReporting'] = self.__metrics
        return obj

    @property
    def consumption(self) -> Optional[MediaConsumptionReportingConfiguration]:
        return self.__consumption

    @consumption.setter
    def consumption(self, value: Optional[MediaConsumptionReportingConfiguration]):
        if value is not None:
            if not isinstance(value, MediaConsumptionReportingConfiguration):
                raise TypeError('MediaReportingConfiguration.consumption must be either None or a MediaConsumptionReportingConfiguration object')
        self.__consumption = value

    @property
    def metrics(self):
        return self.__metrics

    @metrics.setter
    def metrics(self, value: Optional[Iterable[MediaMetricsReportingConfiguration]]):
        if value is not None:
            if not isinstance(value, list):
                value = list(value)
            if not all(isinstance(v, MediaMetricsReportingConfiguration) for v in value):
                raise TypeError('MediaReportingConfiguration.metrics can only contain MediaMetricsReportingConfiguration objects')
            if len(value) == 0:
                value = None
        self.__metrics = value

    def addMetricsReporting(self, mr: MediaMetricsReportingConfiguration) -> None:
        if not isinstance(mr, MediaMetricsReportingConfiguration):
            raise TypeError('MediaReportingConfiguration.metrics can only contain MediaMetricsReportingConfiguration objects')
        if self.__metrics is None:
            self.__metrics = []
        self.__metrics += [mr]

    def removeMetricsReporting(self, mr: MediaMetricsReportingConfiguration) -> bool:
        if self.__metrics is None:
            return False
        try:
            self.__metrics.remove(mr)
        except ValueError:
            return False
        if len(self.__metrics) == 0:
            self.__metrics = None
        return True

    def unsetMetricsReporting(self):
        self.__metrics = None
