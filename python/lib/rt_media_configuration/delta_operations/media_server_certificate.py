#!/usr/bin/python3 
#==============================================================================
# 5G-MAG Reference Tools: MediaServerCertificateDeltaOperation class
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
5G-MAG Reference Tools: MediaServerCertificateDeltaOperation Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaServerCertificateDeltaOperation class which
holds operation parameters for MediaServerCertificate operations needed to
change one MediaConfiguration into another MediaConfiguration.
'''
from typing import Optional, Tuple

from rt_m1_client.session import M1Session

from ..media_session import MediaSession
from ..media_server_certificate import MediaServerCertificate

from .delta_operation import DeltaOperation

class MediaServerCertificateDeltaOperation(DeltaOperation):
    '''DeltaOperation for a MediaServerCertificate
    '''

    def __init__(self, session: MediaSession, *, add: Optional[Tuple[str,MediaServerCertificate]] = None, remove: Optional[str] = None):
        if sum(1 for p in [add,remove] if p is not None) != 1:
            raise ValueError('MediaServerCertificateDeltaOperation must be initialised as an "add" or "remove" operation')
        super().__init__(session)
        self.__is_add = add is not None
        if self.__is_add:
            self.__cert_id,self.__cert = add
        else:
            self.__cert_id = remove

    def __str__(self):
        if self.__is_add:
            return f'Add ServerCertificate "{self.__cert_id}" to ProvisioningSession "{self.session.identity()}"'
        return f'Remove ServerCertificate "{self.__cert_id}" from ProvisioningSession "{self.session.identity()}"'

    def __repr__(self):
        ret = super().__repr__()[:-1]
        if self.__is_add:
            ret += f', add=({self.__cert_id!r},{self.__cert!r})'
        else:
            ret += f', remove={self.__cert_id!r}'
        ret += ')'
        return ret

    async def apply_delta(self, m1_session: M1Session, update_container: bool = True) -> bool:
        if self.__is_add:
            # add certificate to session
            cert_id = await m1_session.createNewCertificate(self.session.identity(), self.__domain_names)
            if cert_id is None:
                return False
            self.__cert.certificate_id = cert_id
            if self.__cert_id != cert_id:
                self.session.removeCertificate(ident=self.__cert_id)
            if update_container:
                self.session.addCertificate(self.__cert)
        else:
            # remove certificate from session
            if not await m1_session.certificateDelete(self.session.identity(), self.__cert_id):
                return False
            if update_container:
                self.session.removeCertificate(ident=self.__cert_id)
        return True
