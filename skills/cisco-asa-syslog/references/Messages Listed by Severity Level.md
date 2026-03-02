This appendix contains the following sections:

| ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)

**Note** | ___

The ASA does not send severity 0, emergency messages to the syslog server. These are analogous to a UNIX panic message, and denote an unstable system.

___ |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------|

## Alert Messages, Severity 1

The following messages appear at severity 1, alerts:

| ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)

**Note** | ___

The security event syslog messages (430001, 430002, 430003, 430004, 430005, and 430006) appear with varied severity levels depending on the nature of the event. For information on the messages and fields, see Security Event Syslog Message ID in the Cisco Secure Firewall Threat Defense Syslog Messages Guide .

___ |
|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

-   %ASA-1-101001: (Primary) Failover cable OK.
    
-   %ASA-1-101002: (Primary) Bad failover cable.
    
-   %ASA-1-101003: (Primary) Failover cable not connected (this unit)
    
-   %ASA-1-101004: (Primary) Failover cable not connected (other unit).
    
-   %ASA-1-101005: (Primary) Error reading failover cable status.
    
-   %ASA-1-103001: (Primary) No response from other firewall (reason code = _code_).
    
-   %ASA-1-103002: (Primary) Other firewall network interface _interface\_number_ OK.
    
-   %ASA-1-103003: (Primary) Other firewall network interface _interface\_number_ failed.
    
-   %ASA-1-103004: (Primary) Other firewall reports this firewall failed. _reason-string_
    
-   %ASA-1-103005: (Primary) Other firewall reporting failure. Reason: _SSM card failure_
    
-   %ASA-1-103006: (Primary|Secondary) Mate version _ver\_num_ is not compatible with ours _ver\_num_.
    
-   %ASA-1-103007: (Primary|Secondary) Mate version _ver\_num_ is not identical with ours _ver\_num_.
    
-   %ASA-1-103008: _host_ Mate hwdib index _Idx_ is not identical with ours.
    
-   %ASA-1-104001: (Primary) Switching to ACTIVE - _string_.
    
-   %ASA-1-104002: (Primary) Switching to STANDBY (cause: string).
    
-   %ASA-1-104003: (Primary) Switching to FAILED.
    
-   %ASA-1-104004: (Primary) Switching to OK.
    
-   %ASA-1-104501: (Primary|Secondary) Switching to BACKUP - switch reason: _reason_
    
-   %ASA-1-104501: (Primary|Secondary) Switching to BACKUP - switch reason: _reason_
    
-   %ASA-1-104502: (Primary|Secondary) Becoming Backup unit failed
    
-   %ASA-1-105001: (Primary) Disabling failover.
    
-   %ASA-1-105002: (Primary) Enabling failover.
    
-   %ASA-1-105003: (Primary) Monitoring on interface _interface\_name_ waiting
    
-   %ASA-1-105004: (Primary) Monitoring on interface _interface\_name_ normal
    
-   %ASA-1-105005: (Primary) Lost Failover communications with mate on interface _interface\_name_
    
-   %ASA-1-105006: (Primary) Link status 'Up' on interface _interface\_name_
    
-   %ASA-1-105007: (Primary) Link status Down on interface interface\_name.
    
-   %ASA-1-105008: (Primary) Testing Interface _interface\_name_
    
-   %ASA-1-105009: (Primary) Testing on interface _interface\_name_ _{Passed|Failed}_
    
-   %ASA-1-105011: (Primary) Failover cable communication failure
    
-   %ASA-1-105020: (Primary) Incomplete/slow config replication
    
-   %ASA-1-105021: (_failover\_unit_) Standby unit failed to sync due to a locked _context\_name_ config. Lock held by _lock\_owner\_name_
    
-   %ASA-1-105022: (_host_) Config replication failed with reason = _reason_
    
-   %ASA-1-105031: Failover LAN interface is up.
    
-   %ASA-1-105032: LAN Failover interface is down.
    
-   %ASA-1-105033: LAN FO cmd Iface down and up again.
    
-   %ASA-1-105034: Receive a LAN\_FAILOVER\_UP message from peer.
    
-   %ASA-1-105035: Receive a LAN failover interface down msg from peer.
    
-   %ASA-1-105036: dropped a LAN Failover command message.
    
-   %ASA-1-105037: (_Primary and Standby_ ) Both units are switching back and forth as the active unit
    
-   %ASA-1-105038: (Primary) Interface count mismatch
    
-   %ASA-1-105039: (Primary) Unable to verify the Interface count with mate. Failover may be disabled in mate.
    
-   %ASA-1-105040: (Primary) Mate failover version is not compatible.
    
-   %ASA-1-105041: cmd failed during sync.
    
-   %ASA-1-105042: (Primary) Failover interface OK
    
-   %ASA-1-105043: (Primary) Failover interface failed
    
-   %ASA-1-105044: (Primary) Mate operational mode (_mode_) is not compatible with my mode (_mode_).
    
-   %ASA-1-105045: (Primary) Mate license (_number contexts_) is not compatible with my license (_number contexts_).
    
-   %ASA-1-105046: (Primary|Secondary) Mate has a different chassis
    
-   %ASA-1-105047: _(host)_ Mate has a _card\_name1_ card in slot _slot\_number_ which is different with my _card\_name2_.
    
-   %ASA-1-105048: (_unit_) Mate's service module (_application_) is different from mine (_application_).
    
-   %ASA-1-105502: (Primary|Secondary) Restarting Cloud HA on this unit, reason: _string_
    
-   %ASA-1-106021: Deny _protocol_ reverse path check from _source\_address_ to _dest\_address_ on interface _interface\_name_
    
-   %ASA-1-106022: Deny _protocol_ connection spoof from _source\_address_ to _dest\_address_ on interface _interface\_name_
    
-   %ASA-1-106101: Number of cached deny-flows for ACL log has reached limit (_number_)
    
-   %ASA-1-107001: RIP auth failed from _IP\_address_: version=_number_, type=_string_, mode=_string_, sequence=_number_ on interface _interface\_name_
    
-   %ASA-1-107002: RIP pkt failed from _IP\_address_: version=_number_ on interface _interface\_name_
    
-   %ASA-1-111111 error\_message.
    
-   %ASA-1-114001: Failed to initialize _card-type_ I/O card due to _error\_string_.
    
-   %ASA-1-114002: Failed to initialize SFP in _card-type_ I/O card due to _error\_string_.
    
-   %ASA-1-114003: Failed to run cached commands in _card-type_ I/O card due to _error\_string_.
    
-   %ASA-1-1199012: Stack smash during new\_stack\_call in process/fiber process/fiber, call target f, stack size s, process/fiber name of the process/fiber that caused the stack smash.
    
-   %ASA-1-199010: Signal _number_ caught in process/fiber (_rtcli\_async\_executor\_process_)/(_rtcli\_async\_executor_) at address _ip\_address_, corrective action at _ip\_address_
    
-   %ASA-1-199012: Stack overflow during new\_stack\_call in process/fiber _process\_name_/_fiber\_name_, call target _f_, stack size _s_
    
-   %ASA-1-199013: syslog.
    
-   %ASA-1-199021: System memory utilization has reached the configured threshold of _Y_%%. System will now reload.
    
-   %ASA-1-211004: WARNING: Minimum Memory Requirement for _device_ version _ver_ not met. _min_ MB required, _actual_ MB found.
    
-   %ASA-n-216001: internal error in: function: message
    
-   %ASA-1-216005: ERROR: Duplex-mismatch on _interface\_name_ resulted in transmitter lockup. A soft reset of the switch was performed.
    
-   %ASA-1-323006: Module _ips_ experienced a data channel communication failure, data channel is DOWN.
    
-   %ASA-1-332004: Web Cache _IP\_address_/_service\_ID_ lost
    
-   %ASA-1-413007: An unsupported configuration is detected. The combination of an _mpc\_description_ with _ips\_description_ is not supported.
    
-   %ASA-1-413008: An unsupported configuration is detected.
    
-   %ASA-1-505011: Module _ips_ data channel communication is UP.
    
-   %ASA-1-505014: Module _module\_id_, application down "_name_", version "_version_" _reason_
    
-   %ASA-1-505015: Module _module\_id_, application up "_application_", version "_ver\_num_" _version_
    
-   %ASA-1-709003: (Primary) Beginning configuration replication: Send to mate.
    
-   %ASA-1-709004: (Primary) End Configuration Replication (ACT)
    
-   %ASA-1-709005: (Primary) Beginning configuration replication: Receiving from mate.
    
-   %ASA-1-709006: (Primary) End Configuration Replication (STB)
    
-   %ASA-1-713900: Descriptive\_event\_string.
    
-   %ASA-1-716507: Fiber scheduler has reached unreachable code. Cannot continue, terminating.
    
-   %ASA-1-716508: internal error in: function: Fiber scheduler is scheduling rotten fiber. Cannot continuing terminating.
    
-   %ASA-1-716509: internal error in: function: Fiber scheduler is scheduling alien fiber. Cannot continue terminating.
    
-   %ASA-1-716510: internal error in: function: Fiber scheduler is scheduling finished fiber. Cannot continue terminating.
    
-   %ASA-1-716516: internal error in: function: OCCAM has corrupted ROL array. Cannot continue terminating.
    
-   %ASA-1-716519: internal error in: function: OCCAM has corrupted pool list. Cannot continue terminating.
    
-   %ASA-1-716528: Unexpected fiber scheduler error; possible out-of-memory condition.
    
-   %ASA-1-717049: Local CA Server certificate is due to expire in _number_ days and a replacement certificate is available for export.
    
-   %ASA-1-717054: The _type_ certificate in the trustpoint _tp name_ is due to expire in _number_ days. Expiration _date and time_ Subject Name _subject name_ Issuer Name _issuer name_ Serial Number _serial number_
    
-   %ASA-1-717055: The _type_ certificate in the trustpoint _tp name_ has expired. Expiration _date and time_ Subject Name _subject name_ Issuer Name _issuer name_ Serial Number _serial number_
    
-   %ASA-1-735001 Cooling Fan var1: OK.
    
-   %ASA-1-735002 Cooling Fan var1: Failure Detected.
    
-   %ASA-1-735003 Power Supply var1: OK.
    
-   %ASA-1-735004 Power Supply var1: Failure Detected.
    
-   %ASA-1-735005 Power Supply Unit Redundancy OK.
    
-   %ASA-1-735006 Power Supply Unit Redundancy Lost.
    
-   %ASA-1-735007 CPU var1: Temp: var2 var3, Critical.
    
-   %ASA-1-735008 IPMI: Chassis Ambient var1: Temp: var2 var3, Critical.
    
-   %ASA-1-735011: Power Supply _var1_: Fan OK
    
-   %ASA-1-735012: Power Supply _var1_: Fan Failure Detected
    
-   %ASA-1-735013: Voltage Channel _var1_: Voltage OK
    
-   %ASA-1-735014: Voltage Channel _var1_: Voltage Critical
    
-   %ASA-1-735017: Power Supply _var1_: Temp: _var2_ _var3_, OK
    
-   %ASA-1-735020: CPU _var1_: Temp: _var2_ _var3_, OK
    
-   %ASA-1-735021: Chassis Ambient _var1_: Temp: _var2_ _var3_, OK
    
-   %ASA-1-735022: CPU_num_ is running beyond the max thermal operating temperature and the device will be shutting down immediately to prevent permanent damage to the CPU
    
-   %ASA-1-735024: CPU_var1_ Voltage Regulator is running beyond the max thermal operating temperature and the device will be shutting down immediately. The chassis and CPU need to be inspected immediately for ventilation issues
    
-   %ASA-1-735025: _var1_ was previously shutdown due to a CPU Voltage Regulator running beyond the max thermal operating temperature. The chassis and CPU need to be inspected immediately for ventilation issues
    
-   %ASA-1-735027: CPU cpu\_num Voltage Regulator is running beyond the max thermal operating temperature and the device will be shutting down immediately. The chassis and CPU need to be inspected immediately for ventilation issues.
    
-   %ASA-1-735029: IO Hub is running beyond the max thermal operating temperature and the device will be shutting down immediately to prevent permanent damage to the circuit
    
-   %ASA-1-743000: The PCI device with vendor ID: _vendor\_id_ device ID: _device\_id_ located at bus:device.function (hex) _bus\_num_:_dev\_num_._func\_num_ has a link _link\_attr\_name_ of _actual\_link\_attr\_val_ when it should have a link _link\_attr\_name_ of _expected\_link\_attr\_val_
    
-   %ASA-1-743001: Backplane health monitoring detected link failure
    
-   %ASA-1-743002: Backplane health monitoring detected link OK
    
-   %ASA-1-743004: System is not fully operational - The PCI device with vendor ID: _vendor\_id_ (_vendor\_name_) device ID: _device\_id_ (_device\_name_) could not be found in the system.
    
-   %ASA-1-770002: _Resource_ resource allocation is more than the permitted limit of _limit_, _Device_ will be rebooted
    

## Critical Messages, Severity 2

The following messages appear at severity 2, critical:

-   %ASA-2-105506: (Primary|Secondary) Unable to create socket for port _port_ for _failover connection | load balancer probes_, error: _error\_string_
    
-   %ASA-2-105507: (Primary|Secondary) Unable to bind socket for port _port_ for _failover connection | load balancer probes_, error: _error\_string_
    
-   %ASA-2-105508: (Primary|Secondary) Error creating failover connection socket for port _port_\\n
    
-   %ASA-2-105525: (Primary|Secondary) Incomplete configuration to initiate access token change request
    
-   %ASA-2-105526: (Primary|Secondary) Unexpected status in response to access token request: _status_ (_status\_string_)
    
-   %ASA-2-105527: (Primary|Secondary) Failure reading response to access token request
    
-   %ASA-2-105528: (Primary|Secondary) No access token in response to access token request
    
-   %ASA-2-105529: (Primary|Secondary) Error creating authentication header from access token
    
-   %ASA-2-105530: (Primary|Secondary) No response to access token request from _url_
    
-   %ASA-2-105531: (Primary|Secondary) Failed to obtain route-table information needed for change request for route-table _route\_table\_name_
    
-   %ASA-2-105532: (Primary|Secondary) Unexpected status in response to route-table change request for route-table _route\_table\_name_: _status_ (_status\_string_)
    
-   %ASA-2-105533: (Primary|Secondary) Failure reading response to route-table change request for route-table _route\_table\_name_
    
-   %ASA-2-105534: (Primary|Secondary) No provisioning state in response to route-table change request route-table route\_table\_name
    
-   %ASA-2-105535: (Primary|Secondary) No response to route-table change request for route-table _route\_table\_name_ from _url_
    
-   %ASA-2-105536: (Primary|Secondary) Failed to obtain Azure authentication header for route status request for route _route\_name_
    
-   %ASA-2-105537: (Primary|Secondary) Unexpected status in response to route state request for route _route\_name_: _status_ (_status\_string_)
    
-   %ASA-2-105538: (Primary|Secondary) Failure reading response to route state request for route _route\_name_
    
-   %ASA-2-105539: (Primary|Secondary) No response to route state request for route _route\_name_ from _url_
    
-   %ASA-2-105540: (Primary|Secondary) No route-tables configured
    
-   %ASA-2-105541: (Primary|Secondary) Failed to update route-table _route\_table\_name_, provisioning state: _state\_string_
    
-   %ASA-2-105544: (Primary|Secondary) Error creating load balancer probe socket for port _port_
    
-   %ASA-2-106001: Inbound TCP connection denied from _IP\_address__port__IP\_address__port__tcp\_flags__interface\_name_
    
-   %ASA-2-106002: protocol Connection denied by outbound list acl\_ID src inside\_address dest outside\_address
    
-   %ASA-2-106006: Deny inbound UDP from _outside\_address__outside\_port__inside\_address__inside\_port__interface\_name_
    
-   %ASA-2-106007: Deny inbound UDP from _outside\_address__outside\_port__inside\_address__inside\_port__{Response|Query}_
    
-   %ASA-2-106013: Dropping echo request from _IP\_address__IP\_address_
    
-   %ASA-2-106016: Deny IP spoof from (_ip\_address_) to _ip\_address_ on interface _interface\_name_
    
-   %ASA-2-106017: Deny IP due to Land Attack from _IP\_address__IP\_address_
    
-   %ASA-2-106018: ICMP packet type _ICMP\_type__acl\_ID__inside\_address__outside\_address_
    
