## Messages 201002 to 210022

This chapter includes messages from 201002 to 210022.

### 201002

**Error Message** `%ASA-3-201002: Too many TCP connections on {static|xlate} _global_address_ ! _econns_nconns_`

**Explanation** The maximum number of TCP connections to the specified global address was exceeded.

-   econns—The maximum number of embryonic connections
-   nconns—The maximum number of connections permitted for the static or xlate global address

**Recommended Action** Use the show static or show nat command to check the limit imposed on connections to a static address. The limit is configurable.

### 201003

**Error Message** `%ASA-2-201003: Embryonic limit exceeded _nconns_/_elimit_ for _outside_address_/_outside_port_ to _inside_address_(_global_address_)/_inside_port_ on interface _interface_name_`

**Explanation** The number of embryonic connections from the specified foreign address with the specified static global address to the specified local address exceeds the embryonic limit. When the limit on embryonic connections to the Secure Firewall ASA is reached, the Secure Firewall ASA attempts to accept them anyway, but puts a time limit on the connections. This situation allows some connections to succeed even if the Secure Firewall ASA is very busy. This message indicates a more serious overload than message 201002, which can be caused by a SYN attack, or by a very heavy load of legitimate traffic.

-   nconns—The maximum number of embryonic connections received
-   _elimit_ —The maximum number of embryonic connections specified in the static or nat command

**Recommended Action** Use the show static command to check the limit imposed on embryonic connections to a static address.

### 201004

**Error Message** `%ASA-3-201004: Too many udp connections on _{static|xlate}_ _global_address_! _udp_connections_limit_`

**Explanation** The maximum number of UDP connections to the specified global address was exceeded.

-   udp conn limit—The maximum number of UDP connections permitted for the static address or translation
    

**Recommended Action** Use the show static or show nat command to check the limit imposed on connections to a static address. You can configure the limit.

### 201005

**Error Message** `%ASA-3-201005: FTP data connection failed for _IP_address_`

**Explanation** The Secure Firewall ASA cannot allocate a structure to track the data connection for FTP because of insufficient memory.

**Recommended Action** Reduce the amount of memory usage or purchase additional memory.

### 201006

**Error Message** `%ASA-3-201006: RCMD backconnection failed for _IP_address_/_port_`

**Explanation** The Secure Firewall ASA cannot preallocate connections for inbound standard output for rsh commands because of insufficient memory.

**Recommended Action** Check the rsh client version; the Secure Firewall ASA only supports the Berkeley rsh client version. You can also reduce the amount of memory usage, or purchase additional memory.

### 201008

**Error Message** `%ASA-3-201008: Disallowing new connections.`

**Explanation** You have enabled TCP system log messaging and the syslog server cannot be reached, or when using the ASA syslog server (PFSS) and the disk on the Windows NT system is full, or when the auto-update timeout is configured and the auto-update server is not reachable.

**Recommended Action** Disable TCP syslog messaging. If using PFSS, free up space on the Windows NT system where PFSS resides. Also, make sure that the syslog server is up and you can ping the host from the ASA console. Then restart TCP system message logging to allow traffic. If the Auto Update Server has not been contacted for a certain period of time, enter the \[no\] auto-update timeout period command to have it stop sending packets.

### 201009

**Error Message** `%ASA-3-201009: _TCP_ connection limit of _number_ for host _IP_address_ on _interface_name_ exceeded`

**Explanation** The maximum number of connections to the specified static address was exceeded.

-   number—The maximum of connections permitted for the host
-   IP\_address—The host IP address
-   _interface\_name—_ The name of the interface to which the host is connected

**Recommended Action** Use the show static and show nat commands to check the limit imposed on connections to an address. The limit is configurable.

### 201010

**Error Message** `%ASA-6-201010: Embryonic connection limit exceeded _econns_/_limit_ for _dir_ packet from _source_address_/_source_port_ to _dest_address_/_dest_port_ on interface _interface_name_`

**Explanation** An attempt to establish a TCP connection failed because of an exceeded embryonic connection limit, which was configured with the set connection embryonic-conn-max MPC command for a traffic class.

To reduce the impact of anomalous incoming traffic on ASA's different management or data interfaces and protocols, the interfaces are configured with a default embryonic limit of 100. This syslog message appears when the embryonic connections to ASA interface exceeds 100. This default value cannot be modified or disabled.

-   econns—The current count of embryonic connections associated to the configured traffic class
-   limit—The configured embryonic connection limit for the traffic class
-   dir—input: The first packet that initiates the connection is an input packet on the interface interface\_name output: The first packet that initiates the connection is an output packet on the interface interface\_name
-   _source\_address/source\_port_ —The source real IP address and the source port of the packet initiating the connection
-   _dest\_address/dest\_port_ —The destination real IP address and the destination port of the packet initiating the connection
-   interface\_name—The name of the interface on which the policy limit is enforced

**Recommended Action** None required.

### 201011

