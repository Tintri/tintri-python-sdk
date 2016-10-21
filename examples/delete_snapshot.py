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
from datetime import datetime

from tintri.common import TintriServerError
from tintri.v310 import Tintri
from tintri.v310 import SnapshotFilterSpec

"""
 This Python script deletes the oldest user generated snapshot.

 Command usage: delete_snapshot <server_name> <userName> <password>

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
    print("\nDelete the oldest user generated snapshot.\n")
    print("Usage: " + sys.argv[0] + " server_name user_name password\n")
    sys.exit(-1)

server_name = sys.argv[1]
user_name = sys.argv[2]
password = sys.argv[3]

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
    # Create filter to get the oldest user generated snapshot
    snapshot_filter = SnapshotFilterSpec()
    snapshot_filter.queryType = "TOP_DOCS_BY_TIME"
    snapshot_filter.limit = 1
    snapshot_filter.type = "USER_GENERATED_SNAPSHOT"

    # Get the oldest user generated snapshot
    snapshot_result = tintri.get_snapshots(filters = snapshot_filter)

    number_of_snapshots = snapshot_result.filteredTotal
    print_debug("Number of Snapshots fetched from get Snapshots call to the server " +
      server_name + " is : " + str(number_of_snapshots))

    if number_of_snapshots == 0:
        raise TintriServerError(0, -2, "Cannot proceed, since this are no user generated snapshots")

    snapshot = snapshot_result[0]

    # Collect useful information
    vm_name = snapshot.vmName
    snapshot_uuid = snapshot.uuid.uuid
    raw_create_time = snapshot.createTime
    formatted_time = datetime.fromtimestamp(int(raw_create_time) / 1000).strftime('%Y-%m-%d %H:%M:%S')
    clone_ref_count = snapshot.cloneReferenceCount

    print("Snapshot " + snapshot_uuid + " created on " + formatted_time + " for VM: " + vm_name)
    if clone_ref_count > 0:
        raise TintriServerError(0, -2, "Can't delete oldest snapshot because its clone reference count > 0.")

    try:
        # Let's make sure you want to delete the snapshot
        answer = raw_input("Delete it? (y/n): ")
    except NameError:
        answer = input("Delete it? (y/n): ")

    if answer != 'y':
        tintri.logout()
        print "Snapshot not deleted"
        sys.exit(0)

    # Delete the snapshot
    tintri.delete_snapshot(snapshot_uuid)

except TintriServerError as tse:
    print_error(tse.__str__())
    tintri.logout()
    sys.exit(3)
    
# log out
tintri.logout()

print_info("Successfully deleted " + snapshot_uuid)
 
