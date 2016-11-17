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
import getpass

from tintri.common import TintriServerError
from tintri.v310 import Tintri

"""
 This scripts reboots or shuts down a VMstore.

 Command usage: reboot_shutdown.py <server> [reboot | shutdown]

"""

# For exhaustive messages on console, make it to True; otherwise keep it False
debug_mode = False


def print_with_prefix(prefix, out):
    print(prefix + out)
    return


def print_debug(out):
    if debug_mode:
        print_with_prefix("[Debug] : ", out)
    return


def print_error(out):
    print_with_prefix("[ERROR] : ", out)
    return


def print_info(out):
    print_with_prefix("[Info] : ", out)
    return


# main
if len(sys.argv) < 3:
    print("\nShutsdown or reboot a VMstore.\n")
    print("Usage: " + sys.argv[0] + " <server> <operation>")
    print("   Where: server    - the VMstore name or IP address.")
    print("          operation - operation to preform. Either 'reboot' or 'shutdown'.")
    print("")
    sys.exit(2)

# Get the input parameters
server = sys.argv[1]
operation = sys.argv[2]

# Assume the user name is admin for reboot or shutdown.
user_name = "admin"

# Read the password
password = getpass.getpass("Enter " + user_name + " password: ")

try:
    # instantiate the Tintri server.
    tintri = Tintri(server)

    # Get version and product. Check the product for VMstore.
    version_info = tintri.version
    product_name = version_info.productName
    if (not tintri.is_vmstore()):
        raise TintriServerError(0, -1, "Tintri server needs to be VMstore, not " + product_name)

    version = version_info.preferredVersion
    print("API Version: " + version)

    # Login to TGC
    tintri.login(user_name, password)

    # Validate and execute the operations.
    if operation == "shutdown":
        print_info("Shuting down " + server)
        tintri.shutdown("default")

    elif operation == "reboot":
        print_info("Rebooting " + server)
        tintri.reboot("default")

    else:
        print_error("Invalid server operation. Only 'reboot' or 'shutdown' is allowed.")

except TintriServerError as tse:
    print_error(tse.__str__())
    tintri.logout()
    sys.exit(3)
    
# All pau, log out
tintri.logout()

