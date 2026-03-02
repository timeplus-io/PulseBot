## Messages 101001 to 109213

This section includes messages from 101001 to 109213.

### 101001

**Error Message** `%ASA-1-101001: (Primary) Failover cable OK.`

**Explanation** The failover cable is present and functioning correctly. Primary can also be listed as Secondary for the secondary unit.

**Recommended Action** None required.

### 101002

**Error Message** `%ASA-1-101002: (Primary) Bad failover cable.`

**Explanation** The failover cable is present, but not functioning correctly. Primary can also be listed as Secondary for the secondary unit.

**Recommended Action** Replace the failover cable.

### 101003, 101004

**Error Message** `%ASA-1-101003: (Primary) Failover cable not connected (this unit)`

**Error Message** `%ASA-1-101004: (Secondary) Failover cable not connected (other unit)`

**Explanation** Failover mode is enabled, but the failover cable is not connected to one unit of the failover pair. Primary can also be listed as Secondary for the secondary unit.

**Recommended Action** Connect the failover cable to both units of the failover pair.

### 101005

**Error Message** `%ASA-1-101005: (Primary) Error reading failover cable status.`

**Explanation** The failover cable is connected, but the primary unit is unable to determine its status.

**Recommended Action** Replace the cable.

### 103001

**Error Message** `%ASA-1-103001: (Primary) No response from other firewall (reason code = _code_).`

**Explanation** The primary unit is unable to communicate with the secondary unit over the failover cable. Primary can also be listed as Secondary for the secondary unit. The following table lists the reason codes and the descriptions to determine why the failover occurred.

| Reason Code |                                                                                               Description                                                                                                |
|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      1      | The local unit is not receiving the hello packet on the failover LAN interface when LAN failover occurs or on the serial failover cable when serial failover occurs, and declares that the peer is down. |
|      2      |                        An interface did not pass one of the four failover tests, which are as follows: 1) Link Up, 2) Monitor for Network Traffic, 3) ARP, and 4) Broadcast Ping.                        |
|      3      |                                                               No proper ACK for 15+ seconds after a command was sent on the serial cable.                                                                |
|      4      |            The failover LAN interface is down, and other data interfaces are not responding to additional interface testing. In addition, the local unit is declaring that the peer is down.             |
|      5      |                                                               The standby peer went down during the configuration synchronization process.                                                               |
|      6      |                                                                   Replication is not complete; the failover unit is not synchronized.                                                                    |

**Recommended Action** Verify that the failover cable is connected correctly and both units have the same hardware, software, and configuration. If the problem persists, contact the Cisco TAC.

### 103002

**Error Message** `%ASA-1-103002: (Primary) Other firewall network interface _interface_number_ OK.`

**Explanation** The primary unit has detected that the network interface on the secondary unit is okay. Primary can also be listed as Secondary for the secondary unit.

**Recommended Action** None required.

### 103003

**Error Message** `%ASA-1-103003: (Primary) Other firewall network interface _interface_number_ failed.`

**Explanation** The primary unit has detected a bad network interface on the secondary unit. Primary can also be listed as Secondary for the secondary unit.

**Recommended Action** Check the network connections on the secondary unit and the network hub connection. If necessary, replace the failed network interface.

### 103004

**Error Message** `%ASA-1-103004: (Primary) Other firewall reports this firewall failed. _reason-string_`

**Explanation** The primary unit received a message from the secondary unit indicating that the primary unit has failed. Primary can also be listed as Secondary for the secondary unit. The reason can be one of the following:

-   Missed poll packets on failover command interface exceeded threshold.
-   LAN failover interface failed.
-   Peer failed to enter Standby Ready state.
-   Failed to complete configuration replication. This firewall's configuration may be out of sync.
-   Failover message transmit failure and no ACK for busy condition received.

**Recommended Action** Verify the status of the primary unit.

### 103005

**Error Message** `%ASA-1-103005: (Primary) Other firewall reporting failure. Reason: _SSM_card_failure_`

**Explanation** The secondary unit has reported an SSM card failure to the primary unit. Primary can also be listed as Secondary for the secondary unit.

**Recommended Action** Verify the status of the secondary unit.

### 103006

**Error Message** `%ASA-1-103006: (Primary|Secondary) Mate version _ver_num_ is not compatible with ours _ver_num_.`

**Explanation** The Secure Firewall ASA has detected a peer unit that is running a version that is different than the local unit and is not compatible with the HA Hitless Upgrade feature.

-   _ver\_num_ —Version number.
    

**Recommended Action** Install the same or a compatible version image on both units.

### 103007

**Error Message** `%ASA-1-103007: (Primary|Secondary) Mate version _ver_num_ is not identical with ours _ver_num_.`

**Explanation** The Secure Firewall ASA has detected that the peer unit is running a version that is not identical, but supports Hitless Upgrade and is compatible with the local unit. The system performance may be degraded because the image version is not identical, and the Secure Firewall ASA may develop a stability issue if the nonidentical image runs for an extended period.

-   ver\_num—Version number

**Recommended Action** Install the same image version on both units as soon as possible.

### 103008

**Error Message** `%ASA-1-103008: _host_ Mate hwdib index _Idx_ is not identical with ours.`

**Explanation** The number of interfaces on the active and standby units is not the same.

**Recommended Action** Verify that the units have the same number of interfaces. You might need to install additional interface modules, or use different devices. After the physical interfaces match, force a configuration sync by entering the **write standby** command.

### 104001, 104002

**Error Message** `%ASA-1-104001: (Primary) Switching to ACTIVE - _string_.`

**Error Message** `%ASA-1-104002: (Secondary) Switching to STANDBY - _string_.`

**Explanation** You have forced the failover pair to switch roles, either by entering the failover active command on the standby unit, or the no failover active command on the active unit. Primary can also be listed as Secondary for the secondary unit. Possible values for the string variable are as follows:

-   state check
-   bad/incomplete config
-   ifc \[interface\] check, mate is healthier
-   the other side wants me to standby
-   in failed state, cannot be active
-   switch to failed state
-   other unit set to active by CLI config command fail active

**Recommended Action** If the message occurs because of manual intervention, no action is required. Otherwise, use the cause reported by the secondary unit to verify the status of both units of the pair.

### 104003

**Error Message** `%ASA-1-104003: (Primary) Switching to FAILED.`

**Explanation** The primary unit has failed.

**Recommended Action** Check the messages for the primary unit for an indication of the nature of the problem (see message 104001). Primary can also be listed as Secondary for the secondary unit.

### 104004

**Error Message** `%ASA-1-104004: (Primary) Switching to OK.`

**Explanation** A previously failed unit reports that it is operating again. Primary can also be listed as Secondary for the secondary unit.

**Recommended Action** None required.

### 104500

**Error Message** `%ASA-1-104500: (Primary|Secondary) Switching to ACTIVE - switch reason: _reason_`

**Explanation**

This HA unit is assuming the Active role for the Cloud HA pair. Possible values for the reason string are:

-   no existing Active unit present
    
-   unable to send message to Active unit
    
-   no response to Hello message received from Active unit
    
-   user initiated failover on this unit
    
-   user initiated failover on peer unit
    
-   invalid message received on failover connection
    

**Recommended Action** None required.

### 104501

**Error Message** `%ASA-1-104501: (Primary|Secondary) Switching to BACKUP - switch reason: _reason_`

**Explanation** This HA unit is assuming the Backup role for the Cloud HA pair. Possible values for the reason string are:

-   existing Active unit present
    
-   user initiated failover on this unit
    
-   user initiated failover on peer unit
    

**Recommended Action** None required.

### 104502

**Error Message** `%ASA-1-104502: (Primary|Secondary) Becoming Backup unit failed`

**Explanation** This HA unit failed to assume the Backup role for the Cloud HA pair. The reason being the same as that of 104500 and 104501.

**Recommended Action** None required.

### 105001

**Error Message** `%ASA-1-105001: (Primary) Disabling failover.`

**Explanation** In version 7.x and later, this message may indicate the following: failover has been automatically disabled because of a mode mismatch (single or multiple), a license mismatch (encryption or context), or a hardware difference (one unit has an IPS SSM installed, and its peer has a CSC SSM installed). Primary can also be listed as Secondary for the secondary unit.

**Recommended Action** None required.

### 105002

**Error Message** `%ASA-1-105002: (Primary) Enabling failover.`

**Explanation** You have used the failover command with no arguments on the console, after having previously disabled failover. Primary can also be listed as Secondary for the secondary unit.

**Recommended Action** None required.

### 105003

**Error Message** `%ASA-1-105003: (Primary) Monitoring on interface _interface_name_ waiting`

**Explanation** The Secure Firewall ASA is testing the specified network interface with the other unit of the failover pair. Primary can also be listed as Secondary for the secondary unit.

| ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)

**Note** | ___

There could be delay in the logging of syslog when compared to the actual status change. This delay is due to the poll time and hold time that is configured for the interface monitoring.

___ |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

**Recommended Action** None required. The Secure Firewall ASA monitors its network interfaces frequently during normal operation.

### 105004

**Error Message** `%ASA-1-105004: (Primary) Monitoring on interface _interface_name_ normal`

**Explanation** The test of the specified network interface was successful. Primary can also be listed as Secondary for the secondary unit.

| ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)

**Note** | ___

There could be delay in the logging of syslog when compared to the actual status change. This delay is due to the poll time and hold time that is configured for the interface monitoring.

___ |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

**Recommended Action** None required.

### 105005

**Error Message** `%ASA-1-105005: (Primary) Lost Failover communications with mate on interface _interface_name_`

**Explanation** One unit of the failover pair can no longer communicate with the other unit of the pair. Primary can also be listed as Secondary for the secondary unit.

**Recommended Action** Verify that the network connected to the specified interface is functioning correctly.

### 105006, 105007

**Error Message** `%ASA-1-105006: (Primary) Link status 'Up' on interface _interface_name_`

**Error Message** `%ASA-1-105007: (Primary) Link status 'Down' on interface _interface_name_.`

**Explanation** The results of monitoring the link status of the specified interface have been reported. Primary can also be listed as Secondary for the secondary unit.

**Recommended Action** If the link status is down, verify that the network connected to the specified interface is operating correctly.

### 105008

**Error Message** `%ASA-1-105008: (Primary) Testing Interface _interface_name_`

**Explanation** Testing of a specified network interface has occurred. This testing is performed only if the Secure Firewall ASA fails to receive a message from the standby unit on that interface after the expected interval. Primary can also be listed as Secondary for the secondary unit.

**Recommended Action** None required.

### 105009

**Error Message** `%ASA-1-105009: (Primary) Testing on interface _interface_name_ _{Passed|Failed}_`

**Explanation** The result (either Passed or Failed) of a previous interface test has been reported. Primary can also be listed as Secondary for the secondary unit.

**Recommended Action** None required if the result is Passed. If the result is Failed, you should check the network cable connection to both failover units, that the network itself is functioning correctly, and verify the status of the standby unit.

### 105010

**Error Message** `%ASA-3-105010: (Primary) Failover message block alloc failed`

**Explanation** Block memory was depleted. This is a transient message and the Secure Firewall ASA should recover. Primary can also be listed as Secondary for the secondary unit.

**Recommended Action** Use the show blocks command to monitor the current block memory.

### 105011

**Error Message** `%ASA-1-105011: (Primary) Failover cable communication failure`

**Explanation** The failover cable is not permitting communication between the primary and secondary units. Primary can also be listed as Secondary for the secondary unit.

**Recommended Action** Ensure that the cable is connected correctly.

### 105020

**Error Message** `%ASA-1-105020: (Primary) Incomplete/slow config replication`

**Explanation** When a failover occurs, the active Secure Firewall ASA detects a partial configuration in memory. Normally, this is caused by an interruption in the replication service. Primary can also be listed as Secondary for the secondary unit.

**Recommended Action** After the Secure Firewall ASA detects the failover, the Secure Firewall ASA automatically reboots and loads the configuration from flash memory and/or resynchronizes with another Secure Firewall ASA. If failovers occurs continuously, check the failover configuration and make sure that both Secure Firewall ASAs can communicate with each other.

### 105021

**Error Message** `%ASA-1-105021: (Failover_unit) Standby unit failed to sync due to a locked _context_name_ config. Lock held by _lock_owner_name_`

**Explanation** During configuration synchronization, a standby unit will reload itself if some other process locks the configuration for more than five minutes, which prevents the failover process from applying the new configuration. This can occur when an administrator pages through a running configuration on the standby unit while configuration synchronization is in process. See also the show running-config command in privileged EXEC mode and the pager lines num command in global configuration mode in the _Command Reference Guides_.

**Recommended Action** Avoid viewing or modifying the configuration on the standby unit when it first boots up and is in the process of establishing a failover connection with the active unit.

### 105022

**Error Message** `%ASA-1-105022: (_host_) Config replication failed with reason = _reason_`

**Explanation** When high availability replication fails, the message is generated. Where,

-   _host_—Indicates the current failover unit, namely, primary or secondary.
    
-   _reason_—The time out expiry reason for termination of the failover configuration replication:
    
    -   CFG\_SYNC\_TIMEOUT—Where, the 60-second timer for the configuration to be replicated from active to standby lapses, and the device starts to reboot.
        
    -   CFG\_PROGRESSION\_TIMEOUT—Where, the interval timer of 6 hours which governs the high availability configuration replication lapses.
        

**Recommended Action** None.

### 105031

**Error Message** `%ASA-1-105031: Failover LAN interface is up`

**Explanation** The LAN failover interface link is up.

**Recommended Action** None required.

### 105032

**Error Message** `%ASA-1-105032: LAN Failover interface is down`

**Explanation** The LAN failover interface link is down.

**Recommended Action** Check the connectivity of the LAN failover interface. Make sure that the speed or duplex setting is correct.

### 105033

**Error Message** `%ASA-1-105033: LAN FO cmd Iface down and up again`

**Explanation** LAN interface of failover gone down.

**Recommended Action** Verify the failover link, might be a communication problem.

### 105034

**Error Message** `%ASA-1-105034: Receive a LAN_FAILOVER_UP message from peer.`

**Explanation** The peer has just booted and sent the initial contact message.

**Recommended Action** None required.

### 105035

**Error Message** `%ASA-1-105035: Receive a LAN failover interface down msg from peer.`

**Explanation** The peer LAN failover interface link is down. The unit switches to active mode if it is in standby mode.

**Recommended Action** Check the connectivity of the peer LAN failover interface.

### 105036

**Error Message** `%ASA-1-105036: dropped a LAN Failover command message.`

**Explanation** The Secure Firewall ASA dropped an unacknowledged LAN failover command message, indicating a connectivity problem exists on the LAN failover interface.

**Recommended Action** Check that the LAN interface cable is connected.

### 105037

**Error Message** `%ASA-1-105037: (_Primary and Standby_ ) Both units are switching back and forth as the active unit`

**Explanation** The primary and standby units are switching back and forth as the active unit, indicating a LAN failover connectivity problem or software bug exists.

**Recommended Action** Make sure that the LAN interface cable is connected.

### 105038

**Error Message** `%ASA-1-105038: (Primary) Interface count mismatch`

**Explanation** When a failover occurs, the active Secure Firewall ASA detects a partial configuration in memory. Normally, this is caused by an interruption in the replication service. Primary can also be listed as Secondary for the secondary unit.

**Recommended Action** Once the failover is detected by the Secure Firewall ASA, the Secure Firewall ASA automatically reboots and loads the configuration from flash memory and/or resynchronizes with another Secure Firewall ASA. If failovers occur continuously, check the failover configuration and make sure that both Secure Firewall ASAs can communicate with each other.

### 105039

**Error Message** `%ASA-1-105039: (Primary) Unable to verify the Interface count with mate. Failover may be disabled in mate.`

**Explanation** Failover initially verifies that the number of interfaces configured on the primary and secondary Secure Firewall ASAs are the same. This message indicates that the primary Secure Firewall ASA is not able to verify the number of interfaces configured on the secondary Secure Firewall ASA. This message indicates that the primary Secure Firewall ASA is not able to communicate with the secondary Secure Firewall ASA over the failover interface. Primary can also be listed as Secondary for the secondary unit.

**Recommended Action** Verify the failover LAN, interface configuration, and status on the primary and secondary Secure Firewall ASAs. Make sure that the secondary Secure Firewall ASA is running the Secure Firewall ASA application and that failover is enabled.

### 105040

**Error Message** `%ASA-1-105040: (Primary) Mate failover version is not compatible.`

**Explanation** The primary and secondary Secure Firewall ASAs should run the same failover software version to act as a failover pair. This message indicates that the secondary Secure Firewall ASA failover software version is not compatible with the primary Secure Firewall ASA. Failover is disabled on the primary Secure Firewall ASA. Primary can also be listed as Secondary for the secondary Secure Firewall ASA.

**Recommended Action** Maintain consistent software versions between the primary and secondary Secure Firewall ASAs to enable failover.

### 105041

**Error Message** `%ASA-1-105041: cmd failed during sync`

**Explanation** Replication of the nameif command failed, because the number of interfaces on the active and standby units is not the same.

**Recommended Action** Verify that the units have the same number of interfaces. You might need to install additional interface modules, or use different devices. After the physical interfaces match, force a configuration sync by entering the **write standby** command.

### 105042

**Error Message** `%ASA-1-105042: (Primary) Failover interface OK`

**Explanation** The interface that sends failover messages could go down when physical status of the failover link is down or when L2 connectivity between the failover peers is lost resulting in dropping of ARP packets. This message is generated after restoring the L2 ARP connectivity.

**Recommended Action** None required.

### 105043

**Error Message** `%ASA-1-105043: (Primary) Failover interface failed`

**Explanation** This syslog is generated when physical status of the failover link is down or when L2 connectivity between the failover peers is lost. The disconnection results in loss of ARP packets flowing between the units.

**Recommended Action**

-   Check the physical status of the failover link, ensure its physical and operational status is functional.
    
-   Ensure ARP packets flow through the transit path of the failover links between the failover pairs.
    

