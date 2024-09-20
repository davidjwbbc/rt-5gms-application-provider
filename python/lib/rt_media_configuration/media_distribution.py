# 5G-MAG Reference Tools: MediaDistribution class
#==============================================================================
#
# File: rt_media_configuration/media_distribution.py
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
5G-MAG Reference Tools: MediaDistribution Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the MediaDistribution class which models a distribution
configuration for a MediaEntry.
'''

import json
from typing import Optional, List, Iterable, Type, Any, Final, TypedDict

from rt_m1_client.types import DistributionConfiguration

from .media_entry_point import MediaEntryPoint
#from .media_session import MediaSession
from .media_path_rewrite_rule import MediaPathRewriteRule
from .media_caching_configuration import MediaCachingConfiguration
from .media_geo_fencing import MediaGeoFencing
from .media_url_signature import MediaURLSignature
from .media_supplementary_distribution_network import MediaSupplementaryDistributionNetwork

class MediaDistribution:
    '''MediaDistribution class
=======================
This class models the distribution configurations for a MediaEntry.
'''

    def __init__(self, content_prep_template_id: Optional[str] = None, canonical_domain_name: Optional[str] = None,
                 domain_name_alias: Optional[str] = None, base_url: Optional[str] = None,
                 entry_point: Optional[MediaEntryPoint] = None,
                 path_rewrite_rules: Optional[Iterable[MediaPathRewriteRule]] = None,
                 caching_configurations: Optional[Iterable[MediaCachingConfiguration]] = None,
                 geo_fencing: Optional[MediaGeoFencing] = None, url_signature: Optional[MediaURLSignature] = None,
                 certificate_id: Optional[str] = None,
                 supplementary_distrib_networks: Optional[Iterable[MediaSupplementaryDistributionNetwork]] = None):
        self.content_prep_template_id = content_prep_template_id
        self.canonical_domain_name = canonical_domain_name
        self.domain_name_alias = domain_name_alias
        self.base_url = base_url
        self.entry_point = entry_point
        self.path_rewrite_rules = path_rewrite_rules
        self.caching_configurations = caching_configurations
        self.geo_fencing = geo_fencing
        self.url_signature = url_signature
        self.certificate_id = certificate_id
        self.supplementary_distrib_networks = supplementary_distrib_networks

    def __await__(self):
        return self.__asyncInit().__await__()

    async def __asyncInit(self):
        '''Asynchronous object instantiation
        :meta private:
        :return: self
        '''
        return self

    __cmp_params: Final[List[str]] = [
            'content_prep_template_id',
            'canonical_domain_name',
            'domain_name_alias',
            'base_url',
            'entry_point',
            'path_rewrite_rules',
            'caching_configurations',
            'url_signature',
            'certificate_id',
            'supplementary_distrib_networks',
    ]

    def __eq__(self, other: Optional["MediaDistribution"]) -> bool:
        if other is None:
            return False
        for param in self.__cmp_params:
            sp = getattr(self, param)
            op = getattr(other, param)
            if sp is not None:
                if op is None:
                    return False
                if isinstance(sp, list): 
                    lsp = len(sp)
                    lop = len(op)
                    if lsp != lop:
                        return False
                    ssp = sorted(sp)
                    sop = sorted(op)
                    if ssp != sop:
                        return False
                elif sp != op:
                    return False
            elif op is not None:
                return False
        return True

    async def shalloweq(self, other: Optional["MediaDistribution"]) -> bool:
        if other is None:
            return False
        only_if_set: Final[List[str]] = ['content_prep_template_id', 'canonical_domain_name', 'base_url']
        not_values: Final[List[str]] = ['certificate_id']
        for param in self.__cmp_params:
            sp = getattr(self, param)
            op = getattr(other, param)
            if sp is not None:
                if op is None:
                    if param not in only_if_set:
                        return False
                elif isinstance(sp, list): 
                    lsp = len(sp)
                    lop = len(op)
                    if lsp != lop:
                        return False
                    if param not in not_values:
                        ssp = sorted(sp)
                        sop = sorted(op)
                        if ssp != sop:
                            return False
                elif param not in not_values and sp != op:
                    return False
            elif op is not None and param not in only_if_set:
                return False
        return True

    def __ne__(self, other: "MediaDistribution") -> bool:
        return not self == other

    def __lt__(self, other: Optional["MediaDistribution"]) -> bool:
        if other is None:
            return False
        for param in self.__cmp_params:
            sp = getattr(self, param)
            op = getattr(other, param)
            if sp is not None:
                if op is None:
                    return False
                if isinstance(sp, list):
                    lsp = len(sp)
                    lop = len(op)
                    if lsp != lop:
                        return lsp < lop
                    ssp = sorted(sp)
                    sop = sorted(op)
                    if ssp != sop:
                        return ssp < sop
                elif sp != op:
                    return sp < op
            elif op is not None:
                return True
        return False

    def __le__(self, other: Optional["MediaDistribution"]) -> bool:
        if other is None:
            return False
        for param in self.__cmp_params:
            sp = getattr(self, param)
            op = getattr(other, param)
            if sp is not None:
                if op is None:
                    return False
                if isinstance(sp, list): 
                    lsp = len(sp)
                    lop = len(op)
                    if lsp != lop:
                        return lsp < lop
                    ssp = sorted(sp)
                    sop = sorted(op)
                    if ssp != sop:
                        return ssp < sop
                elif sp != op:
                    return sp < op
            elif op is not None:
                return True
        return True

    def __ge__(self, other: Optional["MediaDistribution"]) -> bool:
        return not (self < other)

    def __gt__(self, other: Optional["MediaDistribution"]) -> bool:
        return not (self <= other)

    def __repr__(self) -> str:
        '''Python constructor string for this object'''
        ret = f'{self.__class__.__name__}('
        np = ''
        for param in self.__cmp_params:
            sp = getattr(self, param)
            if sp is not None:
                ret += f'{np}{param}={sp!r}'
                np = ', '
        ret += ')'
        return ret

    def __str__(self) -> str:
        return self.serialise(pretty=True)

    def serialise(self, pretty: bool = False) -> str:
        '''Serialise'''
        from .media_configuration import MediaConfiguration
        kwargs = {}
        if pretty:
            kwargs = {"sort_keys": True, "indent": 4}
        return json.dumps(self, default=MediaConfiguration.jsonObjectHandler, **kwargs)

    @staticmethod
    def deserialise(json_obj: str) -> "MediaDistribution":
        '''Deserialise'''
        try:
            obj = json.loads(json_obj)
        except json.JSONDecodeError:
            raise ValueError("Bad JSON")
        return MediaDistribution.fromJSONObject(obj)

    @staticmethod
    def fromJSONObject(obj: dict) -> "MediaDistribution":
        kwargs = {}
        for k,v in obj.items():
            if k == 'contentPreparationTemplateId':
                kwargs['content_prep_template_id'] = v
            elif k == 'canonicalDomainName':
                kwargs['canonical_domain_name'] = v
            elif k == 'domainNameAlias':
                kwargs['domain_name_alias'] = v
            elif k == 'baseURL':
                kwargs['base_url'] = v
            elif k == 'entryPoint':
                kwargs['entry_point'] = MediaEntryPoint.fromJSONObject(v)
            elif k == 'pathRewriteRules':
                kwargs['path_rewrite_rules'] = [MediaPathRewriteRule.fromJSONObject(value) for value in v]
            elif k == 'cachingConfigurations':
                kwargs['caching_configurations'] = [MediaCachingConfiguration.fromJSONObject(value) for value in v]
            elif k == 'geoFencing':
                kwargs['geo_fencing'] = MediaGeoFencing.fromJSONObject(v)
            elif k == 'urlSignature':
                kwargs['url_signature'] = MediaURLSignature.fromJSONObject(v)
            elif k == "certificateId":
                kwargs["certificate_id"] = v
            elif k == 'supplementaryDistributionNetworks':
                kwargs['supplementary_distrib_networks'] = [MediaSupplementaryDistributionNetwork.fromJSONObject(value) for value in v]
            else:
                raise TypeError(f'MediaDistribution: JSON field "{k}" not understood')
        return MediaDistribution(**kwargs)

    def jsonObject(self) -> dict:
        obj = {}
        if self.__content_prep_template_id is not None:
            obj['contentPreparationTemplateId'] = self.__content_prep_template_id
        if self.__canonical_domain_name is not None:
            obj['canonicalDomainName'] = self.__canonical_domain_name
        if self.__domain_name_alias is not None:
            obj['domainNameAlias'] = self.__domain_name_alias
        if self.__base_url is not None:
            obj['baseURL'] = self.__base_url
        if self.__entry_point is not None:
            obj['entryPoint'] = self.__entry_point
        if self.__path_rewrite_rules is not None:
            obj['pathRewriteRules'] = self.__path_rewrite_rules
        if self.__caching_configurations is not None:
            obj['cachingConfigurations'] = self.__caching_configurations
        if self.__geo_fencing is not None:
            obj['geoFencing'] = self.__geo_fencing
        if self.__url_signature is not None:
            obj['urlSignature'] = self.__url_signature
        if self.__certificate_id is not None:
            obj['certificateId'] = self.__certificate_id
        if self.__supplementary_distrib_networks is not None:
            obj['supplementaryDistributionNetworks'] = self.__supplementary_distrib_networks
        return obj

    @property
    def content_prep_template_id(self) -> Optional[str]:
        return self.__content_prep_template_id

    @content_prep_template_id.setter
    def content_prep_template_id(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value,str):
                raise TypeError('MediaDistribution.content_prep_template_id can be either None or a str')
        self.__content_prep_template_id = value

    @property
    def canonical_domain_name(self) -> Optional[str]:
        return self.__canonical_domain_name

    @canonical_domain_name.setter
    def canonical_domain_name(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value,str):
                raise TypeError('MediaDistribution.canonical_domain_name can be either None or a str')
        self.__canonical_domain_name = value

    @property
    def domain_name_alias(self) -> Optional[str]:
        return self.__domain_name_alias

    @domain_name_alias.setter
    def domain_name_alias(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value,str):
                raise TypeError('MediaDistribution.domain_name_alias can be either None or a str')
        self.__domain_name_alias = value

    @property
    def base_url(self) -> Optional[str]:
        return self.__base_url

    @base_url.setter
    def base_url(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value,str):
                raise TypeError('MediaDistribution.base_url can be either None or a str')
        self.__base_url = value

    @property
    def entry_point(self) -> Optional[MediaEntryPoint]:
        return self.__entry_point

    @entry_point.setter
    def entry_point(self, value: Optional[MediaEntryPoint]):
        if value is not None:
            if not isinstance(value,MediaEntryPoint):
                raise TypeError('MediaDistribution.entry_point can be either None or a MediaEntryPoint')
        self.__entry_point = value

    @property
    def path_rewrite_rules(self) -> Optional[List[MediaPathRewriteRule]]:
        return self.__path_rewrite_rules

    @path_rewrite_rules.setter
    def path_rewrite_rules(self, value: Optional[Iterable[MediaPathRewriteRule]]):
        if value is not None:
            if not isinstance(value, list):
                value = list(value)
            if not all(isinstance(v,MediaPathRewriteRule) for v in value):
                raise TypeError('MediaDistribution.path_rewrite_rules can be either None or a non-empty list of MediaPathRewriteRule')
            if len(value) == 0:
                value = None
        self.__path_rewrite_rules = value

    @property
    def caching_configurations(self) -> Optional[List[MediaCachingConfiguration]]:
        return self.__caching_configurations

    @caching_configurations.setter
    def caching_configurations(self, value: Optional[Iterable[MediaCachingConfiguration]]):
        if value is not None:
            if not isinstance(value, list):
                value = list(value)
            if not all(isinstance(v,MediaCachingConfiguration) for v in value):
                raise TypeError('MediaDistribution.caching_configurations can be either None or a non-empty list of MediaCachingConfiguration')
            if len(value) == 0:
                value = None
        self.__caching_configurations = value

    @property
    def geo_fencing(self) -> Optional[MediaGeoFencing]:
        return self.__geo_fencing

    @geo_fencing.setter
    def geo_fencing(self, value: Optional[MediaGeoFencing]):
        if value is not None:
            if not isinstance(value, MediaGeoFencing):
                raise TypeError('MediaDistribution.geo_fencing can be either None or a MediaGeoFencing')
        self.__geo_fencing = value

    @property
    def url_signature(self) -> Optional[MediaURLSignature]:
        return self.__url_signature

    @url_signature.setter
    def url_signature(self, value: Optional[MediaURLSignature]):
        if value is not None:
            if not isinstance(value, MediaURLSignature):
                raise TypeError('MediaDistribution.url_signature can be either None or a MediaURLSignature')
        self.__url_signature = value

    @property
    def certificate_id(self) -> Optional[str]:
        return self.__certificate_id

    @certificate_id.setter
    def certificate_id(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value,str):
                raise TypeError('MediaDistribution.certificate_id can be either None or a str')
        self.__certificate_id = value
    
    @property
    def supplementary_distrib_networks(self) -> Optional[List[MediaSupplementaryDistributionNetwork]]:
        return self.__supplementary_distrib_networks

    @supplementary_distrib_networks.setter
    def supplementary_distrib_networks(self, value: Optional[Iterable[MediaSupplementaryDistributionNetwork]]):
        if value is not None:
            if not isinstance(value, list):
                value = list(value)
            if not all(isinstance(v,MediaSupplementaryDistributionNetwork) for v in value):
                raise TypeError('MediaDistribution.caching_configurations can be either None or a non-empty list of MediaSupplementaryDistributionNetwork')
            if len(value) == 0:
                value = None
        self.__supplementary_distrib_networks = value

    __conv_3gpp: Final[List[TypedDict('3GPPConversion', {'param': str, 'field': str, 'cls': Type})]] = [
        {'param': 'content_prep_template_id', 'field': 'contentPreparationTemplateId', 'cls': str},
        {'param': 'canonical_domain_name', 'field': 'canonicalDomainName', 'cls': str},
        {'param': 'domain_name_alias', 'field': 'domainNameAlias', 'cls': str},
        {'param': 'base_url', 'field': 'baseURL', 'cls': str},
        {'param': 'entry_point', 'field': 'entryPoint', 'cls': MediaEntryPoint},
        {'param': 'path_rewrite_rules', 'field': 'pathRewriteRules', 'cls': List[MediaPathRewriteRule]},
        {'param': 'caching_configuration', 'field': 'cachingConfigurations', 'cls': List[MediaCachingConfiguration]},
        {'param': 'geo_fencing', 'field': 'geoFencing', 'cls': MediaGeoFencing},
        {'param': 'url_signature', 'field': 'urlSignature', 'cls': MediaURLSignature},
        {'param': 'certificate_id', 'field': 'certificateId', 'cls': str},
        {'param': 'supplementary_distrib_networks', 'field': 'supplementaryDistributionNetworks', 'cls': List[MediaSupplementaryDistributionNetwork]}
    ]

    @classmethod
    async def from3GPPObject(cls, dc: DistributionConfiguration) -> "MediaDistribution":
        kwargs = {}
        for cnv in cls.__conv_3gpp:
            if cnv['field'] in dc:
                kwargs[cnv['param']] = await cls.doConversion(dc[cnv['field']],cnv['cls'],'from3GPPObject')
        return await cls(**kwargs)

    async def to3GPPObject(self, session: "MediaSession") -> DistributionConfiguration:
        from .media_session import MediaSession
        ret = {}
        for cnv in self.__conv_3gpp:
            v = getattr(self, cnv['param'], None)
            if v is not None:
                ret[cnv['field']] = await self.doConversion(v, cnv['cls'], 'to3GPPObject', session)
        if 'certificateId' in ret:
            # Do local Id to certificateId conversion if necessary
            cert = session.certificateByIdent(ret['certificateId'])
            if cert is not None:
                ret['certificateId'] = cert.certificate_id
        return DistributionConfiguration(ret)

    @staticmethod
    async def doConversion(value: Any, typ: Type, convfn, session: Optional["MediaSession"] = None) -> Any:
        from .media_session import MediaSession
        if value is None:
            return None
        if getattr(typ, '__origin__', None) is list:
            return [await MediaDistribution.doConversion(v, typ.__args__[0], convfn, session=session) for v in value]
        fn = getattr(typ, convfn, None)
        if fn is not None:
            if session is not None:
                return await fn(value, session=session)
            else:
                return await fn(value)
        return typ(value)
