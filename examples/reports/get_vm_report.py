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
import csv
import os.path
import getpass

from tintri.common import TintriServerError
from tintri.v310 import Tintri
from tintri.v310 import VirtualMachineDownloadableReportFilter

"""
 This Python script prints a URL that downloads a CSV report.

 Command usage: get_vm_report.py <server_name> <field_file_name> <csv_file_name>

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


# Gets the fields to be in the report from a file.
def get_fields(field_file_loc):

    fields = []
    
    try:
        if os.path.isfile(field_file_loc):
            with open(field_file_loc,'r') as csv_file:
                csv_list = csv.reader(csv_file)
                for row in csv_list:
                    print_debug(str(row))
                    field = row[0].strip(' ')
                    if (field[0] != '#'):
                        fields.append(field)
        else:
            raise Exception("Could not find file " + field_file_loc)
    
        return fields
    
    except Exception as tre:
        print_error(tre.__str__())
        sys.exit(4)


# main
if len(sys.argv) < 4:
    print("\nDownloads a CSV VM report. \n")
    print("Usage: " + sys.argv[0] + " server_name field_file_name csv_file_name\n")
    print("Where:")
    print("   server_name:     TGC server name or IP address")
    print("   field_file_name: input file name that contains the fields to report")
    print("   csv_file_name:   output report CSV file name")
    print ""
    sys.exit(1)

server_name = sys.argv[1]
field_file_name = sys.argv[2]
csv_file_name = sys.argv[3]

# Get the field attributes to report
attributes = get_fields(field_file_name)
if len(attributes) == 0:
    print_error("No fields specified in " + field_file_name)
    sys.exit(1)

print("Fields to report:\n" + str(attributes))

# Credentials Gathering - support Python 2.X and 3.X
print("")
try: 
	user_name = raw_input("Enter user name: ")
except NameError:
	user_name = input("Enter user name: ")
password = getpass.getpass("Enter password: ")
print("")

# Try to login into the TGC.
try:
    # instantiate the Tintri server.
    tgc = Tintri(server_name)

    # Get version and product
    version_info = tgc.version
    product = version_info.productName
    if product != "Tintri Global Center":
        raise TintriServerError(0, cause="Server needs to be a TGC")

    print_info("API Version: " + version_info.preferredVersion)

    # Login to Tintri server
    tgc.login(user_name, password)

except TintriServerError as tse:
    print_error(tse.__str__())
    sys.exit(2)

    
try:
    # Create the report filter.
    report_filter = VirtualMachineDownloadableReportFilter()
    report_filter.attachment = csv_file_name
    report_filter.attributes = attributes
    report_filter.since = ""
    report_filter.until = ""
    report_filter.format = "CSV"

    # Invoke API to get a useable report URL.
    report_url = tgc.create_vm_list_report(report_filter)

    # Print the URL.
    print("URL: {" + report_url + "} is good for 30 days")
    
    # Get the report.
    tgc.download_file(report_url, csv_file_name)
    
    print(csv_file_name + " is ready")


except TintriServerError as tse:
    print_error(tse.__str__())

finally:
    tgc.logout()
