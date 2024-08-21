#!/usr/bin/python3 
#==============================================================================
# 5G-MAG Reference Tools: MediaConfiguration class
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
5G-MAG Reference Tools: MediaConfiguration Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaConfiguration class which models a collection
of media assets and provides methods to manipulate the model and use the
rt_m1_client.M1Session object to synchronise that configuration with the
5GMS AF.
'''
import configparser
import json
import logging
from typing import Optional, Iterable, Dict, List
import uuid

import aiofiles

from rt_m1_client.configuration import Configuration
from rt_m1_client.session import M1Session
from rt_m1_client.data_store import DataStore

from .media_session import MediaSession
from .delta_operations import *

DEFAULT_CONFIG = '''[media-configuration]
m5_authority = example.com:7777
docroot = /var/cache/rt-5gms/as/docroots
default_docroot = /usr/share/nginx/html
'''

class MediaConfiguration:
    '''MediaConfiguration Class
========================
This class provides modelling for a collection of media assets and the
logic to use the rt_m1_client.M1Session object to synchronise that
configuration with the 5GMS AF.
'''

    def __init__(self, configfile: Optional[str] = None, asp_id: Optional[str] = None,
                 persistent_data_store: Optional[DataStore] = None):
        self.__outputs = []
        self.__model = {"sessions": {}, "aspId": None}
        self.asp_id = asp_id
        self.__extraConfigFile = configfile
        self.__config = Configuration()
        self.__config.addSection('media-configuration', DEFAULT_CONFIG, self.__extraConfigFile)
        self.__data_store = persistent_data_store
        self.__log = logging.getLogger(__name__ + '.' + self.__class__.__name__)
        self.__m1_session = None

    def __await__(self):
        '''``await`` provider for asynchronous instantiation.
        '''
        return self.__asyncInit().__await__()

    def __repr__(self) -> str:
        ret = f'{__name__}.{self.__class__.__name__}({self.__extraConfigFile!r}'
        if self.__model['aspId'] is not None:
            ret += f', asp_id={self.__model["aspId"]!r}'
        if self.__data_store is not None:
            ret += f', persistent_data_store={self.__data_store!r}'
        ret += ')'
        return ret

    def __str__(self) -> str:
        return self.serialise(pretty=True)

    def serialise(self, pretty: bool = False) -> str:
        obj = {'streams': self.__model["sessions"]}
        kwargs = {}
        if pretty:
            kwargs = {'sort_keys': True, 'indent': 2}
        if self.__model['aspId'] is not None:
            obj['aspId'] = self.__model['aspId']
        return json.dumps(obj, default=MediaConfiguration.jsonObjectHandler, **kwargs)

    async def reset(self) -> None:
        self.__model["sessions"] = {}

    async def restoreModel(self) -> bool:
        '''Restore the model to the last known configuration.

        Loads the current configuration from the 5GMS AF and supplements it
        with model configuration stored in the Datastore.

        :return: ``True`` if the model was successfully restored.
        '''
        try:
            m1_imp = await M1SessionImporter()
            m1_imp.import_to(self)
            await self.__loadModelFromDatastore()
        except Exception as exc:
            self.__log.error(f"Failed to restore model: {exc}")
            return False
        return True

    async def newMediaSession(self, *args, **kwargs) -> MediaSession:
        '''Create a new MediaSession and attach it to this MediaConfiguration

        :see: MediaSession constructor for parameters.
        :return: A new MediaSession object attached to this MediaConfiguration.
        '''
        entry = await MediaSession(*args, **kwargs)
        if entry.id is None:
            entry.id = str(uuid.uuid4())
        self.__model["sessions"][entry.id] = entry
        return entry
        
    async def addMediaSession(self, session: MediaSession) -> bool:
        if session.id is None:
            session.id = str(uuid.uuid4())
        self.__model["sessions"][session.id] = session
        return True

    async def removeMediaSession(self, *, session_id: Optional[str] = None, entry: Optional[MediaSession] = None) -> bool:
        if session_id is None and entry is None:
            return False
        if session_id is not None:
            if entry is not None:
                raise RuntimeError('MediaConfiguration.removeMediaEntry takes either session_id or entry, not both')
            if session_id not in self.__model["sessions"]:
                return False
            del self.__model["sessions"][session_id]
            return True
        else:
            for k,v in self.__model["sessions"]:
                if v == entry:
                    del self.__model["sessions"][k]
                    return True
        return False

    async def mediaSessions(self) -> Iterable[MediaSession]:
        return self.__model["sessions"].values()

    async def mediaSessionById(self, session_id: str) -> Optional[MediaSession]:
        return self.__model["sessions"].get(session_id, None)

    async def synchronise(self):
        '''Synchronise MediaConfiguration

        This will update the 5GMS AF configuration and M8 published objects to match this media configuration. This will determine
        the differences between this configuration and what is present on the 5GMS AF and apply the deltas to the 5GMS AF in order
        to synchronise it with this configuration. The parts of the configuration not representable in the 5GMS AF will be written
        out the DataStore (as configured in the constructor). The M8 outputs will be triggered to republish any M8 objects.
        '''
        if self.__m1_session is None:
            m1_authority = (self.__config.get('m1_address'),self.__config.get('m1_port'))
            cert_signer = self.__config.get('certificate_signing_class')
            self.__m1_session = await M1Session(host_address=m1_authority, persistent_data_store=self.__data_store,
                                                certificate_signer=cert_signer)
        af_mc = await MediaConfiguration(self.__extraConfigFile, asp_id=self.__model['aspId'], persistent_data_store=self.__data_store)
        af_imp = await M1SessionImporter(authority=m1_authority, persistent_data_store=self.__data_store, certificate_signer=cert_signer)
        await af_imp.import_to(af_mc)
        deltas = await af_mc.deltas(self)
        print(repr(deltas))
        raise Exception("not implemented yet")

    async def deltas(self, other: "MediaConfiguration") -> List[DeltaOperation]:
        '''Get the list of operations needed to change this configuration into the configuration in other
        '''
        ret = []
        # Check each session I hold to see if it exists in the other configuration or not
        to_del = []
        have = []
        to_add = list(other.__model['sessions'].values())
        for session in self.__model['sessions'].values():
            for o_session in to_add:
                if session.shallow_eq(o_session):
                    have += [(session, o_session)]
                    to_add.remove(o_session)
                    break
            else:
                to_del += [session]
        ret += [await MediaSessionDeltaOperation(self, add=session) for session in to_add]
        ret += [await MediaSessionDeltaOperation(self, remove=session) for session in to_del]
        # check sub-structures of sessions we have for changes
        for session,o_session in have:
            if session.certificates is None and o_session.certificates is not None:
                ret += [await MediaServerCertificateDeltaOperation(session, add=(cert_id,cert)) for cert_id,cert in o_session.certificates.items()]
            elif session.certificates is not None:
                if o_session.certificates is None:
                    ret += [await MediaServerCertificateDeltaOperation(session, remove=cert_id) for cert_id in session.certificates.keys()]
                else:
                    certs_add = o_session.certificates.copy()
                    certs_del = []
                    for cert_id in session.certificates.keys():
                        if cert_id in certs_add:
                            del certs_add[cert_id]
                        else:
                            certs_del += [cert_id]
                    ret += [await MediaServerCertificateDeltaOperation(session, add=(cid,cert)) for cid,cert in certs_add.items()]
                    ret += [await MediaServerCertificateDeltaOperation(session, remove=cid) for cid in certs_del]
                
            if session.media_entry is None and o_session.media_entry is not None:
                ret += [await MediaEntryDeltaOperation(session, add=o_session.media_entry)]
            elif session.media_entry is not None:
                if o_session.media_entry is None:
                    ret += [await MediaEntryDeltaOperation(session, remove=True)]
                elif session.media_entry != o_session.media_entry:
                    ret += [await MediaEntryDeltaOperation(session, add=o_session.media_entry)]

            if session.dynamic_policies is None and o_session.dynamic_policies is not None:
                ret += [await MediaDynamicPolicyDeltaOperation(session, add=dp) for dp in o_session.dynamic_policies]
            elif session.dynamic_policies is not None and o_session.dynamic_policies is None:
                ret += [await MediaDynamicPolicyDeltaOperation(session, remove=dp) for dp in session.dynamic_policies]
            elif session.dynamic_policies is not None and o_session.dynamic_policies is not None:
                # make deltas for individual dynamic policies
                for dp_id,dp in o_session.dynamic_policies.items():
                    if dp_id not in session.dynamic_policies:
                        ret += [await MediaDynamicPolicyDeltaOperation(session, add=(dp_id,dp))]
                    elif dp != session.dynamic_policies[dp_id]:
                        ret += [await MediaDynamicPolicyDeltaOperation(session, modify(dp_id,dp))]
                for dp_id in session.dynamic_policies.keys():
                    if dp_id not in o_session.dynamic_policies:
                        ret += [await MediaDynamicPolicyDeltaOperation(session, remove=dp_id)]

            if session.reporting_configurations is None and o_session.reporting_configurations is not None:
                if o_session.reporting_configurations.consumption is not None:
                    ret += [await MediaConsumptionReportingDeltaOperation(session, add=o_session.reporting_configurations.consumption)]
                if o_session.reporting_configurations.metrics is not None:
                    ret += [await MediaMetricsReportingDeltaOperation(session, add=mr) for mr in o_session.reporting_configurations.metrics]
            elif session.reporting_configurations is not None:
                if session.reporting_configurations.consumption is not None:
                    if o_session.reporting_configurations is None or o_session.reporting_configurations.consumption is None:
                        ret += [await MediaConsumptionReportingDeltaOperation(session, remove=True)]
                    elif session.reporting_configurations.consumption != o_session.reporting_configurations.consumption:
                        ret += [await MediaConsumptionReportingDeltaOperation(session, add=o_session.reporting_configurations.consumption)]
                else:
                    if o_session.reporting_configurations is not None and o_session.reporting_configurations.consumption is not None:
                        ret += [await MediaConsumptionReportingDeltaOperation(session, add=o_session.reporting_configurations.consumption)]
                if session.reporting_configurations.metrics is not None:
                    metric_to_del = []
                    if o_session.reporting_configurations is not None and o_session.reporting_configurations.metrics is not None:
                        metric_to_add = o_session.reporting_configurations.metrics.copy()
                    else:
                        metric_to_add = []
                    for metric in session.reporting_configurations.metrics:
                        if metric in metric_to_add:
                            metric_to_add.remove(metric)
                        else:
                            metric_to_del += [metric]
                    ret += [await MediaMetricsReportingDeltaOperation(session, add=metric) for metric in metric_to_add]
                    ret += [await MediaMetricsReportingDeltaOperation(session, remove=metric) for metric in metric_to_del]
                elif o_session.reporting_configurations is not None and o_session.reporting_configurations.metrics is not None:                         ret += [await MediaMetricsReportingDeltaOperation(session, add=metric) for metric in o_session.reporting_configurations.metrics]
        return ret

    async def __asyncInit(self):
        '''Asynchronous object instantiation

        Loads previous state from the DataStore.

        :meta private:
        :return: self
        '''
        return self

    @staticmethod
    def jsonObjectHandler(obj):
        fn = getattr(obj, "jsonObject", None)
        if fn is not None:
            return fn()
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serialisable')

    @property
    def asp_id(self) -> Optional[str]:
        return self.__model["aspId"]

    @asp_id.setter
    def asp_id(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str) or len(value) == 0:
                raise TypeError('MediaConfiguration.aspId must be a non-empty str or None')
        self.__model["aspId"] = value

# vim:ts=8:sts=4:sw=4:expandtab:
