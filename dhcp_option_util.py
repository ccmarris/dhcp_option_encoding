#!/usr/bin/env python3
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
"""
------------------------------------------------------------------------

 Description:
  DHCP Hex Encoding/Decoding Utility for Option Encoding

 Requirements:
  bloxone
  yaml

 Usage:

 Author: Chris Marrison

 Date Last Updated: 20210722

Copyright 2021 Chris Marrison / Infoblox

Redistribution and use in source and binary forms,
with or without modification, are permitted provided
that the following conditions are met:

1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

------------------------------------------------------------------------
"""
__version__ = '0.0.3'
__author__ = 'Chris Marrison'
__email__ = 'chris@infoblox.com'

import bloxone
import argparse
import logging
from bloxone.dhcputils import dhcp_encode
import yaml
from pprint import pprint
import os


def parseargs():
    # Parse arguments
    parser = argparse.ArgumentParser(description='DHCP Option Encoding and Decoding Utility')
    parser.add_argument('-c', '--config', action="store", help="Path to database file", required=True)
    # parser.add_argument('-p', '--output_path', action="store", default='', help="Output file path (optional)")
    parser.add_argument('--dump', type=str, default='', help="Dump Vendor")
    parser.add_argument('--vendor', type=str, default='', help="Vendor Identifier")
    parser.add_argument('--suboptions', type=str, default='', help="Sub Options to encode")
    parser.add_argument('-v', '--version', action='store_true', help="Config Version")
    # parser.add_argument('-y', '--yaml', action="store", help="Alternate yaml config file for objects")
    # parser.add_argument('--debug', help="Enable debug logging", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)

    return parser.parse_args()


def dump_vendor(vendor):
    '''
    '''
    global definitions
    global dhcp_encoder

    if definitions.included(vendor):
        print(f'Vendor: ')
        print(yaml.dump(definitions.dump_vendor_def(vendor)))
    else:
        print(f'Vendor: {vendor} not found.')
    
    return


def process_vendor(vendor):
    '''
    '''
    global definitions
    global dhcp_encoder

    if definitions.included(vendor):
        sub_opts = definitions.sub_options(vendor)
        if len(sub_opts):
            encoded_opts = dhcp_encoder.encode_dhcp_option(sub_opts)
            print(f'Vendor: {vendor}, Encoding: {encoded_opts}')
        else:
            print(f'Vendor: {vendor} has no sub-options to encode')
    
    return

def process_suboptions(sub_options):
    '''
    '''
    global definitions
    global dhcp_encoder

    optionns= []
    subopt = []
    subopt_def = {}
    suboptions_def = []

    options = sub_options.split(',')
    for option in options:
        subopt = option.split(':')
        if len(subopt) == 3:
            if subopt[1] in dhcp_encoder.opt_types:
                subopt_def = { 'code': subopt[0],
                            'type': subopt[1],
                            'data': subopt[2] }
                suboptions_def.append(subopt_def)
            else:
                print(f'Option type: {subopt[1]} is not supported')
                print(f'Supported types: {dhcp_encoder.opt_types}')
        else:
            print('--suboptions data incorrect format')
            print('Format is "<code>:<type>:<data>,<code>:<type>:<data>,..."')
            break
    
    if len(suboptions_def) == len(options):
        encoding = dhcp_encoder.encode_dhcp_option(suboptions_def)
        print(f'Encoded sub-options: {encoding}')

    return


def process_all():
    '''
    '''
    global definitions
    global dhcp_encoder

    for vendor in definitions.vendors():
        sub_opts = definitions.sub_options(vendor)
        if len(sub_opts):
            encoded_opts = dhcp_encoder.encode_dhcp_option(sub_opts)
            print(f'Vendor: {vendor}, Encoding: {encoded_opts}')
        else:
            print(f'Vendor: {vendor} has no sub-options to encode')

    return


def main():
    '''
    Main logic
    '''
    exitcode = 0
    options = parseargs()

    global definitions
    global dhcp_encoder

    definitions = bloxone.DHCP_OPTION_DEFS(options.config)
    dhcp_encoder = bloxone.dhcp_encode()

    if options.dump:
        dump_vendor(options.dump)
    elif options.vendor:
        process_vendor(options.vendor)
    elif options.suboptions:
        process_suboptions(options.suboptions)
    else:
        process_all()
        
    return exitcode

### Main ###
if __name__ == '__main__':
    exitcode = main()
    exit(exitcode)