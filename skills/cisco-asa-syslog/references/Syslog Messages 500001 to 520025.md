## Messages 500001 to 504002

This chapter includes messages from 500001 to 504002.

### 500001

**Error Message-1** `%ASA-5-500001: ActiveX content modified src _forward_ip_address_ dest _reverse_ip_address_ on interface _interface_name_`

**Error Message-2** `%ASA-5-500001: ActiveX content in java script is modified: src _forward_ip_address_ dest _reverse_ip_address_ on interface _interface_name_`

**Explanation** Ensure the blocking of Java/ActiveX content present in Java script when the policy (filter Java (or) filter ActiveX) is enabled on the Secure Firewall ASA.

**Recommended Action** None required.

### 500002

**Error Message-1** `%ASA-5-500002: Java content modified: src _forward_ip_address_ dest _reverse_ip_address_ on interface _interface_name_`

**Error Message-2** `%ASA-5-500002: Java content in java script is modified: src _forward_ip_address_ dest _reverse_ip_address_ on interface _interface_name_`

**Explanation** Ensure the blocking of Java/ActiveX content present in Java script when the policy (filter Java (or) filter ActiveX) is enabled on the Secure Firewall ASA.

**Recommended Action** None required.

### 500003

**Error Message** `%ASA-5-500003: Bad TCP hdr length (hdrlen=_bytes_, pktlen=_bytes_) from _source_address_/_source_port_ to _dest_address_/_dest_port_, flags:_tcp_flags_, on interface_interface_name_`

**Explanation** A header length in TCP was incorrect. Some operating systems do not handle TCP resets (RSTs) correctly when responding to a connection request to a disabled socket. If a client tries to connect to an FTP server outside the Secure Firewall ASA and the FTP server is not listening, then it sends an RST. Some operating systems send incorrect TCP header lengths, which causes this problem. UDP uses ICMP port unreachable messages.

The TCP header length may indicate that it is larger than the packet length, which results in a negative number of bytes being transferred. A negative number appears by a message as an unsigned number, which makes it appear much larger than it would be normally; for example, it may show 4 GB transferred in one second. This message should occur infrequently.

**Recommended Action** None required.

### 500004

**Error Message** `%ASA-4-500004: Invalid transport field for protocol=_protocol_, from _source_address_/_source_port_ to _dest_address_/_dest_port_`

**Explanation** An invalid transport number was used, in which the source or destination port number for a protocol is zero. The protocol value is 6 for TCP and 17 for UDP.

**Recommended Action** If these messages persist, contact the administrator of the peer.

### 500005

**Error Message** `%ASA-3-500005: Connection terminated for _protocol_ from _in_ifc_name_:_src_adddress_/_src_port_ to _out_ifc_name_:_dest_address_/_dest_port_ due to invalid combination of inspections on same flow. Inspect _inspect_name_ is not compatible with filter _filter_name_`

**Explanation** A connection matched with single or multiple inspection and/or single or multiple filter features that are not allowed to be applied to the same connection.

-   _protocol—_ The protocol that the connection was using
-   _in\_ifc\_name_ —The input interface name
-   _src\_address_ —The source IP address of the connection
-   _src\_port_ —The source port of the connection
-   _out\_ifc\_name_ —The output interface name
-   _dest\_address_ —The destination IP address of the connection
-   _dest\_port_ —The destination port of the packet
-   _inspect\_name_ —The inspect or filter feature name
-   _filter\_name_ —The filter feature name

**Recommended Action** Review the class-map, policy-map, service-policy, and/or filter command configurations that are causing the referenced inspection and/or filter features that are matched for the connection. The rules for inspection and filter feature combinations for a connection are as follows:

-   -   The inspect http \[http-policy-map\] and/or filter url and/or filter java and/or filter activex commands are valid.
    -   The inspect ftp \[ftp-policy-map\] and/or filter ftp commands are valid.
    -   The filter https command with any other inspect command or filter command is not valid.

Besides these listed combinations, any other inspection and/or filter feature combinations are not valid.

### 500006

**Error Message** `%ASA-4-500006: For flow _inside_:_IP_Address_/_port_ to _outside_:_IP_Address_/_port_ :_existing_flow_message_:_connection_id_`

