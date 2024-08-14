#!/usr/bin/python3 
#==============================================================================
# 5G-MAG Reference Tools: MediaEntry class
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
5G-MAG Reference Tools: MediaEntry Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaEntry class which models a 3GPP TS 26.512
ProvisioningSession with ContentHostingConfiguration, but also extends this
model by allowing further named media distribution points to be added which
will only be published via M8.
'''

import json
from typing import Optional, List, Dict, Iterable

from .media_dynamic_policy import MediaDynamicPolicy
from .media_distribution import MediaDistribution
from .media_reporting_configuration import MediaReportingConfiguration
from .media_consumption_reporting_configuration import MediaConsumptionReportingConfiguration
from .media_metrics_reporting_configuration import MediaMetricsReportingConfiguration

class MediaEntry:
    '''MediaEntry class
================
This class models a 3GPP TS 26.512 ProvisioningSession with ContentHostingConfiguration, but also extends this model by allowing
further named media distribution points to be added. The ProvisioningSession information will be published via M5 but the extended
media distributions information will only be published via M8.
'''

    def __init__(self, name: str, ingest_url_prefix: str, distributions: Iterable[MediaDistribution],
                 app_distributions: Optional[Iterable[MediaDistribution]] = None,
                 reporting_configurations: Optional[MediaReportingConfiguration] = None,
                 dynamic_policies: Optional[Dict[str,MediaDynamicPolicy]] = None):
        '''Constructor

        When this object is synchronised with the 5GMS AF it will gain a `provisioning_session_id` attribute.

        :param name: The name of the media entry which may appear in the App.
        :param ingest_url: The ingest URL prefix for this media entry.
        :param distributions: A list of MediaDistributions (min. 1 entry) to directly attach to be published via M5.
        :param app_distributions: An optional list of MediaDistributions to attach to the media entry to be published via M8.
        :param reporting_configurations: The reporting configurations to use with this media entry for publication via M5.
        :param dynamic_policies: The QoS dynamic policies to attach to this media entry for publication via M5.
        :return: A new MediaEntry object attached to this MediaConfiguration.
        '''
        self.provisioning_session_id = None
        self.name = name
        self.ingest_url_prefix = ingest_url_prefix
        self.distributions = distributions
        self.app_distributions = app_distributions
        self.reporting_configurations = reporting_configurations
        self.dynamic_policies = dynamic_policies
        
    def __await__(self):
        return self.__asyncInit().__await__()

    def __eq__(self, other: "MediaEntry") -> bool:
        if (self.__name != other.__name):
            return False
        if (self.__ingest_url_prefix != other.__ingest_url_prefix):
            return False
        if (len(self.__distributions) != len(other.__distributions)):
            return False
        if (len(self.__app_distributions) != len(other.__app_distributions)):
            return False
        if (sorted(self.__distributions) != sorted(other.__distributions)):
            return False
        if (sorted(self.__app_distributions) != sorted(other.__app_distributions)):
            return False
        if (self.__reporting_configurations != other.__reporting_configurations):
            return False
        return (self.__dynamic_policies == other.__dynamic_policies)

    def __ne__(self, other: "MediaEntry") -> bool:
        return not (self == other)

    def __repr__(self) -> str:
        '''Python constructor string for this object'''
        ret = f'{self.__class__.__name__}({self.__name!r}, {self.__ingest_url_prefix!r}, {self.__distributions!r}'
        if self.__app_distributions is not None and len(self.__app_distributions) > 0:
            ret += f', app_distributions={self.__app_distributions!r}'
        if self.__reporting_configurations is not None and (self.__reporting_configurations.consumption is not None or (self.__reporting_configurations.metrics is not None and len(self.__reporting_configurations.metrics) > 0)):
            ret += f', reporting_configurations={self.__reporting_configurations!r}'
        if self.__dynamic_policies is not None and len(self.__dynamic_policies) > 0:
            ret += f', dynamic_policies={self.__dynamic_policies!r}'
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
    def deserialise(json_obj: str) -> "MediaEntry":
        try:
            obj = json.loads(json_obj)
        except json.JSONDecodeError:
            raise ValueError("Bad JSON")

        return MediaEntry._fromJSONObject(obj)

    @staticmethod
    def _fromJSONObject(obj: dict) -> "MediaEntry":
        if "name" not in obj or "ingestURL" not in obj or "distributionConfigurations" not in obj or len(obj["distributionConfigurations"]) < 1:
            raise ValueError("Missing mandatory fields")

        kwargs = {}
        reporting = None
        if "consumptionReporting" in obj:
            reporting = MediaReportingConfiguration()
            reporting.consumption = MediaConsumptionReportingConfiguration._fromJSONObject(obj["consumptionReporting"])
            kwargs["reporting_configurations"] = reporting
        if "metricsReporting" in obj:
            mr_objs = obj["metricsReporting"]
            if reporting is None:
                reporting = MediaReportingConfiguration()
                kwargs["reporting_configurations"] = reporting
            for mr_obj in mr_objs:
                reporting.addMetricsReporting(MediaMetricsReportingConfiguration._fromJSONObject(mr_obj))
        if "policies" in obj:
            kwargs["dynamic_policies"] = {}
            for extId, policy in obj["policies"].items():
                kwargs["dynamic_policies"][extId] = MediaDynamicPolicy._fromJSONObject(policy)
        if "appDistributions" in obj:
            kwargs["app_distributions"] = []
            for app_dist_obj in obj["appDistributions"]:
                kwargs["app_distributions"] += [MediaDistribution._fromJSONObject(app_dist_obj)]
        dcs = []
        for dc_obj in obj["distributionConfigurations"]:
            dcs += [MediaDistribution._fromJSONObject(dc_obj)]
        return MediaEntry(obj["name"], obj["ingestURL"], dcs, **kwargs)

    def _jsonObject(self) -> dict:
        obj = {"name": self.__name, "ingestURL": self.__ingest_url_prefix, "distributionConfiguration": self.__distributions}
        if self.__app_distributions is not None and len(self.__app_distributions) > 0:
            obj["appDistributions"] = self.__app_distributions
        if self.__reporting_configurations is not None:
            if self.__reporting_configurations.consumption is not None:
                obj['consumptionReporting'] = self.__reporting_configurations.consumption
            if self.__reporting_configurations.metrics is not None and len(self.__reporting_configurations.metrics) > 0:
                obj['metricsReporting'] = self.__reporting_configurations.metrics
        if self.__dynamic_policies is not None and len(self.__dynamic_policies) > 0:
            obj['policies'] = self.__dynamic_policies
        return obj

    async def __asyncInit(self):
        '''Asynchronous object instantiation
        :meta private:
        :return: self
        '''
        return self

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError('MediaEntry.name must be a str')
        if len(value) == 0:
            raise ValueError('MediaEntry.name must be a non-empty string')
        self.__name = value

    @property
    def ingest_url_prefix(self) -> str:
        return self.__ingest_url_prefix

    @ingest_url_prefix.setter
    def ingest_url_prefix(self, value: str):
        if not isinstance(value, str):
            raise TypeError('MediaEntry.ingest_url_prefix must be a str')
        if len(value) == 0:
            raise ValueError('MediaEntry.ingest_url_prefix must be a non-empty string')
        self.__ingest_url_prefix = value

    @property
    def distributions(self) -> List[MediaDistribution]:
        return self.__distributions

    @distributions.setter
    def distributions(self, value: Iterable[MediaDistribution]):
        if not isinstance(value,list):
            value = list(value)
        if len(value) == 0 or not all(isinstance(v, MediaDistribution) for v in value):
            raise ValueError('MediaEntry.distributions must be a non-empty list of MediaDistribution objects')
        self.__distributions = value

    def addDistribution(self, value: MediaDistribution):
        if not isinstance(value,MediaDistribution):
            raise TypeError('MediaEntry.distributions can only contain MediaDistribution objects')
        self.__distributions += [value]

    def removeDistribution(self, value: MediaDistribution) -> bool:
        if len(self.__distributions) == 1 and value in self.__distributions:
            raise ValueError('MediaEntry.distributions must hold at least one MediaDistribution object')
        try:
            self.__distributions.remove(value)
        except ValueError:
            return False
        return True

    @property
    def app_distributions(self) -> Optional[List[MediaDistribution]]:
        return self.__app_distributions

    @app_distributions.setter
    def app_distributions(self, value: Optional[Iterable[MediaDistribution]]):
        if value is not None:
            if not isinstance(value, list):
                value = list(value)
            if not all(isinstance(v, MediaDistribution) for v in value):
                raise ValueError('MediaEntry.app_distributions list must only contain MediaDistribution objects')
            if len(value) == 0:
                value = None
        self.__app_distributions = value

    def addAppDistribution(self, value: MediaDistribution):
        if not isinstance(value,MediaDistribution):
            raise TypeError('MediaEntry.app_distributions can only contain MediaDistribution objects')
        if self.__app_distributions is None:
            self.__app_distributions = []
        self.__app_distributions += [value]

    def removeAppDistribution(self, value: MediaDistribution) -> bool:
        if self.__app_distributions is None:
            return False
        try:
            self.__app_distributions.remove(value)
        except ValueError:
            return False
        if len(self.__app_distributions) == 0:
            self.__app_distributions = None
        return True

    @property
    def reporting_configurations(self) -> Optional[MediaReportingConfiguration]:
        return self.__reporting_configurations

    @reporting_configurations.setter
    def reporting_configurations(self, value: Optional[MediaReportingConfiguration]):
        if value is not None:
            if not isinstance(value,MediaReportingConfiguration):
                raise TypeError('MediaEntry.reporting_configurations can be either None or a MediaReportingConfiguration object')
            if value.consumption is None and (value.metrics is None or len(value.metrics) == 0):
                value = None
        self.__reporting_configurations = value

    def setConsumptionReportingConfiguration(self, value: MediaConsumptionReportingConfiguration):
        if self.__reporting_configurations is None:
            self.__reporting_configurations = MediaReportingConfiguration()
        self.__reporting_configurations.consumption = value

    def unsetConsumptionReportingConfiguration(self):
        self.__reporting_configurations.consumption = None
        if self.__reporting_configurations.metrics is None or len(self.__reporting_configurations.metrics) == 0:
            self.__reporting_configurations = None

    def addMetricsReportingConfiguration(self, value: MediaMetricsReportingConfiguration):
        if self.__reporting_configurations is None:
            self.__reporting_configurations = MediaReportingConfiguration()
        self.__reporting_configurations.addMetricsReportingConfiguration(value)

    def removeMetricsReportingConfiguration(self, value: MediaMetricsReportingConfiguration) -> bool:
        if self.__reporting_configurations is None:
            return False
        ret = self.__reporting_configurations.removeMetricsReportingConfiguration(value)
        if self.__reporting_configurations.metrics is None and self.__reporting_configurations.consumption is None:
            self.__reporting_configurations = None
        return ret

    def unsetMetricsReportingConfigurations(self):
        self.__reporting_configurations = None

    @property
    def dynamic_policies(self) -> Optional[List[MediaDynamicPolicy]]:
        return self.__dynamic_policies

    @dynamic_policies.setter
    def dynamic_policies(self, value: Optional[Iterable[MediaDynamicPolicy]]):
        if value is not None:
            if not isinstance(value, list):
                value = list(value)
            if not all(isinstance(v, MediaDynamicPolicy) for v in value):
                raise TypeError('MediaEntry.dynamic_policies can only hold MediaDynamicPolicy objects')
            if len(value) == 0:
                value = None
        self.__dynamic_policies = value

    def addDynamicPolicy(self, value: MediaDynamicPolicy):
        if not isinstance(value, MediaDynamicPolicy):
            raise TypeError('MediaEntry.dynamic_policies can only hold MediaDynamicPolicy objects')
        if self.__dynamic_policies is None:
            self.__dynamic_policies = []
        self.__dynamic_policies += [value]

    def removeDynamicPolicy(self, value: MediaDynamicPolicy) -> bool:
        if self.__dynamic_policies is None:
            return False
        try:
            self.__dynamic_policies.remove(value)
        except ValueError:
            return False
        if len(self.__dynamic_policies) == 0:
            self.__dynamic_policies = None
        return True

    def unsetDynamicPolicies(self):
        self.__dynamic_policies = None
