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
ContentHostingConfiguration, but also extends this model by allowing
further named media distribution points to be added which will only be
published via M8.
'''

import json
from typing import Optional, List, Dict, Iterable

from .media_app_distribution import MediaAppDistribution
from .media_distribution import MediaDistribution

class MediaEntry:
    '''MediaEntry class
================
This class models a 3GPP TS 26.512 ContentHostingConfiguration, but also extends this model by allowing further named media
distribution points to be added. The ProvisioningSession information will be published via M5 but the extended media distributions
information will only be published via M8.
'''

    def __init__(self, name: str, ingest_url_prefix: str, distributions: Iterable[MediaDistribution], is_pull: bool = True,
                 app_distributions: Optional[Iterable[MediaAppDistribution]] = None):
        '''Constructor

        When this object is synchronised with the 5GMS AF it will gain a `provisioning_session_id` attribute.

        :param name: The name of this media entry.
        :param ingest_url: The ingest URL prefix for this media entry.
        :param distributions: A list of MediaDistributions (min. 1 entry) to directly attach to be published via M5.
        :param is_pull: This media entry will pull media from the source.
        :param app_distributions: An optional list of MediaAppDistributions to attach to the media entry to be published via M8.
        :return: A new MediaEntry object attached to be attached to a MediaSession.
        '''
        self.name = name
        self.ingest_url_prefix = ingest_url_prefix
        self.distributions = distributions
        self.is_pull = is_pull
        self.app_distributions = app_distributions
        
    def __await__(self):
        return self.__asyncInit().__await__()

    def __eq__(self, other: "MediaEntry") -> bool:
        if (self.__name != other.__name):
            return False
        if (self.__ingest_url_prefix != other.__ingest_url_prefix):
            return False
        if (self.__is_pull != other.__is_pull):
            return False
        if (len(self.__distributions) != len(other.__distributions)):
            return False
        if (sorted(self.__distributions) != sorted(other.__distributions)):
            return False
        if self.__app_distributions is None and other.__app_distributions is not None:
            return False
        if self.__app_distributions is not None:
            if other.__app_distributions is None:
                return False
            if (len(self.__app_distributions) != len(other.__app_distributions)):
                return False
            return (sorted(self.__app_distributions) == sorted(other.__app_distributions))
        return True

    def __ne__(self, other: "MediaEntry") -> bool:
        return not (self == other)

    def __repr__(self) -> str:
        '''Python constructor string for this object'''
        ret = f'{self.__class__.__name__}({self.__name!r}, {self.__ingest_url_prefix!r}, {self.__distributions!r}'
        if not self.__is_pull:
            ret += ', is_pull=False'
        if self.__app_distributions is not None and len(self.__app_distributions) > 0:
            ret += f', app_distributions={self.__app_distributions!r}'
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

        return MediaEntry.fromJSONObject(obj)

    @staticmethod
    def fromJSONObject(obj: dict) -> "MediaEntry":
        kwargs = {}
        mand_fields = ['name', 'ingestURL', 'distributionConfigurations']
        name = None
        ingest_url = None
        dcs = None
        for k,v in obj.items():
            if k == 'name':
                name = v
                mand_fields.remove(k)
            if k == 'ingestURL':
                ingest_url = v
                mand_fields.remove(k)
            elif k == 'distributionConfigurations':
                dcs = [MediaDistribution.fromJSONObject(dc) for dc in v]
                mand_fields.remove(k)
            elif k == 'pull':
                kwargs['is_pull'] = v
            elif k == "appDistributions":
                kwargs["app_distributions"] = [MediaAppDistribution.fromJSONObject(app_dist_obj) for app_dist_obj in v]
            else:
                raise TypeError(f'MediaEntry: JSON field "{k}" not understood')
        if len(mand_fields) > 0:
            raise TypeError(f'MediaEntry: Mandatory JSON fields {mand_fields!r} are missing')
        return MediaEntry(name, ingest_url, dcs, **kwargs)

    def jsonObject(self) -> dict:
        obj = {"name": self.__name, "ingestURL": self.__ingest_url_prefix, "distributionConfiguration": self.__distributions}
        if not self.__is_pull:
            obj['pull'] = False
        if self.__app_distributions is not None and len(self.__app_distributions) > 0:
            obj["appDistributions"] = self.__app_distributions
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
    def is_pull(self) -> bool:
        return self.__is_pull

    @is_pull.setter
    def is_pull(self, value: bool):
        if not isinstance(value, bool):
            value = bool(value)
        self.__is_pull = value

    @property
    def app_distributions(self) -> Optional[List[MediaAppDistribution]]:
        return self.__app_distributions

    @app_distributions.setter
    def app_distributions(self, value: Optional[Iterable[MediaAppDistribution]]):
        if value is not None:
            if not isinstance(value, list):
                value = list(value)
            if not all(isinstance(v, MediaAppDistribution) for v in value):
                raise ValueError('MediaEntry.app_distributions list must only contain MediaAppDistribution objects')
            if len(value) == 0:
                value = None
        self.__app_distributions = value

    def addAppDistribution(self, value: MediaAppDistribution):
        if not isinstance(value,MediaAppDistribution):
            raise TypeError('MediaEntry.app_distributions can only contain MediaAppDistribution objects')
        if self.__app_distributions is None:
            self.__app_distributions = []
        self.__app_distributions += [value]

    def removeAppDistribution(self, value: MediaAppDistribution) -> bool:
        if self.__app_distributions is None:
            return False
        try:
            self.__app_distributions.remove(value)
        except ValueError:
            return False
        if len(self.__app_distributions) == 0:
            self.__app_distributions = None
        return True