-   %ASA-2-106020: Deny IP teardrop fragment (size = _number__number__IP\_address__IP\_address_
    
-   %ASA-2-106024: Access rules memory exhausted. Aborting current compilation and continuing to use the existing access rules
    
-   %ASA-2-108002: SMTP replaced _string__source\_address__inside\_address__string_
    
-   %ASA-2-108003: Terminating ESMTP connection; malicious pattern detected in the mail address from _source\_interface__source\_address__source\_port__dest\_interface__dest\_address__dset\_port__string_
    
-   %ASA-2-109011: Authen Session Start: user '_user__number_
    
-   %ASA-2-112001: Clear finished
    
-   %ASA-2-113022: AAA Marking _protocol_ server {_IP\_address | hostname_} in aaa-server group _tag_ as FAILED
    
-   %ASA-2-113023: AAA Marking _protocol__ip-addr__tag_
    
-   %ASA-2-113027: Error activating tunnel-group scripts
    
-   %ASA-2-115000: Critical assertion in process: process name fiber: fiber name, component: component name, subcomponent: subcomponent name, file: filename, line: line number, cond: condition
    
-   %ASA-2-199011: Close on bad channel in process/fiber _process\_name_/_fiber\_name_, channel ID _p_, channel state _channel\_state_
    
-   %ASA-2-199014: syslog
    
-   %ASA-2-199020: System memory utilization has reached X%. System will reload if memory usage reaches the configured trigger level of Y%.
    
-   %ASA-2-201003: Embryonic limit exceeded _nconns__elimit__outside\_address__outside\_port__inside\_address__global\_address__inside\_port__interface\_name_
    
-   %ASA-2-214001: Terminating manager session from _IP\_address__interface\_name__number__number_
    
-   %ASA-2-215001:Bad route\_compress() call, sdb= number
    
-   %ASA-2-217001: No memory for _string_ in _string_
    
-   %ASA-2-218001: Failed Identification Test in slot# \[fail#/res\].
    
-   %ASA-2-218002: Module _slot#__Cisco_
    
-   %ASA-2-218003: Module Version in _slot#__slot#__Cisco_
    
-   %ASA-2-218004: Failed Identification Test in _slot#__fail#__res_
    
-   %ASA-2-218005: Inconsistency detected in the system information programmed in non-volatile memory.
    
-   %ASA-2-304007: URL Server not responding, ENTERING ALLOW mode
    
-   %ASA-2-304008: LEAVING ALLOW mode, URL Server is up
    
-   %ASA-2-321005: System CPU utilization reached _utilization %_
    
-   %ASA-2-321006: System Memory usage reached _utilization %_
    
-   %ASA-2-410002: Dropped _num__sec__src\_ifc__sip__sport__dest\_ifc__dip__dport_
    
-   %ASA-2-444004: Timebased activation key _xxx__xxx__xxx__xxx__xxx__permanent license__xxx__xxx__xxx__xxx__xxx_
    
-   %ASA-2-444007: Timebased activation key _xxx__xxx__xxx__xxx__xxx_
    
-   %ASA-2-444009: _license-type_
    
-   %ASA-2-444102: Shared license service inactive. License server is not responding.
    
-   %ASA-2-444105: Released _value__licensetype_
    
-   %ASA-2-444111: Shared license backup service has been terminated due to the primary license server _address__days_
    
-   %ASA-2-444302: %SMART\_LIC-2-PLATFORM\_ERROR: Platform error.
    
-   %ASA-2-709007: Configuration replication failed for command _command\_name_
    
-   %ASA-2-713078: Group = _groupname_, Username = _username_, IP = _peerIP_ Temp buffer for building mode config attributes exceeded: bufsize _available\_size_, used _value_
    
-   %ASA-2-713176: _Device\_type_ memory resources are critical, IKE key acquire message on interface _interface\_number_, for Peer _IP\_address_ ignored
    
-   %ASA-2-713901: Descriptive\_text\_string.
    
-   %ASA-2-716500: internal error in: function: Fiber library cannot locate AK47 instance
    
-   %ASA-2-716501: internal error in: function: Fiber library cannot attach AK47 instance
    
-   %ASA-2-716502: internal error in: function: Fiber library cannot allocate default arena
    
-   %ASA-2-716503: internal error in: function: Fiber library cannot allocate fiber descriptors pool
    
-   %ASA-2-716504: internal error in: function: Fiber library cannot allocate fiber stacks pool
    
-   %ASA-2-716505: internal error in: function: Fiber has joined fiber in unfinished state
    
-   %ASA-2-716506: UNICORN\_SYSLOGID\_JOINED\_UNEXPECTED\_FIBER
    
-   %ASA-2-716512: internal error in: function: Fiber has joined fiber waited upon by someone else
    
-   %ASA-2-716513: internal error in: function: Fiber in callback blocked on other channel
    
-   %ASA-2-716515: internal error in: function: OCCAM failed to allocate memory for AK47 instance
    
-   %ASA-2-716517: internal error in: function: OCCAM cached block has no associated arena
    
-   %ASA-2-716518: internal error in: function: OCCAM pool has no associated arena
    
-   %ASA-2-716520: internal error in: function: OCCAM pool has no block list
    
-   %ASA-2-716521: internal error in: function: OCCAM no realloc allowed in named pool
    
-   %ASA-2-716522: internal error in: function: OCCAM corrupted standalone block
    
-   %ASA-2-716525: UNICORN\_SYSLOGID\_SAL\_CLOSE\_PRIVDATA\_CHANGED
    
-   %ASA-2-716526: UNICORN\_SYSLOGID\_PERM\_STORAGE\_SERVER\_LOAD\_FAIL
    
-   %ASA-2-716527: UNICORN\_SYSLOGID\_PERM\_STORAGE\_SERVER\_STORE\_FAI
    
-   %ASA-2-717008: Insufficient memory to process\_requiring\_memory.
    
-   %ASA-2-717011: Unexpected event: _event__event\_ID_
    
-   %ASA-2-717040: Local CA Server has failed and is being disabled. Reason: _reason._
    
-   %ASA-2-735009: Environment Monitoring has failed initialization and configuration. Environment Monitoring is not running.
    
-   %ASA-2-735023: _device_
    
-   %ASA-2-735028: ASA was previously shutdown due to a CPU Voltage Regulator running beyond the max thermal operating temperature. The chassis and CPU need to be inspected immediately for ventilation issues.
    
-   %ASA-2-736001: Unable to allocate enough memory at boot for jumbo-frame reservation. Jumbo-frame support has been disabled.
    
-   %ASA-2-747009: Clustering: Fatal error due to failure to create RPC server for module module name.
    
-   %ASA-2-747011: Clustering: Memory allocation error.%ASA-2-752001: Tunnel Manager received invalid parameter to remove record.
    
-   %ASA-2-748007: Failed to de-bundle the ports for module slot\_number in chassis chassis\_number; traffic may be black holed
    
-   %ASA-2-752001: Tunnel Manager received invalid parameter to remove record
    
-   %ASA-2-752005: Tunnel Manager failed to dispatch a KEY\_ACQUIRE message. Memory may be low. Map Tag = _mapTag_ . Map Sequence Number = _mapSeq._
    
-   %ASA-2-772003: PASSWORD: _session__username__ip_
    
-   %ASA-2-772006: REAUTH: user '_username_
    
-   %ASA-2-774001: POST: unspecified error
    
-   %ASA-2-774002: POST: error '_err__func__eng__alg__mode__dir__len_
    
-   %ASA-2-775007: Scansafe: No reachable servers found
    
-   %ASA-2-815002: Denied packet, hard limit, _hard limit value_, for object-group search exceeded for _UDP_ from _source_:_source IP address_/_port_ to _destination_:_destination IP address_/_port_
    

## Error Messages, Severity 3

The following messages appear at severity 3, errors:

-   %ASA-3-105010: (Primary) Failover message block alloc failed
    
-   %ASA-3-105050: _(host)_ Number of Ethernet interfaces on Standby unit _(int\_number)_ is less than number on Active unit _(int\_number)_.
    
-   %ASA-3-105052: HA cipher in use _algorithm name_ strong encryption is AVAILABLE, please reboot to use strong cipher and preferably change the key in use.
    
-   %ASA-3-105509: (Primary|Secondary) Error sending _message\_name_ message to peer unit _peer-ip_, error: _error\_string_
    
-   %ASA-3-105510: (Primary|Secondary) Error receiving message from peer unit _peer-ip_, error: _error\_string_
    
-   %ASA-3-105511: (Primary|Secondary) Incomplete read of message header of message from peer unit _peer-ip_: _bytes_ bytes read of expected _header\_length_ header byte
    
-   %ASA-3-105512: (Primary|Secondary) Error receiving message body of message from peer unit _peer-ip_, error: _error\_string_
    
-   %ASA-3-105513: (Primary|Secondary) Incomplete read of message body of message from peer unit _peer-ip_: _bytes_ bytes read of expected _message\_length_ message body bytes
    
-   %ASA-3-105514: (Primary|Secondary) Error occurred when responding to _message\_name_ message received from peer unit _peer-ip_, error: _error\_string_
    
-   %ASA-3-105515: (Primary|Secondary) Error receiving _message\_name_ message from peer unit _peer-ip_, error: _error\_string_
    
-   %ASA-3-105516: (Primary|Secondary) Incomplete read of message header of _message\_name_ message from peer unit _peer-ip_: _bytes_ bytes read of expected _header\_length_ header bytes
    
-   %ASA-3-105517: (Primary|Secondary) Error receiving message body of _message\_name_ message from peer unit _peer-ip_, error: _error\_string_
    
-   %ASA-3-105518: (Primary|Secondary) Incomplete read of message body of _message\_name_ message from peer unit _peer-ip_: _bytes_ bytes read of expected _message\_length_ message body bytes
    
-   %ASA-3-105519: (Primary|Secondary) Invalid response to _message\_name_ message received from peer unit _peer-ip_: type _message\_type_, version _message\_version_, length _message\_length_
    
-   %ASA-3-105545: (Primary|Secondary) Error starting load balancer probe socket for port _port_, error code: _error\_code_
    
-   %ASA-3-105546: (Primary|Secondary) Error starting load balancer probe handler
    
-   %ASA-3-105547: (Primary|Secondary) Error generating encryption key for Azure secret key
    
-   %ASA-3-105548: (Primary|Secondary) Error storing encryption key for Azure secret key
    
-   %ASA-3-105549: (Primary|Secondary) Error retrieving encryption key for Azure secret key
    
-   %ASA-3-105550: (Primary|Secondary) Error encrypting Azure secret key
    
-   %ASA-3-105551: (Primary|Secondary) Error decrypting Azure secret key
    
-   %ASA-3-106010: Deny inbound _protocol__src_ \[_interface\_name_ : _source\_address/source\_port_ \] \[(\[_idfw\_user_ | _FQDN\_string_ \], _sg\_info_ )\] _dst_ \[_interface\_name_ : _dest\_address_ /_dest\_port_ }\[(\[_idfw\_user_ | _FQDN\_string_ \], _sg\_info_ )\]
    
-   %ASA-3-106011: Deny inbound (No xlate) _protocol src Interface:IP/port dst Interface-nameif:IP/port_
    
-   %ASA-3-106014: Deny inbound _src_
    
-   %ASA-3-109010: Auth from _inside\_address__inside\_port__outside\_address__outside\_port__interface\_name_
    
-   %ASA-3-109013: User must authenticate before using this service
    
-   %ASA-3-109016: Cannot find authorization ACL '_acl\_id_' on '_server\_name_' for user '_user_'
    
-   %ASA-3-109018: Downloaded ACL '_acl\_ID_
    
-   %ASA-3-109019: Downloaded ACL '_acl\_ID__string__string_
    
-   %ASA-3-109020: Downloaded ACL has config error; ACE
    
-   %ASA-3-109023: User from _source\_address__source\_port__dest\_address__dest\_port__outside\_interface__service\_name_
    
-   %ASA-3-109026: \[ _aaa protocol_
    
-   %ASA-3-109032: Unable to install ACL '_access\_list__username__ace_
    
-   %ASA-3-109035: Exceeded maximum number (999) of DAP attribute instances for user = _user_
    
-   %ASA-3-109037: Exceeded _5000__attribute name__username_
    
-   %ASA-3-109038: Attribute _internal-attribute-name__string-from-server__type_
    
-   %ASA-3-109103: CoA _action-type__coa-source-ip__username__audit-session-id_
    
-   %ASA-3-109104: CoA (Action type: _action-type__coa-source-ip__username__audit-session-id_
    
-   %ASA-3-109105: Failed to determine the egress interface for locally generated traffic destined to _protocol_ _IP_:_port_.
    
-   %ASA-3-109203: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP Address_, Failed adding entry.
    
-   %ASA-3-109205: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP Address_, Failed applying filter.
    
-   %ASA-3-109206: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP Address_, Removing stale entry added _hours_ ago.
    
-   %ASA-3-109208: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP Address_, Failed updating entry - no entry.
    
-   %ASA-3-109209: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP Address_, Failed updating filter for entry. Entry was allocated to Session=_session_, User=_username_ _hours_ ago.
    
-   %ASA-3-109212: UAUTH: Session=_session_, User=_user\_name_, Assigned IP=_ip\_address_, Failed removing entry - _reason\_string_.
    
-   %ASA-3-109213: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP Address_, Failed removing entry. Address was allocated to Session=_session_, User=_username_ _hours_ ago.
    
-   %ASA-3-113001: Unable to open AAA session. Session limit \[_limit_
    
-   %ASA-3-113018: User: '_user__ACL\_entry__action_
    
-   %ASA-3-113020: Kerberos error : Clock skew with server _ip\_address__time in seconds_
    
-   %ASA-3-113021: Attempted console login failed user '_username_
    
-   %ASA-3-114006: Failed to get port statistics in _card-type__error\_string_
    
-   %ASA-3-114007: Failed to get current msr in _card-type__error\_string_
    
-   %ASA-3-114008: Failed to enable port after link is up in _card-type__error\_string_
    
-   %ASA-3-114009: Failed to set multicast address in _card-type__error\_string_
    
-   %ASA-3-114010: Failed to set multicast hardware address in _card-type__error\_string_
    
-   %ASA-3-114011: Failed to delete multicast address in _card-type__error\_string_
    
-   %ASA-3-114012: Failed to delete multicast hardware address in _card-type__error\_string_
    
-   %ASA-3-114013: Failed to set mac address table in _card-type__error\_string_
    
-   %ASA-3-114014: Failed to set mac address in _card-type__error\_string_
    
-   %ASA-3-114015: Failed to set mode in _card-type__error\_string_
    
-   %ASA-3-114016: Failed to set multicast mode in _card-type__error\_string_
    
-   %ASA-3-114017: Failed to get link status in _card-type__error\_string_
    
-   %ASA-3-114018: Failed to set port speed in _card-type__error\_string_
    
-   %ASA-3-114019: Failed to set media type in _card-type__error\_string_
    
-   %ASA-3-114020: Port link speed is unknown in _4GE SSM_
    
-   %ASA-3-114021: Failed to set multicast address table in _4GE SSM__error_
    
-   %ASA-3-114022: Failed to pass broadcast traffic in 4GE SSM I/O card due to error\_string
    
-   %ASA-3-114023: Failed to cache/flush mac table in _4GE SSM__error\_string_
    
-   %ASA-3-115001: Error in process: process name fiber: fiber name, component: component name, subcomponent: subcomponent name, file: filename, line: line number, cond: condition.
    
-   %ASA-3-120010: Call-Home _command__client__reason_
    
-   %ASA-3-199015: syslog
    
-   %ASA-3-201002: Too many TCP connections on {static|xlate} global\_address! econns nconns
    
-   %ASA-3-201004: Too many udp connections on _{static|xlate}__global\_address__udp connections limit_
    
-   %ASA-3-201005: FTP data connection failed for _IP\_address_
    
-   %ASA-3-201006: RCMD backconnection failed for _IP\_address__port_
    
-   %ASA-3-201008: Disallowing new connections.
    
-   %ASA-3-201009: _TCP__number__IP\_address__interface\_name_
    
-   %ASA-3-201011: Connection limit exceeded _cnt__limit__dir__sip__sport__dip__dport__if\_name_
    
-   %ASA-3-201013: Per-client connection limit exceeded _curr\_num_/_limit_ for _\[input|output\]_ packet from _ip\_address_/_port_ to _ip\_address_/_port_ on interface _interface\_name_
    
-   %ASA-3-202001: Out of address translation slots!
    
-   %ASA-3-202005: Non-embryonic in embryonic list _outside\_address__outside\_port__inside\_address__inside\_port_
    
-   %ASA-3-202010: {NAT | PAT} pool exhausted in pool'_pool\_name_' IP _ip\_address__port\_range \[1-511 | 512-1023 | 1024-65535\]_ Unable to create _protocol_ connection from _inside\_interface_:_src\_ip_/_src\_port_ to _outside\_interface_:_dest\_ip_/_dest\_port_.
    
-   %ASA-3-202010: NAT/PAT pool exhausted in pool '_pool\_name_' IP _ip\_address_. Unable to create connection.
    
-   %ASA-3-202016: Unable to pre-allocate SIP _ip\_protocol_ secondary channel for message from _src\_ifname_:_src\_ip\_addr_/_src\_port_ to _dst\_ifname_:_dest\_ip\_addr_/_dest\_port_ with PAT and missing port information.
    
-   %ASA-3-208005: Clear (_command__code_
    
-   %ASA-3-210001: LU _sw\_module\_name__number_
    
-   %ASA-3-210002: LU allocate block (_bytes_
    
-   %ASA-3-210003: Unknown LU Object _number_
    
-   %ASA-3-210005: LU allocate secondary(optional) connection failed for protocol\[TCP|UDP\] connection from ingress interface name:Real IP Address/Real Port to egress interface name:Real IP Address/Real Port
    
-   %ASA-3-210006: LU look NAT for _IP\_address_
    
-   %ASA-3-210007: LU allocate xlate failed for _type__static__dynamic__NAT__PAT__secondary(optional)__protocol__ingress interface name__Real IP Address__real port__Mapped IP Address__Mapped Port__egress interface name__Real IP Address_
    
-   %ASA-3-210008: LU no xlate for _inside\_address__inside\_port__outside\_address__outside\_port_
    
-   %ASA-3-210010: LU make UDP connection for _outside\_address__outside\_port__inside\_address__inside\_port_
    
-   %ASA-3-210020: LU PAT port _port_
    
-   %ASA-3-210021: LU create static xlate _global\_address__interface\_name_
    
-   %ASA-3-211001: Memory allocation Error
    
-   %ASA-3-211003: Error in computed percentage CPU usage value
    
-   %ASA-3-212001: Unable to open SNMP channel (UDP port _port__interface\_number__code_
    
-   %ASA-3-212002: Unable to open SNMP trap channel (UDP port _port__interface\_number__code_
    
-   %ASA-3-212003: Unable to receive an SNMP request on interface "_interface\_number__code_
    
-   %ASA-3-212004: Unable to send an SNMP response to _IP\_address__port_
    
-   %ASA-3-212005: incoming SNMP request (_number__interface\_name_
    
-   %ASA-3-212006: Dropping SNMP request from _src\_addr__src\_port__ifc__dst\_addr__dst\_port__reason__username_
    
-   %ASA-3-212010: Configuration request for SNMP user _s__s__reason_
    
-   %ASA-3-212011: engineBoots is set to maximum value. Reason: _Reason_
    
-   %ASA-3-212012: Unable to write engine data to persistent storage.
    
-   %ASA-3-213001: PPTP control daemon socket io _string__number_
    
-   %ASA-3-213002: PPTP tunnel hashtable insert failed, peer = _IP\_address_
    
-   %ASA-3-213003: PPP virtual interface _interface\_number_
    
-   %ASA-3-213004: PPP virtual interface _interface\_number_
    
-   %ASA-3-213005: Dynamic-Access-Policy action (DAP) action aborted
    
-   %ASA-3-213006: L2TP: Dynamic-Access-Policy failure
    
-   %ASA-3-216002: Unexpected event (major: major\_id, minor: minor\_id) received by task\_string in function at line: line\_num
    
-   %ASA-3-216003: Unrecognized timer timer\_ptr, timer\_id received by task\_string in function at line: line\_num
    
-   %ASA-3-219002: _I2C\_API\_name__slot\_number__device\_number__address__count__reason\_string_
    
-   %ASA-3-302019: H.323 _library\_name__number_
    
-   %ASA-3-302302: _ACL = deny; no sa created_
    
-   %ASA-3-304003: URL Server _IP\_address__url_
    
-   %ASA-3-304006: URL Server _IP\_address_
    
-   %ASA-3-305005: No translation group found for protocol src interface\_name: source\_address/source\_port \[(idfw\_user)\] dst interface\_nam: dest\_address/dest\_port \[(idfw\_user)\]
    
-   %ASA-3-305006: {outbound static|identity|portmap|regular) translation creation failed for protocol src interface\_name:source\_address/source\_port \[(idfw\_user)\] dst interface\_name:dest\_address/dest\_port \[(idfw\_user)\]
    
-   %ASA-3-305008: Detecting free unallocated global IP _IP\_ address__interface\_name_
    
-   %ASA-3-305016: Unable to create _protocol_ connection from _source\_interface\_name_:_source\_ip\_address_/_source\_port_ to _destination\_interface\_name_:_destination\_ip_/_destination\_port_ due to reaching per-host PAT port block limit of _threshold-limit_.
    
-   %ASA-3-305016: Unable to create _protocol_ connection from _source\_interface\_name_:_source\_ip\_address_/_source\_port_ to _destination\_interface\_name_:_destination\_ip\_address_/_destination\_port_ due to port block exhaustion in PAT pool '_pool\_name_' IP _pool\_ip\_address_.
    
-   %ASA-3-305016: Port blocks exhausted in PAT pool '_pool\_name_' IP _pool\_address_. Unable to create connection.
    
-   %ASA-3-305017: Pba-interim-logging: Active _Active ICMP__source__device IP__destination__device IP__Active Port__Block_
    
-   %ASA-3-305019: MAP node address _ip_/_port_ has inconsistent Port Set ID encoding
    
-   %ASA-3-305020: MAP node with address _ip_ is not allowed to use port _port_
    
-   %ASA-3-305023: Unable to create connection from inside:_<ip/port>_ to outside:_<ip/port>_ due to IP port block exhaustion in PAT pool _pool\_name_ IP _port\_address_.
    
-   %ASA-3-313001: Denied ICMP type=_number__code__IP\_address__interface\_name_
    
-   %ASA-3-313008: Denied IPv6-ICMP type=_number__code__IP\_address__interface\_name_
    
-   %ASA-3-315004: Fail to establish SSH session because RSA host key retrieval failed.
    
-   %ASA-3-315012: Weak SSH _type__alg__IP\_address__Int_
    
-   %ASA-3-316001: Denied new tunnel to IP\_address. VPN peer limit (platform\_vpn\_peer\_limit) exceeded
    
-   %ASA-3-316002: VPN Handle error: protocol=_protocol__in\_if\_num__src\_addr__out\_if\_num__dst\_addr_
    
-   %ASA-3-317001: No memory available for _limit\_slow_
    
-   %ASA-3-317002: Bad path pointer of _number_ for _IP\_address_, _number_ max
    
-   %ASA-3-317003: IP routing table creation failure - _reason_
    
-   %ASA-3-317004: IP routing table limit warning - _limit\_context_
    
-   %ASA-3-317005: IP routing table limit exceeded - _reason_
    
-   %ASA-3-317006: Pdb index error %08x, %04x, _pdb_
    
-   %ASA-3-317012: Interface IP route counter negative -  _nameif-string-value_ 
    
-   %ASA-3-318001: Internal error: _reason_
    
-   %ASA-3-318002: Flagged as being an ABR without a backbone area
    
-   %ASA-3-318003: Reached unknown state in neighbor state machine
    
-   %ASA-3-318004: DB already exist : area _string_ lsid _IP\_address_ adv _netmask_ type 0x_number_
    
-   %ASA-3-318005: No corresponding LSA in retransmission database for _ip\_address_
    
-   %ASA-3-318006: if _interface\_name_ if\_state _number_
    
-   %ASA-3-318008: Reconfigure virtual link
    
-   %ASA-3-318101: Internal error: _REASON_
    
-   %ASA-3-318102: Flagged as being an ABR without a backbone area
    
-   %ASA-3-318103: Reached unknown state in neighbor state machine
    
-   %ASA-3-318104: DB already exist : area _AREA\_ID\_STR_ lsid _i_ adv _i_ type 0x_x_
    
-   %ASA-3-318105: No corresponding LSA in retransmission database for _i_
    
-   %ASA-3-318106: if _IF\_NAME_ if\_state _d_
    
-   %ASA-3-318108: OSPF process _d_ is changing router-id. Reconfigure virtual link neighbors with our new router-id
    
-   %ASA-3-318109: Received packet with wrong state _x_
    
-   %ASA-3-318110: Invalid encrypted key _key\_string_.
    
-   %ASA-3-318111: IPSEC policy for area _u_ already exists
    
-   %ASA-3-318112: IPSEC SPI _u_ already in use for area _d_
    
-   %ASA-3-318113: IPSEC SPI _s s_ reused for different policy on area _u_
    
-   %ASA-3-318114: IPSEC invalid key length _spi\_value_
    
-   %ASA-3-318115: IPSEC create policy error _s_ for area _u_
    
-   %ASA-3-318116: IPSEC policy does not exist for area _u_
    
-   %ASA-3-318117: IPSEC policy still in use for area _u_
    
-   %ASA-3-318118: IPSEC remove policy error _s_ for area _u_
    
-   %ASA-3-318119: IPSEC close session error _u_ for area _s_
    
-   %ASA-3-318120: OSPFv3 was unable to register with Ipsec
    
-   %ASA-3-318121: IPSEC general error _s_ for area _d_
    
-   %ASA-3-318122: IPSEC error message retry for area _s_
    
-   %ASA-3-318123: IPSEC error message abort for area _s_
    
-   %ASA-3-318125: Interface _IF\_NAME_ initialization failed
    
-   %ASA-3-318126: Interface _IF\_NAME_ attached to multiple areas
    
-   %ASA-3-318127: Could not allocate or find the neighbor
    
-   %ASA-3-319001: Acknowledge for arp update for IP address _dest\_address__number_
    
-   %ASA-3-319002: Acknowledge for route update for IP address _dest\_address__number_
    
-   %ASA-3-319003: Arp update for IP address _address__n_
    
-   %ASA-3-319004: Route update for IP address _dest\_address__number_
    
-   %ASA-3-320001: The subject name of the peer cert is not allowed for connection
    
-   %ASA-3-321007: System is low on free memory blocks of size _block\_size__free\_blocks__max\_blocks_
    
-   %ASA-3-322001: Deny MAC address _MAC\_address__interface_
    
-   %ASA-3-322002: ARP inspection check failed for arp _{request|response}__MAC\_address__interface__MAC\_address\_1__IP\_address__{statically|dynamically}__MAC\_address\_2_
    
-   %ASA-3-322003: ARP inspection check failed for arp _{request|response}__MAC\_address__interface__MAC\_address\_1__IP\_address_
    
-   %ASA-3-323001: Module _module\_id_
    
-   %ASA-3-323002: Module _module\_id_
    
-   %ASA-3-323003: Module _module\_id_
    
-   %ASA-3-323004: Module in slot _string one__newver__ver__reason_
    
-   %ASA-3-323005: Module _syslog\_string_ can not be started completely.
    
-   %ASA-3-323005: Module _syslog\_string_ powerfail recovery is in progress.
    
-   %ASA-3-323007: Module in slot _slot_
    
-   %ASA-3-324000: Drop GTP message _msg\_type__source\_interface__source\_address__source\_port__dest\_interface__dest\_address__dest\_port__reason_
    
-   %ASA-3-324001: GTPv0 packet parsing error from source\_interface:source\_address/source\_port to dest\_interface:dest\_address/dest\_port, TID: tid\_value, Reason: reason
    
-   %ASA-3-324002: No PDP\[MCB\] exists to process GTPv0 msg\_type from source\_interface:source\_address/source\_port to dest\_interface:dest\_address/dest\_port, TID: tid\_value
    
-   %ASA-3-324003: _msg\_type__source\_interface__source\_address__source\_port__dest\_interface__dest\_address__dest\_port_
    
-   %ASA-3-324004: GTP packet with version _Ver\_number__source\_interface__source\_address__source\_port__dest\_interface__dest\_address__dest\_port_
    
-   %ASA-3-324005: Unable to create tunnel from _source\_interface__source\_address__source\_port__dest\_interface__dest\_address__dest\_port_
    
-   %ASA-3-324006: GSN _IP\_address__tunnel\_limit__tid_
    
-   %ASA-3-324007: Unable to create GTP connection for response from _source\_address__0__dest\_address_
    
-   %ASA-3-324008: No PDP exists to update the data _sgsn \[ggsn\]__teid\_value__teid\_value__IPaddress__VPIfNum__IPaddress__VPIfNum_
    
-   %ASA-3-324009: Drop GTP message G-PDU from inside\_interface :inside\_ip /inside\_port to outside\_interface :outside\_ip /outside\_port _<Reason>_
    
-   %ASA-3-324300: Radius Accounting Request from _from\_addr_
    
-   %ASA-3-324301: Radius Accounting Request has a bad header length _hdr\_len__pkt\_len_
    
-   %ASA-3-325001: Router _ipv6\_address__interface_
    
-   %ASA-3-326001: Unexpected error in the timer library: error\_message
    
-   %ASA-3-326002: Error in error\_message: error\_message
    
-   %ASA-3-326004: An internal error occurred while processing a packet queue
    
-   %ASA-3-326005: Mrib notification failed for (IP\_address, IP\_address)
    
-   %ASA-3-326006: Entry-creation failed for (IP\_address, IP\_address)
    
-   %ASA-3-326007: Entry-update failed for (IP\_address, IP\_address)
    
-   %ASA-3-326008: MRIB registration failed
    
-   %ASA-3-326009: MRIB connection-open failed
    
-   %ASA-3-326010: MRIB unbind failed
    
-   %ASA-3-326011: MRIB table deletion failed
    
-   %ASA-3-326012: Initialization of string functionality failed
    
-   %ASA-3-326013: Internal error: string in string line %d (%s)
    
-   %ASA-3-326014: Initialization failed: error\_message error\_message
    
-   %ASA-3-326015: Communication error: error\_message error\_message
    
-   %ASA-3-326016: Failed to set un-numbered interface for interface\_name (string)
    
-   %ASA-3-326017: Interface Manager error - string in string: string
    
-   %ASA-3-326019: string in string: string
    
-   %ASA-3-326020: List error in string: string
    
-   %ASA-3-326021: Error in string: string
    
-   %ASA-3-326022: Error in string: string
    
-   %ASA-3-326023: string - IP\_address: string
    
-   %ASA-3-326024: An internal error occurred while processing a packet queue.
    
-   %ASA-3-326025: string
    
-   %ASA-3-326026: Server unexpected error: error\_message
    
-   %ASA-3-326027: Corrupted update: error\_message
    
-   %ASA-3-326028: Asynchronous error: error\_message
    
-   %ASA-3-327001: IP SLA Monitor: Cannot create a new process
    
-   %ASA-3-327002: IP SLA Monitor: Failed to initialize, IP SLA Monitor functionality will not work
    
-   %ASA-3-327003: IP SLA Monitor: Generic Timer wheel timer functionality failed to initialize
    
-   %ASA-3-328001: Attempt made to overwrite a set stub function in string.
    
-   %ASA-3-329001: The string0 subblock named string1 was not removed
    
-   %ASA-3-331001: Dynamic DNS Update for '_fqdn\_name__ip\_address_
    
-   %ASA-3-332001: Unable to open cache discovery socket, WCCP V_2_
    
-   %ASA-3-332002: Unable to allocate message buffer, WCCP V_2_
    
-   %ASA-3-336001 Route desination\_network stuck-in-active state in EIGRP-ddb\_name as\_num. Cleaning up
    
-   %ASA-3-336002: Handle not allocated in pool
    
-   %ASA-3-336003: Unable to alloc pkt buffer
    
-   %ASA-3-336004: Negative refcount in pakdesc
    
-   %ASA-3-336005: Flow control error
    
-   %ASA-3-336006: Peers exist on IIDB
    
-   %ASA-3-336007: Anchor Count negative
    
-   %ASA-3-336008: Lingering DRDB deleting IIDB
    
-   %ASA-3-336009 ddb\_name as\_id: Internal Error
    
-   %ASA-3-336018: process\_name as\_number: prefix\_source threshold prefix level (prefix\_threshold) reached
    
-   %ASA-3-338305: Failed to download dynamic filter data file from updater server _url_
    
-   %ASA-3-338306: Failed to authenticate with dynamic filter updater server _url_
    
-   %ASA-3-338307: Failed to decrypt downloaded dynamic filter data file
    
-   %ASA-3-338309: The license on this _device_
    
-   %ASA-3-338310: Failed to update from dynamic filter updater server _url,__reason string_
    
-   %ASA-3-339001: DNSCRYPT certificate update failed for _<num\_tries>_
    
-   %ASA-3-339002: Umbrella device registration failed with error code _<err\_code>_
    
-   %ASA-3-339003: Umbrella device registration was successful.
    
-   %ASA-3-339004: Umbrella device registration failed due to missing token
    
-   %ASA-3-339005: Umbrella device registration failed after _<num\_tries>_
    
-   %ASA-3-339006: Umbrella resolver _current resolver ipv46_ is reachable. Resuming redirect
    
-   %ASA-3-339007: Umbrella resolver _current resolver ipv46_ is unreachable, moving to fail-open. Starting probe to resolver
    
-   %ASA-3-339008: Umbrella resolver _current resolver ipv46_ is unreachable, moving to fail-close
    
-   %ASA-3-339011: Umbrella API token request received no responses.
    
-   %ASA-3-339012: Umbrella API token request failed with error code _error code_.
    
-   %ASA-3-339013: Umbrella API token request failed in response processing.
    
-   %ASA-3-339014: Umbrella API token request failed after _retry\_number_ retries.
    
-   %ASA-3-340001: Vnet-proxy handshake error _error\_string__context\_id__version_
    
-   %ASA-3-341003: Policy Agent failed to start for VNMC _vnmc\_ip\_addr_
    
-   %ASA-3-341004: Storage device not available. Attempt to shutdown module _module\_name_
    
-   %ASA-3-341005: Storage device not available. Shutdown issued for module _module\_name_
    
-   %ASA-3-341006: Storage device not available. Failed to stop recovery of module _module\_name_
    
-   %ASA-3-341007: Storage device not available. Further recovery of module _module\_name_
    
-   %ASA-3-341008: Storage device not found. Auto-boot of module _module\_name_
    
-   %ASA-3-341011: Storage device with serial number _ser\_no__bay\_no_
    
-   %ASA-3-342002: REST API Agent failed, reason: _reason_
    
-   %ASA-3-342003: REST API Agent failure notification received. Agent will be restarted automatically.
    
-   %ASA-3-342004: Failed to automatically restart the REST API Agent after _num_
    
-   %ASA-3-342006: Failed to install REST API image, reason: _reason_
    
-   %ASA-3-342008: Failed to uninstall REST API image, reason: _reason_
    
-   %ASA-3-402140: CRYPTO: _RSA__len_
    
-   %ASA-3-402141: CRYPTO: Key zeroization error: key set '_type__reason_
    
-   %ASA-3-402142: CRYPTO: Bulk data _op__alg__mode_
    
-   %ASA-3-402143: CRYPTO: _alg_ _type__op_
    
-   %ASA-3-402144: CRYPTO: Digital signature error: signature algorithm '_sig__hash_
    
-   %ASA-3-402145: CRYPTO: Hash generation error: algorithm '_hash_
    
-   %ASA-3-402146: CRYPTO: Keyed hash generation error: algorithm '_hash__len_
    
-   %ASA-3-402147: CRYPTO: HMAC generation error: algorithm '_alg_
    
-   %ASA-3-402148: CRYPTO: Random Number Generator error
    
-   %ASA-3-402149: CRYPTO: Weak _encryption type__length_
    
-   %ASA-3-402150: CRYPTO: Deprecated hash algorithm used for RSA _operation__hash alg_
    
-   %ASA-3-403501: PPPoE - Bad host-unique in PADO - packet dropped. AC:_interface\_name_
    
-   %ASA-3-403502: PPPoE - Bad host-unique in PADS - packet dropped. AC:_interface\_name_
    
-   %ASA-3-403503: _Header\_string_:PPP link down\[:_reason string_\]
    
-   %ASA-3-403504: _group\_name_
    
-   %ASA-3-403507: _PPPoE__interface__group\_name_
    
-   %ASA-3-414001: Failed to save logging buffer to FTP server _filename__ftp\_server\_address__interface\_name__fail\_reason_
    
-   %ASA-3-414002: Failed to save logging buffer to _flash:/syslog__filename__fail\_reason_
    
-   %ASA-3-414003: TCP Syslog Server _intf__IP\_Address__port__\[permitted|denied\]_
    
-   %ASA-3-414005: TCP Syslog Server intf: IP\_Address/port connected, New connections are permitted based on logging permit-hostdown policy
    
-   %ASA-3-414006: TCP syslog server configured and logging queue is full. New connections denied based on logging permit-hostdown policy.
    
-   %ASA-3-418018: neighbor _IP\_Address__vrf\_identifie__topology\_identifier__address\_family__state\_change_
    
-   %ASA-3-418019: received from _IP\_Address_ error\_code/_error\_subcode_(_error\_text_) _data\_bytes_bytes _hex\_data_
    
-   %ASA-3-418040: Unsupported or malformed message: _IP\_Address_
    
-   %ASA-3-418044: Connection closed remotely by _IP\_Address_
    
-   %ASA-3-420001: IPS card not up and fail-close mode used, dropping _ICMP__ifc\_in__SIP__port__ifc\_out__DIP__port_
    
-   %ASA-3-420006: Virtual sensor not present and fail-close mode used, dropping _protocol__ifc\_in__SIP__SPORT__ifc\_out__DIP__DPORT_
    
-   %ASA-3-420008: IPS module license disabled and fail-close mode used, dropping packet.
    
-   %ASA-3-421001: TCP|UDP flow from interface\_name:ip/port to interface\_name:ip/port is dropped because application has failed.
    
-   %ASA-3-421003: Invalid data plane encapsulation
    
-   %ASA-3-421007: TCP|UDP flow from interface\_name:IP\_address/port to interface\_name:IP\_address/port is skipped because application has failed.
    
-   %ASA-3-425006 Redundant interface redundant\_interface\_name switch active member to interface\_name failed.
    
-   %ASA-3-429001: CX card not up and fail-close mode used, dropping _protocol__interface\_name__ip\_address__port__interface\_name__ip\_address__port_
    
-   %ASA-3-429004: Unable to set up _rule\_name__interface\_name__policy\_type_
    
-   %ASA-3-444303: %SMART\_LIC-3-AGENT\_REG\_FAILED: Smart Agent for licensing registration with Cisco licensing cloud failed.
    
-   %ASA-3-444303: %SMART\_LIC-3-AGENT\_DEREG\_FAILED: Smart Agent for licensing deregistration with CSSM failed.
    
-   %ASA-3-444303: %SMART\_LIC-3-OUT\_OF\_COMPLIANCE: One or more entitlements are out of compliance.
    
-   %ASA-3-444303: %SMART\_LIC-3-EVAL\_EXPIRED: Evaluation period expired.
    
-   %ASA-3-444303: %SMART\_LIC-3-BAD\_MODE: An unknown mode was specified.
    
-   %ASA-3-444303: %SMART\_LIC-3-BAD\_NOTIF: A bad notification type was specified.
    
-   %ASA-3-444303: %SMART\_LIC-3-ID\_CERT\_EXPIRED: Identity certificate expired. Agent will transition to the unidentified (not registered) state.
    
-   %ASA-3-444303: %SMART\_LIC-3-ID\_CERT\_RENEW\_NOT\_STARTED: Identity certificate start date not reached yet.
    
-   %ASA-3-444303: %SMART\_LIC-3-ID\_CERT\_RENEW\_FAILED: Identity certificate renewal failed.
    
-   %ASA-3-444303: %SMART\_LIC-3-ENTITLEMENT\_RENEW\_FAILED: Entitlement authorization with Cisco licensing cloud failed.
    
-   %ASA-3-444303: %SMART\_LIC-3-COMM\_FAILED: Communications failure with Cisco licensing cloud.
    
-   %ASA-3-444303: %SMART\_LIC-3-CERTIFICATE\_VALIDATION: Certificate validation failed by smart agent.
    
-   %ASA-3-444303: %SMART\_LIC-3-AUTH\_RENEW\_FAILED: Authorization renewal with Cisco licensing cloud failed.
    
-   %ASA-3-444303: %SMART\_LIC-3-INVALID\_TAG: The entitlement tag is invalid.
    
-   %ASA-3-444303: %SMART\_LIC-3-INVALID\_ROLE\_STATE: The current role is not allowed to move to the new role.
    
-   %ASA-3-444303: %SMART\_LIC-3-EVAL\_WILL\_EXPIRE\_WARNING: Evaluation period will expire in time.
    
-   %ASA-3-444303: %SMART\_LIC-3-EVAL\_EXPIRED\_WARNING: Evaluation period expired on time.
    
-   %ASA-3-444303: %SMART\_LIC-3-ID\_CERT\_EXPIRED\_WARNING: This device's registration will expire in time.
    
-   %ASA-3-444303: %SMART\_LIC-3-CONFIG\_OUT\_OF\_SYNC: Trusted Store Enable flag not in sync with System Configuration, TS flag Config flag.
    
-   %ASA-3-444303: %SMART\_LIC-3-REG\_EXPIRED\_CLOCK\_CHANGE: Smart Licensing registration has expired because the system time was changed outside the validity period of the registration period. The agent will transition to the un-registered state in 60 minutes.
    
-   %ASA-3-444303: %SMART\_LIC-3-ROOT\_CERT\_MISMATCH\_PROD: Certificate type mismatch.
    
-   %ASA-3-444303: %SMART\_LIC-3-HOT\_STANDBY\_OUT\_OF\_SYNC: Smart Licensing agent on hot standby is out of sync with active Smart Licensing agent.
    
-   %ASA-3-444714: Azure failed to retrieve Wireserver IPv4 address.
    
-   %ASA-3-505016: Module _module\_id__name__version__state__name__version__state_
    
-   %ASA-3-500005: Connection terminated for _protocol__in\_ifc\_name__src\_adddress__src\_port__out\_ifc\_name__dest\_address__dest\_port__inspect\_name__filter\_name_
    
-   %ASA-3-507003: _protocol__originating interface__src\_ip__src\_port_ _dest\_if__dest\_ip__dest\_port_ _reason_
    
-   %ASA-3-520001: error\_string
    
-   %ASA-3-520002: bad new ID table size
    
-   %ASA-3-520003: bad id in error\_string (id: 0xid\_num)
    
-   %ASA-3-520004: error\_string
    
-   %ASA-3-520005: error\_string
    
-   %ASA-3-520010: Bad queue elem – qelem\_ptr: flink flink\_ptr, blink blink\_ptr, flink->blink flink\_blink\_ptr, blink->flink blink\_flink\_ptr
    
-   %ASA-3-520011: Null queue elem
    
-   %ASA-3-520013: Regular expression access check with bad list acl\_ID
    
-   %ASA-3-520020: No memory available
    
-   %ASA-3-520021: Error deleting trie entry, error\_message
    
-   %ASA-3-520022: Error adding mask entry, error\_message
    
-   %ASA-3-520023: Invalid pointer to head of tree, 0x<radix\_node\_ptr>
    
-   %ASA-3-520024: Orphaned mask #radix\_mask\_ptr, refcount= radix\_mask\_ptr ‘s ref count at # radix\_node\_address, next=# radix\_node\_next
    
-   %ASA-3-520025: No memory for radix initialization: error\_msg
    
-   %ASA-3-602305: IPSEC: SA creation error, source _source address__destination address__error string_
    
-   %ASA-3-602306: IPSEC: SA change peer IP error, SPI: _IPsec SPI_, (src _original src IP address_/_original src port_, dest _original dest IP address_/_original dest port_ => src _new src IP address_/_new src port_, dest: _new dest IP address_/_new dest port_), reason _failure reason_.
    
-   %ASA-3-610001: NTP daemon interface _interface\_name__IP\_address_
    
-   %ASA-3-610002: NTP daemon interface _interface\_name__IP\_address_
    
-   %ASA-3-611313: VPNClient: Backup Server List Error: _reason_
    
-   %ASA-3-613004: Internal error: memory allocation failure
    
-   %ASA-3-613005: Flagged as being an ABR without a backbone area
    
-   %ASA-3-613006: Reached unknown state in neighbor state machine
    
-   %ASA-3-613007: area string lsid IP\_address mask netmask type number
    
-   %ASA-3-613008: if inside if\_state number
    
-   %ASA-3-613011: OSPF process number is changing router-id. Reconfigure virtual link neighbors with our new router-id
    
-   %ASA-3-613013: OSPF LSID IP\_address adv IP\_address type number gateway IP\_address metric number forwarding addr route IP\_address /mask type number has no corresponding LSA
    
-   %ASA-3-613029: Router-ID IP\_address is in use by ospf process number%ASA-3-613016: Area string router-LSA of length number bytes plus update overhead bytes is too large to flood.
    
-   %ASA-3-613032: Init failed for interface inside, area is being deleted. Try again.%ASA-3-613033: Interface inside is attached to more than one area
    
-   %ASA-3-613034: Neighbor IP\_address not configured
    
-   %ASA-3-613035: Could not allocate or find neighbor IP\_address%ASA-4-613015: Process 1 flushes LSA ID IP\_address type-number adv-rtr IP\_address in area mask
    
-   %ASA-3-702305: IPSEC: An _direction_ _tunnel\_type__spi_ _local\_IP__remote\_IP_
    
-   %ASA-3-710003: _{TCP|UDP}__source\_IP__source\_port__interface\_name__dest\_IP__service_
    
-   %ASA-3-713004: _device_ scheduled for reboot, IKE key acquire message on interface _interface num_, for peer _IP\_address_ ignored
    
-   %ASA-3-713008: IP = _peerIP_ Key ID in ID payload too big for pre-shared IKE tunnel
    
-   %ASA-3-713009: IP = _peerIP_ OU in DN in ID payload too big for Certs IKE tunnel
    
-   %ASA-3-713012: Group = _groupname_, Username = _username_, IP = _peerIP_ Unknown protocol (_protocol_ ). Not adding SA w/spi= _SPI value_
    
-   %ASA-3-713014: Group = _groupname_, Username = _username_, IP = _peerIP_ Unknown Domain of Interpretation (DOI): _DOI value_
    
-   %ASA-3-713016: Group = _groupname_, Username = _username_, IP = _peerIP_ Unknown identification type, Phase _1 or 2_, Type _ID\_Type_
    
-   %ASA-3-713017: Group = _groupname_, Username = _username_, IP = _peerIP_ Identification type not supported, Phase _1 or 2_, Type _ID\_Type_
    
-   %ASA-3-713018: IP = _peerIP_ Unknown ID type during find of group name for certs, Type _ID\_Type_
    
-   %ASA-3-713020: IP = _peerIP_ No Group found by matching OU(s) from ID payload: _OU\_value_
    
-   %ASA-3-713022: IP = _peerIP_ No Group found matching _peer\_ID or IP\_address_ for Pre-shared key peer _IP\_address_
    
-   %ASA-3-713032: Group = _groupname_, Username = _username_, IP = _peerIP_ Received invalid local Proxy Range _IP\_address_ - _IP\_address_
    
-   %ASA-3-713033: Group = _groupname_, Username = _username_, IP = _peerIP_ Received invalid remote Proxy Range _IP\_address_ - _IP\_address_
    
-   %ASA-3-713042: IKE Initiator unable to find policy: Intf _interface\_number_, Src: _source\_address_, Dst: _dest\_address_
    
-   %ASA-3-713043: Cookie/peer address _IP\_address_ session already in progress
    
-   %ASA-3-713047: Unsupported Oakley group: Group <Diffie-Hellman group>
    
-   %ASA-3-713048: Group = _groupname_, Username = _username_, IP = _peerIP_ Error processing payload: Payload ID: id
    
-   %ASA-3-713056: Group = _groupname_, Username = _username_, IP = _peerIP_ Tunnel rejected: SA (_SA\_name_ ) not found for group (_group\_name_ )!
    
-   %ASA-3-713060: Group = _groupname_, Username = _username_, IP = _peerIP_ Tunnel Rejected: User (_user_ ) not member of group (_group\_name_ ), group-lock check failed.
    
-   %ASA-3-713061: Group = _groupname_, Username = _username_, IP = _peerIP_ Tunnel rejected: Crypto Map Policy not found for Src:_source\_address_, Dst: _dest\_address_ !
    
-   %ASA-3-713062: IKE Peer address same as our interface address _IP\_address_
    
-   %ASA-3-713063: IKE Peer address not configured for destination _IP\_address_
    
-   %ASA-3-713065: IKE Remote Peer did not negotiate the following: _proposal attribute_
    
-   %ASA-3-713072: Group = _groupname_, Username = _username_, IP = _peerIP_ Password for user (_user_ ) too long, truncating to _number_ characters
    
-   %ASA-3-713081: Group = _groupname_, Username = _username_, IP = _peerIP_ Unsupported certificate encoding type _encoding\_type_
    
-   %ASA-3-713082: Group = _groupname_, Username = _username_, IP = _peerIP_ Failed to retrieve identity certificate
    
-   %ASA-3-713083: Group = _groupname_, Username = _username_, IP = _peerIP_ Invalid certificate handle
    
-   %ASA-3-713084: Group = _groupname_, Username = _username_, IP = _peerIP_ Received invalid phase 1 port value (_port_ ) in ID payload
    
-   %ASA-3-713085: Group = _groupname_, Username = _username_, IP = _peerIP_ Received invalid phase 1 protocol (_protocol_ ) in ID payload
    
-   %ASA-3-713086: Group = _groupname_, Username = _username_, IP = _peerIP_ Received unexpected Certificate payload Possible invalid Auth Method (Auth method (auth numerical value))
    
-   %ASA-3-713088: Group = _groupname_, Username = _username_, IP = _peerIP_ Set Cert filehandle failure: no IPsec SA in group _group\_name_
    
-   %ASA-3-713098: Group = _groupname_, Username = _username_, IP = _peerIP_ Aborting: No identity cert specified in IPsec SA (_SA\_name_ )!
    
-   %ASA-3-713102: Group = _groupname_, Username = _username_, IP = _peerIP_ Phase 1 ID Data length _number_ too long - reject tunnel!
    
-   %ASA-3-713105: Group = _groupname_, Username = _username_, IP = _peerIP_ Zero length data in ID payload received during phase 1 or 2 processing
    
-   %ASA-3-713107: Group = _groupname_, Username = _username_, IP = _peerIP_ IP\_Address request attempt failed!
    
-   %ASA-3-713109: Group = _groupname_, Username = _username_, IP = _peerIP_ Unable to process the received peer certificate
    
-   %ASA-3-713112: Group = _groupname_, Username = _username_, IP = _peerIP_ Failed to process CONNECTED notify (SPI _SPI\_value_ )!
    
-   %ASA-3-713014: Group = _groupname_, Username = _username_, IP = _peerIP_ Unknown Domain of Interpretation (DOI): _DOI value_
    
-   %ASA-3-713016: Group = _groupname_, Username = _username_, IP = _peerIP_ Unknown identification type, Phase _1 or 2_, Type _ID\_Type_
    
-   %ASA-3-713017: Group = _groupname_, Username = _username_, IP = _peerIP_ Identification type not supported, Phase _1 or 2_, Type _ID\_Type_
    
-   %ASA-3-713118: Detected invalid Diffie-Helmann _group\_descriptor_ _group\_number_, in IKE area
    
-   %ASA-3-713122: IP = _peerIP_ Keep-alives configured _keepalive\_type_ but peer _IP\_address_ support keep-alives (type = _keepalive\_type_ )
    
-   %ASA-3-713123: Group = _groupname_, Username = _username_, IP = _peerIP_ IKE lost contact with remote peer, deleting connection (keepalive type: _keepalive\_type_ )
    
-   %ASA-3-713127: Group = _groupname_, Username = _username_, IP = _peerIP_ Xauth required but selected Proposal does not support xauth, Check priorities of ike xauth proposals in ike proposal list
    
-   %ASA-3-713129: Group = _groupname_, Username = _username_, IP = _peerIP_ Received unexpected Transaction Exchange payload type: payload\_id
    
-   %ASA-3-713132: Group = _groupname_, Username = _username_, IP = _peerIP_ Cannot obtain an _IP\_address_ for remote peer
    
-   %ASA-3-713133: Group = _groupname_, Username = _username_, IP = _peerIP_ Mismatch: Overriding phase 2 DH Group(DH group _DH group\_id_ ) with phase 1 group(DH group _DH group\_number_
    
-   %ASA-3-713134: Group = _groupname_, Username = _username_, IP = _peerIP_ Mismatch: P1 Authentication algorithm in the crypto map entry different from negotiated algorithm for the L2L connection
    
-   %ASA-3-713138: IP = _peerIP_ Group _group\_name_ not found and BASE GROUP default preshared key not configured
    
-   %ASA-3-713140: Group = _groupname_, Username = _username_, IP = _peerIP_ Split Tunneling Policy requires network list but none configured
    
-   %ASA-3-713141: IP = _peerIP_ Client-reported firewall does not match configured firewall: _action_ tunnel. Received -- Vendor: _vendor(id)_, Product _product(id)_, Caps: _capability\_value_ . Expected -- Vendor: _vendor(id)_, Product: _product(id)_, Caps: _capability\_value_
    
-   %ASA-3-713142: IP = _peerIP_ Client did not report firewall in use, but there is a configured firewall: _action_ tunnel. Expected -- Vendor: _vendor(id)_, Product _product(id)_, Caps: _capability\_value_
    
-   %ASA-3-713146: Group = _groupname_, Username = _username_, IP = _peerIP_ Could not add route for Hardware Client in network extension mode, address: _IP\_address_, mask: _netmask_
    
-   %ASA-3-713149: Group = _groupname_, Username = _username_, IP = _peerIP_ Hardware client security attribute _attribute\_name_ was enabled but not requested.
    
-   %ASA-3-713152: IP = _peerIP_ Unable to obtain any rules from filter _ACL\_tag_ to send to client for CPP, terminating connection.
    
-   %ASA-3-713159: TCP Connection to Firewall Server has been lost, restricted tunnels are now allowed full network access
    
-   %ASA-3-713161: Group = _groupname_, Username = _username_, IP = _peerIP_ Remote user (session Id - _id_ ) network access has been restricted by the Firewall Server
    
-   %ASA-3-713162: Group = _groupname_, Username = _username_, IP = _peerIP_ Remote user (session Id - _id_ ) has been rejected by the Firewall Server
    
-   %ASA-3-713163: Group = _groupname_, Username = _username_, IP = _peerIP_ Remote user (session Id - _id_ ) has been terminated by the Firewall Server
    
-   %ASA-3-713165: Group = _groupname_, Username = _username_, IP = _peerIP_ Client IKE Auth mode differs from the group's configured Auth mode
    
-   %ASA-3-713166: Group = _groupname_, Username = _username_, IP = _peerIP_ Headend security gateway has failed our user authentication attempt - check configured username and password
    
-   %ASA-3-713167: Group = _groupname_, Username = _username_, IP = _peerIP_ Remote peer has failed user authentication - check configured username and password
    
-   %ASA-3-713168: Re-auth enabled, but tunnel must be authenticated interactively!
    
-   %ASA-3-713174: Group = _groupname_, Username = _username_, IP = _peerIP_ Hardware Client connection rejected! Network Extension Mode is not allowed for this group!
    
-   %ASA-3-713182: Group = _groupname_, Username = _username_, IP = _peerIP_ IKE could not recognize the version of the client! IPsec Fragmentation Policy will be ignored for this connection!
    
-   %ASA-3-713185: IP = _peerIP_ Error: Username too long - connection aborted
    
-   %ASA-3-713186: Invalid secondary domain name list received from the authentication server. List Received: _list\_text_ Character _index_ (_value_ ) is illegal
    
-   %ASA-3-713189: Group = _groupname_, Username = _username_, IP = _peerIP_ Attempted to assign network or broadcast _IP\_address_, removing ( _IP\_address_ ) from pool.
    
-   %ASA-3-713191: IP = _IP\_address_ Maximum concurrent IKE negotiations exceeded!
    
-   %ASA-3-713193: Received packet with missing payload, Expected payload: _payload\_id_
    
-   %ASA-3-713194: Group = _groupname_, Username = _username_, IP = _peerIP_ Sending _IKE_ |_IPsec_ Delete With Reason message: _termination\_reason_
    
-   %ASA-3-713195: Group = _groupname_, Username = _username_, IP = _peerIP_ Tunnel rejected: Originate-Only: Cannot accept incoming tunnel yet!
    
-   %ASA-3-713198: Group = _groupname_, Username = _username_, IP = _peerIP_ User Authorization failed: _user_ User authorization failed. Username could not be found in the certificate
    
-   %ASA-3-713203: IKE Receiver: Error reading from socket.
    
-   %ASA-3-713205: Group = _groupname_, Username = _username_, IP = _peerIP_ Could not add static route for client address: _IP\_address_
    
-   %ASA-3-713206: Group = _groupname_, Username = _username_, IP = _peerIP_ Tunnel Rejected: Conflicting protocols specified by tunnel-group and group-policy
    
-   %ASA-3-713208: Cannot create dynamic rule for Backup L2L entry rule _rule\_id_
    
-   %ASA-3-713209: Cannot delete dynamic rule for Backup L2L entry rule id
    
-   %ASA-3-713210: Cannot create dynamic map for Backup L2L entry rule\_id
    
-   %ASA-3-713212: Group = _groupname_, Username = _username_, IP = _peerIP_ Could not add route for L2L peer coming in on a dynamic map. address:
    
-   %ASA-3-713214: Group = _groupname_, Username = _username_, IP = _peerIP_ Could not delete route for L2L peer that came in on a dynamic map. address: _IP\_address_, mask: _netmask_
    
-   %ASA-3-713217: Group = _groupname_, Username = _username_, IP = _peerIP_ Skipping unrecognized rule: action: _action_ client type: _client\_type_ client version: _client\_version_
    
-   %ASA-3-713218: Group = _groupname_, Username = _username_, IP = _peerIP_ Tunnel Rejected: Client Type or Version not allowed.
    
-   %ASA-3-713226: Connection failed with peer _IP\_address_, no trust-point defined in tunnel-group _tunnel\_group_
    
-   %ASA-3-713227: IP = _IP\_address_ Rejecting new IPsec SA negotiation for peer _Peer\_address_ . A negotiation was already in progress for local Proxy _Local\_address_ /_Local\_netmask_, remote Proxy _Remote\_address_ /_Remote\_netmask_
    
-   %ASA-3-713230: Internal Error, ike\_lock trying to lock bit that is already locked for type type
    
-   %ASA-3-713231: Internal Error, ike\_lock trying to unlock bit that is not locked for type type
    
-   %ASA-3-713232: SA lock refCnt = value, bitmask = hexvalue, p1\_decrypt\_cb = value, qm\_decrypt\_cb = value, qm\_hash\_cb = value, qm\_spi\_ok\_cb = value, qm\_dh\_cb = value, qm\_secret\_key\_cb = value, qm\_encrypt\_cb = value
    
-   %ASA-3-713238: Group = _groupname_, Username = _username_, IP = _peerIP_ Invalid source proxy address: 0.0.0.0! Check private address on remote client
    
-   %ASA-3-713258: IP = _var1_ IP = _var1_, Attempting to establish a phase2 tunnel on _var2_ interface but phase1 tunnel is on _var3_ interface. Tearing down old phase1 tunnel due to a potential routing change.
    
-   %ASA-3-713254: Group = _groupname_, Username = _username_, IP = _peerip_ Group = _groupname_, Username = _username_, IP = _peerip_, Invalid IPsec/UDP port = _portnum_, valid range is _minport_ - _maxport_, except port 4500, which is reserved for IPsec/NAT-T
    
-   %ASA-3-713260: Output interface _%d_ to peer was not found
    
-   %ASA-3-713262: IP = _IP\_address_ Rejecting new IPSec SA negotiation for peer _Peer\_address_ . A negotiation was already in progress for local Proxy _Local\_address_ /_Local\_prefix\_len_, remote Proxy _Remote\_address_ /_Remote\_prefix\_len_
    
-   %ASA-3-713266: Group = _groupname_, Username = _username_, IP = _peerIP_ Could not add route for L2L peer coming in on a dynamic map. address: _IP\_address_, mask: /_prefix\_len_
    
-   %ASA-3-713268: Group = _groupname_, Username = _username_, IP = _peerIP_ Could not delete route for L2L peer that came in on a dynamic map. address: _IP\_address_, mask: /_prefix\_len_
    
-   %ASA-3-713270: Group = _groupname_, Username = _username_, IP = _peerIP_ Could not add route for Hardware Client in network extension mode, address: _IP\_address_, mask: /_prefix\_len_
    
-   %ASA-3-713274: Group = _groupname_, Username = _username_, IP = _peerIP_ Could not delete static route for client address: _IP\_Address IP\_Address_ address of client whose route is being removed
    
-   %ASA-3-713275: IKEv1 Unsupported certificate keytype %s found at trustpoint %s
    
-   %ASA-3-713276: IP = _IP\_address_ Dropping new negotiation - IKEv1 in-negotiation context limit of %u reached
    
-   %ASA-3-713902: Descriptive\_event\_string.
    
-   %ASA-3-716056: Group group-name User user-name IP IP\_address Authentication to SSO server name: name type type failed reason: reason
    
-   %ASA-3-716057: Group _group__user__ip__type_
    
-   %ASA-3-716061: Group _DfltGrpPolicy__user__ip addr__tempipv6_
    
-   %ASA-3-716158: Failed to create SAML logout request, initiated by _user_. reason: _reason_.
    
-   %ASA-3-716159: Failed to process SAML logout request. reason: _reason_.
    
-   %ASA-3-716160: Failed to create SAML authentication request. reason: _reason_.
    
-   %ASA-3-716162: Failed to consume SAML assertion. reason: _reason_.
    
-   %ASA-3-716163: SAML response relay state failed data integrity check. Client IP: _IP address_
    
-   %ASA-3-716164: SAML response relay state missing data integrity hash. Client IP: _IP address_
    
-   %ASA-3-716600: Rejected _size-recv__src-ip__default__configured_
    
-   %ASA-3-716601: Rejected _size-recv__src-ip__default__configured_
    
-   %ASA-3-716602: Memory allocation error. Rejected _size-recv__src-ip_
    
-   %ASA-3-717001: Querying keypair failed.
    
-   %ASA-3-717002: Certificate enrollment failed for trustpoint _trustpoint\_name__reason\_string_
    
-   %ASA-3-717009: Certificate validation failed. _reason\_string_
    
-   %ASA-3-717010: CRL polling failed for trustpoint _trustpoint\_name_
    
-   %ASA-3-717012: Failed to refresh CRL cache entry from the server for trustpoint trustpoint\_name at time\_of\_failure
    
-   %ASA-3-717015: CRL received from issuer is too large to process (CRL size = crl\_size, maximum CRL size = max\_crl\_size)
    
-   %ASA-3-717017: Failed to query CA certificate for trustpoint _trustpoint\_name__enrollment\_url_
    
-   %ASA-3-717018: CRL received from issuer has too many entries to process (number of entries = number\_of\_entries, maximum number allowed = max\_allowed)
    
-   %ASA-3-717019: Failed to insert CRL for trustpoint _trustpoint\_name__failure\_reason_
    
-   %ASA-3-717020: Failed to install device certificate for trustpoint _label__reason string_
    
-   %ASA-3-717021: Certificate data could not be verified. Reason: _reason\_string__serial number_
    
-   %ASA-3-717023: SSL failed to set device certificate for trustpoint _trustpoint name__reason\_string_
    
-   %ASA-3-717027: Certificate chain failed validation. _reason\_string_
    
-   %ASA-3-717032: OCSP status check failed. Reason: _reason\_string_.
    
-   %ASA-3-717039: Local CA Server internal error detected: _error._
    
-   %ASA-3-717042: Failed to enable Local CA Server. Reason: _reason_
    
-   %ASA-3-717044: Local CA Server certificate enrollment related error for user: _user__error_
    
-   %ASA-3-717046: Local CA Server CRL error: _error_
    
-   %ASA-3-717051: SCEP Proxy: Denied processing the request type _type__client ip address__username__tunnel group name__group policy name__ca ip address__msg_
    
-   %ASA-3-717057: Automatic import of trustpool certificate bundle has failed. _Maximum retry attempts reached. Failed to reach CA server | Cisco root bundle signature validation failed | Failed to update trustpool bundle in flash | Failed to install trustpool bundle in memory_
    
-   %ASA-3-717060: Peer certificate with _serial number: serial, subject: subject\_name, issuer: issuer\_name_ failed to match the configured certificate map _map\_name_
    
-   %ASA-3-717063: _protocol__tpname__ca_
    
-   %ASA-3-717069: ACME Certificate enrollment failed for the trustpoint _tpname_ with CA _ca_
    
-   %ASA-3-717071: CRL signature validation failed. Issuer: _issuer name_. Last Update: _date and time_. Next Update: _date and time_.
    
-   %ASA-3-719002: Email Proxy session pointer from source\_address has been terminated due to reason error.
    
-   %ASA-3-719008: Email Proxy service is shutting down.
    
-   %ASA-3-722007: Group _group__user-name__IP\_address__type-num__message_
    
-   %ASA-3-722008: Group _group__user-name__IP\_address__type-num__message_
    
-   %ASA-3-722009: Group _group__user-name__IP\_address__type-num__message_
    
-   %ASA-3-722020: TunnelGroup _tunnel\_group__group\_policy__user-name__IP\_address_
    
-   %ASA-3-722021: Group _group__user-name__IP\_address_
    
-   %ASA-3-722035: Group _group__user-name__IP\_address__length__num_
    
-   %ASA-3-722045: Connection terminated: no SSL tunnel initialization data
    
-   %ASA-3-722046: Group _group__user__ip_
    
-   %ASA-3-725015 Error verifying client certificate. Public key size in client certificate exceeds the maximum supported key size.
    
-   %ASA-3-730005: Group _DfltGrpPolicy__username__IP__vlan\_id_
    
-   %ASA-3-734004: DAP: Processing error: Code _internal_
    
-   %ASA-3-735010: Environment Monitoring has failed to update one or more of its records.
    
-   %ASA-3-737002: IPAA: Session=_session__num_
    
-   %ASA-3-737027: IPAA: Session=
    
-   %ASA-3-737202: VPNFIP: Pool=_pool__message_
    
-   %ASA-3-737403: POOLIP: Pool=_pool__message_
    
-   %ASA-3-742001: failed to read master key for password encryption from persistent store
    
-   %ASA-3-742002: failed to set master key for password encryption
    
-   %ASA-3-742003: failed to save master key for password encryption, reason=_reason\_text_
    
-   %ASA-3-742004: failed to sync master key for password encryption, reason=_reason\_text_
    
-   %ASA-3-742005: cipher text _enc\_pass_
    
-   %ASA-3-742006: password decryption failed due to unavailable memory
    
-   %ASA-3-742007: password encryption failed due to unavailable memory
    
-   %ASA-3-742008: password _enc\_pass_
    
-   %ASA-3-742009: password encryption failed due to encoding error
    
-   %ASA-3-742010: encrypted password _enc\_pass_
    
-   %ASA-3-743010: EOBC RPC server failed to start for client module _client name_
    
-   %ASA-3-743011: EOBC RPC call failed, return code _code_
    
-   %ASA-3-746003: user-identity: _user-to-IP address databases__reason_
    
-   %ASA-3-746005: user-identity: The AD Agent _AD agent IP address__reason_ _action_
    
-   %ASA-3-746010: user-identity: Update import-user _domain\_name__group\_name_
    
-   %ASA-3-746016: user-identity: DNS lookup for _ip__reason_
    
-   %ASA-3-746019: user-identity: _Update__Remove__AD agent IP Address__user\_IP__domain\_name_
    
-   %ASA-3-747001: Clustering: Recovered from state machine event queue depleted. Event (event-id, ptr-in-hex, ptr-in-hex) dropped. Current state state-name, stack ptr-in-hex, ptr-in-hex, ptr-in-hex, ptr-in-hex, ptr-in-hex, ptr-in-hex
    
-   %ASA-3-747010: Clustering: RPC call failed, message message-name, return code code-value.
    
-   %ASA-3-747012: Clustering: Failed to replicate global object id hex-id-value in domain domain-name to peer unit-name, continuing operation.
    
-   %ASA-3-747013: Clustering: Failed to remove global object id hex-id-value in domain domain-name from peer unit-name, continuing operation.
    
-   %ASA-3-747014: Clustering: Failed to install global object id hex-id-value in domain domain-name, continuing operation.
    
-   %ASA-3-747018: Clustering: State progression failed due to timeout in module module-name.
    
-   %ASA-3-747021: Clustering: Master unit unit-name is quitting due to interface health check failure on failed-interface.
    
-   %ASA-3-747022: Clustering: Asking slave unit unit-name to quit because it failed interface health check x times, rejoin will be attempted after y min. Failed interface: interface-name.
    
-   %ASA-3-747023: Clustering: Master unit unit-name is quitting due to card name card health check failure, and master Security Service Card state is state-name.
    
-   %ASA-3-747024: Clustering: Asking slave unit unit-name to quit due to card name card health check failure, and its Security Service Card state is state-name.
    
-   %ASA-3-747030: Clustering: Asking slave unit unit-name to quit because it failed interface health check x times (last failure on interface-name), Clustering must be manually enabled on the unit to re-join.
    
-   %ASA-3-747031: Clustering: Platform mismatch between cluster master (platform-type) and joining unit unit-name (platform-type). unit-name aborting cluster join.
    
-   %ASA-3-747032: Clustering: Service module mismatch between cluster master (module-name) and joining unit unit-name (module-name) in slot slot-number. unit-name aborting cluster join.
    
-   %ASA-3-747033: Clustering: Interface mismatch between cluster master and joining unit unit-name. unit-name aborting cluster join.
    
-   %ASA-3-747036: Application software mismatch between cluster master %s\[Master unit name\] (%s\[Master application software name\]) and joining unit (%s\[Joining unit application software name\]). %s\[Joining member name\] aborting cluster join.
    
-   %ASA-3-747037: Asking slave unit %s to quit due to its Security Service Module health check failure %d times, and its Security Service Module state is %s. Rejoin will be attempted after %d minutes.
    
-   %ASA-3-747038: Asking slave unit %s to quit due to Security Service Module health check failure %d times, and its Security Service Card Module is %s. Clustering must be manually enabled on this unit to rejoin.
    
-   %ASA-3-747039: Unit %s is quitting due to system failure for %d time(s) (last failure is %s\[cluster system failure reason\]). Rejoin will be attempted after %d minutes.
    
-   %ASA-3-747040: Unit %s is quitting due to system failure for %d time(s) (last failure is %s\[cluster system failure reason\]). Clustering must be manually enabled on the unit to rejoin.
    
-   %ASA-3-747041: Unit %s is quitting due to system failure for %d time(s) (last failure is %s\[cluster system failure reason\]). Clustering must be manually enabled on the unit to rejoin.Master unit %s is quitting due to interface health check failure on %s\[interface name\], %d times. Clustering must be manually enabled on the unit to rejoin.
    
-   %ASA-3-747042: Clustering: Master received the config hash string request message from an unknown member, id <cluster-member-id>
    
-   %ASA-3-747043: Clustering: Get config hash string from master error.
    
-   %ASA-6-747044: Clustering: Configuration Hash string verification <result>.
    
-   %ASA-3-748005: Failed to bundle the ports for module slot\_number in chassis chassis\_number; clustering is disabled
    
-   %ASA-3-748006: Asking module slot\_number in chassis chassis\_number to leave the cluster due to a port bundling failure
    
-   %ASA-3-748100: <application\_name> application status is changed from <status> to <status>.
    
-   %ASA-3-748101: Peer unit <unit\_id> reported its <application\_name> application status is <status>.
    
-   %ASA-3-748102: Master unit <unit\_id> is quitting due to <application\_name> Application health check failure, and master's application state is <status>.
    
-   %ASA-3-748103: Asking slave unit <unit\_id> to quit due to <application\_name> Application health check failure, and slave's application state is <status>.
    
-   %ASA-3-748202: Module <module\_id> in chassis <chassis id> is leaving the cluster due to <aplpication name> application failure.
    
-   %ASA-3-750011: Tunnel Rejected: Selected IKEv2 encryption algorithm (_IKEV2 encry algo_ ) is not strong enough to secure proposed IPSEC encryption algorithm (_IPSEC encry algo_ ).
    
-   %ASA-3-751001: Failed to complete Diffie-Hellman operation. Error: _error_.
    
-   %ASA-3-751002: No pre-shared key or trustpoint configured for self in tunnel group _group_
    
-   %ASA-3-751004: No remote authentication method configured for peer in tunnel group _group_
    
-   %ASA-3-751005: AnyConnect client reconnect authentication failed. Session ID: _session\_id_, Error: _error_
    
-   %ASA-3-751006: Certificate authentication failed. Error: _error_
    
-   %ASA-3-751008: Group=_group_, Tunnel rejected: IKEv2 not enabled in group policy
    
-   %ASA-3-751009: Unable to find tunnel group for peer.
    
-   %ASA-3-751010: Local: localIP:port Remote:remoteIP:port Username: username/group Unable to determine self-authentication method. No crypto map setting or tunnel group found.
    
-   %ASA-3-751011: Failed user authentication. Error: _error_
    
-   %ASA-3-751012: Failure occurred during Configuration Mode processing. Error: _error_
    
-   %ASA-3-751013: Failed to process Configuration Payload request for attribute _attribute\_id_. Error: _error_
    
-   %ASA-3-751017: Configuration Error: _error\_description_.
    
-   %ASA-3-751018: Terminating the VPN connection attempt from _attempted group_.
    
-   %ASA-3-751020: Local:%A:%u Remote:%A:%u Username:%s An %s remote access connection failed. Attempting to use an NSA Suite B crypto algorithm (%s) without an AnyConnect Premium license.
    
-   %ASA-3-751022: Tunnel rejected: Crypto Map Policy not found for remote traffic selector _rem-ts-start_/_rem-ts-end_/_rem-ts.startport_/_rem-ts.endport_/_rem-ts.protocol_ local traffic selector _local-ts-start_/_local-ts-end_/_local-ts.startport_/_local-ts.endport_/_local-ts.protocol_!
    
-   %ASA-3-751024: IPv6 User Filter _tempipv6_ configured. This setting has been deprecated, terminating connection
    
-   %ASA-3-752006: Tunnel Manager failed to dispatch a KEY\_ACQUIRE message. Probable mis-configuration of the crypto map or tunnel-group. Map Tag = _Tag_ . Map Sequence Number = _num,_ SRC Addr: _address_ port_: port_ Dst Addr: _address_ port: _port_ .
    
-   %ASA-3-752007: Tunnel Manager failed to dispatch a KEY\_ACQUIRE message. Entry already in Tunnel Manager. Map Tag = _mapTag_ . Map Sequence Number = _mapSeq_
    
-   %ASA-3-752015: Tunnel Manager has failed to establish an L2L SA. All configured IKE versions failed to establish the tunnel. Map Tag = _mapTag_ . Map Sequence Number = _mapSeq_ .
    
-   %ASA-3-768003: QUOTA: _management session_ quota exceeded for user _user name_: current _3_,user limit _3_
    
-   %ASA-3-768004: QUOTA: _management session_ quota exceeded for _ssh/telnet/http_ protocol: current _2_, protocol limit _2_
    
-   %ASA-3-769006: UPDATE: _ASA__image\_name_
    
-   %ASA-3-771003: CLOCK: Hardware clock UIP bit is set to 1, for _duration_ secs, start time _duration_ secs, end time _duration_ secs. Read clock time from linux system clock
    
-   %ASA-3-776001: CTS SXP: Configured source IP source ip error
    
-   %ASA-3-776002: CTS SXP: Invalid message from peer peer IP: error
    
-   %ASA-3-776003: CTS SXP: Connection with peer peer IP failed: error
    
-   %ASA-3-776004: CTS SXP: Fail to start listening socket after TCP process restart.
    
-   %ASA-3-776005: CTS SXP: Binding Binding IP - SGname(SGT) from peer IP instance connection instance num error.
    
-   %ASA-3-776006: CTS SXP: Internal error: error
    
-   %ASA-3-776007: CTS SXP: Connection with peer peer IP (instance connection instance num) state changed from original state to Off.
    
-   %ASA-3-776020: CTS SXP: Unable to locate egress interface to peer peer IP.
    
-   %ASA-3-776202: CTS Env: PAC for Server _IP\_address__PAC issuer name_
    
-   %ASA-3-776203: CTS Env: Unable to retrieve data from _source\_type__source__reason_
    
-   %ASA-3-776204: CTS Env: Data from _source_
    
-   %ASA-3-776254: CTS SGT-MAP: Binding manager unable to action binding binding IP - SGname (SGT) from source name.
    
-   %ASA-3-776313: CTS Policy: Failure to update policies for security-group "_sgname__sgt_
    
-   %ASA-3-768001: QUOTA: _resource__req__curr__level_
    
-   %ASA-3-768002: QUOTA: _resource__req__curr__limit_
    
-   %ASA-3-772002: PASSWORD: _console__username_
    
-   %ASA-3-772004: PASSWORD: _session__username__ip_
    
-   %ASA-3-779003: STS: Failed to read tag-switching table - _reason_
    
-   %ASA-3-779004: STS: Failed to write tag-switching table - _reason_
    
-   %ASA-3-779005: STS: Failed to parse tag-switching request from http - _reason_
    
-   %ASA-3-779006: STS: Failed to save tag-switching table to flash - _reason_
    
-   %ASA-3-779007: STS: Failed to replicate tag-switching table to peer - _reason_
    
-   %ASA-3-840001: Failed to create the backup for an IKEv2 session <Local IP>, <Remote IP>
    
-   %ASA-3-850001: SNORT ID (<snort-instance-id>/<snort-process-id>) Automatic-Application-Bypass due to delay of <delay>ms (threshold <AAB-threshold>ms) with <connection-info>
    
-   %ASA-3-850002: SNORT ID (_snort-instance-id__snort-process-id__timeout-delay__AAB-threshold_
    
-   %ASA-3-861001: AVC: Creating AVC app directory _directory\_name_ failed; _reason\_string_.
    
-   %ASA-3-861002: AVC: Downloading file from link _link_ to directory _directory\_name_ succeeded.
    
-   %ASA-3-861003: AVC: Downloading file from link _link_ to directory _directory\_name_ failed; _reason\_string_.
    
-   %ASA-3-861004: AVC: Getting VDB version from file _file_ failed; _reason\_string_.
    
-   %ASA-3-861005: AVC: Getting VDB file path from file _file_ failed; _reason\_string_.
    
-   %ASA-3-861006: AVC: Getting VDB file name from file _file_ failed; _reason\_string_.
    
-   %ASA-3-861008: AVC Loading network service (app) definition file (_file_) success.
    
-   %ASA-3-861010: AVC: Loading app category definition file warning; _reason\_string_.
    
-   %ASA-3-861013: AVC: Installing visibility NSG success.
    
-   %ASA-3-8300003: Failed to send session redistribution message to <variable 1>
    
-   %ASA-3-8300005: Failed to receive session move response from <variable 1>
    

## Warning Messages, Severity 4

The following messages appear at severity 4, warning:

-   %ASA-4-105505: (Primary|Secondary) Failed to connect to peer unit _peer-ip_:_port_
    
-   %ASA-4-105524: (Primary|Secondary) Transitioning to Negotiating state due to the presence of another Active HA unit
    
-   %ASA-4-105553: (Primary|Secondary) Detected another Active HA unit
    

-   %ASA-4-106023: Deny _interface\_name__source\_address__source\_port__idfw\_user_
    
-   %ASA-4-106027: Deny _int\_type_ src _src\_address_:_src\_mac_ dst _dst\_address_:_dest\_mac_ by access-group _"access-list name"_.
    
-   %ASA-4-106103: access-list _acl\_ID__denied__protocol__username__source\_address__source\_port interface\_name__interface\_name__dest\_address__dest\_port__interface\_name__number__first hit__hash code1__hashcode2_
    
-   %ASA-4-108004: _action\_class: action_ _req\_resp_ _src\_ifc__sip__sport_ _dest\_ifc_ _dip__dport__further\_info_
    
-   %ASA-4-109017: User at _IP\_address__limit_
    
-   %ASA-4-109022: HTTPS proxy resource limit reached.
    
-   %ASA-4-109027: \[ _aaa protocol__server\_IP\_address__user_
    
-   %ASA-4-109028: aaa bypassed for same-security traffic from _ingress\_interface__source\_address__source\_port__egress\_interface__dest\_address__dest\_port_
    
-   %ASA-4-109030: Autodetect ACL convert wildcard did not convert ACL _access\_list source__dest__netmask_
    
-   %ASA-4-109031: NT Domain Authentication Failed: rejecting guest login for username.
    
-   %ASA-4-109033: Authentication failed for admin user _user__src\_IP__protocol_
    
-   %ASA-4-109040: User at _IP_
    
-   %ASA-4-109034: Authentication failed for network user _user__src\_IP__port__dst\_IP__port__protocol_
    
-   %ASA-4-109102: Received CoA _action-type__coa-source-ip__audit-session-id_
    
-   %ASA-4-113019: Group = _group__username__peer\_address__type__duration__count__count__reason_
    
-   %ASA-4-113026: Error _error__tunnel group_
    
-   %ASA-4-113029: Group _group__user__ipaddr__num_
    
-   %ASA-4-113030: Group _group__user__ipaddr__acl_
    
-   %ASA-4-113031: Group _group__user__ipaddr__AnyConnect__filter_
    
-   %ASA-4-113032: Group _group__user__ipaddr__AnyConnect__filter_
    
-   %ASA-4-113034: Group _group__user__ipaddr__acl_
    
-   %ASA-4-113035: Group <_group_\> User <_user_\> IP <_ip\_address_\> Session terminated: AnyConnect not enabled or invalid AnyConnect image on the _device\_name_
    
-   %ASA-4-113036: Group _group__user__ipaddr__name_
    
-   %ASA-4-113038: Group _group__user__ipaddr__AnyConnect parent_
    
-   %ASA-4-113040: Group _group__user__ipaddr__attempted group__locked group._
    
-   %ASA-4-113041: Redirect ACL configured for _assigned IP_
    
-   %ASA-4-113042: Non-HTTP connection from _src\_if__src\_ip__src\_port__dest\_if__dest\_ip__dest\_port_
    
-   %ASA-4-115002: Warning in process: process name fiber: fiber name, component: component name, subcomponent: subcomponent name, file: filename, line: line number, cond: condition
    
-   %ASA-4-120004: Call-Home _group__title__reason_
    
-   %ASA-4-120005: Call-Home _group__destination__reason_
    
-   %ASA-4-120006: Call-Home _group__destination__reason_
    
-   %ASA-4-120011: To ensure Smart Call Home can properly communicate with Cisco, use the command \\ to configure at least one DNS server.
    
-   %ASA-4-199016: syslog
    
-   %ASA-4-209003: Fragment database limit of number exceeded: src = source\_address, dest = dest\_address, proto = protocol, id = number
    
-   %ASA-4-209004: Invalid IP fragment, size = bytes exceeds maximum size = bytes: src = source\_address, dest = dest\_address, proto = protocol, id = number
    
-   %ASA-4-209005: Discard IP fragment set with more than number elements: src = Too many elements are in a fragment set.
    
-   %ASA-4-209006: Fragment queue threshold exceeded, dropped TCP fragment from IP address/port to IP address/port on outside interface.
    
-   %ASA-4-213007: L2TP: Failed to install Redirect URL: _redirect URL__non\_exist__assigned IP_
    
-   %ASA-4-216004: prevented: _error_ in _function_ at _file_(_line_) - _stack trace_
    
-   %ASA-4-302034: Unable to Pre-allocate H323 GUP Connection for faddr _interface\_name_:_foreign\_ip\_address_ to laddr _interface\_name_:_local\_ip\_address_/_local\_port_
    
-   %ASA-4-302034: Unable to Pre-allocate H323 GUP Connection for faddr _interface\_name_:_foreign\_ip\_address_/_foreign\_port_ to laddr _interface\_name_:_local\_ip\_address_
    
-   %ASA-4-302310: SCTP _packet__src\_ifc__src\_ip__src\_port__dst\_ifc__dst\_ip__dst\_port_
    
-   %ASA-4-302311: Failed to create a new _protocol_ connection from _ingress\_interface_:_source\_ip_/_source\_port_ to _egress\_interface_:_destination\_ip_/_destination\_port_ due to application cache memory allocation failure. The app-cache memory threshold level is _threshold%_ and threshold check is _enabled/disabled_
    
-   %ASA-4-305021: Ports exhausted in pre-allocated PAT pool IP _mapped\_ip\_address_ for host _real\_host\_ip_. Allocating from new PAT pool IP _mapped\_ip\_address_
    
-   %ASA-4-305022: Cluster unit _unit\_name_ has been allocated _num\_of\_port\_blocks_ port-blocks from _ip\_address_ on interface _interface\_name_ for PAT usage. All units should have at least _min\_num\_of\_port\_blocks_ port-blocks
    
-   %ASA-4-308002: static _global\_address__inside\_address__netmask__global\_address__inside\_address__netmask_
    
-   %ASA-4-308003: WARNING: The enable password is not configured
    
-   %ASA-4-308004: The enable password has been configured by user _admin_
    
-   %ASA-4-313004: Denied ICMP type=_icmp\_type_, from laddr _source\_ip\_address_ on interface _interface\_name_ to _destination\_ip\_address_: no matching session
    
-   %ASA-4-313004: Denied ICMP type=_icmp\_type_, from laddr _source\_ip\_address_ on interface shared _physical\_interface\_name_ to _destination\_ip\_address_: no matching session
    
-   %ASA-4-313005: No matching connection for ICMP error message: _icmp\_msg\_info__interface\_name__embedded\_frame\_info icmp\_msg\_info =_
    
-   %ASA-4-313009: Denied invalid ICMP code _icmp\_code_, for _src\_ifc_:_src\_address_/_src\_port_ (_mapped\_src\_address_/_mapped\_src\_port_) to _dest\_ifc_:_dest\_address_/_dest\_port_ (_mapped\_dest\_address_/_mapped\_dest\_port_) \[(_user_)\], ICMP id icmp\_id, ICMP type _icmp\_type_
    
-   %ASA-4-315009: SSH: connection timed out: username <username> , IP <ip>
    
-   %ASA-4-324302: Server=_IPaddr_:_port_, ID=_id_: Rejecting the RADIUS response: _Reason_.
    
-   %ASA-4-325002: Duplicate address _ipv6\_address__MAC\_address__interface_
    
-   %ASA-4-325004: IPv6 Extension Header _hdr\_type__action__protocol__src\_int__src\_ipv6\_addr__src\_port__dst\_interface__dst\_ipv6\_addr__dst\_port_
    
-   %ASA-4-325005: Invalid IPv6 Extension Header Content:_string__detail regarding protocol__ingress interface__IP__port__egress interface__IP__port_
    
-   %ASA-4-325006: IPv6 Extension Header not in order: Type _hdr\_type__hdr\_type__prot__src\_int__src\_ipv6\_addr__src\_port__dst\_interface__dst\_ipv6\_addr__dst\_port_
    
-   %ASA-4-335005: NAC Downloaded ACL parse failure - host-address
    
-   %ASA-4-337005: Phone Proxy SRTP: Media session not found for media\_term\_ip/media\_term\_port for packet from in\_ifc:src\_ip/src\_port to out\_ifc:dest\_ip/dest\_port
    
-   %ASA-4-338001: Dynamic Filter _monitored__protocol__in\_interface__src\_ip\_addr__src\_port__mapped-ip__mapped-port)__out\_interface__dest\_ip\_addr__dest\_port__mapped-ip__mapped-port),_ _malicious address__local or dynamic__domain name_ _level\_value_ _category\_name_
    
-   %ASA-4-338002: Dynamic Filter _monitored__protocol__in\_interface__src\_ip\_addr__src\_port__mapped-ip__mapped-port__out\_interface__dest\_ip\_addr__dest\_port__mapped-ip__mapped-port__malicious address__local or dynamic__domain name__level\_value__category\_name_
    
-   %ASA-4-338003: Dynamic Filter _monitored__protocol__in\_interface__src\_ip\_addr__src\_port__mapped-ip__mapped-port)__out\_interface__dest\_ip\_addr__dest\_port__mapped-ip__mapped-port)_ _malicious address__local or dynamic__ip address_ _netmask_ _level\_value_ _category\_name_
    
-   %ASA-4-338004: Dynamic Filter _monitored__protocol__in\_interface__src\_ip\_addr__src\_port__mapped-ip__mapped-port__out\_interface__dest\_ip\_addr__dest\_port__mapped-ip__mapped-port__malicious address__local or dynamic__ip address__netmask__level\_value__category\_name_
    
-   %ASA-4-338005: Dynamic Filter _dropped__protocol__in\_interface__src\_ip\_addr__src\_port__mapped-ip__mapped-port__out\_interface__dest\_ip\_addr__dest\_port__mapped-ip__mapped-port__malicious address__local or dynamic__domain name_ _level\_value__category\_name_
    
-   %ASA-4-338006: Dynamic Filter _dropped__protocol__in\_interface__src\_ip\_addr__src\_port__mapped-ip__mapped-port__out\_interface__dest\_ip\_addr__dest\_port__mapped-ip__mapped-port__malicious address__local or dynamic__domain name_ _level\_value_ _category\_name_
    
-   %ASA-4-338007: Dynamic Filter _dropped__protocol__in\_interface__src\_ip\_addr__src\_port__mapped-ip__mapped-port__out\_interface__dest\_ip\_addr__dest\_port__mapped-ip__mapped-port__malicious address__local or dynamic__ip address__netmask_ _level\_value_ _category\_name_
    
-   %ASA-4-338008: Dynamic Filter _dropped__protocol__in\_interface__src\_ip\_addr__src\_port__mapped-ip__mapped-port__out\_interface__dest\_ip\_addr__dest\_port__mapped-ip__mapped-port__malicious address__local or dynamic__ip address__netmask_ _level\_value_ _category\_name_
    
-   %ASA-4-338101: Dynamic Filter _action_ whitelisted _protocol_ traffic from _in\_interface_:_src\_ip\_addr_/_src\_port_ (_mapped-ip_/_mapped-port_) to _out\_interface_:_dest\_ip\_addr_/_dest\_port_ (_mapped-ip_/_mapped-port_), source _malicious address_ resolved from _local or dynamic_ list: _domain name_
    
-   %ASA-4-338102: Dynamic Filter _action__protocol__in\_interface__src\_ip\_addr__src\_port__mapped-ip__mapped-port__out\_interface__dest\_ip\_addr__dest\_port__mapped-ip__mapped-port__malicious address__local or dynamic__domain name_
    
-   %ASA-4-338103: Dynamic Filter _action__protocol__in\_interface__src\_ip\_addr__src\_port__mapped-ip__mapped-port)__out\_interface__dest\_ip\_addr__dest\_port__mapped-ip__mapped-port__malicious address__local or dynamic__ip address__netmask_
    
-   %ASA-4-338104: Dynamic Filter _action__protocol__in\_interface__src\_ip\_addr__src\_port__mapped-ip__mapped-port__out\_interface__dest\_ip\_addr__dest\_port__mapped-ip__mapped-port__malicious address__local or dynamic__ip address__netmask_
    
-   %ASA-4-338201: Dynamic Filter _monitored__protocol__in\_interface__src\_ip\_addr__src\_port__mapped-ip__mapped-port)__out\_interface__dest\_ip\_addr__dest\_port__mapped-ip__mapped-port)_ _malicious address__local or dynamic__domain name_ _level\_value_ _category\_name_
    
-   %ASA-4-338202: Dynamic Filter _monitored__protocol__in\_interface__src\_ip\_addr__src\_port__mapped-ip__mapped-port__out\_interface__dest\_ip\_addr__dest\_port__mapped-ip__mapped-port__malicious address__local or dynamic__domain name_ _level\_value_ _category\_name_
    
-   %ASA-4-338203: Dynamic Filter _dropped__protocol__in\_interface__src\_ip\_addr__src\_port__mapped-ip__mapped-port__out\_interface__dest\_ip\_addr__dest\_port__mapped-ip__mapped-port__malicious address__local or dynamic__domain name_ _level\_value_ _category\_name_
    
-   %ASA-4-338204: Dynamic Filter _dropped__protocol__in\_interface__src\_ip\_addr__src\_port__mapped-ip__mapped-port__out\_interface__dest\_ip\_addr__dest\_port__mapped-ip__mapped-port__malicious address__local or dynamic__domain name_ _level\_value__category\_name_
    
-   %ASA-4-338301: Intercepted DNS reply for name _name__in\_interface__src\_ip\_addr__src\_port__out\_interface__dest\_ip\_addr__dest\_port__list_
    
-   %ASA-4-4000nn: IPS:number string from IP\_address to IP\_address on interface interface\_name
    
-   %ASA-4-401001: Shuns cleared
    
-   %ASA-4-401002: Shun added: _IP\_address__IP\_address__port_ _port_
    
-   %ASA-4-401003: Shun deleted: _IP\_address_
    
-   %ASA-4-401004: Shunned packet: _IP\_address__IP\_address__interface\_name_
    
-   %ASA-4-401005: Shun add failed: unable to allocate resources for _IP\_address_ _IP\_address_ _port__port_
    
-   %ASA-4-402114: IPSEC: Received an _protocol__spi__seq\_num__remote\_IP__local\_IP_
    
-   %ASA-4-402115: IPSEC: Received a packet from _remote\_IP__local\_IP__act\_prot__exp\_prot_
    
-   %ASA-4-402116: IPSEC: Received an _protocol_ packet (SPI= _spi_, sequence number= _seq\_num_) from _remote\_ip_ (user= _username_) to _local\_ip_. The decapsulated inner packet doesn't match the negotiated policy in the SA. The packet specifies its destination as _pkt\_daddr_, its source as _pkt\_saddr_, and its protocol as _pkt\_prot_. The SA specifies its local proxy as _id\_daddr_/_id\_dmask_/_id\_dprot_/_id\_dport_ and its remote\_proxy as _id\_saddr_/_id\_smask_/_id\_sprot_/_id\_sport_.
    
-   %ASA-4-402117: IPSEC: Received a non-IPSec packet (protocol= _protocol__remote\_IP__local\_IP_
    
-   %ASA-4-402118: IPSEC: Received an _protocol__spi__seq\_num__remote\_IP__username__local\_IP__frag\_len__frag\_offset_
    
-   %ASA-4-402119: IPSEC: Received an _protocol__spi__seq\_num__remote\_IP__username__local\_IP_
    
-   %ASA-4-402120: IPSEC: Received an _protocol__spi__seq\_num__remote\_IP__username__local\_IP_
    
-   %ASA-4-402121: IPSEC: Received an _protocol__spi__seq\_num__peer\_addr__username__lcl\_addr__drop\_reason_
    
-   %ASA-4-402122: IPSEC: Received a cleartext packet from _src\_addr__dest\_addr__drop\_reason_
    
-   %ASA-4-402123: CRYPTO: The _accel\_type__eror\_type__error\_string__command name__command_
    
-   %ASA-4-402124: CRYPTO: The _platform_ hardware accelerator encountered an error (HWErrAddr= 0x_error\_address_, Core= _error\_core_, HwErrCode= _error\_code_, IstatReg= 0x_Istat_, PciErrReg= 0x_PCI_, CoreErrStat= 0x_core\_error\_stat_, CoreErrAddr= 0x_core\_err\_address_, Doorbell Size\[0\]= _size_, DoorBell Outstanding\[0\]= _outstanding_, Doorbell Size\[1\]= _size_, DoorBell Outstanding\[1\]= _outstanding_, SWReset= _Reset\_code_)
    
-   %ASA-4-402124: CRYPTO: The _platform_ hardware accelerator encountered an error (HWErrAddr= 0x_error\_address_, Core= _error\_core_, HwErrCode= _error\_code_, Queue= _queue\_string_ (_0_), IstatReg= 0x_Istat_, Station= _core\_station_, CoreRptr= 0x_core\_pointer_, CoreConfig= 0x_core\_config\_pointer_, SWReset= _Reset\_code_)
    
-   %ASA-4-402125: The _platform_ hardware accelerator _ring\_string_ ring timed out (Desc= 0x_descriptor\_address_, CtrlStat= 0x_control\_or\_status value_, ResultP= 0x_success\_pointer_, ResultVal= _success\_value_, Cmd= 0x_crypto\_command_, CmdSize= _command\_size_, Param= 0x_command\_parameters_, Dlen= _Data\_length_, DataP= 0x_Data\_pointer_, CtxtP= 0x_VPN\_context\_pointer_, SWReset= _reset\_number_)
    
-   %ASA-4-402126: CRYPTO: The _platform__Archive Filename__Cisco_
    
-   %ASA-4-402127: CRYPTO: The _platform__max\_number__archive\_directory__Archive Directory_
    
-   %ASA-4-402131: CRYPTO: _status__accel\_instance__old\_config\_bias__new\_config\_bias_
    
-   %ASA-4-403101: PPTP session state not established, but received an XGRE packet, tunnel\_id=_number__number_
    
-   %ASA-4-403102: PPP virtual interface _interface\_name__protocol__reason_
    
-   %ASA-4-403103: PPP virtual interface max connections reached
    
-   %ASA-4-403104: PPP virtual interface _interface\_name_
    
-   %ASA-4-403106: PPP virtual interface _interface\_name_
    
-   %ASA-4-403107: PPP virtual interface _interface\_name_
    
-   %ASA-4-403108: PPP virtual interface _interface\_name_
    
-   %ASA-4-403109: Rec'd packet not a PPTP packet.\\n\\t(ip) dest\_addr= _ip__dest\_address__source\_address_
    
-   %ASA-4-403110: PPP virtual interface _interface\_name__user_
    
-   %ASA-4-403505: _PPPoE__IP\_address__interface\_name__interface_
    
-   %ASA-4-403506: _PPPoE__IP\_address__netmask___interface_ _interface\_name__
    
-   %ASA-4-405001: Received ARP _{request | response}_ collision from _ip\_address_/_MAC\_address_ on interface _interface\_name_ with existing ARP entry _ip\_address_/_MAC\_address_
    
-   %ASA-4-405002: Received mac mismatch packet from _IP\_address_/{_MAC\_bytes|MAC\_address_} for authenticated host
    
-   %ASA-4-405003: IP address collision detected between host IP\_address at MAC\_address and interface interface\_name, MAC\_address.
    
-   %ASA-4-405101: Unable to Pre-allocate H225 Call Signalling Connection for faddr _foreign\_ip\_address_ to laddr _local\_ip\_address_/_local\_port_
    
-   %ASA-4-405101: Unable to Pre-allocate H225 Call Signalling Connection for faddr _foreign\_ip\_address_/_foreign\_port_ to laddr _local\_ip\_address_
    
-   %ASA-4-405102: Unable to Pre-allocate H245 Connection for faddr _foreign\_ip\_address_ to laddr _local\_ip\_address_/_local\_port_
    
-   %ASA-4-405102: Unable to Pre-allocate H245 Connection for faddr _foreign\_ip\_address_/_foreign\_port_ to laddr _local\_ip\_address_
    
-   %ASA-4-405103: H225 message from _source\_address__source\_port__dest\_address__dest\_port__hex_
    
-   %ASA-4-405104: H225 message _string__outside\_address__outside\_port__inside\_address__inside\_port_
    
-   %ASA-4-405105: H323 RAS message AdmissionConfirm received from _source\_address__source\_port__dest\_address__dest\_port_
    
-   %ASA-4-405106: H323 num channel is not created from %I/%d to %I/%d %s
    
-   %ASA-4-405107: H245 Tunnel is detected and connection dropped from %I/%d to %I/%d %s
    
-   %ASA-4-405201: ILS _ILS\_message\_type__inside\_interface__source\_IP\_address__port__outside\_interface__destination\_IP\_address__port__embedded\_IP\_address_
    
-   %ASA-4-405300: Radius Accounting Request received from _from\_addr_
    
-   %ASA-4-405301: Attribute _attribute\_number__user\_ip_
    
-   %ASA-4-406001: FTP port command low port: _IP\_address__port__IP\_address__interface\_name_
    
-   %ASA-4-406002: FTP port command different address: _IP\_address__IP\_address__IP\_address__interface\_name_
    
-   %ASA-4-407001: Deny traffic for local-host _interface\_name__inside\_address__number_
    
-   %ASA-4-407002: Embryonic limit for through connections exceeded _nconns__elimit__outside\_address__outside\_port__global\_address__inside\_address__inside\_port__interface\_name_
    
-   %ASA-4-407003: Established limit for RPC services exceeded
    
-   %ASA-4-408001: IP route counter negative
    
-   %ASA-4-408101: KEYMAN : Type <encrption\_type> encryption unknown. Interpreting keystring as literal.
    
-   %ASA-4-408102: KEYMAN : Bad encrypted keystring for key id <key id>
    

-   %ASA-4-409014: No valid authentication \[send\] key is available on interface <nameif>
    
-   %ASA-4-409015: Key ID <key-id> <received> on interface <nameif>
    
-   %ASA-4-409016: Key chain name <key-chain-name> on <nameif>  is invalid
    
-   %ASA-4-409017: Key ID <key-id> in key chain <key-chain-name> is invalid.
    
-   %ASA-4-409023: Attempting AAA Fallback method _method\_name__request\_type__user__Auth-server_
    
-   %ASA-4-410001: Dropped UDP DNS _request__source\_interface__source\_address__source\_port__dest\_interface__dest\_address__dest\_port__label | domain-name_ _number__remaining packet length__number_
    
-   %ASA-4-410003: _action\_class__action__query\_response__src\_ifc__sip__sport__dest\_ifc__dip__dport_
    
-   %ASA-4-411001: Line protocol on Interface _interface\_name_
    
-   %ASA-4-411002: Line protocol on Interface _interface\_name_
    
-   %ASA-4-411003: Interface _interface\_name_
    
-   %ASA-4-411004: Interface _interface\_name_
    
-   %ASA-4-411005: Interface _variable 1_
    
-   %ASA-4-412001: MAC _MAC\_address__interface\_1__interface\_2_
    
-   %ASA-4-412002: Detected bridge table full while inserting MAC _MAC\_address__interface__num_
    
-   %ASA-4-413001: Module _module\_id__errnum__message_
    
-   %ASA-4-413002: Module _module\_id__errnum_ _message_
    
-   %ASA-4-413003: Module _string one_
    
-   %ASA-4-413004: Module in slot _string one__newver__ver__reason_
    
-   %ASA-4-413005: Module _module\_id__app\_name__app\_vers__app\_type_
    
-   %ASA-4-413006: _prod-id__slot__prod-id__running-vers__slot__prod-id__required-vers_
    
-   %ASA-4-413009: _<internal interface>_
    
-   %ASA-4-415016: policy-map _map\_name__connection\_action__int\_type__IP\_address__port\_num__int\_type__IP\_address__port\_num_
    
-   %ASA-4-416001: Dropped UDP SNMP packet from _source\_interface__source\_IP__source\_port__dest\_interface__dest\_address__dest\_port__prot\_version_
    
-   %ASA-4-417001: Unexpected event received: _number_
    
-   %ASA-4-417004: Filter violation error: conn _number_ (_string_:_string_) in _string_
    
-   %ASA-4-417006: No memory for _string_ in _string_ (warning)
    
-   %ASA-4-418001: Through-the-device packet to/from management-only network is denied: _protocol\_string_
    
-   %ASA-4-419001: Dropping TCP packet from _src\_ifc__src\_IP__src\_port__dest\_ifc__dest\_IP__dest\_port__reason__size__size_
    
-   %ASA-4-419002: Duplicate TCP SYN from _in\_interface__src\_address__src\_port__out\_interface__dest\_address__dest\_port_
    
-   %ASA-4-419003: Cleared TCP urgent flag from _out\_ifc_:_src\_ip_/_src\_port_ to _in\_ifc_:_dest\_ip_/_dest\_port_
    
-   %ASA-4-420002: IPS requested to drop _ICMP__ifc\_in__SIP__port__ifc\_out__DIP__port_
    
-   %ASA-4-420003: IPS requested to reset TCP connection from _ifc\_in__SIP__SPORT__ifc\_out__DIP__DPORT_
    
-   %ASA-4-420007: _application-string__slot\_id__slot\_id_
    
-   %ASA-4-422004: IP SLA Monitor number0: Duplicate event received. Event number number1
    
-   %ASA-4-422005: IP SLA Monitor Probe(s) could not be scheduled because clock is not set.
    
-   %ASA-4-422006: IP SLA Monitor Probe number: string
    
-   %ASA-4-423001: _{Allowed | Dropped}__pkt\_type\_name__error\_reason\_str__ifc\_name__ip\_address__port__ifc\_name__ip\_address__port_
    
-   %ASA-4-423002: _{Allowed | Dropped}__pkt\_type\_name__error\_reason\_str__ifc\_name__ip\_address__port__ifc\_name__ip\_address__port_
    
-   %ASA-4-423003: _{Allowed | Dropped}__pkt\_type\_name__error\_reason\_str__ifc\_name__ip\_address__port__ifc\_name__ip\_address__port_
    
-   %ASA-4-423004: _{Allowed | Dropped}__pkt\_type\_name__error\_reason\_str__ifc\_name__ip\_address__port__ifc\_name__ip\_address__port_
    
-   %ASA-4-423005: _{Allowed | Dropped}__pkt\_type\_name__error\_reason\_str__ifc\_name__ip\_address__port__ifc\_name__ip\_address__port_
    
-   %ASA-4-424001: Packet denied: _protocol\_string__intf\_in_
    
-   %ASA-4-424002: Connection to the backup interface is denied: _protocol\_string_
    
-   %ASA-4-426004: PORT-CHANNEL:Interface _ifc\_name1__ifc\_name__speed of__ifc\_name1_ _X Mbps__Y__1000 Mbps_
    
-   %ASA-4-429002: CX requested to drop _protocol__interface\_name__ip\_address__port__interface\_name__ip\_address__port_
    
-   %ASA-4-429003: CX requested to reset TCP connection from _interface\_name__ip\_addr__port__interface\_name__ip\_addr__port_
    
-   %ASA-4-429007: CXSC redirect will override Scansafe redirect for flow from _interface\_name_:_ip\_address_/_port_ to _interface\_name_:_ip\_address_/_port_ \[(_username_)\]
    
-   %ASA-4-429008: Unable to respond to VPN query from CX for session 0x%x. Reason %s
    
-   %ASA-4-431001: RTP conformance: Dropping RTP packet from _in\_ifc_:_src\_ip_/_src\_port_ to _out\_ifc_:_dest\_ip_/_dest\_port_, Drop reason: _drop\_reason_ _value_
    
-   %ASA-4-431002: RTCP conformance: Dropping RTCP packet from _in\_ifc_:_src\_ip_/_src\_port_ to _out\_ifc_:_dest\_ip_/_dest\_port_, Drop reason: _drop\_reason_ _value_
    
-   %ASA-4-434001: SFR card not up and fail-close mode used, dropping _protocol__ingress__source__IP address__source port__egress interface__destination IP address_
    
-   %ASA-4-434002: SFR requested to drop _protocol__ingress interface__source IP address__source port__egress interface__destination IP address__destination port_
    
-   %ASA-4-434003: SFR requested to reset TCP connection from _ingress interface__source IP address__source port_ _egress__interface__destination IP address_
    
-   %ASA-4-434007: SFR redirect will override Scansafe redirect for flow from _inside\_interface_:_source\_ip\_address_/_source\_port_ to _outside\_interface_:_destination\_IP\_address_/_destination\_port_ \[(_user_)\]
    
-   %ASA-4-444005: Timebased license key _xxx__xxx__xxx__xxx__xxx__num_
    
-   % ASA-4-444008: <i>license-type</i> license has expired, and the system is scheduled to reload in <i>number</i> days. Apply a new activation key to enable <i>license-type</i> license and prevent the automatic reload.
    
-   %ASA-4-444106: Shared license backup server _address_
    
-   %ASA-4-444109: Shared license backup server role change to _state_
    
-   %ASA-4-444110: Shared license server backup has _days_
    
-   %ASA-4-444304: %SMART\_LIC-4-IN\_OVERAGE: One or more entitlements are in overage.
    
-   %ASA-4-446001: Maximum TLS Proxy session limit of _max\_sess_
    
-   %ASA-4-446003: Denied TLS Proxy session from src\_int:src\_ip/src\_port to dst\_int:dst\_ip/dst\_port, UC-IME license is disabled.
    
-   %ASA-4-447001: ASP DP to CP _queue\_name_ was full. Queue length _length_, limit _limit_
    
-   %ASA-4-448001: Denied SRTP crypto session setup on flow from _src\_int__src\_ip__src\_port__dst\_int__dst\_ip__dst\_port__limit_
    
-   %ASA-4-450001: Deny traffic for protocol protocol\_id src interface\_name:IP\_address/port dst interface\_name:IP\_address/port, licensed host limit of num exceeded.
    
-   %ASA-4-450002: Teardown _string_ connection _connection_ for _interface_:_address_/_port_ to _interface_:_address_/_port_ duration _hh:mm:ss_ bytes _bytes_ reason _reason\_string_
    
-   %ASA-4-500004: Invalid transport field for protocol=_protocol__source\_address__source\_port__dest\_address__dest\_port_
    
-   %ASA-4-500006: For flow _inside_:_IP Address_/_port_ to _outside_:_IP Address_/_port_ :_existing flow message_:_connection id_
    
-   %ASA-4-507002: Data copy in proxy-mode exceeded the buffer limit
    
-   %ASA-4-603110: Failed to establish L2TP session, tunnel\_id = _tunnel\_id__peer\_ip__username_
    
-   %ASA-4-604105: Unable to send DHCP reply to client _hardware\_address__interface\_name__options\_field\_size__number\_of\_octets_
    
-   %ASA-4-607002: _action\_class__action__req\_resp__req\_resp\_info__src\_ifc__sip__sport__dest\_ifc__dip__dport_
    
-   %ASA-4-607004: Phone Proxy: Dropping SIP message from _src\_if__src\_ip__src\_port__dest\_if__dest\_ip__dest\_port__mac\_address_
    
-   %ASA-4-608002: Dropping Skinny message for _in\_ifc__src\_ip__src\_port__out\_ifc__dest\_ip__dest\_port__value_
    
-   %ASA-4-608003: Dropping Skinny message for _in\_ifc__src\_ip__src\_port__out\_ifc__dest\_ip__dest\_port__value_
    
-   %ASA-4-608004: Dropping Skinny message for _in\_ifc__src\_ip__src\_port__out\_ifc__dest\_ip__dest\_port__value_
    
-   %ASA-4-608005: Dropping Skinny message for _in\_ifc__src\_ip__src\_port__out\_ifc__dest\_ip__dest\_port__value_
    
-   %ASA-4-612002: Auto Update failed: _filename__number__reason_
    
-   %ASA-4-612003: Auto Update failed to contact: _url__reason_
    
-   %ASA-4-613017: Bad LSA mask: Type number, LSID IP\_address Mask mask from IP\_address
    
-   %ASA-4-613018: Maximum number of non self-generated LSA has been exceeded “OSPF number” - number LSAs
    
-   %ASA-4-613019: Threshold for maximum number of non self-generated LSA has been reached "OSPF number" - number LSAs
    
-   %ASA-4-613021: Packet not written to the output queue
    
-   %ASA-4-613022: Doubly linked list linkage is NULL
    
-   %ASA-4-613023: Doubly linked list prev linkage is NULL number
    
-   %ASA-4-613024: Unrecognized timer number in OSPF string
    
-   %ASA-4-613025: Invalid build flag number for LSA IP\_address, type number
    
-   %ASA-4-613026: Can not allocate memory for area structure
    
-   %ASA-4-613030: Router is currently an ASBR while having only one area which is a stub area
    
-   %ASA-4-613031: No IP address for interface inside
    
-   %ASA-4-613036: Can not use configured neighbor: cost and database-filter options are allowed only for a point-to-multipoint network
    
-   %ASA-4-613037: Can not use configured neighbor: poll and priority options are allowed only for a NBMA network
    
-   %ASA-4-613038: Can not use configured neighbor: cost or database-filter option is required for point-to-multipoint broadcast network
    
-   %ASA-4-613039: Can not use configured neighbor: neighbor command is allowed only on NBMA and point-to-multipoint networks
    
-   %ASA-4-613040: OSPF-1 Area string: Router IP\_address originating invalid type number LSA, ID IP\_address, Metric number on Link ID IP\_address Link Type number
    
-   %ASA-4-613042: OSPF process number lacks forwarding address for type 7 LSA IP\_address in NSSA string - P-bit cleared
    
-   %ASA-4-620002: Drop CTIQBE packet from _interface\_name_:_ip\_address_/_port_ to _interface\_name_:_ip\_address_/_port_ Reason: _reason\_string_
    
-   %ASA-4-709008: (Primary | Secondary) Configuration sync in progress. Command: ‘command’ executed from (terminal/http) will not be replicated to or executed by the standby unit.
    
-   %ASA-4-709013: Failover configuration replication hash comparison timeout expired _failover\_state_
    
-   %ASA-4-711002: Task ran for _elapsed\_time__process\_name__PC__traceback_
    
-   %ASA-4-711004: Task ran for _msec__process\_name__pc__call stack_
    
-   %ASA-4-713154: DNS lookup for _peer\_description_ Server \[_server\_name_ \] failed!
    
-   %ASA-4-713157: IP = _peerIP_ Timed out on initial contact to server \[_server\_name_ or _IP\_address_ \] Tunnel could not be established.
    
-   %ASA-4-713207: Group = _groupname_, Username = _username_, IP = _peerIP_ Terminating connection: IKE Initiator and tunnel group specifies L2TP Over IPSec
    
-   %ASA-4-713241: IE Browser Proxy Method setting\_number is Invalid
    
-   %ASA-4-713242: Group = _groupname_, Username = _username_, IP = _peerIP_ Remote user is authenticated using Hybrid Authentication. Not starting IKE rekey.
    
-   %ASA-4-713243: _META-DATA_ Unable to find the requested certificate
    
-   %ASA-4-713244: Group = _groupname_, Username = _username_, IP = _peerIP_ _META-DATA_ Received Legacy Authentication Method(LAM) type _type_ is different from the last type received _type_ .
    
-   %ASA-4-713245: Group = _groupname_, Username = _username_, IP = _peerIP_ _META-DATA_ Unknown Legacy Authentication Method(LAM) type _type_ received.
    
-   %ASA-4-713246: Group = _groupname_, Username = _username_, IP = _peerIP_ _META-DATA_ Unknown Legacy Authentication Method(LAM) attribute type _type_ received.
    
-   %ASA-4-713247: Group = _groupname_, Username = _username_, IP = _peerIP_ _META-DATA_ Unexpected error: in Next Card Code mode while not doing SDI.
    
-   %ASA-5-713248: Group = _groupname_, Username = _username_, IP = _peerIP_ _META-DATA_ Rekey initiation is being disabled during CRACK authentication.
    
-   %ASA-4-713249: Group = _groupname_, Username = _username_, IP = _peerIP_ _META-DATA_ Received unsupported authentication results: _result_
    
-   %ASA-4-713251: Group = _groupname_, Username = _username_, IP = _peerIP_ _META-DATA_ Received authentication failure message
    
-   %ASA-4-713255: IP = _peer-IP_ IP = _peer-IP_, Received ISAKMP Aggressive Mode message 1 with unknown tunnel group name _group-name_
    
-   %ASA-4-713261: IPV6 address on output interface _interface\_number_ was not found
    
-   %ASA-4-713903: Group = group policy, Username = user name, IP = remote IP, ERROR: Failed to install Redirect URL: redirect URL Redirect ACL: non\_exist for assigned IP.
    
-   %ASA-4-716007: Group _group__user__IP_
    
-   %ASA-4-716022: Unable to connect to proxy server _reason_
    
-   %ASA-4-716023: Group _name__user__ip__maximum\_sessions_
    
-   %ASA-4-716044: Group _group-name__user-name__IP\_address__param-name__param-value_
    
-   %ASA-4-716045: Group _group-name__user-name__IP\_address__param-name_
    
-   %ASA-4-716046: Group _group-name__user-name__IP\_address__access-list-name_
    
-   %ASA-4-716047: Group _group-name__user-name__IP\_address__access-list-name_
    
-   %ASA-4-716048: Group _group-name__user-name__IP\_address_
    
-   %ASA-4-716052: Group _group-name__user-name__IP\_address_
    
-   %ASA-4-716165: SAML assertion cannot be replay protected because it does not contain time constraints
    
-   %ASA-4-717026: Name lookup failed for hostname _hostname_
    
-   %ASA-4-717031: Failed to find a suitable trustpoint for the issuer: issuer Reason: reason\_string
    
-   %ASA-4-717035: OCSP status is being checked for certificate. _certificate\_identifier._
    
-   %ASA-4-717037: Tunnel group search using certificate maps failed for peer certificate: _certificate\_identifier_
    
-   %ASA-4-717052: Group _group name__user name__IP Address__id subject name__id issuer name__id serial number_
    
-   %ASA-4-720001: (VPN-unit) Failed to initialize with Chunk Manager.
    
-   %ASA-4-720007: (VPN-unit) Failed to allocate chunk from Chunk Manager.
    
-   %ASA-4-720008: (VPN-unit) Failed to register to High Availability Framework.
    
-   %ASA-4-720009: (VPN-unit) Failed to create version control block.
    
-   %ASA-4-720011: (VPN-unit) Failed to allocate memory
    
-   %ASA-4-720013: (VPN-unit) Failed to insert certificate in trust point trustpoint\_name
    
-   %ASA-4-720022: (VPN-unit) Cannot find trust point trustpoint
    
-   %ASA-4-720033: (VPN-unit) Failed to queue add to message queue.
    
-   %ASA-4-720038: (VPN-unit) Corrupted message from active unit.
    
-   %ASA-4-720043: (VPN-unit) Failed to send type message id to standby unit
    
-   %ASA-4-720044: (VPN-unit) Failed to receive message from active unit
    
-   %ASA-4-720047: (VPN-unit) Failed to sync SDI node secret file for server IP\_address on the standby unit.
    
-   %ASA-4-720051: (VPN-unit) Failed to add new SDI node secret file for server id on the standby unit.
    
-   %ASA-4-720052: (VPN-unit) Failed to delete SDI node secret file for server id on the standby unit.
    
-   %ASA-4-720053: (VPN-unit) Failed to add cTCP IKE rule during bulk sync, peer=IP\_address, port=port
    
-   %ASA-4-720054: (VPN-unit) Failed to add new cTCP record, peer=IP\_address, port=port.
    
-   %ASA-4-720055: (VPN-unit) VPN Stateful failover can only be run in single/non-transparent mode.
    
-   %ASA-4-720064: (VPN-unit) Failed to update cTCP database record for peer=IP\_address, port=port during bulk sync.
    
-   %ASA-4-720065: (VPN-unit) Failed to add new cTCP IKE rule, peer=peer, port=port.
    
-   %ASA-4-720066: (VPN-unit) Failed to activate IKE database.
    
-   %ASA-4-720067: (VPN-unit) Failed to deactivate IKE database.
    
-   %ASA-4-720068: (VPN-unit) Failed to parse peer message.
    
-   %ASA-4-720069: (VPN-unit) Failed to activate cTCP database.
    
-   %ASA-4-720070: (VPN-unit) Failed to deactivate cTCP database.
    
-   %ASA-4-720073: VPN Session failed to replicate - ACL acl\_name not found
    
-   %ASA-4-721007: (device) Fail to update access list list\_name on standby unit.
    
-   %ASA-4-721011: (device) Fail to add access list rule list\_name, line line\_no on standby unit.
    
-   %ASA-4-721013: (device) Fail to enable APCF XML file file\_name on the standby unit.
    
-   %ASA-4-721015: (device) Fail to disable APCF XML file file\_name on the standby unit.
    
-   %ASA-4-721017: (device) Fail to create WebVPN session for user user\_name, IP ip\_address.
    
-   %ASA-4-721019: (device) Fail to delete WebVPN session for client user user\_name, IP ip\_address.
    
-   %ASA-4-722001: IP _IP\_address_
    
-   %ASA-4-722002: IP _IP\_address_
    
-   %ASA-4-722003: IP _IP\_address_
    
-   %ASA-4-722004: Group _group__user-name__IP\_address_
    
-   %ASA-4-722015: Group _group__user-name__IP\_address__type-num_
    
-   %ASA-4-722016: Group _group__user-name__IP\_address__length__expected-length_
    
-   %ASA-4-722017: Group _group__user-name__ip\_address__xx__xx__xx__xx_
    
-   %ASA-4-722018: Group _group__user-name__IP\_address__version__expected_
    
-   %ASA-4-722019: Group _group__user-name__IP\_address__length_
    
-   %ASA-4-722039: Group _group__user__ip__acl_
    
-   %ASA-4-722040: Group _group__user__ip__acl_
    
-   %ASA-4-722041: TunnelGroup _tunnel\_group__group\_policy__username__peer\_address_
    
-   %ASA-4-722042: Group _group__user__ip__Cisco_
    
-   %ASA-4-722047: Group _group__user__ip__ASA_
    
-   %ASA-4-722048: Group _group__user__ip_
    
-   %ASA-4-722049: Group _group__user__ip__ASA_
    
-   %ASA-4-722050: Group group User user IP ip Session terminated: SVC not enabled for the user.
    
-   %ASA-4-722054: Group _group policy__user name__remote IP__redirect URL__non\_exist__assigned IP_
    
-   %ASA-4-722057: Group _group policy_ User _username_ IP _client IP_ SVC terminating connection: Failed to bind SGT _tag_ with assigned IP: _assigned IP_.
    
-   %ASA-4-724001: Group _group-name__user-name__IP\_address_
    
-   %ASA-4-724002: Group _group-name__user-name__IP\_address_
    
-   %ASA-4-733100: \[_Object__rate\_ID__rate\_val__rate\_val__rate\_val__rate\_val__total\_cnt_
    
-   %ASA-4-733101: _Object objectIP__rate\_val__rate\_val__rate\_val__rate\_val__total\_cnt._
    
-   %ASA-4-733102: Threat-detection adds host _host_
    
-   %ASA-4-733103: Threat-detection removes host _host_
    
-   %ASA-4-733104: TCP Intercept SYN flood attack detected to _host\_ip_/_host\_port_ (_real\_ip_/_real\_port_). Average rate of _avg\_rate_ SYNs/sec exceeded the threshold of _threshold\_rate_.
    
-   %ASA-4-733105: TCP Intercept SYN flood attack detected to _host\_ip_/_host\_port_ (_real\_ip_/_real\_port_). Burst rate of _burst\_rate_ SYNs/sec exceeded the threshold of _threshold\_rate_.
    
-   (For IKEv2 connection requests) %ASA-4-733201: Threat-detection: Service\[_remote-access-client-initiations_\] Peer\[_peer-ip_\]: failure threshold of _threshold-value_ exceeded: adding shun to interface _interface_. _IKEv2: RA excessive client initiation requests_
    
-   (For SSL connection requests) %ASA\-4-733201: Threat-detection: Service\[remote-access-client-initiations\] Peer\[_peer_\-_ip_\]: failure threshold of _value_ exceeded: adding shun to interface _interface_. SSL: RA excessive client initiation requests.
    
-   %ASA-4-735015: CPU _var1__var2__var3_
    
-   %ASA-4-735016: Chassis Ambient _var1__var2__var3_
    
-   %ASA-4-735018: Power Supply _var1__var2__var3_
    
-   %ASA-4-735019: Power Supply _var1__var2__var3_
    
-   %ASA-4-735026: IO Hub _var1__var2__var3_
    
-   %ASA-4-737012: IPAA: Session=_session_
    
-   %ASA-4-737013: IPAA: Session=_session__ip-address_
    
-   %ASA-4-737019: IPAA: Session=_session_
    
-   %ASA-4-737028: IPAA: Session= _session_
    
-   %ASA-4-737030: IPAA: Session=_session_, Unable to send {_ip\_address | ipv6\_address_} to standby: address in use
    
-   %ASA-4-737032: IPAA: Session= _session_
    
-   %ASA-4-737033: IPAA: Session= _session__addr\_allocator__ip\_addr_
    
-   %ASA-4-737038: IPAA: Session=session, specified address ip-address was in-use, trying to get another.
    
-   % ASA-4-737203: VPNFIP: Pool=<i>pool</i>, WARN: <i>message</i>
    
-   % ASA-4-737402: POOLIP: Pool=<i>pool</i>, Failed to return <i>ip-address</i> to pool (recycle=<i>recycle</i>). Reason: <i>message</i>
    
-   % ASA-4-737404: POOLIP: POOLIP: Pool=<i>pool</i>, WARN: <i>message</i>
    
-   %ASA-4-741005: Coredump operation '_variable 1_ _variable 2 variable 3_
    
-   %ASA-4-741006: Unable to write Coredump Helper configuration, reason _variable 1_
    
-   %ASA-4-746004: user-identity: Total number of activated user groups exceeds the maximum number of _max\_groups_
    
-   %ASA-4-746006: user-identity: Out of sync with AD Agent, start bulk download
    
-   %ASA-4-746011: user-identity: Total number of users created exceeds the maximum number of _max\_users_
    
-   %ASA-4-747008: Clustering: New cluster member name with serial number serial-number-A rejected due to name conflict with existing unit with serial number serial-number-B.
    
-   %ASA-4-747015: Clustering: Forcing stray member unit-name to leave the cluster.
    
-   %ASA-4-747016: Clustering: Found a split cluster with both unit-name-A and unit-name-B as master units. Master role retained by unit-name-A, unit-name-B will leave, then join as a slave.
    
-   %ASA-4-747017: Clustering: Failed to enroll unit unit-name due to maximum member limit limit-value reached.
    
-   %ASA-4-747019: Clustering: New cluster member name rejected due to Cluster Control Link IP subnet mismatch (ip-address/ip-mask on new unit, ip-address/ip-mask on local unit).
    
-   %ASA-4-747020: Clustering: New cluster member unit-name rejected due to encryption license mismatch.
    
-   %ASA-4-747025: Clustering: New cluster member unit-name rejected due to firewall mode mismatch.
    
-   %ASA-4-747026: Clustering: New cluster member unit-name rejected due to cluster interface name mismatch (ifc-name on new unit, ifc-name on local unit).
    
-   %ASA-4-747027: Clustering: Failed to enroll unit unit-name due to insufficient size of cluster pool pool-name in context-name.
    
-   %ASA-4-747028: Clustering: New cluster member unit-name rejected due to interface mode mismatch (mode-name on new unit, mode-name on local unit).
    
-   %ASA-4-747029: Clustering: Unit unit-name is quitting due to Cluster Control Link down.
    
-   %ASA-4-747034: Unit %s is quitting due to Cluster Control Link down (%d times after last rejoin). Rejoin will be attempted after %d minutes.
    
-   %ASA-4-747035: Unit %s is quitting due to Cluster Control Link down. Clustering must be manually enabled on the unit to rejoin.
    
-   %ASA-4-748002: Clustering configuration on the chassis is missing or incomplete; clustering is disabled.
    
-   %ASA-4-748003: Module slot\_number in chassis chassis\_number is leaving the cluster due to a chassis health check failure
    
-   %ASA-4-748201: <Application name> application on module <module id> in chassis <chassis id> is <status>.
    
-   %ASA-4-750003: Local: _local IP:local port_ Remote: _remote IP:remote port_ Username: _username_ Negotiation aborted due to ERROR: _error_
    
-   %ASA-4-750012: Selected IKEv2 encryption algorithm (_IKEV2 encry algo_ ) is not strong enough to secure proposed IPSEC encryption algorithm (_IPSEC encry algo_ ).
    
-   %ASA-4-750014: Local:_self ip_:_self port_ Remote:_peer ip_:_peer port_ Username:_TG or Username_ IKEv2 Session aborted. Reason: Initial Contact received for Local ID: _self ID_, Remote ID: _peer ID_ from remote peer:_peer ip_:_peer port_ to _self ip_:_self port_
    
-   %ASA-4-750015: Local:_self ip_:_self port_ Remote:_peer ip_:_peer port_ Username:_TG or Username_ deleting IPSec SA. Reason: invalid SPI notification received for SPI 0x_SPI_; local traffic selector = Address Range: _start address_\-_end address_ Protocol: _protocol number_ Port Range: _start port_\-_end port_ ; remote traffic selector = Address Range: _start address_\-_end address_ Protocol: _protocol number_ Port Range: _start port_\-_end port_
    
-   %ASA-4-751014: Warning Configuration Payload request for attribute _attribute\_id_ could not be processed. Error: _error_
    
-   %ASA-4-751015: SA request rejected by CAC. Reason: _reason_
    
-   %ASA-4-751016: Remote L2L Peer initiated a tunnel with same outer and inner addresses. Peer could be Originate Only - Possible misconfiguration!
    
-   %ASA-4-751019: Failed to obtain an _licenseType_ license. Maximum license limit _limit_ exceeded.
    
-   %ASA-4-751021: _variable\_1 variable\_2_ with _variable\_3_ encryption is not supported with this version of the AnyConnect Client. Please upgrade to the latest Anyconnect Client.
    
-   %ASA-4-751027: Local:local IP:local port Remote:peer IP:peer port Username:username IKEv2 Received INVALID\_SELECTORS Notification from peer. Peer received a packet (SPI=spi). The decapsulated inner packet didn’t match the negotiated policy in the SA. Packet destination pkt\_daddr, port pkt\_dest\_port, source pkt\_saddr, port pkt\_src\_port, protocol pkt\_prot.
    
-   %ASA-4-752009: IKEv2 Doesn't support Multiple Peers
    
-   %ASA-4-752010: IKEv2 Doesn't have a proposal specified
    
-   %ASA-4-752011: IKEv1 Doesn't have a transform set specified
    
-   %ASA-4-752012: IKEv _protocol_ was unsuccessful at setting up a tunnel. Map Tag = _mapTag_ . Map Sequence Number = _mapSeq_ .
    
-   %ASA-4-752013: Tunnel Manager dispatching a KEY\_ACQUIRE message to IKEv2 after a failed attempt. Map Tag = _mapTag_ . Map Sequence Number = _mapSeq_ .
    
-   %ASA-4-752014: Tunnel Manager dispatching a KEY\_ACQUIRE message to IKEv1 after a failed attempt. Map Tag = _mapTag_ . Map Sequence Number = _mapSeq_ .
    
-   %ASA-4-752017: IKEv2 Backup L2L tunnel initiation denied on interface _interface_ matching crypto map _name_, sequence number _number_ . Unsupported configuration.
    
-   %ASA-4-753001: Unexpected IKEv2 packet received from <IP>:<port>. Error: <reason>
    
-   %ASA-4-768003: SSH: connection timed out: username username, IP ip
    
-   %ASA-4-769009: UPDATE: Image booted _image\_name_ is different from boot images
    
-   %ASA-4-770001: _Resource__limit__ASA_
    
-   %ASA-4-770003: Resource resource allocation is less than the minimum requirement of value for this platform. If this condition persists, performance will be lower than normal.
    
-   %ASA-4-775002: Scansafe: _Reason__protocol_ _conn\_id_ _interface\_name__real\_address__real\_port_ _idfw\_user__interface\_name__real\_address__real\_port_ _action_
    
-   %ASA-4-775004: Scansafe: Primary server _server-name__ip\_address_
    
-   %ASA-4-776201: CTS Env: PAC for Server _IP\_address__PAC issuer name__number_
    
-   %ASA-4-776304: CTS Policy: Unresolved security-group name "_sgname_
    
-   %ASA-4-776305: CTS Policy: Security-group table cleared, all polices referencing security-group names will be deactivated
    
-   %ASA-4-776312: CTS Policy: Previously resolved security-group name "_sgname_
    
-   %ASA-4-802006: IP ip\_address MDM request details has been rejected: details.
    
-   %ASA-4-812005: Link-State-Propagation activated on inline-pair due to failure of interface <interface-name> bringing down pair interface <interface-name>
    
-   %ASA-4-812006: Link-State-Propagation de-activated on inline-pair due to recovery of interface <interface-name> bringing up pair interface <interface-name>
    
-   %ASA-4-815003: Object-Group-Search threshold exceeded <current value> threshold (10000) for packet UDP from <source IP address/port> to <destination IP address/port>
    
-   %ASA-4-861011: AVC: Loading app category definition file _file_ success.
    
-   %ASA-4-870001: policy-route path-monitoring, remote peer _interface\_name_:_IP\_Address_ _reachable\_status_.
    
-   %ASA-4-880002: Internal-Data no-buffer counter stats: _counter stats_
    

## Notification Messages, Severity 5

The following messages appear at severity 5, notifications:

-   %ASA-5-105500: (Primary|Secondary) Started HA
    
-   %ASA-5-105501: (Primary|Secondary) Stopping HA
    
-   %ASA-5-105503: (Primary|Secondary) Internal state changed from _previous\_state_ to _new\_state_
    
-   %ASA-5-105504: (Primary|Secondary) Connected to peer _peer-ip_:_port_
    
-   %ASA-5-105520: (Primary|Secondary) Responding to Azure Load Balancer probes
    
-   %ASA-5-105521: (Primary|Secondary) No longer responding to Azure Load Balancer probes
    
-   %ASA-5-105522: (Primary|Secondary) Updating route-table _route\_table\_name_
    
-   %ASA-5-105523: (Primary|Secondary) Updated route-table _route\_table\_name_
    
-   %ASA-5-105542: (Primary|Secondary) Enabling load balancer probe responses
    
-   %ASA-5-105543: (Primary|Secondary) Disabling load balancer probe responses
    
-   %ASA-5-105552: (Primary|Secondary) Stopped HA
    

-   %ASA-5-109012: Authen Session End: user '_user__number__number_
    
-   %ASA-5-109029: Parsing downloaded ACL: _string_
    
-   %ASA-5-109039: AAA Authentication: Dropping an unsupported IPv6/IP46/IP64 packet from _lifc__laddr__fifc__faddr_
    
-   %ASA-5-109201: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP Address_, Succeeded adding entry.
    
-   %ASA-5-109204: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP Address_, Succeeded applying filter.
    
-   %ASA-5-109207: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP Address_, Succeeded updating entry.
    
-   %ASA-5-109210: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP Address_, Succeeded removing entry.
    
-   %ASA-5-111001: Begin configuration: _IP\_address__device_
    
-   %ASA-5-111002: Begin configuration: _ip\_address_ reading from _device_
    
-   %ASA-5-111003: _IP\_address_
    
-   %ASA-5-111004: _IP\_address__{FAILED|OK}_
    
-   %ASA-5-111005: _IP\_address_
    
-   %ASA-5-111007: Begin configuration: _IP\_address__device_
    
-   %ASA-5-111008: User '_user__string_
    
-   %ASA-5-111010: User '_username__application-name__ip addr__cmd_
    
-   %ASA-5-113024: Group _tg__type__ip__user\_name_
    
-   %ASA-5-113025: Group _tg__fields_ _connection type__ip_
    
-   %ASA-5-120001: Call-Home Module started.
    
-   %ASA-5-120002: Call-Home Module terminated.
    
-   %ASA-5-120008: Call-Home client _client_
    
-   %ASA-5-120009: Call-Home client _client_
    
-   %ASA-5-120012: User "_username__choice_
    
-   %ASA-5-121001: _id_
    
-   %ASA-5-121002: _status._
    
-   %ASA-5-199001: Reloaded at _time_ by _user_. Reload reason: _reload reason_
    
-   %ASA-5-199017: syslog
    
-   %ASA-5-199027: Restore operation was aborted at _<HH:MM:SS> UTC <DD:MM:YY>_.
    
-   %ASA-5-212009: Configuration request for SNMP group _groupname__username__reason_
    
-   %ASA-5-303004: FTP _cmd\_string__source\_interface__source\_address__source\_port__dest\_interface__dest\_address__dest\_interface_
    
-   %ASA-5-303005: Strict FTP inspection matched _match\_string__policy-name__action\_string__src\_ifc__sip__sport__dest\_ifc__dip__dport_
    
-   %ASA-5-304001: _URL__user@source\_address__idfw\_user__URL__dest\_address__url_
    
-   %ASA-5-304002: Access denied URL _url_ SRC _(user)__(sip)__(user)_ DEST _dip_ on interface _int\_name_
    
-   (ICMP) %ASA-5-305013: Asymmetric NAT rules matched for forward and reverse flows; Connection for icmp src _interface\_name_:_source\_ip\_address__source\_user_ dst _interface\_name_:_destination\_ip\_address__destination\_user_ (type _type_, code _code_) denied due to NAT reverse path failure
    
-   (TCP, UDP, SCTP) %ASA-5-305013: Asymmetric NAT rules matched for forward and reverse flows; Connection for "protocol" src _interface\_name_:_source\_ip\_address_/_source\_port__source\_user_ dst _interface\_name_:_destination\_ip\_address_/_destination\_port__destination\_user_ denied due to NAT reverse path failure
    
    | ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)
    
    **Note** | ___
    
    Protocol in this error message can be TCP, UDP, or SCTP.
    
    ___ |
    |--------|--------------------------------------------------------------|
    
-   (Any Protocol) %ASA-5-305013: Asymmetric NAT rules matched for forward and reverse flows; Connection for protocol _protocol\_name_ src _interface\_name_:_source\_ip\_address__source\_user_ dst _interface\_name_:_destination\_ip\_address__destination\_user_ denied due to NAT reverse path failure
    
-   %ASA-5-321001: Resource var1 limit of var2 reached.
    
-   %ASA-5-321002: Resource var1 rate limit of var2 reached.
    
-   %ASA-5-324010: Subscriber _IMSI_ PDP Context activated on network _mcc_
    
-   %ASA-5-324011: Subscriber _IMSI_ location changed during _mcc_ from _mnc_ _IE type_
    
-   %ASA\-5-324012: GTP\_PARSE: _GTP IE TYPE_\[_GTP IE TYPE NUMBER_\]: Invalid Length Received Length: _Length Received_, Minimum Expected Length: _Expected Length_
    
-   %ASA-5-331002: Dynamic DNS _type__fqdn\_name__ip\_address_ _ip\_address_
    
-   %ASA-5-332003: Web Cache _IP\_address__service\_ID_
    
-   %ASA-5-333002: Timeout waiting for EAP response - context:EAP-context
    
-   %ASA-5-333010: EAP-SQ response Validation Flags TLV indicates PV request - context:EAP-context
    
-   %ASA-5-334002: EAPoUDP association successfully established - host-address
    
-   %ASA-5-334003: EAPoUDP association failed to establish - host-address
    
-   %ASA-5-334005: Host put into NAC Hold state - host-address
    
-   %ASA-5-334006: EAPoUDP failed to get a response from host - host-address
    
-   %ASA-5-335002: Host is on the NAC Exception List - host-address, OS:oper-sys
    
-   %ASA-5-335003: NAC Default ACL applied, ACL:ACL-name - host-address
    
-   %ASA-5-335008: NAC IPSec terminate from dynamic ACL:ACL-name - host-address
    
-   %ASA-5-336010 EIGRP-ddb\_name tableid as\_id: Neighbor address (%interface) is event\_msg: msg
    
-   %ASA-5-338302: Address _ipaddr__name__list_
    
-   %ASA-5-338303: Address _ipaddr__name)_
    
-   %ASA-5-338308: Dynamic Filter updater server dynamically changed from _old\_server\_host__old\_server\_port__new\_server\_host__new\_server\_port_
    
-   %ASA-5-402128: CRYPTO: An attempt to allocate a large memory block failed, size: _size__limit_
    
-   %ASA-5-415004: HTTP - matched _matched\_string__map\_name__connection\_action__int\_type__IP\_address__port\_num__int\_type__IP\_address__port\_num_
    
-   %ASA-5-415005: HTTP - matched _matched\_string__map\_name__connection\_action__int\_type__IP\_address__port\_num__int\_type__IP\_address__port\_num_
    
-   %ASA-5-415006: HTTP - matched _matched\_string__map\_name__connection\_action__int\_type__IP\_address__port\_num__int\_type__IP\_address__port\_num_
    
-   %ASA-5-415007: HTTP - matched _matched\_string__map\_name__connection\_action__int\_type__IP\_address__port\_num__int\_type__IP\_address__port\_num_
    
-   %ASA-5-415008: HTTP - matched _matched\_string__map\_name__connection\_action__int\_type__IP\_address__port\_num__int\_type__IP\_address__port\_num_
    
-   %ASA-5-415009: HTTP - matched _matched\_string__map\_name__connection\_action__int\_type__IP\_address__port\_num__int\_type__IP\_address__port\_num_
    
-   %ASA-5-415010: matched matched\_string in policy-map map\_name, transfer encoding matched connection\_action from int\_type:IP\_address/port\_num to int\_type:IP\_address/port\_num
    
-   %ASA-5-415011: HTTP - policy-map _map\_name__connection\_action__int\_type__IP\_address__port\_num__int\_type__IP\_address__port\_num_
    
-   %ASA-5-415012: HTTP - matched _matched\_string__map\_name__connection\_action__int\_type__IP\_address__port\_num__int\_type__IP\_address__port\_num_
    
-   %ASA-5-415013: HTTP - policy-map _map-name__connection\_action__int\_type__IP\_address__port\_num__int\_type__IP\_address__port\_num_
    
-   %ASA-5-415014: HTTP - matched _matched\_string__map\_name__connection\_action__int\_type__IP\_address__port\_num__int\_type__IP\_address__port\_num_
    
-   %ASA-5-415015: HTTP - matched _matched\_string__map\_name__connection\_action__int\_type__IP\_address__port\_num__int\_type__IP\_address__port\_num_
    
-   %ASA-5-415018: HTTP - matched _matched\_string__map\_name__connection\_action__int\_type__IP\_address__port\_num__int\_type__IP\_address__port\_num_
    
-   %ASA-5-415019: HTTP - matched _matched\_string__map\_name__connection\_action__int\_type__IP\_address__port\_num__int\_type__IP\_address__port\_num_
    
-   %ASA-5-415020: HTTP - matched _matched\_string__map\_name__connection\_action__int\_type__IP\_address__port\_num__int\_type__IP\_address__port\_num_
    
-   %ASA-5-425005 Interface interface\_name become active in redundant interface redundant\_interface\_name
    
-   %ASA-5-434004: SFR requested device to bypass further packet redirection and process _protocol_ flow from _inside\_ifc\_name_:_src\_ip_/_src\_port_ to _outside\_ifc\_name_:_dst\_ip_/_dst\_port_ locally
    
-   %ASA-5-444100: Shared license _request__reason_
    
-   %ASA-5-444101: Shared license service is active. License server address: _address_
    
-   %ASA-5-444305: %SMART\_LIC-5-SYSTEM\_CLOCK\_CHANGED: Smart Agent for Licensing System clock has been changed.
    
-   %ASA-5-444305: %SMART\_LIC-5-IN\_COMPLIANCE: All entitlements are authorized.
    
-   %ASA-5-444305: %SMART\_LIC-5-EVAL\_START: Entering evaluation period.
    
-   %ASA-5-444305: %SMART\_LIC-5-AUTHORIZATION\_EXPIRED: Authorization expired.
    
-   %ASA-5-444305: %SMART\_LIC-5-COMM\_RESTORED: Communications with Cisco licensing cloud restored.
    
-   %ASA-5-444305: %SMART\_LIC-5-COMM\_INIT\_FAILED: Failed to initialize communications with the Cisco Licensing Cloud.
    
-   %ASA-5-500001: ActiveX content modified src _forward\_ip\_address_ dest _reverse\_ip\_address_ on interface _interface\_name_
    
-   %ASA-5-500001: ActiveX content in java script is modified: src _forward\_ip\_address_ dest _reverse\_ip\_address_ on interface _interface\_name_
    
-   %ASA-5-500002: Java content modified: src _forward\_ip\_address_ dest _reverse\_ip\_address_ on interface _interface\_name_
    
-   %ASA-5-500002: Java content in java script is modified: src _forward\_ip\_address_ dest _reverse\_ip\_address_ on interface _interface\_name_
    
-   %ASA-5-500003: Bad TCP hdr length (hdrlen=bytes, pktlen=bytes) from source\_address/source\_port to dest\_address/dest\_port, flags: tcp\_flags, on interface interface\_name
    
-   %ASA-5-501101: User transitioning priv level
    
-   %ASA-5-502101: New user added to local dbase: Uname: _user__privilege\_level_
    
-   %ASA-5-502102: User deleted from local dbase: Uname: _user__privilege\_level_
    
-   %ASA-5-502103: User priv level changed: Uname: _user__privilege\_level__privilege\_level_
    
-   %ASA-5-502111: New group policy added: name: _policy\_name__policy\_type_
    
-   %ASA-5-502112: Group policy deleted: name: _policy\_name__policy\_type_
    
-   %ASA-5-503001: Process _process\_number_, Nbr _IP\_address_ on _interface\_name_ from _old\_state_ to _new\_state_, _reason_
    
-   %ASA-5-503002: Last valid authentication key for neighbor _nameif_ expires
    
-   %ASA-5-503003: Expired key ID _sent | received_ used by neighbor _nameif_
    
-   %ASA-5-503004: No key ID _key-id_ for neighbor _key-chain-name_
    
-   %ASA-5-503005: No crypto algorithm for neighbor _key-id_ key ID _key-chain-name_
    
-   %ASA-5-504001: Security context _context\_name_
    
-   %ASA-5-504002: Security context _context\_name_
    
-   %ASA-5-505001: Module _string one_
    
-   %ASA-5-505002: Module _ips_
    
-   %ASA-5-505003: Module _string one_
    
-   %ASA-5-505004: Module _string one_
    
-   %ASA-5-505005: Module _module\_name_
    
-   %ASA-5-505006: Module _string one_
    
-   %ASA-5-505007: Module _module\_id_
    
-   %ASA-5-505008: Module _module\_id__newver__ver_
    
-   %ASA-5-505009: Module in slot _string one__newver__prevver_
    
-   %ASA-5-505010: Module in slot _slot_
    
-   %ASA-5-505012: Module _module\_id__application__ver\_num__version_
    
-   %ASA-5-505013: Module _module\_id__application__version__newapplication_
    
-   %ASA-5-506001: _event\_source\_string_ _event\_string_
    
-   %ASA-5-507001: Terminating TCP-Proxy connection from _interface\_inside__source\_address__source\_port__interface\_outside__dest\_address__dest\_port__limit_
    
-   %ASA-5-508001: DCERPC _message\_type__version\_type__version\_number__src\_if__src\_ip__src\_port__dest\_if__dest\_ip__dest\_port_
    
-   %ASA-5-508002: DCERPC response has low endpoint port _port\_number__src\_if__src\_ip__src\_port__dest\_if__dest\_ip__dest\_port_
    
-   %ASA-5-509001: Connection attempt was prevented by \\ command: _src\_intf_
    
-   %ASA-5-503101: Process _d_, Nbr _i_ on _s_ from _s_ to _s_, _s_
    
-   %ASA-5-611103: User logged out: Uname: _user_
    
-   %ASA-5-611104: Serial console idle timeout exceeded
    
-   %ASA-5-612001: Auto Update succeeded: _filename__number_
    
-   %ASA-5-711005: _call\_stack_
    
-   %ASA-5-713006: Group = _groupname_, Username = _username_, IP = _peerIP_ Failed to obtain state for message Id _message\_number_, Peer Address: _IP\_address_
    
-   %ASA-5-713010: Group = _groupname_, Username = _username_, IP = _peerIP_ _IKE area_: failed to find centry for message Id _message\_number_
    
-   %ASA-5-713041: Group = _groupname_, Username = _username_, IP = _peerIP_ IKE Initiator: _new_ or _rekey_ Phase 1 or 2, Intf _interface\_number_, IKE Peer _IP\_address_ local Proxy Address _IP\_address_, remote Proxy Address _IP\_address_, Crypto map (_crypto map tag_ )
    
-   %ASA-5-713049: Group = _groupname_, Username = _username_, IP = _peerIP_ Security negotiation complete for _tunnel\_type_ type (_group\_name_ ) _Initiator_ /_Responder_, Inbound SPI = _SPI_, Outbound SPI = _SPI_
    
-   %ASA-5-713050: Group = _groupname_, Username = _username_, IP = _peerIP_ Connection terminated for peer _IP\_address_ . Reason: termination reason Remote Proxy _IP\_address_, Local Proxy _IP\_address_
    
-   %ASA-5-713068: Group = _groupname_, Username = _username_, IP = _peerIP_ Received non-routine Notify message: notify\_type (notify\_value)
    
-   %ASA-5-713073: Group = _groupname_, Username = _username_, IP = _peerIP_ Responder forcing change of _Phase 1_ /_Phase 2_ rekeying duration from _larger\_value_ to _smaller\_value_ seconds
    
-   %ASA-5-713074: Group = _groupname_, Username = _username_, IP = _peerIP_ Responder forcing change of IPsec rekeying duration from _larger\_value_ to _smaller\_value_ Kbs
    
-   %ASA-5-713075: Group = _groupname_, Username = _username_, IP = _peerIP_ Overriding Initiator's IPsec rekeying duration from _larger\_value_ to _smaller\_value_ seconds
    
-   %ASA-5-713076: Group = _groupname_, Username = _username_, IP = _peerIP_ Overriding Initiator's IPsec rekeying duration from _larger\_value_ to _smaller\_value_ Kbs
    
-   %ASA-5-713092: Group = _groupname_, Username = _username_, IP = _peerIP_ Failure during phase 1 rekeying attempt due to collision
    
-   %ASA-5-713115: Group = _groupname_, Username = _username_, IP = _peerIP_ Client rejected NAT enabled IPsec request, falling back to standard IPsec
    
-   %ASA-5-713119: Group = _groupname_, Username = _username_, IP = _peerIP_ Group _group_ IP _ip_ PHASE 1 COMPLETED
    
-   %ASA-5-713120: Group = _groupname_, Username = _username_, IP = _peerIP_ PHASE 2 COMPLETED (msgid=_msg\_id_ )
    
-   %ASA-5-713130: Group = _groupname_, Username = _username_, IP = _peerIP_ Received unsupported transaction mode attribute: attribute id
    
-   %ASA-5-713131: Group = _groupname_, Username = _username_, IP = _peerIP_ Received unknown transaction mode attribute: attribute\_id
    
-   %ASA-5-713135: Group = _groupname_, Username = _username_, IP = _peerIP_ message received, redirecting tunnel to _IP\_address_ .
    
-   %ASA-5-713136: Group = _groupname_, Username = _username_, IP = _peerIP_ IKE session establishment timed out \[_IKE\_state\_name_ \], aborting!
    
-   %ASA-5-713137: Group = _groupname_, Username = _username_, IP = _peerIP_ Reaper overriding refCnt \[ref\_count\] and tunnelCnt \[tunnel\_count\] -- deleting SA!
    
-   %ASA-5-713139: IP = _peerIP_ _group\_name_ not found, using BASE GROUP default preshared key
    
-   %ASA-5-713144: IP = _peerIP_ Ignoring received malformed firewall record; reason - _error\_reason_ TLV type _attribute\_value correction_
    
-   %ASA-5-713148: Group = _groupname_, Username = _username_, IP = _peerIP_ Terminating tunnel to Hardware Client in network extension mode, unable to delete static route for address: _IP\_address_, mask: _netmask_
    
-   %ASA-5-713155: DNS lookup for Primary VPN Server \[_server\_name_ \] successfully resolved after a previous failure. Resetting any Backup Server init.
    
-   %ASA-5-713156: Initializing Backup Server \[_server\_name_ or _IP\_address_ \]
    
-   %ASA-5-713158: Group = _groupname_, Username = _username_, IP = _peerIP_ Client rejected NAT enabled IPsec Over UDP request, falling back to IPsec Over TCP
    
-   %ASA-5-713178: Group = _groupname_, Username = _username_, IP = _peerIP_ IKE Initiator received a packet from its peer without a Responder cookie
    
-   %ASA-5-713179: Group = _groupname_, Username = _username_, IP = _peerIP_ IKE AM Initiator received a packet from its peer without a _payload\_type_ payload
    
-   %ASA-5-713196: Group = _groupname_, Username = _username_, IP = _peerIP_ Remote L2L Peer _IP\_address_ initiated a tunnel with same outer and inner addresses. Peer could be Originate Only - Possible misconfiguration!
    
-   %ASA-5-713197: Group = _groupname_, Username = _username_, IP = _peerIP_ The configured Confidence Interval of _number_ seconds is invalid for this _tunnel\_type_ connection. Enforcing the second default.
    
-   %ASA-5-713199: Group = _groupname_, Username = _username_, IP = _peerIP_ Reaper corrected an SA that has not decremented the concurrent IKE negotiations counter ( _counter\_value_ )!
    
-   %ASA-5-713201: Group = _groupname_, Username = _username_, IP = _peerIP_ Duplicate Phase _Phase_ packet detected. _Action_
    
-   %ASA-5-713202: IP = _IP\_address_ Duplicate _IP\_addr_ packet detected.
    
-   %ASA-5-713216: Group = _groupname_, Username = _username_, IP = _peerIP_ Rule: _action_ \[Client type\]: _version_ Client: _type_ version allowed/not allowed
    
-   %ASA-5-713229: Group = _groupname_, Username = _username_, IP = _peerIP_ Auto Update - Notification to client _client\_ip_ of update string: _message\_string_ .
    
-   %ASA-5-713237: Group = _groupname_, Username = _username_, IP = _peerIP_ ACL update (_access\_list_ ) received during re-key re-authentication will not be applied to the tunnel.
    
-   %ASA-5-713239: Group = _groupname_, Username = _username_, IP = _peerIP__IP\_Address_ : Tunnel Rejected: The maximum tunnel count allowed has been reached
    
-   %ASA-5-713240: Received DH key with bad length: received length=<i>rlength</i> expected length=<i>elength</i>
    
-   %ASA-5-713248: Group = _groupname_, Username = _username_, IP = _peerIP_ _META-DATA_ Rekey initiation is being disabled during CRACK authentication.
    
-   %ASA-5-713250: Group = _groupname_, Username = _username_, IP = _peerIP_ _META-DATA_ Received unknown Internal Address attribute: _attribute_
    
-   %ASA-5-713252: Group = _group_, Username = _user_, IP = _ip_ Group = _group_, Username = _user_, IP = _ip_, Integrity Firewall Server is not available. VPN Tunnel creation rejected for client.
    
-   %ASA-5-713253: Group = _group_, Username = _user_, IP = _ip_ Group = _group_, Username = _user_, IP = _ip_, Integrity Firewall Server is not available. Entering ALLOW mode. VPN Tunnel created for client.
    
-   %ASA-5-713257: Phase _var1_ failure: Mismatched attribute types for class _var2_ : Rcv'd: _var3_ Cfg'd: _var4_
    
-   %ASA-5-713259: Group = _groupname_, Username = _username_, IP = _peerIP_ Group = _groupname_, Username = _username_, IP = _peerIP_, Session is being torn down. Reason: _reason_
    
-   %ASA-5-713272: Group = _groupname_, Username = _username_, IP = _peerIP_ Terminating tunnel to Hardware Client in network extension mode, unable to delete static route for address: _IP\_address_, mask: /_prefix\_len_
    
-   %ASA-5-713904: Descriptive\_event\_string.
    
-   %ASA-5-716053: SAML Server added: Name: _name__SP_
    
-   %ASA-5-716054: SAML Server deleted: Name: _name__SP_
    
-   %ASA-5-717013: Removing a cached CRL to accommodate an incoming CRL Issuer: _issuer_
    
-   %ASA-5-717014: Unable to cache a CRL received from _CDP__size__space_
    
-   %ASA-5-717050: SCEP Proxy: Processed request type _type__client ip address__username__tunnel\_group name__group-policy name__ca ip address_
    
-   %ASA-5-717053: Group _group name__user name__IP Address__id subject name__id issuer name__id serial number_
    
-   %ASA-5-717061: Starting _protocol__tpname__ca\_name__type__mode_
    
-   %ASA-5-717062: _protocol__tpname__ca__subject__issuer__serial_
    
-   %ASA-5-717064: Keypair _keyname__tpname__mode__protocol_
    
-   %ASA-5-717067: Starting ACME certificate enrollment for the trustpoint _tpname_ with CA _ca\_name_. Mode _mode_
    
-   %ASA-5-717068: ACME Certificate enrollment succeeded for trustpoint _tpname_ with CA _ca_. Received a new certificate with Subject Name _subject_ Issuer Name _issuer_ Serial Number _serial_
    
-   %ASA-5-717070: Keypair _keyname_ in the trustpoint _tpname_ is regenerated for _mode_ ACME certificate enrollment
    
-   %ASA-5-717072: A CRL with an older version than the currently cached one was downloaded.
    
-   %ASA-5-718002: Create peer _IP\_address__number\_of\_peers_
    
-   %ASA-5-718005: Fail to send to _IP\_address__port_
    
-   %ASA-5-718006: Invalid load balancing state transition \[cur=_state\_number__event\_number_
    
-   %ASA-5-718007: Socket open failure \[_failure\_code__failure\_text_
    
-   %ASA-5-718008: Socket bind failure \[_failure\_code__failure\_text_
    
-   %ASA-5-718009: Send HELLO response failure to \[_IP\_address_
    
-   %ASA-5-718010: Sent HELLO response to \[_IP\_address_
    
-   %ASA-5-718011: Send HELLO request failure to \[_IP\_address_
    
-   %ASA-5-718012: Sent HELLO request to \[_IP\_address_
    
-   %ASA-5-718014: Master peer\[_IP\_address_
    
-   %ASA-5-718015: Received HELLO request from \[_IP\_address_
    
-   %ASA-5-718016: Received HELLO response from \[_IP\_address_
    
-   %ASA-5-718024: Send CFG UPDATE failure to \[_IP\_address_
    
-   %ASA-5-718028: Send OOS indicator failure to \[_IP\_address_
    
-   %ASA-5-718031: Received OOS obituary for \[_IP\_address_
    
-   %ASA-5-718032: Received OOS indicator from \[_IP\_address_
    
-   %ASA-5-718033: Send TOPOLOGY indicator failure to \[_IP\_address_
    
-   %ASA-5-718042: Unable to ARP for \[_IP\_address_
    
-   %ASA-5-718043: Updating/removing duplicate peer entry \[_IP\_address_
    
-   %ASA-5-718044: Deleted peer\[_IP\_address_
    
-   %ASA-5-718045: Created peer\[_IP\_address_
    
-   %ASA-5-718048: Create of secure tunnel failure for peer \[_IP\_address_
    
-   %ASA-5-718050: Delete of secure tunnel failure for peer \[_IP\_address_
    
-   %ASA-5-718052: Received GRAT-ARP from duplicate control node\[_MAC\_address_
    
-   %ASA-5-718053: Detected duplicate control node, mastership stolen\[_MAC\_address_
    
-   %ASA-5-718054: Detected duplicate control node\[_MAC\_address_
    
-   %ASA-5-718055: Detected duplicate control node\[_MAC\_address_
    
-   %ASA-5-718057: Queue send failure from ISR, msg type _failure\_code_
    
-   %ASA-5-718060: Inbound socket select fail: context=_context\_ID_
    
-   %ASA-5-718061: Inbound socket read fail: context=_context\_ID_
    
-   %ASA-5-718062: Inbound thread is awake (context=_context\_ID_
    
-   %ASA-5-718063: Interface _interface\_name_
    
-   %ASA-5-718064: Admin. interface _interface\_name_
    
-   %ASA-5-718065: Cannot continue to run (public=_up__down__up__down__LB\_state_
    
-   %ASA-5-718066: Cannot add secondary address to interface _interface\_name__IP\_address_
    
-   %ASA-5-718067: Cannot delete secondary address to interface _interface\_name__IP\_address_
    
-   %ASA-5-718068: Start VPN Load Balancing in context _context\_ID_
    
-   %ASA-5-718069: Stop VPN Load Balancing in context _context\_ID_
    
-   %ASA-5-718070: Reset VPN Load Balancing in context _context\_ID_
    
-   %ASA-5-718071: Terminate VPN Load Balancing in context _context\_ID_
    
-   %ASA-5-718072: Becoming control node of Load Balancing in context _context\_ID_
    
-   %ASA-5-718073: Becoming data node of Load Balancing in context _context\_ID_
    
-   %ASA-5-718074: Fail to create access list for peer _context\_ID_
    
-   %ASA-5-718075: Peer _IP\_address_
    
-   %ASA-5-718076: Fail to create tunnel group for peer _IP\_address_
    
-   %ASA-5-718077: Fail to delete tunnel group for peer _IP\_address_
    
-   %ASA-5-718078: Fail to create crypto map for peer _IP\_address_
    
-   %ASA-5-718079: Fail to delete crypto map for peer _IP\_address_
    
-   %ASA-5-718080: Fail to create crypto policy for peer _IP\_address_
    
-   %ASA-5-718081: Fail to delete crypto policy for peer _IP\_address_
    
-   %ASA-5-718082: Fail to create crypto ipsec for peer _IP\_address_
    
-   %ASA-5-718083: Fail to delete crypto ipsec for peer _IP\_address_
    
-   %ASA-5-718084: Public/cluster IP not on the same subnet: public _IP\_address__netmask__IP\_address_
    
-   %ASA-5-718085: Interface _interface\_name_
    
-   %ASA-5-718086: Fail to install LB NP rules: type _rule\_type__interface\_name__port_
    
-   %ASA-5-718087: Fail to delete LB NP rules: type _rule\_type__rule\_ID_
    
-   %ASA-5-719014: Email Proxy is changing listen port from old\_port to new\_port for mail protocol protocol.
    
-   %ASA-5-720016: (VPN-unit) Failed to initialize default timer #index.
    
-   %ASA-5-720017: (VPN-unit) Failed to update LB runtime data
    
-   %ASA-5-720018: (VPN-unit) Failed to get a buffer from the underlying core high availability subsystem. Error code code.
    
-   %ASA-5-720019: (VPN-unit) Failed to update cTCP statistics.
    
-   %ASA-5-720020: (VPN-unit) Failed to send type timer message.
    
-   %ASA-5-720021: (VPN-unit) HA non-block send failed for peer msg message\_number. HA error code.
    
-   %ASA-5-720035: (VPN-unit) Fail to look up CTCP flow handle
    
-   %ASA-5-720036: (VPN-unit) Failed to process state update message from the active peer.
    
-   %ASA-5-720071: (VPN-unit) Failed to update cTCP dynamic data.
    
-   %ASA-5-720072: Timeout waiting for Integrity Firewall Server \[interface,ip\] to become available.
    
-   %ASA-5-722037: Group _group__user-name__ip\_address__reason_
    
-   %ASA-5-722038: Group _group__name__user-name__reason_
    
-   %ASA-5-722005: Group _group__user-name__IP\_address_
    
-   %ASA-5-722006: Group _group__user-name__ip\_address__ip\_address_
    
-   %ASA-5-722010: Group _group__user-name__IP\_address__type-num__message_
    
-   %ASA-5-722011: Group _group__user-name__IP\_address__type-num__message_
    
-   %ASA-5-722012: Group _group__user-name__IP\_address__type-num__message_
    
-   %ASA-5-722028: Group _group__user-name__IP\_address_
    
-   %ASA-5-722032: Group <_group_\> User <_user\_name_\> IP <_ip\_address_\> New _TCP|UDP_ SVC connection replacing old connection.
    
-   %ASA-5-722033: Group <_group_\> User <_user\_name_\> IP <_ip\_address_\> First _TCP|UDP_ SVC connection established for SVC session.
    
-   %ASA-5-722034: Group <_group_\> User <_user\_name_\> IP <_ip\_address_\> New _TCP|UDP_ SVC connection, no existing connection.
    
-   %ASA-5-722037: Group _group__user-name__ip\_address__reason_
    
-   %ASA-5-722038: Group _group__name__user-name__reason_
    
-   %ASA-5-722043: Group _group__user__ip_
    
-   %ASA-5-722044: Group _group__user__ip__ver_
    
-   %ASA-5-730009: Group groupname, User username, IP ipaddr, CAS casaddr, capacity exceeded, terminating connection.
    
-   %ASA-5-734002: DAP: User _user,_ _ipaddr_
    
-   %ASA-5-737003: IPAA: Session=_session__tunnel-group_
    
-   %ASA-5-737004: IPAA: Session=_session__'tunnel-group'_
    
-   %ASA-5-737007: IPAA: Session=_session__tunnel-group_
    
-   %ASA-5-737008: IPAA: Session=_session__'tunnel-group'_
    
-   %ASA-5-737011: IPAA: Session=_session__ip-address_
    
-   %ASA-5-737018: IPAA: Session=_session__num_
    
-   %ASA-5-737021: IPAA: Address from local pool (ip-address) duplicates address from DHCP
    
-   %ASA-5-737022: IPAA: Address from local pool (ip-address) duplicates address from AAA
    
-   %ASA-5-737023: IPAA: Session=_session__ip-address_
    
-   %ASA-5-737024: IPAA: Session= _:_
    
-   %ASA-5-737025: IPAA: Not releasing local pool ip-address, due to local pool duplicate issue
    
-   %ASA-5-737034: IPAA: Session=<session>, <IP version> address: <explanation>
    
-   % ASA-5-737204: VPNFIP: Pool=_pool__message_
    
-   %ASA-5-737405: POOLIP: Pool=_pool__message_
    
-   %ASA-5-746007: user-identity: NetBIOS response failed from User _user\_name__user\_ip_
    
-   %ASA-5-746012: user-identity: Add IP-User mapping IP Address - domain\_name\\user\_name result - reason
    
-   %ASA-5-746013: user-identity: Delete IP-User mapping IP Address - domain\_name\\user\_name result - reason
    
-   %ASA-5-746014: user-identity: \[FQDN\] _fqdn__IP Address_
    
-   %ASA-5-746015: user-identity: \[FQDN\] _fqdn__IP address_
    
-   %ASA-5-747002: Clustering: Recovered from state machine dropped event (event-id, ptr-in-hex, ptr-in-hex). Intended state: state-name. Current state: state-name.
    
-   %ASA-5-747003: Clustering: Recovered from state machine failure to process event (event-id, ptr-in-hex, ptr-in-hex) at state state-name.
    
-   %ASA-5-747007: Clustering: Recovered from finding stray config sync thread, stack ptr-in-hex, ptr-in-hex, ptr-in-hex, ptr-in-hex, ptr-in-hex, ptr-in-hex.
    
-   %ASA-5-748001: Module _slot\_number__chassis\_number_
    
-   %ASA-5-748004: Module _slot\_number__chassis\_number_
    
-   %ASA-5-748203: Module <module\_id> in chassis <chassis id> is re-joining the cluster due to a service chain application recovery.
    
-   %ASA-5-750001: Local:_local IP_ :_local port_ Remote:_remote IP_ : _remote port_ Username: _username_ Received request to _request_ an IPsec tunnel; local traffic selector = _local selectors: range, protocol, port range_ ; remote traffic selector = _remote selectors: range, protocol, port range_
    
-   %ASA-5-750002: Local:_local IP_ :_local port_ Remote: _remote IP_ : _remote port_ Username: _username_ Received a IKE\_INIT\_SA request
    
-   %ASA-5-750004: Local: _local IP: local port_ Remote: _remote IP: remote port_ Username: _username_ Sending COOKIE challenge to throttle possible DoS
    
-   %ASA-5-750005: Local: _local IP: local port_ Remote: _remote IP: remote port_ Username: _username_ IPsec rekey collision detected. I am lowest nonce initiator, deleting SA with inbound SPI _SPI_
    
-   %ASA-5-750006: Local: _local IP: local port_ Remote: _remote IP: remote port_ Username: _username_ SA UP. Reason: _reason_
    
-   %ASA-5-750007: Local: _local IP: local port_ Remote: r_emote IP: remote port_ Username: _username_ SA DOWN. Reason: _reason_
    
-   %ASA-5-750008: Local: _local IP: local port_ Remote: _remote IP: remote port_ Username: _username_ SA rejected due to system resource low
    
-   %ASA-5-750009: Local: _local IP: local port_ Remote: _remote IP: remote port_ Username: _username_ SA request rejected due to CAC limit reached: Rejection reason: _reason_
    
-   %ASA-5-750010: Local: _local-ip_ Remote: _remote-ip_ Username:_username_ IKEv2 local throttle-request queue depth threshold of _threshold_ reached; increase the window size on peer _peer_ for better performance
    
-   %ASA-5-750013 - IKEv2 SA (iSPI <ISPI> rRSP <rSPI>) Peer Moved: Previous <prev\_remote\_ip>:<prev\_remote\_port>/<prev\_local\_ip>:<prev\_local\_port>. Updated <new\_remote\_ip>:<new\_remote\_port>/<new\_local\_ip>:<new\_local\_port>
    
-   %ASA-5-751007: Configured attribute not supported for IKEv2. Attribute: _attribute_
    
-   %ASA-5-751025: Group:_group-policy_ IPv4 Address=_assigned\_IPv4\_addr_ IPv6 address=_assigned\_IPv6\_addr_ assigned to session
    
-   %ASA-5-751028: Overriding configured keepalive values of threshold:_config\_threshold_/retry:_config\_retry_ to threshold:_applied\_threshold_/retry:_applied\_retry_.
    
-   %ASA-5-752003: Tunnel Manager dispatching a KEY\_ACQUIRE message to IKEv2. Map Tag = _mapTag_ . Map Sequence Number = _mapSeq_
    
-   %ASA-5-752004: Tunnel Manager dispatching a KEY\_ACQUIRE message to IKEv1. Map Tag = _mapTag_ . Map Sequence Number = _mapSeq_
    
-   %ASA-5-752016: IKEv _protocol_ was successful at setting up a tunnel. Map Tag = _mapTag_ . Map Sequence Number = _mapSeq._
    
-   %ASA-5-776009: CTS SXP: password changed.
    
-   %ASA-5-776010: CTS SXP: SXP default source IP is changed original source IP final source IP.
    
-   %ASA-5-776011: CTS SXP: operational state.
    
-   %ASA-5-776252: CTS SGT-MAP: CTS SGT-MAP: Binding binding IP - SGname(SGT) from source name deleted from binding manager.
    
-   %ASA-5-776309: CTS Policy: Previously known security-group tag _sgt_
    
-   %ASA-5-776310: CTS Policy: Security-group name "_sgname__old\_sgt__new\_sgt_
    
-   %ASA-5-769001: UPDATE: _ASA__src_
    
-   %ASA-5-769002: UPDATE: _ASA__src__dest_
    
-   %ASA-5-769003: UPDATE: _ASA__src__dest_
    
-   %ASA-5-769004: UPDATE: ASA image src\_file failed verification, reason: failure\_reason
    
-   %ASA-5-769005: UPDATE: _ASA__image\_name_
    
-   %ASA-5-771001: CLOCK: System clock set, source: _src__time__time_
    
-   %ASA-5-771002: CLOCK: System clock set, source: _src__ip__time__time_
    
-   %ASA-5-771002: CLOCK: System clock set, source: _src__ip__time__time_
    
-   %ASA-5-8300006: Cluster topology change detected. VPN session redistribution aborted.
    

## Informational Messages, Severity 6

The following messages appear at severity 6, informational:

-   %ASA-6-106012: Deny IP from _IP\_address__IP\_address__hex_
    
-   %ASA-6-106015: Deny TCP (no connection) from IP\_address/port to IP\_address/port flags tcp\_flags on interface interface\_name.
    
-   %ASA-6-106025: Failed to determine security context for packet: vlan_source__Vlan__source\_address__source\_port__dest\_address__dest\_port protocol_
    
-   %ASA-6-106026: Failed to determine the security context for the packet:sourceVlan:source\_address dest\_address source\_port dest\_port protocol
    
-   %ASA-6-106100: access-list _acl\_ID_ _protocol__interface\_name__source\_address__source\_port__idfw\_user__sg\_info__interface\_name__dest\_address__dest\_port__idfw\_user__sg\_info__number__number_
    
-   %ASA-6-106102: access-list acl\_ID {permitted | denied} protocol for user username interface\_name/source\_address source\_port interface\_name/dest\_address dest\_port hit-cnt number {first hit | number-second interval} hash codes
    
-   %ASA-6-108005: _action\_class: Received__req\_resp_ _src\_ifc__sip__sport_ _dest\_ifc_ _dip__dport__further\_info_
    
-   %ASA-6-108007: TLS started on ESMTP session between client _client-side interface-name__client IP address__client port__server-side interface-name__server IP address__server port_
    
-   %ASA-6-109001: Auth start for user '_user__inside\_address__inside\_port__outside\_address__outside\_port_
    
-   %ASA-6-109002: Auth from _inside\_address__inside\_port__outside\_address__outside\_port__IP\_address__interface\_name_
    
-   %ASA-6-109003: Auth from _inside\_address__inside\_port__outside\_address__outside\_port__interface\_name_
    
-   %ASA-6-109005: Authentication succeeded for user '_user__inside\_address__inside\_port__outside\_address__outside\_port__interface\_name_
    
-   %ASA-6-109006: Authentication failed for user '_user__inside\_address__inside\_port__outside\_address__outside\_port__interface\_name_
    
-   %ASA-6-109007: Authorization permitted for user '_user__inside\_address__inside\_port__outside\_address__outside\_port__interface\_name_
    
-   %ASA-6-109008: Authorization denied for user '_user__outside\_address__outside\_port__inside\_address__inside\_port__interface\_name_
    
-   %ASA-6-109024: Authorization denied from _source\_address__source\_port__dest\_address__dest\_port__interface\_name__protocol_
    
-   %ASA-6-109025: Authorization denied (acl=_acl\_ID__user__source\_address__source\_port__dest\_address__dest\_port__interface\_name__protocol_
    
-   %ASA-6-109036: Exceeded _1000__attribute name__username_
    
-   %ASA-6-109100: Received CoA update from _coa-source-ip__username__audit-session-id_
    
-   %ASA-6-109101: Received CoA disconnect request from _coa-source-ip__username__audit-session-id_
    
-   %ASA-6-109202: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP Address_, Succeeded incrementing entry use
    
-   %ASA-6-109211: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP Address_, Succeeded decrementing entry use.
    
-   %ASA-6-110002: Failed to locate egress interface for _protocol_ from _src\_interface_:_src\_ip_/_src\_port_ to _dest\_ip_/_dest\_port_
    
-   %ASA-6-110003: Routing failed to locate next hop for _protocol_ from _src\_interface_:_src\_ip_/_src\_port_ to _dest\_interface_:_dest\_ip_/_dest\_port_
    
-   %ASA-6-110004: Egress interface changed from _old\_active\_ifc_ to _new\_active\_ifc_ on _ip\_protocol_ connection _conn\_id_ for _outside\_zone_/_parent\_outside\_ifc_:_outside\_addr_/_outside\_port_ (_mapped\_addr_/_mapped\_port_) to _inside\_zone_/_parent\_inside\_ifc_:_inside\_addr_/_inside\_port_ (_mapped\_addr_/_mapped\_port_)
    
-   %ASA-6-110005: Routing failed to locate next hop for protocol from _interface_:_address_/_port_ to _interface_:_address_/_port_
    
-   %ASA-6-113003: AAA group policy for user _user__policy\_name_
    
-   %ASA-6-113004: AAA user _aaa\_type__server\_IP\_address__user_
    
-   %ASA-6-113005: AAA user authentication Rejected : reason = _reason_ : server = _ip\_address_ : user =_user\_name_ : user IP = _ip\_address_
    
-   %ASA-6-113005: AAA user authorization Rejected : reason = _reason_ : server = _ip\_address_ : user =_user\_name_ : user IP = _ip\_address_
    
-   %ASA-6-113006: User '_user__number_
    
-   %ASA-6-113007: User '_user__administrator_
    
-   %ASA-6-113008: AAA transaction status _ACCEPT__user_
    
-   %ASA-6-113009: AAA retrieved default group policy (_policy__username_
    
-   %ASA-6-113010: AAA challenge received for user _user__server\_IP\_address_
    
-   %ASA-6-113011: AAA retrieved user specific group policy (_policy__user_
    
-   %ASA-6-113012: AAA user authentication Successful : local database : user = _user_
    
-   %ASA-6-113013: AAA unable to complete the request Error : reason = _reason__user_
    
-   %ASA-6-113014: AAA _authentication__server\_IP\_address__user_
    
-   %ASA-6-113015: AAA user authentication Rejected : reason = _reason__user:_ _xxx.xxx.xxx.xxx_
    
-   %ASA-6-113016: AAA credentials rejected : reason = _reason__server\_IP\_address__user<915CLI>:_ _xxx.xxx.xxx.xxx_
    
-   %ASA-6-113017: AAA credentials rejected : reason = _reason__user:_ _xxx.xxx.xxx.xxx_
    
-   %ASA-6-113033: Group _group__user__ipaddr__AnyConnect_
    
-   %ASA-6-113037: Group <_group_\> User <_user_\> IP <_ip\_address_\> Reboot pending, new sessions disabled. Denied user login.
    
-   %ASA-6-113039: Group _group__user__ipaddr__AnyConnect parent_
    
-   %ASA-6-113045: AAA SDI server IP\_address in aaa-server group group\_name: status changed from previous-state to current-state
    
-   %ASA-6-114004: _4GE SSM_
    
-   %ASA-6-114005: _4GE SSM_
    
-   %ASA-6-120003: Call-Home is processing _group__title_
    
-   %ASA-6-120007: Call-Home _group__destination_
    
-   %ASA-6-121003: _id_
    
-   %ASA-6-199002: Startup completed. Beginning operation.
    
-   %ASA-6-199003: Reducing Link MTU _dec_
    
-   %ASA-6-199005: Startup begin
    
-   %ASA-6-199018: syslog
    
-   %ASA-6-201010: Embryonic connection limit exceeded _econns__limit__dir__source\_address__source\_port__dest\_address__dest\_port__interface\_name_
    
-   %ASA-6-201012: Per-client embryonic connection limit exceeded _curr\_num_/_limit_ for _\[input|output\]_ packet from _ip\_address_/_port_ to _ip\_address_/_port_ on interface _interface\_name_
    
-   %ASA-6-210022: LU missed _number_
    
-   %ASA-6-302003: Built H245 connection for faddr _foreign\_ip\_address_ laddr _local\_ip\_address_/_local\_port_
    
-   %ASA-6-302003: Built H245 connection for faddr _foreign\_ip\_address_/_foreign\_port_ laddr _local\_ip\_address_
    
-   %ASA-6-302004: Pre-allocate H323 {_TCP | UDP_} backconnection for faddr _foreign\_ip\_address_ to laddr _local\_ip\_address_/__local\_port__
    
-   %ASA-6-302004: Pre-allocate H323 {_TCP | UDP_} backconnection for faddr _foreign\_ip\_address_/_foreign\_port_ to laddr _local\_ip\_address_
    
-   %ASA-6-302010: _connections__connections_
    
-   %ASA-6-302012: Pre-allocate H225 Call Signalling Connection for faddr _foreign\_ip\_address_ to laddr _local\_ip\_address_/_local\_port_
    
-   %ASA-6-302012: Pre-allocate H225 Call Signalling Connection for faddr _foreign\_ip\_address_/_foreign\_port_ to laddr _local\_ip\_address_
    
-   %ASA-6-302013: Built _{inbound | outbound}__\[Probe\]_ TCP connection _connection\_id_ for _interface_:_real-address_/_real-port_ (_(mapped-address/mapped-port)_)_idfw\_user_ to _interface_:_real-address_/_real-port_ (_mapped-address/mapped-port_)_inside\_idfw\_and\_sg\_info_ _id\_port\_num_ _rx\_ring\_num_ \[(_user_)\]
    
-   %ASA-6-302014: Teardown \[_Probe_\]TCP connection _connection\_id_ for _interface_:_real\_address_/_real\_port__idfw\_user_ to _interface_:_real\_address_/_real\_port__idfw\_user_ duration _hh:mm:ss_ bytes _bytes_ _reason\_string__teardown\_initiator__initiator_ _port\_num_ _rx\_ring\_num_ \[(_user_)\]
    
-   %ASA-6-302015: Built {_inbound | outbound_} UDP connection _connection\_id_ for _interface_:_real\_address_/_real\_port_ (_mapped\_address_/_mapped\_port_)_idfw\_user_ to _interface_:_real\_address_/_real\_port_ (_mapped\_address_/_mapped\_port_)_idfw\_user_ _id\_port\_num_ _rx\_ring\_num_ \[(_user_)\]
    
-   %ASA-6-302016: Teardown UDP connection _connection\_id_ for _interface_:_real\_address_/_real\_port__idfw\_user_ to _interface_:_real\_address_/_real\_port__idfw\_user_ duration _hh:mm:ss_ bytes _bytes_ _id\_port\_num_ _rx\_ring\_num_ \[(_user_)\]
    
-   %ASA-6-302017: Built {_inbound | outbound_} GRE connection _id_ from _interface_:_real\_address_ (_translated\_address_)_idfw\_user_ to _interface_:_real\_address_/_real\_cid_ (_translated\_address_/_translated\_cid_)_idfw\_user_ _id\_port\_num_ _rx\_ring\_num_ \[(_user_)\]
    
-   %ASA-6-302018: Teardown GRE connection _id_ from _interface_:_real\_address__translated\_address_ to _interface_:_real\_address_/_real\_cid__idfw\_user_ duration _hh:mm:ss_ bytes _bytes_ _id\_port\_num_ _rx\_ring\_num_ \[(_user_)\]
    
-   (Inbound) %ASA-6-302020: Built _inbound_ ICMP connection for faddr _src\_ip\_address_/_src\_port__outside\_idfw\_user_ gaddr _dest\_ip\_address_/_dest\_port_ laddr _dest\_ip\_address_/_dest\_port__inside\_idfw\_user_ \[(_user_)\] type _type_ code _code_ Internal-Data0/_port\_num_:RX\[_rx\_ring\_num_\]
    
-   (Outbound) %ASA-6-302020: Built _outbound_ ICMP connection for faddr _dest\_ip\_address_/_dest\_port__outside\_idfw\_user_ gaddr _src\_ip_/_src\_port_ laddr _src\_ip_/_src\_port__inside\_idfw\_user_\[_(user)_\] type _type_ code _code_ Internal-Data0/_port\_num_:RX\[rx\_ring\_num\]
    
-   %ASA-6-302021: Teardown ICMP connection for faddr _src\_ip\_address_/_src\_port__outside\_idfw\_user_ gaddr _dest\_ip\_address_/_dest\_port_ laddr _dest\_ip\_address_/_dest\_port__inside\_idfw\_user_ \[(_user_)\] type _type_ code _code_ Internal-Data0/_port\_num_:RX\[_rx\_ring\_num_\]
    
-   %ASA-6-302022: Built _role__interface__real-address__real-port__mapped-address__mapped-port__interface__real-address__real-port__mapped-address__mapped-port)_
    
-   %ASA-6-302023: Teardown _stub__interface__real-address__real-port__interface__real-address__real-port__hh:mm:ss__bytes__reason_
    
-   %ASA-6-302024: Built _role__interface__real-address__real-port__mapped-address__mapped-port__interface__real-address__real-port__mapped-address__mapped-port_
    
-   %ASA-6-302025: Teardown _stub__interface__real-address__real-port__interface__real-address__real-port__hh:mm:ss__bytes__reason_
    
-   %ASA-6-302026: Built _role__interface__real-address__real-port__mapped-address__interface__real-address__real-port__mapped-address_
    
-   %ASA-6-302027: Teardown _stub__interface__real-address__real-port__interface__real-address__real-port__hh:mm:ss__bytes__reason_
    
-   %ASA-6-302033: Pre-allocated H323 GUP Connection for faddr _interface\_name_:_foreign\_ip\_address_ to laddr _interface\_name_:_local\_address_/_local\_port_
    
-   %ASA-6-302033: Pre-allocated H323 GUP Connection for faddr _interface\_name_:_foreign\_ip\_address_/_foreign\_port_ to laddr _interface\_name_:_local\_address_
    
-   %ASA-6-302035: Built {_inbound | outbound_} SCTP connection _conn\_id_ for _outside\_interface_:_outside\_ip_/_outside\_port_ (_mapped\_outside\_ip_/_mapped\_outside\_port_)_outside\_idfw\_user_ to _inside\_interface_:_inside\_ip_/_inside\_port_ (_mapped\_inside\_ip_/_mapped\_inside\_port_)_inside\_idfw\_user_ _port\_num_ _rx\_ring\_num_ \[(user)\]
    
-   %ASA-6-302036: Teardown SCTP connection _conn\_id_ for _inside\_interface_:_inside\_ip\_address_/_inside\_port__outside\_idfw\_user_ to _outside\_interface_:_outside\_ip\_address_/_outside\_port__inside\_idfw\_user_ duration _time\_value_ bytes _bytes_ _reason\_string_ _id\_port\_num_ _rx\_ring\_num_ \[(_user_)\]
    
-   %ASA-6-302037: Built {inbound|outbound} IPINIP connection _conn\_id_ from _outside\_interface_:_outside\_ip_/{_outside\_mapped\_ip|outside\_port_} _outside\_idfw\_user_ to _inside\_interface\_name_:_inside\_ip_/{_inside\_mapped\_ip|inside\_port_} _inside\_idfw\_user_ \[(_user_)\]
    
-   (Inbound flow)%ASA-6-302038: Teardown IPINIP connection _conn\_id_ for _inside\_interface_:_inside\_ip_/_inside\_port__outside\_idfw\_user_ to _outside\_interface_:_outside\_ip_/_outside\_port__inside\_idfw\_user_ duration _time\_value_ bytes _bytes_ \[(_user_)\]
    
-   (Outbound flow)%ASA-6-302038: Teardown IPINIP connection _conn\_id_ for _outside\_interface_:_outside\_ip_/_outside\_port__outside\_idfw\_user_ to _inside\_interface_:_inside\_ip_/_inside\_port__inside\_idfw\_user_ duration _time\_value_ bytes _bytes_ \[(_user_)\]
    
-   %ASA-6-302303: Built TCP state-bypass connection conn\_id from initiator\_interface:real\_ip/real\_port(mapped\_ip/mapped\_port) to responder\_interface:real\_ip/real\_port (mapped\_ip/mapped\_port)
    
-   %ASA-6-302304: Teardown TCP state-bypass connection conn\_id from initiator\_interface:ip/port to responder\_interface:ip/port duration, bytes, teardown reason.
    
-   %ASA-6-302305: Built SCTP state-bypass connection _conn\_id__outside\_interface__outside\_ip__outside\_port__mapped\_outside\_ip__mapped\_outside\_port__outside\_idfw\_user__outside\_sg\_info__inside\_interface__inside\_ip__inside\_port__mapped\_inside\_ip__mapped\_inside\_port__inside\_idfw\_user__inside\_sg\_info_
    
-   %ASA-6-302306: Teardown SCTP state-bypass connection _conn\_id__outside\_interface__outside\_ip__outside\_port__outside\_idfw\_user__outside\_sg\_info__inside\_interface__inside\_ip__inside\_port__inside\_idfw\_user__inside\_sg\_info__time__bytes__reason_
    
-   %ASA-6-303002: FTP connection from _src\_ifc__src\_ip__src\_port__dst\_ifc__dst\_ip__dst\_port__username__action__filename_
    
-   %ASA-6-304004: URL Server _IP\_address__url_
    
-   %ASA-6-305007: _addrpool\_free__IP\_address__interface\_number_
    
-   %ASA-6-305009: Built _{dynamic|static}__interface\_name \[(acl-name)\]__real\_address__idfw\_user__interface__name__mapped\_address_
    
-   %ASA-6-305010: Teardown _{dynamic|static}__interface\_name__real\_address_ _idfw\_user__interface__name__mapped\_address__time_
    
-   %ASA-6-305011: Built _{dynamic|static}__{TCP|UDP|ICMP}__interface\_name__real\_address__real\_port__idfw\_user__interface__name__mapped\_address__mapped\_port_
    
-   %ASA-6-305012: Teardown _interface\_name__acl-name__real\_address__real\_port__real\_ICMP\_ID__idfw\_user__interface\_name__mapped\_address__mapped\_port__mapped\_ICMP\_ID__time_
    
-   %ASA-6-305014: Allocated _num\_of\_blocks_ block of ports for translation from _real\_interface_:_real\_host\_ip_ to _real\_dest\_interface_:_real\_dest\_ip_/_real\_dest\_port\_start_\-_real\_dest\_port\_end_
    
-   %ASA-6-305015: Released _block\_size_ block of ports for translation from _real\_interface_:_real\_host\_ip_ to _real\_destination\_interface_:_real\_dest\_ip_/_port\_start_\-_port\_end_
    
-   %ASA-6-305018: MAP translation from _src\_ifc_:_src\_ip_/_src\_port_\-_dst\_ifc_:_dst\_ip_/_dst\_port_ to _src\_ifc_:_translated\_src\_ip_/_src\_port_\-_dst\_ifc_:_translated\_dst\_ip_/_dst\_port_
    
-   %ASA-6-308001: Console enable password incorrect for _number__IP\_address_
    
-   %ASA-6-311001: LU loading standby start
    
-   %ASA-6-311002: LU loading standby end
    
-   %ASA-6-311003: LU recv thread up
    
-   %ASA-6-311004: LU xmit thread up
    
-   %ASA-6-312001: RIP hdr failed from _IP\_address__string__number__string__interface\_name_
    
-   %ASA-6-314001: Pre-allocate RTSP UDP backconnection for _src\_intf__src\_IP__dst\_intf__dst\_IP__dst\_port._
    
-   %ASA-6-314002: RTSP failed to allocate UDP media connection from _src\_intf__src\_IP__dst\_intf__dst\_IP__dst\_port__reason\_string._
    
-   %ASA-6-314003: Dropped RTSP traffic from _src\_intf__src\_ip__reason_
    
-   %ASA-6-314004: RTSP client _src\_intf__src\_IP_ _RTSP URL_
    
-   %ASA-6-314005: RTSP client _src\_intf__src\_IP_ _RTSP\_URL._
    
-   %ASA-6-314006: RTSP client _src\_intf__src\_IP__rate_ _request\_method_
    
-   %ASA-6-315011: SSH session from _remote\_ip\_address_ on interface _interface\_name_ for user \\'_user\_name_\\' terminated normally
    
-   %ASA-6-315011: SSH session from _remote\_ip\_address_ on interface _interface\_name_ for user \\'_user\_name_\\' terminated
    
-   %ASA-6-315011: SSH session from _remote\_ip\_address_ on interface _interface\_name_ for user \\'_user\_name_\\' disconnected by SSH server, reason: \\'_reason\_string_\\' (_reason\_state_)
    
-   %ASA-6-315013: SSH session from _SSH client address__interface name__user name_
    
-   %ASA-6-317007: Added route\_type route dest\_address netmask via gateway\_address \[distance/metric\] on interface\_name route\_type
    
-   %ASA-6-317008: Community list check with bad list _list\_number_
    
-   %ASA-6-317077: Added _protocol\_name_ route _destination\_address_ _subnet-mask_ via _gateway-address_ \[_admin\_distance_/_metric_\] on \[_inf\_name_\] \[_vrf\_name_\] tableid \[_table\_id_\]
    
-   %ASA-6-317078: Deleted _protocol\_name_ route _destination\_address_ _subnet-mask_ via _gateway-address_ \[_admin\_distance_/_metric_\] on \[_inf\_name_\] \[_vrf\_name_\] tableid \[_table\_id_\]
    
-   %ASA-6-317079: Added static route _destination\_address_ \[_admin\_distance/metric_\] via _inf\_name_ tableid \[_table\_id_\]
    
-   %ASA-6-317080: Deleted static route _destination\_address_ \[_admin\_distance/metric_\] via _inf\_name_ tableid \[_table\_id_\]
    
-   %ASA-6-321003: Resource var1 log level of var2 reached.
    
-   %ASA-6-321004: Resource var1 rate log level of var2 reached
    
-   %ASA-6-322004: No management IP address configured for transparent firewall. Dropping protocol _protocol__interface\_in__source\_address__source\_port__interface\_out__dest\_address__dest\_port_
    
-   %ASA-6-324303: Server=IPaddr:port ID=id The RADIUS server supports and included the Message-Authenticator payload in its response. To prevent Man-In-The-Middle attacks, consider enabling ‘ message-authenticator’ on the aaa-server-group configuration for this server as a security best practice.
    
-   %ASA-6-333001: EAP association initiated - context:EAP-context
    
-   %ASA-6-333003: EAP association terminated - context:EAP-context
    
-   %ASA-6-333009: EAP-SQ response MAC TLV is invalid - context:EAP-context
    
-   %ASA-6-334001: EAPoUDP association initiated - host-address
    
-   %ASA-6-334004: Authentication request for NAC Clientless host - host-address
    
-   %ASA-6-334007: EAPoUDP association terminated - host-address
    
-   %ASA-6-334008: NAC EAP association initiated - host-address, EAP context:EAP-context
    
-   %ASA-6-334009: Audit request for NAC Clientless host - Assigned\_IP.
    
-   %ASA-6-335001: NAC session initialized - host-address
    
-   %ASA-6-335004: NAC is disabled for host - host-address
    
-   %ASA-6-335006: NAC Applying ACL:ACL-name - host-address
    
-   %ASA-6-335009: NAC 'Revalidate' request by administrative action - host-address
    
-   %ASA-6-335010: NAC 'Revalidate All' request by administrative action - num sessions
    
-   %ASA-6-335011: NAC 'Revalidate Group' request by administrative action for group-name group - num sessions
    
-   %ASA-6-335012: NAC 'Initialize' request by administrative action - host-address
    
-   %ASA-6-335013: NAC 'Initialize All' request by administrative action - num sessions
    
-   %ASA-6-335014: NAC 'Initialize Group' request by administrative action for group-name group - num sessions
    
-   %ASA-6-336011: hw or sw error occurred
    
-   %ASA-6-337000: Session created, NeighAddr: _Created BFD session with local discriminator _id_, SrcAddr: _real\_interface__
    
-   %ASA-6-337001: Session destroyed, NeighAddr: _Terminated BFD session with local discriminator _id_, SrcAddr: _real\_interface__
    

-   %ASA-6-338304: Successfully downloaded dynamic filter data file from updater server _url_
    
-   %ASA-6-339010: Umbrella API token request was successful.
    
-   %ASA-6-340002: Vnet-proxy data relay error _error\_string__context\_id__version__request\_type__address\_type__client\_address\_internal__client\_port\_internal_
    
-   %ASA-6-341001: Policy Agent started successfully for VNMC _vnmc\_ip\_addr_
    
-   %ASA-6-341002: Policy Agent stopped successfully for VNMC _vnmc\_ip\_addr_
    
-   %ASA-6-341010: Storage device with serial number _ser\_no__\[inserted into | removed from\]__bay\_no_
    
-   %ASA-6-402129: CRYPTO: An attempt to release a DMA memory block failed, location: _address_
    
-   %ASA-6-402130: CRYPTO: Received an ESP packet (SPI = xxxxxxxxxx, sequence number=xxxx) from 172.16.0.1 (user=user) to 192.168.0.2 with incorrect IPsec padding.
    
-   %ASA-6-403500: PPPoE - Service name 'any' not received in _interface\_name__ac\_name_
    
-   %ASA-6-410004: _action\_class__action__query\_response__src\_ifc__sip__sport__dest\_ifc__dip__dport_
    
-   %ASA-6-414004: TCP Syslog Server _intf__IP\_Address__port_
    
-   %ASA-6-414007: TCP syslog server connection restored. New connections allowed.
    
-   %ASA-6-414008: New connections are now allowed due to change of logging permit-hostdown policy.
    
-   %ASA-6-414009: TCP syslog server connection removed. New connections allowed.
    
-   %ASA-6-415001: HTTP - matched _matched\_string__map\_name__connection\_action__int\_type__IP\_address__port\_num__int\_type__IP\_address__port\_num_
    
-   %ASA-6-415002: HTTP - matched _matched\_string__map\_name__connection\_action__int\_type__IP\_address__port\_num__int\_type__IP\_address__port\_num_
    
-   %ASA-6-415003: HTTP - matched _matched\_string__map\_name__connection\_action__int\_type__IP\_address__port\_num__int\_type__IP\_address__port\_num_
    
-   %ASA-6-415017: HTTP - matched _matched\_string__map\_name__connection\_action__int\_type__IP\_address__port\_num__int\_type__IP\_address__port\_num_
    
-   %ASA-6-419004: TCP connection _ID_ from _src\_ifc_:_src\_ip_/_src\_port_ (_src\_ip_/_src\_port_) to _dst\_ifc_:_dst\_ip_/_dst\_port_ (_dst\_ip_/_dst\_port_) is probed by DCD
    
-   %ASA-6-419005: TCP connection _ID_ from _src\_ifc_:_src\_ip_/_src\_port_ (_src\_ip_/_src\_port_) to _dest\_ifc_:_des\_ip_/_des\_port_ (_des\_ip_/_des\_port_) duration _hh:mm:ss_ data _bytes_, is kept open by DCD as valid connection
    
-   %ASA-6-419006: Teardown TCP connection _ID_ from _src\_ifc_:_src\_ip_/_src\_port_ (_src\_ip_/_src\_port_) to _dst\_ifc_:_dst\_ip_/_dst\_port_ (_dst\_ip_/_dst\_port_) duration _hh:mm:ss_ data _bytes_, DCD probe was not responded from _client/server_ interface _ifc\_name_
    
-   %ASA-6-420004: Virtual Sensor _sensor\_name_
    
-   %ASA-6-420005: Virtual Sensor _sensor\_name_
    
-   %ASA-6-421002: TCP|UDP flow from interface\_name:IP\_address/port to interface\_nam:IP\_address/port bypassed application checking because the protocol is not supported.
    
-   %ASA-6-421005: _interface\_name__IP\_address__application_
    
-   %ASA-6-421006: There are _number__application_
    
-   %ASA-6-425001 Redundant interface redundant\_interface\_name created.
    
-   %ASA-6-425002 Redundant interface redundant\_interface\_name removed.
    
-   %ASA-6-425003 Interface interface\_name added into redundant interface redundant\_interface\_name.
    
-   %ASA-6-425004 Interface interface\_name removed from redundant interface redundant\_interface\_name.
    
-   %ASA-6-426001: PORT-CHANNEL:Interface _ifc\_name__num_
    
-   %ASA-6-426002: PORT-CHANNEL:Interface _ifc\_name__num_
    
-   %ASA-6-426003: PORT-CHANNEL:Interface _ifc\_name1__num_
    
-   %ASA-6-426101: PORT-CHANNEL:Interface _ifc\_name__port-channel id_
    
-   %ASA-6-426102: PORT-CHANNEL:Interface _ifc\_name__port-channel id_
    
-   %ASA-6-426103: PORT-CHANNEL:Interface _ifc\_name__port-channel id_
    
-   %ASA-6-426104: PORT-CHANNEL:Interface _ifc\_name__port-channel id_
    
-   %ASA-6-428001: WAAS confirmed from in\_interface:src\_ip\_addr/src\_port to out\_interface:dest\_ip\_addr/dest\_port, inspection services bypassed on this connection
    
-   %ASA-6-429005: Set up _protocol\_type__interface\_name__ip\_address__port__policy\_type_
    
-   %ASA-6-429006: Cleaned up authentication-proxy rule for the cxsc action on interface _interface\_name__ip\_address__policy\_type_
    
-   %ASA-6-444103: Shared _licensetype_
    
-   %ASA-6-444104: Shared _licensetype__value_
    
-   %ASA-6-444107: Shared license service _status__ifname_
    
-   %ASA-6-444108: Shared license _state__id_
    
-   %ASA-6-444306: %SMART\_LIC-6-AGENT\_READY: Smart Agent for Licensing is initialized.
    
-   %ASA-6-444306: %SMART\_LIC-6-AGENT\_ENABLED: Smart Agent for Licensing is enabled.
    
-   %ASA-6-444306: %SMART\_LIC-6-AGENT\_REG\_SUCCESS: Smart Agent for Licensing Registration with Cisco licensing cloud successful.
    
-   %ASA-6-444306: %SMART\_LIC-6-AGENT\_DEREG\_SUCCESS: Smart Agent for Licensing De-registration with Cisco licensing cloud successful.
    
-   %ASA-6-444306: %SMART\_LIC-6-DISABLED: Smart Agent for Licensing disabled.
    
-   %ASA-6-444306: %SMART\_LIC-6-ID\_CERT\_RENEW\_SUCCESS: Identity certificate renewal successful.
    
-   %ASA-6-444306: %SMART\_LIC-6-ENTITLEMENT\_RENEW\_SUCCESS: Entitlement authorization renewal with Cisco licensing cloud successful.
    
-   %ASA-6-444306: %SMART\_LIC-6-AUTH\_RENEW\_SUCCESS: Authorization renewal with Cisco licensing cloud successful.
    
-   %ASA-6-444306: %SMART\_LIC-6-HA\_ROLE\_CHANGED: Smart Agent HA role changed to role.
    
-   %ASA-6-444306: %SMART\_LIC-6-HA\_CHASSIS\_ROLE\_CHANGED: Smart Agent HA chassis role changed to role.
    
-   %ASA-6-444306: %SMART\_LIC-6-AGENT\_ALREADY\_REGISTER: Smart Agent is already registered with the Cisco licensing cloud.
    
-   %ASA-6-444306: %SMART\_LIC-6-AGENT\_ALREADY\_DEREGISTER: Smart Agent is already Deregistered with the CSSM.
    
-   %ASA-6-444306: %SMART\_LIC-6-EXPORT\_CONTROLLED: Usage of export controlled features is status.
    
-   %ASA-6-602101: PMTU-D packet _number__number__dest\_address__source\_address__protocol_
    
-   %ASA-6-602103: IPSEC: Received an ICMP Destination Unreachable from _src\_addr__rcvd\_mtu__peer\_addr__spi__username__old\_mtu__new\_mtu_
    
-   %ASA-6-602104: IPSEC: Received an ICMP Destination Unreachable from _src\_addr__rcvd\_mtu__curr\_mtu__peer\_addr__spi__username_
    
-   %ASA-6-602303: IPSEC: An _direction_ _tunnel\_type__spi__local\_IP__remote\_IP__username_
    
-   %ASA-6-602304: IPSEC: An _direction__tunnel\_type__spi__local\_IP__remote\_IP__username_
    
-   %ASA-6-603101: PPTP received out of seq or duplicate pkt, tnl\_id=_number__number__number_
    
-   %ASA-6-603102: PPP virtual interface _interface\_name__user_
    
-   %ASA-6-603103: PPP virtual interface _interface\_name__user__status_
    
-   %ASA-6-603104: PPTP Tunnel created, tunnel\_id is _number__remote\_address__number__IP\_address__user__string_
    
-   %ASA-6-603105: PPTP Tunnel deleted, tunnel\_id = _number__remote\_address_
    
-   %ASA-6-603106: L2TP Tunnel created, tunnel\_id is _number__remote\_address__number__IP\_address__user_
    
-   %ASA-6-603107: L2TP Tunnel deleted, tunnel\_id = _number__remote\_address_
    
-   %ASA-6-603108: Built PPPOE Tunnel, tunnel\_id = _interface\_name__number__IP\_address__number__IP\_address_
    
-   %ASA-6-603109: Teardown PPPOE Tunnel, tunnel\_id = _interface\_name__number_
    
-   %ASA-6-604101: DHCP client interface _interface\_name__IP\_address_ _netmask__gateway\_address_
    
-   %ASA-6-604102: DHCP client interface _interface\_name_
    
-   %ASA-6-604103: DHCP daemon interface _interface\_name__MAC\_address__IP\_address_
    
-   %ASA-6-604104: DHCP daemon interface _interface\_name__build\_number__IP\_address_
    
-   %ASA-6-604201: DHCPv6 PD client on interface _pd-client-iface_ received delegated prefix _prefix_/_prefix_ from DHCPv6 PD server _server-address_ with preferred lifetime _in-seconds_ seconds and valid lifetime _in-seconds_ seconds
    
-   %ASA-6-604202: DHCPv6 PD client on interface _pd-client-iface_ releasing delegated prefix _prefix_/_prefix_ received from DHCPv6 PD server _server-address_
    
-   %ASA-6-604203: DHCPv6 PD client on interface _pd-client-iface_ renewed delegated prefix _prefix_/_prefix_ from DHCPv6 PD server _server-address_ with preferred lifetime _in-seconds_ seconds and valid lifetime _in-seconds_ seconds
    
-   %ASA-6-604204: DHCPv6 delegated prefix _delegated prefix_/_prefix_ got expired on interface _pd-client-iface_, received from DHCPv6 PD server _server-address_
    
-   %ASA-6-604205: DHCPv6 client on interface _client-iface_ allocated address _ipv6-address_ from DHCPv6 server _server-address_ with preferred lifetime _in-seconds_ seconds and valid lifetime _in-seconds_ seconds
    
-   %ASA-6-604206: DHCPv6 client on interface _client-iface_ releasing address _ipv6-address_ received from DHCPv6 server _server-address_
    
-   %ASA-6-604207: DHCPv6 client on interface _client-iface_ renewed address _ipv6-address_ from DHCPv6 server _server-address_ with preferred lifetime _in-seconds_ seconds and valid lifetime _in-seconds_ seconds
    
-   %ASA-6-604208: DHCPv6 client address _ipv6-address_ got expired on interface _client-iface_, received from DHCPv6 server _server-address_
    
-   %ASA-6-605004: Login denied from _source\_ip\_address_/_source\_port_ to _interface_:_destination\_ip\_address_/_service\_name_ for user \\'_username_\\'
    
-   %ASA-6-605004: Login denied from _serial_ to _console_ for user \\'_username_\\'
    
-   %ASA-6-605005: Login permitted from _source\_ip\_address_/_source\_port_ to _interface_:_destination\_ip\_address_/_service\_name_ for user \\'_username_\\'
    
-   %ASA-6-605005: Login permitted from _serial_ to _console_ for user \\'_username_\\'
    
-   %ASA-6-606001: ASDM session number _number__IP\_address_
    
-   %ASA-6-606002: ASDM session number _number__IP\_address_
    
-   %ASA-6-606003: ASDM logging session number _id__IP\_address_
    
-   %ASA-6-606004: ASDM logging session number _id__IP\_address_
    
-   %ASA-6-607001: Pre-allocate SIP _connection\_type_ secondary channel for _interface\_name_:_ip\_address_ to _interface\_name_:_ip\_address_/_port_ from _message\_string_ message
    
-   %ASA-6-607001: Pre-allocate SIP _connection\_type_ secondary channel for _interface\_name_:_ip\_address_/_port_ to _interface\_name_:_ip\_address_ from _message\_string_ message
    
-   %ASA-6-607003: _action\_class__req\_resp__req\_resp\_info__src\_ifc__sip__sport__dest\_ifc__dip__dport__further\_info_
    
-   %ASA-6-608001: Pre-allocate Skinny connection\_type secondary channel for interface\_name:IP\_address to interface\_name:IP\_address from string message
    
-   %ASA-6-610101: Authorization failed: Cmd: _command__command\_modifier_
    
-   %ASA-6-611101: User authentication succeeded: IP address: _IP address__user_
    
-   %ASA-6-611102: User authentication failed: IP address: _IP address,_ _user_
    
-   %ASA-6-611301: VPNClient: NAT configured for Client Mode with no split tunneling: NAT addr: _mapped\_address_
    
-   %ASA-6-611302: VPNClient: NAT exemption configured for Network Extension Mode with no split tunneling
    
-   %ASA-6-611303: VPNClient: NAT configured for Client Mode with split tunneling: NAT addr: _mapped\_address__IP\_address_
    
-   %ASA-6-611304: VPNClient: NAT exemption configured for Network Extension Mode with split tunneling: Split Tunnel Networks: _IP\_address_
    
-   %ASA-6-611305: VPNClient: DHCP Policy installed: _IP\_address_
    
-   %ASA-6-611306: VPNClient: Perfect Forward Secrecy Policy installed
    
-   %ASA-6-611307: VPNClient: Head end : _IP\_address_
    
-   %ASA-6-611308: VPNClient: Split DNS Policy installed: List of domains: _string string_
    
-   %ASA-6-611309: VPNClient: Disconnecting from head end and uninstalling previously downloaded policy: Head End : _IP\_address_
    
-   %ASA-6-611310: VPNClient: XAUTH Succeeded: Peer: _IP\_address_
    
-   %ASA-6-611311: VPNClient: XAUTH Failed: Peer: _IP\_address_
    
-   %ASA-6-611312: VPNClient: Backup Server List: _reason_
    
-   %ASA-6-611314: VPNClient: Load Balancing Cluster with Virtual IP: _IP\_address__IP\_address_
    
-   %ASA-6-611315: VPNClient: Disconnecting from Load Balancing Cluster member _IP\_address_
    
-   %ASA-6-611316: VPNClient: Secure Unit Authentication Enabled
    
-   %ASA-6-611317: VPNClient: Secure Unit Authentication Disabled
    
-   %ASA-6-611318: VPNClient: User Authentication Enabled: Auth Server IP: _IP\_address__port__time_
    
-   %ASA-6-611319: VPNClient: User Authentication Disabled
    
-   %ASA-6-611320: VPNClient: Device Pass Through Enabled
    
-   %ASA-6-611321: VPNClient: Device Pass Through Disabled
    
-   %ASA-6-611322: VPNClient: Extended XAUTH conversation initiated when SUA disabled
    
-   %ASA-6-611323: VPNClient: Ignoring duplicate split network entry _network\_address_/_network\_mask_
    
-   %ASA-6-613001: Bad checksum _string_ from _IP\_address_ on _number_
    
-   %ASA-6-613002: Interface _interface\_name_ has zero bandwidth configuration
    
-   %ASA-6-613003: Network range _IP\_address netmask_ changed from area _string_ to _string_
    
-   %ASA-6-613014: Base topology enabled on interface string attached to MTR compatible mode area string
    
-   %ASA-6-613027: OSPF process number removed from interface interface\_name
    
-   %ASA-6-613028: Unrecognized virtual interface intetface\_name. Treat it as loopback stub route
    
-   %ASA-6-613041: OSPF-100 Areav string: LSA ID IP\_address, Type number, Adv-rtr IP\_address, LSA counter DoNotAge
    
-   %ASA-6-613043:
    
-   %ASA-6-613104: Unrecognized virtual interface %IF\_NAME.
    
-   %ASA-6-614001: Split DNS: request patched from server: _IP\_address_ _IP\_address_
    
-   %ASA-6-614002: Split DNS: reply from server: _IP\_address__IP\_address_
    
-   %ASA-6-615001: vlan _number_
    
-   %ASA-6-615002: vlan _number_
    
-   %ASA-6-616001: Pre-allocate MGCP _data\_channel__inside\_interface__inside\_address__outside\_interface__outside\_address__port__message\_type message_
    
-   %ASA-6-617001: GTPv_(version)_ _msg\_type_ from _dest\_interface_:_dest\_address_/_dest\_port_ not accepted by _source\_interface_:_source\_address_/_source\_port_, Cause: value _cause\_info_ (_cause\_string_)
    
-   %ASA-6-617002: Removing v0 PDP Context with TID _tid_ from GGSN _ip\_address_ and SGSN _ip\_address_, Cause: value _error\_code_ (_string_), Reason: _reason_
    
-   %ASA-6-617002: Removing v1 {_primary | secondary_} PDP Context with TID _tid_ from GGSN _ip\_address_ and SGSN _ip\_address_, Cause: value _error\_code_ (_string_), Reason: _reason_
    
-   %ASA-6-617002: Removing v2 {_primary | secondary_} PDP Context with TID _tid_ from PGW _ip\_address_ and SGW _ip\_address_, Cause: value _error\_code_ (_string_), Reason: _reason_
    
-   %ASA-6-617003: GTP Tunnel created from _source\_interface__source\_address__source\_port__source\_interface__dest\_address_
    
-   %ASA-6-617004: GTP connection created for response from _source\_interface__source\_address__0__source\_interface__dest\_address_
    
-   %ASA-6-617100: Teardown _num\_conns__user\_ip_
    
-   %ASA-6-618001: Denied STUN packet _msg\_type_ from _inside\_ifc_:_source\_addr_/_source\_port_ to _outside\_ifc_:_destination\_addr_/_destination\_port_ for connection _conn\_id_, malformed message header
    
-   %ASA-6-618001: Denied STUN packet _msg\_type_ from _inside\_ifc_:_source\_addr_/_source\_port_ to _outside\_ifc_:_destination\_addr_/_destination\_port_ for connection _conn\_id_, translation id doesn't match previous entry
    
-   %ASA-6-620001: Pre-allocate CTIQBE {_RTP | RTCP_} channel for _interface\_name_:_outside\_address_ to _interface\_name_:_inside\_address_/_inside\_port_ from _message\_name_ message
    
-   %ASA-6-620001: Pre-allocate CTIQBE {_RTP | RTCP_} channel for _interface\_name_:_outside\_address_/_outside\_port_ to _interface\_name_:_inside\_address_ from _message\_name_ message
    
-   %ASA-6-621001: Interface interface\_name does not support multicast, not enabled
    
-   %ASA-6-621002: Interface interface\_name does not support multicast, not enabled
    
-   %ASA-6-621003: The event queue size has exceeded number
    
-   %ASA-6-621006: Mrib disconnected, (IP\_address, IP\_address) event cancelled
    
-   %ASA-6-621007: Bad register from interface\_name:IP\_address to IP\_address for (IP\_address, IP\_address)
    
-   %ASA-6-622001: _action_ tracked route _destination\_network_ _netmask_ _nexthop\_address_, distance _admin\_distance_, table _routing\_table\_name_, on interface _interface\_name_
    
-   %ASA-6-622101: Starting regex table compilation for _match\_command_, table entries = _regex\_num_ entries
    
-   %ASA-6-622102: Completed regex table compilation for _match\_command_, table size = _num_ bytes
    
-   %ASA-6-634001: DAP: User user, Addr ipaddr, Connection connection; The following DAP records were selected for this connection: DAP Record names
    
-   %ASA-6-709009: (unit-role) Configuration on Active and Standby is matching. No config sync. Time elapsed <time-elapsed> ms
    
-   %ASA-6-709010: Configuration between units doesn't match. Going for config sync (_sync-string_). Time elapsed _time-elapsed_ ms
    
-   %ASA-6-709011: Failover configuration replication completed in _time_ ms
    
-   %ASA-6-709012: Skip configuration replication from mate as configuration on Active and Standby is matching
    
-   %ASA-6-713124: Group = _groupname_, Username = _username_, IP = _peerIP_ Received DPD sequence number _rcv\_sequence\_#_ in _DPD Action, description expected seq #_
    
-   %ASA-6-713128: IP = _peerIP_ Connection attempt to VCPIP redirected to VCA peer _IP\_address_ via load balancing
    
-   %ASA-6-713145: Group = _groupname_, Username = _username_, IP = _peerIP_ Detected Hardware Client in network extension mode, adding static route for address: _IP\_address_, mask: _netmask_
    
-   %ASA-6-713147: Group = _groupname_, Username = _username_, IP = _peerIP_ Terminating tunnel to Hardware Client in network extension mode, deleting static route for address: _IP\_address_, mask: _netmask_
    
-   %ASA-6-713172: Group = _groupname_, Username = _username_, IP = _peerIP_ Automatic NAT Detection Status: Remote end _is_ |_is not_ behind a NAT device This end _is_ |_is not_ behind a NAT device
    
-   %ASA-6-713177: Group = _groupname_, Username = _username_, IP = _peerIP_ Received remote Proxy Host FQDN in ID Payload: Host Name: _host\_name_ Address _IP\_address_, Protocol _protocol_, Port _port_
    
-   %ASA-6-713184: Group = _groupname_, Username = _username_, IP = _peerIP_ Client Type: _Client\_type_ Client Application Version: _Application\_version\_string_
    
-   %ASA-6-713211: Group = _groupname_, Username = _username_, IP = _peerIP_ Adding static route for L2L peer coming in on a dynamic map. address: _IP\_address_, mask: _netmask_
    
-   %ASA-6-713213: Group = _groupname_, Username = _username_, IP = _peerIP_ Deleting static route for L2L peer that came in on a dynamic map. address: _IP\_address_, mask: _netmask_
    
-   %ASA-6-713215: Group = _groupname_, Username = _username_, IP = _peerIP_ No match against Client Type and Version rules. Client: _type version is_ /_is_ not allowed by default
    
-   %ASA-6-713219: Group = _groupname_, Username = _username_, IP = _peerIP_ Queuing KEY-ACQUIRE messages to be processed when P1 SA is complete.
    
-   %ASA-6-713220: Group = _groupname_, Username = _username_, IP = _peerIP_ De-queuing KEY-ACQUIRE messages that were left pending.
    
-   %ASA-6-713228: Group = _group_, Username = _uname_, IP = _remote\_IP\_address_ Assigned private IP address _assigned\_private\_IP_ to remote user
    
-   %ASA-6-713235: Group = _groupname_, Username = _username_, IP = _peerIP_ Attempt to send an IKE packet from standby unit. Dropping the packet!
    
-   %ASA-6-713256: IP = _peer-IP_ IP = _peer-IP_, Sending spoofed ISAKMP Aggressive Mode message 2 due to receipt of unknown tunnel group. Aborting connection.
    
-   %ASA-6-713265: Group = _groupname_, Username = _username_, IP = _peerIP_ Adding static route for L2L peer coming in on a dynamic map. address: _IP\_address_, mask: /_prefix\_len_
    
-   %ASA-6-713267: Group = _groupname_, Username = _username_, IP = _peerIP_ Deleting static route for L2L peer that came in on a dynamic map. address: _IP\_address_, mask: /_prefix\_len_
    
-   %ASA-6-713269: Group = _groupname_, Username = _username_, IP = _peerIP_ Detected Hardware Client in network extension mode, adding static route for address: _IP\_address_, mask: /_prefix\_len_
    
-   %ASA-6-713271: Group = _groupname_, Username = _username_, IP = _peerIP_ Terminating tunnel to Hardware Client in network extension mode, deleting static route for address: _IP\_address_, mask:/_prefix\_len_
    
-   %ASA-6-713273: Group = _groupname_, Username = _username_, IP = _peerIP_ Deleting static route for client address: _IP\_Address IP\_Address_ address of client whose route is being removed
    
-   %ASA-6-713905: Descriptive\_event\_string.
    
-   %ASA-6-716001: Group _group__user__ip_
    
-   %ASA-6-716002: Group _GroupPolicy__username__ip__User Requested_
    
-   %ASA-6-716003: Group _group__user__ip__url__string__string_
    
-   %ASA-6-716004: Group _group__user__ip__url__string__string_
    
-   %ASA-6-716005: Group _group__user__ip__reason__string_
    
-   %ASA-6-716006: Group _name__user__iP_
    
-   %ASA-6-716009: Group _group__user__IP_
    
-   %ASA-6-716038: Group _group__user__ip_
    
-   %ASA-6-716039: Group _name__user__ip__session-type_
    
-   %ASA-6-716040: Reboot pending, new sessions disabled. Denied user login.
    
-   %ASA-6-716041: access-list _acl\_ID_ _action__url__count_
    
-   %ASA-6-716042: access-list _acl\_ID__action__source\_interface__source\_address__source\_port__dest\_interface__dest\_address__dest\_port__count_
    
-   %ASA-6-716043 Group group-name, User user-name, IP IP\_address: WebVPN Port Forwarding Java applet started. Created new hosts file mappings
    
-   %ASA-6-716049: Group _group-name__user-name__IP\_address_
    
-   %ASA-6-716050: Error adding to ACL: _ace\_command\_line_
    
-   %ASA-6-716051: Group _group-name__user-name__IP\_address_
    
-   %ASA-6-716055: Group group-name User user-name IP IP\_address Authentication to SSO server name: name type type succeeded
    
-   %ASA-6-716058: Group _group__user__ip_
    
-   %ASA-6-716059: Group _group__user__ip__ip2_
    
-   %ASA-6-716060: Group _group__user__ip_
    
-   %ASA-6-717003: Certificate received from Certificate Authority for trustpoint _trustpoint\_name_
    
-   %ASA-6-717004: PKCS #12 export failed for trustpoint _trustpoint\_name_
    
-   %ASA-6-717005: PKCS #12 export succeeded for trustpoint _trustpoint\_name_
    
-   %ASA-6-717006: PKCS #12 import failed for trustpoint _trustpoint\_name_
    
-   %ASA-6-717007: PKCS #12 import succeeded for trustpoint _trustpoint\_name_
    
-   %ASA-6-717016: Removing expired CRL from the CRL cache. Issuer: _issuer_
    
-   %ASA-6-717022: Certificate was successfully validated. _certificate\_identifiers_
    
-   %ASA-6-717028: Certificate chain was successfully validated _additional info_
    
-   %ASA-6-717033: OCSP response received.
    
-   %ASA-6-717043: Local CA Server certificate enrollment related info for user: _user__info_
    
-   %ASA-6-717047: Revoked certificate issued to user: _username,__serial number_
    
-   %ASA-6-717048: Unrevoked certificate issued to user: _username,__serial number_
    
-   %ASA-6-717056: Attempting _type__Src__Interface__Src__IP__Src Port__Dst IP_
    
-   %ASA-6-717058: Automatic import of trustpool certificate bundle is successful: _No change in trustpool bundle | Trustpool updated in flash_
    
-   %ASA-6-717059: Peer certificate with _serial number: serial, subject: subject\_name, issuer: issuer\_name_ matched the configured certificate map _map\_name_
    
-   %ASA-6-718003: Got unknown peer message \[_message\_number__IP\_address__version\_number__version\_number_
    
-   %ASA-6-718004: Got unknown internal message \[_message\_number_
    
-   %ASA-6-718013: Peer\[_IP\_address_
    
-   %ASA-6-718027: Received unexpected KEEPALIVE request from \[_IP\_address_
    
-   %ASA-6-718030: Received planned OOS from \[_IP\_address_
    
-   %ASA-6-718037: Master processed _number\_of\_timeouts_
    
-   %ASA-6-718038: Slave processed _number\_of\_timeouts_
    
-   %ASA-6-718039: Process dead peer\[_IP\_address_
    
-   %ASA-6-718040: Timed-out exchange ID\[_exchange\_ID_
    
-   %ASA-6-718051: Deleted secure tunnel to peer\[_IP\_address_
    
-   %ASA-6-719001: Email Proxy session could not be established: session limit of maximum\_sessions has been reached.
    
-   %ASA-6-719003: Email Proxy session pointer resources have been freed for source\_address.
    
-   %ASA-6-719004: Email Proxy session pointer has been successfully established for source\_address.
    
-   %ASA-6-719010: protocol Email Proxy feature is disabled on interface interface\_name.
    
-   %ASA-6-719011: Protocol Email Proxy feature is enabled on interface interface\_name.
    
-   %ASA-6-719012: Email Proxy server listening on port port for mail protocol protocol.
    
-   %ASA-6-719013: Email Proxy server closing port port for mail protocol protocol.
    
-   %ASA-6-719017: WebVPN user: vpnuser invalid dynamic ACL.
    
-   %ASA-6-719018: WebVPN user: vpnuser ACL ID acl\_ID not found
    
-   %ASA-6-719019: WebVPN user: vpnuser authorization failed.
    
-   %ASA-6-719020: WebVPN user vpnuser authorization completed successfully.
    
-   %ASA-6-719021: WebVPN user: vpnuser is not checked against ACL.
    
-   %ASA-6-719022: WebVPN user vpnuser has been authenticated.
    
-   %ASA-6-719023: WebVPN user vpnuser has not been successfully authenticated. Access denied.
    
-   %ASA-6-719024: Email Proxy piggyback auth fail: session = pointer user=vpnuser addr=source\_address
    
-   %ASA-6-719025: Email Proxy DNS name resolution failed for hostname.
    
-   %ASA-6-719026: Email Proxy DNS name hostname resolved to IP\_address.
    
-   %ASA-6-720002: (VPN-unit) Starting VPN Stateful Failover Subsystem...
    
-   %ASA-6-720003: (VPN-unit) Initialization of VPN Stateful Failover Component completed successfully
    
-   %ASA-6-720004: (VPN-unit) VPN failover main thread started.
    
-   %ASA-6-720005: (VPN-unit) VPN failover timer thread started.
    
-   %ASA-6-720006: (VPN-unit) VPN failover sync thread started.
    
-   %ASA-6-720010: (VPN-unit) VPN failover client is being disabled
    
-   %ASA-6-720012: (VPN-unit) Failed to update IPSec failover runtime data on the standby unit.
    
-   %ASA-6-720014: (VPN-unit) Phase 2 connection entry (msg\_id=message\_number, my cookie=mine, his cookie=his) contains no SA list.
    
-   %ASA-6-720015: (VPN-unit) Cannot found Phase 1 SA for Phase 2 connection entry (msg\_id=message\_number, my cookie=mine, his cookie=his).
    
-   %ASA-6-720023: (VPN-unit) HA status callback: Peer is not present.
    
-   %ASA-6-720024: (VPN-unit) HA status callback: Control channel is status.
    
-   %ASA-6-720025: (VPN-unit) HA status callback: Data channel is status.
    
-   %ASA-6-720026: (VPN-unit) HA status callback: Current progression is being aborted.
    
-   %ASA-6-720027: (VPN-unit) HA status callback: My state state.
    
-   %ASA-6-720028: (VPN-unit) HA status callback: Peer state state.
    
-   %ASA-6-720029: (VPN-unit) HA status callback: Start VPN bulk sync state.
    
-   %ASA-6-720030: (VPN-unit) HA status callback: Stop bulk sync state.
    
-   %ASA-6-720032: (VPN-unit) HA status callback: id=ID, seq=sequence\_#, grp=group, event=event, op=operand, my=my\_state, peer=peer\_state.
    
-   %ASA-6-720037: (VPN-unit) HA progression callback: id=id,seq=sequence\_number,grp=group,event=event,op=operand, my=my\_state,peer=peer\_state.
    
-   %ASA-6-720039: (VPN-unit) VPN failover client is transitioning to active state
    
-   %ASA-6-720040: (VPN-unit) VPN failover client is transitioning to standby state.
    
-   %ASA-6-720045: (VPN-unit) Start bulk syncing of state information on standby unit.
    
-   %ASA-6-720046: (VPN-unit) End bulk syncing of state information on standby unit
    
-   %ASA-6-720056: (VPN-unit) VPN Stateful failover Message Thread is being disabled.
    
-   %ASA-6-720057: (VPN-unit) VPN Stateful failover Message Thread is enabled.
    
-   %ASA-6-720058: (VPN-unit) VPN Stateful failover Timer Thread is disabled.
    
-   %ASA-6-720059: (VPN-unit) VPN Stateful failover Timer Thread is enabled.
    
-   %ASA-6-720060: (VPN-unit) VPN Stateful failover Sync Thread is disabled.
    
-   %ASA-6-720061: (VPN-unit) VPN Stateful failover Sync Thread is enabled.
    
-   %ASA-6-720062: (VPN-unit) Active unit started bulk sync of state information to standby unit.
    
-   %ASA-6-720063: (VPN-unit) Active unit completed bulk sync of state information to standby.
    
-   %ASA-6-721001: (device) WebVPN Failover SubSystem started successfully.(device) either WebVPN-primary or WebVPN-secondary.
    
-   %ASA-6-721002: (device) HA status change: event event, my state my\_state, peer state peer.
    
-   %ASA-6-721003: (device) HA progression change: event event, my state my\_state, peer state peer.
    
-   %ASA-6-721004: (device) Create access list list\_name on standby unit.
    
-   %ASA-6-721005: (device) Fail to create access list list\_name on standby unit.
    
-   %ASA-6-721006: (device) Update access list list\_name on standby unit.
    
-   %ASA-6-721008: (device) Delete access list list\_name on standby unit.
    
-   %ASA-6-721009: (device) Fail to delete access list list\_name on standby unit.
    
-   %ASA-6-721010: (device) Add access list rule list\_name, line line\_no on standby unit.
    
-   %ASA-6-721012: (device) Enable APCF XML file file\_name on the standby unit.
    
-   %ASA-6-721014: (device) Disable APCF XML file file\_name on the standby unit.
    
-   %ASA-6-721016: (device) WebVPN session for client user user\_name, IP ip\_address has been created.
    
-   %ASA-6-721018: (device) WebVPN session for client user user\_name, IP ip\_address has been deleted.
    
-   %ASA-6-722013: Group _group__user-name__IP\_address__type-num__message_
    
-   %ASA-6-722014: Group _group__user-name__IP\_address__type-num__message_
    
-   %ASA-6-722022: Group _group-name__user-name__addr__(TCP | UDP)__(with | without)_
    
-   %ASA-6-722023: Group <_group_\> User <_user\_name_\> IP <ip\_address> _conn\_type_ SVC connection terminated _with|without_ compression
    
-   %ASA-6-722024: SVC Global Compression Enabled
    
-   %ASA-6-722025: SVC Global Compression Disabled
    
-   %ASA-6-722026: Group _group__user-name__IP\_address_
    
-   %ASA-6-722027: Group _group__user-name__IP\_address_
    
-   %ASA-6-722036: Group _group__user-name__IP\_address__length__num_
    
-   %ASA-6-722051: Group _group-policy_ User _username_ IP _public-ip_ IPv4 Address _assigned-ip_ IPv6 address _assigned-ip_ assigned to session
    
-   %ASA-6-722053: Group _g__u__ip__user-agent_
    
-   %ASA-6-722055: Group _group-policy__username__public-ip__user-agent_
    
-   %ASA-6-723001: Group _group-name__user-name__IP\_address__connection_
    
-   %ASA-6-723002: Group _group-name__user-name__IP\_address__connection_
    
-   %ASA-6-725001: Starting SSL handshake with _peer-type__interface__src-ip__src-port__dst-ip__dst-port__protocol_
    
-   %ASA-6-725002: Device completed SSL handshake with _peer-type__interface__src-ip__src-port__dst-ip__dst-port__protocol-version_
    
-   %ASA-6-725003: SSL client _peer-type__interface__src-ip__src-port__dst-ip_
    
-   %ASA-6-725004: Device requesting certificate from SSL client _peer-type__interface__src-ip__src-port__dst-ip_
    
-   %ASA-6-725005: SSL server _peer-type__interface__src-ip__src-port__dst-ip_
    
-   %ASA-6-725006: Device failed SSL handshake with _peer-type__interface__src-ip__src-port__dst-ip__dst-port_
    
-   %ASA-6-725007: SSL session with _peer-type__interface__src-ip__src-port__dst-ip__dst-port_
    
-   %ASA-6-725025: SSL Pre-auth connection rate limit hit _s_ watermark
    
-   %ASA-6-726001: Inspected _im\_protocol__im\_service__im\_client\_1__im\_client\_2__src\_ifc__sip__sport__dest\_ifc__dip__dport__action_
    
-   %ASA-6-730002: Group <groupname>, User <username>, IP <ipaddr>: VLAN Mapping to VLAN vlanid failed.
    
-   %ASA-6-730004: Group _groupname__username__ipaddr__vlanid_
    
-   %ASA-6-730005: Group groupname User username IP ipaddr VLAN ID vlanid from AAA is invalid.
    
-   %ASA-6-730008: Group groupname, User username, IP ipaddr, VLAN MAPPING timeout waiting NACApp.
    
-   %ASA-6-725016: Device selects trust-point _trustpoint__peer-type__interface__src-ip__src-port__dst-ip__dst-port_
    
-   %ASA-6-731001: NAC policy added: name: policyname Type: policytype.
    
-   %ASA-6-731002: NAC policy deleted: name: policyname Type: policytype.
    
-   %ASA-6-731003: nac-policy unused: name: policyname Type: policytype.
    
-   %ASA-6-732001: Group groupname, User username, IP ipaddr, Fail to parse NAC-SETTINGS nac-settings-id, terminating connection.
    
-   %ASA-6-732002: Group groupname, User username, IP ipaddr, NAC-SETTINGS settingsid from AAA ignored, existing NAC-SETTINGS settingsid\_inuse used instead.
    
-   %ASA-6-732003: Group groupname, User username, IP ipaddr, NAC-SETTINGS nac-settings-id from AAA is invalid, terminating connection.
    
-   %ASA-6-734001: DAP: User _user,_ _ipaddr__connection_
    
-   %ASA-6-737005: IPAA: Session=_session__tunnel-group_
    
-   %ASA-6-737006: IPAA: Session=_session__tunnel-group_
    
-   %ASA-6-737009: IPAA: Session=_session__ip-address_
    
-   %ASA-6-737010: IPAA: Session=_session__ip-address_
    
-   %ASA-6-737014: IPAA: Session=_session__ip-address_
    
-   %ASA-6-737015: IPAA: Session=_session__ip-address_
    
-   %ASA-6-737016: IPAA: Session=_session__pool-name__ip-address_
    
-   %ASA-6-737017: IPAA: Session=_session__num_
    
-   %ASA-6-737026: IPAA: Session= _session__ip-address_
    
-   %ASA-6-737029: IPAA: Session=_session_, Added {_ip\_address | ipv6\_address_} to standby
    
-   %ASA-6-737031: IPAA: Session= _session_
    
-   %ASA-6-737035: IPAA: Session=_session__<address>_
    
-   %ASA-6-737036: IPAA: Session=<session>, Client assigned <address> from DHCP
    
-   %ASA-6-737205: VPNFIP: Pool=_pool__message_
    
-   %ASA-6-737406: POOLIP: Pool=_pool__message_
    
-   %ASA-6-741000: Coredump filesystem image created on _variable 1__variable 2_
    
-   %ASA-6-741001: Coredump filesystem image on _variable__variable__variable_
    
-   %ASA-6-741002: Coredump log and filesystem contents cleared on _variable 1_
    
-   %ASA-6-741003: Coredump filesystem and it's contents removed on _variable 1_
    
-   %ASA-6-741004: Coredump configuration reset to default values
    
-   %ASA-6-746001: user-identity: _user-to-IP address databases_
    
-   %ASA-6-746002: user-identity: _user-to-IP address databases_
    
-   %ASA-6-746008: user-identity: NetBIOS Logout Probe Process started
    
-   %ASA-6-746009: user-identity: NetBIOS Logout Probe Process stopped
    
-   %ASA-6-746017: user-identity: Update import-user _domain\_name_
    
-   %ASA-6-746018: user-identity: Update import-user _domain\_name_
    
-   %ASA-6-747004: Clustering: state machine changed from state state-name to state-name.
    
-   %ASA-6-748008: \[CPU load _percentage__percentage__slot\_number__chassis\_number__member-name__percentage__percentage_
    
-   %ASA-6-748009: \[CPU load percentage | memory load percentage\] of chassis chassis\_number exceeds overflow protection threshold \[CPU percentage | memory percentage}. System may be oversubscribed on chassis failure.
    
-   %ASA-6-780005: RULE ENGINE: Started compilation for session transaction - _description of the transaction_
    
-   %ASA-6-780006: RULE ENGINE: Finished compilation for session transaction - _description of the transaction_
    
-   %ASA-6-803001: bypass is continuing after power up, no protection will be provided by the system for traffic over _Interface_
    
-   %ASA-6-803002: no protection will be provided by the system for traffic over _Interface_
    
-   %ASA-6-751023: Unknown client connection.
    
-   %ASA-6-751026: Client OS: _client-os_ Client: _client-name_ _client-version_
    
-   %ASA-6-767001: Inspect-name: Dropping an unsupported IPv6/IP46/IP64 packet from interface:IP Addr to interface:IP Addr (fail-close)
    
-   %ASA-6-769007: UPDATE: Image version is _version\_number_
    
-   %ASA-6-776008: CTS SXP: Connection with peer IP (instance connection instance num) state changed from original state to final state.
    
-   %ASA-6-776251: CTS SGT-MAP: Binding binding IP - SGname(SGT) from source name added to binding manager.
    
-   %ASA-6-776253: CTS SGT-MAP: Binding binding IP - new SGname(SGT) from new source name changed from old sgt: old SGname(SGT) from old source old source name.
    
-   %ASA-6-776303: CTS Policy: Security-group name "_sgname__sgt_
    
-   %ASA-6-776311: CTS Policy: Previously unresolved security-group name "_sgname__sgt_
    
-   %ASA-6-775001: Scansafe: _protocol__conn\_id__interface\_name__real\_address__real\_port__idfw\_user__interface\_name__real\_address__real\_port__server\_interface\_name__server\_ip\_address_
    
-   %ASA-6-775003: Scansafe: _protocol__conn\_id__interface\_name__real\_address__real\_port__idfw\_user__interface\_name__real\_address__real\_port_
    
-   %ASA-6-775006: Scansafe: Reachable backup server _interface__ip\_address_
    
-   %ASA-6-772005: REAUTH: user '_username_
    
-   %ASA-6-775005: Scansafe: Primary server _server-name__ip\_address_
    
-   %ASA-6-778001: VXLAN: Packet was discarded with invalid segment-id _segment\_id_ for _protocol_ from _ifc\_name_:_ip\_address_/_port_ to _ip\_address_/_port_
    
-   %ASA-6-778002: VXLAN: There is no VNI interface for segment-id. Packet was discarded _segment\_id_
    
-   %ASA-6-778003: VXLAN: Invalid VXLAN segment-id segment-id for protocol from ifc-name:(IP-address/port) to ifc-name:(IP-address/port) in FP.
    
-   %ASA-6-778004: VXLAN: Invalid VXLAN header for protocol from ifc-name:(IP-address/port) to ifc-name:(IP-address/port) in FP.
    
-   %ASA-6-778005: VXLAN: Packet with VXLAN segment-id segment-id from ifc-name is denied by FP L2 check.
    
-   %ASA-6-778006: VXLAN: Invalid VXLAN UDP checksum from ifc-name:(IP-address/port) to ifc-name:(IP-address/port) in FP.
    
-   %ASA-6-778007: VXLAN: Packet from ifc-name:IP-address/port to IP-address/port was discarded due to invalid NVE peer.
    
-   %ASA-6-778008: VXLAN: There is no VNI interface for segment-id. Packet was discarded
    
-   %ASA-6-779001: STS: Out-tag lookup failed for in-tag segment-id of protocol from ifc-name:IP-address/port to IP-address/port.
    
-   %ASA-6-779002: STS: STS and NAT locate different egress interface for segment-id _segment-id__protocol__ifc-name__IP-address__port__IP-address__port_
    
-   %ASA-6-780001: RULE ENGINE: Started compilation for access-group transaction - _description of the transaction_.
    
-   %ASA-6-780002: RULE ENGINE: Finished compilation for access-group transaction - _description of the transaction_.
    
-   %ASA-6-780003: RULE ENGINE: Started compilation for nat transaction - _description of the transaction_
    
-   %ASA-6-780004: RULE ENGINE: Finished compilation for nat transaction - _description of the transaction_
    
-   %ASA-6-801001: Dropping UDP from _address_/_port_ to _address_/_port_ on interface _interface\_name_.
    
-   %ASA-6-801002: Dropping TCP from _address_/_port_ to _address_/_port_ flags on interface _interface\_name_
    
-   %ASA-6-801003: Dropping ICMP type=_number_, code=_code_ from _address_ to _address_ on interface _interface\_name_
    
-   %ASA-6-802005: IP ip\_address Received MDM request details.
    
-   %ASA-6-803001: bypass is continuing after power up, no protection will be provided by the system for traffic over _Interface_
    
-   %ASA-6-803002: no protection will be provided by the system for traffic over _Interface_
    
-   %ASA-6-803003: User disabled bypass manually on _Interface_
    
-   %ASA-6-804001: Interface _GigabitEthernet1/3__1000BaseSX_
    
-   %ASA-6-804002: Interface _GigabitEthernet1/3_
    
-   %ASA-6-805001: Offloaded _conn_ Flow for connection _conn\_id_ from _outside\_ifc_:_outside\_addr_/_outside\_port_ (_mapped\_addr_/_mapped\_port_) to _inside\_ifc_:_inside\_addr_/_inside\_port_ (_mapped\_addr_/_mapped\_port_)
    
-   %ASA-6-805002: _conn_ Flow is no longer offloaded for connection _conn\_id_ from _outside\_ifc_:_outside\_addr_/_outside\_port_ (_mapped\_addr_/_mapped\_port_) to _inside\_ifc_:_inside\_addr_/_inside\_port_ (_mapped\_addr_/_mapped\_port_)
    
-   %ASA-6-805003: _TCP_ Flow could not be offloaded for connection _conn\_id_ from _outside\_ifc_:_outside\_addr_/_outside\_port_ (_mapped\_addr_/_mapped\_port_) to _inside\_ifc_:_inside\_addr_/_inside\_port_ (_mapped\_addr_/_mapped\_port_) _reason_
    
-   %ASA-6-806001: Primary alarm CPU temperature is High _temp_
    
-   %ASA-6-806002: Primary alarm for CPU high temperature is cleared
    
-   %ASA-6-806003: Primary alarm CPU temperature is Low _temp_
    
-   %ASA-6-806004: Primary alarm for CPU Low temperature is cleared
    
-   %ASA-6-806005: Secondary alarm CPU temperature is High _temp_
    
-   %ASA-6-806006: Secondary alarm for CPU High temperature is cleared
    
-   %ASA-6-806007: Secondary alarm CPU temperature is Low _temp_
    
-   %ASA-6-806008: Secondary alarm for CPU Low temperature is cleared
    
-   %ASA-6-806009: Alarm asserted for ALARM\_IN\_1 _description_
    
-   %ASA-6-806010: Alarm cleared for ALARM\_IN\_1 _description_
    
-   %ASA-6-806011: Alarm asserted for ALARM\_IN\_2 _description_
    
-   %ASA-6-806012: Alarm cleared for ALARM\_IN\_2 _description_
    
-   %ASA-6-812007: Inline-set hardware-bypass mode configuration _status_
    
-   %ASA-6-861012: AVC: Installing visibility NSG failed; _error\_string_.
    
-   %ASA-6-880001: Ingress ifc _Ingress interface__source ipaddress_ _destination ipaddress__outside interface 1__metric-type__outside interface 2_
    
-   %ASA-6-8300001: VPN session redistribution <variable 1>
    
-   %ASA-6-8300002: Moved <variable 1> sessions to <variable 2>
    
-   %ASA-6-8300004: <variable 1> request to move <variable 2> sessions from <variable 3> to <variable 4>
    

## Debugging Messages, Severity 7

The following messages appear at severity 7, debugging:

-   %ASA-7-108006: Detected ESMTP size violation from _src\_ifc__sip__sport__dest\_ifc__dip__dport__decl\_size__act\_size_
    
-   %ASA-7-109014: A non-telnet connection was denied to the configured Virtual Telnet IP Address
    
-   %ASA-7-109021: Uauth null proxy error (uap _number_
    
-   %ASA-7-111009: User '_user__string_
    
-   %ASA-7-113028: Extraction of username from VPN client certificate has _string.__num_
    
-   %ASA-7-199019: syslog
    
-   %ASA-7-304005: URL Server _IP\_address__url_
    
-   %ASA-7-304009: Ran out of buffer blocks specified by url-block command
    
-   %ASA-7-325007: IPv6 security check failed. Dropped packet from _interface_:_address_/_port_ to _address_/_port_ with source MAC address _MAC\_address_ and hop limit _limit\_value_
    
-   %ASA-7-333004: EAP-SQ response invalid - context:EAP-context
    
-   %ASA-7-333005: EAP-SQ response contains invalid TLV(s) - context:EAP-context
    
-   %ASA-7-333006: EAP-SQ response with missing TLV(s) - context:EAP-context
    
-   %ASA-7-333007: EAP-SQ response TLV has invalid length - context:EAP-context
    
-   %ASA-7-333008: EAP-SQ response has invalid nonce TLV - context:EAP-context
    
-   %ASA-7-335007: NAC Default ACL not configured - host-address
    
-   %ASA-7-342001: The REST API Agent was successfully started.
    
-   %ASA-7-342005: REST API image has been successfully installed.
    
-   %ASA-7-342007: REST API image has been successfully uninstalled.
    
-   %ASA-7-419003: Cleared TCP urgent flag
    
-   %ASA-7-421004: Failed to inject _{TCP|UDP}__IP\_address__port__IP\_address__port_
    
-   %ASA-7-444307: %SMART\_LIC-7-DAILY\_JOB\_TIMER\_RESET: Daily job timer reset.
    
-   %ASA-7-609001: Built local-host _zone\_name_:_ip\_address_
    
-   %ASA-7-609002: Teardown local-host _zone\_name_:_ip\_address_ duration _time_
    
-   %ASA-7-701001: alloc\_user() out of Tcp\_user objects
    
-   %ASA-7-701002: alloc\_proxy() out of Tcp\_proxy objects
    
-   %ASA-7-702307: IPSEC: An _direction__tunnel\_type__spi_ _local\_IP__remote\_IP_
    
-   %ASA-7-703001: H.225 message received from _interface\_name__IP\_address__port__interface\_name__IP\_address__port__number_
    
-   %ASA-7-703002: Received H.225 Release Complete with newConnectionNeeded for _interface\_name__IP\_address__interface\_name__IP\_address__port_
    
-   %ASA-7-703008: Allowing early-message: _msg\_str_ before SETUP from _src\_int\_name_:_src\_ip_/_src\_port_ to _dest\_int\_name_:_dest\_ip_/_dest\_port_
    
-   %ASA-7-709001: FO replication failed: cmd=_command__code_
    
-   %ASA-7-709002: FO unreplicable: cmd=command
    
-   %ASA-7-710001: _TCP__source\_address__source\_port__interface\_name__dest\_address__service_
    
-   %ASA-7-710002: _{TCP|UDP}_ access permitted from _source\_address_/_source\_port_ to _interface\_name_:_dest\_address_/_service_
    
-   %ASA-7-710004: _TCP__Src\_ip__Src\_port__In\_name__Dest\_ip__Dest\_port__Curr\_conn__Conn\_lmt_
    
-   %ASA-7-710005: _{TCP|UDP|SCTP}__source\_address__source\_port__interface\_name__dest\_address__service_
    
-   %ASA-7-710006: _protocol__source\_address__interface\_name__dest\_address_
    
-   %ASA-7-710007: NAT-T keepalive received from _inside: ip-Addr__port__outside__ip-Addr__port_
    
-   %ASA-7-711001: _debug\_trace\_msg_
    
-   %ASA-7-711003: Unknown/Invalid interface identifier(vpifnum) detected.
    
-   %ASA-7-711006: CPU profiling has started for _n-samples__reason-string_
    
-   %ASA-7-713024: Group = _groupname_, Username = _username_, IP = _peerIP_ Group _group_ IP _ip_ Received local Proxy Host data in ID Payload: Address _IP\_address_, Protocol _protocol_, Port _port_
    
-   %ASA-7-713025: Group = _groupname_, Username = _username_, IP = _peerIP_ Received remote Proxy Host data in ID Payload: Address _IP\_address_, Protocol _protocol_, Port _port_
    
-   %ASA-7-713028: Group = _groupname_, Username = _username_, IP = _peerIP_ Received local Proxy Range data in ID Payload: Addresses _IP\_address_ - _IP\_address_, Protocol _protocol_, Port _port_
    
-   %ASA-7-713029: Group = _groupname_, Username = _username_, IP = _peerIP_ Received remote Proxy Range data in ID Payload: Addresses _IP\_address_ - _IP\_address_, Protocol _protocol_, Port _port_
    
-   %ASA-7-713034: Group = _groupname_, Username = _username_, IP = _peerIP_ Received local IP Proxy Subnet data in ID Payload: Address _IP\_address_, Mask _netmask_, Protocol _protocol_, Port _port_
    
-   %ASA-7-713035: Group = _groupname_, Username = _username_, IP = _peerIP_ Group _group_ IP _ip_ Received remote IP Proxy Subnet data in ID Payload: Address _IP\_address_, Mask _netmask_, Protocol _protocol_, Port _port_
    
-   %ASA-7-713039: Group = _groupname_, Username = _username_, IP = _peerIP_ Send failure: Bytes (_number_ ), Peer: _IP\_address_
    
-   %ASA-7-713040: Group = _groupname_, Username = _username_, IP = _peerIP_ Could not find connection entry and can not encrypt: msgid _message\_number_
    
-   %ASA-7-713052: Group = _groupname_, Username = _username_, IP = _peerIP_ User (_user_ ) authenticated.
    
-   %ASA-7-713066: Group = _groupname_, Username = _username_, IP = _peerIP_ IKE Remote Peer configured for SA: _SA\_name_
    
-   %ASA-7-713094: Group = _groupname_, Username = _username_, IP = _peerIP_ Cert validation failure: handle invalid for _Main_ /_Aggressive Mode Initiator_ /_Responder_ !
    
-   %ASA-7-713099: Group = _groupname_, Username = _username_, IP = _peerIP_ Tunnel Rejected: Received NONCE length _number_ is out of range!
    
-   %ASA-7-713103: Group = _groupname_, Username = _username_, IP = _peerIP_ Invalid (NULL) secret key detected while computing hash
    
-   %ASA-7-713104: Group = _groupname_, Username = _username_, IP = _peerIP_ Attempt to get Phase 1 ID data failed while _hash computation_
    
-   %ASA-7-713113: Group = _groupname_, Username = _username_, IP = _peerIP_ Deleting IKE SA with associated IPsec connection entries. IKE peer: _IP\_address_, SA address: _internal\_SA\_address_, tunnel count: _count_
    
-   %ASA-7-713114: Group = _groupname_, Username = _username_, IP = _peerIP_ Connection entry (conn entry internal address) points to IKE SA (_SA\_internal\_address_ ) for peer _IP\_address_, but cookies don't match
    
-   %ASA-7-713117: Group = _groupname_, Username = _username_, IP = _peerIP_ Received Invalid SPI notify (SPI _SPI\_Value_ )!
    
-   %ASA-7-713121: IP = _peerIP_ Keep-alive type for this connection: _keepalive\_type_
    
-   %ASA-7-713143: IP = _peerIP_ Processing firewall record. Vendor: _vendor(id)_, Product: _product(id)_, Caps: _capability\_value_, Version Number: _version\_number_, Version String: _version\_text_
    
-   %ASA-7-713160: Group = _groupname_, Username = _username_, IP = _peerIP_ Remote user (session Id - _id_ ) has been granted access by the Firewall Server
    
-   %ASA-7-713164: The Firewall Server has requested a list of active user sessions
    
-   %ASA-7-713169: Group = _groupname_, Username = _username_, IP = _peerIP_ IKE Received delete for rekeyed SA IKE peer: _IP\_address_, SA address: _internal\_SA\_address_, tunnelCnt: tunnel\_count
    
-   %ASA-7-713170: Group = _groupname_, Username = _username_, IP = _peerIP_ Group _group_ IP _ip_ IKE Received delete for rekeyed centry IKE peer: _IP\_address_, centry address: _internal\_address_, msgid: _id_
    
-   %ASA-7-713171: Group = _groupname_, Username = _username_, IP = _peerIP_ NAT-Traversal sending NAT-Original-Address payload
    
-   %ASA-7-713187: Group = _groupname_, Username = _username_, IP = _peerIP_ Tunnel Rejected: IKE peer does not match remote peer as defined in L2L policy IKE peer address: _IP\_address_, Remote peer address: _IP\_address_
    
-   %ASA-7-713190: Group = _groupname_, Username = _username_, IP = _peerIP_ Got bad refCnt ( _ref\_count\_value_ ) assigning _IP\_address_ ( _IP\_address_ )
    
-   %ASA-7-713204: Group = _groupname_, Username = _username_, IP = _peerIP_ Adding static route for client address: _IP\_address_
    
-   %ASA-7-713221: Group = _groupname_, Username = _username_, IP = _peerIP_ Static Crypto Map check, checking map = _crypto\_map\_tag_, seq = _seq\_number..._
    
-   %ASA-7-713222: Group = _groupname_, Username = _username_, IP = _peerIP_ Group _group_ Username _username_ IP _ip_ Static Crypto Map check, map = _crypto\_map\_tag_, seq = _seq\_number_, ACL does not match proxy IDs src:_source\_address_ dst:_dest\_address_
    
-   %ASA-7-713223: Group = _groupname_, Username = _username_, IP = _peerIP_ Static Crypto Map check, map = _crypto\_map\_tag_, seq = _seq\_number_, no ACL configured
    
-   %ASA-7-713224: Group = _groupname_, Username = _username_, IP = _peerIP_ Static Crypto Map Check by-passed: Crypto map entry incomplete!
    
-   %ASA-7-713225: Group = _groupname_, Username = _username_, IP = _peerIP_ \[IKEv1\], Static Crypto Map check, map _map\_name_, seq = _sequence\_number_ is a successful match
    
-   %ASA-7-713233: (VPN-unit) Remote network (remote network) validated for network extension mode.
    
-   %ASA-7-713234: (VPN-unit) Remote network (remote network) from network extension mode client mismatches AAA configuration (aaa network).
    
-   %ASA-7-713236: Group = _groupname_, Username = _username_, IP = _peerIP_ IKE\_DECODE tx/rx Message (msgid=msgid) with payloads:payload1 (payload1\_len) + payload2 (payload2\_len)...total length: tlen
    
-   %ASA-7-713263: Group = _groupname_, Username = _username_, IP = _peerIP_ Received local IP Proxy Subnet data in ID Payload: Address _IP\_address_, Mask /_prefix\_len_, Protocol _protocol_, Port _port_
    
-   %ASA-7-713264: Group = _groupname_, Username = _username_, IP = _peerIP_ Received local IP Proxy Subnet data in ID Payload: Address _IP\_address_, Mask/_prefix\_len_, Protocol _protocol_, Port _port_ {“Received remote IP Proxy Subnet data in ID Payload: Address _ip\_address_, Mask/_mask_, Protocol _protocol\_nane_, Port _port\_number_ ”}
    
-   %ASA-7-713906: Descriptive\_event\_string.
    
-   %ASA-7-714001: _description\_of\_event\_or\_packet_
    
-   %ASA-7-714002: Group = _groupname_, Username = _username_, IP = _IP\_address_ IKE Initiator starting QM: msg id = _message\_number_
    
-   %ASA-7-714003: IP = _IP\_address_ IKE Responder starting QM: msg id = _message\_number_
    
-   %ASA-7-714004: Group = _groupname_, Username = _username_, IP = _IP\_address_ IKE Initiator sending 1st QM pkt: msg id = _message\_number_
    
-   %ASA-7-714005: Group = _groupname_, Username = _username_, IP = _IP\_address_ IKE Responder sending 2nd QM pkt: msg id = _message\_number_
    
-   %ASA-7-714006: Group = _groupname_, Username = _username_, IP = _IP\_address_ IKE Initiator sending 3rd QM pkt: msg id = _message\_number_
    
-   %ASA-7-714007: IKE Initiator sending Initial Contact
    
-   %ASA-7-714011: Group = _groupname_, Username = _username_, IP = _IP\_address_ _Description of received ID values_
    
-   %ASA-7-715001: _Descriptive statement_
    
-   %ASA-7-715004: subroutine _name_ Q Send failure: RetCode (_return\_code_ )
    
-   %ASA-7-715005: subroutine _name_ Bad message code: Code (_message\_code_ )
    
-   %ASA-7-715006: Group = _groupname_, Username = _username_, IP = _IP\_address_ IKE got SPI from key engine: SPI = _SPI\_value_
    
-   %ASA-7-715007: Group = _groupname_, Username = _username_, IP = _IP\_address_ IKE got a KEY\_ADD msg for SA: SPI = _SPI\_value_
    
-   %ASA-7-715008: Could not delete SA SA\_address, refCnt = _number_, caller = _calling\_subroutine\_address_
    
-   %ASA-7-715009: Group = _groupname_, Username = _username_, IP = _IP\_address_ IKE Deleting SA: Remote Proxy _IP\_address_, Local Proxy _IP\_address_
    
-   %ASA-7-715013: Group = _groupname_, Username = _username_, IP = _IP\_address_ Tunnel negotiation in progress for destination _IP\_address_, discarding data
    
-   %ASA-7-715018: Group = _groupname_, Username = _username_, IP = _IP\_address_ IP Range type id was loaded: Direction %s,  From: %a, Through: %a
    
-   %ASA-7-715019: Group = _group_, Username = _username_, IP = _ip_ Group _group_ Username _username_ IP _ip_ IKEGetUserAttributes: Attribute name = _name_
    
-   %ASA-7-715020: Group = _group_, Username = _username_, IP = _ip_ construct\_cfg\_set: Attribute name = _name_
    
-   %ASA-7-715021: Group = _group_, Username = _username_, IP = _ip_ Delay Quick Mode processing, Cert/Trans Exch/RM DSID in progress
    
-   %ASA-7-715022: Group = _group_, Username = _username_, IP = _ip_ Resume Quick Mode processing, Cert/Trans Exch/RM DSID completed
    
-   %ASA-7-715027: Group = _group_, Username = _username_, IP = _ip_ IPsec SA Proposal _\# chosen\_proposal_, Transform # _chosen\_transform_ acceptable Matches global IPsec SA entry _\# crypto\_map\_index_
    
-   %ASA-7-715028: Group = _group_, Username = _username_, IP = _ip_ IKE SA Proposal # 1, Transform # chosen\_transform acceptable Matches global IKE entry _\# crypto\_map\_index_
    
-   %ASA-7-715031: Obtained IP addr (%s) prior to initiating Mode Cfg (XAuth %s)
    
-   %ASA-7-715032: Sending subnet mask (%s) to remote client
    
-   %ASA-7-715033: Group = _group_, Username = _username_, IP = _ip_ Processing CONNECTED notify (MsgId _message\_number_ )
    
-   %ASA-7-715034: IP = _ip_ action IOS keep alive payload: proposal=_time 1_ /_time 2_ sec.
    
-   %ASA-7-715035: IP = _ip_ Starting IOS keepalive monitor: _seconds_ sec.
    
-   %ASA-7-715036: Group = _group_, Username = _username_, IP = _ip_ Sending keep-alive of type _notify\_type_ (seq number _number_ )
    
-   %ASA-7-715037: Group = _group_, Username = _username_, IP = _ip_ Unknown IOS Vendor ID version: _major.minor.variance_
    
-   %ASA-7-715038: Group = _group_, Username = _username_, IP = _ip_ _action Spoofing\_information_ Vendor ID payload (version: _major.minor.variance_, capabilities: _value_ )
    
-   %ASA-7-715039: Group = _group_, Username = _username_, IP = _ip_ Unexpected cleanup of tunnel table entry during SA delete.
    
-   %ASA-7-715040: Deleting active auth handle during SA deletion: handle = _internal\_authentication\_handle_
    
-   %ASA-7-715041: Group = _group_, Username = _username_, IP = _ip_ Received keep-alive of type _keepalive\_type_, not the negotiated type
    
-   %ASA-7-715042: Group = _group_, Username = _username_, IP = _ip_ IKE received response of type _failure\_type_ to a request from the _IP\_address_ utility
    
-   %ASA-7-715044: IP = _ip_ Ignoring Keepalive payload from vendor not support KeepAlive capability
    
-   %ASA-7-715045: ERROR: malformed Keepalive payload
    
-   %ASA-7-715046: Group = _groupname_, Username = _username_, IP = _IP\_address_ Group = _groupname_, Username = _username_, IP = _IP\_address_, constructing _payload\_description_ payload
    
-   %ASA-7-715047: Group = _groupname_, Username = _username_, IP = _IP\_address_ processing _payload\_description_ payload
    
-   %ASA-7-715048: Group = _groupname_, Username = _username_, IP = _IP\_address_ Send _VID\_type_ VID
    
-   %ASA-7-715049: Group = _groupname_, Username = _username_, IP = _IP\_address_ Received _VID\_type_ VID
    
-   %ASA-7-715050: Group = _groupname_, Username = _username_, IP = _IP\_address_ Claims to be IOS but failed authentication
    
-   %ASA-7-715051: IP = _IP\_address_ Received unexpected TLV type _TLV\_type_ while processing FWTYPE ModeCfg Reply
    
-   %ASA-7-715052: Group = _groupname_, Username = _username_, IP = _IP\_address_ Old P1 SA is being deleted but new SA is DEAD, cannot transition centries
    
-   %ASA-7-715053: Group = _groupname_, Username = _username_, IP = _IP\_address_ MODE\_CFG: Received request for _attribute\_info_ !
    
-   %ASA-7-715054: MODE\_CFG: Received _attribute\_name_ reply: _value_
    
-   %ASA-7-715055: Group = _groupname_, Username = _username_, IP = _IP\_address_ Send _attribute\_name_
    
-   %ASA-7-715056: Group = _groupname_, Username = _username_, IP = _IP\_address_ Client is configured for _TCP\_transparency_
    
-   %ASA-7-715057: Group = _groupname_, Username = _username_, IP = _IP\_address_ Auto-detected a NAT device with NAT-Traversal. Ignoring IPsec-over-UDP configuration.
    
-   %ASA-7-715058: Group = _groupname_, Username = _username_, IP = _IP\_address_ NAT-Discovery payloads missing. Aborting NAT-Traversal.
    
-   %ASA-7-715059: Group = _groupname_, Username = _username_, IP = _IP\_address_ Proposing/Selecting only UDP-Encapsulated-Tunnel and UDP-Encapsulated-Transport modes defined by NAT-Traversal
    
-   %ASA-7-715060: Group = _groupname_, Username = _username_, IP = _IP\_address_ Dropped received IKE fragment. Reason: _reason_
    
-   %ASA-7-715061: Group = _groupname_, Username = _username_, IP = _IP\_address_ Rcv'd fragment from a new fragmentation set. Deleting any old fragments.
    
-   %ASA-7-715062: Group = _groupname_, Username = _username_, IP = _IP\_address_ Error assembling fragments! Fragment numbers are non-continuous.
    
-   %ASA-7-715063: Group = _groupname_, Username = _username_, IP = _IP\_address_ Successfully assembled an encrypted pkt from rcv'd fragments!
    
-   %ASA-7-715064 -- IKE Peer included IKE fragmentation capability flags: Main Mode: true/false Aggressive Mode: true/false
    
-   %ASA-7-715065: Group = _groupname_, Username = _username_, IP = _IP\_address_ IKE _state\_machine subtype_ FSM error history (struct _data\_structure\_address_ ) _state_, _event_ : _state_ /_event_ pairs
    
-   %ASA-7-715066: Group = _groupname_, Username = _username_, IP = _IP\_address_ Can't load an IPsec SA! The corresponding IKE SA contains an invalid logical ID.
    
-   %ASA-7-715067: QM IsRekeyed: existing sa from different peer, rejecting new sa
    
-   %ASA-7-715068: Group = _groupname_, Username = _username_, IP = _IP\_address_ QM IsRekeyed: duplicate sa found by _address_, deleting old sa
    
-   %ASA-7-715069: Group = _groupname_, Username = _username_, IP = _IP\_address_ Invalid ESP SPI size of _SPI\_size_
    
-   %ASA-7-715070: Group = _groupname_, Username = _username_, IP = _IP\_address_ Invalid IPComp SPI size of _SPI\_size_
    
-   %ASA-7-715071: Group = _groupname_, Username = _username_, IP = _IP\_address_ AH proposal not supported
    
-   %ASA-7-715072: Group = _groupname_, Username = _username_, IP = _IP\_address_ Received proposal with unknown protocol ID _protocol\_ID_
    
-   %ASA-7-715074: Group = _groupname_, Username = _username_, IP = _IP\_address_ Could not retrieve authentication attributes for peer _IP\_address_
    
-   %ASA-7-715075: Group = _group\_name_, Username = _username_, IP = _IP\_address_ Group = _group\_name_, IP = _IP\_address_ Received keep-alive of type _message\_type_ (seq number _number_ )
    
-   %ASA-7-715076: Group = _group\_name_, Username = _username_, IP = _IP\_address_ Computing hash for ISAKMP
    
-   %ASA-7-715077: Pitcher: _msg string_, spi _spi_
    
-   %ASA-7-715078: Group = _group\_name_, Username = _username_, IP = _IP\_address_ Received %s LAM attribute
    
-   %ASA-7-715079: Group = _group\_name_, Username = _username_, IP = _IP\_address_ INTERNAL\_ADDRESS: Received request for %s
    
-   %ASA-7-715080: Group = _group\_name_, Username = _username_, IP = _IP\_address_ VPN: Starting P2 rekey timer: 28800 seconds.
    
-   %ASA-7-716008: WebVPN ACL: _action__string_
    
-   %ASA-7-716010: Group _group__user__ip_
    
-   %ASA-7-716011: Group _group__user__ip__domain_
    
-   %ASA-7-716012: Group _group__user__ip__directory_
    
-   %ASA-7-716013: Group _group__user__ip__filename_
    
-   %ASA-7-716014: Group _group__user__ip__filename_
    
-   %ASA-7-716015: Group _group__user__ip__filename_
    
-   %ASA-7-716016: Group _group__user__ip__old\_filename__new\_filename_
    
-   %ASA-7-716017: Group _group__user__ip__filename_
    
-   %ASA-7-716018: Group _group__user__ip__filename_
    
-   %ASA-7-716019: Group _group__user__ip__directory_
    
-   %ASA-7-716020: Group _group__user__ip__directory_
    
-   %ASA-7-716021: File access DENIED, _filename_
    
-   %ASA-7-716024: Group _name__user__ip__description_
    
-   %ASA-7-716025: Group _name__user__ip__domain__description_
    
-   %ASA-7-716026: Group _name__user__ip__directory__description_
    
-   %ASA-7-716027: Group _name__user__ip__filename__description_
    
-   %ASA-7-716028: Group _name__user__ip__filename__description_
    
-   %ASA-7-716029: Group _name__user__ip__filename__description_
    
-   %ASA-7-716030: Group _name__user__ip__filename__description_
    
-   %ASA-7-716031: Group _name__user__ip__filename__description_
    
-   %ASA-7-716032: Group _name__user__ip__folder__description_
    
-   %ASA-7-716033: Group _name__user__ip__folder__description_
    
-   %ASA-7-716034: Group _name__user__ip__filename_
    
-   %ASA-7-716035: Group _name__user__ip__filename_
    
-   %ASA-7-716036: Group _name__user__ip__user__server_
    
-   %ASA-7-716037: Group _name__user__ip__user__server_
    
-   %ASA-7-716603: Received _size-recv__src-ip_
    
-   %ASA-7-717024: Checking CRL from trustpoint: trustpoint name for purpose
    
-   %ASA-7-717025: Validating certificate chain containing _number of certs_
    
-   %ASA-7-717029: Identified client certificate within certificate chain. _serial\_number_
    
-   %ASA-7-717030: Found a suitable trustpoint _trustpoint name_
    
-   %ASA-7-717034: No-check extension found in certificate. CRL check bypassed.
    
-   %ASA-7-717036: Looking for a tunnel group match based on certificate maps for peer certificate with _certificate\_identifier_
    
-   %ASA-7-717038: Tunnel group match found. Tunnel Group: _tunnel\_group\_name__certificate\_identifier_
    
-   %ASA-7-717041: Local CA Server event: _event info_
    
-   %ASA-7-717045: Local CA Server CRL info: _info_
    
-   %ASA-7-718001: Internal interprocess communication queue send failure: code \[_error\_code_
    
-   %ASA-7-718017: Got timeout for unknown peer\[_IP\_address__message\_type_
    
-   %ASA-7-718018: Send KEEPALIVE request failure to \[_IP\_address_
    
-   %ASA-7-718019: Sent KEEPALIVE request to \[_IP\_address_
    
-   %ASA-7-718020: Send KEEPALIVE response failure to \[_IP\_address_
    
-   %ASA-7-718021: Sent KEEPALIVE response to \[_IP\_address_
    
-   %ASA-7-718022: Received KEEPALIVE request from \[_IP\_address_
    
-   %ASA-7-718023: Received KEEPALIVE response from \[_IP\_address_
    
-   %ASA-7-718025: Sent CFG UPDATE to \[_IP\_address_
    
-   %ASA-7-718026: Received CFG UPDATE from \[_IP\_address_
    
-   %ASA-7-718029: Sent OOS indicator to \[_IP\_address_
    
-   %ASA-7-718034: Sent TOPOLOGY indicator to \[_IP\_address_
    
-   %ASA-7-718035: Received TOPOLOGY indicator from \[_IP\_address_
    
-   %ASA-7-718036: Process timeout for req-type\[_type\_value__exchange\_ID__IP\_address_
    
-   %ASA-7-718041: Timeout \[msgType=_type_
    
-   %ASA-7-718046: Create group policy \[_policy\_name_
    
-   %ASA-7-718047: Fail to create group policy \[_policy\_name_
    
-   %ASA-7-718049: Created secure tunnel to peer\[_IP\_address_
    
-   %ASA-7-718056: Deleted Master peer, IP _IP\_address_
    
-   %ASA-7-718058: State machine return code: _action\_routine__return\_code_
    
-   %ASA-7-718059: State machine function trace: state=_state\_name__event\_name__action\_routine_
    
-   %ASA-7-718088: Possible VPN LB misconfiguration. Offending device MAC \[_MAC\_address_
    
-   %ASA-7-719005: FSM NAME has been created using protocol for session pointer from source\_address.
    
-   %ASA-7-719006: Email Proxy session pointer has timed out for source\_address because of network congestion.
    
-   %ASA-7-719007: Email Proxy session pointer cannot be found for source\_address.
    
-   %ASA-7-719009: Email Proxy service is starting.
    
-   %ASA-7-719015: Parsed emailproxy session pointer from source\_address username: mailuser = mail\_user, vpnuser = VPN\_user, mailserver = server
    
-   %ASA-7-719016: Parsed emailproxy session pointer from source\_address password: mailpass = \*\*\*\*\*\*, vpnpass= \*\*\*\*\*\*
    
-   %ASA-7-720031: (VPN-unit) HA status callback: Invalid event received. event=event\_ID.
    
-   %ASA-7-720034: (VPN-unit) Invalid type (type) for message handler.
    
-   %ASA-7-720041: (VPN-unit) Sending type message id to standby unit
    
-   %ASA-7-720042: (VPN-unit) Receiving type message id from active unit
    
-   %ASA-7-720048: (VPN-unit) FSM action trace begin: state=state, last event=event, func=function.
    
-   %ASA-7-720049: (VPN-unit) FSM action trace end: state=state, last event=event, return=return, func=function.
    
-   %ASA-7-720050: (VPN-unit) Failed to remove timer. ID = id.
    
-   %ASA-7-722029: Group _group__user-name__IP\_address__connections__DPD\_conns__compression\_resets__decompression\_resets_
    
-   %ASA-7-722030: Group _group__user-name__IP\_address__data\_bytes__ctrl\_bytes__data\_pkts__ctrl\_pkts__drop\_pkts_
    
-   %ASA-7-722031: Group _group__user-name__IP\_address__data\_bytes__ctrl\_bytes__data\_pkts__ctrl\_pkts__drop\_pkts_
    
-   %ASA-7-723003: No memory for WebVPN Citrix ICA connection _connection_
    
-   %ASA-7-723004: WebVPN Citrix encountered bad flow control _flow_
    
-   %ASA-7-723005: No channel to set up WebVPN Citrix ICA connection.
    
-   %ASA-7-723006: WebVPN Citrix SOCKS errors.
    
-   %ASA-7-723007: WebVPN Citrix ICA connection _connection_
    
-   %ASA-7-723008: WebVPN Citrix ICA SOCKS Server _server_
    
-   %ASA-7-723009: Group _group-name__user-name__IP\_address__connection_
    
-   %ASA-7-723010: Group _group-name__user-name__IP\_address__channel_
    
-   %ASA-7-723011: Group _group-name__user-name__IP\_address__socks__exp-msg-length_
    
-   %ASA-7-723012: Group _group-name__user-name__IP\_address__socks_
    
-   %ASA-7-723013: WebVPN Citrix encountered invalid connection _connection_
    
-   %ASA-7-723014: Group _group-name__user-name__IP\_address__connection__server__channel_
    
-   %ASA-7-725008: SSL client _peer-type__interface__src-ip__src-port__dst-ip__dst-port_
    
-   %ASA-7-725009: Device proposes the following n cipher(s) peer-type interface:src-ip/src-port to dst-ip/dst-port.
    
-   %ASA-7-725010: Device supports the following _n_
    
-   %ASA-7-725011: Cipher\[order\]: cipher\_name
    
-   %ASA-7-725012: Device chooses cipher _cipher__peer-type__interface__src-ip__src-port__dst-ip_
    
-   %ASA-7-725013: SSL peer-type interface:src-ip/src-port to dst-ip/dst-port chooses cipher cipher
    
-   %ASA-7-725014: SSL lib error. Function: function Reason: reason
    
-   %ASA-7-725017: No certificates received during the handshake with _s__s__B__d__B__d__s_
    
-   %ASA-7-725021: Device preferring _cipher-suite__interface__src-ip__src-port__dst-ip__dst-port_
    
-   %ASA-7-725022: Device skipping cipher: _cipher__reason__interface__src-ip__src-port__dst-ip__dst-port_
    
-   %ASA-7-730001: Group groupname, User username, IP ipaddr: VLAN MAPPING to VLAN vlanid
    
-   %ASA-7-730003: IP _ipaddr__vlanid_
    
-   %ASA-7-730006: Group groupname, User username, IP ipaddr: is on NACApp AUTH VLAN vlanid.
    
-   %ASA-7-730007: Group _groupname__username__ipaddr__vlan__vlanid_
    
-   %ASA-7-730010: Group _groupname__username,__ipaddr__vlanid_
    
-   %ASA-7-734003: DAP: User _name__ipaddr__attr name/value_
    
-   %ASA-7-737001: IPAA: Session=_session__message-type_
    
-   %ASA-7-737035: IPAA: Session=_session__'message type'_
    
-   %ASA-7-746012: user-identity: Add IP-User mapping _ip address__domain\_name__user\_name__result__reason_
    
-   %ASA-7-746013: user-identity: Delete IP-User mapping _ip address__domain\_name__user__name__result__reason_
    
-   %ASA-7-747005: Clustering: State machine notify event event-name (event-id, ptr-in-hex, ptr-in-hex)
    
-   %ASA-7-747006: Clustering: State machine is at state state-name
    
-   %ASA-7-737200: VPNFIP: Pool=_pool__ip-address_
    
-   %ASA-7-737201: VPNFIP: Pool=_pool__ip-address__recycle_
    
-   %ASA-7-737206: VPNFIP: Pool=_pool__message_
    
-   %ASA-7-737400: POOLIP: Pool=_pool__ip-address_
    
-   %ASA-7-737401: POOLIP: Pool=_pool__ip-address__recycle_
    
-   %ASA-7-737407: POOLIP: Pool=_pool__message_
    
-   %ASA-7-750016: Local: _localIP:port_ Remote:_remoteIP:port_ Username:_username_ Need to send a DPD message to peer
    
-   %ASA-7-751003: Need to send a DPD message to peer
    
-   %ASA-7-752002: Tunnel Manager Removed entry. Map Tag = _mapTag_ . Map Sequence Number = _mapSeq_ .
    
-   %ASA-7-752008: Duplicate entry already in Tunnel Manager
    
-   %ASA-7-776012: CTS SXP: timer name timer started for connection with peer peer IP.
    
-   %ASA-7-776013: CTS SXP: timer name timer stopped for connection with peer peer IP.
    
-   %ASA-7-776014: CTS SXP: SXP received binding forwarding request (action) binding binding IP - SGname(SGT).
    
-   %ASA-7-776015: CTS SXP: Binding binding IP - SGname(SGT) is forwarded to peer peer IP (instance connection instance num).
    
-   %ASA-7-776016: CTS SXP: Binding binding IP - SGName(SGT) from peer peer IP (instance binding's connection instance num) changed from old instance: old instance num, old sgt: old SGName(SGT).
    
-   %ASA-7-776017: CTS SXP: Binding binding IP - SGname(SGT) from peer peer IP (instance connection instance num) deleted in SXP database.
    
-   %ASA-7-776018: CTS SXP: Binding binding IP - SGname(SGT) from peer peer IP (instance connection instance num) added in SXP database.
    
-   %ASA-7-776019: CTS SXP: Binding binding IP - SGname(SGT) action taken. Update binding manager.
    
-   %ASA-7-776301: CTS Policy: Security-group tag _sgt__sgname_
    
-   %ASA-7-776302: CTS Policy: Unknown security-group tag _sgt_
    
-   %ASA-7-776307: CTS Policy: Security-group name for security-group tag _sgt__old\_sgname__new\_sgname_
    
-   %ASA-7-776308: CTS Policy: Previously unknown security-group tag _sgt__sgname_
    
-   %ASA-7-785001: Clustering: Ownership for existing flow from _in\_interface_:_src\_ip\_addr_/_src\_port_ to _out\_interface_:_dest\_ip\_addr_/_dest\_port_ moved from unit _old-owner-unit-id_ at site _old-site-id_ to unit _new-owner-unit-id_ at site _old-site-id_ due to _reason_
    
-   %ASA-7-815004: OGS: Packet <protocol> from <source IP address/port> to <destination IP address/port> matched <number of source network objects> source network objects and <number of source network objects> destination network objects total search entries <total number of entries>. Resultant key-set has <number of entries> entries
    

## Variables Used in Syslog Messages

Syslog messages often include variables. The following table lists most variables that are used in this guide to describe syslog messages. Some variables that appear in only one syslog message are not listed.

Variable Fields in Syslog Messages

|     Variable     |                                                                     Description                                                                      |
|------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
|      _acl_ID_      |                                                                     An ACL name.                                                                     |
|      _bytes_       |                                                                 The number of bytes.                                                                 |
|       _code_       |       A decimal number returned by the syslog message to indicate the cause or source of the error, according to the syslog message generated.       |
|     _command_      |                                                                   A command name.                                                                    |
| _command_modifier_ | The command_modifier is one of the following strings:

-   cmd (this string means the command has no modifier)
-   clear
-   no
-   show |
|   _connections_    |                                                              The number of connections.                                                              |
| _connection_type_  | The connection type:

-   SIGNALLING UDP
-   SIGNALLING TCP
-   SUBSCRIBE UDP
-   SUBSCRIBE TCP
-   Via UDP
-   Route
-   RTP
-   RTCP |
|       _dec_        |                                                                   Decimal number.                                                                    |
|   _dest_address_   |                                                         The destination address of a packet.                                                         |
|    _dest_port_     |                                                             The destination port number.                                                             |
|      _device_      |      The memory storage device. For example, the floppy disk, internal flash memory, TFTP, the failover standby unit, or the console terminal.       |
|      _econns_      |                                                           Number of embryonic connections.                                                           |
|      _elimit_      |                                       Number of embryonic connections specified in the static or nat command.                                        |
|     _filename_     |                                            A filename of the type ASAimage, ASDM file, or configuration.                                             |
|    _ftp-server_    |                                                       External FTP server name or IP address.                                                        |
| _gateway_address_  |                                                           The network gateway IP address.                                                            |
|  _global_address_  |                                          Global IP address, an address on a lower security level interface.                                          |
|   _global_port_    |                                                               The global port number.                                                                |
|       _hex_        |                                                                 Hexadecimal number.                                                                  |
|  _inside_address_  |                                    Inside (or local) IP address, an address on a higher security level interface.                                    |
|   _inside_port_    |                                                               The inside port number.                                                                |
|  _interface_name_  |                                                              The name of the interface.                                                              |
|    _IP_address_    |                                        IP address in the form _n_ _n_ _n_ _n_ , where _n_ is an integer from 1 to 255.                                         |
|   _MAC_address_    |                                                                   The MAC address.                                                                   |
|  _mapped_address_  |                                                              The translated IP address.                                                              |
|   _mapped_port_    |                                                             The translated port number.                                                              |
|  _message_class_   |                                       Category of syslog message associated with a functional area of the ASA.                                       |
|   _message_list_   |                        Name of a file you create containing a list of syslog message ID numbers, classes, or severity levels.                        |
|  _message_number_  |                                                                The syslog message ID.                                                                |
|      _nconns_      |                                            Number of connections permitted for the static or xlate table.                                            |
|     _netmask_      |                                                                   The subnet mask.                                                                   |
|      _number_      |                                               A number. The exact form depends on the syslog message.                                                |
|      _octal_       |                                                                    Octal number.                                                                     |
| _outside_address_  | Outside (or foreign) IP address, an address of a syslog server typically on a lower security level interface in a network beyond the outside router. |
|   _outside_port_   |                                                               The outside port number.                                                               |
|       _port_       |                                                             The TCP or UDP port number.                                                              |
| _privilege_level_  |                                                              The user privilege level.                                                               |
|     _protocol_     |                                             The protocol of the packet, for example, ICMP, TCP, or UDP.                                              |
|   _real_address_   |                                                           The real IP address, before NAT.                                                           |
|    _real_port_     |                                                          The real port number, before NAT.                                                           |
|      _reason_      |                                             A text string describing the reason for the syslog message.                                              |
|     _service_      |                                          The service specified by the packet, for example, SNMP or Telnet.                                           |
|  _severity_level_  |                                                       The severity level of a syslog message.                                                        |
|  _source_address_  |                                                           The source address of a packet.                                                            |
|   _source_port_    |                                                               The source port number.                                                                |
|      _string_      |                                                        Text string (for example, a username).                                                        |
|    _tcp_flags_     | Flags in the TCP header such as:

-   ACK
-   FIN
-   PSH
-   RST
-   SYN
-   URG |
|       _time_       |                                                           Duration, in the format _hh_ _mm_ _ss_                                                           |
|       _url_        |                                                                        A URL.                                                                        |
|       _user_       |                                                                     A username.                                                                      |

[![Back to Top](https://www.cisco.com/etc/designs/cdc/fw/i/responsive/Default-bTop-36.svg)](https://www.cisco.com/c/en/us/td/docs/security/asa/syslog/asa-syslog/messages-listed-by-severity-level.html# "Back to Top")