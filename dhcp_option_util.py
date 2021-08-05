#!/usr/bin/env python3
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
"""
------------------------------------------------------------------------

 Description:
  Demonstration script for Hex Encoding/Decoding of DHCP Options
  using the bloxone module
  

 Requirements:
  bloxone
  yaml

 Author: Chris Marrison

 Date Last Updated: 20210805

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
__version__ = '0.1.0'
__author__ = 'Chris Marrison'
__email__ = 'chris@infoblox.com'

import bloxone
import argparse
import logging
from bloxone.dhcputils import dhcp_decode
import yaml
from pprint import pprint
import os


def parseargs():
    # Parse arguments
    parser = argparse.ArgumentParser(description='DHCP Option Encoding ' +
                                    'and Decoding Utility')
    exclusive = parser.add_mutually_exclusive_group()
    parser.add_argument('-c', '--config', type=str, default='vendor_dict.yaml',
                         help="Path to vendor file")
    exclusive.add_argument('--vendor', type=str, default='',
                        help="Vendor Identifier")
    exclusive.add_argument('--suboptions', type=str, default='',
                        help="Sub Options to encode")
    parser.add_argument('--prefix', type=str, default='',
                        help="Optional prefix for use with --suboptions")
    parser.add_argument('--decode', type=str, default='',
                        help="Hex string to decode")
    exclusive.add_argument('--data_only', action="store_true", 
                        help="Decode hex as 'string' or specified by --type")
    parser.add_argument('--type', type=str, default='string',
                        help="Optional data_type for --decode --data_only")
    parser.add_argument('--dump', type=str, default='', help="Dump Vendor")
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
        prefix = definitions.vendor_prefix(vendor)
        if len(sub_opts):
            encoded_opts = prefix + dhcp_encoder.encode_dhcp_option(sub_opts)
            print(f'Vendor: {vendor}, Encoding: {encoded_opts}')
        else:
            print(f'Vendor: {vendor} has no sub-options to encode')
    
    return

def process_suboptions(sub_options, prefix=''):
    '''
    '''
    global dhcp_encoder

    options= []
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
        if prefix:
            encoding = prefix + encoding
        print(f'Encoded sub-options: {encoding}')

    return


def opttypes_to_list(sub_options):
    '''
    '''
    global dhcp_decoder
    options= []
    subopt = []
    subopt_def = {}
    suboptions_def = []

    options = sub_options.split(',')
    for option in options:
        subopt = option.split(':')
        if len(subopt) >= 2:
            if subopt[1] in dhcp_decoder.opt_types:
                subopt_def = { 'code': subopt[0],
                            'type': subopt[1] }
                suboptions_def.append(subopt_def)
            else:
                print(f'Option type: {subopt[1]} is not supported')
                print(f'Supported types: {dhcp_encoder.opt_types}')
        else:
            print('--suboptions for decode hex incorrect format')
            print('Format is "<code>:<type>,<code>:<type>,..."')
            break
    
    return suboptions_def


def process_all():
    '''
    '''
    global definitions
    global dhcp_encoder

    for vendor in definitions.vendors():
        process_vendor(vendor)

    return


def decode_hex(hex_str, opt_defs=None, data_only=False, data_type='string'):
    '''
    '''
    global definitions
    global dhcp_decoder

    if (len(hex_str) % 2) == 0:
        if not data_only:
            if opt_defs:
                if not isinstance(opt_defs, list):
                    opt_defs = opttypes_to_list(opt_defs)
            else:
                opt_defs = []
            
            print()
            if opt_defs:
                print('Decoding as sub-options, using definitions:')
            else:
                print('Attempting to decode as sub-options:')
            d = dhcp_decoder.decode_dhcp_option(hex_str, sub_opt_defs=opt_defs)
            dhcp_decoder.output_decoded_options(d)
        
        # Decode as data_type, only
        print()
        print(f'Decoding as data-only, using type: {data_type}')
        d = dhcp_decoder.decode_data(hex_str, data_type=data_type)
        print(repr(d))
    else:
        logging.error(f'Hex string contains incomplete octets, decoding halted') 

    return


def main():
    '''
    Main logic
    '''
    exitcode = 0
    options = parseargs()

    global definitions
    global dhcp_encoder
    global dhcp_decoder

    dhcp_encoder = bloxone.dhcp_encode()
    dhcp_decoder = bloxone.dhcp_decode()

    # Check for direct options
    if options.suboptions and not options.decode:
        process_suboptions(options.suboptions, prefix=options.prefix)
    elif options.decode:
        if options.suboptions:
            decode_hex(options.decode, opt_defs=options.suboptions)
        elif options.vendor:
            definitions = bloxone.DHCP_OPTION_DEFS(options.config)
            decode_hex(options.decode, opt_defs=definitions.sub_options(options.vendor))
        else:
            decode_hex(options.decode, 
                       data_type=options.type, 
                       data_only=options.data_only)
    else:
        definitions = bloxone.DHCP_OPTION_DEFS(options.config)

        # Process using config file based on options
        if options.dump:
            dump_vendor(options.dump)
        elif options.vendor:
            process_vendor(options.vendor)
        else:
            process_all()
        
    return exitcode

### Main ###
if __name__ == '__main__':
    exitcode = main()
    exit(exitcode)