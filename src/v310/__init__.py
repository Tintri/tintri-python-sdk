#
# The BSD License (BSD)
#
# Copyright (c) 2016 Tintri, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#     without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

__author__ = 'Tintri'
__copyright__ = 'Copyright 2016 Tintri Inc'
__license__ = 'BSD'
__version__ = '1.0'

import types
import logging
import collections
import json
import time
from functools import wraps
from ..utils import object_to_json, map_to_object, dump_object, convert_to_camel_case
from ..common import TintriBase, TintriPage, TintriEntity, TintriObject, TintriError
import inspect

class Uuid(object): pass
class Page(TintriObject): pass

class TintriEntityV310(TintriEntity): pass # Base class for verion v310 resource classes   

class Request(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.Request'

    def __init__(self):
        super(Request, self).__init__()
        self.objectsWithNewValues = []
        self.propertiesToBeUpdated = [] # string list

class MultipleSelectionRequest(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.MultipleSelectionRequest'

    def __init__(self):
        super(MultipleSelectionRequest, self).__init__()
        self.newValue = None
        self.ids = []
        self.propertyNames = []
        
class CollectionChangeRequest(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.CollectionChangeRequest'

    def __init__(self):
        super(CollectionChangeRequest, self).__init__()
        self.objectIdsAdded = []
        self.objectIdsRemoved = []

class Response(TintriObject): pass # com.tintri.api.rest.v310.dto.Response

class DateTime(TintriObject): pass

class Access(TintriEntityV310): pass

class Ace(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.fileShare.Ace'
    _url = 'datastore/%s/fileShare/%s/acl'

class Acl(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.fileShare.Acl'
    _property_map = { 'shareDacl': Ace }
    _is_singleton = True
    _url = 'datastore/%s/fileShare/%s/acl'

class AlertFilterProperty(TintriObject): pass
class AlertFilterScopeValue(TintriObject): pass

class AlertFilterScopeValueMap(TintriObject): # Not a Java class
    _property_map = { 'filterProperty': AlertFilterProperty, 'filterScopeValues': AlertFilterScopeValue }

class AlertFilterScope(TintriEntityV310):
    _url = 'alert/filter'
    _is_singleton = True
    _property_map = { 'filterScopeValueMap': AlertFilterScopeValueMap }

class AlertDownloadableReportFilter(TintriEntityV310):
    _url = 'alert/alertListDownloadable'
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.alerts.AlertDownloadableReportFilter'

class Alert(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.Alert'
    _url = 'alert'
    _property_map = { 'uuid': Uuid, 'lastUpdatedTime': DateTime }
    _is_paginated = True

class ApplianceComponent(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.hardware.ApplianceComponent'
    _url = 'appliance/%s/component'

class ApplianceControllerRole(TintriObject): pass
class ApplianceControllerNetworkBond(TintriObject): pass
class DOM(TintriObject): pass

class ApplianceController(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.hardware.ApplianceController'
    _url = 'appliance/%s/controller'
    _property_map = { 'role': ApplianceControllerRole, 'component': ApplianceComponent, 'networkBonds': ApplianceControllerNetworkBond, 'doms': DOM }

class ApplianceCustomizationInfo(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.hardware.ApplianceCustomizationInfo'
    _url = 'appliance/%s/customizationInfo'
    _is_singleton = True

class ApplianceDateTime(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.hardware.ApplianceDateTime'
    _url = 'appliance/%s/dateTime'
    _is_singleton = True

class ApplianceDisk(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.hardware.ApplianceDisk'
    _url = 'appliance/%s/disk'

class ApplianceOperationalInfo(TintriEntityV310): 
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.hardware.ApplianceOperationalInfo'
    _url = 'appliance/%s/operationalStatus'
    _is_singleton = True
    _property_map = { 'sampleTime': DateTime }

class ApplianceDiskEncryptionInfo(TintriEntityV310):
    _url = 'appliance/%s/encryptionInfo'
    _is_singleton = True

class ApplianceDiskEncryptionResult(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.hardware.ApplianceDiskEncryptionResult'

class ApplianceAlertCounts(TintriEntityV310):
    _url = 'appliance/%s/alertCounts'
    _is_singleton = True
    _ignore_plural = True

class ApplianceAllowSnapshotIncompleteVm(TintriObject): pass

class ApplianceDns(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.hardware.ApplianceDns'
    _url = 'appliance/%s/dns'
    _is_singleton = True
    _ignore_plural = True

class ApplianceEmail(TintriEntityV310):
    _url = 'appliance/%s/emailalerts'
    _is_singleton = True
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.hardware.ApplianceEmail'

class ApplianceInfo(TintriEntityV310): 
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.hardware.ApplianceInfo'
    _url = 'appliance/%s/info'
    _is_singleton = True

class ApplianceIp(TintriEntityV310): 
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.hardware.ApplianceIp'
    _url = 'appliance/%s/ips'

class ApplianceIpmi(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.hardware.ApplianceIpmi'
    _url = 'appliance/%s/ipmi'
    _is_singleton = True

class ApplianceLacp(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.hardware.ApplianceLacp'
    _url = 'appliance/%s/lacp'
    _is_singleton = True

class ApplianceMaintenanceMode(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.hardware.ApplianceMaintenanceMode'
    _url = 'appliance/%s/maintenanceMode'
    _is_singleton = True

class ApplianceSnmpUser(TintriEntityV310): 
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.snmp.ApplianceSnmpUser'
    _url = 'appliance/%s/snmpUser'

class ApplianceSnmpTarget(TintriEntityV310): 
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.snmp.ApplianceSnmpTarget'
    _url = 'appliance/%s/snmpTarget'

class ApplianceSnmp(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.snmp.ApplianceSnmp'
    _url = 'appliance/%s/snmp'
    _is_singleton = True
    _property_map = {'users': ApplianceSnmpUser, 'targets': ApplianceSnmpTarget}

class ApplianceSupport(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.hardware.ApplianceSupport'
    _url = 'appliance/%s/support'
    _is_singleton = True

class ApplianceSyslogForwarding(TintriEntityV310): 
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.hardware.ApplianceSyslogForwarding'
    _url = 'appliance/%s/syslogForwarding'
    _is_singleton = True

class ApplianceUpgradeInfo(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.hardware.ApplianceUpgradeInfo'
    _is_singleton = True

class Temperature(TintriEntityV310): 
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.hardware.Temperature'
    _url = 'appliance/%s/temperature'

class Appliance(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.Appliance'
    _url = 'appliance' # need vmstore id
    _property_map = { 
                     'alertCounts': ApplianceAlertCounts, 'allowSnapshotIncompleteVm': ApplianceAllowSnapshotIncompleteVm, 'components': ApplianceComponent,
                     'configIps': ApplianceIp, 'controllers': ApplianceController, 'customizationInfo': ApplianceCustomizationInfo,
                     'dateTimeConfig': ApplianceDateTime, 'disks': ApplianceDisk, 'diskEncryptionInfo': ApplianceDiskEncryptionInfo, 'dnsConfig': ApplianceDns,
                     'emailConfig': ApplianceEmail, 'info': ApplianceInfo, 'ipmiConfig': ApplianceIpmi, 
                     'lacpConfig': ApplianceLacp, 'maintenanceMode': ApplianceMaintenanceMode, 'operationalInfo': ApplianceOperationalInfo,
                     'snmpConfig': ApplianceSnmp, 'supportConfig': ApplianceSupport, 'syslogForwarding': ApplianceSyslogForwarding,
                     'temperatures': Temperature, 'upgradeInfo': ApplianceUpgradeInfo, 'uuid': Uuid }
    
class ApplianceFailedComponent(TintriObject): pass
class ApplianceFailedComponents(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.hardware.ApplianceFailedComponents'
    _url = 'appliance/%s/failedComponents'
    _is_singleton = True
    _property_map = { 'failedComponents': ApplianceFailedComponent }
    _ignore_plural = True

class ApplianceEmailAlerts(TintriEntityV310):
    _url = 'appliance/%s/emailalerts'
    _is_singleton = True
    _ignore_plural = True

class AdsConfig(TintriObject): pass
class LdapConfig(TintriObject): pass
class RbacExternalConfig(TintriEntityV310):
    _url = 'appliance/%s/rbacExternalConfig'
    _is_singleton = True
    _property_map = { 'adsConfig': AdsConfig, 'ldapConfig': LdapConfig }

class ApplianceTintriUuid(TintriObject): pass

class Certificate(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.Certificate'
    _url = 'appliance/%s/certificate'

class ClusterConfiguration(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.ClusterConfiguration'
    _url = 'clusterConfig'
    _is_singleton = True

class CommonStat(TintriObject): pass
class MinMax(TintriObject): pass

class CommonStatFilterScope(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.CommonStatFilterScope'
    _property_map = { 'cloneDedupFactor': MinMax, 'compressionFactor': MinMax, 'dedupFactor': MinMax,
                        'flashHitPercent': MinMax, 'ioAlignedPercent': MinMax, 'latencyContentionMs': MinMax, 'latencyDiskMs': MinMax, 'latencyFlashMs': MinMax, 
                        'latencyHostMs': MinMax, 'latencyStorageMs': MinMax, 'latencyThrottleMs': MinMax, 'latencyTotalMs': MinMax, 'liveLogicalFootprint': MinMax, 
                        'maxNormalizedIops': MinMax, 'minNormalizedIops': MinMax, 'networkLatency': MinMax, 'normalizedTotalIops': MinMax, 'operationsTotalIops': MinMax, 
                        'performanceReserveActual': MinMax, 'performanceReserveChange': MinMax, 'performanceReserveChangePercent': MinMax, 'spaceProvisioned': MinMax, 
                        'spaceSavingsFactor': MinMax, 'spaceUsed': MinMax, 'spaceUsedChangedPercent': MinMax, 'spaceUsedChangeGiB': MinMax, 'spaceUsedChangeMBPerDay': MinMax, 
                        'spaceUsedChangePercent': MinMax, 'spaceUsedPhysical': MinMax, 'spaceUsedSnapshotsHypervisorGiB': MinMax, 'spaceUsedSnapshotsHypervisorPhysicalGiB': MinMax, 
                        'spaceUsedSnapshotsTintriGiB': MinMax, 'spaceUsedSnapshotsTintriPhysicalGiB': MinMax, 'throughputTotalMBps': MinMax, }

class DatastoreNfsAccess(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.nfsaccess.DatastoreNfsAccess'

class DatastoreNfsAccesses(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.nfsaccess.DatastoreNfsAccesses'
    _url = 'datastore/%s/nfsaccess'
    _is_singleton = True
    _property_map = { 'configs': DatastoreNfsAccess }
    _ignore_plural = True

class DatastoreQosInfo(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.DatastoreQoSInfo'
    _url = 'datastore/%s/qosInfo'
    _is_singleton = True

class DatastoreReplicationPathThrottle(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.repl.DatastoreReplicationPathThrottle'

class DatastoreReplicationPath(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.repl.DatastoreReplicationPath'
    _url = 'datastore/%s/replicationPath'
    _property_map = { 'throttle': DatastoreReplicationPathThrottle }
    _is_singleton = True

class DatastoreReplicationInfo(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.DatastoreReplicationInfo'
    _url = 'datastore/%s/replicationInfo'
    _is_singleton = True
    _property_map = { 'pathsIncoming': DatastoreReplicationPath, 'pathsOutgoing': DatastoreReplicationPath }

class ReplicationStat(TintriObject): pass

class DatastoreStat(TintriObject):
    _property_map = { 'replicationIncoming': ReplicationStat, 'replicationOutgoing': ReplicationStat }

class VirtualMachineSnapshotSchedule(TintriEntityV310):
    _url = 'vm/%s/snapshotSchedule'
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.vm.VirtualMachineSnapshotSchedule'
    
    def __init__(self):
        super(VirtualMachineSnapshotSchedule, self).__init__()
        self.consistency = 'CRASH_CONSISTENT'
        self.cronExpressions = []
        self.retentionDestinationMinutes = -1
        self.retentionSourceMinutes = -1
        self.initialDefaultCronExpression = None
        self.initialDefaultRetentionMinutes = None
        self.isSystemDefaultSchedule = None
        self.name = None
        self.type = None

class HypervisorDatastore(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.HypervisorDatastore'
    _url = 'datastore/%s/hypervisorDatastore'

class Datastore(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.Datastore'
    _url = 'datastore'
    _property_map = { 'applianceUuid': ApplianceTintriUuid, 'nfsAccesses': DatastoreNfsAccesses, 'qosInfo': DatastoreQosInfo, 
                     'replication': DatastoreReplicationInfo, 'snapshotSchedules': VirtualMachineSnapshotSchedule,
                     'storageContainers': HypervisorDatastore, 'stat': DatastoreStat, 'uuid': Uuid }

class DatastoreSmbSetting(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.fileShare.DatastoreSmbSettings'
    _url = 'datastore/%s/smbSettings'
    _is_singleton = True

class DatastoreStatDownloadableReportFilter(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.DatastoreStatDownloadableReportFilter'
    def __init__(self):
        super(DatastoreStatDownloadableReportFilter, self).__init__()
        self.attributes = []

class FilterScope(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.FilterScope'
    _url = 'vm/filterScope'

class FilterSpec(TintriObject):
    _attr_l = ['typeId', 'filterAttributeList', 'filterParams', 'name', 'qParams', 'QUERY_JOB_COMPLETION_TIMEOUT_IN_MINUTES_MAX', 'QUERY_TIMEOUT_IN_SEC_DEFAULT', 'QUERY_TIMEOUT_IN_SEC_MAX', 'uuid']
    def __init__(self):
        super(FilterSpec, self).__init__()
        self.addattr(self._attr_l)
            
    def addattr(self, attr_l):
        for attr in attr_l:
            setattr(self, attr, None)

    def to_map(self):
        query_param = {}
        if hasattr(self, '__dict__'):
            for k, v in self.__dict__.iteritems():
                if not self.__dict__[k] is None:
                    query_param[k] = v
        return query_param

class PageFilterSpec(FilterSpec):
    _page_attr_l = ['allStats', 'limit', 'metric', 'offset', 'offsetType', 'offsetValue', 'page', 'queryType', 'refresh', 'replLinkId', 'since', 'sortedBy', 'sortOrder', 'syslogForwarding', 'target', 'timeout', 'until']
    def __init__(self):
        super(PageFilterSpec, self).__init__()
        self.addattr(self._page_attr_l)

class AlertFilterSpec(PageFilterSpec):
    _alert_attr_l = ['message', 'severities', 'severity', 'sources', 'state', 'states']
    def __init__(self):
        super(AlertFilterSpec, self).__init__()
        self.addattr(self._alert_attr_l)

class PolicyErrorStatFilterSpec(PageFilterSpec):
    _policyerror_attr_l = ['serviceGroupUuid', 'vmStoreUuid']
    def __init__(self):
        super(PolicyErrorStatFilterSpec, self).__init__()
        self.addattr(self._policyerror_attr_l)

class SnapshotFilterSpec(PageFilterSpec):
    _ss_attr_l = ['consistency', 'contain', 'deleted', 'fromDate', 'fromVmstore', 'hasClone', 'orphaned', 'removeReplica', 'replica', 'replicaTintriUuids', 'toDate', 'type', 'vmUuid']
    def __init__(self):
        super(SnapshotFilterSpec, self).__init__()
        self.addattr(self._ss_attr_l)

class TaskFilterSpec(PageFilterSpec):
    _task_attr_l = ['id', 'jobTarget', 'jobType', 'state', 'targetId', 'timeoutInSeconds']
    def __init__(self):
        super(TaskFilterSpec, self).__init__()
        self.addattr(self._task_attr_l)

class VirtualEntityFilterSpec(PageFilterSpec):
    _virtualentity_attr_l = ['cloneDedupeFactor', 'compressionFactor', 'dedupeFactor', 'flashHitPercent', 'instanceUuid', 'ioAlignedPercent', 'latencyContentionMs', 'latencyDiskMs', 'latencyFlashMs', 'latencyHostMs',
               'latencyNetworkMs', 'latencyStorageMs', 'latencyThrottleMs', 'latencyTotalMs', 'liveLogicalFootprint', 'performanceReserveAutoAllocated', 'performanceReserveChange', 'performanceReserveChangePercent',
               'performanceReserveUsed', 'requestSizeKiB', 'spaceProvisionedGiB', 'spaceSavingsFactor', 'spaceUsedChangeGiB', 'spaceUsedChangePercent', 'spaceUsedGiB', 'spaceUsedLiveGiB', 'spaceUsedSnapshotsHypervisorGiB',
               'spaceUsedSnapshotsTintriGiB', 'totalIops', 'totalMBps', 'totalNormalizedIops', 'totalUsedSpace']
    def __init__(self):
        super(VirtualEntityFilterSpec, self).__init__()
        self.addattr(self._virtualentity_attr_l)

class VirtualDiskFilterSpec(VirtualEntityFilterSpec):
    _vdisk_attr_l = ['autoAligned', 'displayName', 'isDiskDrive', 'path', 'vmName', 'vmUuid'] 
    def __init__(self):
        super(VirtualDiskFilterSpec, self).__init__()
        self.addattr(self._vdisk_attr_l)

class VirtualMachineFilterSpec(VirtualEntityFilterSpec):
    _vm_attr_l = ['affinityRuleTypes', 'bytesRemainingMB', 'changeMBPerDay', 'cloneFrom', 'cpuPercent', 'cpuReadyPercent', 'cpuSwapWaitPercent', 'datastores', 'deleted', 'hasSnapshots', 'highFrequencySnapshotEnabled', 'host',
               'hosts', 'hypervisorManagerDisplayName', 'hypervisorPath', 'hypervisorPathPrefixes', 'hypervisorType', 'includeComposition', 'lastReplicatedSnapshotDate', 'lastSnapshotDate', 'latestSliceUuid', 'live', 'maxNormalizedIops',
               'migrationBytesRemainingMB', 'migrationDestination', 'migrationThroughputLogicalMBps', 'migrationThroughputPhysicalMBps', 'minNormalizedIops', 'policyErrorCodes', 'powered', 'protections', 'provisionedType', 'qosConfigured',
               'replDestination', 'replicationHasIssue', 'replLinkIds', 'replSource', 'replState', 'serviceGroupId', 'serviceGroupIds', 'serviceGroupName', 'snapshotScheduleType', 'storageContainer', 'storageContainerId', 'subdir', 'template',
               'throughputLogicalMBps', 'throughputPhysicalMBps', 'timeRemainingSeconds', 'types',  'useDefaultSchedule', 'vcenterName', 'vcenterNames'] 
    def __init__(self):
        super(VirtualMachineFilterSpec, self).__init__()
        self.addattr(self._vm_attr_l)

class FileShare(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.FileShare'
    _url = 'datastore/%s/fileShare'
    _id_fields = ['name']

class GenericRestApiRole(TintriEntityV310):
    typeId = 'com.tintri.api.rest.vcommon.dto.rbac.GenericRestApiRole'
    _property_map = { 'lastUpdatedTime': DateTime, 'uuid': Uuid }

class HypervisorManagerConfig(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.HypervisorManagerConfig'
    _url = 'datastore/%s/hypervisorManagerConfig'

class LicenseFeatureType(TintriEntityV310): pass
class LicenseModelType(TintriEntityV310): pass

class License(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.License'
    _url = 'license'
    _property_map = { 'uuid': Uuid, 'feature': LicenseFeatureType, 'model': LicenseModelType }

class LicenseCounts(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.license.LicenseCounts'

class TrialPeriodSummary(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.license.TrialPeriodSummary'
    
class LicenseSummary(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.license.LicenseSummary'
    _url = 'license/summary'
    _is_singleton = True
    _property_map = { 'counts': LicenseCounts, 'trialPeriod': TrialPeriodSummary }

class LicenseDownloadableReportFilter(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.license.LicenseDownloadableReportFilter'

class MigrationStat(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.perf.MigrationStat'

class RestApiAccess(TintriEntityV310): pass

class Privilege(TintriEntityV310):
    _property_map = { 'allowedAccess': RestApiAccess }

class ReplicationPolicy(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.svg.ReplicationPolicy'

class VirtualMachineQoSConfig(TintriObject):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.vm.VirtualMachineQoSConfig'
    
    def __init__(self, min_normalized_iops=None, max_normalized_iops=None, inheritance_enabled=True):
        # Check for invalid inputs
        if min_normalized_iops and min_normalized_iops < 0:
            raise Exception("Parameter min_normalized_iops must be at least 0.")
        elif max_normalized_iops and max_normalized_iops < 0:
            raise Exception("Parameter max_normalized_iops must be at least 0.")
        elif min_normalized_iops > max_normalized_iops:
            raise Exception("Parameter min_normalized_iops cannot be greater than max_normalized_iops.")
        else:
            super(VirtualMachineQoSConfig, self).__init__()
            self.maxNormalizedIops = max_normalized_iops or 0
            self.minNormalizedIops = min_normalized_iops or 0
            self.inheritanceEnabled = inheritance_enabled

class PolicyConfig(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.svg.PolicyConfig'
    _url = "servicegroup/%s/policyConfig"
    _property_map = { 'qosPolicy': VirtualMachineQoSConfig, 'replPolicy': ReplicationPolicy, 'snapshotSchedules': VirtualMachineSnapshotSchedule }
    _is_singleton = True

class RbacTestResult(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.rbac.RbacTestResult'

class RecommendationFeedback(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.loadbalance.recommendation.RecommendationFeedback'

class RecommendationActionResult(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.loadbalance.recommendation.RecommendationActionResult'
    _property_map = { 'completionTime': DateTime, 'lastUpdatedTime': DateTime, 'startedTime': DateTime }

class RecommendationAction(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.loadbalance.recommendation.RecommendationAction'
    _property_map = { 'lastUpdatedTime': DateTime, 'result':RecommendationActionResult }

class RecommendationActionGroup(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.loadbalance.recommendation.RecommendationActionGroup'
    _property_map = { 'actions': RecommendationAction }

class RecommendationFlashOutcome(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.loadbalance.recommendation.RecommendationFlashOutcome'

class RecommendationIopsOutcome(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.loadbalance.recommendation.RecommendationIopsOutcome'
    
class RecommendationSpaceOutcome(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.loadbalance.recommendation.RecommendationSpaceOutcome'

class RecommendationOutcome(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.loadbalance.recommendation.RecommendationOutcome'
    _property_map = { 'lastUpdatedTime': DateTime, 'flashInfo': RecommendationFlashOutcome, 'iopsInfo': RecommendationIopsOutcome, 'spaceInfo': RecommendationSpaceOutcome }

class RecommendationFlashAnalysis(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.loadbalance.recommendation.RecommendationFlashAnalysis'
    
class RecommendationIopsAnalysis(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.loadbalance.recommendation.RecommendationIopsAnalysis'

class RecommendationSpaceAnalysis(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.loadbalance.recommendation.RecommendationSpaceAnalysis'

class RecommendationAnalysis(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.loadbalance.recommendation.RecommendationAnalysis'
    _property_map = { 'lastUpdatedTime': DateTime, 'flashInfo': RecommendationFlashAnalysis, 'iopsInfo': RecommendationIopsAnalysis, 'spaceInfo': RecommendationSpaceAnalysis }

class Recommendation(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.loadbalance.recommendation.Recommendation'
    _property_map = { 'acceptedTime': DateTime, 'acknowledegedTime': DateTime, 'completionTime': DateTime, 'creationTime': DateTime,
                      'expirationTime': DateTime, 'lastUpdatedTime': DateTime, 'actionGroups': RecommendationActionGroup, 'expectedOutcomes': RecommendationOutcome,
                      'feedback': RecommendationFeedback, 'issues': RecommendationAnalysis }
    _url = 'vmstorePool/%s/recommendation'
    _is_paginated = True

class RecommendationIssueSelection(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.loadbalance.recommendation.RecommendationIssueSelection'

class Stats(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.perf.Stats'

class ReplLink(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.ReplLink'
    _property_map = { 'stat': Stats, 'uuid': Uuid, 'linkThrottle': DatastoreReplicationPathThrottle}

class RestApiCredentials(TintriEntityV310):
    typeId = 'com.tintri.api.rest.vcommon.dto.rbac.RestApiCredentials'

class Role(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.Role'
    _url = 'role'
    _property_map = { 'uuid': Uuid, 'privileges': Privilege, 'restrictedAccesses': Access }

class RoleExternal(TintriEntityV310):
    _url = 'role/external'
    typeId = 'com.tintri.api.rest.v310.dto.domain.Role'

class ServiceGroup(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.ServiceGroup'
    _url = 'servicegroup'
    _is_paginated = True

class ServiceGroupMember(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.svg.ServiceGroupMember'
    _url = 'servicegroup/%s/members'
    _is_paginated = True

class ServiceGroupOperationStatus(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.svg.ServiceGroupOperationStatus'
    _url = 'servicegroup/%s/operationStatus'
    _is_singleton = True
    _ignore_plural = True

class ServiceGroupRules(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.svg.ServiceGroupRules'

class SmbConfig(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.SmbConfig'

class SmbTestResult(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.rbac.SmbTestResult'

class Snapshot(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.Snapshot'
    _url = 'snapshot'
    _property_map = { 'uuid': Uuid, 'vmUuid': Uuid }
    _is_paginated = True

class SnapshotSpec(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.snapshot.SnapshotSpec'
    def __init__(self, retention_minutes=None, consistency='CRASH_CONSISTENT', replica_retention_minutes=None, snapshot_name=None, source_vm_id=None):
        super(SnapshotSpec, self).__init__()
        self.retentionMinutes = retention_minutes
        self.consistency = consistency
        self.replicaRetentionMinutes = replica_retention_minutes
        self.snapshotName = snapshot_name
        self.sourceVmTintriUUID = source_vm_id

class SrmConfig(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.svg.srm.SrmConfig'
    _url = 'servicegroup/%s/srmConfig'
    _is_singleton = True

class SvgDownloadableReportFilter(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.svg.SvgDownloadableReportFilter'

class Task(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.Task'
    _url = 'task'
    _property_map = { 'uuid': Uuid }
    _is_paginated = True

class TestReplicationPath(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.repl.TestReplicationPath'

class UserAccount(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.UserAccount'
    _url = 'userAccount'
    _id_fields = ['name', 'password']

class UserAgreement(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.UserAgreement'
    _url = 'userAgreement'
    _is_singleton = True

class UserSession(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.UserSession'
    _property_map = { 'loginTime': DateTime }

class VirtualMachineAffinityRule(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.vm.VirtualMachineAffinityRule'

class VMwareCloneInfo(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.vm.VirtualMachineCloneSpec$VMwareCloneInfo'
    
class HyperVCloneInfo(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.vm.VirtualMachineCloneSpec$HyperVCloneInfo'
    
class RhevCloneInfo(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.vm.VirtualMachineCloneSpec$RhevCloneInfo'

class RemoteCopyInfo(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.vm.VirtualMachineCloneSpec$RemoteCopyInfo'

class RestoreInfo(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.vm.VirtualMachineCloneSpec$RestoreInfo'

class VirtualMachineCloneSpec(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.vm.VirtualMachineCloneSpec'
    _url = 'vm'
    _property_map = { 'vmware': VMwareCloneInfo, 'hyperv': HyperVCloneInfo, 'rhev': RhevCloneInfo, 'remoteCopyInfo': RemoteCopyInfo, 'restoreInfo': RestoreInfo }
    
    def __init__(self):
        TintriEntityV310.__init__(self)
        self.consistency = 'CRASH_CONSISTENT'
        self.count = 1

class VirtualMachineCustomizationScript(TintriEntityV310):
    _url = 'vm/%s/customizationScripts'

class VirtualMachineCustomizationSpec(TintriEntityV310): # TODO add decorator to simplify the required path_params
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.vm.VirtualMachineCustomizationSpec'
    _url = 'datastore/%s/customizationSpec'

class VirtualMachineDownloadableReportFilter(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.vm.VirtualMachineDownloadableReportFilter'

class VirtualMachineHostResource(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.vm.VirtualMachineHostResource'
    _url = 'datastore/%s/hostResources'

class VirtualMachineReplicationConfig(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.repl.VirtualMachineReplicationConfig'
    _property_map = { 'vmUuid': Uuid, 'stat': ReplicationStat, 'path': DatastoreReplicationPath }
    _url = 'vm/%s/replicationConfigs'

    def __init__(self):
        TintriEntityV310.__init__(self)
        self.datastoreUuid = None
        self.vmUuid = None
        self.id = 0
        self.isPaused = False
        self.path = None
        self.isSource = True
        self.alertThresholdMinutes = 3000
        self.replicateParentsRequested = False
        self.isOneshot = False
        self.stat = None
        self.sourceIpAddress = None
        self.isSystemDefault = False
        self.isDisabled = False
        self.isTgcServiceGroupDefault = False

class VirtualMachineReplicationInfo(TintriObject):
    _property_map = { 'configurationsIncoming': VirtualMachineReplicationConfig, 'configurationsOutgoing': VirtualMachineReplicationConfig }

class VirtualMachineServiceGroupInfo(TintriObject): pass

class HighFrequencySnapshotConfig(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.HighFrequencySnapshotConfig'
    _url = 'vm/%s/hfSnapshotConfig'
    def __init__(self, is_enabled=False):
        super(HighFrequencySnapshotConfig, self).__init__()
        self.isEnabled = is_enabled

class VirtualMachineSnapshotInfo(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.vm.VirtualMachineSnapshotInfo'
    _property_map = { 'schedules': VirtualMachineSnapshotSchedule, 'highFrequencySnapshotConfig': HighFrequencySnapshotConfig, 'latest': Snapshot }

class VirtualMachineStat(TintriEntityV310):
    _property_map = { 'uuid': Uuid, 'replication': ReplicationStat }
    _is_paginated = True
    _url = None # For subclass use only.

class VirtualMachineStatDownloadableReportFilter(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.vm.VirtualMachineStatDownloadableReportFilter'
    def __init__(self):
        super(VirtualMachineStatDownloadableReportFilter, self).__init__()
        self.attributes = []
    
class VirtualMachineSyncTakeSnapshotSpec(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.vm.VirtualMachineSyncSpec$VirtualMachineSyncTakeSnapshotSpec'

class VirtualMachineSyncVmConfig(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.vm.VirtualMachineSyncSpec$VirtualMachineSyncVmConfig'
  
class VirtualMachineVmwareSyncSpec(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.vm.VirtualMachineSyncSpec$VirtualMachineVmwareSyncSpec'
 
class VirtualMachineSyncSpec(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.vm.VirtualMachineSyncSpec'
    _url = 'vm/sync'
    _property_map = { 'takeSnapshotSpec': VirtualMachineSyncTakeSnapshotSpec, 'vmConfig': VirtualMachineSyncVmConfig, 'vmwareSpec': VirtualMachineVmwareSyncSpec }
  
    def __init__(self):
        TintriEntityV310.__init__(self)
        self.snapshotTintriUuid = None
        self.targetVmTintriUuids = []

class VirtualDisk(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.VirtualDisk'
    _is_paginated = True
    _property_map = { 'lastUpdatedTime': DateTime, 'datastoreUuid': Uuid, 'stat': CommonStat, 'syncVmConfig': VirtualMachineSyncVmConfig, 'uuid': Uuid, 'vmUuid': Uuid }

class Stat(TintriObject):
    _property_map = { 'sortedStats': VirtualMachineStat }

class VirtualMachineVmwareInfo(TintriObject): pass

class Vm(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.VirtualMachine'
    _property_map = { 'qosConfig': VirtualMachineQoSConfig, 'replication': VirtualMachineReplicationInfo, 'serviceGroup': VirtualMachineServiceGroupInfo,
                     'snapshot': VirtualMachineSnapshotInfo, 'stat': Stat, 'uuid': Uuid, 'vmware': VirtualMachineVmwareInfo}
    _is_paginated = True

class VmFilterScope(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.VmFilterScope'
    _url = 'vm/filter'
    _property_map = { 'opterationsTotalIops': MinMax, 'normalizedTotalIops': MinMax, 'minNormalizedIops': MinMax, 'maxNormalizedIops': MinMax,
                        'throughputTotalMBps': MinMax, 'latencyTotalMs': MinMax, 'latencyHostMs': MinMax, 'latencyStorageMs': MinMax, 'latencyDiskMs': MinMax,
                        'latencyContentionMs': MinMax, 'latencyFlashMs': MinMax, 'latencyThrottleMs': MinMax, 'flashHitPercent': MinMax, 'spaceProvisioned': MinMax,
                        'spaceUsedSnapshotsTintriGiB': MinMax, 'spaceUsedSnapshotsTintriPhysicalGiB': MinMax, 'spaceUsedSnapshotsHypervisorGiB': MinMax,
                        'spaceUsedSnapshotsHypervisorPhysicalGiB': MinMax, 'spaceUsedChangeGiB': MinMax, 'spaceUsedChangePercent': MinMax, 'spaceUsedChangeMBPerDay': MinMax,
                        'performanceReserveActual': MinMax, 'performanceReserveChange': MinMax, 'performanceReserveChangePercent': MinMax, 'ioAlignedPercent': MinMax, 
                        'spaceSavingsFactor': MinMax, 'cloneDedupFactor': MinMax, 'dedupFactor': MinMax, 'liveLogicalFootprint': MinMax, 'spaceUsedChangedPercent': MinMax, 
                        'compressionFactor': MinMax, 'cpuPercent': MinMax, 'readyPercent': MinMax, 'swapWaitPercent': MinMax, 'spaceUsed': MinMax, 'networkLatency': MinMax,
                        'spaceUsedPhysical': MinMax }

class VmPolicyErrorStat(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.VmPolicyErrorStat'
    _url = 'vm/policyErrorStat'
    _is_paginated = True

class VmstoreSessionStatusInfo(TintriObject): pass

class VmStoreCredentials(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.VmStoreCredentials'

class Vmstore(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.VmStore'
    _url = 'vmstore'
    _property_map = { 'applianceInfo': ApplianceInfo, 'sessionStatusInfo': VmstoreSessionStatusInfo, 'credentials': VmStoreCredentials }

class VMstoreDownloadableReportFilter(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.VMstoreDownloadableReportFilter'

class VmstorePool(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.VmstorePool'
    _url = 'vmstorePool'
    _property_map = { 'lastUpdatedTime': DateTime, 'stat': VmstoreSessionStatusInfo, 'uuid': Uuid }
    _is_paginated = True

class VmstorePoolStat(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.perf.VmstorePoolStat'
    _property_map = { 'migration': MigrationStat, 'replicationIncoming': ReplicationStat, 'replicationOutgoing': ReplicationStat, 'uuid': Uuid}
    
class VmstorePoolDownloadableReportFilter(TintriEntityV310):
    typeId = 'com.tintri.api.rest.v310.dto.domain.beans.VmstorePoolDownloadableReportFilter'

def _get_request_object(attributes_d, attributes_l, obj_class):
    if 'request' in attributes_d and attributes_d['request']:
        return attributes_d['request']

    # remove non attributes
    if 'request' in attributes_d:
        del attributes_d['request']
    for item in attributes_l:
        del attributes_d[item]

    # prepare object and fill in attributes
    obj = obj_class()
    request = Request()
    for key, value in attributes_d.iteritems():
        setattr(obj, convert_to_camel_case(key, capitalize_first_letter=False), value)

    # prepare request
    request.objectsWithNewValues = [obj]
    request.propertiesToBeUpdated = []
    for key, value in list(attributes_d.items()):
        if value is not None:
            request.propertiesToBeUpdated.append(convert_to_camel_case(key, capitalize_first_letter=False))
    return request

# Use this decorator for all apis. For usage, please see get_vm
# Anytime resource is added/updated, keep the decorated apis consistent
def api(func=None, filter_class=None, target="all", version="all"):
    def is_plural(func):
        if not func.func_name.endswith('s'):
            return False

        resource = "_".join(func.func_name.split("_")[1:])
        resource = convert_to_camel_case(resource)
        if resource not in func.func_globals:
            return True
        
        resource_class = func.func_globals[resource]
        if hasattr(resource_class, '_ignore_plural') and resource_class._ignore_plural:
            return False

        return True

    def get_resource_class_from_func_name(func_name, func):
            """Figure out resource class name using function name"""
            if func_name in ["get_appliance_timezones"]:
                return None
            obj_str = convert_to_camel_case("_".join(func_name.split("_")[1:]))
            return func.func_globals[obj_str]

    def get_op(func):
        if func.func_name.startswith('get'):
            if is_plural(func):
                return 'get_all', func.func_name[:-1]
            else:
                return 'get_one', func.func_name
        elif func.func_name.startswith('create'):
            return 'create', func.func_name
        elif func.func_name.startswith('delete'):
            return 'delete', func.func_name
        elif func.func_name.startswith('update'):
            return 'update', func.func_name
        else:
            raise TintriError("Unknown API operation: %s" % func.func_name)

    def wrap(func):
        def verify_filter(api_filter, filter_class):
            if filter_class and not type(api_filter) is dict and not type(api_filter) is filter_class:
                raise Exception("Invalid filter spec, filter should be a map or of type %s" % str(filter_class))   

        def verify_target(api_target, tintri_obj):
            if api_target.lower() == "tgc" and tintri_obj.is_vmstore():
                raise TintriError("API applicable to TGC only")
            if api_target.lower() == "vmstore" and tintri_obj.is_tgc():
                raise TintriError("API applicable to VMstore only")
        
        def verify_version(api_version, tintri_obj):
            if version.lower() != "all" and not version in tintri_obj.version.supportedVersionSet:
                raise TintriError("Unsupported API, please check API minimum version")

        def is_generated_function(func, tintri_obj):
            if len(tintri_obj._generated_function.func_code.co_code) == len(tintri_obj._generated_function_with_doc.func_code.co_code):
                if len(func.func_code.co_code) == len(tintri_obj._generated_function.func_code.co_code):
                    return func.func_code.co_code == tintri_obj._generated_function.func_code.co_code or func.func_code.co_code == tintri_obj._generated_function_with_doc.func_code.co_code
                return False
            else:
                if len(func.func_code.co_code) == len(tintri_obj._generated_function.func_code.co_code):
                    return func.func_code.co_code == tintri_obj._generated_functiontion.func_code.co_code
                elif len(func.func_code.co_code) == len(tintri_obj._generated_function_with_doc.func_code.co_code):
                    return func.func_code.co_code == tintri_obj._generated_function_with_doc.func_code.co_code
                return False

        def is_property_updateable(key, value, data):
            ret = False
            if value is not None and key != 'id' and key != 'uuid' and key != 'typeId':
                ret = True
                if hasattr(type(data), '_id_fields') and key in type(data)._id_fields:
                    ret = False
            return ret

        @wraps(func)
        def wrapped(*args, **kwargs):
            data = None
            query_params = {}
            filters = None
            path_params = []
            response_class = None

            tintri_obj = args[0]
            
            # verify target and version before proceeding
            verify_target(target, tintri_obj)
            verify_version(version, tintri_obj)

            if not is_generated_function(func, tintri_obj):
                return func(*args, **kwargs)
            
            if 'filters' in kwargs:
                verify_filter(kwargs['filters'], filter_class)
                filters = kwargs['filters']
                del kwargs['filters']

            if 'query_params' in kwargs:
                query_params = kwargs['query_params']
                del kwargs['query_params']
                
            op_type, actual_func_name = get_op(func)
            resource_class = get_resource_class_from_func_name(actual_func_name, func)
            request_class = resource_class
            if resource_class._is_paginated:
                response_class = resource_class

            if len(args) > 1:
                path_params = list(args[1:])
            if op_type == "create":
                # first argument is data
                data = path_params.pop(0)
            elif op_type == "update":
                '''
                first argument is considered as data
                1. If data is not None, construct Request from data
                2. If data is None, Request is not None, use Request as data
                3. If data is None, and Request is None, construct Request from kwargs
                '''
                if len(path_params) == 0:
                    raise TypeError("Incorrect usage of API, please provide either updated object or Request object or set properties")
                data = path_params.pop(0)
                if data is None:
                    if 'request' in kwargs and kwargs['request']:
                        data = kwargs['request']
                    else:
                        if len(kwargs):
                            data = _get_request_object(kwargs, [], resource_class)
                        else:
                            # obj, Request and kwargs are None
                            raise TintriError("Incorrect usage of API, please provide either updated object or Request object or set properties")
                else:
                    if 'request' in kwargs:
                        # construct Request from data
                        request = Request()
                        # prepare request
                        request.objectsWithNewValues = [data]
                        request.propertiesToBeUpdated = []
                        for key, value in data.__dict__.iteritems():
                            # ignore None, ID and UUID keys; ignore name key for FileShare
                            if is_property_updateable(key, value, data):
                                request.propertiesToBeUpdated.append(key)
                        data = request
                dump_object(data, logger=tintri_obj.logger)

            if op_type.lower() == "get_one":
                return tintri_obj._get_one(path_params=path_params, query_params=query_params, filters=filters, request_class=request_class, response_class=response_class)
            elif op_type.lower() == "get_all":
                return tintri_obj._get_all(path_params=path_params, query_params=query_params, filters=filters, request_class=request_class, response_class=response_class)
            elif op_type.lower() == "create":
                return tintri_obj._create(data, path_params=path_params, query_params=query_params, filters=filters, request_class=request_class, response_class=response_class)
            elif op_type.lower() == "delete":
                return tintri_obj._delete(path_params=path_params, query_params=query_params, filters=filters, request_class=request_class, response_class=response_class)
            elif op_type.lower() == "update":
                return tintri_obj._update(data, path_params=path_params, query_params=query_params, filters=filters, request_class=request_class, response_class=response_class)
            else:
                raise TintriError("Unrecognized request op_type %s" % op_type)
        return wrapped

    def get_method_doc_string(func):

        def get_param_desc(param):
            param_desc = ''
            if param.endswith('id'):
                for word in param.split("_")[:-1]:
                    param_desc = param_desc + word.capitalize()
                    param_desc = param_desc + ' '
                param_desc = param_desc + "Object's UUID"
            else:
                for word in param.split("_"):
                    param_desc = param_desc + word.capitalize()
                    param_desc = param_desc + ' '
            return param_desc

        op_type, actual_func_name = get_op(func)
        resource_class = get_resource_class_from_func_name(actual_func_name, func)
        doc_string = "Invalid doc string."

        # Get text based on API verb.
        if op_type == 'get_all':
            doc_string = "Gets all " + resource_class.__name__ + "s, and returns them in a Page object."
        elif op_type == 'get_one':
            doc_string = "Gets a specific " + resource_class.__name__ + " object by its ID."
        elif op_type == 'create':
            doc_string = "Creates %s " % ("an" if resource_class.__name__[0] in 'aeiouAEIOU' else "a") + resource_class.__name__ + " object." 
        elif op_type == 'update':
            doc_string = "Updates the " + resource_class.__name__ + " object specified by its ID."
        elif op_type == 'delete':
            doc_string = "Deletes the " + resource_class.__name__ + " object specified by its ID."

        # Get which Tintri server is supported.
        doc_string += "\n\n**Supported on:** "
        if target == "tgc":
            doc_string += "TGC"
        elif target == "vmstore":
            doc_string += "VMstore"
        elif target == "all":
            doc_string += "VMstore and TGC"
        if version == "all":
            doc_string += " (all versions)"
        else:
            doc_string+= " (since %s)" % version

        # Get input arguments.
        obj_name = ""
        param_l = inspect.getargspec(func)[0]
        param_l.remove("self")
        if param_l:
            doc_string += "\n\nArgs:"
        for param in param_l:
            if param == "filters":
                doc_string += "\n\tfilters (dict or `%s`): Filter Spec object" % filter_class.__name__
            elif param == "query_params":
                doc_string += "\n\tquery_params (dict): Specify query parameters as a dictionary"
            elif param == "request":
                doc_string += "\n\trequest (`Request`<`%s`>): %s request" % (resource_class.__name__, resource_class.__name__)
            else:
                if param == 'obj':
                    # Special case for create_acl.
                    if actual_func_name == "create_acl":
                        obj_name = "Ace"
                    else:
                        obj_name = resource_class.__name__
                    doc_string += "\n\tobj (`%s`): An instance of %s." % (obj_name, resource_class.__name__)
                else:
                    doc_string += "\n\t"
                    doc_string += param + " (str): "
                    doc_string += get_param_desc(param)

        if not param_l:
            doc_string += "\n\n"
        
        # Get return output.
        if op_type == 'get_all':
            if resource_class._is_paginated:
                doc_string = doc_string + "\nReturns:\n\t`Page`: Paginated `" + resource_class.__name__ + "` objects."
            else:
                doc_string = doc_string + "\nReturns:\n\tList[`" + resource_class.__name__ + "`]: A list of " + resource_class.__name__ + " objects."
        elif op_type == 'get_one':
            doc_string = doc_string + "\nReturns:\n\t`" + resource_class.__name__ + "`: The " + resource_class.__name__ + " with the specified ID."
        elif (op_type == 'create') and (len(param_l) >= 1) and (param_l[0] == 'obj'):
            doc_string += "\nReturns:\n\t`" + obj_name + "`: The " + obj_name + " object created."

        return doc_string

    if func is None:
        def decorator(func):
            if not func.__doc__ and not 'internal' in func.__module__:
                func.__doc__ = get_method_doc_string(func)
            TintriBase.method_registry[func.func_name] = func
            return wrap(func)
        return decorator

    if not func.__doc__ and not 'internal' in func.__module__:
        func.__doc__ = get_method_doc_string(func)
    TintriBase.method_registry[func.func_name] = func

    return wrap(func)

class Tintri(TintriBase):
    """Tintri class which provides APIs to interact with Tintri Server."""
    # Utility methods
    def _get_param(self, params, kwargs):
        for param in params:
            if param in kwargs:
                return param
        return None

    def _get_vm_id(self, **kwargs):
        return self._get_param(['vm', 'id'], **kwargs)

    def _wait_for_task(self, taskuuid, refreshInterval=3):
        def is_job_done(task):
            return task.state in ['CANCELLED', 'FAILED', 'SUCCESS'];

        task = self.get_task(taskuuid)
        while not is_job_done(task):
            #self.__logger.debug('Waiting for task %s to complete' % task.uuid.uuid)
            time.sleep(refreshInterval)
            task = self.get_task(task.uuid.uuid)
        return task

    def _process_page(self, json_object, entity_class, context={}):
        if 'typeId' in json_object and json_object['typeId'] == 'com.tintri.api.rest.v310.dto.Page':
            json_items = json_object.pop('items', None)
            items = []
            if json_items:
                for item in json_items:
                    items.append(self._json_object_to_object(item, entity_class, False))

            return TintriPage(paginated=entity_class._is_paginated, auto_page=self.auto_page, items=items, context=context)
        else:
            raise ValueError('Not a page object')

    def _to_map(self, filter_spec):
        if not filter_spec: return {}
        if isinstance(filter_spec, dict):
            return filter_spec
        return filter_spec.to_map()
    
    def _to_query_params(self, query_params, filters):
        if filters is None and query_params is None: return {}
        if filters is None: return query_params
        ret = {}
        ret.update(query_params)
        ret.update(self._to_map(filters))
        return ret

    def _generated_function(self, filters=None, query_params={}): pass

    def _generated_function_with_doc(self, filters=None, query_params={}):
        """
        Sample documentation
        """
        pass

    def _get_one(self, path_params=[], query_params={}, filters=None, resource_url=None, request_class=None, response_class=None, name=None):
        return self._send_http_request('GET', path_params, self._to_query_params(query_params, filters), resource_url, request_class, response_class)

    def _get_all(self, path_params=[], query_params={}, filters=None, resource_url=None, request_class=None, response_class=None, name=None):
        return self._send_http_request('GET', path_params, self._to_query_params(query_params, filters), resource_url, request_class, response_class)

    def _create(self, obj, path_params=[], query_params={}, filters=None, resource_url=None, request_class=None, response_class=None, name=None):
        return self._send_http_request('POST', path_params, self._to_query_params(query_params, filters), resource_url, request_class, response_class, data=obj)

    def _update(self, obj, path_params=[], query_params={}, filters=None, resource_url=None, request_class=None, response_class=None, name=None):
        return self._send_http_request('PUT', path_params, self._to_query_params(query_params, filters), resource_url, request_class, response_class, obj)

    def _patch(self, obj, path_params=[], query_params={}, filters=None, resource_url=None, request_class=None, response_class=None, name=None):
        return self._send_http_request('PATCH', path_params, self._to_query_params(query_params, filters), resource_url, request_class, response_class, obj)

    def _delete(self, path_params=[], query_params={}, filters=None, resource_url=None, request_class=None, response_class=None, name=None):
        return self._send_http_request('DELETE', path_params, self._to_query_params(query_params, filters), resource_url, request_class, response_class)

    @api(target="tgc")
    def create_historic_stats_report(self, datastore_id, report_filter):
        """
        Create a URL for retrieving the system historical performance statistics report which is returned as output.

        **Supported on:** TGC (all versions)

        Args:
            datastore_id (str): Datastore object's UUID
            report_filter (`DatastoreStatDownloadableReportFilter`): filter for generating the report

        Returns:
            str: URL to retrieve historic datastore statistics report
        """
        return self._create(report_filter, path_params=[datastore_id], resource_url="datastore/%s/statsDownloadable", request_class=types.StringType)

    @api(target="vmstore", version="v310.41")
    def create_certificate(self, appliance_id):
        """
        Generate new self-signed host certificate with hostname and IP address in the Subject Alternative Name extension on VMstore.

        **Supported on:** TGC (since v310.41)

        Args:
            appliance_id (str): Appliance object's UUID
        """
        return self._create(None, path_params=[appliance_id], resource_url='%s/generate' % Certificate._url)

    # Alerts
    @api(target="tgc")
    def create_alert_report(self, report_filter):
        """
        Gets the URL for retrieving specified alert report.

        **Supported on:** TGC (all versions)

        Args:
            repot_filter (`AlertDownloadableReportFilter`): filter for generating report

        Returns:
            str: URL to retrieve alert list report
        """
        return self._create(report_filter, resource_url="alert/alertListDownloadable", request_class=types.StringType)

    @api(target="tgc")
    def get_alert_filter_scope(self):
        """
        Returns alert properties as specified by a filter request such as VMstore names and log message count.

        **Supported on:** TGC (all versions)

        Returns:
            FilterScope: filter scope
        """
        return self._get_all(resource_url='alert/filter', response_class=FilterScope)

    @api
    def update_alerts(self, objs, properties_to_update, request=None):
        """
        Updates the specified properties by values of passed alerts instance, either specify updated alerts or Request Alert object

        **Supported on:** VMstore and TGC (all versions)

        Args:
            objs (List[`Alert`]): List of Updated Alert objects
            properties_to_update (List[str]): List of properties to update
            request (`Request`<`Alert`>): Alert Request object
        """
        if request is None:
            request = Request()
            request.objectsWithNewValues = objs
            request.propertiesToBeUpdated = properties_to_update
        return self._update(request, resource_url="alert")

    @api(filter_class=PageFilterSpec)
    def get_appliance(self, appliance_id, filters=None):
        """
        Gets Tintri Appliance properties

        **Supported on:** VMstore and TGC (all versions)

        Args:
            appliance_id (str): Appliance object's UUID. ("default") is valid.
            filters (dict or `PageFilterSpec`): Filter Specification object.

        Returns:
            `Appliance`: One appliance instance
        """
        appliances = self._get_one(path_params = [appliance_id], request_class=Appliance, filters=filters)
        if appliances and len(appliances) == 1: return appliances[0]
        else: return None

    @api
    def get_appliance_timezones(self, appliance_id):
        """
        Returns list of time zones supported by the server

        **Supported on:** VMstore and TGC (all versions)

        Args:
            appliance_id (str): Appliance object's UUID

        Returns:
            List[str]: List of string representation of time zones
        """
        return self._get_one(path_params = [appliance_id], resource_url="appliance/%s/timezones")
    
    @api
    def get_appliance_upgrade_info(self, appliance_id):
        """
        Gets the Tintri appliance upgrade information, which includes upgrade state, checksum, version, error message. This is asynchronous information

        **Supported on:** VMstore and TGC (all versions)

        Args:
            appliance_id (str): Appliance object's UUID

        Returns:
            `ApplianceUpgradeInfo`: Appliance upgrade information
        """
        return self._get_one(path_params=[appliance_id], resource_url="appliance/%s/upgradeInfo", request_class=ApplianceUpgradeInfo)

    @api
    def get_certificate(self, appliance_id=None, certificate_id=None):
        """
        Returns certificate(s) that matche the certificate ID or empty collection if not found.

        **Supported on:** VMstore and TGC (all versions)

        Args:
            appliance_id (str): Appliance object's UUID
            certificate_id (str): Certificate Object's UUID

        Returns:
            `Certificate`: Certificate if found, else None
        """
        certs = self._get_one(path_params = [appliance_id, certificate_id], request_class=Certificate)
        if certs and len(certs) == 1: return certs[0]
        else: return None
    
    @api
    def add_certificate(self, appliance_id, cert):
        """
        Upload a certificate to VMStore.

        **Supported on:** VMstore and TGC (all versions)

        Args:
            appliance_id (str): Appliance object's UUID
            cert (`Certificate`): An instance of Certificate
        """
        return self._update(cert, path_params=[appliance_id], resource_url='appliance/%s/certificate', request_class=Certificate)
    
    @api(target="vmstore")
    def enable_disk_encryption(self, appliance_id):
        """
        Enables disk encryption.

        **Supported on:** VMstore (all versions)

        Args:
            appliance_id (str): Appliance object's UUID

        Returns:
            `ApplianceDiskEncryptionResult`: Appliance disk encryption result
        """
        return self._create(None, [appliance_id], resource_url='appliance/%s/enableEncryption', request_class=ApplianceDiskEncryptionResult)

    @api
    def mark_alerts_archived(self):
        """
        Marks all non-archived alerts to archived.

        **Supported on:** VMstore and TGC (all versions)
        """

        return self._update(None, resource_url='alert/markArchived')
    
    @api
    def mark_alerts_read(self):
        """
        Marks all non-acknowledged alerts to acknowledged.

        **Supported on:** VMstore and TGC (all versions)
        """
        return self._update(None, resource_url='alert/markRead')

    @api
    def test_email(self, appliance_id, email):
        """
        Tests alert email. An email is sent to the configured alert email address.

        **Supported on:** VMstore and TGC (all versions)

        Args:
            appliance_id (str): Appliance object's UUID
            email (`ApplianceEmail`): email

        Returns:
            Response: Response to indicate if test email is successful or not
        """
        if 'v310.41' in self.version.supportedVersionSet:
            url = 'appliance/%s/testEmail'
        else:
            url = 'appliance/%s/action=testEmail'
        return self._create(email, resource_url=url, path_params=[appliance_id], request_class=Response)

    @api(target="vmstore")
    def test_snmp(self, appliance_id, username=None, targets=None, users=None, request=None):
        """
        Send a SNMP test trap to a remote trap receiver host, provide either request object or set params.

        **Supported on:** VMstore (all versions)

        Args:
            appliance_id (str): Appliance object's UUID
            username (str): Active SNMP user name
            targets (List[`ApplianceSnmpTarget`]): SNMP trap targets and their settings
            users (List[`ApplianceSnmpUser`]): SNMP users and their settings
            request (`Request`<`ApplianceSnmp`>): ApplianceSnmp request

        Returns:
            Response: Formatted error message if operation fails
        """
        if 'v310.41' in self.version.supportedVersionSet:
            url = 'appliance/%s/testSNMP'
        else:
            url = 'appliance/%s/action=testSNMP'
        return self._create(_get_request_object(locals(), ["self", "appliance_id"], ApplianceSnmp), 
                            resource_url=url, path_params=[appliance_id], request_class=Response)

    @api(target="vmstore")
    def test_syslog_forwarding(self, appliance_id, remote_host=None, request=None):
        """
        Send a test log forwarding message to the remote host, provide either request or remote host.

        **Supported on:** VMstore (all versions)

        Args:
            appliance_id (str): Appliance object's UUID
            remote_host (str): remote host name or IP address for syslog forwarding
            request (`Request`<`ApplianceSyslogForwarding`>): ApplicaneSysLogForwarding request
        """
        if 'v310.41' in self.version.supportedVersionSet:
            url = 'appliance/%s/testSyslogForwarding'
        else:
            url = 'appliance/%s/action=testSyslogForwarding'
        return self._create(_get_request_object(locals(), ["self", "appliance_id"], ApplianceSyslogForwarding), 
                            resource_url=url, path_params=[appliance_id], request_class=Response)

    @api
    def test_rbac_external_config(self, config, appliance_id):
        """
        Tests the external directory service authentication configuration.

        **Supported on:** VMstore and TGC (all versions)

        Args:
            config (`RbacExternalConfig`): Rbac external config
            appliance_id (str): Appliance object's UUID

        Returns:
            List[`RbacTestResult`]: List of test results
        """
        return self._create(config, path_params=[appliance_id], resource_url='appliance/%s/testRbacExternalConfig', request_class=RbacTestResult)
    
    @api(target="vmstore")
    def test_replication_path(self, datastore_id, destinationIp=None, destionationPassphrase=None, destionationPort=None, sourceIp=None, testType=None, request=None):
        """
        Tests the specified replication path on the specified datastore, provide either request or set other params.

        **Supported on:** VMstore (all versions)

        Args:
            datastore_id: Datastore object's UUID
            destinationIp: Remote IPv4 address of another datastore where replication data is received.
            destionationPassphrase: Authorization key used on the remote end of this replication link.
            destionationPort: Remote port of another datastore where replication data is received.
            sourceIp: Local IPv4 address used by datastore to send replication data.
            testType: Test to perform
            request: TestReplicationPath request
        """
        if 'v310.41' in self.version.supportedVersionSet:
            url = "datastore/%s/testReplicationPath"
        else:
            url = "datastore/%s/replicationPath/test"
        self._update(_get_request_object(locals(), ["self", "datastore_id"], TestReplicationPath),
                     path_params = [datastore_id], resource_url=url, request_class=types.StringType)

    @api(target="vmstore", version="v310.11")
    def test_smb_config(self, datastore_id, smb_config):
        """
        Tests SMB host name configuration

        **Supported on:** VMstore (since v310.11)

        Args:
            datastore_id (str): Datastore object's UUID
            smb_config (`SmbConfig`): SMB configuration

        Returns:
            List[`SmbResult`]: List of test results
        """
        return self._update(smb_config, path_params=[datastore_id], resource_url="datastore/%s/testSmbConfig", response_class=SmbTestResult)

    @api(version="v310.41")
    def upgrade(self, appliance_id):
        """
        Starts the Tintri appliance upgrade

        **Supported on:** VMstore and TGC (since v310.41)

        Args:
            appliance_id (str): Appliance object's UUID

        Returns:
            `Response`: Response to indicate if request is successful or not
        """
        return self._create(None, path_params=[appliance_id], resource_url="appliance/%s/upgrade", request_class=Response)

    # Snapshot
    @api(filter_class=SnapshotFilterSpec, target="vmstore")
    def delete_snapshots(self, filters=None):
        """
        Removes snapshots that matches given snapshot filter criteria.

        **Supported on:** VMstore (all versions)

        Args:
            filter (dict or `SnapshotFilterSpec`): Filter criteria for the snapshots to be removed.

        Returns:
            str: Formatted string
        """
        return self._delete(resource_url='snapshot', filters=filters)

    @api(target="vmstore", version="v310.21")
    def get_virtual_disk_from_snapshot(self, snapshot_id):
        """
        Fetches disks of a snapshot. Only these two attributes are populated: - name (example: scsi0:0) - path (example: "ttvm23-vm19000/ttvm23-vm19000.vmdk")

        **Supported on:** VMstore (since v310.21)

        Args:
            snapshot_id (str): The snapshot ID.

        Returns:
            List[`VirtualDisk`]: List of VirtualDisk objects of snapshot.
        """
        return self._get_all(resource_url='snapshot/%s/disks', path_params=[snapshot_id], response_class=VirtualDisk)

    # Task
    @api(target="vmstore")
    def acknowledge_task(self, task_id):
        """
        Acknowledge a job

        **Supported on:** VMstore (all versions)

        Args:
            task_id (str): The ID of the Task to be acknowledged.
        """
        return self._update(None, resource_url='task/%s/acknowledge', path_params=[task_id])

    # Virtual Machine
    @api(target="vmstore")
    def clone_vm(self, clonespec, wait=False, refreshInterval=3):
        """
        Clone a VM

        **Supported on:** VMstore (all versions)

        Args:
            clonespec (`VirtualMachineCloneSpec`): Clone spec
            wait (bool): True if wait for clone VM task to complete, False otherwise
            refreshInterval (int): interval to refresh task status
        Returns:
            str: task ID
        """
        # Need to specify resource_url, because otherwise Task._url will be used
        task = self._create(clonespec, resource_url=VirtualMachineCloneSpec._url, response_class=Task)
        if not wait:
            return task
        else:
            return self._wait_for_task(task.uuid.uuid, refreshInterval)

    @api(target="vmstore", version="v310.21")
    def sync_vm(self, syncspec):
        """
        Synchronize virtual machine to one of its snapshots.

        **Supported on:** VMstore (since v310.21)

        Args:
            syncspec (`VirtualMachineSyncSpec`): Sync spec

        Returns:
            Task: Task object
        """
        return self._create(syncspec, resource_url=VirtualMachineSyncSpec._url, response_class=Task)

    @api(target="vmstore", version="v310.31")
    def delete_vm_sync_disks(self, vm_ids):
        """
        Delete all the virtual disks that restored via SyncVM File-Level Restore operation for each of the targeted virtual machine.

        **Supported on:** VMstore (since v310.31)

        Args:
            vm_ids (List[str]): A list of Virtual Macine object's UUID
        """
        return self._update(vm_ids, resource_url='vm/deleteSyncDisks')

    @api(target="vmstore", version="v310.21")
    def update_vms_qos_config(self, vm_ids=None, min_normalized_iops=None, max_normalized_iops=None, request=None):
        """
        Updates the QoS configuration for all specified VMs, either specify properties in a MultipleSelectionRequest object or set the properties to be updated.

        **Supported on:** VMstore (since v310.21)

        Args:
            vm_ids (List[str]): A list of Virtual Macine object's UUID
            min_normalized_iops (int): VM's minimum configured IOPS. If using default QoS, the minimum normalized IOPS value will be zero.
            max_normalized_iops (int): VM's maximum configured IOPS. If using default QoS, the maximum normalized IOPS value will be zero.
            request (`MultipleSelectionRequest`<`VirtualMachineQoSConfig`>): A MultipleSelectionRequest object populated with updated values.
        """
        if request is None:
            request = MultipleSelectionRequest()
            request.ids = vm_ids
            request.propertyNames = []
            vm_qos_config = VirtualMachineQoSConfig()
            if min_normalized_iops is not None:
                request.propertyNames.append('minNormalizedIops')
                vm_qos_config.minNormalizedIops = min_normalized_iops
            if max_normalized_iops is not None:
                request.propertyNames.append('maxNormalizedIops')
                vm_qos_config.maxNormalizedIops = max_normalized_iops
            request.newValue = vm_qos_config

        return self._update(request, path_params=[], resource_url='vm/qosConfig')

    @api(version="v310.21")
    def update_vm_qos_config(self, obj, vm_id, min_normalized_iops=None, max_normalized_iops=None, request=None):
        """
        Update QoS per VM, either specify properties in a Request VirtualMachineQoSConfig object or set the properties to be updated.

        **Supported on:** VMstore and TGC (since v310.21)

        Args:
            obj (`VirtualMachineQoSConfig`): Updated VirtualMachineQoSConfig object
            vm_id (str): VM object's UUID
            min_normalized_iops (int): min IOPS
            max_normalized_iops (int): max IOPS
            request (`Request`<`VirtualMachineQoSConfig`>): VirtualMachineQoSConfig request
        """
        return self._update(_get_request_object(locals(), ["self", "vm_id"], VirtualMachineQoSConfig),
                            path_params=[vm_id], resource_url="vm/%s/qosConfig")

    @api
    def update_vm_snapshot_schedule(self, obj, vm_id=None, consistency=None, cron_expressions=None, initial_default_cron_expression=None, initial_default_retention_minutes=None,
                                    is_system_default_schedule=None, name=None, retention_destination_minutes=None, retention_source_minutes=None, type=None, version=None,
                                    is_tgc_service_group_default=None, request=None):
        """
        Update VM snapshot schedule properties, either specify properties in a Request VirtualMachineSnapshotSchedule object or set the properties to be updated.

        **Supported on:** VMstore and TGC (all versions)

        Args:
            obj (`VirtualMachineSnapshotSchedule`): Updated VirtualMachineSnapshotSchedule object
            vm_id (str): VM object's UUID
            consistency (str): Snapshot consistency
            cron_expressions (str): A list of cron expressions describing snapshot schedule
            initial_default_cron_expression (str): Quartz cron format
            initial_default_retention_minutes (int): The intial defautlt retention time in minutes.
            is_system_default_schedule (bool): True if the schedule name matches any of the default schedule names, False otherwise
            name (str): User assigned name
            retention_destination_minutes (int): length of time in minutes the snapshot replica on the replication destination is to be retained
            retention_source_minutes (int): Number of minutes, a snapshot generated as per this schedule is to be retained
            type (str): Schedule type to indicate whether it is hourly, daily, weekly, monthly or quarterly.
            version (str): version 
            is_tgc_service_group_default (bool): Boolean value indicates if the requested Snapshot Schedule is Service Group default from TGC.
            request (`Request`<`VirtualMachineSnapshotSchedule`>): VirtualMachineSnapshotSchedule request
        """
        return self._update(_get_request_object(locals(), ["self", "vm_id"], VirtualMachineSnapshotSchedule),
                            path_params=[vm_id], resource_url="vm/%s/snapshotSchedule")

    @api
    def update_vm_snapshot_schedule_to_default(self, vm_ids):
        """
        Update the outgoing replication configurations for the specified VMs to the system default replication configuration. 
        This will first clean up the existing outgoing replication configurations, before applying the system default replication configuration to the VM.

        **Supported on:** VMstore and TGC (all versions)

        Args:
            vm_ids (List[str]): A list of VM IDs.
        """
        self._update(vm_ids, resource_url='vm/updateScheduleToDefault')

    @api(target="vmstore", version="v310.11")
    def convert_vm_to_thin_provision(self, vm_ids):
        """
        Convert a collection of VMs and all their files to thin-provisioning for maximum space savings. 
        If a VM is already thin-provisioned, then it will be skipped. This operation is only allowed on 
        T800 series or newer models of VMStore and supported for VMs originating from VMWare Hypervisor only.

        **Supported on:** VMstore (since v310.11)

        Args:
            vm_ids (List[str]): A list of VM IDs.
        """
        return self._update(vm_ids, resource_url='vm/thinProvision')

    @api(target="vmstore", version="v310.21")
    def update_hf_snapshot_config(self, obj, vm_id, is_enabled=None, request=None):
        """
        Update the VM high frequency snapshot configuration properties, either specify properties in a Request HighFrequencySnapshotConfig object or set the properties to be updated.

        **Supported on:** VMstore (since v310.21)

        Args:
            obj (`HighFrequencySnapshotConfig`): Updated HighFrequencySnapshotConfig object
            vm_id (str): VM object's UUID
            is_enabled (bool): True if HFS is to be enabled, False otherwise
            request (`Request`<`HighFrequencySnapshotConfig`>): HighFrequencySnapshotConfig request
        """
        return self._update(_get_request_object(locals(), ["self", "vm_id"], HighFrequencySnapshotConfig),
                            path_params=[vm_id], resource_url='vm/%s/hfSnapshotConfig')

    @api(target="vmstore", version="v310.21")
    def pin_vm(self, vm_id):
        """
        Operation will pin the VM to Flash storage in case of hybrid platform. This operation is not advisable. It may degrade the system performance.

        **Supported on:** VMstore (since v310.21)

        Args:
            vm_id (str): VM Object's UUID.
        """
        self._update(None, resource_url='vm/%s/pin', path_params=[vm_id])

    @api(target="vmstore", version="v310.21")
    def unpin_vm(self, vm_id):
        """
        Un-pin VM from Flash storage in case of hybrid platform. Pinning operation is not advised.

        **Supported on:** VMstore (since v310.21)

        Args:
            vm_id (str): VM Object's UUID.
        """
        self._update(None, resource_url='vm/%s/unpin', path_params=[vm_id])

    @api(filter_class=VirtualMachineFilterSpec)
    def get_vm_historic_stats(self, vm_id, filters=None):
        """
        Gets the historic VM performance slice containing all of the statistics for the VM specified by query parameters.

        **Supported on:** VMstore and TGC (all versions)

        Args:
            vm_id (str): VM Object's UUID.
            filter (dict or `VirtualMachineFilterSpec`): dictionary or VirtualMachineFilterSpec to filter vms

        Returns:
            `Page`: Paginated `Stats` items containing a list of `VirtualMachineStat`.
        """
        return self._get_all(resource_url='vm/%s/statsHistoric', path_params=[vm_id], response_class=VirtualMachineStat, filters=filters)

    @api(filter_class=VirtualMachineFilterSpec, target="vmstore")
    def get_vm_realtime_stats(self, vm_id, filters=None):
        """
        Gets the real time VM performance slice containing all of the statistics for the VM.

        **Supported on:** VMstore (all versions)

        Args:
            vm_id (str): VM Object's UUID.
            filter (dict or `VirtualMachineFilterSpec`): dictionary or VirtualMachineFilterSpec to filter vms

        Returns:
            `Page`: Paginated `Stats` items containing a list of `VirtualMachineStat`.
        """
        return self._get_all(resource_url='vm/%s/statsRealtime', path_params=[vm_id], response_class=VirtualMachineStat, filters=filters)
    
    # Replication
    @api(target="vmstore")
    def update_vm_replication_config(self, vm_id, replication_configs):
        """
        Update the outgoing replication configurations for the VM specified by the guven vmId to the new replication configurations specified.

        **Supported on:** VMstore (all versions)

        Args:
            vm_id (str): VM Object's UUID
            replication_configs (List[`VirtualMachineReplicationConfig`]): A list of VirtualMachineReplicationConfig objects
        """
        self._update(replication_configs, resource_url=VirtualMachineReplicationConfig._url % vm_id)

    @api(version="v310.21")
    def update_vm_replication_config_to_default(self, vm_ids):
        """
        Update the outgoing replication configurations for the specified VMs to the system default replication configuration. 
        This will first clean up the existing outgoing replication configurations, before applying the system default replication configuration to the VM.

        **Supported on:** VMstore and TGC (since v310.21)

        Args:
            vm_ids (List[str]): A list of VM IDs.
        """
        return self._update(vm_ids, resource_url='vm/updateReplicationConfigToDefault')

    @api(target="vmstore", version="v310.51")
    def delete_vm_incoming_replication_config(self, vm_id):
        """
        Delete incoming replication configuration for a VM.

        **Supported on:** VMstore (since v310.51)

        Args:
            vm_id (str): VM object's UUID
        """
        return self._delete(path_params=[vm_id], resource_url="vm/%s/replicationConfig/incoming")

    # Datastore
    @api(target="vmstore", version="v310.31")
    def get_hypervisor_managers_from_ad(self, datastore_id):
        """
        Find potential Hyper-V hosts from Active Directory that this Datastore can manage.

        **Supported on:** VMstore (since v310.31)

        Args:
            datastore_id (str): Datastore object's UUID

        Returns:
            List[`HypervisorManagerConfig`]: A list of Hyper-V hosts.
        """
        return self._get_all(datastore_id, resource_url='datastore/%s/hypervisorManagersFromAD', response_class=HypervisorManagerConfig)

    @api
    def get_vm_replication_config_from_datastore(self, datastore_id):
        """
        Returns the system-wide replication configuration.

        **Supported on:** VMstore and TGC (all versions)

        Args:
            datastore_id (str): Datastore object's UUID

        Returns:
            `VirtualMachineReplicationConfig`: The system-wide replication configuration.
        """
        return self._get_all(datastore_id, resource_url='datastore/%s/replicationConfig', response_class=VirtualMachineReplicationConfig)

    @api(target="vmstore")
    def update_vm_replication_config_from_datastore(self, datastore_id, replication_config):
        """
        Update the system replication configuration, for example, from system disabled to system enabled. While applying the system default replication configuration 
        to the VMs, the VMs with a custom outgoing replication configuration will be ignored. In addition to this, a VM which has an incoming replication configuration, 
        or is a part of service group or is not live and does not have any snapshot or has snapshots but its latest snapshot is a replica, will be marked as 
        ineligible for system default configuration, and a disabled system default replication configuration will be added for such a VM instead.

        **Supported on:** VMstore (all versions)

        Args:
            datastore_id (str): Datastore object's UUID
            replication_config (`VirtualMachineReplicationConfig`): The updated VirtualMachineReplicationConfig object.
        """
        return self._update(replication_config, path_params=[datastore_id], resource_url='datastore/%s/replicationConfig')

    @api(target="vmstore")
    def get_distinct_vm_snapshot_schedules(self, datastore_id):
        """
        Gets a list of distinct snapshot schedules, including the system default snapshot schedules. The system default snapshot schedules will be listed at the top of the list.

        **Supported on:** VMstore (all versions)

        Args:
            datastore_id (str): Datastore object's UUID

        Returns:
            List[`VirtualMachineSnapshotSchedule`]: A list of snapshot schedules.
        """
        return self._get_all(datastore_id, resource_url='datastore/%s/schedulesDistinct', response_class=VirtualMachineSnapshotSchedule)

    @api(filter_class=PageFilterSpec)
    def get_datastore_historic_stats(self, datastore_id, filters=None):
        """
        Gets the historic datastore performance slices containing all of the statistics for the datastore.

        **Supported on:** VMstore and TGC (all versions)

        Args:
            datastore_id (str): Datastore object's UUID

        Returns:
            `Page`: Paginated `Stats` items containing a list of `DatastoreStat`.
        """
        return self._get_all(datastore_id, resource_url='datastore/%s/statsHistoric', response_class=Page, filters=filters)

    @api(filter_class=PageFilterSpec)
    def get_datastore_realtime_stats(self, datastore_id, filters=None):
        """
        Gets the real time datastore performance slice containing all of the statistics for the datastore.

        **Supported on:** VMstore and TGC (all versions)

        Args:
            datastore_id (str): The datastore UUID.

        Returns:
            `Page`: Paginated `Stats` items containing a list of `DatastoreStat`.
        """
        return self._get_all(datastore_id, resource_url='datastore/%s/statsRealtime', response_class=Page, filters=filters)

    @api
    def get_datastore_summary_stats(self, datastore_id):
        """
        Gets the latest historic datastore performance slice containing all of the statistics for the datastore.

        **Supported on:** VMstore and TGC (all versions)

        Args:
            datastore_id (str): The datastore UUID.

        Returns:
            `DatastoreStat`: The latest statistics for the datastore.
        """
        return self._get_all(datastore_id, resource_url='datastore/%s/statsSummary', response_class=Page)

    @api(target="vmstore", version="v310.21")
    def ping_hypervisor_managers(self, datastore_id, hypervisor_manager_configs):
        """
        Ping hypervisor managers configured on the Datastore

        **Supported on:** VMstore (since v310.21)

        Args:
            datastore_id (str): Datastore object's UUID
            hypervisor_manager_configs (List[`HypervisorManagerConfigs`]): A list of HypervisorManagerConfigs
        Returns:
            List[`HypervisorManagerConfig`]: Status of the ping calls to hypervisor managers.
        """
        return self._create(hypervisor_manager_configs, request_class=HypervisorManagerConfig, resource_url='datastore/%s/hypervisorManagerStatus', path_params=[datastore_id])

    @api(target="vmstore")
    def update_datastore_replication_info(self, obj, datastore_id, passphrase=None, port=None, paths_incoming=None, request=None):
        """
        Updates the specified replication properties on the specified datastore instance by the incoming replication properties instance, either specify properties in a Request DatastoreReplicationInfo object or set the properties to be updated.

        **Supported on:** VMstore (all versions)

        Args:
            obj (`DatastoreReplicationInfo`): Updated DatastoreReplicationInfo object
            datastore_id (str): Datastore object's UUID
            passphrase (str): Authorization key of this datastore which will be used to validate when another datastore attempts to setup replication with this datastore as the destination.
            port (int): Local listening port of the replication destination which is a 16-bit unsigned integer ranging from 1 to 65535.
            paths_incoming (List[`DatastoreReplicationPath`]): List of incoming replication paths for this datastore.
            request (`Request`<`DatastoreReplicationInfo`>): DatastoreReplicationInfo request
        """
        if request is None:
            request = Request()
            replication_config = self.get_datastore_replication_info('default')
            replication_config.passphrase = passphrase or replication_config.passphrase
            replication_config.port = port or replication_config.port
            replication_config.pathsIncoming = paths_incoming or replication_config.pathsIncoming
            request.objectsWithNewValues = [ replication_config ]
            kwargs = { 'passphrase': passphrase, 'port': port, 'paths_incoming': paths_incoming }
            for key, value in list(kwargs.items()):
                if value is not None:
                    request.propertiesToBeUpdated.append(key)

        return self._update(request, request_class=DatastoreReplicationInfo, resource_url='datastore/%s/replicationInfo', path_params=[datastore_id])

    @api(target="vmstore")
    def update_datastore_snapshot_schedule(self, datastore_id, snapshot_schedule):
        """
        Updates system snapshot schedule

        **Supported on:** VMstore (all versions)

        Args:
            datastore_id (str): Datastore object's UUID
        """
        return self._update(snapshot_schedule, path_params=[datastore_id], resource_url="datastore/%s/schedulesDefault")

    # Virtual Disk
    @api(filter_class=VirtualDiskFilterSpec, target="vmstore")
    def get_virtual_disk_filter_scope(self, filters=None):
        """
        Return virtual disk filter scope.

        **Supported on:** VMstore (all versions)

        Args:
            filter (dict or `VirtualDiskFilterSpec`): A dictionary or VirtualDiskFilterSpec that filters the returned results.

        Returns:
            `CommonStatFilterScope`: A CommonStatFilterScope object.
        """
        return self._get_all(resource_url='virtualDisk/filter', response_class=CommonStatFilterScope, filters=filters)

    @api(target="vmstore", version="v310.21")
    def pin_virtual_disk(self, vm_id, virtual_disk_id):
        """
        Operation will pin the Virtual Disk of the VM to Flash storage in case of hybrid platform. This operation is not advisable. It may degrade the system performance.

        **Supported on:** VMstore (since v310.21)

        Args:
            vm_id (str): The virtual machine ID.
            virtual_disk_id (str): The virtual disk ID.
        """
        return self._update(None, resource_url='virtualDisk/%s/%s/pin', path_params=[vm_id, virtual_disk_id])

    @api(target="vmstore", version="v310.21")
    def unpin_virtual_disk(self, vm_id, virtual_disk_id):
        """
        Operation will unpin the Virtual Disk of the VM from Flash storage in case of hybrid platform. Pinning operation is not advisable.

        **Supported on:** VMstore (since v310.21)

        Args:
            vm_id (str): The virtual machine ID.
            virtual_disk_id (str): The virtual disk ID.
        """
        return self._update(None, resource_url='virtualDisk/%s/%s/unpin', path_params=[vm_id, virtual_disk_id])

    @api(filter_class=VirtualDiskFilterSpec, target="vmstore")
    def get_virtual_disk_historic_stats(self, vm_id, virtual_disk_id, filters=None):
        """
        Performance historic trend data for the virtual disk.

        **Supported on:** VMstore (all versions)

        Args:
            vm_id (str): The virtual machine ID.
            virtual_disk_id (str): The virtual disk ID.
            filter (dict or `VirtualDiskFilterSpec`): A dictionary or VirtualDiskFilterSpec that filters the returned results.

        Returns:
            `Page`: Paginated `Stats` items containing a list of `CommonStat`.
        """
        return self._get_all(resource_url='virtualDisk/%s/%s/statsHistoric', path_params=[vm_id, virtual_disk_id], response_class=Page, filters=filters)

    @api(filter_class=VirtualDiskFilterSpec, target="vmstore")
    def get_virtual_disk_realtime_stats(self, vm_id, virtual_disk_id, filters=None):
        """
        Latest performance trend data for the virtual disk.

        **Supported on:** VMstore (all versions)

        Args:
            vm_id (str): The virtual machine ID.
            virtual_disk_id (str): The virtual disk ID.
            filter (dict or `VirtualDiskFilterSpec`): A dictionary or VirtualDiskFilterSpec that filters the returned results.

        Returns:
            `Page`: Paginated `Stats` items containing a list of `CommonStat`.
        """
        return self._get_all(resource_url='virtualDisk/%s/%s/statsRealtime', path_params=[vm_id, virtual_disk_id], response_class=Page, filters=filters)

    # Appliance
    @api(target="vmstore")
    def get_appliance_snmp_targets(self, appliance_id):
        """
        Get all the SNMP trap targets information. Currently, only one trap target is supported.

        **Supported on:** VMstore (all versions)

        Args:
            appliance_id (str): The appliance ID.
        Returns:
            `Response`: The list of all the SNMP trap target configurations.
        """
        return self._get_one(resource_url='appliance/%s/snmpTarget', path_params=[appliance_id], response_class=Response)

    @api(target="vmstore")
    def get_appliance_snmp_users(self, appliance_id):
        """
        Gets SNMP users.

        **Supported on:** VMstore (all versions)

        Args:
            appliance_id (str): The appliance ID.
        Returns:
            `Response`: The list of all the SNMP user configurations.
        """
        return self._get_one(resource_url='appliance/%s/snmpUser', path_params=[appliance_id], response_class=Response)

    @api
    def get_timezones(self, appliance_id):
        """
        Returns list of all time zones supported by the server. Time zone follows standard format - <Country>/<Region> For more details about latest time zones, Please refer to - http://www.iana.org/time-zones

        **Supported on:** VMstore and TGC (all versions)

        Args:
            appliance_id (str): The appliance ID.
        Returns:
            List[str]: The list of string representation of time zones.
        """
        return self._get_all(resource_url='appliance/%s/timezones', path_params=[appliance_id])

    @api
    def update_appliance(self, obj, appliance_id, alert_counts=None, allow_snapshot_incomplete_vm=None, components=None, config_ips=None, controllers=None, customization_info=None, date_time_config=None, disks=None, disk_encryption_info=None, dns_config=None, email_config=None, info=None, ipmi_config=None, lacp_config=None, maintenance_mode=None, operational_info=None, rbac_external_config=None, snmp_config=None, support_config=None, syslog_forwarding=None, temperatures=None, upgrade_info=None, request=None):
        """
        Updates Tintri Appliance's specified properties, either specify updated object or properties in a Request VMstore object or set the properties to be updated.

        **Supported on:** VMstore and TGC (all versions)

        Args:
            obj (`Appliance`): Updated Appliance object
            appliance_id (str): Appliance Object's UUID
            alert_counts (`ApplianceAlertCounts`): Tintri Appliance's number of notifications from the boot
            allow_snapshot_incomplete_vm (`ApplianceAllowSnapshotIncompleteVm`): Tintri Appliance allow snapshot incomplete VM information
            components (List[`ApplianceComponent`]): List of hardware components in the appliance chassis
            config_ips (List[`ApplianceIp`]): List of IP configurations
            controllers (List[`ApplianceController`]): List of controllers expected in Tintri Appliance
            customization_info (`ApplianceCustomizationInfo`): Tintri Appliance customization information
            date_time_config (`ApplianceDateTime`): Tintri Appliance date time configuration on node
            disks (List[`ApplianceDisk`]): List of hard disks or flash drives installed on Tintri Appliance
            disk_encryption_info (`ApplianceDiskEncryptionInfo`): Tintri Appliance disk encryption information
            dns_config (`ApplianceDns`): Tintri Appliance DNS configuration
            email_config (`ApplianceEmail`): Tintri Appliance e-mail configuration for sending alert
            info (`ApplianceInfo`): Tintri Appliance information
            ipmi_config (`ApplianceIpmi`): Tintri Appliance IPMI configuration
            lacp_config (`ApplianceLacp`): Tintri Appliance LACP configuration
            maintenance_mode (`ApplianceMaintenanceMode`): Tintri Appliance maintenance mode information
            operational_info (`ApplianceOperationalInfo`): Tintri Appliance operational information
            rbac_external_config (`RbacExternalConfig`): Tintri Appliance RBAC External Configuration
            snmp_config (`ApplianceSnmp`): Tintri Appliance SNMP configuration
            support_config (`ApplianceSupport`): Tintri Appliance auto-support configuration
            syslog_forwarding (`ApplianceSyslogForwarding`): Tintri Appliance system log forwarding configuration
            temperatures (List[`Temperature`]): List of temperatures detected by sensors of the chassis
            upgrade_info (`ApplianceUpgradeInfo`): Tintri Appliance upgrade information
            request (`Request`<`Appliance`>): Appliance Request Object
        """
        pass

    # Roles
    @api
    def get_roles(self):
        """
        Returns a collection of fixed access control Role instances.

        **Supported on:** VMstore and TGC (all versions)

        Returns:
            `Page`: Paginated fixed access control `Role` instances.
        """
        return self._get_all(resource_url='role', response_class=Page)
    
    @api
    def get_role(self, alert_id):
        """
        Get access control tole by instance Tintri UUID

        **Supported on:** VMstore and TGC (all versions)

        Args:
            alert_id (str): Alert Object Tintri UUID

        Returns:
            `GenericRestApiRole`: an access control Role by instance Tintri UUID
        """
        return self._get_one(path_params=[alert_id], resource_url='role', request_class=GenericRestApiRole)
    
    @api
    def associate_external_groups_with_role(self, role_id, external_groups):
        """
        Associates collection of external groups with an access control role

        **Supported on:** VMstore and TGC (all versions)

        Args:
            role_id (str): access control role id
            external_groups (List[str]): collection of external groups
        """
        return self._update(external_groups, path_params=[role_id], resource_url="role")

    # ServiceGroups
    @api(target="tgc", version="v310.21")
    def update_service_group_protection_policy(self, service_group_id, policy):
        """
        Update the protection policy (both snapshot schedules and replication configuration) for the given service group.

        **Supported on:** TGC (since v310.21)

        Args:
            service_group_id (str): service group id
            policy (`PolicyConfig`): protection policy
        """
        return self._update(policy, path_params=[service_group_id], resource_url="servicegroup/%s/policyConfig")

    @api
    def get_service_group_replication_config(self, service_group_id):
        """
        Get replication configuration associated with the service group.

        **Supported on:** VMstore and TGC (all versions)

        Args:
            service_group_id (str): The service group ID.

        Returns:
            `VirtualMachineReplicationConfig`: The replication configuration associated with the service group.
        """
        return self._get_one(resource_url='servicegroup/%s/replConfig', path_params=[service_group_id], response_class=VirtualMachineReplicationConfig)

    @api
    def get_service_group_snapshot_schedules(self, service_group_id):
        """
        Returns list of snapshot schedules which will be applied to members of this service group.

        **Supported on:** VMstore and TGC (all versions)

        Args:
            service_group_id (str): The service group ID.
        Returns:
            List[`VirtualMachineSnapshotSchedule`]: List of snapshot schedules associated the service group.
        """
        return self._get_all(resource_url='servicegroup/%s/snapshotSchedules', path_params=[service_group_id], response_class=VirtualMachineSnapshotSchedule)

    @api(target="vmstore", version="v310.21")
    def perform_ha_failover(self, appliance_id):
        """
        Performs HA failover, controller pair state should be REDUNDANT at the time of performing failover operation

        **Supported on:** VMstore (since v310.21)

        Args:
            appliance_id (str): The appliance ID.
        """
        return self._create(None, path_params=[appliance_id], resource_url="appliance/%s/hafailover")
    
    @api(target="vmstore", version="v310.11")
    def reboot(self, appliance_id):
        """
        Reboots specified appliance

        **Supported on:** VMstore (since v310.11)

        Args:
            appliance_id (str): The appliance ID.
        """
        return self._create(None, path_params=[appliance_id], resource_url="appliance/%s/reboot")

    @api(target="vmstore", version="v310.11")
    def shutdown(self, appliance_id):
        """
        Shutsdown appliance

        **Supported on:** VMstore (since v310.11)

        Args:
            appliance_id (str): The appliance ID.
        """
        return self._create(None, path_params=[appliance_id], resource_url="appliance/%s/shutdown")

    @api(version="v310.41")
    def restart_webserver(self, appliance_id):
        """
        Restarts the web server

        **Supported on:** VMstore and TGC (since v310.41)

        Args:
            appliance_id (str): The appliance ID.
        """
        return self._create(None, path_params=[appliance_id], resource_url="appliance/%s/restartWebServer")
    
    @api(target="vmstore")
    def rotate_encryption_key(self, appliance_id):
        """
        Rotates the disk encryption key

        **Supported on:** VMstore (all versions)

        Args:
            appliance_id (str): The appliance ID.
        """
        return self._create(None, path_params=[appliance_id], resource_url="appliance/%s/rotateEncryptionKey")
    
    @api(target="tgc", version="v310.51")
    def create_licenses(self, license_str):
        """
        Adds one or more licenses.

        **Supported on:** TGC (since v310.51)

        Args:
            license_str (str): string of one of more license keys separated by comma, space or line break

        Returns:
            List[str]: List of validated or failed licenses
        """
        return self._create(license_str, resource_url="license/bulk", request_class=License)
    
    @api(target="tgc", version="v310.51")
    def create_license_report(self, license_report_filter):
        """
        Get license list report as URL

        **Supported on:** TGC (since v310.51)

        Args:
            license_report_filter (`LicenseDownloadableReportFilter`): License report filter

        Returns:
            str: URL to retrieve license list report
        """
        return self._create(license_report_filter, resource_url="license/licenseListDownloadable", request_class=types.StringType)
    
    @api(target="tgc")
    def get_replication_links(self):
        """
        Gets the replication links

        **Supported on:** TGC (all versions)

        Returns:
            List[`ReplLink`]: List of replication links
        """
        return self._get_all(resource_url="replTopology", request_class=ReplLink)
    
    @api(target="tgc")
    def create_service_group_report(self, report_filter):
        """
        Get a URL for retrieving service group report

        **Supported on:** TGC (all versions)

        Args:
            report_filter (`SvgDownloadableReportFilter`): filter for generating the report

        Returns:
            str: URL to retrieve service group list report
        """
        return self._create(report_filter, resource_url="servicegroup/svgListDownloadable", request_class=types.StringType)
    
    @api(target="tgc")
    def update_high_priority_service_group(self, service_group_id, request):
        """
        Update the service groups that have higher priority than the given service group

        **Supported on:** TGC (all versions)

        Args:
            service_group_id (int): service group id
            request (`CollectionChangeRequest`): CollectionChangeRequest object
        """
        return self._update(request, path_params=[service_group_id], resource_url="servicegroup/%s/groupsPrioritiesHigher")
    
    @api(target="tgc", version="v310.21")
    def update_service_group_static_members(self, service_group_id, request):
        """
        Update statically assigned members for the given service group. Deleted or non-existent members will be ignored.

        **Supported on:** TGC (since v310.21)

        Args:
            service_group_id (str): service group id
            request (`CollectionChangeRequest`): CollectionChangeRequest object
        """
        return self._update(request, path_params=[service_group_id], resource_url="servicegroup/%s/members/static")
    
    @api(target="tgc")
    def get_service_group_qos_operation_status(self, service_group_id):
        """
        Get QOS operation status of service group

        **Supported on:** TGC (all versions)

        Args:
            service_group_id (str): service group id

        Returns:
            `ServiceGroupOperationStatus`: QoS operation status
        """
        return self._get_one(path_params=[service_group_id], resource_url="servicegroup/%s/qos/operationStatus", request_class=ServiceGroupOperationStatus)

    @api(target="tgc", version="v310.31")
    def update_service_group_qos_config(self, qos_config, service_group_id):
        """
        Updates the QOS policy of service group with given config

        **Supported on:** TGC (since v310.31)

        Args:
            qos_config (`VirtualMachineQoSConfig`): VirtualMachineQoSConfig object
            service_group_id (str): service group id
        """
        return self._update(qos_config, path_params=[service_group_id], resource_url="servicegroup/%s/qosConfig")
    
    @api(target="tgc")
    def apply_service_group_qos_config(self, service_group_id):
        """
        Apply QOS config on service group.
        
        **Supported on:** TGC (all versions)
        
        Args:
            service_group_id (str): service group id
        """
        return self._create(None, path_params=[service_group_id], resource_url="servicegroup/%s/qos")
    
    @api(target="tgc", version="v310.21")
    def update_service_group_rules(self, rules, service_group_id):
        """
        Updates rules of given service group

        **Supported on:** TGC (since v310.21)

        Args:
            rules (`ServiceGroupRules`): ServiceGroupRules object
            service_group_id (str): service group id
        """
        return self._update(rules, path_params=[service_group_id], resource_url="servicegroup/%s/rules")

    @api(target="tgc", version="v310.31")
    def get_service_group_qos_config(self, service_group_id):
        """
        Gets the QOS policy of given service group

        **Supported on:** TGC (since v310.31)

        Args:
            service_group_id (str): service group id

        Returns:
            `VirtualMachineQosConfig`: QoS config associated with service group
        """
        return self._get_one(path_params=[service_group_id], resource_url="servicegroup/%s/qosConfig", response_class=VirtualMachineQoSConfig)

    @api(target="vmstore", version="v310.51")
    def get_user_sessions(self):
        """
        Gets a list of user sessions information that are currently logged in

        **Supported on:** VMstore (since v310.51)

        Returns:
            List[`UserSession`]: list of UserSession objects
        """
        return self._get_all(resource_url="session/active", request_class=UserSession)
    
    @api(target="vmstore", version="v310.51")
    def get_current_session(self):
        """
        Gets the current user sessions information

        **Supported on:** VMstore (since v310.51)

        Returns:
            `UserSession`: Current User session
        """
        return self._get_all(resource_url="session/current", request_class=UserSession)
    
    @api(target="vmstore")
    def sso_authorize(self):
        """
        Creates a valid session after successful authentication with Kerberos tickets and successful authorization on Tintri API server.

        **Supported on:** VMstore (all versions)

        Returns:
            str: Tintri Role name associated with the credentials
        """
        return self._get_one(resource_url="session/ssoauth")
    
    @api
    def reset_user_password(self, cred):
        """
        Resets the password of a local user.

        **Supported on:** VMstore and TGC (all versions)

        Args:
            cred (`RestApiCredentials`): RestApiCredentials object
        """
        return self._create(cred, resource_url="userAccount/resetPassword")

    @api(target="tgc")
    def create_vm_list_report(self, report_filter):
        """
        Creates a URL for retrieving specified VM list report.

        **Supported on:** TGC (all versions)

        Args:
            report_filter (`VirtualMachineDownloadableReportFilter`): Filter to use for generating report
        Returns:
            str: URL to the report
        """
        return self._create(report_filter, resource_url="vm/vmListDownloadable", request_class=types.StringType)
    
    @api(target="tgc", version="v310.51")
    def update_vm_affinity(self, affinity, vm_id):
        """
        Updates VM affinity rule

        **Supported on:** TGC (since v310.51)

        Args:
            affinity (`VirtualMachineAffinityRule`): VirtualMachineAffinityRule to set
            vm_id (str): VM Object's UUID
        """
        return self._update(affinity, path_params=[vm_id], resource_url="vm/%s/affinity")
    
    @api(target="tgc")
    def create_vm_historical_stats_report(self, vm_id, report_filter):
        """
        Creates a URL for retrieving specified VM historical statistics report.

        **Supported on:** TGC (all versions)

        Args:
            vm_id (str): VM Object's UUID
            report_filter (`VirtualMachineStatDownloadableReportFilter`): Filter to use for generating report

        Returns:
            str: URL to the report
        """
        return self._create(report_filter, path_params=[vm_id], resource_url="vm/%s/statsDownloadable", request_class=types.StringType)
    
    @api(target="tgc")
    def add_vmstore(self, vmstore):
        """
        Add a VMstore to Tintri Global Center

        **Supported on:** TGC (all versions)

        Args:
            vmstore (`Vmstore`): VMStore and its properties

        Returns:
            `Vmstore`: VMStore with the new Tintri UUID assigned by the system
        """
        return self._create(vmstore, resource_url=Vmstore._url, request_class=Vmstore)

    @api(target="tgc")
    def create_vmstore_list_report(self, report_filter):
        """
        Creates a URL for retrieving specified VM historical statistics report.

        **Supported on:** TGC (all versions)

        Args:
            report_filter (`VMstoreDownloadableReportFilter`): Filter to use for generating report

        Returns:
            str: URL to the report
        """
        return self._create(report_filter, resource_url="vmstore/vmstoreListDownloadable", request_class=types.StringType)
    
    @api(target="tgc", version="v310.51")
    def create_vmpool_list_report(self, report_filter):
        """
        Creates a URL for retrieving specified VM pool report.

        **Supported on:** TGC (since v310.51)

        Args:
            report_filter (`VmstorePoolDownloadableReportFilter`): Filter to use for generating report

        Returns:
            str: URL to the report
        """
        return self._create(report_filter, resource_url="vmstorePool/vmPoolListDownloadable", request_class=types.StringType)

    @api(target="tgc", version="v310.51")
    def update_vmstore_pool_members(self, vmstore_pool_id, request):
        """
        Add or delete members of the given VMstore pool.

        **Supported on:** TGC (since v310.51)

        Args:
            vmstore_pool_id (str): Vmstore pool ID
            request (`CollectionChangeRequest`): CollectionChangeRequest object which specifies new and deleted members to be updated
        """
        return self._update(request, path_params=[vmstore_pool_id], resource_url="vmstorePool/%s/members")

    @api(target="tgc", version="v310.51")
    def get_current_recommendation(self, vmstore_pool_id):
        """
        Gets the current recommendation for specified VMstore pool ID

        **Supported on:** TGC (since v310.51)

        Args:
            vmstore_pool_id (str): Vmstore pool ID
        """
        return self._get_one(path_params=[vmstore_pool_id], resource_url="vmstorePool/%s/recommendation/current", response_class=Recommendation)

    @api(target="tgc", version="v310.51")
    def accept_recommendation(self, vmstore_pool_id, recommendation_id):
        """
        Accept a Recommendation. A Recommendation can only be accepted when Recommendation is in Available and Available_Acked state. All other
        states, an error will be returned.

        **Supported on:** TGC (since v310.51)

        Args:
            vmstore_pool_id (str): Vmstore pool ID
            recommendation_id (str): Recommendation ID
        """
        return self._create(None, path_params=[vmstore_pool_id, recommendation_id], resource_url='vmstorePool/%s/recommendation/%s/accept')

    @api(target="tgc", version="v310.51")
    def acknowledge_recommendation(self, vmstore_pool_id, recommendation_id):
        """
        Acknowledge a Recommendation. If Recommendation is not in Available state, an error will be returned.

        **Supported on:** TGC (since v310.51)

        Args:
            vmstore_pool_id (str): Vmstore pool ID
            recommendation_id (str): Recommendation ID
        """
        return self._create(None, path_params=[vmstore_pool_id, recommendation_id], resource_url='vmstorePool/%s/recommendation/%s/acknowledge')

    @api(target="tgc", version="v310.51")
    def cancel_recommendation(self, vmstore_pool_id, recommendation_id):
        """
        Cancel a Recommendation. If Recommendation is not in accepted state, an error will be returned.

        **Supported on:** TGC (since v310.51)

        Args:
            vmstore_pool_id (str): Vmstore pool ID
            recommendation_id (str): Recommendation ID
        """
        return self._create(None, path_params=[vmstore_pool_id, recommendation_id], resource_url='vmstorePool/%s/recommendation/%s/cancel')

    @api(target="tgc", version="v310.51")
    def update_vmstore_issues(self, recommendation_issues, vmstore_pool_id, recommendation_id):
        """
        Updates Recommendation specified with RecommendationIssueSelection

        **Supported on:** TGC (since v310.51)

        Args:
            recommendation_issues (List[`RecommendationIssueSelection`]): List of RecommendationIssueSelection
            vmstore_pool_id (str): Vmstore pool ID
            recommendation_id (str): Recommendation ID
        """
        return self._update(recommendation_issues, path_params=[vmstore_pool_id, recommendation_id], resource_url='vmstorePool/%s/recommendation/%s/issues')

    @api(target="tgc", version="v310.51")
    def reset_recommendation(self, vmstore_pool_id, recommendation_id):
        """
        Reset a Recommendation. If Recommendation is not in Available or Available_Ack state, an error will be returned.

        **Supported on:** TGC (since v310.51)

        Args:
            vmstore_pool_id (str): Vmstore pool ID
            recommendation_id (str): Recommendation ID
        """
        return self._create(None, path_params=[vmstore_pool_id, recommendation_id], resource_url='vmstorePool/%s/recommendation/%s/reset')

    @api(filter_class=PageFilterSpec, target="tgc", version="v310.51")
    def get_recommendations(self, vmstore_pool_id, filters=None):
        """
        Gets a list of Recommendation based on query parameters

        **Supported on:** TGC (since v310.51)

        Args:
            vmstore_pool_id (str): Vmstore pool ID
        """
        return self._get_all(path_params=[vmstore_pool_id], filters=filters, resource_url="vmstorePool/%s/recommendationHistory", response_class=Recommendation)

    @api
    def update_certificate(self, obj, appliance_id):
        """
        Upload a certificate to VMstore
        
        **Supported on:** VMstore and TGC (all versions)
        
        Args:
            obj (Certificate): Updated Certificate object
            appliance_id (str): Appliance object's UUID
        """
        return self._update(obj, path_params=[appliance_id], resource_url=Certificate._url)
    
    @api(target="vmstore")
    def delete_datastore_replication_path(self, datastore_id, repl_id):
        """
        Deletes the DatastoreReplicationPath object specified by its ID.

        **Supported on:** VMstore (all versions)
        
        Args:
            datastore_id (str): Datastore Object's UUID
            repl_id (str): DatastoreReplicationPath Object's UUID
        """
        return self._delete(path_params=[datastore_id, repl_id], resource_url=DatastoreReplicationPath._url + "/%s")

# These apis depict operations supported by resource and are decorated with 'api'.
# If api takes filter spec, add the filter_class.
# If api is applicable only to vmstore/tgc, add target.
# If api is applicable to certain version, add version.
# Anytime resource is added/updated, keep apis consistent.
# create/update apis use obj to be created/updated followed by any arguments.
    @api(target="vmstore", version="v310.11")
    def create_acl(self, obj, datastore_id, fileshare_name): pass

    @api(target="vmstore")
    def create_appliance_snmp_target(self, obj, appliance_id):
        """
        Creates an ApplianceSnmpTarget object

        **Supported on:** VMstore (all versions)
        
        Args:
            obj (`ApplianceSnmpTarget`): An instance of ApplianceSnmpTarget.
            appliance_id (str): Appliance object's UUID.
        """
        pass

    @api(target="vmstore")
    def create_appliance_snmp_user(self, obj, appliance_id):
        """
        Creates an ApplianceSnmpUser object

        **Supported on:** VMstore (all versions)
        
        Args:
            obj (`ApplianceSnmpUser`): An instance of ApplianceSnmpUser.
            appliance_id (str): Appliance object's UUID.
        """
        pass
    
    @api(target="vmstore")
    def create_datastore_replication_path(self, obj, datastore_id): pass

    @api(target="vmstore", version="v310.11")
    def create_file_share(self, obj, datastore_id): pass

    @api(target="vmstore", version="v310.21")
    def create_hypervisor_manager_config(self, obj, datastore_id): pass

    @api
    def create_license(self, obj): pass

    @api
    def create_service_group(self, obj):
        """
        Creates a Service Group on the server.

        **Supported on:** VMstore and TGC (all versions)
        
        Args:
            obj (`ServiceGroup`): An instance of ServiceGroup.

        Returns:
            (str): The created ServiceGroup UUID.
        """
        pass

    @api(target="vmstore")
    def create_snapshot(self, obj):
        """
        Creates a snapshots from a list of snapshot specification.

        **Supported on:** VMstore (all versions)
        
        Args:
            SnapshotSpes (List[`SnapshotSpec`]): List of SnapshotSpecs.

        Returns:
            (List[str]): A list of created snapshot UUIDs.
        """
        pass

    @api
    def create_user_account(self, obj): pass

    @api
    def create_vmstore(self, obj): pass

    @api(target="tgc", version="v310.51")
    def create_vmstore_pool(self, obj): pass

    @api(target="vmstore", version="v310.11")
    def delete_ace(self, datastore_id, fileshare_id, ace_id): pass
    
    @api
    def delete_appliance(self, appliance_id): pass
    
    @api(target="vmstore")
    def delete_appliance_snmp_target(self, appliance_id, target_id): pass

    @api(target="vmstore")
    def delete_appliance_snmp_user(self, appliance_id, snmp_username): pass
    
    @api
    def delete_certificate(self, appliance_id, certificate_id): pass
    
    @api(target="vmstore", version="v310.11")
    def delete_file_share(self, datastore_id, fileshare_name): pass
    
    @api(target="vmstore", version="v310.21")
    def delete_hypervisor_manager_config(self, datastore_id, config_id): pass
    
    @api
    def delete_license(self, license_key): pass
    
    @api
    def delete_service_group(self, service_group_id): pass
    
    @api(target="vmstore")
    def delete_snapshot(self, snapshot_id): pass
    
    @api(target="vmstore")
    def delete_task(self, task_id): pass
    
    @api
    def delete_user_account(self, user_account_id): pass
    
    @api
    def delete_vmstore(self, vmstore_id): pass
    
    @api(target="tgc", version="v310.51")
    def delete_vmstore_pool(self, vmstore_pool_id): pass

    @api(target="vmstore", version="v310.11")
    def get_ace(self, datastore_id, fileshare_name, ace_id): pass
    
    @api(target="vmstore", version="v310.11")
    def get_acl(self, datastore_id, fileshare_name): pass

    @api(filter_class=AlertFilterSpec)
    def get_alerts(self, filters=None): pass

    @api(target="vmstore")
    def get_appliance_alert_counts(self, appliance_id): pass

    @api(target="vmstore", version="v310.31")
    def get_appliance_components(self, appliance_id): pass

    @api(target="vmstore", version="v310.31")
    def get_appliance_controllers(self, appliance_id): pass

    @api(target="vmstore")
    def get_appliance_customization_info(self, appliance_id): pass

    @api
    def get_appliance_date_time(self, appliance_id): pass

    @api(target="vmstore")
    def get_appliance_disk_encryption_info(self, appliance_id): pass

    @api(target="vmstore", version="v310.31")
    def get_appliance_disks(self, appliance_id): pass 

    @api
    def get_appliance_dns(self, appliance_id): pass

    @api
    def get_appliance_email(self, appliance_id): pass

    @api
    def get_appliance_email_alerts(self, appliance_id): pass

    @api(target="vmstore")
    def get_appliance_failed_components(self, appliance_id): pass

    @api
    def get_appliance_info(self, appliance_id): pass

    @api(target="vmstore")
    def get_appliance_ipmi(self, appliance_id): pass

    @api
    def get_appliance_ips(self, appliance_id): pass

    @api(target="vmstore")
    def get_appliance_lacp(self, appliance_id): pass

    @api(target="vmstore")
    def get_appliance_maintenance_mode(self, appliance_id): pass

    @api
    def get_appliance_operational_info(self, appliance_id): pass

    @api(target="vmstore")
    def get_appliance_snmp(self, appliance_id): pass

    @api(target="vmstore")
    def get_appliance_snmp_target(self, appliance_id, target_id): pass

    @api(target="vmstore")
    def get_appliance_snmp_user(self, appliance_id, snmp_username): pass

    @api
    def get_appliance_support(self, appliance_id): pass

    @api(target="vmstore")
    def get_appliance_syslog_forwarding(self, appliance_id): pass

    @api(filter_class=PageFilterSpec)
    def get_appliances(self, filters=None): pass

    @api
    def get_certificates(self, appliance_id): pass

    @api(target="tgc")
    def get_cluster_configuration(self): pass

    @api
    def get_datastore(self, datastore_id): pass
    
    @api(target="vmstore")
    def get_datastore_nfs_accesses(self, datastore_id): pass

    @api(target="vmstore", version="v310.21")
    def get_datastore_qos_info(self, datastore_id): pass
    
    @api
    def get_datastore_replication_info(self, datastore_id): pass
    
    @api
    def get_datastore_replication_paths(self, datastore_id): pass
    
    @api(target="vmstore", version="v310.11")
    def get_datastore_smb_setting(self, datastore_id): pass
    
    @api
    def get_datastores(self): pass
    
    @api(target="vmstore", version="v310.11")
    def get_file_share(self, datastore_id, fileshare_name): pass
    
    @api(target="vmstore", version="v310.11")
    def get_file_shares(self, datastore_id): pass
    
    @api(target="tgc")
    def get_filter_scopes(self): pass
    
    @api(target="vmstore")
    def get_hypervisor_datastores(self, datastore_id, query_params={}): pass
    
    @api(target="vmstore", version="v310.21")
    def get_hypervisor_manager_configs(self, datastore_id): pass
    
    @api
    def get_licenses(self): pass

    @api(target="tgc", version="v310.51")
    def get_license_summary(self): pass

    @api(target="tgc", version="v310.21")
    def get_policy_config(self, service_group_id): pass

    @api
    def get_rbac_external_config(self, appliance_id): pass

    @api(target="tgc", version="v310.51")
    def get_recommendation(self, vmstore_pool_id, recommendation_id): pass
    
    @api
    def get_role_external(self, group_id): pass
    
    @api
    def get_role_externals(self): pass
    
    @api(filter_class=PageFilterSpec)
    def get_service_group_members(self, service_group_id, filters=None): pass
    
    @api(target="tgc")
    def get_service_group_operation_status(self, service_group_id): pass
    
    @api
    def get_service_group(self, service_group_id): pass
    
    @api(filter_class=PageFilterSpec)
    def get_service_groups(self, filters=None): pass
    
    @api
    def get_srm_config(self, service_group_id): pass
    
    @api(target="vmstore")
    def get_snapshot(self, tid): pass
    
    @api(filter_class=SnapshotFilterSpec, target="vmstore")
    def get_snapshots(self, filters=None): pass
    
    @api(filter_class=TaskFilterSpec, target="vmstore")
    def get_task(self, task_id, filters=None): pass
    
    @api(filter_class=TaskFilterSpec, target="vmstore")
    def get_tasks(self, filters=None): pass
    
    @api(target="vmstore", version="v310.31")
    def get_temperatures(self, appliance_id): pass
    
    @api
    def get_user_account(self, tid): pass
    
    @api
    def get_user_accounts(self): pass
    
    @api
    def get_user_agreement(self): pass
    
    @api(filter_class=VirtualDiskFilterSpec, target="vmstore")
    def get_virtual_disks(self, filters=None): pass
    
    @api(target="vmstore", version="v310.21")
    def get_virtual_machine_customization_scripts(self, vm_id):
        """
        Gets customization scripts for VM specified.

        **Supported on:** VMstore (since v310.21)

        Args:
            vm_id (str): VM Object's UUID
        Returns:
            List[str] - A list of strings
        """
        pass
    
    @api(target="vmstore")
    def get_virtual_machine_customization_spec(self, datatore_id, vcenter_name): pass
    
    @api(target="vmstore")
    def get_virtual_machine_host_resources(self, datatore_id, query_params={}): pass
    
    @api
    def get_vm(self, vm_id): pass

    @api(filter_class=VirtualMachineFilterSpec, target="vmstore")
    def get_vm_filter_scopes(self, filters=None): pass
    
    @api(filter_class=PolicyErrorStatFilterSpec, target="tgc")
    def get_vm_policy_error_stats(self, filters=None): pass
    
    @api(filter_class=VirtualMachineFilterSpec)
    def get_vms(self, filters=None): pass
    
    @api(target="tgc")
    def get_vmstores(self): pass

    @api(target="tgc", version="v310.51")
    def get_vmstore_pool(self, vmstore_pool_id): pass
    
    @api(filter_class=PageFilterSpec, target="tgc", version="v310.51")
    def get_vmstore_pools(self, filters=None): pass

    @api(target="vmstore")
    def update_appliance_snmp(self, obj, appliance_id): pass

    @api(target="vmstore")
    def update_appliance_snmp_target(self, obj, appliance_id, target_id): pass

    @api(target="vmstore")
    def update_appliance_snmp_user(self, obj, appliance_id, snmp_username): pass

    @api(target="tgc")
    def update_cluster_configuration(self, obj): pass
    
    @api(target="vmstore")
    def update_datastore(self, obj, datastore_id, display_name=None, is_data_from_appliance=None, last_updated_time=None, local_alias=None, snapshot_high_frequency_vms_count=None, snapshot_high_frequency_vms_max=None, vaai_thick_support_disabled=None, appliance_uuid=None, nfs_accesses=None, qos_info=None, replication=None, snapshot_schedules=None, stat=None, storage_containers=None, request=None):
        """
        Updates the specified properties of the specified datastore, either specify properties in a Request Datastore object or set the properties to be updated.

        **Supported on:** VMstore (all versions)
        
        Args:
            obj (`Datastore`): Updated Datastore object
            datastore_id (str): Datastore object's UUID
            display_name (str): This name to be used to display in a UI.
            is_data_from_appliance (bool): Set to true if the current data in the datastore was fetched from the appliance. If the appliance is not accessible set it to false to indicate that the data contained in the datastore is from local system management databases.
            last_updated_time (`DateTime`): Last time the entity is updated in the format YYYY-MM-DDThh:mm:ss.ms-/+zz:zz
            local_alias (str): Alias used for the entity instance in this Tintri API server. If an alias is not set, then localAlias is not returned.
            snapshot_high_frequency_vms_count (int): Returns the current number of VMs using RPO (high frequency) snapshots
            snapshot_high_frequency_vms_max (int): Returns the maximum number of VMs permitted to take high frequency snapshots.
            vaai_thick_support_disabled (str): Option to ensure the VMStore treats all new VMWare VAAI provisioned VMs as Thin-provisioned. A "true" value indicates that VMStore file system will always use thin provisioning to get maximum space savings. But a "false" value indicates that the VMStore file system will use the VAAI setting provided by the user during provisioning. 
            appliance_uuid (`Uuid`): The Tintri appliance UUID.
            nfs_accesses (`DatastoreNfsAccesses`): NFS control access.
            qos_info (`DatastoreQoSInfo`): Datastore QOS Info object
            replication (`DatastoreReplicationInfo`): The replication links from and to this datastore and other replication related properties at datastore level.
            snapshot_schedules (List[`VirtualMachineSnapshotSchedule`]): A list of of default Snapshot schedules.
            stat (`DatastoreStat`): Latest performance data at datastore level. It is aggregated for all VMs and artifacts on the datastore.
            storage_containers list (`HypervisorDatastore`): A list of storage container information contined within the datastore.
            request (`Request`<`Datastore`>): Datastore request object
        """
        pass
    
    @api(target="vmstore")
    def update_datastore_nfs_accesses(self, obj, datastore_id): pass

    @api(target="vmstore")
    def update_datastore_replication_path(self, obj, datastore_id, request=None):
        """
        Updates the specified replication link on the specified datastore instance by the incoming replication instance, either specify properties in a Request DatastoreReplicationPath object or use the updated object.
        In both cases, make sure that 'id' attribute is present.

        **Supported on:** VMstore (all versions)

        Args:
            obj (`DatastoreReplicationPath`): Updated DatastoreReplicationPath object
            datastore_id (str): Datastore object's UUID
            request (`Request`<`DatastoreReplicationPath`>): DatastoreReplicationPath request
        """
        pass

    @api(target="vmstore", version="v310.11")
    def update_datastore_smb_setting(self, obj, datastore_id): pass

    @api(target="vmstore", version="v310.31")
    def update_file_share(self, obj, datastore_id, fileshare_name, comment=None, encrypt_data=None, file_share_type=None, file_system_name=None, name=None, nominal_consumed_bytes=None, quota_bytes=None, request=None):
        """
        Updates a file share, either specify properties in a Request FileShare object or set the properties to be updated.

        **Supported on:** VMstore (since v310.31)

        Args:
            obj (`FileShare`): Updated FileShare object
            datastore_id (str): Datastore object's UUID
            fileshare_name (str): File share to update
            comment (str): Comments regarding the file share
            encrypt_data (bool): 'True' indicates SMB communication with this FileShare shall be encrypted. 'False' indicates SMB communication with this FileShare shall not be encrypted.
            file_share_type (str): FileShare type REALSTORE|SNAPSHOT
            file_system_name (str): The file system name underlying the FileShare, used by System Center Virtual Machine Manager
            name (str): FileShare name
            nominal_consumed_bytes (int): The bytes nominally consumed by the FileShare. Does not include deduplication, compression, cloning, or thin-provisioning space savings
            quota_bytes (int): The quota in bytes allocated to the FileShare, used by System Center Virtual Machine Manager
            request (`Request`<`FileShare`>): FileShare request
        """
        pass

    @api(target="vmstore", version="v310.21")
    def update_hypervisor_manager_config(self, obj, datastore_id, manager_config_id, username=None, password=None, request=None):
        """
        Updates username or password of already configured hypervisor manager, either specify properties in a Request HypervisorManagerConfig object or set the properties to be updated.

        **Supported on:** VMstore (since v310.21)

        Args:
            obj (`HypervisorManagerConfig`): Updated HypervisorManagerConfig object
            datastore_id (str): Datastore object's UUID
            manager_config_id (str): Hypervisor Manager config UUID
            username (str): Username for the hypervisor manager
            password (str): Password for the hypervisor manager
            request (`Request`<`HypervisorManagerConfig`>): HypervisorManagerConfig request
        """
        pass

    @api(target="tgc", version="v310.21")
    def update_policy_config(self, obj, service_group_id): pass
    
    @api
    def update_rbac_external_config(self, obj, appliance_id): pass

    @api(target="tgc", version="v310.51")
    def update_recommendation(self, obj, vmstore_pool_id, recommendation_id, accepted_time=None, acknowledged_time=None, completion_time=None, creation_time=None, execution_state=None,
                              expiration_time=None, group_id=None, last_updated_time=None, state=None, state_reason=None, vm_affinity_not_now_tintri_uuids=None,
                              action_groups=None, expected_outcomes=None, feedback=None, issues=None, request=None):
        """
        Update attribute of a Recommendation for supported attribute, either specify properties in a Request Recommendation object or set the properties to be updated.

        **Supported on:** TGC (since v310.51)

        Args:
            obj (`Recommendation`): Updated Recommendation object
            vmstore_pool_id (str): VMstorePool Object's UUID
            recommendation_id (str): Recommendation Object's UUID
            accepted_time (`DateTime`): Time when recommendation is accepted by user
            acknowledged_time (`DateTime`): The acknowledged time by user
            completion_time (`DateTime`): Recommendation completion time
            creation_time (`DateTime`): Recommendation creation time
            execution_state (str): Execution state of the Recommendation
            expiration_time (`DateTime`): The expiration time
            group_id (str): Returns the groupId. The attribute is undocumented by default and used only for testing
            last_updated_time (`DateTime`): Last time the recommendation was updated
            state (str): Recommendation state
            state_reason (str): Reason that the recommendation is unavailable or invalidated
            vm_affinity_not_now_tintri_uuids (str): The VM affinity "NOT NOW" for this Recommendation. Only applied when Recommendation state is AVAILABLE or AVAILABLE_ACKED
            action_groups (List[`RecommendationActionGroup`]): A list of action groups. The group must be executed in the order it is returned. The action inside a group can be safely executed in parallel
            expected_outcomes (List[`RecommendationOutcome`]): The expected condition of one or more VMstore if the recommendation is applied
            feedback (`RecommendationFeedback`): The user feedback on the recommendation. Only applied when Recommendation state is AVAILABLE or AVAILABLE_ACKED
            issues (List[`RecommendationAnalysis`]): The predicted issues of one or more VMstore in the next 7 days
            request (`Request`<`Recommendation`>): Recommendation request
        """
        pass

    @api
    def update_role(self, obj, role_id): pass

    @api
    def update_service_group(self, obj):
        """
        Update an existing service group.
        
        **Supported on:** VMstore and TGC (all versions)
        
        Args:
            obj (`ServiceGroup`): Updated Servicegroup object
        """
        return self._update(obj, resource_url=ServiceGroup._url)

    @api
    def update_user_account(self, obj, user_account_id, is_deletable=None, is_disabled=None, last_updated_time=None, local_alias=None, role=None, role_names=None, request=None):
        """
        Updates the specified properties by values of passed UserAccount instance, either specify updated object or properties in a Request VMstore object or set the properties to be updated.

        **Supported on:** VMstore and TGC (all versions)
        
        Args:
            obj (`UserAccount`): Updated UserAccount object
            user_account_id (str): UserAccount object's UUID
            is_deletable (bool): 'True' indicates account can be deleted, 'False' otherwise
            is_disabled (bool): 'True' indicates account is disabled, 'False' otherwise
            last_updated_time (`DateTime`): Last time the entity is updated in YYYY-MM-DDThh:mm:ss:ms-/+zz:zz format
            local_alias (str): Alias used for entity instance
            name (str): Role name
            password (str): Password for this user account, its only used when adding or updating user accounts
            role (`Role`): Return the access control role assigned for the user account
            role_names (List[str]): List of role names assigned to this user account
            request (`Request`<`UserAccount`>): Request UserAccount object
        """
        pass

    @api
    def update_user_agreement(self, obj): pass
    
    @api
    def update_vm(self, obj, vm_id, request=None): pass

    @api(target="tgc", version="v310.51")
    def update_vmstore_pool(self, obj, vmstore_pool_id): pass

_populate_methods = Tintri('','','')
del _populate_methods
