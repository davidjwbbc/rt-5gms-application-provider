#!/usr/bin/python3 
#==============================================================================
# 5G-MAG Reference Tools: MediaSessionDeltaOperation class
#==============================================================================
#
# File: rt_media_configuration/delta_operations/media_session.py
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
5G-MAG Reference Tools: MediaSessionDeltaOperation Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaSessionDeltaOperation class which can holds
information about changes to a MediaSession in a MediaConfiguration.
'''
from typing import Optional

from rt_m1_client.session import M1Session
from rt_m1_client.types import (PROVISIONING_SESSION_TYPE_DOWNLINK,
                                PROVISIONING_SESSION_TYPE_UPLINK)

from ..media_session import MediaSession

from .delta_operation import DeltaOperation
from .media_entry import MediaEntryDeltaOperation
from .media_server_certificate import MediaServerCertificateDeltaOperation
from .media_consumption_reporting import MediaConsumptionReportingDeltaOperation
from .media_metrics_reporting import MediaMetricsReportingDeltaOperation
from .media_dynamic_policy import MediaDynamicPolicyDeltaOperation

class MediaSessionDeltaOperation(DeltaOperation):
    '''DeltaOperation for a MediaSession
    '''

    def __init__(self, config: "MediaConfiguration", *, add: Optional[MediaSession] = None,
                 remove: Optional[MediaSession] = None):
        from ..media_configuration import MediaConfiguration
        if (add is None and remove is None) or (add is not None and remove is not None):
            raise ValueError('MediaSessionDeltaOperation must be initialised as an "add" or "remove" operation')
        if add is not None:
            super().__init__(add)
        else:
            super().__init__(remove)
        self.__config = config
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

    async def apply_delta(self, m1_session: M1Session, update_container: bool = True) -> bool:
        if self.__is_add:
            prov_type = {True: PROVISIONING_SESSION_TYPE_DOWNLINK, False: PROVISIONING_SESSION_TYPE_UPLINK}[self.session.is_downlink]
            self.session.provisioning_session_id = await m1_session.provisioningSessionCreate(prov_type, self.session.external_app_id, self.session.asp_id)
            if self.session.provisioning_session_id is None:
                return False
            if self.session.certificates is not None:
                for cert_id,cert in self.session.certificates.items():
                    op = await MediaServerCertificateDeltaOperation(self.session, add=(cert_id,cert))
                    if not await op.apply_delta(m1_session, update_container=False):
                        return False
            if self.session.media_entry is not None:
                if not await (await MediaEntryDeltaOperation(self.session, add=self.session.media_entry)).apply_delta(m1_session, update_container=False):
                    return False
            if self.session.reporting_configurations is not None and self.session.reporting_configurations.consumption is not None:
                if not await (await MediaConsumptionReportingDeltaOperation(self.session, add=self.session.reporting_configurations.consumption)).apply_delta(m1_session, update_container=False):
                    return False
            if self.session.reporting_configurations is not None and self.session.reporting_configurations.metrics is not None:
                for mr in self.session.reporting_configurations.metrics:
                    op = await MediaMetricsReportingDeltaOperation(self.session, add=mr)
                    if not await op.apply_delta(m1_session, update_container=False):
                        return False
            if self.session.dynamic_policies is not None:
                for dp_id, dp in self.session.dynamic_policies.items():
                    if dp.id is None:
                        dp.id = dp_id
                    op = await MediaDynamicPolicyDeltaOperation(self.session, add=dp)
                    if not await op.apply_delta(m1_session, update_container=False):
                        return False
            if update_container:
                self.__config.addMediaSession(self.session)
        else:
            if not await m1_session.provisioningSessionDestroy(self.session.identity()):
                return False
            if update_container:
                return self.__config.removeMediaSession(entry=self.session)
        return True