**Error Message** `%ASA-3-201011: Connection limit exceeded _cnt_/_limit_ for _dir_ packet from _sip_/_sport_ to _dip_/_dport_ on interface _if_name_`

**Explanation** A new connection through the Secure Firewall ASA resulted in exceeding at least one of the configured maximum connection limits. This message applies both to connection limits configured using a static command, or to those configured using Cisco Modular Policy Framework. The new connection will not be allowed through the Secure Firewall ASA until one of the existing connections is torn down, which brings the current connection count below the configured maximum.

-   _cnt_ —Current connection count
-   _limit_ —Configured connection limit
-   _dir_ —Direction of traffic, inbound or outbound
-   _sip_ —Source real IP address
-   _sport_ —Source port
-   _dip_ —Destination real IP address
-   _dpor_ t—Destination port
-   _if\_name_ —Name of the interface on which the traffic was received

**Recommended Action** None required.

### 201012

**Error Message** `%ASA-6-201012: Per-client embryonic connection limit exceeded _curr_num_/_limit_ for _[input|output]_ packet from _ip_address_/_port_ to _ip_address_/_port_ on interface _interface_name_`

**Explanation** An attempt to establish a TCP connection failed because the per-client embryonic connection limit was exceeded. By default, this message is rate limited to 1 message every 10 seconds.

-   _curr\_num_—The current number
-   _limit_—The configured limit
-   _\[input|output\]_—Input or output packet on interface interface\_name
-   _ip\_address_—Real IP address
-   _port_—TCP or UDP port
-   _interface\_name_—The name of the interface on which the policy is applied

**Recommended Action** When the limit is reached, any new connection request will be proxied by the Secure Firewall ASA to prevent a SYN flood attack. The Secure Firewall ASA will only connect to the server if the client is able to finish the three-way handshake. This usually does not affect the end user or the application. However, if this creates a problem for any application that has a legitimate need for a higher number of embryonic connections, you can adjust the setting by entering the set connection per-client-embryonic-max command.

### 201013

**Error Message** `%ASA-3-201013: Per-client connection limit exceeded _curr_num_/_limit_ for _[input|output]_ packet from _ip_address_/_port_ to _ip_address_/_port_ on interface _interface_name_`

**Explanation** A connection was rejected because the per-client connection limit was exceeded.

-   _curr num_—The current number
-   _limit_—The configured limit
-   _\[input|output\]_—The input or output packet on interface interface\_name
-   _ip_—The real IP address
-   _port_—The TCP or UDP port
-   interface\_name—The name of the interface on which the policy is applied

**Recommended Action** When the limit is reached, any new connection request will be silently dropped. Normally an application will retry the connection, which will cause a delay or even a timeout if all retries also fail. If an application has a legitimate need for a higher number of concurrent connections, you can adjust the setting by entering the set connection per-client-max command.

### 202001

**Error Message** `%ASA-3-202001: Out of address translation slots!`

**Explanation** The ASA has no more address translation slots available.

**Recommended Action** Check the size of the global pool compared to the number of inside network clients. A PAT address may be necessary. Alternatively, shorten the timeout interval of translates and connections. This error message can also be caused by insufficient memory; reduce the amount of memory usage, or purchase additional memory, if possible.

### 202005

**Error Message** `%ASA-3-202005: Non-embryonic in embryonic list _outside_address_/_outside_port_ _inside_address_/_inside_port_`

**Explanation** A connection object (xlate) is in the wrong list.

**Recommended Action** Contact the Cisco TAC.

### 202010

**Error Message-1** `%ASA-3-202010: {NAT | PAT} pool exhausted in pool'_pool_name_' IP _ip_address__port_range [1-511 | 512-1023 | 1024-65535]_ Unable to create _protocol_ connection from _inside_interface_:_src_ip_/_src_port_ to _outside_interface_:_dest_ip_/_dest_port_.`

**Error Message-2** `%ASA-3-202010: NAT/PAT pool exhausted in pool '_pool_name_' IP _ip_address_. Unable to create connection.`

**Explanation**

-   _pool\_name_ —The name of the NAT or PAT pool. If the interface PAT or mapped IP is a raw address, pool name is logged as empty string ("").
-   _protocol_ —The protocol used to create the connection
-   _inside\_interface_ —The ingress interface
-   _src\_ip_ —The source IP address
-   _src\_port_ —The source port
-   _outside\_interface_ —The egress interface
-   _dest\_ip_ —The destination IP address
-   _dest\_port_ —The destination port

The Secure Firewall ASA has no more address translation pools available.

**Recommended Action** Use the show nat pool and show nat detail commands to determine why all addresses and ports in the pool are used up. If this occurs under normal conditions, then add additional IP addresses to the NAT/PAT pool.

### 202016

**Error Message** `%ASA-3-202016: Unable to pre-allocate SIP _ip_protocol_ secondary channel for message from _src_ifname_:_src_ip_addr_/_src_port_ to _dst_ifname_:_dest_ip_addr_/_dest_port_ with PAT and missing port information.`

**Explanation**

When SIP application generates an SDP payload with Media port set to 0, you cannot allocate a PAT xlate for such invalid port request and drop the packet with this syslog.

**Recommended Action** None. This is an application specific issue.

### 208005

**Error Message** `%ASA-3-208005: Clear (_command_) return _code_`

**Explanation** The Secure Firewall ASA received a nonzero value (an internal error) when attempting to clear the configuration in flash memory. The message includes the reporting subroutine filename and line number.

**Recommended Action** For performance reasons, the end host should be configured not to inject IP fragments. This configuration change is probably because of NFS. Set the read and write size equal to the interface MTU for NFS.

### 209003

**Error Message** `%ASA-4-209003: Fragment database limit of _number_ exceeded: src = _source_address_ , dest = _dest_address_ , proto = _protocol_ , id = _number_`

**Explanation** Too many IP fragments are currently awaiting reassembly. By default, the maximum number of fragments is 200 (to raise the maximum, see the fragment size command in the command reference guide). The Secure Firewall ASA limits the number of IP fragments that can be concurrently reassembled. This restriction prevents memory depletion at the Secure Firewall ASA under abnormal network conditions. In general, fragmented traffic should be a small percentage of the total traffic mix. An exception is in a network environment with NFS over UDP where a large percentage is fragmented traffic; if this type of traffic is relayed through the Secure Firewall ASA, consider using NFS over TCP instead. To prevent fragmentation, see the sysopt connection tcpmss bytes command in the command reference guide.

**Recommended Action** If this message persists, a denial of service (DoS) attack might be in progress. Contact the remote peer administrator or upstream provider.

### 209004

**Error Message** `%ASA-4-209004: Invalid IP fragment, size = _bytes_ exceeds maximum size = _bytes_ : src = _source_address_ , dest = _dest_address_ , proto = _protocol_ , id = _number_`

**Explanation** An IP fragment is malformed. The total size of the reassembled IP packet exceeds the maximum possible size of 65,535 bytes.

**Recommended Action** A possible intrusion event may be in progress. If this message persists, contact the remote peer administrator or upstream provider.

### 209005

**Error Message** `%ASA-4-209005: Discard IP fragment set with more than number elements: src = Too many elements are in a fragment set.`

**Explanation** The Secure Firewall ASA disallows any IP packet that is fragmented into more than 24 fragments. For more information, see the fragment command in the command reference guide.

**Recommended Action** A possible intrusion event may be in progress. If the message persists, contact the remote peer administrator or upstream provider. You can change the number of fragments per packet by using the fragment chain xxx interface\_name command.

### 209006

**Error Message** `%ASA-4-209006: Fragment queue threshold exceeded, dropped protocol fragment from IP address/port to IP address/port on outside interface.`

**Explanation** The Secure Firewall ASA drops the fragmented packets when the fragment database threshold, that is 2/3 of the queue size per interface, has exceeded.

**Recommended Action** None required.

### 210001

**Error Message** `%ASA-3-210001: LU _sw_module_name_ error = _number_`

**Explanation** A Stateful Failover error occurred.

**Recommended Action** If this error persists after traffic lessens through the Secure Firewall ASA, report this error to the Cisco TAC.

### 210002

**Error Message** `%ASA-3-210002: LU allocate block (_bytes_) failed`

**Explanation** Stateful Failover cannot allocate a block of memory to transmit stateful information to the standby Secure Firewall ASA.

**Recommended Action** Check the failover interface using the show interface command to make sure its transmit is normal. Also check the current block memory using the show block command. If current available count is 0 within any of the blocks of memory, then reload the Secure Firewall ASA software to recover the lost blocks of memory.

### 210003

**Error Message** `%ASA-3-210003: Unknown LU Object _number_`

**Explanation** Stateful Failover received an unsupported Logical Update object and was unable to process it. This can be caused by corrupted memory, LAN transmissions, and other events.

**Recommended Action** If you see this error infrequently, then no action is required. If this error occurs frequently, check the Stateful Failover link LAN connection. If the error was not caused by a faulty failover link LAN connection, determine if an external user is trying to compromise the protected network. Also check for misconfigured clients.

### 210005

**Error Message** `%ASA-3-210005: LU allocate _secondary_ (_optional_ ) connection failed for _protocol_ [_TCP_ |_UDP_ ] connection from _ingress interface name_ :_Real IP Address_ /_Real Port_ to _egress interface name_ :_Real IP Address_ /_Real Port_`

**Explanation** Stateful Failover cannot allocate a new connection on the standby unit. This may be caused by little or no RAM memory available within the Secure Firewall ASA. This could additionally be caused by flow creation failure due to resource limitation or reaching configured resource usage limits.

| ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)

**Note** | ___

The _secondary_ field in the syslog message is optional and appears only if the connection is a secondary connection.

___ |
|--------|-------------------------------------------------------------------------------------------------------------------------|

**Recommended Action** Check the available memory using the show memory command to make sure that the Secure Firewall ASA has free memory. If there is no available memory, add more physical memory to the Secure Firewall ASA. Check resource limitation using the show resource usage command and show asp drop to ensure that the device is not reaching the resource limitation.

### 210006

**Error Message** `%ASA-3-210006: LU look NAT for _IP_address_ failed`

**Explanation** Stateful Failover was unable to locate a NAT group for the IP address on the standby unit. The active and standby Secure Firewall ASAs may be out-of-sync with each other.

**Recommended Action** Use the write standby command on the active unit to synchronize system memory with the standby unit.

### 210007

**Error Message** `%ASA-3-210007: LU allocate xlate failed for _type_-_static__dynamic_ _NAT_ translation from _PAT_:_secondary(optional)_/_protocol_ (_ingress_interface_name_/_Real_IP_Address_) to _real_port_:_Mapped_IP_Address_/_Mapped_Port_ (_egress_interface_name_/_Real_IP_Address_)`

**Explanation** Stateful Failover failed to allocate a translation slot record.

**Recommended Action** Check the available memory by using the show memory command to make sure that the Secure Firewall ASA has free memory available. If no memory is available, add more memory.

### 210008

**Error Message** `%ASA-3-210008: LU no xlate for _inside_address_/_inside_port_ _outside_address_/_outside_port_`

**Explanation** The Secure Firewall ASA cannot find a translation slot record for a Stateful Failover connection; as a result, the Secure Firewall ASA cannot process the connection information.

**Recommended Action** Use the write standby command on the active unit to synchronize system memory between the active and standby units.

### 210010

**Error Message** `%ASA-3-210010: LU make UDP connection for _outside_address_:_outside_port_ _inside_address_:_inside_port_ failed`

**Explanation** Stateful Failover was unable to allocate a new record for a UDP connection.

**Recommended Action** Check the available memory by using the show memory command to make sure that the Secure Firewall ASA has free memory available. If no memory is available, add more memory.

### 210020

**Error Message** `%ASA-3-210020: LU PAT port _port_ reserve failed`

**Explanation** Stateful Failover is unable to allocate a specific PAT address that is in use.

**Recommended Action** Use the write standby command on the active unit to synchronize system memory between the active and standby units.

### 210021

**Error Message** `%ASA-3-210021: LU create static xlate _global_address_ ifc _interface_name_ failed`

**Explanation** Stateful Failover is unable to create a translation slot.

**Recommended Action** Enter the write standby command on the active unit to synchronize system memory between the active and standby units.

### 210022

**Error Message** `%ASA-6-210022: LU missed _number_ updates`

**Explanation** Stateful Failover assigns a sequence number for each record sent to the standby unit. When a received record sequence number is out of sequence with the last updated record, the information in between is assumed to be lost, and this error message is sent as a result.

**Recommended Action** Unless LAN interruptions occur, check the available memory on both Secure Firewall ASA units to ensure that enough memory is available to process the stateful information. Use the show failover command to monitor the quality of stateful information updates.

## Messages 211001 to 219002

This chapter includes messages from 211001 to 219002.

### 211001

**Error Message** `%ASA-3-211001: Memory allocation Error`

**Explanation** The Secure Firewall ASA failed to allocate RAM system memory.

**Recommended Action** If this message occurs periodically, it can be ignored. If it repeats frequently, contact the Cisco TAC.

### 211003

**Error Message** `%ASA-3-211003: Error in computed percentage CPU usage value`

**Explanation** The percentage of CPU usage is greater than 100 percent.

**Recommended Action** If this message occurs periodically, it can be ignored. If it repeats frequently, contact the Cisco TAC.

### 211004

**Error Message** `%ASA-1-211004: WARNING: Minimum Memory Requirement for _device_ version _ver_ not met. _min_ MB required, _actual_ MB found.`

**Explanation** The Secure Firewall ASA does not meet the minimum memory requirements for this version.

-   ver—Running image version number
-   min—Minimum required amount of RAM to run the installed image.

-   actual—Amount of RAM currently installed in the system

**Recommended Action** Install the required amount of RAM.

### 212001

**Error Message** `%ASA-3-212001: Unable to open SNMP channel (UDP port _port_) on interface "_interface_number_", error code = _code_`

**Explanation** The Secure Firewall ASA is unable to receive SNMP requests destined for the Secure Firewall ASA from SNMP management stations located on this interface. The SNMP traffic passing through the Secure Firewall ASA on any interface is not affected. The error codes are as follows:

-   An error code of -1 indicates that the Secure Firewall ASA cannot open the SNMP transport for the interface. This can occur when the user attempts to change the port on which SNMP accepts queries to one that is already in use by another feature. In this case, the port used by SNMP will be reset to the default port for incoming SNMP queries (UDP 161).
-   An error code of -2 indicates that the Secure Firewall ASA cannot bind the SNMP transport for the interface.

**Recommended Action** After the Secure Firewall ASA reclaims some of its resources when traffic is lighter, reenter the snmp-server host command for that interface.

### 212002

**Error Message** `%ASA-3-212002: Unable to open SNMP trap channel (UDP port _port_) on interface "_interface_number_", error code = _code_`

**Explanation** The Secure Firewall ASA is unable to send its SNMP traps from the Secure Firewall ASA to SNMP management stations located on this interface. The SNMP traffic passing through the Secure Firewall ASA on any interface is not affected. The error codes are as follows:

-   An error code of -1 indicates that the Secure Firewall ASA cannot open the SNMP trap transport for the interface.
-   An error code of -2 indicates that the Secure Firewall ASA cannot bind the SNMP trap transport for the interface.
-   An error code of -3 indicates that the Secure Firewall ASA cannot set the trap channel as write-only.

**Recommended Action** After the Secure Firewall ASA reclaims some of its resources when traffic is lighter, reenter the snmp-server host command for that interface.

### 212003

**Error Message** `%ASA-3-212003: Unable to receive an SNMP request on interface "_interface_number_", error code = _code_, will try again.`

**Explanation** An internal error occurred in receiving an SNMP request destined for the Secure Firewall ASA on the specified interface. The error codes are as follows:

-   An error code of -1 indicates that the Secure Firewall ASA cannot find a supported transport type for the interface.
-   An error code of -5 indicates that the Secure Firewall ASA received no data from the UDP channel for the interface.
-   An error code of -7 indicates that the Secure Firewall ASA received an incoming request that exceeded the supported buffer size.
-   An error code of -14 indicates that the Secure Firewall ASA cannot determine the source IP address from the UDP channel.
-   An error code of -22 indicates that the Secure Firewall ASA received an invalid parameter.

**Recommended Action** None required. The Secure Firewall ASA SNMP agent goes back to wait for the next SNMP request.

### 212004

**Error Message** `%ASA-3-212004: Unable to send an SNMP response to _IP_address_, error code = _port_`

**Explanation** An internal error occurred in sending an SNMP response from the Secure Firewall ASA to the specified host on the specified interface. The error codes are as follows:

-   An error code of -1 indicates that the Secure Firewall ASA cannot find a supported transport type for the interface.
-   An error code of -2 indicates that the Secure Firewall ASA sent an invalid parameter.
-   An error code of -3 indicates that the Secure Firewall ASA was unable to set the destination IP address in the UDP channel.
-   An error code of -4 indicates that the Secure Firewall ASA sent a PDU length that exceeded the supported UDP segment size.
-   An error code of -5 indicates that the Secure Firewall ASA was unable to allocate a system block to construct the PDU.

**Recommended Action** None required.

### 212005

**Error Message** `%ASA-3-212005: incoming SNMP request (_number_ bytes) from _interface_name_ exceeds data buffer size, discarding this SNMP request.`

**Explanation** The length of the incoming SNMP request that is destined for the Secure Firewall ASA exceeds the size of the internal data buffer (512 bytes) used for storing the request during internal processing. The Secure Firewall ASA is unable to process this request. The SNMP traffic passing through the Secure Firewall ASA on any interface is not affected.

**Recommended Action** Have the SNMP management station resend the request with a shorter length. For example, instead of querying multiple MIB variables in one request, try querying only one MIB variable in a request. You may need to modify the configuration of the SNMP manager software.

### 212006

**Error Message** `%ASA-3-212006: Dropping SNMP request from _src_addr_/_src_port_ to _ifc_:_dst_addr_/_dst_port_ because: _reason__username_`

**Explanation** The Secure Firewall ASA cannot process the SNMP request being sent to it for the following reasons:

-   user not found—The username cannot be located in the local SNMP user database.
-   username exceeds maximum length—The username embedded in the PDU exceeds the maximum length allowed by the SNMP RFCs.
-   authentication algorithm failure—An authentication failure caused by an invalid password or a packet authenticated using the incorrect algorithm.
-   privacy algorithm failure—A privacy failure caused by an invalid password or a packet encrypted using the incorrect algorithm.
-   error decrypting request—An error occurred in the platform crypto module decrypting the user request.
-   error encrypting response—An error occurred in the platform crypto module encrypting the user response or trap notification.
-   engineBoots has reached maximum value—The engineBoots variable has reached the maximum allowed value. For more information, see message 212011.

| ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)

**Note** | ___

The username appears after each reason listed.

___ |
|--------|----------------------------------------------------|

**Recommended Action** Check the Secure Firewall ASA SNMP server settings and confirm that the NMS configuration is using the expected user, authentication, and encryption settings. Enter the show crypto accelerator statistics command to isolate errors in the platform crypto module.

### 212009

**Error Message** `%ASA-5-212009: Configuration request for SNMP group _groupname_ failed. User _username_ _reason_`

**Explanation** A user has tried to change the SNMP server group configuration. One or more users that refer to the group have insufficient settings to comply with the requested group changes.

-   groupname—A string that represents the group name
-   _username_ —A string that represents the username
-   reason—A string that represents one of the following reasons:

_\- missing auth-password_ —A user has tried to add authentication to the group, and the user has not specified an authentication password

_\- missing priv-password_ —A user has tried to add privacy to the group, and the user has not specified an encryption password

_\- reference group intended for removal_ —A user has tried to remove a group that has users belonging to it

**Recommended Action** The user must update the indicated user configurations before changing the group or removing indicated users, and then add them again after making changes to the group.

### 212010

**Error Message** `%ASA-3-212010: Configuration request for SNMP user _s_ failed. Host _s_ _reason_`

**Explanation** A user has tried to change the SNMP server user configuration by removing one or more hosts that reference the user. One message is generated per host.

-   %s—A string that represents the username or hostname
-   _reason_ —A string the represents the following reason:

_\- references user intended for removal—_ The name of the user to be removed from the host.

**Recommended Action** The user must either update the indicated host configuration before changing a user or remove the indicated hosts, then add them again after making changes to the user.

### 212011

**Error Message** `%ASA-3-212011: engineBoots is set to maximum value. Reason: _Reason_. User intervention necessary.`

For example:

```vbnet
%ASA-3-212011: SNMP engineBoots is set to maximum value. Reason: error accessing persistent data. User intervention necessary.
```

**Explanation** The device has rebooted 214783647 times, which is the maximum allowed value of the engineBoots variable, or an error reading the persistent value from flash memory has occurred. The engineBoots value is stored in flash memory in the flash:/snmp/_ctx-name_ file_,_ where _ctx-name_ is the name of the context. In single mode, the name of this file is flash:/snmp/single\_vf. In multi-mode, the name of the file for the admin context is flash:/snmp/admin. During a reboot, if the device is unable to read from the file or write to the file, the engineBoots value is set to the maximum.

-   %s—A string that represents the reason that the engineBoots value is set to the maximum allowed value. The two valid strings are “device reboots” and “error accessing persistent data.”

**Recommended Action** For the first string, the administrator must delete all SNMP Version 3 users and add them again to reset the engineBoots variable to 1. All subsequent Version 3 queries will fail until all users have been removed. For the second string, the administrator must delete the context-specific file, then delete all SNMP Version users, and add them again to reset the engineBoots variable to 1. All subsequent Version 3 queries will fail until all users have been removed.

### 212012

**Error Message** `%ASA-3-212012: Unable to write engine data to persistent storage.`

**Explanation** The SNMP engine data is written to the file, flash:/snmp/_context-name_ . For example: in single mode, the data is written to the file, flash:/snmp/single\_vf. In the admin context in multi-mode, the file is written to the directory, flash:/snmp/admin. The error may be caused by a failure to create the flash:/snmp directory or the flash:/snmp/_context-name_ file. The error may also be caused by a failure to write to the file.

**Recommended Action** The system administrator should remove the flash:/snmp/_context-name_ file, then remove all SNMP Version 3 users, and add them again. This procedure should recreate the flash:/snmp/_context-name_ file. If the problem persists, the system administrator should try reformatting the flash.

### 213001

**Error Message** `%ASA-3-213001: PPTP control daemon socket io _string_, errno = _number_`

**Explanation** An internal TCP socket I/O error occurred.

**Recommended Action** Contact the Cisco TAC.

### 213002

**Error Message** `%ASA-3-213002: PPTP tunnel hashtable insert failed, peer = _IP_address_`

**Explanation** An internal software error occurred while creating a new PPTP tunnel.

**Recommended Action** Contact the Cisco TAC.

### 213003

**Error Message** `%ASA-3-213003: PPP virtual interface _interface_number_ isn't opened`

**Explanation** An internal software error occurred while closing a PPP virtual interface.

**Recommended Action** Contact the Cisco TAC.

### 213004

**Error Message** `%ASA-3-213004: PPP virtual interface _interface_number_ client ip allocation failed`

**Explanation** An internal software error occurred while allocating an IP address to the PPTP client when the IP local address pool was depleted.

**Recommended Action** Consider allocating a larger pool with the ip local pool command.

### 213005

**Error Message** `%ASA-3-213005: L2TP: Dynamic-Access-Policy action is not continue,"abort connection"`

**Explanation** The DAP is dynamically created by selecting configured access policies based on the authorization rights of the user and the posture assessment results of the remote endpoint device. The resulting dynamic policy indicates that the session should be terminated.

**Recommended Action** None required.

### 213006

**Error Message** `%ASA-3-213006: L2TP: Dynamic-Access-Policy failure`

**Explanation** There was either an error in retrieving the DAP policy record data, or the action configuration was missing.

**Recommended Action** A configuration change might have resulted in deleting a DAP record. Use ASDM to recreate the DAP record.

### 213007

**Error Message** `%ASA-4-213007: L2TP: Failed to install Redirect URL: _redirect_URL_ Redirect ACL: _non_exist_ for _assigned_IP_.`

**Explanation** An error occurred for an L2TP connection when the redirect URL was installed and the ACL was received from the ISE, but the redirect ACL does not exist on the ASA.

-   _redirect URL_ —The URL for the HTTP traffic redirection
-   _assigned IP_ —The IP address that is assigned to the user

**Recommended Action** Configure the redirect ACL on the ASA.

### 214001

**Error Message** `%ASA-2-214001: Terminating manager session from _IP_address_ on interface _interface_name_. Reason: incoming encrypted data (_number_ bytes) longer than _number_ bytes`

**Explanation** An incoming encrypted data packet destined for the Secure Firewall ASA management port indicates a packet length exceeding the specified upper limit. This may be a hostile event. The Secure Firewall ASA immediately terminates this management connection.

**Recommended Action** Ensure that the management connection was initiated by Cisco Secure Policy Manager.

### 215001

**Error Message** `%ASA-2-215001:Bad route_compress() call, sdb = _number_`

**Explanation** An internal software error occurred.

**Recommended Action** Contact the Cisco TAC.

### 217001

**Error Message** `%ASA-2-217001: No memory for _string_ in _string_`

**Explanation** An operation failed because of low memory.

**Recommended Action** If sufficient memory exists, then send the error message, the configuration, and any details about the events leading up to the error to the Cisco TAC.

### 216001

**Error Message** `%ASA-n-216001: internal error in _function_: _message_`

**Explanation** Various internal errors have occurred that should not appear during normal operation. The severity level varies depending on the cause of the message.

-   n—The message severity
-   function—The affected component
-   message—A message describing the cause of the problem

**Recommended Action** Search the Bug Toolkit for the specific text message and try to use the Output Interpreter to resolve the problem. If the problem persists, contact the Cisco TAC.

### 216002

**Error Message** `%ASA-3-216002: Unexpected event (major: _major_id_ , minor: _minor_id_ ) received by _task_string_ in _function_ at line: _line_num_`

**Explanation** A task registers for event notification, but the task cannot handle the specific event. Events that can be watched include those associated with queues, booleans, and timer services. If any of the registered events occur, the scheduler wakes up the task to process the event. This message is generated if an unexpected event woke up the task, but it does not know how to handle the event.

If an event is left unprocessed, it can wake up the task very often to make sure that it is processed, but this should not occur under normal conditions. If this message appears, it does not necessarily mean the device is unusable, but something unusual has occurred and needs to be investigated.

-   _major\_id_ —Event identifier
-   _minor\_id_ — Event identifier
-   _task\_string_ —Custom string passed by the task to identify itself
-   _function_ —The function that received the unexpected event
-   _line\_num_ —Line number in the code

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 216003

**Error Message** `%ASA-3-216003: Unrecognized timer _timer_ptr_ , _timer_id_ received by _task_string_ in _function_ at line: _line_num_`

**Explanation** An unexpected timer event woke up the task, but the task does not know how to handle the event. A task can register a set of timer services with the scheduler. If any of the timers expire, the scheduler wakes up the task to take action. This message is generated if the task is awakened by an unrecognized timer event.

An expired timer, if left unprocessed, wakes up the task continuously to make sure that it is processed, and this is undesirable. This should not occur under normal conditions. If this message appears, it does not necessarily mean the device is unusable, but something unusual has occurred and needs to be investigated.

-   _timer\_ptr_ —Pointer to the timer
-   _timer\_id_ —Timer identifier
-   _task\_string_ —Custom string passed by the task to identify itself
-   _function_ —The function that received the unexpected event
-   _line\_num_ —Line number in the code

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 216004

**Error Message** `%ASA-4-216004: prevented: _error_ in _function_ at _file_(_line_) - _stack trace_`

**Explanation** An internal logic error has occurred, which should not occur during normal operation.

-   _error_ —Internal logic error. Possible errors include the following:

\- Exception

\- Dereferencing null pointer

\- Array index out of bounds

\- Invalid buffer size

\- Writing from input

\- Source and destination overlap

\- Invalid date

\- Access offset from array indices

-   _function_ —The calling function that generated the error
-   _file(line)_ —The file and line number that generated the error
-   _stack trace_ —Full call stack traceback, starting with the calling function. For example: (“0x001010a4 0x00304e58 0x00670060 0x00130b04”)

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 216005

**Error Message** `%ASA-1-216005: ERROR: Duplex-mismatch on _interface_name_ resulted in transmitter lockup. A soft reset of the switch was performed.`

**Explanation** A duplex mismatch on the port caused a problem in which the port can no longer transmit packets. This condition was detected, and the switch was reset to autorecover. This message applies only to the ASA 5505.

-   _interface\_name_ —The interface name that was locked up

**Recommended Action** A duplex mismatch exists between the specified port and the ASA 5505 that is connected to it. Correct the duplex mismatch by either setting both devices to autorecover, or hard coding the duplex mismatch for both devices to be the same.

### 218001

**Error Message** `%ASA-2-218001: Failed Identification Test in _slot#_ [_fail_ #/_res_ ].`

**Explanation** The module in slot# of the Secure Firewall ASA cannot be identified as a genuine Cisco product. Cisco warranties and support programs apply only to genuine Cisco products. If Cisco determines that the cause of a support issue is related to non-Cisco memory, SSM modules, SSC modules, or other modules, Cisco may deny support under your warranty or under a Cisco support program such as SmartNet.

