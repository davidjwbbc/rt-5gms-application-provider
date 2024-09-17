#!/usr/bin/python3 
#==============================================================================
# 5G-MAG Reference Tools: DVBIFormatter class
#==============================================================================
#
# File: rt_m8_output/dvbi.py
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
5G-MAG Reference Tools: DVBIFormatter Class
=====================================================
Copyright: (C) 2024 British Broadcasting Corporation
Author(s): David Waring <david.waring2@bbc.co.uk>
Licence: 5G-MAG Public License (v1.0)

For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
=====================================================

This module provides the DVBIFormatter M8 Output Formatting class.
Objects of this class are used by rt_media_configuration.MediaConfiguration
to write out the static files to be served to the 5GMS Aware App via the
interface at reference point M8.
'''

from rt_media_configuration import MediaConfiguration

from .m8_output import M8Output

class DVBIFormatter(M8Output):
    '''DVBIFormatter class
    ===================
    Output formatter to represent a MediaConfiguration as a (set of) DVB-I Service
    description file.
    '''
    def __init__(self, root_dir: str, config: Configuration = app_configuration):
        super().__init__(root_dir)
        self.__config = config

    async def writeOutput(self, media_config: MediaConfiguration):
        '''Write out the DVB-I Service XML file.
        '''
        if not os.path.isdir(self.root_dir):
            os.makedirs(self.root_dir, mode=0o755)
        raise NotImplemented(f'{__name__}.{self.__class__.__name__}.writeOutput() has not been implemented yet')

#MediaConfiguration.registerM8OutputClass(DVBIFormatter)

# vim:ts=8:sts=4:sw=4:expandtab:
