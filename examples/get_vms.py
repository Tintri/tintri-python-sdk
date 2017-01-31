#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2017 Tintri, Inc.
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

"""
 This Python script gets all the VMs using a page size and demostrates various filters.
 The PySDK automatically handles pages.  Paged invocations are useful so that the
 client doesn't have to suck-in all the information at one time.

 Command usage: get_vms_paged server_name userName password [vm_name]

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


# Print VMs with a description.
def print_vms(vms, description):
    count = 1
    done = False
    print description + ": " + str(vms.filteredTotal)

    # Get more VM information until done.
    for vm in vms:
        vm_name = vm.vmware.name
        vm_uuid = vm.uuid.uuid
        print(str(count) + ": " + vm_name + ", " + vm_uuid)
        count += 1
    
    return


# main
if len(sys.argv) < 4:
    print("\nPrints VM information using filters.\n")
    print("Usage: " + sys.argv[0] + " server_name user_name password [VM name]\n")
    print("    If [VM name] is specified, it is used a filter")
    sys.exit(1)

server_name = sys.argv[1]
user_name = sys.argv[2]
password = sys.argv[3]

if len(sys.argv) == 5:
   vm_name_in = sys.argv[4]
else:
    vm_name_in = None

page_size = 50

# instantiate the Tintri server.
tintri = Tintri(server_name)

# Get version and product
version_info = tintri.version
product = version_info.productName
print("Product: " + product + " (" + version_info.preferredVersion + ")")
print ""

try:
    # Login to VMstore
    tintri.login(user_name, password)
    
    vm_filter_spec = VirtualMachineFilterSpec()
    vm_filter_spec.limit = page_size
    
    # Get VMs with page size filter.
    vms = tintri.get_vms(filters = vm_filter_spec)
    if vms.filteredTotal == 0:
        raise TintriServerError(0, cause="No VMs present")
    
    print_vms(vms, "Total")
    print ""
    
    vm_filter_spec.live = "true"
    
    # Repeat with the live filter.
    vms = tintri.get_vms(filters = vm_filter_spec)
    if vms.filteredTotal == 0:
        print_error("No Live VMs present")
    else:
        print_vms(vms, "Live Total")
    print ""
    
    if (vm_name_in):
        vm_filter_spec.name = vm_name_in
    
        # Repeat with name filter.
        vms = tintri.get_vms(filters = vm_filter_spec)
        if vms.filteredTotal == 0:
            print_error("No VMs present with name:" + vm_name_in)
        else:
            print_vms(vms, vm_name_in + " pattern match total")
        print ""
    
except TintriServerError as tse:
    print_error(tse.__str__())
    tintri.logout()
    sys.exit(2)

# All pau, log out
tintri.logout()
