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
from typing import Optional, List, Iterable, Final, Type, Any, TypedDict

from rt_m1_client.types import MetricsReportingConfiguration

from .snssai import Snssai

class MediaMetricsReportingConfiguration:
    '''MediaMetricsReportingConfiguration class
========================================
This class models the configuration parameters for metrics reporting.
'''

    def __init__(self, sampling_period: int, metrics_reporting_configuration_id: Optional[str] = None,
                 slice_scope: Optional[Iterable[Snssai]] = None, scheme: Optional[str] = None,
                 data_network_name: Optional[str] = None, reporting_interval: Optional[int] = None,
                 sample_percentage: Optional[float] = None, url_filters: Optional[Iterable[str]] = None,
                 metrics: Optional[Iterable[str]] = None):
        self.sampling_period = sampling_period
        self.metrics_reporting_configuration_id = metrics_reporting_configuration_id
        self.slice_scope = slice_scope
        self.scheme = scheme
        self.data_network_name = data_network_name
        self.reporting_interval = reporting_interval
        self.sample_percentage = sample_percentage
        self.url_filters = url_filters
        self.metrics = metrics

    def __await__(self):
        return self.__asyncInit().__await__()

    async def __asyncInit(self):
        '''Asynchronous object instantiation
        :meta private:
        :return: self
        '''
        return self

    def __eq__(self, other: "MediaMetricsReportingConfiguration") -> bool:
        if self.__metrics_reporting_configuration_id != other.__metrics_reporting_configuration_id:
            return False
        if self.__reporting_interval != other.__reporting_interval:
            return False
        if self.__sampling_period != other.__sampling_period:
            return False
        if self.__sample_percentage != other.__sample_percentage:
            return False
        if self.__scheme != other.__scheme:
            return False
        if self.__data_network_name != other.__data_network_name:
            return False
        if self.__metrics is not None and other.__metrics is None:
            return False
        if self.__metrics is None and other.__metrics is not None:
            return False
        if self.__metrics is not None and sorted(self.__metrics) != sorted(other.__metrics):
            return False
        if self.__url_filters is not None and other.__url_filters is None:
            return False
        if self.__url_filters is None and other.__url_filters is not None:
            return False
        if self.__url_filters is not None and sorted(self.__url_filters) != sorted(other.__url_filters):
            return False
        if self.__slice_scope is not None and other.__slice_scope is None:
            return False
        if self.__slice_scope is None and other.__slice_scope is not None:
            return False
        if self.__slice_scope is None:
            return True
        return sorted(self.__slice_scope) == sorted(other.__slice_scope)

    async def shalloweq(self, other: "MediaMetricsReportingConfiguration") -> bool:
        if self.__metrics_reporting_configuration_id is not None and other.__metrics_reporting_configuration_id is not None and self.__metrics_reporting_configuration_id != other.__metrics_reporting_configuration_id:
            return False
        if self.__reporting_interval != other.__reporting_interval:
            return False
        if self.__sampling_period != other.__sampling_period:
            return False
        if self.__sample_percentage != other.__sample_percentage:
            return False
        if self.__scheme != other.__scheme:
            return False
        if self.__data_network_name != other.__data_network_name:
            return False
        if self.__metrics is not None and other.__metrics is None:
            return False
        if self.__metrics is None and other.__metrics is not None:
            return False
        if self.__metrics is not None and sorted(self.__metrics) != sorted(other.__metrics):
            return False
        if self.__url_filters is not None and other.__url_filters is None:
            return False
        if self.__url_filters is None and other.__url_filters is not None:
            return False
        if self.__url_filters is not None and sorted(self.__url_filters) != sorted(other.__url_filters):
            return False
        if self.__slice_scope is not None and other.__slice_scope is None:
            return False
        if self.__slice_scope is None and other.__slice_scope is not None:
            return False
        if self.__slice_scope is None:
            return True
        return sorted(self.__slice_scope) == sorted(other.__slice_scope)

    def __ne__(self, other: "MediaMetricsReportingConfiguration") -> bool:
        return not (self == other)

    def __repr__(self) -> str:
        '''Python constructor string for this object'''
        ret = f'{self.__class__.__name__}({self.__sampling_period!r}'
        if self.__metrics_reporting_configuration_id is not None:
            ret += f', metrics_reporting_configuration_id={self.__metrics_reporting_configuration_id!r}'
        if self.__slice_scope is not None:
            ret += f', slice_scope={self.__slice_scope!r}'
        if self.__scheme is not None:
            ret += f', scheme={self.__scheme!r}'
        if self.__reporting_interval is not None:
            ret += f', reporting_interval={self.__reporting_interval!r}'
        if self.__sample_percentage is not None:
            ret += f', sample_percentage={self.__sample_percentage!r}'
        if self.__data_network_name is not None:
            ret += f', data_network_name={self.__data_network_name!r}'
        if self.__metrics is not None and len(self.__metrics) > 0:
            ret += f', metrics={self.__metrics!r}'
        if self.__url_filters is not None and len(self.__url_filters) > 0:
            ret += f', url_filters={self.__url_filters!r}'
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
        mand_fields = ['samplingPeriod']
        sampling_period = None
        for k,v in obj.items():
            if k == 'scheme':
                kwargs['scheme'] = v
            elif k == 'reportingInterval':
                kwargs['reporting_interval'] = v
            elif k == 'samplePercentage' in obj:
                kwargs['sample_percentage'] = v
            elif k == 'samplingPeriod' in obj:
                sampling_period = v
                mand_fields.remove(k)
            elif k == 'metricsReportingConfigurationId':
                kwargs['metrics_reporting_configuration_id'] = v
            elif k == 'dataNetworkName':
                kwargs['data_network_name'] = v
            elif k == 'metrics':
                kwargs['metrics'] = v
            elif k == 'urlFilters':
                kwargs['url_filters'] = v
            elif k == 'sliceScope':
                kwargs['slice_scope'] = [Snssai.fromJSONObject(sns) for sns in v]
            else:
                raise TypeError(f'MediaMetricsReportingConfiguration: JSON field "{k}" not understood')
        if len(mand_fields) != 0:
            raise TypeError(f'MediaMetricsReportingConfiguration: mandatory fields {mand_fields!r} are missing')
        return MediaMetricsReportingConfiguration(sampling_period, **kwargs)

    def jsonObject(self) -> dict:
        obj = {'samplingPeriod': self.__sampling_period}
        if self.__scheme is not None:
            obj['scheme'] = self.__scheme
        if self.__reporting_interval is not None:
            obj['reportingInterval'] = self.__reporting_interval
        if self.__sample_percentage is not None:
            obj['samplePercentage'] = self.__sample_percentage
        if self.__metrics_reporting_configuration_id is not None:
            obj['metricsReportingConfigurationId'] = self.__metrics_reporting_configuration_id
        if self.__data_network_name is not None:
            obj['dataNetworkName'] = self.__data_network_name
        if self.__metrics is not None:
            obj['metrics'] = self.__metrics
        if self.__url_filters is not None:
            obj['urlFilters'] = self.__url_filters
        if self.__slice_scope is not None:
            obj['sliceScope'] = self.__slice_scope
        return obj

    @property
    def metrics_reporting_configuration_id(self) -> Optional[str]:
        return self.__metrics_reporting_configuration_id

    @metrics_reporting_configuration_id.setter
    def metrics_reporting_configuration_id(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeError('MediaMetricsReportingConfiguration.metrics_reporting_configuration_id must be either None or a str')
        self.__metrics_reporting_configuration_id = value

    @property
    def slice_scope(self) -> Optional[List[Snssai]]:
        return self.__slice_scope

    @slice_scope.setter
    def slice_scope(self, value: Optional[Iterable[Snssai]]):
        if value is not None:
            if not isinstance(value, list):
                value = list(value)
            if not all(isinstance(v, Snssai) for v in value):
                raise TypeError('MediaMetricsReportingConfiguration.metrics_reporting_configuration_id can only contain rt_media_configuration.Snssai')
            if len(value) == 0:
                value = None
        self.__slice_scope = value

    def addSliceScope(self, value: Snssai):
        if not isinstance(value, Snssai):
            raise TypeError('MediaMetricsReportingConfiguration.metrics_reporting_configuration_id can only contain rt_media_configuration.Snssai')
        if self.__slice_scope is None:
            self.__slice_scope = []
        self.__slice_scope += [value]

    def removeSliceScope(self, value: Snssai) -> bool:
        if self.__slice_scope is None:
            return False
        ret = self.__slice_scope.remove(value)
        if ret and len(self.__slice_scope) == 0:
            self.__slice_scope = None
        return ret

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
    def data_network_name(self) -> Optional[str]:
        return self.__data_network_name

    @data_network_name.setter
    def data_network_name(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeError('MediaMetricsReportingConfiguration.data_network_name must be a str or None')
        self.__data_network_name = value

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

    @property
    def url_filters(self) -> Optional[List[str]]:
        return self.__url_filters

    @url_filters.setter
    def url_filters(self, value: Optional[Iterable[str]]):
        if value is not None:
            if not isinstance(value, list):
                value = list(value)
            if not all(isinstance(v, str) for v in value):
                raise TypeError('MediaMetricsReportingConfiguration.url_filters can only hold str values')
            if len(value) == 0:
                value = None
        self.__url_filters = value

    @property
    def metrics(self) -> Optional[List[str]]:
        return self.__metrics

    @metrics.setter
    def metrics(self, value: Optional[Iterable[str]]):
        if value is not None:
            if not isinstance(value, list):
                value = list(value)
            if not all(isinstance(v, str) for v in value):
                raise TypeError('MediaMetricsReportingConfiguration.metrics can only hold str values')
            if len(value) == 0:
                value = None
        self.__metrics = value

    __conv_3gpp: Final[List[TypedDict('3GPPConversion', {'param': str, 'field': str, 'cls': Type, 'mandatory': bool})]] = [
        {'param': 'sampling_period', 'field': 'samplingPeriod', 'cls': int, 'mandatory': True},
        {'param': 'metrics_reporting_configuration_id', 'field': 'metricsReportingConfigurationId', 'cls': str, 'mandatory': False},
        {'param': 'slice_scope', 'field': 'sliceScope', 'cls': List[Snssai], 'mandatory': False},
        {'param': 'scheme', 'field': 'scheme', 'cls': str, 'mandatory': False},
        {'param': 'data_network_name', 'field': 'dataNetworkName', 'cls': str, 'mandatory': False},
        {'param': 'reporting_interval', 'field': 'reportingInterval', 'cls': int, 'mandatory': False},
        {'param': 'sample_percentage', 'field': 'samplePercentage', 'cls': float, 'mandatory': False},
        {'param': 'url_filters', 'field': 'urlFilters', 'cls': List[str], 'mandatory': False},
        {'param': 'metrics', 'field': 'metrics', 'cls': List[str], 'mandatory': False}
    ]

    @classmethod
    async def from3GPPObject(cls, cc: MetricsReportingConfiguration) -> "MediaMetricsReportingConfiguration":
        args = []
        kwargs = {}
        for cnv in cls.__conv_3gpp:
            if cnv['mandatory']:
                args += [await cls.doConversion(cc[cnv['field']],cnv['cls'],'from3GPPObject')]
            elif cnv['field'] in cc:
                kwargs[cnv['param']] = await cls.doConversion(cc[cnv['field']],cnv['cls'],'from3GPPObject')
        return await cls(*args, **kwargs)

    async def to3GPPObject(self, session: "MediaSession") -> MetricsReportingConfiguration:
        from .media_session import MediaSession
        ret = {}
        for cnv in self.__conv_3gpp:
            v = getattr(self, cnv['param'], None)
            if v is not None:
                ret[cnv['field']] = await self.doConversion(v, cnv['cls'], 'to3GPPObject', session)
        return MetricsReportingConfiguration(ret)

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

