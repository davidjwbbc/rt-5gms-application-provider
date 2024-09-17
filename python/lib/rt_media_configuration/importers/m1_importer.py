#!/usr/bin/python3
#==============================================================================
# 5G-MAG Reference Tools: M1 Session
#==============================================================================
#
# File: rt_media_configuration/importers/m1_importer.py
# License: 5G-MAG Public License (v1.0)
# Author: David Waring
# Copyright: (C) 2024 British Broadcasting Corporation
#
# For full license terms please see the LICENSE file distributed with this
# program. If this file is missing then the license can be retrieved from
# https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
#
#==============================================================================
#
# This module provides the M1SessionImporter class to import the current state
# of the AF (via M1Session class and DataStore) into a MediaConfiguration.
'''5G-MAG Reference Tools: M1Session Importer module
=================================================

This module provides the M1SessionImporter class to import the current state
of the AF (via M1Session class and DataStore) into a MediaConfiguration.
'''

from typing import Optional, Union, Tuple

from rt_m1_client import M1Session, DataStore, CertificateSigner, PROVISIONING_SESSION_TYPE_DOWNLINK, ProvisioningSession

from ..media_session import MediaSession
from ..media_entry import MediaEntry
from ..media_distribution import MediaDistribution
from ..media_entry_point import MediaEntryPoint

from .importer import MediaConfigurationImporter

class M1SessionImporter(MediaConfigurationImporter):
    '''M1SessionImporter class
=======================
This class reads the current configuration, via M1Session, from the AF and
supplementary information from the DataStore and uses it to populate a
MediaConfiguration model.
    '''

    def __init__(self, authority_or_session: Union[Tuple[str, int],M1Session], *, persistent_data_store: Optional[DataStore] = None, certificate_signer: Optional[Union[CertificateSigner,type,str]] = None):
        '''Constructor
        '''
        super().__init__()
        if isinstance(authority_or_session, M1Session):
            self.__authority = authority_or_session.authority()
            self.__data_store = authority_or_session.data_store()
            self.__certificate_signer = authority_or_session.certificate_signer()
            self.__session = authority_or_session
        else:
            if persistent_data_store is None:
                raise ValueError('M1SessionImporter must be given a DataStore when initialised with an authority tuple')
            self.__authority = authority_or_session
            self.__data_store = persistent_data_store
            self.__certificate_signer = certificate_signer
            self.__session = None
        self.__psid_to_id_map = {}

    async def _asyncInit(self):
        '''Asynchronous object instantiation

        :meta private:
        :return: self
        '''
        await super()._asyncInit()
        if self.__session is None:
            self.__session = await M1Session(self.__authority, persistent_data_store=self.__data_store, certificate_signer=self.__certificate_signer)
        await self.__loadFromDataStore()
        return self

    async def import_to(self, model: "MediaConfiguration") -> bool:
        '''Import the model into ``model``.
        '''
        await model.reset()
        provisioning_ids = await self.__session.provisioningSessionIds()
        for psid in provisioning_ids:
            ps = await self.__session.provisioningSessionGet(psid)
            if ps is not None:
                session = await MediaSession(ps['provisioningSessionType']==PROVISIONING_SESSION_TYPE_DOWNLINK, ps['appId'], provisioning_session_id=psid, asp_id=ps.get('aspId',None))
                await model.addMediaSession(session)
                chc = await self.__session.provisioningSessionContentHostingConfiguration(psid)
                if chc is not None:
                    dcs = [await MediaDistribution.from3GPPObject(dc) for dc in chc['distributionConfigurations']]
                    entry = await MediaEntry(chc['name'], chc['ingestConfiguration']['baseURL'], dcs)
                    # TODO: Add AppDistributions from DataStore map
                    entry.id = self.__psid_to_id_map.get(psid, psid)
                    entry.provisioning_session_id = psid
                    session.media_entry = entry
        return True

    async def __loadFromDataStore(self):
        self.__psid_to_id_map = await self.__data_store.get('media-configuration-psid-map', {})
