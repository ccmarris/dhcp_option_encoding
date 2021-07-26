===================
dhcp_option_util.py
===================

Version: 0.0.4
Author: Chris Marrison
Email: chris@infoblox.com

Description
-----------

Demonstration script for Hex Encoding/Decoding of DHCP Options
using the dhcputils from the bloxone module.


Prerequisites
-------------

Python 3.6 or above 
bloxone Module


Modules
~~~~~~~

Requires:

	- bloxone
    - yaml


Installing the bloxone Module
-----------------------------

The bloxone module can be installed either from source or via PyPi::

	pip3 install bloxone

Source is available from github::

	https://github.com/ccmarris/python-bloxone


Usage
-----

Help information is available via the --help option::

	% ./dhcp_option_util.py --help
	usage: dhcp_option_util.py [-h] [-c CONFIG] [--dump DUMP] [--vendor VENDOR] [--suboptions SUBOPTIONS] [--prefix PREFIX]

	DHCP Option Encoding and Decoding Utility

	optional arguments:
	-h, --help            show this help message and exit
	-c CONFIG, --config CONFIG
							Path to vendor file
	--dump DUMP           Dump Vendor
	--vendor VENDOR       Vendor Identifier
	--suboptions SUBOPTIONS
							Sub Options to encode
	--prefix PREFIX       Optional prefix for use with --suboptions
        

The script allows encoding of DHCP Options through either the use of a YAML
vendor dictionary file, or directly from the CLI.

A sample YAML file *vendor_dict.yaml* is included, whilst the file format is 
described in the :ref:`yaml-format`.

Basic examples::

 
 To process all vendors in the configuration file::

    $ ./dhcp_option_util.py -c vendor_dict.yaml


To process a specific vendor::

    $ ./dhcp_option_util.py -c vendor_dict.yaml --vendor <vendor>


Dump the configuarion of a vendor::

    $ ./dhcp_option_util.py -c vendor_dict.yaml --dump <vendor>


The CLI also support direct encoding from the CLI using the *--sub-option*
option. This allows you to specify options using the format::
    
    '<code>:<type>:<data>,<code>:<type>:<data>,<code>:<type>:<data>'


Encode direct from CLI::

    $ ./dhcp_option_util.py --sub-options '1:string:https,2:ipv4_address:10.10.10.10'


    
.. yaml-format:
YAML File Format
----------------

The base file definition allows for a file version number and a list of 
vendors, a sample showing all of the options is shown below::

    ---
    # DHCP Vendor Option Definitions
    version: 0.0.1

    vendors:

        Sample-Vendor:
            vci: sample-vci
            description: My Vendor Class
            prefix: "<prefix str if required>"
            option-def: 
                parent-option:
                    name: option name
                    code: 43
                    type: binary
                    array: False
                sub-options:
                    - name: Sub Opt 1
                        code: 1
                        type: string
                        data: Encode this string
                        array: False
                        data-only: False
                    - name: Sub Opt 2
                        code: 5
                        type: ipv4_address
                        data: 10.10.10.10,20.20.20.20
                        array: True
                        data-only: False

The format allows the complete definition of a vendor, with the core element
being the *option-def* that defines, in particular, the list of sub-options
for encoding.

The definition can include a prefix to prepend to the encoding, and data-only
flags to handle both option 43 style encodings and option 125 style encodings.

Example Definitions::

    ---
    # DHCP Vendor Option Definitions
    version: 0.0.1

    vendors:

        MS-UC-Client:
            vci: MS-UC-Client
            description: Microsoft Lync Client
            option-def:
                parent-option:
                    name: option 43
                    code: 43
                    type: binary
                    array: False
                sub-options:
                    - name: UC Identifier
                        code: 1
                        type: string
                        data: MS-UC-Client
                        array: False
                    - name: URL Scheme
                        code: 2
                        type: string
                        data: https
                        array: False
                    - name: Web Server FQDN
                        code: 3
                        type: string
                        data: epslync01.epsilonhq.local
                        array: False
                    - name: Web Server Port
                        code: 4
                        type: string
                        data: 443
                        array: False
                    - name: Certificate Web Service
                        code: 5
                        type: string
                        data: /CertProv/CertProvisioningService.svc
                        array: False


        ####### CISCO
        # Option 43 sub-option 241

        Cisco AP:
            vci: Cisco AP
            description: Cisco Aironet Series APs
            option-def:
                parent-option:
                    name: option 43
                    code: 43
                    type: binary
                    array: False
                sub-options:
                    - name: Controller IP
                        code: 241
                        type: ipv4_address
                        data: 10.150.1.15,10.150.50.15
                        array: True


        ####### MITEL

        Mitel:
            vci: Mitel
            description: Mitel Phone (prepend 00000403)
            prefix: "00000403"
            option-def:
                parent-option:
                    name: option 125
                    code: 125
                    type: binary
                    array: False
                sub-options:
                    - code: 125
                        type: string
                        data: id:ipphone.mitel.com;call_srv=X;vlan=X;dscp=46;l2p=X;sw_tftp=X
                        data-only: True



License
-------

This project is licensed under the 2-Clause BSD License - please see LICENSE
file for details.

Aknowledgements
---------------

Thanks to John Steele, John Neerdael and Sif for their input and thanks to 
Don Smith for the vendor examples.
