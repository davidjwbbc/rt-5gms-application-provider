#!/usr/bin/python3
#==============================================================================
# 5G-MAG Reference Tools: MediaServerCertificate class
#==============================================================================
#
# File: rt_media_configuration/media_server_certificate.py
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
5G-MAG Reference Tools: MediaServerCertificate class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaServerCertificate class which models AS
certificates attached to a MediaSession.
'''

from typing import Optional

class MediaServerCertificate:
    '''MediaServerCertificate class
============================
This class models AS certificates which are part of a MediaSession.
'''

    def __init__(self, local_ident: Optional[str] = None, certificate_id: Optional[str] = None, public_cert: Optional[str] = None):
        self.id = local_ident
        self.certificate_id = certificate_id
        self.public_cert = public_cert

    def __await__(self):
        return self._asyncInit().__await__

    async def _asyncInit(self):
        return self

    def __eq__(self, other: "MediaServerCertificate") -> bool:
        if self.__id != other.__id:
            return False
        if self.__certificate_id != other.__certificate_id:
            return False
        return self.__public_cert == other.__public_cert

    def __ne__(self, other: "MediaServerCertificate") -> bool:
        return not (self == other)

    def __repr__(self) -> str:
        ret = f'{self.__class__.__name__}('
        np = ''
        if self.__id is not None:
            ret += f'local_ident={self.__id!r}'
            np = ', '
        if self.__certificate_id is not None:
            ret += f'{np}certificate_id={self.__certificate_id!r}'
            np = ', '
        if self.__public_cert is not None:
            ret += f'{np}public_cert={self.__public_cert!r}'
        ret += ')'
        return ret

    def __str__(self) -> str:
        return self.serialise(pretty=True)

    @staticmethod
    def deserialise(json_obj: str) -> "MediaServerCertificate":
        try:
            obj = json.loads(json_obj)
        except json.JSONDecodeError:
            raise ValueError("Bad JSON")
        return MediaServerCertificate.fromJSONObject(obj)

    @staticmethod
    def fromJSONObject(obj: dict) -> "MediaServerCertificate":
        kwargs = {}
        for k,v in obj.items():
            if k == 'localId':
                kwargs['local_ident'] = v
            elif k == 'certificateId':
                kwargs['certificate_id'] = v
            elif k == 'publicCert':
                kwargs['public_cert'] = v
            else:
                raise TypeError(f'MediaServerCertificate: JSON field "{k}" not understood')
        return MediaServerCertificate(**kwargs)

    def jsonObject(self) -> dict:
        obj = {}
        if self.__id is not None:
            obj['localId'] = self.__id
        if self.__certificate_id is not None:
            obj['certificateId'] = self.__certificate_id
        if self.__public_cert is not None:
            obj['publicCert'] = self.__public_cert
        return obj

    def identity(self) -> Optional[str]:
        if self.__certificate_id is not None:
            return self.__certificate_id
        return self.__id

    @property
    def id(self) -> Optional[str]:
        return self.__id

    @id.setter
    def id(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeError('MediaServerCertificate.id must be either None or a str')
        self.__id = value

    @property
    def certificate_id(self) -> Optional[str]:
        return self.__certificate_id

    @certificate_id.setter
    def certificate_id(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeError('MediaServerCertificate.certificate_id must be either None or a str')
        self.__certificate_id = value

    @property
    def public_cert(self) -> Optional[str]:
        return self.__public_cert

    @public_cert.setter
    def public_cert(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeError('MediaServerCertificate.public_cert must be either None or a PEM encoded str')
        self.__public_cert = value