### 105044

**Error Message** `%ASA-1-105044: (Primary) Mate operational mode (_mode_) is not compatible with my mode (_mode_).`

**Explanation** When the operational mode (single or multiple) does not match between failover peers, failover will be disabled.

**Recommended Action** Configure the failover peers to have the same operational mode, and then reenable failover.

### 105045

**Error Message** `%ASA-1-105045: (Primary) Mate license (_number_contexts_) is not compatible with my license (_number_contexts_).`

**Explanation** When the feature licenses do not match between failover peers, failover will be disabled.

**Recommended Action** Configure the failover peers to have the same feature license, and then reenable failover.

### 105046

**Error Message** `%ASA-1-105046: (Primary|Secondary) Mate has a different chassis`

**Explanation** Two failover units have a different type of chassis. For example, one has a three-slot chassis; the other has a six-slot chassis.

**Recommended Action** Make sure that the two failover units are the same.

### 105047

**Error Message** `%ASA-1-105047: Mate has a _io_card_name1_ card in slot _slot_number_ which is different from my _io_card_name2_`

**Explanation** The two failover units have different types of cards in their respective slots.

**Recommended Action** Make sure that the card configurations for the failover units are the same.

### 105048

**Error Message** `%ASA-1-105048: (_unit_) Mate's service module (_application_) is different from mine (_application_).`

**Explanation** The failover process detected that different applications are running on the service modules in the active and standby units. The two failover units are incompatible if different service modules are used.

-   unit—Primary or secondary
-   application—The name of the application, such as InterScan Security Card

**Recommended Action** Make sure that both units have identical service modules before trying to reenable failover.

### 105050

**Error Message** `%ASA-3-105050: _(host)_ Number of Ethernet interfaces on Standby unit _(int_number)_ is less than number on Active unit _(int_number)_.`

**Explanation** Number of Ethernet interfaces on standby unit is less than that on active unit.

**Recommended Action** Secure Firewall ASA with same number of interfaces should be paired up with each other. Verify that the units have the same number of interfaces. You might need to install additional interface modules, or use different devices. After the physical interfaces match, force a configuration sync by entering the **write standby** command.

### 105052

**Error Message** `%ASA-3-105052: HA:cipher in use _algorithm name_ strong encryption is _status_, please reboot to use strong cipher and preferably change the key in use`

**Explanation** When the failover key is configured prior to a license update, the weaker cipher is not switched to a stronger cipher automatically. This syslog is generated, every 30 seconds to alert that a weaker cipher is still being used when a stronger cipher is available.

**Example** %ASA\-3-105052 HA cipher in use DES strong encryption is AVAILABLE, please reboot to use strong cipher and preferably change the key in use.

**Recommended Action** Remove the failover key configuration and reconfigure the key. Reload the standby, and then reload the active device.

### 105500

**Error Message** `%ASA-5-105500: (Primary|Secondary) Started HA`

**Explanation** Cloud HA has been enabled on this ASA Virtual.

**Recommended Action** None required.

### 105501

**Error Message** `%ASA-5-105501: (Primary|Secondary) Stopping HA`

**Explanation** Cloud HA has been disabled on this ASA Virtual.

**Recommended Action** None required.

### 105502

**Error Message** `%ASA-1-105502: (Primary|Secondary) Restarting Cloud HA on this unit, reason: _string_`

**Explanation** An error occurred and caused this HA unit to restart Cloud HA. Possible values for the reason string are:

-   failed to become Backup unit
    
-   unable to create failover connection
    

**Recommended Action** None required.

### 105503

**Error Message** `%ASA-5-105503: (Primary|Secondary) Internal state changed from _previous_state_ to _new_state_`

**Explanation** There was a change to the internal HA state.

**Recommended Action** None required.

### 105504

**Error Message** `%ASA-5-105504: (Primary|Secondary) Connected to peer _peer-ip_:_port_`

**Explanation** This HA unit has established communication with its HA peer.

**Recommended Action** None required.

### 105505

**Error Message** `%ASA-4-105505: (Primary|Secondary) Failed to connect to peer unit _peer-ip_:_port_`

**Explanation** This HA unit has failed to establish communication with its HA peer.

**Recommended Action**

This may occur if there is no HA peer present. If there is an HA peer present with failover enabled there could be connectivity issue between peers. Verify using the show failover command that:

-   The peer IP address configured on each unit is matches an interface IP address on the peer
    
-   The peer port number on each unit matches the failover control (server) port on the peer
    
-   The interfaces used for the peer connection are not shutdown
    
-   Any IP routes required for IP connectivity are present
    

### 105506

**Error Message** `%ASA-2-105506: (Primary|Secondary) Unable to create socket for port _port_ for _failover_connection|load_balancer_probes_, error: _error_string_`

**Explanation** An internal error occurred while attempting to create a socket needed for the failover connection or resonding to Azure load balancer probes.

**Recommended Action** Copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105507

**Error Message** `%ASA-2-105507: (Primary|Secondary) Unable to bind socket for port _port_ for _failover_connection|load_balancer_probes_, error: _error_string_`

**Explanation** An internal error occurred while attempting to start a socket needed for the failover connection or resonding to Azure load balancer probes.

**Recommended Action** Copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105508

**Error Message** `%ASA-2-105508: (Primary|Secondary) Error creating failover connection socket for port _port_`

**Explanation** An internal error occurred while attempting to create a socket on the Active unit for exchanging failover control messages with the Backup unit.

**Recommended Action** This message is preceeded by a 104509 or 104510 message. Follow the Recommended Action for the message that precedes this one.

### 105509

**Error Message** `%ASA-3-105509: (Primary|Secondary) Error sending _message_name_ message to peer unit _peer-ip_, error: _error_string_`

**Explanation** An error occurred while attempting to send a failover control message to the peer unit.

**Recommended Action** If the error was not caused by the failure of the peer unit, copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105510

**Error Message** `%ASA-3-105510: (Primary|Secondary) Error receiving message from peer unit _peer-ip_, error: _error_string_`

**Explanation** An error occurred while attempting to receive a failover control message to the peer unit.

**Recommended Action** If the error was not caused by the failure of the peer unit, copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105511

**Error Message** `%ASA-3-105511: (Primary|Secondary) Incomplete read of message header of message from peer unit _peer-ip_: _bytes_ bytes read of expected _header_length_ header byte`

**Explanation** An error occurred while attempting to receive a failover control message to the peer unit.

**Recommended Action** If the error was not caused by the failure of the peer unit, copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105512

**Error Message** `%ASA-3-105512: (Primary|Secondary) Error receiving message body of message from peer unit _peer-ip_, error: _error_string_`

**Explanation** An error occurred while attempting to receive a failover control message to the peer unit.

**Recommended Action** If the error was not caused by the failure of the peer unit, copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105513

**Error Message** `%ASA-3-105513: (Primary|Secondary) Incomplete read of message body of message from peer unit _peer-ip_: _bytes_ bytes read of expected _message_length_ message body bytes`

**Explanation** An error occurred while attempting to receive a failover control message to the peer unit.

**Recommended Action** If the error was not caused by the failure of the peer unit, copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105514

**Error Message** `%ASA-3-105514: (Primary|Secondary) Error occurred when responding to _message_name_ message received from peer unit _peer-ip_, error: _error_string_`

**Explanation** An error occurred while attempting to receive a failover control message to the peer unit.

**Recommended Action** If the error was not caused by the failure of the peer unit, copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105515

**Error Message** `%ASA-3-105515: (Primary|Secondary) Error receiving _message_name_ message from peer unit _peer-ip_, error: _error_string_`

**Explanation** An error occurred while attempting to receive a failover control message to the peer unit.

**Recommended Action** If the error was not caused by the failure of the peer unit, copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105516

**Error Message** `%ASA-3-105516: (Primary|Secondary) Incomplete read of message header of _message_name_ message from peer unit _peer-ip_: _bytes_ bytes read of expected _header_length_ header bytes`

**Explanation** An error occurred while attempting to receive a failover control message to the peer unit.

**Recommended Action** If the error was not caused by the failure of the peer unit, copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105517

**Error Message** `%ASA-3-105517: (Primary|Secondary) Error receiving message body of _message_name_ message from peer unit _peer-ip_, error: _error_string_`

**Explanation** An error occurred while attempting to receive a failover control message to the peer unit.

**Recommended Action** If the error was not caused by the failure of the peer unit, copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105518

**Error Message** `%ASA-3-105518: (Primary|Secondary) Incomplete read of message body of _message_name_ message from peer unit _peer-ip_: _bytes_ bytes read of expected _message_length_ message body bytes`

**Explanation** An error occurred while attempting to receive a failover control message to the peer unit.

**Recommended Action** If the error was not caused by the failure of the peer unit, copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105519

**Error Message** `%ASA-3-105519: (Primary|Secondary) Invalid response to _message_name_ message received from peer unit _peer-ip_: type _message_type_, version _message_version_, length _message_length_`

**Explanation** An unexpected message was received in response to a failover control message.

**Recommended Action** Copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105520

**Error Message** `%ASA-5-105520: (Primary|Secondary) Responding to Azure Load Balancer probes`

**Explanation** The Active unit has begun responding to Azure Load Balancer probes.

**Recommended Action** None required

### 105521

**Error Message** `%ASA-5-105521: (Primary|Secondary) No longer responding to Azure Load Balancer probes`

**Explanation** The Backup unit has stopped responding to Azure Load Balancer probes.

**Recommended Action** None required

### 105522

**Error Message** `%ASA-5-105522: (Primary|Secondary) Updating route-table _route_table_name_`

**Explanation** The Active unit has started the process of updating an Azure route-table.

**Recommended Action** None required

### 105523

**Error Message** `%ASA-5-105523: (Primary|Secondary) Updated route-table _route_table_name_`

**Explanation** The Active unit has completed the process of updating an Azure route-table.

**Recommended Action** None required

### 105524

**Error Message** `%ASA-4-105524: (Primary|Secondary) Transitioning to Negotiating state due to the presence of another Active HA unit`

**Explanation** Another Active HA unit was detected, transitioning unit to negotiating state.

**Recommended Action** None required

### 105524

**Error Message** `%ASA-4-105524: (Primary|Secondary) Transitioning to Negotiating state due to the presence of another Active HA unit`

**Explanation** Another Active HA unit was detected, transitioning unit to negotiating state.

**Recommended Action** None required

### 105525

**Error Message** `%ASA-2-105525: (Primary|Secondary) Incomplete configuration to initiate access token change request`

**Explanation** An attempt was made to acquire an access token but there was not enough configuration information need to initiate the request.

**Recommended Action** Ensure that an Azure authentication client ID, tenant ID and secret key are all present in the ASA configuration.

### 105526

**Error Message** `%ASA-2-105526: (Primary|Secondary) Unexpected status in response to access token request: _status_ (_status_string_)`

**Explanation** A response to an Azure access token request was received but the HTTP status code in the response was not 200 (OK).

**Recommended Action** Ensure that the Azure authentication client ID, tenant ID and secret key are all correct in the ASA configuration.

### 105527

**Error Message** `%ASA-2-105527: (Primary|Secondary) Failure reading response to access token request`

**Explanation** An internal error occurred while receiving a response to an Azure access token request.

**Recommended Action** Copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105528

**Error Message** `%ASA-2-105528: (Primary|Secondary) No access token in response to access token request`

**Explanation** A response to an Azure route change request was received but it did not contain an access\_token value.

**Recommended Action** Verify that the Azure authentication client ID, tenant ID and secret key are all correct in the ASA configuration.

### 105529

**Error Message** `%ASA-2-105529: (Primary|Secondary) Error creating authentication header from access token`

**Explanation** An internal error occurred while attempting to create an authentication header needed for changing Azure routes.

**Recommended Action** Copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105530

**Error Message** `%ASA-2-105530: (Primary|Secondary) No response to access token request from _url_`

**Explanation** Azure route-table information was not able to be obtained for an Azure route-table change.

**Recommended Action** Verify route-table name is correct in ASA configuration and exists in Azure.

### 105531

**Error Message** `%ASA-2-105531: (Primary|Secondary) Failed to obtain route-table information needed for change request for route-table _route_table_name_`

**Explanation** Azure route-table information was not able to be obtained for an Azure route-table change.

**Recommended Action** Verify route-table name is correct in ASA configuration and exists in Azure.

### 105532

**Error Message** `%ASA-2-105532: (Primary|Secondary) Unexpected status in response to route-table change request for route-table _route_table_name_: _status_ (_status_string_)`

**Explanation** A response to an Azure route-tablechange request was received but the HTTP status code in the response was not 200 (OK).

**Recommended Action** Verify that the configured Azure subscription ID, route-table name and route-table resource group are correct.

### 105533

**Error Message** `%ASA-2-105533: (Primary|Secondary) Failure reading response to route-table change request for route-table _route_table_name_`

**Explanation** An internal error occurred while receiving a response to an Azure route-table change request.

**Recommended Action** Copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105534

**Error Message** `%ASA-2-105534: (Primary|Secondary) No provisioning state in response to route-table change request route-table route_table_name`

**Explanation** A response to an Azure route-table change request was received but it did not contain a provisioningState value containing the route-table change status.

**Recommended Action** Copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105535

**Error Message** `%ASA-2-105535: (Primary|Secondary) No response to route-table change request for route-table _route_table_name_ from _url_`

**Explanation** No response was received to an Azure route-table change request.

**Recommended Action** Verify that management.azure.com is reachable from the ASA Virtual.

### 105536

**Error Message** `%ASA-2-105536: (Primary|Secondary) Failed to obtain Azure authentication header for route status request for route _route_name_`

**Explanation** An Azure access token was not able to be obtained for an Azure route status query.

**Recommended Action** See the Recommended Action of access token related message that preceeds this message.

### 105537

**Error Message** `%ASA-2-105537: (Primary|Secondary) Unexpected status in response to route state request for route _route_name_: _status_ (_status_string_)`

**Explanation** A response to an Azure route state request was received but the HTTP status code in the response was not 200 (OK).

**Recommended Action** Verify that the configured Azure subscription ID, route table name and route table resource group are correct.

### 105538

**Error Message** `%ASA-2-105538: (Primary|Secondary) Failure reading response to route state request for route _route_name_`

**Explanation** An internal error occurred while receiving a response to an Azure route state request.

**Recommended Action** Copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105539

**Error Message** `%ASA-2-105539: (Primary|Secondary) No response to route state request for route _route_name_ from _url_`

**Explanation** No response was received to an Azure route state request.

**Recommended Action** Verify that management.azure.com is reachable from the ASA Virtual.

### 105540

**Error Message** `%ASA-2-105540: (Primary|Secondary) No route-tables configured`

**Explanation** No Azure route-tables were detected to change.

**Recommended Action** Confirm that route-tables are correctly configured in ASA configuration.

### 105541

**Error Message** `%ASA-2-105541: (Primary|Secondary) Failed to update route-table _route_table_name_, provisioning state: _state_string_`

**Explanation** A response to an Azure route-table state request was received that contained a provisioningState that indicated a failure to update the route-table.

**Recommended Action** The Active unit will make three attempts to update an Azure route-table. If all three attempts fail, copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105542

**Error Message** `%ASA-5-105542: (Primary|Secondary) Enabling load balancer probe responses`

**Explanation** The Active unit is will now respond to probes from the Azure Load Balancer.

**Recommended Action** None required.

### 105543

**Error Message** `%ASA-5-105543: (Primary|Secondary) Disabling load balancer probe responses`

**Explanation** The Active unit is no longer responding to probes from the Azure Load Balancer.

**Recommended Action** None required.

### 105544

**Error Message** `%ASA-2-105544: (Primary|Secondary) Error creating load balancer probe socket for port _port_`

**Explanation** An internal error occurred while attempting to create a socket for responding to probes from an Azure Load Balancer.

**Recommended Action** This message will be preceeded by a 104509 or 104510 message. Follow the Recommended Action for the message that precedes this one.

### 105545

**Error Message** `%ASA-3-105545: (Primary|Secondary) Error starting load balancer probe socket for port _port_, error code: _error_code_`

**Explanation** An internal error occurred while attempting to start receiving probes from an Azure Load Balancer. The Active unit will continue to attempt to enable the receiving of probes.

**Recommended Action** If this condition persists copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105546

**Error Message** `%ASA-3-105546: (Primary|Secondary) Error starting load balancer probe handler`

**Explanation** An internal error occurred while attempting to create a process for receiving probes from an Azure Load Balancer.

**Recommended Action** Copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105547

**Error Message** `%ASA-3-105547: (Primary|Secondary) Error generating encryption key for Azure secret key`

**Explanation** An internal error occurred while attempting to generate the encryption key used for encrypting the Azure secret key in the configuration.

**Recommended Action** Copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105548

**Error Message** `%ASA-3-105548: (Primary|Secondary) Error storing encryption key for Azure secret key`

**Explanation** An internal error occurred while attempting to store the encryption key used for encrypting the Azure secret key in the configuration.

**Recommended Action** Copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105549

**Error Message** `%ASA-3-105549: (Primary|Secondary) Error retrieving encryption key for Azure secret key`

**Explanation** An internal error occurred while attempting to retrieve the encryption key used for encrypting the Azure secret key in the configuration.

**Recommended Action** Copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105550

**Error Message** `%ASA-3-105550: (Primary|Secondary) Error encrypting Azure secret key`

**Explanation** An internal error occurred while encrypting the Azure secret key in the configuration.

**Recommended Action** Copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105551

**Error Message** `%ASA-3-105551: (Primary|Secondary) Error decrypting Azure secret key`

**Explanation** An internal error occurred while decrypting the Azure secret key in the configuration.

**Recommended Action** Copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 105552

**Error Message** `%ASA-5-105552: (Primary|Secondary) Stopped HA`

**Explanation** Cloud HA has been disabled on this ASA Virtual.

**Recommended Action** None required.

### 105553

