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
import datetime

from tintri.common import TintriServerError
from tintri.v310 import Tintri
from tintri.v310 import VirtualMachineFilterSpec
from tintri.v310 import SnapshotSpec

"""
 This Python script takes a snapshot for the specified VM.

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


# Take a manual snapshot.
def take_snapshot(tintri, vm_uuid, snapshot_name, consistency_type):

    snapshot_spec = SnapshotSpec()
    snapshot_spec.consistency = consistency_type
    snapshot_spec.retentionMinutes = 240  # 4 hours
    snapshot_spec.snapshotName = snapshot_name
    snapshot_spec.sourceVmTintriUUID = vm_uuid 
        
    snapshot_specs = [snapshot_spec]
    
    snapshot_result = tintri.create_snapshot(snapshot_specs)
    print_info(snapshot_name + ": " + snapshot_result[0])
    return


# main
if len(sys.argv) < 5:
    print("\nSnapshot a VM.\n")
    print("Usage: " + sys.argv[0] + " server_name user_name password vm_name [consistency type]\n")
    print("    consistency type can be 'crash' or 'vm'. The default is 'crash'.")
    sys.exit(-1)

server_name = sys.argv[1]
user_name = sys.argv[2]
password = sys.argv[3]
vm_name = sys.argv[4]
if (len(sys.argv) == 6):
    consistency_type = sys.argv[5]
else:
    consistency_type = "crash"

try:
    # Confirm the consistency type.
    if (consistency_type == "crash"):
        consistency_type = "CRASH_CONSISTENT"
    elif (consistency_type == "vm"):
        consistency_type = "VM_CONSISTENT"
    else:
        raise tintri.TintriServerError(0, cause="consistency_type is not 'crash' or 'vm': " + consistency_type)

    # instantiate the Tintri server.
    tintri = Tintri(server_name)

    # Get version and product
    version_info = tintri.version
    product_name = version_info.productName
    print_info("API Version: " + version_info.preferredVersion)

    # Login to VMstore
    tintri.login(user_name, password)

except TintriServerError as tse:
    print_error(tse.__str__())
    sys.exit(2)
    
try:
    # Create query filter to get the VM specified by the VM name.
    vm_filter_spec = VirtualMachineFilterSpec()
    vm_filter_spec.name = vm_name

    vms = tintri.get_vms(filters = vm_filter_spec)

    if vms.filteredTotal == 0:
        raise tintri.TintriServerError(0, cause="VM " + vm_name + " doesn't exist")

    # Get the information from the first item and hopefully the only item.
    vm = vms[0]
    vm_name = vm.vmware.name
    vm_uuid = vm.uuid.uuid

    print_info(vm_name + ": " + vm_uuid)

    # Get the time for the snapshot description.
    now = datetime.datetime.now()
    now_sec = datetime.datetime(now.year, now.month, now.day,
                                now.hour, now.minute, now.second)
    snapshot_name = vm_name + now_sec.isoformat()

    # Take a manual snapshot.
    take_snapshot(tintri, vm_uuid, snapshot_name, consistency_type)

except TintriServerError as tse:
    print_error(tse.__str__())
    tintri.logout()
    sys.exit(3)
    
# log out
tintri.logout()

