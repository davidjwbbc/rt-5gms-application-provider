#!/usr/bin/python3 
#==============================================================================
# 5G-MAG Reference Tools: MediaEntryDeltaOperation class
#==============================================================================
#
# File: rt_media_configuration/delta_operations/media_entry.py
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
5G-MAG Reference Tools: MediaEntryDeltaOperation Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaEntryDeltaOperation class which holds operations
on MediaEntry objects needed to change one MediaConfiguration into another
MediaConfiguration.
'''
from typing import Optional

from rt_m1_client.session import M1Session
from rt_m1_client.types import (DistributionConfiguration,
                                M1MediaEntryPoint)

from ..media_session import MediaSession
from ..media_entry import MediaEntry
from ..media_entry_point import MediaEntryPoint
from ..media_distribution import MediaDistribution

from .delta_operation import DeltaOperation

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
        ret = super().__repr__()[:-1]
        if self.__is_add:
            ret += ', add={self.session!r}'
        else:
            ret += ', remove=True'
        ret += f')'
        return ret

    async def apply_delta(self, m1_session: M1Session, update_container: bool = True) -> bool:
        if self.__is_remove:
            if not await m1_session.contentHostingConfigurationRemove(self.session.provisioning_session_id):
                return False
            if update_container:
                self.session.media_entry = None
        elif self.__is_add:
            chc = {'name': self.__media_entry.name, 'ingestConfiguration': {'pull': self.__media_entry.is_pull, 'baseURL': self.__media_entry.ingest_url_prefix}, 'distributionConfigurations': [self.__distribution3GPPObject(dc, self.session) for dc in self.__media_entry.distributions]}
            if not await m1_session.contentHostingConfigurationCreate(self.session.provisioning_session_id, chc):
                return False
            if update_container:
                self.session.media_entry = self.__media_entry
        return True

    @staticmethod
    def __distribution3GPPObject(distrib: MediaDistribution, session: MediaSession) -> DistributionConfiguration:
        ret = {}
        if distrib.domain_name_alias is not None:
            ret['domainNameAlias'] = distrib.domain_name_alias
        if distrib.entry_point is not None:
            ret['entryPoint'] = MediaEntryDeltaOperation.__entryPoint3GPPObject(distrib.entry_point)
        if distrib.certificate_id is not None:
            cert = session.serverCertificateByIdent(distrib.certificate_id)
            if cert is not None:
                ret['certificateId'] = cert.identity()
            else:
                ret['certificateId'] = distrib.certificate_id
        return ret

    @staticmethod
    def __entryPoint3GPPObject(entry_point: MediaEntryPoint) -> M1MediaEntryPoint:
        ret = {'relativePath': entry_point.relative_path, 'contentType': entry_point.content_type}
        if entry_point.profiles is not None:
            ret['profiles'] = entry_point.profiles
        return ret