**Explanation** This message is generated when staleness in pinhole flows persist due to failure to clear timeout expiry, interface flap, and so on. The flow message with connection ID in the message helps in debugging the issue:

-   _Existing flow message_—Displays the current flow information for the connection id, such as:
    
    -   found existing flow
        
    -   pin-hole consumption maybe in progress
        
    -   pin-hole delete
        
-   _connection id_—Displays the unique connection ID.
    

**Recommended Action** None.

### 501101

**Error Message** `%ASA-5-501101: User transitioning priv level`

**Explanation** The privilege level of a command was changed.

**Recommended Action** None required.

### 502101

**Error Message** `%ASA-5-502101: New user added to local dbase: Uname: _user_ Priv: _privilege_level_ Encpass: *****`

**Explanation** A new username record was created, which included the username, privilege level, and encrypted password.

**Recommended Action** None required.

### 502102

**Error Message** `%ASA-5-502102: User deleted from local dbase: Uname: _user_ Priv: _privilege_level_ Encpass: *****`

**Explanation** A username record was deleted, which included the username, privilege level, and encrypted password.

**Recommended Action** None required.

### 502103

**Error Message** `%ASA-5-502103: User priv level changed: Uname: _user_ From: _privilege_level_ To: _privilege_level_`

**Explanation** The privilege level of a user changed.

**Recommended Action** None required.

### 502111

**Error Message** `%ASA-5-502111: New group policy added: name: _policy_name_ Type: _policy_type_`

**Explanation** A group policy was configured using the group-policy CLI command.

-   policy\_name—The name of the group policy
-   policy\_type—Either internal or external

**Recommended Action** None required.

### 502112

**Error Message** `%ASA-5-502112: Group policy deleted: name: _policy_name_ Type: _policy_type_`

**Explanation** A group policy has been removed using the group-policy CLI command.

-   policy\_name—The name of the group policy
-   policy\_type—Either internal or external

**Recommended Action** None required.

### 503001

**Error Message** `%ASA-5-503001: Process number, Nbr _IP_address_ on _interface_name_ from _string_ to _string_ , _reason_`

**Explanation** An OSPFv2 neighbor has changed its state. The message describes the change and the reason for it. This message appears only if the log-adjacency-changes command is configured for the OSPF process.

**Recommended Action** Copy the message exactly as it appears, and report it to the Cisco TAC.

### 503002

**Error Message** `%ASA-5-503002: Last valid authentication key for neighbor _nameif_ expires`

**Explanation** None of the security associations have a lifetime that include the current system time.

**Recommended Action** Configure a new security association or alter the lifetime of a current security association.

### 503003

**Error Message** `%ASA-5-503003: Expired key ID _sent | received_ used by neighbor _nameif_`

**Explanation** The Key ID configured on the interface expired.

**Recommended Action** Configure a new key.

### 503004

**Error Message** `%ASA-5-503004: No key ID _key-id_ for neighbor _key-chain-name_`

**Explanation** OSPF has been configured to use cryptographic authentication, however a key or password has not been configured.

**Recommended Action** Configure a new security association or alter the lifetime of a current security association.

### 503005

**Error Message** `%ASA-5-503005: No crypto algorithm for neighbor _key-id_ key ID _key-chain-name_`

**Explanation** OSPF has been configured to use cryptographic authentication, however an algorithm has not been configured.

**Recommended Action** Configure a cryptographic-algorithm for the security association.

### 503101

**Error Message** `%ASA-5-503101: Process _d_, Nbr _i_ on _s_ from _s_ to _s_, _s_`

**Explanation** An OSPFv3 neighbor has changed its state. The message describes the change and the reason for it. This message appears only if the log-adjacency-changes command is configured for the OSPF process.

**Recommended Action** None required.

### 504001

**Error Message** `%ASA-5-504001: Security context _context_name_ was added to the system`

**Explanation** A security context was successfully added to the Secure Firewall ASA.

**Recommended Action** None required.

### 504002

**Error Message** `%ASA-5-504002: Security context _context_name_ was removed from the system`

**Explanation** A security context was successfully removed from the Secure Firewall ASA.

**Recommended Action** None required.

## Messages 505001 to 520025

This chapter includes messages from 505001 to 520025.

### 505001

**Error Message** `%ASA-5-505001: Module _string_one_ is shutting down. Please wait...`

**Explanation** A module is being shut down.

**Recommended Action** None required.

### 505002

**Error Message** `%ASA-5-505002: Module _ips_ is reloading. Please wait...`

**Explanation** An IPS module is being reloaded.

**Recommended Action** None required.

### 505003

**Error Message** `%ASA-5-505003: Module _string_one_ is resetting. Please wait...`

**Explanation** A module is being reset.

**Recommended Action** None required.

### 505004

**Error Message** `%ASA-5-505004: Module _string_one_ shutdown is complete.`

**Explanation** A module has been shut down.

**Recommended Action** None required.

### 505005

**Error Message** `%ASA-5-505005: Module _module_name_ is initializing control communication. Please wait...`

**Explanation** A module has been detected, and the Secure Firewall ASA is initializing control channel communication with it.

**Recommended Action** None required.

### 505006

**Error Message** `%ASA-5-505006: Module _string_one_ is Up.`

**Explanation** A module has completed control channel initialization and is in the UP state.

**Recommended Action** None required.

### 505007

**Error Message** `%ASA-5-505007: Module _module_id_ is recovering. Please wait...`

**Error Message** `%ASA-5-505007: Module _prod_id_ in slot _slot_num_ is recovering. Please wait...`

**Explanation** A software module is being recovered with the sw-module module _service-module-name_ recover boot command, or a hardware module is being recovered with the hw-module module _slotnum_ recover boot command.

-   module\_id—The name of the software services module.
-   prod\_id—The product ID string.
-   _slot\_num_ —The slot in which the hardware services module is installed. Slot 0 indicates the system main board, and slot 1 indicates the module installed in the expansion slot.

**Recommended Action** None required.

### 505008

**Error Message** `%ASA-5-505008: Module _module_id_ software is being updated to v_newver_ (currently v_ver_)`

**Error Message** `%ASA-5-505008: Module` _module\_id_ in slot _slot\_num_ software is being updated to _newver_ (currently _ver_ )

**Explanation** The services module software is being upgraded. The update is proceeding normally.

-   _module\_id_ —The name of the software services module
-   _slot\_num_ —The slot number that contains the hardware services module
-   _\>newver_ —The new version number of software that was not successfully written to the module (for example, 1.0(1)0)
-   _\>ver_ —The current version number of the software on the module (for example, 1.0(1)0)

**Recommended Action** None required.

### 505009

**Error Message** `%ASA-5-505009: Module in slot _string_one_ software was updated to v_newver_ (previously v_prevver_)`

**Explanation** The 4GE SSM module software was successfully upgraded.

-   _string one_ —The text string that specifies the module
-   _newver_ —The new version number of software that was not successfully written to the module (for example, 1.0(1)0)
-   _ver_ —The current version number of the software on the module (for example, 1.0(1)0)

**Recommended Action** None required.

### 505010

**Error Message** `%ASA-5-505010: Module in slot _slot_ removed`

**Explanation** An SSM was removed from the Secure Firewall ASA chassis.

-   slot—The slot from which the SSM was removed

**Recommended Action** None required.

### 505011

**Error Message** `%ASA-1-505011: Module _ips_ data channel communication is UP.`

**Explanation** The data channel communication recovered from a DOWN state.

**Recommended Action** None required.

### 505012

**Error Message** `%ASA-5-505012: Module _module_id_, application removed "_application_", version "_ver_num_" _version_`

**Error Message** `%ASA-5-505012: Module _prod_id_ in slot _slot_num_ , application stopped _application_ , version _version_`

**Explanation** An application was stopped or removed from a services module. This may occur when the services module upgraded an application or when an application on the services module was stopped or uninstalled.

-   module\_id—The name of the software services module
-   _prod\_id_ —The product ID string for the device installed in the hardwre services module
-   _slot\_num_ —The slot in which the application was stopped
-   application—The name of the application stopped
-   version—The application version stopped

**Recommended Action** If an upgrade was not occurring on the 4GE SSM or the application was not intentionally stopped or uninstalled, review the logs from the 4GE SSM to determine why the application stopped.

### 505013

**Error Message** `%ASA-5-505013: Module _module_id_, application reloading "_application_", version "_version_" _newapplication_`

**Error Message** `%ASA-5-505013: Module _prod_id_ in slot _slot_nunm_ application changed from: _application_ version _version_ to: _newapplication_ version _newversion_ .`

**Explanation** An application version changed, such as after an upgrade. A software update for the application on the services module is complete.

-   module\_id—The name of the software services module
-   application—The name of the application that was upgraded
-   version—The application version that was upgraded
-   prod\_id—The product ID string for the device installed in the hardware services module
-   slot\_num—The slot in which the application was upgraded
-   application—The name of the application that was upgraded
-   version—The application version that was upgraded
-   newapplication—The new application name
-   newversion—The new application version

**Recommended Action** Verify that the upgrade was expected and that the new version is correct.

### 505014

**Error Message** `%ASA-1-505014: Module _module_id_, application down "_name_", version "_version_" _reason_`

**Error Message** `%ASA-1-505014: Module _prod_id_ in slot _slot_num_ , application down _name_ , version _version_ _reason_`

**Explanation** The application running on the module is disabled.

-   module\_id—The name of the software services module
-   prod\_id—The product ID string for the device installed in the hardware services module
-   _slot\_num_ —The slot in which the application was disabled. Slot 0 indicates the system main board, and slot 1 indicates the module installed in the expansion slot.
-   name—Application name (string)
-   application—The name of the application that was upgraded
-   version—The application version (string)
-   reason—Failure reason (string)

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 505015

**Error Message** `%ASA-1-505015: Module _module_id_, application up "_application_", version "_ver_num_" _version_`

**Error Message** `%ASA-1-505015: Module _prod_id_ in slot _slot_num_ , application up _application_ , version _version_`

**Explanation** The application running on the SSM in slot _slot\_num_ is up and running.

-   module\_id—The name of the software services module
-   prod\_id—The product ID string for the device installed in the hardware services module
-   _slot\_num_ —The slot in which the application is running. Slot 0 indicates the system main board, and slot 1 indicates the module installed in the expansion slot.
-   application—The application name (string)
-   version—The application version (string)

**Recommended Action** None required.

### 505016

**Error Message** `%ASA-3-505016: Module _module_id_, application changed from: "_name_" version "_version_" state "_state_" to: "_name_" version "_version_" state "_state_"`

**Error Message** `%ASA-3-505016: Module` _prod\_id_ in slot _slot\_num_ application changed from: _name_ version _version_ state _state_ to: _name version_ state _state_ .

**Explanation** The application version or a name change was detected.

-   module\_id—The name of the software services module
-   prod\_id—The product ID string for the device installed in the hardware services module
-   _slot\_num_ —The slot in which the application changed. Slot 0 indicates the system main board, and slot 1 indicates the module installed in the expansion slot.
-   name—Application name (string)
-   version—The application version (string)
-   state—Application state (string)
-   application—The name of the application that changed

**Recommended Action** Verify that the change was expected and that the new version is correct.

### 506001

**Error Message** `%ASA-5-506001: _event_source_string_ _event_string_`

**Explanation** The status of a file system has changed. The event and the source of the event that caused a file system to become available or unavailable appear. Examples of sources and events that can cause a file system status change are as follows:

-   External CompactFlash removed
-   External CompactFlash inserted
-   External CompactFlash unknown event

**Recommended Action** None required.

### 507001

**Error Message** `%ASA-5-507001: Terminating TCP-Proxy connection from _interface_inside_:_source_address_/_source_port_ to _interface_outside_:_dest_address_/_dest_port_ - reassembly limit of _limit_ bytes exceeded`

**Explanation** The assembly buffer limit was exceeded during TCP segment reassembly.

-   source\_address/source\_port—The source IP address and the source port of the packet initiating the connection
-   dest\_address/dest\_port—The destination IP address and the destination port of the packet initiating the connection
-   interface\_inside—The name of the interface on which the packet which initiated the connection arrives
-   interface\_outside—The name of the interface on which the packet which initiated the connection exits
-   limit—The configured embryonic connection limit for the traffic class

**Recommended Action** None required.

### 507002

