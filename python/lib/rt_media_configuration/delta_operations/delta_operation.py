#!/usr/bin/python3 
#==============================================================================
# 5G-MAG Reference Tools: DeltaOperation class
#==============================================================================
#
# File: rt_media_configuration/delta_operations/delta_operation.py
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
5G-MAG Reference Tools: DeltaOperation Class
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
import logging
from typing import Optional

from rt_m1_client.session import M1Session

from ..media_session import MediaSession

class DeltaOperation:
    '''Interface class for DeltaOperation classes
    '''

    def __init__(self, session: MediaSession):
        self.session = session
        self.log = logging.getLogger(self.__class__.__name__)

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
