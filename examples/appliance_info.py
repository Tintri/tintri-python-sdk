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

"""
 This Python script prints server information.

 Command usage: get_appliance_info <server_name> <userName> <password>

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
    print("\nPrints server information\n")
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
    product_name = version_info.productName

    # Login to VMstore
    tintri.login(user_name, password)

except TintriServerError as tse:
    print_error(tse.__str__())
    sys.exit(2)
    
try:
    print("\nLoading transporter buffers\n")

    # Get all the appliance infomation
    appliance = tintri.get_appliance("default")

    failed_components_resp = tintri.get_appliance_failed_components("default")
    failed_components = failed_components_resp.failedComponents

except TintriServerError as tse:
    print_error(tse.__str__())
    tintri.logout()
    sys.exit(3)
    
# log out
tintri.logout()

# Some basic info
all_flash = False
show_all_flash = False

appliance_info = appliance.info

try:
    all_flash = appliance_info.isAllFlash
    show_all_flash = True
except AttributeError:
    pass


print("Appliance")
table_header = ('Info', 'Value')
table = PrettyTable(table_header)
table.align['Info'] = "l"
table.align['Value'] = "l"

row = ('Product', product_name)
table.add_row(row)

row = ('Model', appliance_info.modelName)
table.add_row(row)

if show_all_flash:
    row = ('All Flash', all_flash)
    table.add_row(row)

long_os_version = appliance_info.osVersion
dash_x = long_os_version.index("-")
os_version = long_os_version[0:dash_x]
row = ('OS version', os_version)
table.add_row(row)

row = ('API version', version_info.preferredVersion)
table.add_row(row)

print(table)
print("")

# Appliance Component info
print("Appliance Components")
table_header = ('Component', 'Status', 'Location')
table = PrettyTable(table_header)
table.align['Component'] = "l"
table.align['Status'] = "l"
table.align['Location'] = "l"

components = appliance.components
for component in components:
    row = (component.type, component.status, component.locator)
    table.add_row(row)

print(table)
print("")

# Show failed components
if (len(failed_components) == 0):
    print("No failed components")
else:
    print("Failed Components")
    table_header = ('Component', 'Serial #', 'Description')
    table = PrettyTable(table_header)
    table.align['Component'] = "l"
    table.align['Serial #'] = "l"
    table.align['Description'] = "l"
    for component in failed_components:
       row = (component.componentType, component.serialNumber, component.description)
       table.add_row(row)
    
    print(table)
print("") 
    
# Show the configured IP address information
table_header = ('IP', 'Service Type', 'Network Bond', 'VLAN ID')
table = PrettyTable(table_header)
table.align['IP'] = 'l'

ip_configs = appliance.configIps
for ip_config in ip_configs:
    row = (ip_config.ip, ip_config.serviceType, ip_config.networkBond, ip_config.vlanId)
    table.add_row(row)

print(table)
print ""

# Now show each controller information
table_header = ('Component', 'Location', 'Status')
nb_table_hdr = ('Port', 'Port Status', 'Role', 'Speed')

# Pull the controller information
controllers = appliance.controllers
for controller in controllers:
    print(controller.locator + ": " + controller.state + " - " + controller.role)
    table = PrettyTable(table_header)
    table.align['Component'] = "l"
    table.align['Location'] = "l"
    table.align['Status'] = "l"

    components = controller.components
    for component in components:
        row = (component.type, component.locator, component.status)
        table.add_row(row)

    print(table)
    print("")

    # Add network information
    network_bonds = controller.networkBonds
    for nb in network_bonds:
        print(controller.locator + ": " + nb.name + ": " + nb.type + ": " + nb.status + ": " + nb.macAddress)
        table = PrettyTable(nb_table_hdr)
        for port in nb.ports:
            port_speed = str(port.maxSpeed) + port.maxUnit
            nb_row = (port.locator, port.status, port.role, port_speed)
            table.add_row(nb_row)
        print(table)

    print("")

# Disks
if (not appliance.disks):
    print("No disk information present")
    sys.exit(0)

print("Disks")
table_header = ('Name', 'Status', 'Type')
table = PrettyTable(table_header)
table.align['Name'] = "l"
table.align['Status'] = "l"
table.align['Type'] = "l"
disks = appliance.disks
for disk in disks:
    if (disk.state == "DISK_STATE_REBUILD"):
        disk_state = disk.state + " (" + str(disk.rebuildPercent) + "%)"
    else:
        disk_state = disk.state
    if disk.diskType:
        row = (disk.locator, disk_state, disk.diskType)
    else:
        row = (disk.locator, disk_state, disk.type)
    table.add_row(row)

print(table)
print("")