**Error Message** `%ASA-4-105553: (Primary|Secondary) Detected another Active HA unit`

**Explanation** Another Active HA unit was detected.

**Recommended Action** None required

### 106001

**Error Message** `%ASA-2-106001: Inbound TCP connection denied from _IP_address_/_port_ to _IP_address_/_port_ flags _tcp_flags_ on interface _interface_name_`

**Explanation** An attempt was made to connect to an inside address is denied by the security policy that is defined for the specified traffic type. The IP address displayed is the real IP address instead of the IP address that appears through NAT. Possible tcp\_flags values correspond to the flags in the TCP header that were present when the connection was denied. For example, a TCP packet arrived for which no connection state exists in the Secure Firewall ASA, and it was dropped. The tcp\_flags in this packet are FIN and ACK.

The tcp\_flags are as follows:

-   ACK—The acknowledgment number was received
-   FIN—Data was sent
-   PSH—The receiver passed data to the application
-   RST—The connection was reset
-   SYN—Sequence numbers were synchronized to start a connection
-   URG—The urgent pointer was declared valid

**Recommended Action** None required.

### 106002

**Error Message** `%ASA-2-106002: _protocol_ Connection denied by outbound list acl_ID src inside_address dest outside_address`

**Explanation** The specified connection failed because of an outbound deny command. The protocol variable can be ICMP, TCP, or UDP.

**Recommended Action** Use the show outbound command to check outbound lists.

### 106006

**Error Message** `%ASA-2-106006: Deny inbound UDP from _outside_address_/_outside_port_ to _inside_address_/_inside_port_ on interface _interface_name_`

**Explanation** An inbound UDP packet was denied by the security policy that is defined for the specified traffic type.

**Recommended Action** None required.

### 106007

**Error Message** `%ASA-2-106007: Deny inbound UDP from _outside_address_/_outside_port_ to _inside_address_/_inside_port_ due to DNS _{Response|Query}_`

**Explanation** A UDP packet containing a DNS query or response was denied.

**Recommended Action** If the inside port number is 53, the inside host probably is set up as a caching name server. Add an access-list command statement to permit traffic on UDP port 53 and a translation entry for the inside host. If the outside port number is 53, a DNS server was probably too slow to respond, and the query was answered by another server.

### 106010

**Error Message** `%ASA-3-106010: Deny inbound __protocol__src_ [_interface_name_ : _source_address/source_port_ ] [([_idfw_user_ | _FQDN_string_ ], _sg_info_ )] _dst_ [_interface_name_ : _dest_address_ /_dest_port_ }[([_idfw_user_ | _FQDN_string_ ], _sg_info_ )]_`

**Explanation** An inbound connection was denied by your security policy.

**Recommended Action** Modify the security policy if traffic should be permitted. If the message occurs at regular intervals, contact the remote peer administrator.

### 106011

**Error Message** `%ASA-3-106011: Deny inbound (No xlate) _protocol_src_Interface:IP/port_dst_Interface-nameif:IP/port_`

**Explanation** The message appears under normal traffic conditions if there are internal users that are accessing the Internet through a web browser. Any time a connection is reset, when the host at the end of the connection sends a packet after the Secure Firewall ASA receives the connection reset, this message appears. It can typically be ignored.

**Recommended Action** Prevent this message from getting logged to the syslog server by entering the no logging message 106011 command.

### 106012

**Error Message** `%ASA-6-106012: Deny IP from _IP_address_ to _IP_address_, IP options: "_hex_"`

**Explanation** An IP packet was seen with IP options. Because IP options are considered a security risk, the packet was discarded.

**Recommended Action** Contact the remote host system administrator to determine the problem. Check the local site for loose source routing or strict source routing.

### 106013

**Error Message** `%ASA-2-106013: Dropping echo request from _IP_address_ to PAT address _IP_address_`

**Explanation** The Secure Firewall ASA discarded an inbound ICMP Echo Request packet with a destination address that corresponds to a PAT global address. The inbound packet is discarded because it cannot specify which PAT host should receive the packet.

**Recommended Action** None required.

### 106014

**Error Message** `%ASA-3-106014: Deny inbound _src_`

**Explanation** The Secure Firewall ASA denied any inbound ICMP packet access. By default, all ICMP packets are denied access unless specifically allowed.

**Recommended Action** None required.

### 106015

**Error Message** `%ASA-6-106015: Deny TCP (no connection) from _IP_address_ /port to _IP_address_ /port flags tcp_flags on interface interface_name.`

**Explanation** The Secure Firewall ASA discarded a TCP packet that has no associated connection in the Secure Firewall ASA connection table. The Secure Firewall ASA looks for a SYN flag in the packet, which indicates a request to establish a new connection. If the SYN flag is not set, and there is no existing connection, the Secure Firewall ASA discards the packet.

**Recommended Action** None required unless the Secure Firewall ASA receives a large volume of these invalid TCP packets. If this is the case, trace the packets to the source and determine the reason these packets were sent.

### 106016

**Error Message** `%ASA-2-106016: Deny IP spoof from (_ip_address_) to _ip_address_ on interface _interface_name_`

**Explanation** A packet arrived at the Secure Firewall ASA interface that has a destination IP address of 0.0.0.0 and a destination MAC address of the Secure Firewall ASA interface. In addition, this message is generated when the Secure Firewall ASA discarded a packet with an invalid source address, which may include one of the following or some other invalid address:

-   Loopback network (127.0.0.0)
-   Broadcast (limited, net-directed, subnet-directed, and all-subnets-directed)
-   The destination host (land.c)

To further enhance spoof packet detection, use the icmp command to configure the Secure Firewall ASA to discard packets with source addresses belonging to the internal network, because the access-list command has been deprecated and is no longer guaranteed to work correctly.

**Recommended Action** Determine if an external user is trying to compromise the protected network. Check for misconfigured clients.

### 106017

**Error Message** `%ASA-2-106017: Deny IP due to Land Attack from _IP_address_ to _IP_address_`

**Explanation** The Secure Firewall ASA received a packet with the IP source address equal to the IP destination, and the destination port equal to the source port. This message indicates a spoofed packet that is designed to attack systems. This attack is referred to as a Land Attack.

**Recommended Action** If this message persists, an attack may be in progress. The packet does not provide enough information to determine where the attack originates.

### 106018

**Error Message** `%ASA-2-106018: ICMP packet type _ICMP_type_ denied by outbound list _acl_ID_ src _inside_address_ dest _outside_address_`

**Explanation** The outgoing ICMP packet with the specified ICMP from local host (inside\_address) to the foreign host (outside\_address) was denied by the outbound ACL list.

**Recommended Action** None required.

### 106020

**Error Message** `%ASA-2-106020: Deny IP teardrop fragment (size = _number_, offset = _number_) from _IP_address_ to _IP_address_`

**Explanation** The Secure Firewall ASA discarded an IP packet with a teardrop signature containing either a small offset or fragment overlapping. This is a hostile event that circumvents the Secure Firewall ASA or an Intrusion Detection System.

**Recommended Action** Contact the remote peer administrator or escalate this issue according to your security policy.

### 106021

**Error Message** `%ASA-1-106021: Deny _protocol_ reverse path check from _source_address_ to _dest_address_ on interface _interface_name_`

**Explanation** An attack is in progress. Someone is attempting to spoof an IP address on an inbound connection. Unicast RPF, also known as reverse route lookup, detected a packet that does not have a source address represented by a route and assumes that it is part of an attack on your Secure Firewall ASA.

This message appears when you have enabled Unicast RPF with the ip verify reverse-path command. This feature works on packets input to an interface; if it is configured on the outside, then the Secure Firewall ASA checks packets arriving from the outside.

The Secure Firewall ASA looks up a route based on the source\_address. If an entry is not found and a route is not defined, then this message appears and the connection is dropped.

If there is a route, the Secure Firewall ASA checks which interface it corresponds to. If the packet arrived on another interface, it is either a spoof or there is an asymmetric routing environment that has more than one path to a destination. The Secure Firewall ASA does not support asymmetric routing.

If the Secure Firewall ASA is configured on an internal interface, it checks static route command statements or RIP, and if the source\_address is not found, then an internal user is spoofing their address.

**Recommended Action** Even though an attack is in progress, if this feature is enabled, no user action is required. The Secure Firewall ASA repels the attack.

### 106022

**Error Message** `%ASA-1-106022: Deny _protocol_ connection spoof from _source_address_ to _dest_address_ on interface _interface_name_`

**Explanation** A packet matching a connection arrived on a different interface from the interface on which the connection began. In addition, the ip verify reverse-path command is not configured.

For example, if a user starts a connection on the inside interface, but the Secure Firewall ASA detects the same connection arriving on a perimeter interface, the Secure Firewall ASA has more than one path to a destination. This is known as asymmetric routing and is not supported on the Secure Firewall ASA.

An attacker also might be attempting to append packets from one connection to another as a way to break into the Secure Firewall ASA. In either case, the Secure Firewall ASA shows this message and drops the connection.

**Recommended Action** Check that the routing is not asymmetric.

### 106023

**Error Message** `%ASA-4-106023: Deny _interface_name_ by access-group "_source_address_" [_source_port_, _idfw_user_]`

**Explanation** A real IP packet was denied by the ACL. This message appears even if you do not have the log option enabled for an ACL. The IP address is the real IP address instead of the values that display through NAT. Both user identity information and FQDN information is provided for the IP addresses if a matched one is found. The Secure Firewall ASA logs either identity information (domain\\user) or FQDN (if the username is not available). If the identity information or FQDN is available, the Secure Firewall ASA logs this information for both the source and destination.

**Recommended Action** If messages persist from the same source address, a footprinting or port scanning attempt might be occurring. Contact the remote host administrator.

### 106024

**Error Message** `%ASA-2-106024: Access rules memory exhausted. Aborting current compilation and continuing to use the existing access rules`

**Explanation** The access list compilation process has run out of memory. All configuration information that has been added since the last successful access list was removed from the Secure Firewall ASA, and the most recently compiled set of access lists will continue to be used.

**Recommended Action** Access lists, AAA, ICMP, SSH, Telnet, and other rule types are stored and compiled as access list rule types. Remove some of these rule types so that others can be added.

### 106025, 106026

**Error Message** `%ASA-6-106025: Failed to determine security context for packet: vlan_source_ _Vlan_ src _source_address_/_source_port_ dest _dest_address_/_dest_port_protocol_`

**Error Message**`%ASA-6-106026: Failed to determine security context for packet: _source_vlan_ src _source_address_/_source_port_ dest _dest_address_/_dest_port_protocol_`

**Explanation** The security context of the packet in multiple context mode cannot be determined. Both messages can be generated for IP packets being dropped in either router and transparent mode.

**Recommended Action** None required.

### 106027

**Error Message** `%ASA-4-106027: Deny _int_type_ src _src_address_:_src_mac_ dst _dst_address_:_dest_mac_ by access-group _"access-list name"_.`

**Explanation** An non IP packet was denied by the ACL. This message is displayed even if you do not have the log option enabled for an extended ACL.

**Recommended Action** If messages persist from the same source address, it might indicate a foot-printing or port-scanning attempt. Contact the remote host administrator.

### 106100

**Error Message** `%ASA-6-106100: access-list _acl_ID_ _protocol_ _interface_name_ _source_address_/_source_port_(_idfw_user_)_sg_info_ -> _interface_name_/_dest_address_(_dest_port_)_idfw_user_ hit-cnt _sg_info_ _number_ [_string_, _number_]`

**Explanation** The initial occurrence or the total number of occurrences during an interval are listed. This message provides more information than message 106023, which only logs denied packets, and does not include the hit count or a configurable level.

When an access-list line has the _log_ argument, it is expected that this message ID might be triggered because of a nonsynchronized packet reaching the Secure Firewall ASA and being evaluated by the access list. For example, if an ACK packet is received on the Secure Firewall ASA (for which no TCP connection exists in the connection table), the Secure Firewall ASA might generate message 106100, indicating that the packet was permitted; however, the packet is later correctly dropped because of no matching connection.

The following list describes the message values:

-   permitted | denied | est-allowed—These values specify if the packet was permitted or denied by the ACL. If the value is est-allowed, the packet was denied by the ACL but was allowed for an already established session (for example, an internal user is allowed to accesss the Internet, and responding packets that would normally be denied by the ACL are accepted).
-   _protocol_ —TCP, UDP, ICMP, or an IP protocol number.
-   _interface\_name_ —The interface name for the source or destination of the logged flow. The VLAN interfaces are supported.
-   _source\_address_ —The source IP address of the logged flow. The IP address is the real IP address instead of the values that display through NAT.
-   _dest\_address_ —The destination IP address of the logged flow. The IP address is the real IP address instead of the values that display through NAT.
-   _source\_port_ —The source port of the logged flow (TCP or UDP). For ICMP, the number after the source port is the message type.
-   _idfw\_user—_ The user identity username, including the domain name that is added to the existing syslog when the Secure Firewall ASA can find the username for the IP address.
-   _sg\_info—_ The security group tag that is added to the syslog when the Secure Firewall ASA can find a security group tag for the IP address. The security group name is displayed with the security group tag, if available.
-   _dest\_port_ —The destination port of the logged flow (TCP or UDP). For ICMP, the number after the destination port is the ICMP message code, which is available for some message types. For type 8, it is always 0. For a list of ICMP message types, see the following URL: [http://www.iana.org/assignments/icmp-parameters/icmp-parameters.xml.](http://www.iana.org/assignments/icmp-parameters/icmp-parameters.xml)
-   hit-cnt _number_ —The number of times this flow was permitted or denied by this ACL entry in the configured time interval. The value is 1 when the Secure Firewall ASA generates the first message for this flow.
-   first hit—The first message generated for this flow.
-   _number_ -second interval—The interval in which the hit count is accumulated. Set this interval using the access-list command with the interval option.
-   hash codes—Two are always printed for the object group ACE and the constituent regular ACE. Values are determined on which ACE that the packet hit. To display these hash codes, enter the show-access list command.

**Recommended Action** None required.

### 106101

**Error Message** `%ASA-1-106101: Number of cached deny-flows for ACL log has reached limit (_number_)`

**Explanation** If you configured the log option for an ACL deny statement (access-list id deny command), and a traffic flow matches the ACL statement, the Secure Firewall ASA caches the flow information. This message indicates that the number of matching flows that are cached on the Secure Firewall ASA exceeds the user-configured limit (using the access-list deny-flow-max command). This message might be generated as a result of a DoS attack.

-   _number—_ The limit configured using the access-list deny-flow-max command

**Recommended Action** None required.

### 106102

**Error Message** `%ASA-[1-7]-106102: access-list _acl_ID_ _permitted_ _source_address_ for user '_user_name_'_source_address_/_source_port_(_interface_name_) -> _dest_address_/_dest_port_(_interface_name_) hit-cnt _sg_info_ _number_ [_string_, _number_]`

**Explanation** A packet was either permitted or denied by an access-list that was applied through a VPN filter. This message is the VPN/AAA filter equivalent of message 106100.

**Recommended Action** None required.

### 106103

**Error Message** `%ASA-4-106103: access-list _acl_ID_ _denied_ _protocol_ for user '_username_' _source_address_/_source_port_interface_name_(_interface_name_) -> _dest_address_/_dest_port_(_interface_name_) hit-cnt _sg_info_ _number_ [_string_, _number_]`

**Explanation** A packet was denied by an access-list that was applied through a VPN filter. This message is the VPN/AAA filter equivalent of message106023.

**Recommended Action** None required.

### 107001

**Error Message** `%ASA-1-107001: RIP auth failed from _IP_address_: version=_number_, type=_string_, mode=_string_, sequence=_number_ on interface _interface_name_`

**Explanation** The Secure Firewall ASA received a RIP reply message with bad authentication. This message might be caused by a misconfiguration on the router or the Secure Firewall ASA or by an unsuccessful attempt to attack the routing table of the Secure Firewall ASA.

**Recommended Action** This message indicates a possible attack and should be monitored. If you are not familiar with the source IP address listed in this message, change your RIP authentication keys between trusted entities. An attacker might be trying to determine the existing keys.

### 107002

**Error Message** `%ASA-1-107002: RIP pkt failed from _IP_address_: version=_number_ on interface _interface_name_`

**Explanation** A router bug, a packet with non-RFC values inside, or a malformed entry may have caused this message to appear. This should not happen, and may be an attempt to exploit the routing table of the ASA.

**Recommended Action** This message indicates a possible attack and should be monitored. The packet has passed authentication, if enabled, and bad data is in the packet. Monitor the situation and change the keys if there are any doubts about the originator of the packet.

### 108002

**Error Message** `%ASA-2-108002: SMTP replaced _string_: out _source_address_ in _inside_address_ data: _string_`

**Explanation** A Mail Guard (SMTP) message has been generated by the inspect esmtp command. The ASA has replaced an invalid character in an e-mail address with a space.

**Recommended Action** None required.

### 108003

**Error Message** `%ASA-2-108003: Terminating ESMTP connection; malicious pattern detected in the mail address from _source_interface_:_source_address_/_source_port_ to _dest_interface_:_dest_address_/_dset_port_. Mail Address:_string_`

**Explanation** The ASA has detected a malicious pattern in an e-mail address and drops the connection. An attack is in progress.

**Recommended Action** None required.

### 108004

**Error Message** `%ASA-4-108004: _action_class:action_ ESMTP _req_resp_ from _src_ifc_:_sip_/_sport_ to _dest_ifc_:_dip_/_dport_; _further_info_`

**Explanation** An ESMTP classification is performed on an ESMTP message, and the specified criteria are satisfied. The configured action is taken.

-   action\_class—The class of action: ESMTP Classification for ESMTP match commands; ESMTP Parameter for parameter commands
-   action—Action taken: Dropped, Dropped connection for, Reset connection for, or Masked header flags for
-   req\_resp—Request or Response
-   src\_ifc—Source interface name
-   sip|sport—Source IP address or source port
-   dest\_ifc—Destination interface name
-   dip|dport—Destination IP address or destination port
-   further info—One of the following:

For a single match command: matched Class _id_ : _match\_command_ (for example, matched Class 1234: match body length 100).

For parameter commands: _parameter-command_ : _descriptive-message_ (for example, mail-relay: No Mail Relay allowed)

**Recommended Action** None required.

### 108005

**Error Message** `%ASA-6-108005: _action_class:Received_ ESMTP _req_resp_ from _src_ifc_:_sip_/_sport_ to _dest_ifc_:_dip_/_dport_; _further_info_`

**Explanation** An ESMTP classification is performed on an ESMTP message, and the specified criteria are satisfied. The standalone log action is taken.

-   action\_class—The class of action: ESMTP Classification for ESMTP match commands; ESMTP Parameter for parameter commands
-   req\_resp—Request or Response
-   src\_ifc—Source interface name
-   sip|sport—Source IP address or source port
-   dest\_ifc—Destination interface name
-   dip|dport—Destination IP address or destination port
-   further info—One of the following:

For a single match command: matched Class _id_ : _match\_command_ (for example, matched Class 1234: match body length 100)

For parameter commands (commands under the parameter section): _parameter-command_ : _descriptive-message_ (for example, mail-relay: No Mail Relay allowed)

**Recommended Action** None required.

### 108006

**Error Message** `%ASA-7-108006: Detected ESMTP size violation from _src_ifc_:_sip_/_sport_ to _dest_ifc_:_dip_/_dport_; declared size is: _decl_size_, actual size is _act_size_`

**Explanation** This event is generated when an ESMTP message size exceeds the size declared in the RCPT command.

-   src\_ifc—Source interface name
-   sip|sport—Source IP address or source port
-   dest\_ifc—Destination interface name
-   dip|dport—Destination IP address or destination port
-   decl\_size—Declared size
-   act\_size—Actual size

**Recommended Action** None required.

### 108007

**Error Message** `%ASA-6-108007: TLS started on ESMTP session between client _client-side_interface-name_:_client_IP_address_/_client_port_ and server _server-side_interface-name_:_server_IP_address_/_server_port_`

**Explanation** On an ESMTP connection, the server has responded with a 220 reply code to the client STARTTLS command. The ESMTP inspection engine no longer inspects the traffic on this connection.

-   _client-side interface-name_ —The name for the interface that faces the client side
-   _client IP address_ —The IP address of the client
-   _client port_ —The TCP port number for the client
-   _server-side interface-name_ —The name for the interface that faces the server side
-   _server IP address_ —The IP address of the server
-   _server port_ —The TCP port number for the server

**Recommended Action** Log and review the message. Check whether the ESMTP policy map associated with this connection has the allow-tls action log setting. If not, contact the Cisco TAC.

### 109001

**Error Message** `%ASA-6-109001: Auth start for user '_user_' from _inside_address_/_inside_port_ to _outside_address_/_outside_port_`

**Explanation** The ASA is configured for AAA and detects an authentication request by the specified user.

**Recommended Action** None required.

### 109002

**Error Message** `%ASA-6-109002: Auth from _inside_address_/_inside_port_ to _outside_address_/_outside_port_ failed (server _IP_address_ failed) on interface _interface_name_`

**Explanation** An authentication request failed because the specified authentication server cannot be contacted by the module.

**Recommended Action** Check that the authentication daemon is running on the specified authentication server.

### 109003

**Error Message** `%ASA-6-109003: Auth from _inside_address_/_inside_port_ to _outside_address_/_outside_port_ failed (all servers failed) on interface _interface_name_`

**Explanation** No authentication server can be found.

**Recommended Action** Ping the authentication servers from the ASA. Make sure that the daemons are running.

### 109005

**Error Message** `%ASA-6-109005: Authentication succeeded for user '_user_' from _inside_address_/_inside_port_ to _outside_address_/_outside_port_ on interface _interface_name_`

**Explanation** The specified authentication request succeeded.

**Recommended Action** None required.

### 109006

**Error Message** `%ASA-6-109006: Authentication failed for user '_user_' from _inside_address_/_inside_port_ to _outside_address_/_outside_port_ on interface _interface_name_`

**Explanation** The specified authentication request failed, possibly because of an incorrect password. The username is hidden when invalid or unknown, but appears when valid or the no logging hide username command has been configured.

**Recommended Action** None required.

### 109007

**Error Message** `%ASA-6-109007: Authorization permitted for user '_user_' from _inside_address_/_inside_port_ to _outside_address_/_outside_port_ on interface _interface_name_`

**Explanation** The specified authorization request succeeded.

**Recommended Action** None required.

### 109008

**Error Message** `%ASA-6-109008: Authorization denied for user '_user_' from _outside_address_/_outside_port_ to _inside_address_/_inside_port_ on interface _interface_name_`

**Explanation** A user is not authorized to access the specified address, possibly because of an incorrect password.

**Recommended Action** None required.

### 109010

**Error Message** `%ASA-3-109010: Auth from _inside_address_/_inside_port_ to _outside_address_/_outside_port_ failed (too many pending auths) on interface _interface_name_`

**Explanation** An authentication request cannot be processed because the server has too many requests pending.

**Recommended Action** Check to see if the authentication server is too slow to respond to authentication requests. Enable the Flood Defender feature with the floodguard enable command.

### 109011

**Error Message** `%ASA-2-109011: Authen Session Start: user '_user_', sid _number_`

**Explanation** An authentication session started between the host and the Secure Firewall ASA and has not yet completed.

**Recommended Action** None required.

### 109012

**Error Message** `%ASA-5-109012: Authen Session End: user '_user_', sid _number_, elapsed _number_ seconds`

**Explanation** The authentication cache has timed out. Users must reauthenticate on their next connection. You can change the duration of this timer with the timeout uauth command.

**Recommended Action** None required.

### 109013

**Error Message** `%ASA-3-109013: User must authenticate before using this service`

**Explanation** The user must be authenticated before using the service.

**Recommended Action** Authenticate using FTP, Telnet, or HTTP before using the service.

### 109014

**Error Message** `%ASA-7-109014: A non-telnet connection was denied to the configured Virtual Telnet IP Address`

**Explanation** A request to authenticate did not have a corresponding request for authorization.

**Recommended Action** Ensure that both the aaa authentication and aaa authorization command statements are included in the configuration.

### 109016

**Error Message** `%ASA-3-109016: Cannot find authorization ACL '_acl_id_' on '_server_name_' for user '_user_'`

**Explanation** The specified on the AAA server for this user does not exist on the Secure Firewall ASA. This error can occur if you configure the AAA server before you configure the Secure Firewall ASA. The Vendor-Specific Attribute (VSA) on your AAA server might be one of the following values:

-   acl=acl\_ID
-   shell:acl=acl\_ID
-   ACS:CiscoSecured-Defined-ACL=acl\_ID

**Recommended Action** Add the ACL to the Secure Firewall ASA, making sure to use the same name specified on the AAA server.

### 109017

**Error Message** `%ASA-4-109017: User at _IP_address_ exceeded auth proxy connection limit (max _limit_)`

**Explanation** A user has exceeded the user authentication proxy limit, and has opened too many connections to the proxy.

**Recommended Action** Increase the proxy limit by entering the proxy-limit _proxy\_limit_ command, or ask the user to close unused connections. If the error persists, it may indicate a possible DoS attack.

### 109018

**Error Message** `%ASA-3-109018: Downloaded ACL '_acl_ID_' is empty`

**Explanation** The downloaded authorization has no ACEs. This situation might be caused by misspelling the attribute string _ip:inacl#_ or omitting the access-list command.

```cpp
junk:junk# 1=permit tcp any any eq junk ip:inacl#1=”
```

**Recommended Action** Correct the ACL components that have the indicated error on the AAA server.

### 109019

**Error Message** `%ASA-3-109019: Downloaded ACL '_acl_ID_' has parsing error; ACE: '_string_'; _string_`

**Explanation** An error occurred during parsing the sequence number NNN in the attribute string ip:inacl#NNN= of a downloaded authorization. The reasons include: - missing = - contains nonnumeric, nonpace characters between # and = - NNN is greater than 999999999.

```cpp
ip:inacl# 1 permit tcp any any
ip:inacl# 1junk2=permit tcp any any
ip:inacl# 1000000000=permit tcp any any
```

**Recommended Action** Correct the ACL element that has the indicated error on the AAA server.

### 109020

**Error Message** `%ASA-3-109020: Downloaded ACL has config error; ACE`

**Explanation** One of the components of the downloaded authorization has a configuration error. The entire text of the element is included in the message. This message is usually caused by an invalid access-list command statement.

**Recommended Action** Correct the ACL component that has the indicated error on the AAA server.

### 109021

**Error Message** `%ASA-7-109021: Uauth null proxy error (uap _number_)`

**Explanation** An internal user authentication error has occurred.

**Recommended Action** None required. However, if this error appears repeatedly, contact the Cisco TAC.

### 109022

**Error Message** `%ASA-4-109022: HTTPS proxy resource limit reached.`

**Explanation**For each HTTPS authentication, the ASA dedicates a process to service the authentication request. When the number of concurrently running processes exceeds the system-imposed limit, the ASA does not perform the authentication, and this message appears.

**Recommended Action** None required.

### 109023

**Error Message** `%ASA-3-109023: User from _source_address_/_source_port_ to _dest_address_/_dest_port_ on interface _outside_interface_ using _service_name_ must authenticate before using this service`

**Explanation** Based on the configured policies, you need to be authenticated before you can use this service port.

**Recommended Action** Authenticate using Telnet, FTP, or HTTP before attempting to use this service port.

### 109024

**Error Message** `%ASA-6-109024: Authorization denied from _source_address_/_source_port_ to _dest_address_/_dest_port_ (not authenticated) on interface _interface_name_ using _protocol_ to`

**Explanation** The ASA is configured for AAA and a user attempted to make a TCP connection across the ASA without prior authentication.

**Recommended Action** None required.

### 109025

**Error Message** `%ASA-6-109025: Authorization denied (acl=_acl_ID_) for user '_user_' from _source_address_/_source_port_ to _dest_address_/_dest_port_ on interface _interface_name_ using _protocol_`

**Explanation**The check failed. The check either matched a deny or did not match anything, such as an implicit deny. The connection was denied by the user acl\_ID, which was defined according to the AAA authorization policy on the Cisco Secure Access Control Server (ACS).

**Recommended Action** None required.

### 109026

**Error Message** `%ASA-3-109026: [ _aaa_protocol_ ] Invalid reply digest received; shared server key may be mismatched.`

**Explanation** The response from the AAA server cannot be validated. The configured server key is probably incorrect. This message may be generated during transactions with RADIUS or TACACS+ servers.

Verify that the server key, configured using the aaa-server command, is correct.

### 109027

**Error Message** `%ASA-4-109027: [ _aaa_protocol_ ] Unable to decipher response message Server = _server_IP_address_, User = _user_`

**Explanation** The response from the AAA server cannot be validated. The configured server key is probably incorrect. This message may be displayed during transactions with RADIUS or TACACS+ servers. The server\_IP\_address is the IP address of the relevant AAA server. The user is the user name associated with the connection.

**Recommended Action** Verify that the server key, configured using the aaa-server command, is correct.

### 109028

**Error Message** `%ASA-4-109028: aaa bypassed for same-security traffic from _ingress_interface_:_source_address_/_source_port_ to _egress_interface_:_dest_address_/_dest_port_`

**Explanation**AAA is being bypassed for same security traffic that matches a configured AAA rule. This can only occur when traffic passes between two interfaces that have the same configured security level, when the same security traffic is permitted, and if the AAA configuration uses the include or exclude syntax.

**Recommended Action** None required.

### 109029

**Error Message** `%ASA-5-109029: Parsing downloaded ACL: _string_`

**Explanation** A syntax error occurred while parsing an access list that was downloaded from a RADIUS server during user authentication.

-   _string_ —An error message detailing the syntax error that prevented the access list from parsing correctly

**Recommended Action** Use the information presented in this message to identify and correct the syntax error in the access list definition within the RADIUS server configuration.

### 109030

**Error Message** `%ASA-4-109030: Autodetect ACL convert wildcard did not convert ACL _access_list_source_ _dest_ netmask _netmask_`

**Explanation**A dynamic ACL that is configured on a RADIUS server is not converted by the mechanism for automatically detecting wildcard netmasks. The problem occurs because this mechanism cannot determine if the netmask is a wildcard or a normal netmask.

-   access\_list—The access list that cannot be converted
-   source—The source IP address
-   dest—The destination IP address
-   netmask—The subnet mask for the destination or source address in dotted-decimal notation

**Recommended Action** Check the access list netmask on the RADIUS server for the wildcard configuration. If the netmask is supposed to be a wildcard, and if all access list netmasks on that server are wildcards, then use the wildcard setting for acl-netmask-convert for the AAA server. Otherwise, change the netmask to a normal netmask or to a wildcard netmask that does not contain holes (that is, where the netmask presents consecutive binary 1s. For example, 00000000.00000000.00011111.11111111 or hex 0.0.31.255). If the mask is supposed to be normal and all access list netmasks on that server are normal, then use the normal setting for acl-netmask-convert for the AAA server.

### 109031

**Error Message** `%ASA-4-109031: NT Domain Authentication Failed: rejecting guest login for _username_ .`

**Explanation** A user has tried to authenticate to an NT domain that was configured for guest account access and the username is not a valid username on the NT server. The connection is denied.

**Recommended Action** If the user is a valid user, add an account to the NT server. If the user is not allowed access, no action is required.

### 109032

**Error Message** `%ASA-3-109032: Unable to install ACL '_access_list_', downloaded for user _username_; Error in ACE: '_ace_'`

**Explanation** The Secure Firewall ASA received an access control list from a RADIUS server to apply to a user connection, but an entry in the list contains a syntax error. Th euse of a list containing an error could result in the violation of a security policy, so the Secure Firewall ASA failed to authenticate the user.

-   _access\_list_ —The name assigned to the dynamic access list as it would appear in the output of the show access-list command
-   _username_ —The name of the user whose connection will be subject to this access list
-   _ace_ —The access list entry that was being processed when the error was detected

**Recommended Action** Correct the access list definition in the RADIUS server configuration.

### 109033

**Error Message** `%ASA-4-109033: Authentication failed for admin user _user_ from _src_IP_. Interactive challenge processing is not supported for _protocol_`

**Explanation** AAA challenge processing was triggered during authentication of an administrative connection, but the Secure Firewall ASA cannot initiate interactive challenge processing with the client application. When this occurs, the authentication attempt will be rejected and the connection denied.

-   _user_ —The name of the user being authenticated
-   _src\_IP_ —The IP address of the client host
-   _protocol_ —The client connection protocol (SSH v1 or administrative HTTP)

**Recommended Action** Reconfigure AAA so that challenge processing does not occur for these connection types. This generally means to avoid authenticating these connection types to RSA SecurID servers or to any token-based AAA server via RADIUS.

### 109034

**Error Message** `%ASA-4-109034: Authentication failed for network user _user_ from _src_IP_/_port_ to _dst_IP_/_port_. Interactive challenge processing is not supported for _protocol_ connections`

**Explanation** AAA challenge processing was triggered during authentication of a network connection, but the Secure Firewall ASA cannot initiate interactive challenge processing with the client application. When this occurs, the authentication attempt will be rejected and the connection denied.

-   _user_ —The name of the user being authenticated
-   _src\_IP/port_ —The IP address and port of the client host
-   _dst\_IP/port_ —The IP address and port of the server to which the client is attempting to connect
-   _protocol_ —The client connection protocol (for example, FTP)

**Recommended Action** Reconfigure AAA so that challenge processing does not occur for these connection types. This generally means to avoid authenticating these connection types to RSA SecurID servers or to any token-based AAA server via RADIUS.

### 109035

**Error Message** `%ASA-3-109035: Exceeded maximum number (999) of DAP attribute instances for user = _user_`

**Explanation** This log is generated when the number of DAP attributes received from the RADIUS server exceeds the maximum number allowed when authenticating a connection for the specified user.

**Recommended Action** Modify the DAP attribute configuration to reduce the number of DAP attributes below the maximum number allowed as specified in the log so that the specified user can connect.

### 109036

**Error Message** `%ASA-6-109036: Exceeded _1000_ attribute values for the _attribute_name_ attribute for user _username_`

**Explanation** The LDAP response message contains an attribute that has more than 1000 values.

-   _attribute\_name_ —The LDAP attribute name
-   _username_ —The username at login

**Recommended Action** None required.

### 109037

**Error Message** `%ASA-3-109037: Exceeded _5000_ attribute values for the _attribute_name_ attribute for user _username_`

**Explanation** The Secure Firewall ASA supports multiple values of the same attribute received from a AAA server. If the AAA server sends a response containing more than 5000 values for the same attribute, then the Secure Firewall ASA treats this response message as being malformed and rejects the authentication. This condition has only been seen in lab environments using specialized test tools. It is unlikely that the condition would occur in a real-world production network.

-   _attribute\_name_ —The LDAP attribute name
-   _username_ —The username at login

**Recommended Action** Capture the authentication traffic between the Secure Firewall ASA and AAA server using a protocol sniffer (such as WireShark), then forward the trace file to the Cisco TAC for analysis.

### 109038

**Error Message** `%ASA-3-109038: Attribute _internal-attribute-name_ value "_string-from-server_" from AAA server could not be parsed as a _type_`

**Explanation** The AAA subsystem tried to parse an attribute from the AAA server into an internal representation and failed.

-   _string-from-server—_ String received from the AAA server, truncated to 40 characters.
-   _type_ —The type of the specified attribute

**Recommended Action** Verify that the attribute is being generated correctly on the AAA server. For additional information, use the debug ldap and debug radius commands.

### 109039

**Error Message** `%ASA-5-109039: AAA Authentication: Dropping an unsupported IPv6/IP46/IP64 packet from _lifc_:_laddr_ to _fifc_:_faddr_`

**Explanation** A packet containing IPv6 addresses or IPv4 addresses translated to IPv6 addresses by NAT requires AAA authentication or authorization. AAA authentication and authorization do not support IPv6 addresses. The packet is dropped.

-   _lifc_ —The ingress interface
-   _laddr_ —The source IP address
-   _fifc_ —The egress interface
-   _faddr_ —The destination IP address after NAT translation, if any

**Recommended Action** None required.

### 109040

**Error Message** `%ASA-4-109040: User at _IP_ exceeded auth proxy rate limit of 10 connections/sec`

**Explanation** A connection attempt has been rejected because the ASA has detected a high frequency of HTTPS authentication requests from the same host.

-   _IP_ —The IP address of the host from which the connection was initiated

**Recommended Action** Limit the number of cut-through proxy authentication attempts from users.

### 109100

**Error Message** `%ASA-6-109100: Received CoA update from _coa-source-ip_ for user "_username_", with session ID _audit-session-id_, changing authorization attributes.`

**Explanation** The Secure Firewall ASA has successfully processed the CoA policy update request from _coa-source-ip_ for user _username_ with session id _audit-session-id_ . This syslog message is generated after a change of authorization policy update has been received by the Secure Firewall ASA, validated and applied. In a non-error case, this is the only syslog message that is generated when a change of authorization is received and processed.

-   _coa-source-ip_ —Originating IP address of the change of authorization request
-   _username_ —User whose session is being changed
-   _audit-session-id_ —The global ID of the session being modified

**Recommended Action** None required.

### 109101

**Error Message** `%ASA-6-109101: Received CoA disconnect request from _coa-source-ip_ for user "_username_", with session ID: _audit-session-id_.`

**Explanation** The Secure Firewall ASA has received a correctly formatted Disconnect-Request for an active VPN session and has successfully terminated the connection.

-   _coa-source-ip_ —Originating IP address of the change of authorization request
-   _username_ —User whose session is being changed
-   _audit-session-id_ —The global ID of the session being modified

**Recommended Action** None required.

### 109102

**Error Message** `%ASA-4-109102: Received CoA _action-type_ from _coa-source-ip_, but cannot find named session _audit-session-id_.`

**Explanation** The Secure Firewall ASA has received a valid change of authorization request, but the session ID specified in the request does not match any active sessions on the Secure Firewall ASA. This could be the result of the change of authorization server attempting to issue a change of authorization on a session that has already been closed by the user.

-   _action-type_ —The requested change of authorization action (update or disconnect)
-   _coa-source-ip_ —Originating IP address of the change of authorization request
-   _audit-session-id_ —The global ID of the session being modified

**Recommended Action** None required.

### 109103

**Error Message** `%ASA-3-109103: CoA _action-type_ from _coa-source-ip_ failed for user "_username_", with session ID: _audit-session-id_.`

**Explanation** The Secure Firewall ASA has received a correctly formatted change of authorization request, but was unable to process it successfully.

-   _action-type_ —The requested change of authorization action (update or disconnect)
-   _coa-source-ip_ —Originating IP address of the change of authorization request
-   _username_ —User whose session is being changed
-   _audit-session-id_ —The global ID of the session being modified

**Recommended Action** Investigate the relevant VPN subsystem logs to determine why the updated attributes could not be applied or why the session could not be terminated.

### 109104

**Error Message** `%ASA-3-109104: CoA (Action type: _action-type_) from _coa-source-ip_ failed for user "_username_", with session ID: _audit-session-id_. Action not supported.`

**Explanation** The Secure Firewall ASA has received a correctly formatted change of authorization request, but did not process it because the indicated action is not supported by the Secure Firewall ASA.

-   _action-type_ —The requested change of authorization action (update or disconnect)
-   _coa-source-ip_ —Originating IP address of the change of authorization request
-   _username_ —User whose session is being changed
-   _audit-session-id_ —The global ID of the session being modified

**Recommended Action** None required.

### 109105

**Error Message** `%ASA-3-109105: Failed to determine the egress interface for locally generated traffic destined to _protocol_ _IP_:_port_.`

**Explanation** It is necessary for Secure Firewall ASA to log a syslog if no routes are present when the interface is BVI. Apparently, if default route is present and it does not route packet to the correct interface then it becomes impossible to track it.

**Recommended Action** It is highly recommended to add default route for correct destination or add static routes.

### 109201

**Error Message** `%ASA-5-109201: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP_Address_, Succeeded adding entry.`

**Explanation** When a VPN user is sucessfully added, this message is generated.

**Recommended Action** None.

### 109202

**Error Message** `%ASA-6-109202: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP_Address_, Succeeded incrementing entry use`

**Explanation** The VPN user account already exists and successfully incremented the reference count.

**Recommended Action** None.

### 109203

**Error Message** `%ASA-3-109203: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP_Address_, Failed adding entry.`

**Explanation** This message is generated when the device failed to apply ACL rules for newly created user entry.

**Recommended Action** Try to reconnect.

### 109204

**Error Message** `%ASA-5-109204: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP_Address_, Succeeded applying filter.`

**Explanation** This message is generated when the device failed to apply ACL rules for newly created user entry.

**Recommended Action** None.

### 109205

**Error Message** `%ASA-3-109205: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP_Address_, Failed applying filter.`

**Explanation** This message is generated when the user entry already exists and failed to apply new rules to session on interface.

**Recommended Action** Try to reconnect.

### 109206

**Error Message** `%ASA-3-109206: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP_Address_, Removing stale entry added _hours_ ago.`

**Explanation** This message is generated when the device failed to add user entry due to collision and has removed stale entry.

**Recommended Action** Try to reconnect.

### 109207

**Error Message** `%ASA-5-109207: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP_Address_, Succeeded updating entry.`

**Explanation** This message is generated when the device has successfully applied rules for user on interface.

**Recommended Action** None.

### 109208

**Error Message** `%ASA-3-109208: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP_Address_, Failed updating entry - no entry.`

**Explanation** This message is generated when the device has failed to update user entry with new rules.

**Recommended Action** Try to reconnect again.

### 109209

**Error Message** `%ASA-3-109209: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP_Address_, Failed updating filter for entry. Entry was allocated to Session=_session_, User=_username_ _hours_ ago.`

**Explanation** This message is generated when the device has failed to update the rules in user entry due to collision.

**Recommended Action** Try to reconnect again.

### 109210

**Error Message** `%ASA-5-109210: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP_Address_, Succeeded removing entry.`

**Explanation** This message is generated when the device has successfully removed the rules for user during tunnel torn down.

**Recommended Action** None.

### 109211

**Error Message** `%ASA-6-109211: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP_Address_, Succeeded decrementing entry use.`

**Explanation** This message is generated when the reference count decremented successfully after tunnel removal.

**Recommended Action** None.

### 109212

**Error Message** `%ASA-3-109212: UAUTH: Session=_session_, User=_user_name_, Assigned IP=_ip_address_, Failed removing entry - _reason_string_.`

**Explanation** This message is generated when the device fails to delete due to invalid address, missing entry, or bad entry.

**Recommended Action** Try to disconnect again.

### 109213

**Error Message** `%ASA-3-109213: UAUTH: Session=_session_, User=_username_, Assigned IP=_IP_Address_, Failed removing entry. Address was allocated to Session=_session_, User=_username_ _hours_ ago.`

**Explanation** This message is generated when the device fails to delete due to collision in user entry.

**Recommended Action** Try to disconnect again.

## Messages 110002 to 113045

This section includes messages from 110002 to 113045.

### 110002

**Error Message** `%ASA-6-110002: Failed to locate egress interface for _protocol_ from _src_interface_:_src_ip_/_src_port_ to _dest_ip_/_dest_port_`

**Explanation** An error occurred when the Secure Firewall ASA tried to find the interface through which to send the packet.

-   _protocol_ —The protocol of the packet
-   _src\_interface_ —The interface from which the packet was received
-   _src\_ip_ —The source IP address of the packet
-   _src\_port_ —The source port number
-   _dest\_ip_ —The destination IP address of the packet
-   _dest\_port_ —The destination port number

**Recommended Action** Copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC.

### 110003

**Error Message** `%ASA-6-110003: Routing failed to locate next hop for _protocol_ from _src_interface_:_src_ip_/_src_port_ to _dest_interface_:_dest_ip_/_dest_port_`

**Explanation** An error occurred when the Secure Firewall ASA tried to find the next hop on an interface routing table.

-   _protocol_ —The protocol of the packet
-   _src\_interface_ —The interface from which the packet was received
-   _src\_ip_ —The source IP address of the packet
-   _src\_port_ —The source port number
-   _dest\_ip_ —The destination IP address of the packet
-   _dest\_port_ —The destination port number

**Recommended Action** Copy the error message, the configuration, and any details about the events leading up to the error, and contact Cisco TAC. During debugging, use the show asp table routing command to view the routing table details.

### 110004

**Error Message** `%ASA-6-110004: Egress interface changed from _old_active_ifc_ to _new_active_ifc_ on _ip_protocol_ connection _conn_id_ for _outside_zone_/_parent_outside_ifc_:_outside_addr_/_outside_port_ (_mapped_addr_/_mapped_port_) to _inside_zone_/_parent_inside_ifc_:_inside_addr_/_inside_port_ (_mapped_addr_/_mapped_port_)`

**Explanation** A flow changed on the egress interface.

**Recommended Action** None required.

### 110005

**Error Message** `%ASA-6-110005: Routing failed to locate next hop for protocol from _interface_:_address_/_port_ to _interface_:_address_/_port_`

**Explanation** A flow not found during output route lookup.

**Recommended Action** None.

### 111001

**Error Message** `%ASA-5-111001: Begin configuration: _IP_address_ writing to _device_`

**Explanation** You have entered the write command to store your configuration on a device (either floppy, flash memory, TFTP, the failover standby unit, or the console terminal). The IP\_address indicates whether the login was made at the console port or with a Telnet connection.

**Recommended Action** None required.

### 111002

**Error Message** `%ASA-5-111002: Begin configuration: _ip_address_ reading from _device_`

**Explanation** You have entered the read command to read your configuration from a device (either floppy disk, flash memory, TFTP, the failover standby unit, or the console terminal). The ip\_address indicates whether the login was made at the console port or with a Telnet connection.

**Recommended Action** None required.

### 111003

**Error Message** `%ASA-5-111003: _IP_address_ Erase configuration.`

**Explanation** You have erased the contents of flash memory by entering the write erase command at the console. The IP\_address value indicates whether the login was made at the console port or through a Telnet connection.

**Recommended Action** After erasing the configuration, reconfigure the Secure Firewall ASA and save the new configuration. Alternatively, you can restore information from a configuration that was previously saved, either on a floppy disk or on a TFTP server elsewhere on the network.

### 111004

**Error Message** `%ASA-5-111004: _IP_address_ end configuration: _{FAILED|OK}_`

**Explanation** You have entered the config floppy/memory/ network command or the write floppy/memory/network/standby command. The IP\_address value indicates whether the login was made at the console port or through a Telnet connection.

**Recommended Action** None required if the message ends with OK. If the message indicates a failure, try to fix the problem. For example, if writing to a floppy disk, ensure that the floppy disk is not write protected; if writing to a TFTP server, ensure that the server is up.

### 111005

**Error Message** `%ASA-5-111005: _IP_address_ end configuration: OK`

**Explanation** You have exited the configuration mode. The IP\_address value indicates whether the login was made at the console port or through a Telnet connection.

**Recommended Action** None required.

### 111007

**Error Message** `%ASA-5-111007: Begin configuration: _IP_address_ reading from _device_`

**Explanation** You have entered the reload or configure command to read in a configuration. The device text can be floppy, memory, net, standby, or terminal. The IP\_address value indicates whether the login was made at the console port or through a Telnet connection.

**Recommended Action** None required.

### 111008

**Error Message** `%ASA-5-111008: User '_user_' executed the '_string_' command.`

**Explanation** The user entered any command, with the exception of a show command.

**Recommended Action** None required.

| ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)

