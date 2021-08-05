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
    - pyyaml


Installing the bloxone Module
-----------------------------

The bloxone module can be installed either from source or via PyPi::

	pip3 install bloxone

Source is available from github::

	https://github.com/ccmarris/python-bloxone


User Guide
----------

Help information is available via the --help option::

    % ./dhcp_option_util.py --helpusage: dhcp_option_util.py [-h] [-c CONFIG] 
    [--vendor VENDOR] [--suboptions SUBOPTIONS] [--prefix PREFIX] 
    [--decode DECODE] [--data_only] [--type TYPE] [--dump DUMP]

    DHCP Option Encoding and Decoding Utility

    optional arguments:
    -h, --help            show this help message and exit
    -c CONFIG, --config CONFIG
                            Path to vendor file
    --vendor VENDOR       Vendor Identifier
    --suboptions SUBOPTIONS
                            Sub Options to encode
    --prefix PREFIX       Optional prefix for use with --suboptions
    --decode DECODE       Hex string to decode
    --data_only           Decode hex as 'string' or specified by --type
    --type TYPE           Optional data_type for --decode --data_only
    --dump DUMP           Dump Vendor 


The script allows encoding of DHCP Options through either the use of a YAML
vendor dictionary file, or directly from the CLI.

A sample YAML file *vendor_dict.yaml* is included, whilst the file format is 
described in the :ref:`yaml-format`.

Encoding examples
+++++++++++++++++

Encoding using the YAML vendor dictionary allows you to define both the
structure and the data to encode for one or more vendors. A number of examples
are included in the default *vendor_dict.yamnl* file, with the intention of
adding additional vendors over time.

 
 To process all vendors in the configuration file::

    $ ./dhcp_option_util.py -c vendor_dict.yaml


To process a specific vendor::

    $ ./dhcp_option_util.py -c vendor_dict.yaml --vendor <vendor>


Dump the configuarion of a vendor::

    $ ./dhcp_option_util.py -c vendor_dict.yaml --dump <vendor>


The script also supports direct encoding from the CLI using the *--sub-option*
option. This allows you to specify options using the format::
    
    '<code>:<type>:<data>,<code>:<type>:<data>,<code>:<type>:<data>'


Encode direct from CLI::

    $ ./dhcp_option_util.py --sub-options '1:string:https,2:ipv4_address:10.10.10.10'


Decoding examples
+++++++++++++++++

Decoding will, by default, attempt to decode as a set of encoded sub-options
but will also decode the provided hex as a single data string.

It is also possible to either specify a vendor (using the vendor
dictionary yaml file) or simple <code>:<type> definitions on the CLI using
--suboptions allowing the user to specify the data types used for Decoding
the data types. 

To decode as data only it is possible to use the --data_only option and 
optionally adding the data_type that should be used with --type. (By default
data will be decoded using the string type.)

.. Note: 
    The --sub-option only uses *code* and *type* for decoding. Therefore a
    simpler set can be defined using <code>:<type>,<code>:<type>,...

Examples::

    ./dhcp_option_util.py --decode <hex_string>
    ./dhcp_option_util.py --decode <hex_string> --suboptions '1:string,2:ip'
    ./dhcp_option_util.py --decode <hex_string> --vendor 'MS-UC-Client
    ./dhcp_option_util.py --decode <hex_string> --data_only
    ./dhcp_option_util.py --decode <hex_string> --data_only --type array_of_ip

    
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

Thanks to John Steele, John Neerdael and Sif Baksh for their input and thanks
to Don Smith for the vendor examples.
