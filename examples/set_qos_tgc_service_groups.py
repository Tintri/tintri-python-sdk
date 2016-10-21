#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Tintri, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys

from tintri.common import TintriServerError
from tintri.v310 import Tintri
from tintri.v310 import VirtualMachineQoSConfig

"""
 This Python script sets the QoS of the VMs in the first TGC service group with
 more than 2 VMs. 

 Command usage:
 set_qos_tgc_service_groups.py server_name user_name password min_value max_value
 Where:"
     server_name - name of a TGC server
     user_name   - user name used to login into the TGC server
     password    - password for the user
     min_value   - the QoS minimum value for the VM
     max_value   - the QoS maximum value for the VM

"""

# For exhaustive messages on console, make it to True; otherwise keep it False
debug_mode = False


def print_with_prefix(prefix, out):
    print(prefix + out)
    return


def print_debug(out):
    if debug_mode:
        print_with_prefix("[DEBUG] : ", out)
    return


def print_info(out):
    print_with_prefix("[INFO] : ", out)
    return


def print_error(out):
    print_with_prefix("[ERROR] : ", out)
    return


# Sets the Minimum and maximum QoS values on a TGC service group.
def set_qos(tintri, sg_uuid, new_min_value, new_max_value):
    
    # Create new QoS object with the fields to be changed
    modify_qos_info = VirtualMachineQoSConfig()
    modify_qos_info.minNormalizedIops = int(new_min_value)
    modify_qos_info.maxNormalizedIops = int(new_max_value)
    print_debug("IOPS: " + str(modify_qos_info.minNormalizedIops) + ", " + str(modify_qos_info.maxNormalizedIops))
                          
    # Set the QoS in the service group.
    tintri.update_service_group_qos_config(modify_qos_info, sg_uuid)
    
    # Apply the QoS values that were set for the service group above.
    tintri.apply_service_group_qos_config(sg_uuid)


# main
if len(sys.argv) < 6:
    print("\nsets the QoS of the VMs in a TGC service group with more than 2 VMs.\n")
    print("Usage: " + sys.argv[0] + " server_name user_name password min_value max_value\n")
    print("Where:")
    print("    server_name - name of a TGC server")
    print("    user_name   - user name used to login into the TGC server")
    print("    password    - password for the TGC and VMstore users")
    print("    min_value   - the QoS minimum value for the VM")
    print("    max_value   - the QoS maximum value for the VM")
    sys.exit(-1)

server_name = sys.argv[1]
user_name = sys.argv[2]
password = sys.argv[3]
new_min_value = sys.argv[4]
new_max_value = sys.argv[5]

try:
    # instantiate the Tintri server.
    tintri = Tintri(server_name)

    # Get version and product
    version_info = tintri.version
    if (not tintri.is_tgc()):
        raise TintriServerError(0, cause="Tintri server needs to be Tintri Global Center, not a " + product_name)

    preferred_version = version_info.preferredVersion
    print("API Version: " + preferred_version)

    versions = preferred_version.split(".")
    major_version = versions[0]
    minor_version = int(versions[1])
    if major_version != "v310":
        raise TintriServerError(0, cause="Incorrect major version: " + major_version + ".  Should be v310.")
    if minor_version < 31:
        raise TintriServerError(0, cause="Incorrect minor Version: " + minor_version + ".  Should be 31 or greater")

    # Login to TGC
    tintri.login(user_name, password)

except TintriServerError as tse:
    print_error(tse.__str__())
    sys.exit(2)
    
try:
    # Get a list of service groups
    service_groups = tintri.get_service_groups()
    num_service_groups = service_groups.absoluteTotal
    if num_service_groups == 0:
        raise TintriServerError(0, cause="No Service Groups present")
    print_info(str(num_service_groups) + " Service Groups present")

    # Initialze the member list
    sg_uuid = ""
    found = False

    # Look for a qualifying service group
    count = 1
    for sg in service_groups:
        sg_name = sg.name
        sg_uuid = sg.uuid.uuid
        sg_member_count = sg.memberCount
        print_info(str(count) + ": " + sg_name + "(" + str(sg_member_count) + "): " + sg_uuid)
        if sg_member_count >= 2: 
            found = True
            break
        count += 1

    if not found:
        raise TintriServerError(0, cause="No service groups matching the criertia, member count >= 2.")
 
    # Set the QoS on the service group.
    set_qos(tintri, sg_uuid, new_min_value, new_max_value)

except TintriServerError as tse:
    print_error(tse.__str__())
    tintri.logout()
    sys.exit(3)

# All pau, log out
tintri.logout()

