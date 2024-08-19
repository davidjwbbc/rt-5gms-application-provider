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

from rt_m1_client import M1Session, DataStore, CertificateSigner

from .importer import MediaConfigurationImporter

class M1SessionImporter(MediaConfigurationImporter):
    '''M1SessionImporter class
=======================
This class reads the current configuration, via M1Session, from the AF and
supplementary information from the DataStore and uses it to populate a
MediaConfiguration model.
    '''

    def __init__(self, authority: Tuple[str, int], persistent_data_store: DataStore, *, certificate_signer: Optional[Union[CertificateSigner,type,str]] = None):
        '''Constructor
        '''
        super().__init__()
        self.__authority = authority
        self.__data_store = persistent_data_store
        self.__certificate_signer = certificate_signer
        self.__psid_to_id_map = {}
        self.__session = None

    async def _asyncInit(self):
        '''Asynchronous object instantiation

        :meta private:
        :return: self
        '''
        await super()._asyncInit()
        self.__session = await M1Session(self.__authority, persistent_data_store=self.__data_store, certificate_signer=self.__certificate_signer)
        await self.__loadFromDataStore()
        return self

    async def import_to(self, model: "MediaConfiguration") -> bool:
        '''Import the model into ``model``.
        '''
        await model.reset()
        provisioning_ids = await self.__session.provisioningSessionIds()
        for psid in provisioning_ids:
            chc = await self.__session.provisioningSessionContentHostingConfiguration(psid)
            if chc is not None:
                dcs = []
                for dc in chc['distributionConfigurations']:
                    media_distrib = await MediaDistribution(domain_name_alias=dc.get('domainNameAlias', None), certificate_id=dc.get('certificateId', None))
                    if 'entryPoint' in dc:
                        media_distrib.entry_point = await MediaEntryPoint(relative_path=dc['entryPoint'].get('relativePath', None),
                                                                          content_type=dc['entryPoint'].get('contentType', None),
                                                                          profiles=dc['entryPoint'].get('profiles', None))
                    dcs += [media_distrib]
                entry = await MediaEntry(chc['name'], chc['ingestConfiguration']['baseURL'], dcs)
                # TODO: Add AppDistributions from DataStore map
                entry.id = self.__psid_to_id_map.get(psid, psid)
                entry.provisioning_session_id = psid
                await model.addMediaEntry(entry.id, entry)
        return True

    async def __loadFromDataStore(self):
        self.__psid_to_id_map = await self.__data_store.get('media-configuration-psid-map', {})