**Recommended Action** If this message recurs, copy it exactly as it appears on the console or in the system log. Research and try to resolve the error using the Output Interpreter. Also perform a search with the Bug Toolkit. If the problem persists, contact the Cisco TAC.

### 218002

**Error Message** `%ASA-2-218002: Module _slot#_ is a registered proto-type for _Cisco_ Lab use only, and not certified for live network operation.`

**Explanation** The hardware in the specified location is a prototype module that came from a Cisco lab.

**Recommended Action** If this message reoccurs, copy it exactly as it appears on the console or in the system log. Research and try to resolve the error using the Output Interpreter. Also perform a search with the Bug Toolkit. If the problem persists, contact the Cisco TAC.

### 218003

**Error Message** `%ASA-2-218003: Module Version in _slot#_ is obsolete. The module in slot = _slot#_ is obsolete and must be returned via RMA to _Cisco_ Manufacturing. If it is a lab unit, it must be returned to Proto Services for upgrade.`

**Explanation** Obsolete hardware has been detected or the show module command has been run for the module. This message is generated once per minute after it first appears.

**Recommended Action** If this message recurs, copy it exactly as it appears on the console or in the system log. Research and try to resolve the error using the Output Interpreter. Also perform a search with the Bug Toolkit. If the problem persists, contact the Cisco TAC.

### 218004

**Error Message** `%ASA-2-218004: Failed Identification Test in _slot#_ [_fail#_/_res_]`

**Explanation** A problem occurred while identifying hardware in the specified location.

**Recommended Action** If this message recurs, copy it exactly as it appears on the console or in the system log. Research and try to resolve the error using the Output Interpreter. Also perform a search with the Bug Toolkit. If the problem persists, contact the Cisco TAC.

### 218005

**Error Message** `%ASA-2-218005: Inconsistency detected in the system information programmed in non-volatile memory.`

**Explanation** System information programmed in non-volatile memory is not consistent. This syslog will be generated during bootup if Secure Firewall ASA detects that the contents of the IDPROM are not identical to the contents of ACT2 EEPROM. Since the IDPROM and ACT2 EEPROM are programmed with exactly the same contents in manufacturing, this would happen either due to an error in manufacturing or if the IDPROM contents are tampered with.

**Recommended Action** If the message recurs, collect the output of the show tech-support command and contact Cisco TAC.

### 219002

**Error Message** `%ASA-3-219002: _I2C_API_name_() error, slot = _slot_number_, device = _device_number_, address = _address_, byte count = _count_. Reason: _reason_string_`

**Explanation** The I2C serial bus API has failed because of a hardware or software problem.

-   _I2C\_API\_name_ —The I2C API that failed, which can be one of the following:
    -   I2C\_read\_byte\_w\_wait()
    -   I2C\_read\_word\_w\_wait()
    -   I2C\_read\_block\_w\_wait()
    -   I2C\_write\_byte\_w\_wait()
    -   I2C\_write\_word\_w\_wait()
    -   I2C\_write\_block\_w\_wait()
    -   I2C\_read\_byte\_w\_suspend()
    -   I2C\_read\_word\_w\_suspend()
    -   I2C\_read\_block\_w\_suspend()
    -   I2C\_write\_byte\_w\_suspend()
    -   I2C\_write\_word\_w\_suspend()
    -   I2C\_write\_block\_w\_suspend()
-   _slot\_number_ —The hexadecimal number of the slot where the I/O operation that generated the message occurred. The slot number cannot be unique to a slot in the chassis. Depending on the chassis, two different slots might have the same I2C slot number. Also, the value is not necessarily less than or equal to the number of slots. The value depends on the way the I2C hardware is wired.
-   _device\_number_ —The hexadecimal number of the device on the slot for which the I/O operation was performed
-   _address_ —The hexadecimal address of the device on which the I/O operation occurred
-   _byte\_count_ —The byte count in decimal format of the I/O operation
-   _error\_string_ —The reason for the error, which can be one of the following:
    -   I2C\_BUS\_TRANSACTION\_ERROR
    -   I2C\_CHKSUM\_ERROR
    -   I2C\_TIMEOUT\_ERROR
    -   I2C\_BUS\_COLLISION\_ERROR
    -   I2C\_HOST\_BUSY\_ERROR
    -   I2C\_UNPOPULATED\_ERROR
    -   I2C\_SMBUS\_UNSUPPORT
    -   I2C\_BYTE\_COUNT\_ERROR
    -   I2C\_DATA\_PTR\_ERROR

**Recommended Action** Perform the following steps:

1.  Log and review the messages and the errors associated with the event. If the message does not occur continuously and disappears after a few minutes, it might be because the I2C serial bus is busy.
2.  Reboot the software running on the Secure Firewall ASA.
3.  Power cycle the device. When you turn off the power, make sure that you wait several seconds before turning the power on.
4.  If the problem persists, contact the Cisco TAC.