#!/usr/bin/python3 
#==============================================================================
# 5G-MAG Reference Tools: MediaDynamicPolicyDeltaOperation class
#==============================================================================
#
# File: rt_media_configuration/delta_operations/media_dynamic_policy.py
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
5G-MAG Reference Tools: MediaDynamicPolicyDeltaOperation Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaDynamicPolicyDeltaOperation class which holds
operation parameters for manipulating DynamicPolicyConfiguration objects.
'''
from typing import Optional

from rt_m1_client.session import M1Session
from rt_m1_client.types import DynamicPolicyConfiguration

from ..media_session import MediaSession
from ..media_dynamic_policy import MediaDynamicPolicy

from .delta_operation import DeltaOperation

class MediaDynamicPolicyDeltaOperation(DeltaOperation):
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
