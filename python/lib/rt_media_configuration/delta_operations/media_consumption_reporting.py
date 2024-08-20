#!/usr/bin/python3 
#==============================================================================
# 5G-MAG Reference Tools: MediaConsumptionReportingDeltaOperation class
#==============================================================================
#
# File: rt_media_configuration/delta_operations/media_consumption_reporting.py
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
5G-MAG Reference Tools: MediaConsumptionReportingDeltaOperation Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaConsumptionReportingDeltaOperation class which
holds operation parameters from changing the MediaConsumptionReportingConfiguration
of a MediaSession.
'''
from typing import Optional

from rt_m1_client.session import M1Session
from rt_m1_client.types import ConsumptionReportingConfiguration

from ..media_session import MediaSession
from ..media_consumption_reporting_configuration import MediaConsumptionReportingConfiguration

from .delta_operation import DeltaOperation

class MediaConsumptionReportingDeltaOperation(DeltaOperation):
    '''DeltaOperation class for MediaConsumptionReportingConfiguration
    '''

    def __init__(self, session: MediaSession, *, add: Optional[MediaConsumptionReportingConfiguration] = None,
                 remove: Optional[bool] = None):
        if sum(1 for p in [add,remove] if p is not None) != 1:
            raise ValueError('MediaConsumptionReportingDeltaOperation must be initialised as an "add" or "remove" operation')
        super().__init__(session)
        self.__is_add = add is not None
        if self.__is_add:
            self.__mcrc = add

    def __str__(self):
        if self.__is_add:
            return f'Add ConsumptionReportingConfiguration to ProvisioningSession "{self.session.identity()}"'
        return f'Remove ConsumptionReportingConfiguration from ProvisioningSession "{self.session.identity()}"'

    def __repr__(self):
        ret = super().__repr__()[:-1]
        if self.__is_add:
            ret += f', add={self.__mcrc!r}'
        else:
            ret += ', remove=True'
        ret += ')'
        return ret
    
    async def apply_delta(self, m1_session: M1Session) -> bool:
        '''Apply this delta to the session via M1Session
        '''
        if self.__is_add:
            crc = self.__consumptionReportingConfiguration3GPPObject(self.__mcrc)
            if not await m1_session.setOrUpdateConsumptionReporting(self.session.identity(), crc):
                return False
            self.session.setConsumptionReportingConfiguration(self.__mcrc)
        else:
            if not await m1_session.consumptionReportingConfigurationDelete(self.session.identity()):
                return False
            self.session.unsetConsumptionReportingConfiguration()
        return True

    @staticmethod
    def __consumptionReportingConfiguration3GPPObject(mcrc: MediaConsumptionReportingConfiguration) -> ConsumptionReportingConfiguration:
        crc = {}
        if mcrc.reporting_interval is not None:
            crc['reportingInterval'] = mcrc.reporting_interval
        if mcrc.sample_percentage is not None:
            crc['samplePercentage'] = mcrc.sample_percentage
        if mcrc.location_reporting is not None:
            crc['locationReporting'] = mcrc.location_reporting
        if mcrc.access_reporting is not None:
            crc['accessReporting'] = mcrc.access_reporting
        return crc