**Note** | ___

There is an exception for this syslog ID. Syslogs will be seen in logging <destination> even though global syslog is disabled.

___ |
|--------|------------------------------------------------------------------------------------------------------------------------------------|

### 111009

**Error Message** `%ASA-7-111009: User '_user_' executed cmd: _string_`

**Explanation** The user entered a command that does not modify the configuration. This message appears only for show commands.

**Recommended Action** None required.

### 111010

**Error Message** `%ASA-5-111010: User '_username_', running '_application-name_' from IP _ip_addr_, executed '_cmd_'`

**Explanation** A user made a configuration change.

-   _username_ —The user making the configuration change
-   _application-name_ —The application that the user is running
-   _ip addr_ —The IP address of the management station
-   _cmd_ —The command that the user has executed

**Recommended Action** None required.

| ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)

**Note** | ___

There is an exception for this syslog ID. Syslogs will be seen in logging <destination> even though global syslog is disabled.

___ |
|--------|------------------------------------------------------------------------------------------------------------------------------------|

### 111111

**Error Message** `%ASA-1-111111: _error_message_`

**Explanation** A system or infrastructure error has occurred.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 112001

**Error Message** `%ASA-2-112001: Clear finished`

**Explanation** A request to clear the module configuration was completed. The source file and line number are identified.

**Recommended Action** None required.

### 113001

**Error Message** `%ASA-3-113001: Unable to open AAA session. Session limit [_limit_] reached`

**Explanation** The AAA operation on an IPsec tunnel or WebVPN connection cannot be performed because of the unavailability of AAA resources. The limit value indicates the maximum number of concurrent AAA transactions.

**Recommended Action** Reduce the demand for AAA resources, if possible.

### 113003

**Error Message** `%ASA-6-113003: AAA group policy for user _user_ is being set to _policy_name_`

**Explanation** The group policy that is associated with the tunnel group is being overridden with a user-specific policy, _policy\_name_ . The _policy\_name_ is specified using the username command when LOCAL authentication is configured or is returned in the RADIUS CLASS attribute when RADIUS authentication is configured.

**Recommended Action** None required.

### 113004

**Error Message** `%ASA-6-113004: AAA user _aaa_type_ Successful : server = _server_IP_address_ : user = _user_`

**Explanation** The AAA operation on an IPsec or WebVPN connection has been completed successfully. The AAA types are authentication, authorization, or accounting. The server\_IP\_address is the IP address of the relevant AAA server. The user is the user name associated with the connection.

**Recommended Action** None required.

### 113005

**Error Message-1** `%ASA-6-113005: AAA user authentication Rejected : reason = _reason_ : server = _ip_address_ : user =_user_name_ : user IP = _ip_address_`

**Explanation** The AAA authentication on a connection has failed. The username is hidden when invalid or unknown, but appears when valid or the no logging hide username command has been configured.

**Recommended Action** Retry the authentication.

**Error Message-2** `%ASA-6-113005: AAA user authorization Rejected : reason = _reason_ : server = _ip_address_ : user =_user_name_ : user IP = _ip_address_`

**Explanation** The AAA authorization on a connection has failed. The username is hidden when invalid or unknown, but appears when valid or the no logging hide username command has been configured.

**Recommended Action** Retry the authorization.

### 113006

**Error Message** `%ASA-6-113006: User '_user_' locked out on exceeding '_number_' successive failed authentication attempts`

**Explanation** A locally configured user is being locked out. This happens when a configured number of consecutive authentication failures have occurred for this user and indicates that all future authentication attempts by this user will be rejected until an administrator unlocks the user using the clear aaa local user lockout command. The user is the user that is now locked, and the number is the consecutive failure threshold configured using the aaa local authentication attempts max-fail command.

**Recommended Action** Try unlocking the user using the clear\_aaa\_local\_user\_lockout command or adjusting the maximum number of consecutive authentication failures that are tolerated.

### 113007

**Error Message** `%ASA-6-113007: User '_user_' unlocked by '_administrator_'`

**Explanation** A locally configured user that was locked out after exceeding the maximum number of consecutive authentication failures set by using the aaa local authentication attempts max-fail command has been unlocked by the indicated administrator.

**Recommended Action** None required.

### 113008

**Error Message** `%ASA-6-113008: AAA transaction status _ACCEPT_ : user = _user_`

**Explanation** The AAA transaction for a user associated with an IPsec or WebVPN connection was completed successfully. The user is the username associated with the connection.

**Recommended Action** None required.

### 113009

**Error Message** `%ASA-6-113009: AAA retrieved default group policy (_policy_) for user = _username_`

**Explanation** The authentication or authorization of an IPsec or WebVPN connection has occurred. The attributes of the group policy that were specified with the tunnel-group or webvpn commands have been retrieved.

**Recommended Action** None required.

### 113010

**Error Message** `%ASA-6-113010: AAA challenge received for user _user_ from server _server_IP_address_.`

**Explanation** The authentication of an IPsec connection has occurred with a SecurID server. The user will be prompted to provide further information before being authenticated.

-   user—The username associated with the connection
-   server \_IP\_address—The IP address of the relevant AAA server

**Recommended Action** None required.

### 113011

**Error Message** `%ASA-6-113011: AAA retrieved user specific group policy (_policy_) for user = _user_`

**Explanation** The authentication or authorization of an IPsec or WebVPN connection has occurred. The attributes of the group policy that was specified with the tunnel-group or webvpn commands have been retrieved.

**Recommended Action** None required.

### 113012

**Error Message** `%ASA-6-113012: AAA user authentication Successful : local database : user = _user_`

**Explanation** The user associated with a IPsec or WebVPN connection has been successfully authenticated to the local user database.

-   user—The username associated with the connection

**Recommended Action** None required.

### 113013

**Error Message** `%ASA-6-113013: AAA unable to complete the request Error : reason = _reason_ : user = _user_`

**Explanation** The AAA transaction for a user associated with an IPsec or WebVPN connection has failed because of an error or has been rejected because of a policy violation.

-   reason—The reason details
-   user—The username associated with the connection

**Recommended Action** None required.

### 113014

**Error Message** `%ASA-6-113014: AAA _authentication_ server not accessible : server = _server_IP_address_ : user = _user_`

**Explanation** The device was unable to communicate with the configured AAA server during the AAA transaction associated with an IPsec or WebVPN connection. This may or may not result in a failure of the user connection attempt depending on the backup servers configured in the aaa-server group and the availability of those servers. The username is hidden when invalid or unknown, but appears when valid or the no logging hide username command has been configured.

**Recommended Action** Verify connectivity with the configured AAA servers.

### 113015

**Error Message** `%ASA-6-113015: AAA user authentication Rejected : reason = _reason_ : local database : user = _user:_ : user IP = _xxx.xxx.xxx.xxx_`

**Explanation** A request for authentication to the local user database for a user associated with an IPsec or WebVPN connection has been rejected. The username is hidden when invalid or unknown, but appears when valid or the no logging hide username command has been configured.

-   reason—The details of why the request was rejected
-   user—The username associated with the connection
-   user\_ip —The IP address of the user who initiated the authentication or authorization request<915CLI>

**Recommended Action** None required.

### 113016

**Error Message** `%ASA-6-113016: AAA credentials rejected : reason = _reason_ : server = _server_IP_address_ : user = _user<915CLI>:_ : user IP = _xxx.xxx.xxx.xxx_`

**Explanation** The AAA transaction for a user associated with an IPsec or WebVPN connection has failed because of an error or rejected due to a policy violation. The username is hidden when invalid or unknown, but appears when valid or the no logging hide username command has been configured.

-   reason—The details of why the request was rejected
-   server\_IP\_address—The IP address of the relevant AAA server
-   user—The username associated with the connection
-   _<915CLI>user\_ip_ —The IP address of the user who initiated the authentication or authorization request

**Recommended Action** None required.

### 113017

**Error Message** `%ASA-6-113017: AAA credentials rejected : reason = _reason_ : local database : user = _user:_ : user IP = _xxx.xxx.xxx.xxx_`

**Explanation** The AAA transaction for a user associated with an IPsec or WebVPN connection has failed because of an error or rejected because of a policy violation. This event only appears when the AAA transaction is with the local user database rather than with an external AAA server.

-   reason—The details of why the request was rejected
-   user—The username associated with the connection
-   user\_ip —The IP address of the user who initiated the authentication or authorization request

**Recommended Action** None required.

### 113018

**Error Message** `%ASA-3-113018: User: '_user_', Unsupported downloaded ACL Entry: '_ACL_entry_', Action: '_action_'`

**Explanation** An ACL entry in unsupported format was downloaded from the authentication server. The following list describes the message values:

-   user—User trying to log in
-   ACL\_entry—Unsupported ACL entry downloaded from the authentication server
-   action—Action taken when encountering the unsupported ACL entry

**Recommended Action** The ACL entry on the authentication server has to be changed by the administrator to conform to the supported ACL entry formats.

### 113019

**Error Message** `%ASA-4-113019: Group = _group_, Username = _username_, IP = _peer_address_, Session disconnected. Session Type: _type_, Duration: _duration_, Bytes xmt: _count_, Bytes rcv: _count_, Reason: _reason_`

**Explanation** An indication of when and why the longest idle user is disconnected.

-   group—Group name
-   username—Username
-   IP—Peer address
-   Session Type—Session type (for example, IPsec or UDP)
-   duration—Connection duration in hours, minutes, and seconds
-   Bytes xmt—Number of bytes transmitted
-   _Bytes rcv_ —Number of bytes received
-   reason—Reason for disconnection

User Requested. Indicates a disconnection from client.

Lost Carrier

Lost Service. The service loss could be due to an issue from ISP during a SSL session establishment.

Idle Timeout

Max time exceeded

Administrator Reset- Indicates disconnection from secure gateway through vpn-sessiondb logoff

Administrator Reboot

Administrator Shutdown

Port Error

NAS Error

NAS Request

NAS Reboot

Port unneeded

Connection preempted. Indicates that the allowed number of simultaneous (same user) logins has been exceeded. To resolve this problem, increase the number of simultaneous logins or have users only log in once with a given username and password.

Port Suspended

Service Unavailable

Callback

User error

Host Requested

SA Expired

IKE Delete

Bandwidth Management Error

Certificate Expired

Phase 2 Mismatch

Firewall Mismatch

Peer Address Changed

ACL Parse Error

Phase 2 Error

Configuration Error

Peer Reconnected

Internal Error

Crypto map policy not found

L2TP initiated

VLAN Mapping Error

NAC-Policy Error

Dynamic Access Policy terminate

Client type not supported

Unknown

**Recommended Action** Unless the reason indicates a problem, then no action is required.

### 113020

**Error Message** `%ASA-3-113020: Kerberos error : Clock skew with server _ip_address_ greater than _time_in_seconds_ seconds`

**Explanation** Authentication for an IPsec or WebVPN user through a Kerberos server has failed because the clocks on the Secure Firewall ASA and the server are more than five minutes (300 seconds) apart. When this occurs, the connection attempt is rejected.

-   _ip\_address_ —The IP address of the Kerberos server

**Recommended Action** Synchronize the clocks on the Secure Firewall ASA and the Kerberos server.

### 113021

**Error Message** `%ASA-3-113021: Attempted console login failed user '_username_' did NOT have appropriate Admin Rights.`

**Explanation** A user has tried to access the management console and was denied.

-   _username_ —The username entered by the user

**Recommended Action** If the user is a newly added admin rights user, check that the service type (LOCAL or RADIUS authentication server) for that user is set to allow access:

-   nas-prompt—Allows login to the console and exec privileges at the required level, but not enable (configuration modification) access
-   admin—Allows all access and can be further constrained by command privileges

Otherwise, the user is inappropriately trying to access the management console; the action to be taken should be consistent with company policy for these matters.

### 113022

**Error Message** `%ASA-2-113022: AAA Marking _protocol_ server {_IP_address | hostname_} in aaa-server group _tag_ as FAILED`

**Explanation** The Secure Firewall ASA has tried an authentication, authorization, or accounting request to the AAA server and did not receive a response within the configured timeout window. The AAA server will be marked as failed and has been removed from service.

-   _protocol_ —The type of authentication protocol, which can be one of the following:

\- RADIUS

\- TACACS+

\- NT

\- RSA SecurID

\- Kerberos

\- LDAP

-   _ip-addr_ —The IP address of the AAA server
-   _tag_ —The server group name

**Recommended Action** Verify that the AAA server is online and is accessible from the Secure Firewall ASA.

### 113023

**Error Message** `%ASA-2-113023: AAA Marking _protocol_ server _ip-addr_ in aaa-server group _tag_ as ACTIVE`

**Explanation** The Secure Firewall ASA has reactivated the AAA server that was previously marked as failed. The AAA server is now available to service AAA requests.

-   _protocol_ —The type of authentication protocol, which can be one of the following:

\- RADIUS

\- TACACS+

\- NT

\- RSA SecurID

\- Kerberos

\- LDAP

-   _ip-addr_ —The IP address of the AAA server
-   _tag_ —The server group name

**Recommended Action** None required.

### 113024

**Error Message** `%ASA-5-113024: Group _tg_: Authenticating _type_ connection from _ip_ with username, _user_name_, from client certificate`

**Explanation** The prefill username feature overrides the username with one derived from the client certificate for use in AAA.

-   _tg_ —The tunnel group
-   _type_ —The type of connection (ssl-client or clientless)
-   _ip_ —The IP address of the connecting user
-   _user\_name_ —The name extracted from the client certificate for use in AAA

**Recommended Action** None required.

### 113025

**Error Message** `%ASA-5-113025: Group _tg_: _fields_ Could not authenticate _connection_type_ connection from _ip_`

**Explanation** A username cannot be successfully extracted from the certificate.

-   _tg_ —The tunnel group
-   _fields_ —The DN fields being searched for
-   _connection type_ —The type of connection (SSL client or clientless)
-   _ip_ —The IP address of the connecting user

**Recommended Action** The administrator should check that the authentication aaa certificate, ssl certificate-authentication, and authorization-dn-attributes keywords have been set correctly.

### 113026

**Error Message** `%ASA-4-113026: Error _error_ while executing Lua script for group _tunnel_group_`

**Explanation** An error occurred while extracting a username from the client certificate for use in AAA. This message is only generated when the username-from-certificate use-script option is enabled.

-   _error_ —Error string returned from the Lua environment
-   _tunnel group_ —The tunnel group attempting to extract a username from a certificate

**Recommended Action** Examine the script being used by the username-from-certificate use-script option for errors.

### 113027

**Error Message** `%ASA-2-113027: Error activating tunnel-group scripts`

**Explanation** The script file cannot be loaded successfully. No tunnel groups using the username-from-certificate use-script option work correctly.

**Recommended Action** The administrator should check the script file for errors using ASDM. Use the debug aaa command to obtain a more detailed error message that may be useful.

### 113028

**Error Message** `%ASA-7-113028: Extraction of username from VPN client certificate has _string._. [Request _num_]`

**Explanation** The processing request of a username from a certificate is running or has finished.

-   _num_ —The ID of the request (the value of the pointer to the fiber), which is a monotonically increasing number.
-   _string_ —The status message, which can one of the following:
    -   been requested
    -   started
    -   finished with error
    -   finished successfully
    -   completed

**Recommended Action** None required.

### 113029

**Error Message** `%ASA-4-113029: Group _group_ User _user_ IP _ipaddr_ Session could not be established: session limit of _num_ reached.`

**Explanation** The user session cannot be established because the current number of sessions exceeds the maximum session load.

**Recommended Action** Increase the configured limit, if possible, to create a load-balanced cluster.

### 113030

**Error Message** `%ASA-4-113030: Group _group_ User _user_ IP _ipaddr_ User ACL _acl_ from AAA doesn't exist on the device, terminating connection.`

**Explanation** The specified ACL was not found on the Secure Firewall ASA.

-   group—The name of the group
-   user—The name of the user
-   ipaddr—The IP address
-   acl—The name of the ACL

**Recommended Action** Modify the configuration to add the specified ACL or to correct the ACL name.

### 113031

**Error Message** `%ASA-4-113031: Group _group_ User _user_ IP _ipaddr_ _AnyConnect_ 'vpn-filter _filter_' is an IPv6 ACL; ACL not applied.`

**Explanation** The type of ACL to be applied is incorrect. An IPv6 ACL has been configured as an IPv4 ACL through the vpn-filter command.

-   _group_ —The group policy name of the user
-   _user_ —The username
-   _ipaddr_ —The public (not assigned) IP address of the user
-   _filter_ —The name of the VPN filter

**Recommended Action** Validate the VPN filter and IPv6 VPN filter configurations on the Secure Firewall ASA, and the filter parameters on the AAA (RADIUS) server. Make sure that the correct type of ACL is specified.

### 113032

**Error Message** `%ASA-4-113032: Group _group_ User _user_ IP _ipaddr_ _AnyConnect_ 'ipv6-vpn-filter _filter_' is an IPv4 ACL; ACL not applied.`

**Explanation** The type of ACL to be applied is incorrect. An IPv4 ACL has been configured as an IPv6 ACL through the ipv6-vpn-filter command.

-   _group_ —The group policy name of the user
-   _user_ —The username
-   _ipaddr_ —The public (not assigned) IP address of the user
-   _filter_ —The name of the VPN filter

**Recommended Action** Validate the VPN filter and IPv6 VPN filter configurations on the Secure Firewall ASA and the filter parameters on the AAA (RADIUS) server. Make sure that the correct type of ACL is specified.

### 113033

**Error Message** `%ASA-6-113033: Group _group_ User _user_ IP _ipaddr_ _AnyConnect_ session not allowed. ACL parse error.`

**Explanation** The WebVPN session for the specified user in this group is not allowed because the associated ACL did not parse. The user will not be allowed to log in via WebVPN until this error has been corrected.

-   _group_ —The group policy name of the user
-   _user_ —The username
-   _ipaddr_ —The public (not assigned) IP address of the user

**Recommended Action** Correct the WebVPN ACL.

### 113034

**Error Message** `%ASA-4-113034: Group _group_ User _user_ IP _ipaddr_ User ACL _acl_ from AAA ignored, AV-PAIR ACL used instead.`

**Explanation** The specified ACL was not used because a Cisco AV-PAIR ACL was used.

-   group—The name of the group
-   user—The name of the user
-   ipaddr—The IP address
-   acl—The name of the ACL

**Recommended Action** Determine the correct ACL to use and correct the configuration.

### 113035

**Error Message** `%ASA-4-113035: Group <_group_> User <_user_> IP <_ip_address_> Session terminated: AnyConnect not enabled or invalid AnyConnect image on the _device_name_`

**Explanation** The user logged in via the AnyConnect client. The SVC service is not enabled globally, or the SVC image is invalid or corrupted. The session connection has been terminated.

-   _group_ —The name of the group policy with which the user is trying to connect
-   _user_ —The name of the user who is trying to connect
-   _iaddrp_ —The IP address of the user who is trying to connect

**Recommended Action** Enable the SVC globally using the svc-enable command. Validate the integrity and versions of the SVC images by reloading new images using the svc image command.

### 113036

**Error Message** `%ASA-4-113036: Group _group_ User _user_ IP _ipaddr_ AAA parameter _name_ value invalid.`

**Explanation** The given parameter has a bad value. The value is not shown because it might be very long.

-   group—The name of the group
-   user—The name of the user
-   ipadddr—The IP address
-   name—The name of the parameter

**Recommended Action** Modify the configuration to correct the indicated parameter.

### 113037

**Error Message** `%ASA-6-113037: Group <_group_> User <_user_> IP <_ip_address_> Reboot pending, new sessions disabled. Denied user login.`

**Explanation** A user was unable to log in to WebVPN because the Secure Firewall ASA is in the process of rebooting.

**Recommended Action** None required.

### 113038

**Error Message** `%ASA-4-113038: Group _group_ User _user_ IP _ipaddr_ Unable to create _AnyConnect_parent_ session.`

**Explanation** The AnyConnect session was not created for the user in the specified group because of resource issues. For example, the user may have reached the maximum login limit.

-   group—The name of the group
-   user—The name of the user
-   ipadddr—The IP address

**Recommended Action** None required.

### 113039

**Error Message** `%ASA-6-113039: Group _group_ User _user_ IP _ipaddr_ _AnyConnect_parent_ session started.`

**Explanation** The AnyConnect session has started for the user in this group at the specified IP address. When the user logs in via the AnyConnect login page, the AnyConnect session starts.

-   group—The name of the group
-   user—The name of the user
-   ipadddr—The IP address

**Recommended Action** None required.

### 113040

**Error Message** `%ASA-4-113040: Group _group_ User _user_ IP _ipaddr_ Terminating the VPN connection attempt from _attempted_group_. Reason: This connection is group locked to _locked_group._.`

**Explanation** The tunnel group over which the connection is attempted is not the same as the tunnel group set in the group lock.

-   _attempted group_ —The tunnel group over which the connection came in
-   _locked group_ —The tunnel group for which the connection is locked or restricted

**Recommended Action** Check the group-lock value in the group policy or the user attributes.

### 113041

**Error Message** `%ASA-4-113041: Redirect ACL configured for _assigned_IP_ does not exist on the device.`

**Explanation** An error occurred when the redirect URL was installed and the ACL was received from the ISE, but the redirect ACL does not exist on the Secure Firewall ASA.

-   _assigned IP_ —The IP address that is assigned to the client

**Recommended Action** Configure the redirect ACL on the Secure Firewall ASA.

### 113042

**Error Message** `%ASA-4-113042: Non-HTTP connection from _src_if_:_src_ip_/_src_port_ to _dest_if_:_dest_ip_/_dest_port_ denied by redirect filter; only HTTP connections are supported for redirection.`

**Explanation** For the CoA feature, the redirect ACL filter drops the matching non-HTTP traffic during the redirect processing and provides information about the terminated traffic flow.

-   _src\_if_ , _src\_ip_ , _src\_port_ —The source interface, IP address, and port of the flow
-   _dest\_if_ , _dest\_ip_ , _dest\_port_ —The destination interface, IP address, and port of the flow
-   _username_ —The name of the user
-   _client\_IP_ —The IP address of the client

**Recommended Action** Validate the redirect ACL configuration on the Secure Firewall ASA. Make sure that the correct filter is used to match the traffic to redirect and does not block the flow that is intended to be allowed through.

### 113045

**Error Message** `%ASA-6-113045: AAA SDI server _IP_address_ in aaa-server group _group_name_: status changed from _previous-state_ to _current-state_`

**Explanation**

When servers are administratively added to or removed from SDI cluster, a new state⏤REMOVED is added to the status transition message.

**Example**

During initial transition:

```vbnet
%ASA-6-113045: AAA SDI server 10.x.x.x in aaa-server group test-SDI-group: status changed from REMOVED to OK
```

When server fails to respond after several attempts:

```vbnet
%ASA-6-113045: AAA SDI server 10.x.x.x in aaa-server group test-SDI-group: status changed from OK to SUSPENDED
```

When server finally responds:

```vbnet
%ASA-6-113045: AAA SDI server 10.x.x.x in aaa-server group test-SDI-group: status changed from SUSPENDED to OK
```

When server is administratively removed from the SDI cluster:

```vbnet
%ASA-6-113045: AAA SDI server 10.x.x.x in aaa-server group test-SDI-group: status changed from OK to REMOVED
```

**Recommended Action** None required.

## Messages 114001 to 199027

This section includes messages from 114001 to 199027.

### 114001

**Error Message** `%ASA-1-114001: Failed to initialize _card-type_ I/O card due to _error_string_.`

**Explanation** The system failed to initialize a 4GE SSM I/O card because of an I2C error or a switch initialization error.

-   _syslog\_id_ —Message identifier
-   _\>error\_string_ —An I2C serial bus error or a switch access error, which is a decimal error code. The following are I2C serial bus errors:
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

1.  Log and review the messages and the errors associated with the event.
2.  Reboot the software running on the Secure Firewall ASA.
3.  Power cycle the device. When you turn off the power, make sure you wait several seconds before turning the power on.
4.  If the problem persists, contact the Cisco TAC.

### 114002

**Error Message** `%ASA-1-114002: Failed to initialize SFP in _card-type_ I/O card due to _error_string_.`

**Explanation** The system failed to initialize an SFP connector in a 4GE SSM I/O card because of an I2C error or a switch initialization error.

-   _\>syslog\_id_ —Message identifier
-   _\>error\_string_ —An I2C serial bus error or a switch access error, which is a decimal error code. The following are the I2C serial bus errors:
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

1.  Log and review the messages and the errors associated with the event.
2.  Reboot the software running on the Secure Firewall ASA.
3.  Power cycle the device. When you turn off the power, make sure you wait several seconds before turning the power on.
4.  If the problem persists, contact the Cisco TAC.

### 114003

**Error Message** `%ASA-1-114003: Failed to run cached commands in _card-type_ I/O card due to _error_string_.`

**Explanation** The system failed to run cached commands in a 4GE SSM I/O card because of an I2C error or a switch initialization error.

-   _\>syslog\_id_ —Message identifier
-   _\>error\_string_ —An I2C serial bus error or a switch access error, which is a decimal error code. The following are the I2C serial bus errors:
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

1.  Log and review the messages and the errors associated with the event.
2.  Reboot the software running on the Secure Firewall ASA.
3.  Power cycle the device. When you turn off the power, make sure you wait several seconds before turning the power on.
4.  If the problem persists, contact the Cisco TAC.

### 114004

**Error Message** `%ASA-6-114004: _4GE_SSM_ I/O card Initialization is started.`

**Explanation** The user has been notified that a 4GE SSM I/O initialization is starting.

-   _\>syslog\_id_ —Message identifier

**Recommended Action** None required.

### 114005

**Error Message** `%ASA-6-114005: _4GE_SSM_ I/O card Initialization has completed.`

**Explanation** The user has been notified that an 4GE SSM I/O initialization is finished.

-   _\>syslog\_id_ —Message identifier

**Recommended Action** None required.

### 114006

**Error Message** `%ASA-3-114006: Failed to get port statistics in _card-type_ I/O card due to _error_string_.`

**Explanation** The Secure Firewall ASA failed to obtain port statistics in a 4GE SSM I/O card because of an I2C error or a switch initialization error.

-   _\>syslog\_id_ —Message identifier
-   _\>error\_string_ —An I2C serial bus error or a switch access error, which is a decimal error code. The following are the I2C serial bus errors:
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

1.  Log and review the messages and the errors associated with the event.
2.  Reboot the software running on the Secure Firewall ASA.
3.  Power cycle the device. When you turn off the power, make sure you wait several seconds before turning the power on.
4.  If the problem persists, contact the Cisco TAC.

### 114007

**Error Message** `%ASA-3-114007: Failed to get current msr in _card-type_ I/O card due to _error_string_.`

**Explanation** The Secure Firewall ASA failed to obtain the current module status register information in a 4GE SSM I/O card because of an I2C error or a switch initialization error.

-   _\>syslog\_id_ —Message identifier
-   _\>error\_string_ —An I2C serial bus error or a switch access error, which is a decimal error code. The following are the I2C serial bus errors:
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

1.  Log and review the messages and the errors associated with the event.
2.  Reboot the software running on the Secure Firewall ASA.
3.  Power cycle the device. When you turn off the power, make sure you wait several seconds before turning the power on.
4.  If the problem persists, contact the Cisco TAC.

### 114008

**Error Message** `%ASA-3-114008: Failed to enable port after link is up in _card-type_ I/O card due to _error_string_.`

**Explanation** The Secure Firewall ASA failed to enable a port after the link transition to Up state is detected in a 4GE SSM I/O card because of either an I2C serial bus access error or a switch access error.

-   _\>syslog\_id_ —Message identifier
-   _\>error\_string_ —An I2C serial bus error or a switch access error, which is a decimal error code. The following are I2C serial bus errors:
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

1.  Log and review the messages and the errors associated with the event.
2.  Reboot the software running on the Secure Firewall ASA.
3.  Power cycle the device. When you turn off the power, make sure you wait several seconds before turning the power on.
4.  If the problem persists, contact the Cisco TAC.

### 114009

**Error Message** `%ASA-3-114009: Failed to set multicast address in _card-type_ I/O card due to _error_string_.`

**Explanation** The Secure Firewall ASA failed to set the multicast address in a 4GE SSM I/O card because of an I2C error or a switch initialization error.

-   _\>syslog\_id_ —Message identifier
-   _\>error\_string_ —An I2C serial bus error or a switch access error, which is a decimal error code. The following are I2C serial bus errors:
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

1.  Log and review the messages and the errors associated with the event.
2.  Reboot the software running on the Secure Firewall ASA.
3.  Power cycle the device. When you turn off the power, make sure you wait several seconds before turning the power on.
4.  If the problem persists, contact the Cisco TAC.

### 114010

**Error Message** `%ASA-3-114010: Failed to set multicast hardware address in _card-type_ I/O card due to _error_string_.`

**Explanation** The Secure Firewall ASA failed to set the multicast hardware address in a 4GE SSM I/O card because of an I2C error or a switch initialization error.

-   _\>syslog\_id_ —Message identifier
-   _\>error\_string_ —An I2C serial bus error or a switch access error, which is a decimal error code. The following are I2C serial bus errors:
    -   I2C\_BUS\_TRANSACTION\_ERROR
    -   I2C\_CHKSUM\_ERROR
    -   I2C\_TIMEOUT\_ERROR
    -   I2C\_BUS\_COLLISION\_ERROR
    -   I2C\_HOST\_BUSY\_ERROR
    -   I2C\_UNPOPULATED\_ERROR
    -   I2C\_SMBUS\_UNSUPPORT
    -   I2C\_BYTE\_COUNT\_ERROR
    -   I2C\_DATA\_PTR\_ERROR
    -   I2C\_DATA\_PTR\_ERROR

**Recommended Action** Perform the following steps:

1.  Log and review the messages and the errors associated with the event.
2.  Reboot the software running on the Secure Firewall ASA.
3.  Power cycle the device. When you turn off the power, make sure you wait several seconds before turning the power on.
4.  If the problem persists, contact the Cisco TAC.

### 114011

**Error Message** `%ASA-3-114011: Failed to delete multicast address in _card-type_ I/O card due to _error_string_.`

**Explanation** The Secure Firewall ASA failed to delete the multicast address in a 4GE SSM I/O card because of either an I2C error or a switch initialization error.

-   _\>syslog\_id_ —Message identifier
-   _\>error\_string_ —An I2C serial bus error or a switch access error, which is a decimal error code. The following are I2C serial bus errors:
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

1.  Log and review the messages and the errors associated with the event.
2.  Reboot the software running on the Secure Firewall ASA.
3.  Power cycle the device. When you turn off the power, make sure you wait several seconds before turning the power on.
4.  If the problem persists, contact the Cisco TAC.

### 114012

**Error Message** `%ASA-3-114012: Failed to delete multicast hardware address in _card-type_ I/O card due to _error_string_.`

**Explanation** The Secure Firewall ASA failed to delete the multicast hardware address in a 4GE SSM I/O card because of an I2C error or a switch initialization error.

-   _\>syslog\_id_ —Message identifier
-   _\>error\_string_ —An I2C serial bus error or a switch access error, which is a decimal error code. The following are I2C serial bus errors:
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

1.  Log and review the messages and the errors associated with the event.
2.  Reboot the software running on the Secure Firewall ASA.
3.  Power cycle the device. When you turn off the power, make sure you wait several seconds before turning the power on.
4.  If the problem persists, contact the Cisco TAC.

### 114013

**Error Message** `%ASA-3-114013: Failed to set mac address table in _card-type_ I/O card due to _error_string_.`

**Explanation** The Secure Firewall ASA failed to set the MAC address table in a 4GE SSM I/O card because of an I2C error or a switch initialization error.

-   _\>syslog\_id_ —Message identifier
-   _\>error\_string_ —An I2C serial bus error or a switch access error, which is a decimal error code. The following are I2C serial bus errors:

\- I2C\_BUS\_TRANSACTION\_ERROR

\- I2C\_CHKSUM\_ERROR

\- I2C\_TIMEOUT\_ERROR

\- I2C\_BUS\_COLLISION\_ERROR

\- I2C\_HOST\_BUSY\_ERROR

\- I2C\_UNPOPULATED\_ERROR

\- I2C\_SMBUS\_UNSUPPORT

\- I2C\_BYTE\_COUNT\_ERROR

\- I2C\_DATA\_PTR\_ERROR

**Recommended Action** Perform the following steps:

1.  Log and review the messages and the errors associated with the event.
2.  Reboot the software running on the Secure Firewall ASA.
3.  Power cycle the device. When you turn off the power, make sure you wait several seconds before turning the power on.
4.  If the problem persists, contact the Cisco TAC.

### 114014

**Error Message** `%ASA-3-114014: Failed to set mac address in _card-type_ I/O card due to _error_string_.`

**Explanation** The Secure Firewall ASA failed to set the MAC address in a 4GE SSM I/O card because of an I2C error or a switch initialization error.

-   _\>syslog\_id_ —Message identifier
-   _\>error\_string_ —An I2C serial bus error or a switch access error, which is a decimal error code. The following are I2C serial bus errors:

\- I2C\_BUS\_TRANSACTION\_ERROR

\- I2C\_CHKSUM\_ERROR

\- I2C\_TIMEOUT\_ERROR

\- I2C\_BUS\_COLLISION\_ERROR

\- I2C\_HOST\_BUSY\_ERROR

\- I2C\_UNPOPULATED\_ERROR

\- I2C\_SMBUS\_UNSUPPORT

\- I2C\_BYTE\_COUNT\_ERROR

\- I2C\_DATA\_PTR\_ERROR

**Recommended Action** Perform the following steps:

1.  Log and review the messages and the errors associated with the event.
2.  Reboot the software running on the Secure Firewall ASA.
3.  Power cycle the device. When you turn off the power, make sure you wait several seconds before turning the power on.
4.  If the problem persists, contact the Cisco TAC.

### 114015

**Error Message** `%ASA-3-114015: Failed to set mode in _card-type_ I/O card due to _error_string_.`

**Explanation** The Secure Firewall ASA failed to set individual or promiscuous mode in a 4GE SSM I/O card because of an I2C error or a switch initialization error.

-   _\>syslog\_id_ —Message identifier
-   _\>error\_string_ —An I2C serial bus error or a switch access error, which is a decimal error code. The following are I2C serial bus errors:

\- I2C\_BUS\_TRANSACTION\_ERROR

\- I2C\_CHKSUM\_ERROR

\- I2C\_TIMEOUT\_ERROR

\- I2C\_BUS\_COLLISION\_ERROR

\- I2C\_HOST\_BUSY\_ERROR

\- I2C\_UNPOPULATED\_ERROR

\- I2C\_SMBUS\_UNSUPPORT

\- I2C\_BYTE\_COUNT\_ERROR

\- I2C\_DATA\_PTR\_ERROR

**Recommended Action** Perform the following steps:

1.  Log and review the messages and the errors associated with the event.
2.  Reboot the software running on the Secure Firewall ASA.
3.  Power cycle the device. When you turn off the power, make sure you wait several seconds before turning the power on.
4.  If the problem persists, contact the Cisco TAC.

### 114016

**Error Message** `%ASA-3-114016: Failed to set multicast mode in _card-type_ I/O card due to _error_string_.`

**Explanation**The Secure Firewall ASA failed to set the multicast mode in a 4GE SSM I/O card because of an I2C error or a switch initialization error.

-   _\>syslog\_id_ —Message identifier
-   _\>error\_string_ —An I2C serial bus error or a switch access error, which is a decimal error code. The following are the I2C serial bus errors:

\- I2C\_BUS\_TRANSACTION\_ERROR

\- I2C\_CHKSUM\_ERROR

\- I2C\_TIMEOUT\_ERROR

\- I2C\_BUS\_COLLISION\_ERROR

\- I2C\_HOST\_BUSY\_ERROR

\- I2C\_UNPOPULATED\_ERROR

\- I2C\_SMBUS\_UNSUPPORT

\- I2C\_BYTE\_COUNT\_ERROR

\- I2C\_DATA\_PTR\_ERROR

**Recommended Action** Perform the following steps:

1.  Log and review the messages and the errors associated with the event.
2.  Reboot the software running on the Secure Firewall ASA.
3.  Power cycle the device. When you turn off the power, make sure you wait several seconds before turning the power on.
4.  If the problem persists, contact the Cisco TAC.

### 114017

**Error Message** `%ASA-3-114017: Failed to get link status in _card-type_ I/O card due to _error_string_.`

**Explanation** The Secure Firewall ASA failed to obtain link status in a 4GE SSM I/O card because of an I2C serial bus access error or a switch access error.

-   _\>syslog\_id_ —Message identifier
-   _\>error\_string_ —An I2C serial bus error or a switch access error, which is a decimal error code. The following are the I2C serial bus errors:

\- I2C\_BUS\_TRANSACTION\_ERROR

\- I2C\_CHKSUM\_ERROR

\- I2C\_TIMEOUT\_ERROR

\- I2C\_BUS\_COLLISION\_ERROR

\- I2C\_HOST\_BUSY\_ERROR

\- I2C\_UNPOPULATED\_ERROR

\- I2C\_SMBUS\_UNSUPPORT

\- I2C\_BYTE\_COUNT\_ERROR

\- I2C\_DATA\_PTR\_ERROR

**Recommended Action** Perform the following steps:

1.  Notify the system administrator.
2.  Log and review the messages and the errors associated with the event.
3.  Reboot the software running on the Secure Firewall ASA.
4.  Power cycle the device. When you turn off the power, make sure you wait several seconds before turning the power on.
5.  If the problem persists, contact the Cisco TAC.

### 114018

**Error Message** `%ASA-3-114018: Failed to set port speed in _card-type_ I/O card due to _error_string_.`

**Explanation** The Secure Firewall ASA failed to set the port speed in a 4GE SSM I/O card because of an I2C error or a switch initialization error.

-   _\>syslog\_id_ —Message identifier
-   _\>error\_string_ —An I2C serial bus error or a switch access error, which is a decimal error code. The following are the I2C serial bus errors:

\- I2C\_BUS\_TRANSACTION\_ERROR

\- I2C\_CHKSUM\_ERROR

\- I2C\_TIMEOUT\_ERROR

\- I2C\_BUS\_COLLISION\_ERROR

\- I2C\_HOST\_BUSY\_ERROR

\- I2C\_UNPOPULATED\_ERROR

\- I2C\_SMBUS\_UNSUPPORT

\- I2C\_BYTE\_COUNT\_ERROR

\- I2C\_DATA\_PTR\_ERROR

**Recommended Action** Perform the following steps:

1.  Log and review the messages and the errors associated with the event.
2.  Reboot the software running on the Secure Firewall ASA.
3.  Power cycle the device. When you turn off the power, make sure you wait several seconds before turning the power on.
4.  If the problem persists, contact the Cisco TAC.

### 114019

**Error Message** `%ASA-3-114019: Failed to set media type in _card-type_ I/O card due to _error_string_.`

**Explanation** The Secure Firewall ASA failed to set the media type in a 4GE SSM I/O card because of an I2C error or a switch initialization error.

-   _\>syslog\_id_ —Message identifier
-   _\>error\_string_ —An I2C serial bus error or a switch access error, which is a decimal error code. The following are the I2C serial bus errors:

\- I2C\_BUS\_TRANSACTION\_ERROR

\- I2C\_CHKSUM\_ERROR

\- I2C\_TIMEOUT\_ERROR

\- I2C\_BUS\_COLLISION\_ERROR

\- I2C\_HOST\_BUSY\_ERROR

\- I2C\_UNPOPULATED\_ERROR

\- I2C\_SMBUS\_UNSUPPORT

\- I2C\_BYTE\_COUNT\_ERROR

\- I2C\_DATA\_PTR\_ERROR

**Recommended Action** Perform the following steps:

1.  Log and review the messages and the errors associated with the event.
2.  Reboot the software running on the Secure Firewall ASA.
3.  Power cycle the device. When you turn off the power, make sure you wait several seconds before turning the power on.
4.  If the problem persists, contact the Cisco TAC.

### 114020

**Error Message** `%ASA-3-114020: Port link speed is unknown in _4GE_SSM_ I/O card.`

**Explanation** The Secure Firewall ASA cannot detect the port link speed in a 4GE SSM I/O card.

**Recommended Action** Perform the following steps:

1.  Log and review the messages associated with the event.
2.  Reset the 4GE SSM I/O card and observe whether or not the software automatically recovers from the event.
3.  If the software does not recover automatically, power cycle the device. When you turn off the power, make sure you wait several seconds before you turn the power on.
4.  If the problem persists, contact the Cisco TAC.

### 114021

**Error Message** `%ASA-3-114021: Failed to set multicast address table in _4GE_SSM_ I/O card due to _error_.`

**Explanation**The Secure Firewall ASA failed to set the multicast address table in the 4GE SSM I/O card because of either an I2C serial bus access error or a switch access error.

-   error—A switch access error (a decimal error code) or an I2C serial bus error. Possible I2C serial bus errors include:

\- I2C\_BUS\_TRANSACTION\_ERROR

\- I2C\_CHKSUM\_ERROR

\- I2C\_TIMEOUT\_ERROR

\- I2C\_BUS\_COLLISION\_ERROR

\- I2C\_HOST\_BUSY\_ERROR

\- I2C\_UNPOPULATED\_ERROR

\- I2C\_SMBUS\_UNSUPPORT

\- I2C\_BYTE\_COUNT\_ERROR

\- I2C\_DATA\_PTR\_ERROR

**Recommended Action** Perform the following steps:

1.  Log and review the messages associated with the event.
2.  Try to reboot the Secure Firewall ASA.
3.  If the software does not recover automatically, power cycle the device. When you turn off the power, make sure you wait several seconds before you turn the power on.
4.  If the problem persists, contact the Cisco TAC.

### 114022

**Error Message** `%ASA-3-114022: Failed to pass broadcast traffic in 4GE SSM I/O card due to _error_string_`

**Explanation**The Secure Firewall ASA failed to pass broadcast traffic in the 4GE SSM I/O card because of a switch access error.

-   _error\_string_ —A switch access error, which will be a decimal error code

**Recommended Action** Perform the following steps:

1.  Log the message and errors surrounding the event.
2.  Retrieve the ssm4ge\_dump file from the compact flash, and send it to Cisco TAC.
3.  Contact Cisco TAC with the information collected in Steps 1 and 2.

| ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)

**Note** | ___

The 4GE SSM will be automatically reset and recover.

___ |
|--------|----------------------------------------------------------|

### 114023

**Error Message** `%ASA-3-114023: Failed to cache/flush mac table in _4GE_SSM_ I/O card due to _error_string_.`

**Explanation** A failure to cache or flush the MAC table in a 4GE SSM I/O card occurred because of an I2C serial bus access error or a switch access error. This message rarely occurs.

-   error\_string— Either an I2C serial bus error (see the second bullet for possible values) or a switch access error (which is a decimal error code).
-   I2C serial bus errors are as follows:

I2C\_BUS\_TRANSACTION\_ERROR

I2C\_CHKSUM\_ERROR

I2C\_TIMEOUT\_ERROR

I2C\_BUS\_COLLISION\_ERROR

I2C\_HOST\_BUSY\_ERROR

I2C\_UNPOPULATED\_ERROR

I2C\_SMBUS\_UNSUPPORT

I2C\_BYTE\_COUNT\_ERROR

I2C\_DATA\_PTR\_ERROR

**Recommended Action** Perform the following steps:

1.  Log the syslog message and the errors surrounding the event.
2.  Try to software reboot the Secure Firewall ASA.
3.  Power cycle the Secure Firewall ASA.

| ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)

**Note** | ___

When you turn off the power, make sure that you wait several seconds before powering on again. After you complete steps 1-3, if the problem persists, contact the Cisco TAC and provide the information described in step 1. You may need to RMA the Secure Firewall ASA.

___ |
|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

### 115000

**Error Message** `%ASA-2-115000: Critical assertion in process: _process name_ fiber: _fiber name_ , component: _component name_ , subcomponent: _subcomponent name_ , file: _filename_ , line: _line number_ , cond: _condition_`

**Explanation**The critical assertion has gone off and is used during development in checked builds only, but never in production builds.

-   process name— The name of the process
-   _fiber name_ —The name of the fiber
-   _component name_ —The name of the specified component
-   _subcomponent name_ —The name of the specified subcomponent
-   _filename_ —The name of the specified file
-   _line number_ —The line number for the specified line
-   _condition_ —The specified condition

**Recommended Action** A high priority defect should be filed, the reason for the assertion should be investigated, and the problem corrected.

### 115001

**Error Message** `%ASA-3-115001: Error in process: _process name_ fiber: _fiber name_ , component: _component name_ , subcomponent: _subcomponent name_ , file: _filename_ , line: _line number_ , cond: _condition_`

**Explanation** An error assertion has gone off and is used during development in checked builds only, but never in production builds.

-   process name— The name of the process
-   _fiber name_ —The name of the fiber
-   _component name_ —The name of the specified component
-   _subcomponent name_ —The name of the specified subcomponent
-   _filename_ —The name of the specified file
-   _line number_ —The line number for the specified line
-   _condition_ —The specified condition

**Recommended Action** A defect should be filed, the reason for the assertion should be investigated, and the problem fixed.

### 115002

**Error Message** `%ASA-4-115002: Warning in process: _process name_ fiber: _fiber name_ , component: _component name_ , subcomponent: _subcomponent name_ , file: _filename_ , line: _line number_ , cond: _condition_`

**Explanation** A warning assertion has gone off and is used during development in checked builds only, but never in production builds.

-   process name— The name of the process
-   _fiber name_ —The name of the fiber
-   _component name_ —The name of the specified component
-   _subcomponent name_ —The name of the specified subcomponent
-   _filename_ —The name of the specified file
-   _line number_ —The line number for the specified line
-   _condition_ —The specified condition

**Recommended Action** The reason for the assertion should be investigated and if a problem is found, a defect should be filed, and the problem corrected.

### 120001

**Error Message** `%ASA-5-120001: Call-Home Module started.`

**Explanation** The Smart Call-Home module started successfully after system bootup and failover in a stable state, and is ready to process Smart-Call Home events.

**Recommended Action** None required.

### 120002

**Error Message** `%ASA-5-120002: Call-Home Module terminated.`

**Explanation** When the Smart Call-Home module is disabled, it is then terminated.

**Recommended Action** None required.

### 120003

**Error Message** `%ASA-6-120003: Call-Home is processing _group_ event _title_.`

**Explanation** The Smart Call-Home module retrieved an event from the queue to process.

-   _group_ —The event group, which may be the following: inventory, configuration, diagnostic, environment, snapshot, telemetry, threat, and test.
-   _title_ —The event title

**Recommended Action** None required.

### 120004

**Error Message** `%ASA-4-120004: Call-Home _group_ event _title_ was dropped. Reason: _reason_`

**Explanation** A Smart Call-Home event was dropped. The event may have been dropped because of an internal error, the event queue is full, or the Smart Call-Home module was disabled after the message was generated, but before it was processed.

-   _group_ —The event group, which can be any of the following: inventory, configuration, diagnostic, environment, snapshot, telemetry, threat, and test.
-   _title_ —The event title
-   _reason_ —The drop reason, which can any of the following:

Internal Error—Various internal system errors occurred, such as being out of memory or parsing a CLI failed.

Queue Full—The number of events reached the configured limit.

Cancelled—The event was cancelled because the Smart Call-Home module is disabled.

**Recommended Action** If the drop reason is Queue Full, try to increase the event queue size and the rate-limit configuration to avoid event queue buildup. If the drop reason is Internal Error, turn on debugging by entering the debug sch fail command to obtain more detailed debugging information.

### 120005

**Error Message** `%ASA-4-120005: Call-Home _group_ message to _destination_ was dropped. Reason: _reason_`

**Explanation** A Smart Call-Home message was dropped. The message may have been dropped because of an internal error, a network error, or the Smart Call-Home module was disabled after the message was generated, but before it was delivered.

-   _group_ —The event group, which can be any of the following: inventory, configuration, diagnostic, environment, snapshot, telemetry, threat, and test.
-   _destination—_ The e-mail or URL destination
-   _reason_ —The drop reason, which can any of the following:

Internal Error—Various internal system errors occurred.

Delivery Failed—The packets cannot be delivered because a network error occurred.

Cancelled—The event was cancelled because the Smart Call-Home module is disabled.

**Recommended Action** If the drop reason is Delivery Failed, the message is dropped after three unsuccessful retransmissions, or because the error is local (such as no route to destination). Search message 120006 for the delivery failure reason, or turn on debugging by entering the debug sch fail command to obtain more detailed debugging information.

### 120006

**Error Message** `%ASA-4-120006: Call-Home _group_ message to _destination_ failed. Reason: _reason_`

**Explanation** An error occurred while the Smart Call Home module tried to deliver a message. The error may be transient. The message is not dropped when message 120006 is generated. The message may be queued for retransmission. The message is only dropped when message 120005 is generated.

-   _group_ —The event group, which can be any of the following: inventory, configuration, diagnostic, environment, snapshot, telemetry, threat, and test
-   _destination—_ The e-mail or URL destination
-   _reason_ —The failure reason

**Recommended Action** Check the error reason in the message. If the reason is NO\_ROUTE, INVALID\_ADDRESS, or INVALID\_URL, check the system configuration, DNS, and the name setting.

### 120007

**Error Message** `%ASA-6-120007: Call-Home _group_ message to _destination_ delivered.`

**Explanation** A Smart Call Home message was successfully delivered.

-   _group_ —The event group, which can be any of the following: inventory, configuration, diagnostic, environment, snapshot, telemetry, threat, and test
-   _destination—_ The e-mail or URL destination

**Recommended Action** None required.

### 120008

**Error Message** `%ASA-5-120008: Call-Home client _client_ was activated.`

**Explanation** The Smart Call Home module is enabled, an event group is also enabled, and that event group is subscribed to by at least one active profile. If these conditions are met, then all clients of that group will be activated.

-   _client_ —The name of the Smart Call Home client

**Recommended Action** None required.

### 120009

**Error Message** `%ASA-5-120009: Call-Home client _client_ was deactivated.`

**Explanation** The Smart Call Home module is disabled, an event group is enabled, or an event group is no longer subscribed to by any active profile. If these conditions are met, clients of that event group will be deactivated.

-   _client_ —The name of the Smart Call Home client

**Recommended Action** None required.

### 120010

**Error Message** `%ASA-3-120010: Call-Home _command_ command to client _client_ failed. Reason: _reason_.`

**Explanation** The Smart Call Home module notified Smart Call Home clients of certain events through the callback function. If the client does not interpret the command correctly, does not understand the command, or cannot process the command, an error will be returned.

-   _command—_ ENABLE, DISABLE, or READY
-   _client_ —The name of the Smart Call Home client
-   _reason_ —The reason for failure

**Recommended Action** Turn on debugging by entering the debug sch fail command to obtain more detailed debugging information.

### 120011

**Error Message** `%ASA-4-120011: To ensure Smart Call Home can properly communicate with Cisco, use the command \ to configure at least one DNS server.`

**Recommended Action** Once this syslog is generated, run the dns name-server command to configure at least one DNS server. Otherwise, network-local DNS server or Cisco DNS server will be used.

### 120012

**Error Message** `%ASA-5-120012: User "_username_" chose to _choice_ call-home anonymous reporting at the prompt.`

**Explanation** The administrator was notified that a user has responded to the Smart Call Home prompt to enable, disable, or postpone anonymous reporting.

-   _username_ —The user who responded to the prompt
-   _choice_ —The available entries are enable, disable, or postpone

**Recommended Action** To enable anonymous reporting in the future, enter the call-home reporting anonymous command. To disable anonymous reporting, enter the no call-home reporting anonymous command.

### 121001

**Error Message** `%ASA-5-121001: _id_`

**Explanation** Whenever telemetry support is enabled or disabled on the chassis, this message is displayed.

-   _id_—The message identifier as in the appAG-appAgent message
-   _status_— The available values are enabled or disabled

**Example**

```csharp
%ASA-5-121001: msgId 1. Telemetry support on the chassis: disabled
```

**Recommended Action** None required.

### 121002

**Error Message** `%ASA-5-121002: _status._`

**Explanation** Whenever telemetry support is enabled or disabled on the blade, this message is displayed.

-   _status_—The available entries are enable or disable

**Example**

```csharp
%ASA-5-121002: Telemetry support on the blade: enabled
%ASA-5-121002: Telemetry support on the blade: disabled
```

**Recommended Action** None required.

### 121003

**Error Message** `%ASA-6-121003: _id_`

**Explanation** The message is displayed whenever ASA receives a telemetry request from FXOS. The message displays the SSE connector status, telemetry support status on the blade, and whether the telemetry data was sent to FXOS.

-   _id_—The message identifier as in the appAG-appAgent message
-   _connector status_—Whether telemetry support is enabled or disabled on the chassis
-   _blade status_—Whether telemetry support is enabled or disabled on the blade
-   _data status_—Whether telemetry data is sent or not

**Example**

```csharp
%ASA-6-121003: msgId 2. Telemetry request from the chassis received. SSE connector status: enabled. Telemetry config on the blade: enabled. Telemetry data Sent
%ASA-6-121003: msgId 1. Telemetry request from the chassis received. SSE connector status: enabled. Telemetry config on the blade: enabled. Telemetry data Sent
```

**Recommended Action** None required.

### 199001

**Error Message** `%ASA-5-199001: Reloaded at _time_ by _user_. Reload reason: _reload reason_`

**Explanation** The address of the host that is initiating an Secure Firewall ASA reboot with the reload command has been recorded.

**Recommended Action** None required.

### 199002

**Error Message** `%ASA-6-199002: Startup completed. Beginning operation.`

**Explanation** The Secure Firewall ASA finished its initial boot and the flash memory reading sequence, and is ready to begin operating normally.

| ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)

**Note** | ___

You cannot block this message by using the no logging message command.

___ |
|--------|----------------------------------------------------------------------------|

**Recommended Action** None required.

### 199003

**Error Message** `%ASA-6-199003: Reducing Link MTU _dec_`

**Explanation** The Secure Firewall ASA received a packet from the outside network that uses a larger MTU than the inside network. The Secure Firewall ASA then sent an ICMP message to the outside host to negotiate an appropriate MTU. The log message includes the sequence number of the ICMP message.

**Recommended Action** None required.

### 199005

**Error Message** `%ASA-6-199005: Startup begin`

**Explanation** The Secure Firewall ASA started.

**Recommended Action** None required.

### 199010

**Error Message** `%ASA-1-199010: Signal _number_ caught in process/fiber (_rtcli_async_executor_process_)/(_rtcli_async_executor_) at address _ip_address_, corrective action at _ip_address_`

**Explanation** The system has recovered from a serious error.

**Recommended Action** Contact the Cisco TAC.

### 199011

**Error Message** `%ASA-2-199011: Close on bad channel in process/fiber _process_name_/_fiber_name_, channel ID _p_, channel state _channel_state_`

**Explanation** An unexpected channel close condition has been detected.

-   _p_—The channel ID
-   _process/fiber_ —The name of the process/fiber that caused the bad channel close operation
-   _s_—The channel state

**Recommended Action** Contact the Cisco TAC and attach a log file.

### 199012

**Error Message** `%ASA-1-199012: Stack overflow during new_stack_call in process/fiber _process_name_/_fiber_name_, call target _f_, stack size _s_`

**Explanation** A stack overflow condition has been detected.

-   _f_—The target of the new\_stack\_call
-   _process/fiber_ —The name of the process/fiber that caused the stack overflow
-   _s_—The new stack size specified in new\_stack\_call

**Recommended Action** Contact the Cisco TAC and attach the log file.

### 199013

**Error Message** `%ASA-1-199013: _syslog_`

**Explanation** A variable syslog was generated by an assistive process.

-   syslog—The alert syslog passed verbatim from an external process

**Recommended Action** Contact the Cisco TAC.

### 199014

**Error Message** `%ASA-2-199014: _syslog_`

**Explanation** A variable syslog was generated by an assistive process.

-   syslog—The critical syslog passed verbatim from an external process

**Recommended Action** Contact the Cisco TAC.

### 199015

**Error Message** `%ASA-3-199015: _syslog_`

**Explanation** A variable syslog was generated by an assistive process.

-   syslog—The error syslog passed verbatim from an external process.
    
    Example of syslog messages generated:
    
    | ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)
    
    **Note** | ___
    
    These logs do not indicate any issues. They are populated only to provide information.
    
    ___ |
    |--------|--------------------------------------------------------------------------------------------|
    -   `port-manager: PHYREG debug list for if_index = _value_ is empty`
        
    -   `port-manager: mrvlGetEpmPhyPortNumfromSlotInterfaceAggrPort finding interfaceName = Ethernet 1/5`
        
    -   `port-manager: mrvlGetEpmPhyPortNumfromSlotInterfaceAggrPort: portNum was not found for slot 0 port = _port_ interfaceName = Ethernet 1/16`
        
    -   `port-manager: mrvlGetPortNumFromSrcId: port was not found for src_id _number_`
        

**Recommended Action** Contact the Cisco TAC.

### 199016

**Error Message** `%ASA-4-199016:` _syslog_

**Explanation** A variable syslog was generated by an assistive process.

-   syslog—The warning syslog passed verbatim from an external process
    

In some instances, the message may appear to be an issue that is internal to the device platform process. For example, in the following message though it indicates to be an internal device issue, it is related to an internal virtual device which is not used on the device platform, and it does not cause any functionality impact.

```ruby
%ASA-4-199016: mm dd HH:MM:SS acpid: input device has been disconnected, fd 4
```

**Recommended Action** Contact the Cisco TAC.

### 199017

**Error Message** `%ASA-5-199017: _syslog_`

**Explanation** A variable syslog was generated by an assistive process.

-   syslog—The notification syslog passed verbatim from an external process

**Recommended Action** None required.

### 199018

**Error Message** `%ASA-6-199018: _syslog_`

**Explanation** A variable syslog was generated by an assistive process.

-   syslog—The informational syslog passed verbatim from an external process

**Recommended Action** None required.

### 199019

**Error Message** `%ASA-7-199019: _syslog_`

**Explanation** A variable syslog was generated by an assistive process.

-   syslog—The debugging syslog passed verbatim from an external process

**Recommended Action** None required.

### 199020

**Error Message** `%ASA-2-199020: System memory utilization has reached _X_ %. System will reload if memory usage reaches the configured trigger level of _Y_ %.`

**Explanation** The system memory utilization has reached 80% of the system memory watchdog facility's configured value.

**Recommended Action** Reduce system memory utilization by reducing traffic load, removing traffic inspections, reducing the number of ACL entries, and so on. If a memory leak is suspected, contact Cisco TAC.

### 199021

**Error Message** `%ASA-1-199021: System memory utilization has reached the configured threshold of _Y_%%. System will now reload.`

**Explanation** The system memory utilization has reached 100% of the system memory watchdog facility's configured value. The system will automatically reload.

**Recommended Action** Reduce system memory utilization by reducing traffic load, removing traffic inspections, reducing the number of ACL entries, and so on. If a memory leak is suspected, contact Cisco TAC.

### 199027

**Error Message** `%ASA-5-199027: Restore operation was aborted at _<HH:MM:SS>UTC<DD:MM:YY>_.`

**Explanation** This message indicates that the backup restoration failed while using the 'restore' command.

**Recommended Action** None