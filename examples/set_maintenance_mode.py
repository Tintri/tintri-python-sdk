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
import time
import datetime

from tintri.common import TintriServerError
from tintri.v310 import Tintri
from tintri.v310 import Appliance
from tintri.v310 import ApplianceMaintenanceMode

"""
 This scripts sets the maintenance mode for a VMstore.

 Command usage: set_maintenance_mode.py <server> <userName> <password> 

"""

# For exhaustive messages on console, make it to True; otherwise keep it False
debug_mode = False
APPLIANCE_URL = "/v310/appliance/default"


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


def my_timezone():
    tz_hours = time.timezone / -3600
    tz_minutes = time.timezone % 3600
    return "{0:0=+3d}:{1:0=2d}".format(tz_hours, tz_minutes)


# Return the DNS primary and secondary IP addresses.
def get_maintenance_mode(server):
    
    maintenance_mode = server.get_appliance_maintenance_mode("default")
    return maintenance_mode


# Print the maintenance mode information.
# If maintenance mode enabled, print the start and end time.
def print_maintenance_mode(maintenance_mode):
    is_enabled = maintenance_mode.isEnabled
    print("Current Maintenance Mode: " + str(is_enabled))
    if (is_enabled):
        print("From: " + maintenance_mode.startTime)
        print("To  : " + maintenance_mode.endTime)
    print""


# Nots the current maintenance mode and sets it interactively
def set_maintenance_mode(server, maint_mode):
    
    is_enabled = maint_mode.isEnabled
    new_is_enabled = not is_enabled
    pline = "Set maintenance mode from " + str(is_enabled) + " to " + str(new_is_enabled) + "? (y/n) "

    try:
        answer = raw_input(pline)
    except NameError:
        answer = input(pline)
    if (answer != "y"):
        print "Maintenance mode not set"
        return

    # Get now and 6 hours from now.  This is what the GUI sets.
    now = datetime.datetime.now()
    add_6 = now + datetime.timedelta(hours=6)
    time_zone = my_timezone()
    now_str = now.isoformat() + time_zone
    add_6_str = add_6.isoformat() + time_zone
    print_debug("Start time: " + now_str)
    print_debug("End time:   " + add_6_str)

    # Create the appliance maintenance mode object.
    new_maint_mode_info = ApplianceMaintenanceMode()

    if (new_is_enabled):
        # Add attributes for enabling.
        new_maint_mode_info.isEnabled =  new_is_enabled
        new_maint_mode_info.endTime =  add_6_str
        new_maint_mode_info.startTime =  now_str
    else:
        # Add attributes for disabling.
        new_maint_mode_info.isEnabled =  new_is_enabled
        
    server.update_appliance(None, "default", maintenance_mode = new_maint_mode_info)
    return 

# main
if len(sys.argv) < 4:
    print("\nSets maintenance mode on the VMstore.\n")
    print("Usage: " + sys.argv[0] + " server user_name password")
    print("   Where: server    - the VMstore name or IP address")
    print("          user_name - an administrative user usually 'admin'")
    print("          password  - the password for User_name")
    print("")
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
    maintenance_mode = get_maintenance_mode(tintri)
    print ""
    print_maintenance_mode(maintenance_mode)

    set_maintenance_mode(tintri, maintenance_mode)

    maintenance_mode = get_maintenance_mode(tintri)
    print ""
    print_maintenance_mode(maintenance_mode)

except TintriServerError as tse:
    print_error(tse.__str__())
    tintri.logout()
    sys.exit(2)
    
    
# All pau, log out
tintri.logout()

