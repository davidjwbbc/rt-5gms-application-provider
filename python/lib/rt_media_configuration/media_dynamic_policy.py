# 5G-MAG Reference Tools: MediaDynamicPolicy class
#==============================================================================
#
# File: rt_media_configuration/media_dynamic_policy.py
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
5G-MAG Reference Tools: MediaDynamicPolicy Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaDynamicPolicy class which models the QoS
settings to apply to a MediaEntry.
'''

import json
from typing import Optional

from .media_dynamic_policy_session_context import MediaDynamicPolicySessionContext
from .media_qos_parameters import MediaQoSParameters
from .media_charging_specification import MediaChargingSpecification

class MediaDynamicPolicy:
    '''MediaDynamicPolicy class
========================
This class models the QoS parameters, charging rules and application rules for dynamic policy activation in a MediaEntry.
'''

    def __init__(self, session_context: Optional[MediaDynamicPolicySessionContext] = None, qos_parameters: Optional[MediaQoSParameters] = None, charging: Optional[MediaChargingSpecification] = None):
        self.session_context = session_context
        self.qos_parameters = qos_parameters
        self.charging = charging

    def __await__(self):
        return self.__asyncInit().__await__()

    async def __asyncInit(self):
        '''Asynchronous object instantiation
        :meta private:
        :return: self
        '''
        return self

    def __eq__(self, other: "MediaDynamicPolicy") -> bool:
        if self.__session_context != other.__session_context:
            return False
        if self.__qos_parameters != other.__qos_parameters:
            return False
        return self.__charging == other.__charging

    def __ne__(self, other: "MediaDynamicPolicy") -> bool:
        return not (self == other)

    def __repr__(self) -> str:
        '''Python constructor string for this object'''
        ret = f'{self.__class__.__name__}('
        np = ""
        if self.__session_context is not None:
            ret += f'session_context={self.__session_context!r}'
            np = ", "
        if self.__qos_parameters is not None:
            ret += f'{np}qos_parameters={self.__qos_parameters!r}'
            np = ", "
        if self.__charging is not None:
            ret += f'{np}charging={self.__charging!r}'
        ret += ')'
        return ret

    def __str__(self) -> str:
        return self.serialise(pretty=True)

    def serialise(self, pretty: bool = False) -> str:
        from .media_configuration import MediaConfiguration
        kwargs = {}
        if pretty:
            kwargs = {"sort_keys": True, "indent": 4}
        return json.dumps(self, default=MediaConfiguration.jsonObjectHandler, **kwargs)

    @staticmethod
    def deserialise(json_obj: str) -> "MediaDynamicPolicy":
        try:
            obj = json.loads(json_obj)
        except json.JSONDecodeError:
            raise ValueError("Bad JSON")

        return MediaDynamicPolicy._fromJSONObject(obj)

    @staticmethod
    def _fromJSONObject(obj: dict) -> "MediaDynamicPolicy":
        kwargs = {}
        if "applicationSessionContext" in obj:
            kwargs["session_context"] = MediaDynamicPolicySessionContext._fromJSONObject(obj["applicationSessionContext"])
        if "qoSSpecification" in obj:
            kwargs["qos_parameters"] = MediaQoSParameters._fromJSONObject(obj["qoSSpecification"])
        if "chargingSpecification" in obj:  
            kwargs["charging"] = MediaChargingSpecification._fromJSONObject(obj["chargingSpecification"])
        return MediaDynamicPolicy(**kwargs)

    def _jsonObject(self) -> dict:
        obj = {}
        if self.__session_context is not None:
            obj['applicationSessionContext'] = self.__session_context
        if self.__qos_parameters is not None:
            obj['qoSSpecification'] = self.__qos_parameters
        if self.__charging is not None:
            obj['chargingSpecification'] = self.__charging
        return obj

    @property
    def session_context(self) -> Optional[MediaDynamicPolicySessionContext]:
        return self.__session_context

    @session_context.setter
    def session_context(self, value: Optional[MediaDynamicPolicySessionContext]):
        if value is not None:
            if not isinstance(value, MediaDynamicPolicySessionContext):
                raise TypeError('MediaDynamicPolicy.session_context can be either None or a MediaDynamicPolicySessionContext')
        self.__session_context = value

    @property
    def qos_parameters(self) -> Optional[MediaQoSParameters]:
        return self.__qos_parameters

    @qos_parameters.setter
    def qos_parameters(self, value: Optional[MediaQoSParameters]):
        if value is not None:
            if not isinstance(value, MediaQoSParameters):
                raise TypeError('MediaDynamicPolicy.qos_parameters can be either None or a MediaQoSParameters object')
        self.__qos_parameters = value

    @property
    def charging(self) -> Optional[MediaChargingSpecification]:
        return self.__charging

    @charging.setter
    def charging(self, value: Optional[MediaChargingSpecification]):
        if value is not None:
            if not isinstance(value, MediaChargingSpecification):
                raise TypeError('MediaDynamicPolicy.charging can be either None or a MediaChargingSpecification object')
        self.__charging = value
