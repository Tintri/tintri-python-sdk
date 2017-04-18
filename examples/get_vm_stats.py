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
from prettytable import PrettyTable

from tintri.common import TintriServerError
from tintri.v310 import Tintri
from tintri.v310 import VirtualMachineFilterSpec
from tintri.utils import dump_object

"""
 This Python script displays VM stats.

 Displays key VM statistics.  The statistics are from the latest 
 historical statistics that were collected in the last 10 minutes
 or earlier. 

 Command usage: get_vm_status <server_name> <userName> <password>

"""

# For exhaustive messages on console, make it to True; otherwise keep it False
debug_mode = False

# dictionary of VM objects
vms = {}


# Holds VM name, UUID, and statistics.
class VmStat:
    def __init__(self, name, uuid, stats):
        self.name = name
        self.uuid = uuid
        self.stats = stats

    def get_name(self):
        return self.name
    
    def get_uuid(self):
        return self.uuid

    def get_stats(self):
        return self.stats

    def get_stat(self, stat):
        return getattr(self.stats, stat, None)
        

# print functions
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


# Returns a dictionary of live VM objects with statistics using
# the VM name as the key.
def get_vms(session_id, page_size):

    vm_filter_spec = VirtualMachineFilterSpec()
    vm_filter_spec.live = "true"
    vm_filter_spec.limit = page_size
    
    # Repeat with the live filter.
    live_vms = tintri.get_vms(filters = vm_filter_spec)
    if live_vms.filteredTotal == 0:
        raise TintriServerError(0, cause="No live VMs present")

    print_info("Live Total = " + str(live_vms.filteredTotal))
    print ""
    
    count = 1
    for vm in live_vms:
        vm_name = vm.vmware.name
        vm_uuid = vm.uuid.uuid
        if debug_mode:
            dump_object(vm.stat.sortedStats[0])

        vm_stats = VmStat(vm_name, vm_uuid, vm.stat.sortedStats[0])
        print_debug(str(count) + ": " + vm_name + ", " + vm_uuid)
        count += 1
			
        # Store the VM stats object keyed by VM name.
        vms[vm_name] = vm_stats

    return vms


# main
if len(sys.argv) < 4:
    print("\nCollect VM stats")
    print("Usage: " + sys.argv[0] + " server_name user_name password");
    sys.exit(-1)

server_name = sys.argv[1]
user_name = sys.argv[2]
password = sys.argv[3]

# Put it here so that it could be made an input parameter if desired.
page_size = 100

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
    sys.exit(-2)
    
try:
    vms = get_vms(tintri, page_size)

except TintriServerError as tse:
    print_error(tse.__str__())
    tintri.logout()
    sys.exit(-3)
    
print_info("Statistics collected")
tintri.logout()

# Define the statistic fields to display.  The fields can be changed
# without modifying the print code below.  See the API documentation
# for more statistic fields.
stat_fields = ['spaceUsedGiB', 'operationsTotalIops', 'latencyTotalMs']

# Create the table header with the fields
table_header = ["VM name"]
for field in stat_fields:
    table_header.append(field)

table = PrettyTable(table_header)
table.align["VM name"] = "l"

# Build the table rows based on the statistic fields
for key, value in sorted(vms.items()):
    print_debug(key + " " + value.get_uuid())

    # Get the value for each statistic field.
    row = [value.get_name()]
    for field in stat_fields:
        stat = value.get_stat(field)
        if stat is None:
            row.append("---")
        else:
            row.append(stat)
    table.add_row(row)

# Print the table
print(table)
