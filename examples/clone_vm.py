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
from tintri.v310 import VirtualMachineCloneSpec
from tintri.v310 import VMwareCloneInfo
from utils import dump_object

"""
 This Python script clones a VM.

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


# Clone a VM from a  snapshot of VM UUID.
def clone_vm(uuid, clone_name, vcenter_name, datastore_name, num_clones):

    # Create and initialize the clone spec minus the UUID
    clone_spec = VirtualMachineCloneSpec()
    clone_spec.consistency = 'CRASH_CONSISTENT'
    clone_spec.count = num_clones

    vmware_clone_info = VMwareCloneInfo()
    clone_spec.vmware = vmware_clone_info
    clone_spec.vmware.cloneVmName = clone_name
    clone_spec.vmware.vCenterName = vcenter_name
    clone_spec.vmware.datastoreName = datastore_name

    # Suss-out if UUID is a Tintri VM or snapshot UUID and set the appropriate field.
    if (uuid.find("VIM") > -1):
        clone_spec.vmId = uuid
    elif (uuid.find("SST") > -1):
        clone_spec.snapshotId = uuid
    else:
        raise TintriServerError(0, cause="UUID is not a VM or snapshot UUID: " + uuid)
       
    print_info("Cloning " + uuid + " to " + clone_name + " for " + str(num_clones) + " times")

    if debug_mode:
        dump_object(clone_spec)

    # Clone the VM specified by the clone_payload
    task_result = tintri.clone_vm(clone_spec, True)
    
    # Get the desired task info
    task_uuid = task_result.uuid.uuid
    task_state = task_result.state
    task_progress = task_result.progressDescription
    task_type = task_result.type
    print_info(task_type + ": " + task_uuid + ": " + task_state + " - " + task_progress)


# main
if len(sys.argv) < 6:
    print("\nClones a VM.\n")
    print("Usage: " + sys.argv[0] + " server_name user_name password vm_name clone_name [num_clones]\n")
    sys.exit(-1)

server_name = sys.argv[1]
user_name = sys.argv[2]
password = sys.argv[3]
vm_name = sys.argv[4]
clone_name = sys.argv[5]
if (len(sys.argv) == 7):
    num_clones = sys.argv[6]
else:
    num_clones = 1

try:
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
        raise TintriServerError(0, cause="VM " + vm_name + " doesn't exist")

    # Get the information from the first item and hopefully the only item.
    vm = vms[0]
    vm_name = vm.vmware.name
    vm_uuid = vm.uuid.uuid
    vcenter_name = vm.vmware.vcenterName

    print_info(vm_name + ": " + vm_uuid + " - " + vcenter_name)

    # Since this is the VMstore, default is the datastore name.
    datastore_name = "default"

    host_resources = tintri.get_virtual_machine_host_resources(datastore_name)

    for hr in host_resources:
        if (vcenter_name == hr.hostname and hr.type == "COMPUTE_RESOURCE"):
            found = True
            break

    if (not found):
        raise TintriRequestExeption(0, cause="Host resource " + vcenter_name + " not found")

    print_info("Found " + vcenter_name + " in host resources")
    
    # Clone from the latest snapshot if available.
    try:
        latest_snapshot_uuid = vm.snapshot.latest.uuid.uuid
        clone_vm(latest_snapshot_uuid, clone_name + "_latest", vcenter_name, datastore_name, num_clones)
        print(str(num_clones) + " were cloned from " + vm_name + " latest snapshot")
    except AttributeError:
        pass

    # Take snapshot and clone.
    clone_vm(vm_uuid, clone_name, vcenter_name, datastore_name, num_clones)
    print(str(num_clones) + " were cloned from " + vm_name + "new snapshot")


except TintriServerError as tse:
    print_error(tse.__str__())
    tintri.logout()
    sys.exit(3)
    
# log out
tintri.logout()

