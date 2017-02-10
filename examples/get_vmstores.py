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
from prettytable import PrettyTable

from tintri.common import TintriServerError
from tintri.v310 import Tintri

"""
 This Python script gets vmstore information from a TGC.

 Command usage: get_vmstores server_name userName password

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


# main
if len(sys.argv) < 4:
    print("\nPrints VMstore information.\n")
    print("Usage: " + sys.argv[0] + " server_name user_name password\n")
    sys.exit(1)

server_name = sys.argv[1]
user_name = sys.argv[2]
password = sys.argv[3]

try:
    # instantiate the Tintri server.
    tintri = Tintri(server_name)

    # Get version and product
    version_info = tintri.version
    if (not tintri.is_tgc()):
        raise TintriServerError(0, cause="Tintri server needs to be Tintri Global Center, not a " + product_name)

    preferred_version = version_info.preferredVersion
    print("API Version: " + preferred_version)

except TintriServerError as tse:
    print_error(tse.__str__())
    sys.exit(2)

# VMstore UUID to datastore name.
vmstore_uuid_to_name = {}

# Datastore UUID to datastore information.
ds_uuid_to_info = {}

#-----------------------------------------------------------
# Note: For this script, VMstore UUID equals datastore UUID.
#-----------------------------------------------------------

try:
    # Login to VMstore
    tintri.login(user_name, password)
    
    vmstore_info = tintri.get_vmstores()
    num_vmstores = len(vmstore_info)
    print_info("Number of vmstores = " + str(num_vmstores))

    # Load the VMstore UUID to name table
    for vmstore in vmstore_info:
        vmstore_uuid_to_name[vmstore.uuid.uuid] = vmstore.hostname

    # Get datastore information
    ds_info = tintri.get_datastores()
    num_datastores = len(ds_info)
    print_info("Number of datastores = " + str(num_datastores))
    print ""

    # Loadd up the datastore UUID to datastore information table.
    for ds in ds_info:
        ds_uuid_to_info[ds.uuid.uuid] = ds

    vmstore_table_hdr = ('VMstore Name', 'Time Stamp', 'Total Capacity GiB', 'Used Physical GiB', 'Used Logical GiB')
    vmstore_table = PrettyTable(vmstore_table_hdr)
    vmstore_table.align['VMstore Name'] = "l"
    vmstore_table.align['Time Stamp'] = "l"
    vmstore_table.align['Total Capacity'] = "r"
    vmstore_table.align['Used Physical'] = "r"
    vmstore_table.align['Used Logical'] = "r"

    # Loop over the VMstore UUIDs to get datastore statistics.
    for uuid, name in vmstore_uuid_to_name.items():
        ds = ds_uuid_to_info[uuid]

        collect_time = ds.stat.timeEnd
        total_space = ds.stat.spaceTotalGiB
        used_physical_space = ds.stat.spaceUsedPhysicalGiB
        used_logical_space = ds.stat.spaceUsedGiB

        row = (name, collect_time, total_space, used_physical_space, used_logical_space)
        vmstore_table.add_row(row)

    print(vmstore_table)

except TintriServerError as tse:
    print_error(tse.__str__())
    tintri.logout()
    sys.exit(2)

finally:
    # All pau, log out
    tintri.logout()
