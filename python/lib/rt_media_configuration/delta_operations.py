#!/usr/bin/python3 
#==============================================================================
# 5G-MAG Reference Tools: DeltaOperation classes
#==============================================================================
#
# File: rt_media_configuration/media_configuration.py
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
5G-MAG Reference Tools: DeltaOperation Classes
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the DeltaOperation classes which identify operations
needed to change one MediaConfiguration into another MediaConfiguration.
'''
from typing import Optional

from rt_m1_client.session import M1Session
from rt_m1_client.types import (DistributionConfiguration,
                                M1MediaEntryPoint,
                                PROVISIONING_SESSION_TYPE_DOWNLINK,
                                PROVISIONING_SESSION_TYPE_UPLINK)

from .media_session import MediaSession
from .media_entry import MediaEntry
from .media_entry_point import MediaEntryPoint
from .media_distribution import MediaDistribution

class DeltaOperation:
    '''Interface class for DeltaOperation classes
    '''

    def __init__(self, session: MediaSession):
        self.session = session

    def __await__(self):
        return self._asyncInit().__await__

    async def _asyncInit(self):
        return self

    def __str__(self):
        raise NotImplementedError('DeltaOperation str operation must be implemented')

    def __repr__(self):
        return f'{self.__class__.__name__}(session={self.session!r})'

    async def apply_delta(self, m1_session: M1Session) -> bool:
        '''Apply this delta to the session via M1Session
        '''
        raise NotImplementedError('DeltaOperation apply_delta method must be implemented')

class MediaSessionDeltaOperation(DeltaOperation):
    '''DeltaOperation for a MediaSession
    '''

    def __init__(self, *, add: Optional[MediaSession] = None,
                 remove: Optional[MediaSession] = None):
        if (add is None and remove is None) or (add is not None and remove is not None):
            raise ValueError('MediaSessionDeltaOperation must be initialised as an "add" or "remove" operation')
        if add is not None:
            super().__init__(add)
        else:
            super().__init__(remove)
        self.__is_add = add is not None

    def __str__(self):
        if self.__is_add:
            return f'Add ProvisioningSession "{self.session.identity()}"'
        return f'Remove ProvisioningSession "{self.session.identity()}"'

    def __repr__(self):
        ret = f'{self.__class__.__name__}('
        if self.__is_add:
            ret += 'add='
        else:
            ret += 'remove='
        ret += f'{self.session!r})'
        return ret

    async def apply_delta(self, m1_session: M1Session) -> bool:
        prov_type = {True: PROVISIONING_SESSION_TYPE_DOWNLINK, False: PROVISIONING_SESSION_TYPE_UPLINK}[self.session.is_downlink]
        self.session.provisioning_session_id = await m1_session.provisioningSessionCreate(prov_type, self.session.external_app_id, self.session.asp_id)
        if self.session.provisioning_session_id is None:
            return False
        if self.session.media_entry is not None:
            if not await MediaEntryDeltaOperation(self.session, add=self.session.media_entry).apply_delta(m1_session):
                return False
        if self.session.reporting_configurations is not None and self.session.reporting_configurations.consumption is not None:
            if not await MediaConsumptionReportingDeltaOperation(self.session, add=self.session.reporting_configurations.consumption).apply_delta(m1_session):
                return False
        if self.session.reporting_configurations is not None and self.session.reporting_configurations.metrics is not None:
            for mr in self.session.reporting_configurations.metrics:
                if not await MediaMetricsReportingDeltaOperation(self.session, add=mr).apply_delta(m1_session):
                    return False
        if self.session.dynamic_policies is not None:
            for dp_id, dp in self.session.dynamic_policies.items():
                if not await MediaDynamicPolicyDeltaOperation(self.session, add=(dp_id, dp)).apply_delta(m1_session):
                    return False
        return True

class MediaEntryDeltaOperation(DeltaOperation):
    '''DeltaOperation for a MediaEntry
    '''

    def __init__(self, session: MediaSession, *, add: Optional[MediaEntry] = None, remove: bool = False):
        if (add is None and not remove) or (add is not None and remove):
            raise ValueError('MediaEntryDeltaOperation must be initialised as an "add" or "remove" operation')
        super().__init__(session)
        self.__media_entry = add
        self.__is_add = add is not None
        self.__is_remove = remove

    def __str__(self):
        if self.__is_add:
            return f'Add ContentHostingConfiguration to ProvisioningSession "{self.session.identity()}"'
        return f'Remove ContentHostingConfiguration from ProvisioningSession "{self.session.identity()}"'

    def __repr__(self):
        ret = f'{self.__class__.__name__}('
        if self.__is_add:
            ret += 'add={self.session!r}'
        else:
            ret += 'remove=True'
        ret += f')'
        return ret

    async def apply_delta(self, m1_session: M1Session) -> bool:
        if self.__is_remove:
            return await m1_session.contentHostingConfigurationRemove(self.session.provisioning_session_id)
        chc = {'name': self.__media_entry.name, 'ingestConfiguration': {'pull': self.session.is_pull, 'baseURL': self.__media_entry.ingest_url_prefix}, distributionConfigurations: [self.__distribution3GPPObject(dc) for dc in self.__media_entry.distributions]}
        await m1_session.contentHostingConfigurationCreate(self.session.provisioning_session_id, chc)

    @staticmethod
    def __distribution3GPPObject(distrib: MediaDistribution) -> DistributionConfiguration:
        ret = {}
        if distrib.domain_name_alias is not None:
            ret['domainNameAlias'] = ditrib.domain_name_alias
        if distrib.entry_point is not None:
            ret['entryPoint'] = self.__entryPoint3GPPObject(distrib.entry_point)
        if distrib.certificate_id is not None:
            ret['certificateId'] = distrib.certificate_id
        return ret

    @staticmethod
    def __entryPoint3GPPObject(entry_point: MediaEntryPoint) -> M1MediaEntryPoint:
        ret = {'relativePath': entry_point.relative_path, 'contentType': entry_point.content_type}
        if entry_point.profiles is not None:
            ret['profiles'] = entry_point.profiles
        return ret
