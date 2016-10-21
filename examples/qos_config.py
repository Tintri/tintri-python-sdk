#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2015 Tintri, Inc.
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
from tintri.v310 import VirtualMachineFilterSpec
from tintri.v310 import VirtualMachineQoSConfig
from tintri.v310 import MultipleSelectionRequest

"""
 This Python script configures QoS on the first 2 live VMs
 QoS configuration consists of mininum and maximum IOPs.

 This script demostrates multiple ways to modify the QoS.

 Command usage: qos_config <server_name> <userName> <password> <min_iops> <max_iops>

"""

# For exhaustive messages on console, make it to True; otherwise keep it False
debug_mode = False

# Class to hold the VM name, UUID, and QOS information, min and max IOPs.
class VmQosInfo:
    def __init__(self, name, uuid, min_value, max_value):
        self.name = name
        self.uuid = uuid
        self.min_value = min_value  # stored as integer
        self.max_value = max_value  # stored as integer

    def get_name(self):
        return self.name

    def get_uuid(self):
        return self.uuid

    def get_min_qos(self):
        return self.min_value

    def get_max_qos(self):
        return self.max_value

    def set_min_qos(self, new_value):
        self.min_value = new_value

    def set_max_qos(self, new_value):
        self.max_value = new_value

    def __str__(self):
        return ("VM name: " + self.name + " UUID: " + self.uuid +
               " (" + str(self.min_value) + ", " + str(self.max_value) + ")")

# Helper print routines.
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


# Prints was and now QOS values.
def print_qos_info(vm, vm_info):
    
    qos_config = vm_info.qosConfig
    print(vm.get_name() + " was: " + str(vm.get_min_qos()) + ", " + str(vm.get_max_qos()))
    print(vm.get_name() + " now: " + str(qos_config.minNormalizedIops) + ", " + str(qos_config.maxNormalizedIops))


# main
if len(sys.argv) < 6:
    print("\nSets the first 2 VMs QoS values to the specified values, and then returns to the original values.\n")
    print("Usage: " + sys.argv[0] + " server_name user_name password min_value, max_value\n")
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
    product_name = version_info.productName
    if (not tintri.is_vmstore()):
        raise TintriServerError(0, -1, "Tintri server needs to be VMstore, not " + product_name)

    preferredVersion = version_info.preferredVersion
    print("API Version: " + preferredVersion)

    # Login to TGC
    tintri.login(user_name, password)

except TintriServerError as tse:
    print_error(tse.__str__())
    sys.exit(2)
    
try:
    vm_filter_spec = VirtualMachineFilterSpec()
    vm_filter_spec.live = True

    # Prime the VM information pump
    vms = tintri.get_vms(filters = vm_filter_spec)
    num_vms = vms.filteredTotal
    if num_vms == 0:
        raise TintriServerError(0, -2, "No live VMs present")

    print_info(str(num_vms) + " live VMs present")

    if num_vms < 2:
        raise TintriServerError(0, -3, "Need at least 2 VMs")


    # Create the first VM object.
    vm1 = VmQosInfo(vms[0].vmware.name, vms[0].uuid.uuid,
                    vms[0].qosConfig.minNormalizedIops, vms[0].qosConfig.maxNormalizedIops)

    # Create the second VM object.
    vm2 = VmQosInfo(vms[1].vmware.name, vms[1].uuid.uuid,
                    vms[1].qosConfig.minNormalizedIops, vms[1].qosConfig.maxNormalizedIops)

    new_min_qos = int(new_min_value)
    new_max_qos = int(new_max_value)

    # Show using Multi-selection Request 
    # Create new QoS object with the fields to be changed
    modify_qos_info = VirtualMachineQoSConfig()
    modify_qos_info.minNormalizedIops = new_min_qos
    modify_qos_info.maxNormalizedIops = new_max_qos

    # Create the MultipleSelectionRequest object
    MS_Request = MultipleSelectionRequest()
    MS_Request.ids = [vm1.get_uuid(), vm2.get_uuid()]
    MS_Request.newValue = modify_qos_info
    MS_Request.propertyNames = ["minNormalizedIops", "maxNormalizedIops"]

    print_info("Changing min and max QOS values to (" + new_min_value + ", " + new_max_value + ")")

    # Update the min and max IOPs using a multiple selection request.
    tintri.update_vms_qos_config(request = MS_Request)

    # Get VM 1 value to show that it changed.
    vm1_info = tintri.get_vm(vm1.get_uuid())
    print_qos_info(vm1, vm1_info)

    # Get VM 2 value to show that it changed.
    vm2_info = tintri.get_vm(vm2.get_uuid())
    print_qos_info(vm2, vm2_info)

    # Show using a list of VMs.
    vm_uuids = [vm1.get_uuid(), vm2.get_uuid()]

    print_info("Changing max QOS value plus 100")

    # Update the max IOPs again using a list of VM UUIDs, and max_normalized_iops.
    tintri.update_vms_qos_config(vm_uuids, max_normalized_iops = new_max_qos+100)

    # Get VM 1 value to show that it changed.
    vm1_info = tintri.get_vm(vm1.get_uuid())
    print_qos_info(vm1, vm1_info)

    # Get VM 2 value to show that it changed.
    vm2_info = tintri.get_vm(vm2.get_uuid())
    print_qos_info(vm2, vm2_info)

    print_info("Changing min and max QOS values to Original values")

    # Show updating one VM at a time using positional parameters.
    # Update the first VM.
    tintri.update_vms_qos_config([vm1.get_uuid()], vm1.get_min_qos(), vm1.get_max_qos())
    
    # Update the second VM.
    tintri.update_vms_qos_config([vm2.get_uuid()], vm2.get_min_qos(), vm2.get_max_qos())
    
    # Get VM 1 value to show that it back to the original values.
    vm1_info = tintri.get_vm(vm1.get_uuid())
    print_qos_info(vm1, vm1_info)

    # Get VM 2 value to show that it back to the original values.
    vm2_info = tintri.get_vm(vm2.get_uuid())
    print_qos_info(vm2, vm2_info)

except TintriServerError as tse:
    print_error(tse.__str__())
    tintri.logout()
    sys.exit(2)
    
tintri.logout()