**Error Message** `%ASA-4-507002: Data copy in proxy-mode exceeded the buffer limit`

**Explanation** An operational error occurred during processing of a fragmented TCP message.

**Recommended Action** None required.

### 507003

**Error Message** `%ASA-3-507003: _protocol_ flow from _originating_interface_:_src_ip_/_src_port_ to _dest_if_:_dest_ip_/_dest_port_ terminated by inspection engine, reason - _reason_.`

**Explanation** The TCP proxy or session API terminated a connection for various reasons, which are provided in the message.

-   protocol—The protocol for the flow
-   src\_ip—The source IP address for the flow
-   _src\_port_ —The name of the source port for the flow
-   _dest\_if_ —The destination interface for the flow
-   _dest\_ip_ —The destination IP address for the flow
-   _dest\_port_ —The destination port for the flow
-   _reason_ —The description of why the flow is being terminated by the inspection engine. Valid reasons include:

\- Failed to create flow

\- Failed to initialize session API

\- Filter rules installed/matched are incompatible

\- Failed to consolidate new buffer data with original

\- Reset unconditionally

\- Reset based on “service reset inbound” configuration

\- Disconnected, dropped packet

\- Packet length changed

\- Reset reflected back to sender

\- Proxy inspector reset unconditionally

\- Proxy inspector drop reset

\- Proxy inspector received data after FIN

\- Proxy inspector disconnected, dropped packet

\- Inspector reset unconditionally

\- Inspector drop reset

\- Inspector received data after FIN

\- Inspector disconnected, dropped packet

\- Could not buffer unprocessed data

\- Session API proxy forward failed

\- Conversion of inspect data to session data failed

\- SSL channel for TLS proxy is closed

\- The number of unprocessed segments are more than the threshold value

**Recommended Action** None required.

### 508001

**Error Message** `%ASA-5-508001: DCERPC _message_type_ non-standard _version_type_ version _version_number_ from _src_if_:_src_ip_/_src_port_ to _dest_if_:_dest_ip_/_dest_port_, terminating connection.`

**Explanation** During DCERPC inspection, a message header included a nonstandard major or minor version.

-   message\_type—The DCERPC message type
-   version\_type—The version type, which can be major or minor
-   version\_number—The nonstandard version in the message header

**Recommended Action** If this is a valid version, and the problem persists, contact the Cisco TAC.

### 508002

**Error Message** `%ASA-5-508002: DCERPC response has low endpoint port _port_number_ from _src_if_:_src_ip_/_src_port_ to _dest_if_:_dest_ip_/_dest_port_, terminating connection.`

**Explanation** During DCERPC inspection, a response message included an endpoint port number less than 1024 (in the range of well-known server ports).

**Recommended Action** None required.

### 509001

**Error Message** `%ASA-5-509001: Connection attempt was prevented by \ command: _src_intf_`

**Explanation** The no forward interface command was entered to block traffic from the source interface to the destination interface given in the message. This command is required on low-end platforms to allow the creation of interfaces beyond the licensed limit.

-   src\_intf—The name of the source interface to which the no forward interface command restriction applies
-   dst\_intf—The name of the destination interface to which the no forward interface command restriction applies
-   _sg\_info_ —The security group name or tag for the specified IP address

**Recommended Action** Upgrade the license to remove the requirement of this command on low-end platforms, then remove the command from the configuration.

### 520001

**Error Message** `%ASA-3-520001: _error_string_`

**Explanation** A malloc failure occurred in ID Manager. The errror string can be either of the following:

-   Malloc failure—id\_reserve
-   Malloc failure—id\_get

**Recommended Action** Contact the Cisco TAC.

### 520002

**Error Message** `%ASA-3-520002: bad new ID table size`

**Explanation** A bad new table request to the ID Manager occurred.

**Recommended Action** Contact the Cisco TAC.

### 520003

**Error Message** `%ASA-3-520003: bad id in _error_string_ (id: 0xid_num)`

**Explanation** An ID Manager error occurred. The error string may be any of the following:

-   id\_create\_new\_table (no more entries allowed)
-   id\_destroy\_table (bad table ID)
-   id\_reserve
-   id\_reserve (bad ID)
-   id\_reserve: ID out of range
-   id\_reserve (unassigned table ID)
-   id\_get (bad table ID)
-   id\_get (unassigned table ID)
-   id\_get (out of IDs!)
-   id\_to\_ptr
-   id\_to\_ptr (bad ID)
-   id\_to\_ptr (bad table ID)
-   id\_get\_next\_id\_ptr (bad table ID)
-   id\_delete
-   id\_delete (bad ID)
-   id\_delete (bad table key)

**Recommended Action** Contact the Cisco TAC.

### 520004

**Error Message** `%ASA-3-520004: _error_string_`

**Explanation** An id\_get was attempted at the interrupt level.

**Recommended Action** Contact the Cisco TAC.

### 520005

**Error Message** `%ASA-3-520005: _error_string_`

**Explanation** An internal error occurred with the ID Manager.

**Recommended Action** Contact the Cisco TAC.

### 520010

**Error Message** `%ASA-3-520010: Bad queue elem – _qelem_ptr_ : flink _flink_ptr_ , blink _blink_ptr_ , flink-blink _flink_blink_ptr_ , blink-flink _blink_flink_ptr_`

**Explanation** An internal software error occurred, which can be any of the following:

-   _qelem\_ptr_ —A pointer to the queue data structure
-   _flink\_ptr_ —A pointer to the forward element of the queue data structure
-   _blink\_ptr_ —A pointer to the backward element of the queue data structure
-   _flink\_blink\_ptr_ —A pointer to the forward element’s backward pointer of the queue data structure
-   _blink\_flink\_ptr_ —A pointer to the backward element’s forward pointer of the queue data structure

**Recommended Action** Contact the Cisco TAC.

### 520011

**Error Message** `%ASA-3-520011: Null queue elem`

**Explanation** An internal software error occurred.

**Recommended Action** Contact the Cisco TAC.

### 520013

**Error Message** `%ASA-3-520013: Regular expression access check with bad list acl_ID`

**Explanation** A pointer to an access list is invalid.

**Recommended Action** The event that caused this message to be issued should not have occurred. It can mean that one or more data structures have been overwritten. If this message recurs, and you decide to report it to your TAC representative, you should copy the text of the message exactly as it appears and include the associated stack trace. Because access list corruption may have occurred, a TAC representative should verify that access lists are functioning correctly.

### 520020

**Error Message** `%ASA-3-520020: No memory available`

**Explanation** The system is out of memory.

**Recommended Action** Try one of the following actions to correct the problem:

-   Reduce the number of routes accepted by this router.
-   Upgrade hardware.
-   Use a smaller subset image on run-from-RAM platforms.

### 520021

**Error Message** `%ASA-3-520021: Error deleting trie entry, _error_message_`

**Explanation** A software programming error occurred. The error message can be any of the following:

-   Inconsistent annotation
-   Couldn't find our annotation
-   Couldn't find deletion target

**Recommended Action** Copy the error message exactly as it appears, and report it to Cisco TAC.

### 520022

**Error Message** `%ASA-3-520022: Error adding mask entry, _error_message_`

**Explanation** A software or hardware error occurred. The error message can be any of the following:

-   Mask already in tree
-   Mask for route not entered
-   Non-unique normal route, mask not entered

**Recommended Action** Copy the error message exactly as it appears, and report it to Cisco TAC.

### 520023

**Error Message** `%ASA-3-520023: Invalid pointer to head of tree, 0x _radix_node_ptr_`

**Explanation** A software programming error occurred.

**Recommended Action** Copy the error message exactly as it appears, and report it to Cisco TAC.

### 520024

**Error Message** `%ASA-3-520024: Orphaned mask #radix_mask_ptr, refcount= radix_mask_ptr’s ref count at #radix_node_address, next= #radix_node_nxt`

**Explanation** A software programming error occurred.

**Recommended Action** Copy the error message exactly as it appears, and report it to Cisco TAC.

### 520025

**Error Message** `%ASA-3-520025: No memory for radix initialization: err_msg`

**Explanation** The system ran out of memory during initialization. This should only occur if an image is too large for the existing dynamic memory. The error message can be either of the following:Initializing leaf nodesMask housekeeping

**Recommended Action** Use a smaller subset image or upgrade hardware.