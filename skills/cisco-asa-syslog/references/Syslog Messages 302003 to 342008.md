## Messages 302003 to 319004

This chapter includes messages from 302003 to 319004 .

### 302003

**Error Message** `%ASA-6-302003: Built H245 connection for faddr _foreign_ip_address_ laddr _local_ip_address_/_local_port_`

**Error Message** `%ASA-6-302003: Built H245 connection for faddr _foreign_ip_address_/_foreign_port_ laddr _local_ip_address_`

**Explanation** An H.245 connection has been started from the f_oreign\_ip\_address_ to the _local\_ip\_address_. The Secure Firewall ASA has detected the use of an Intel Internet Phone. The foreign port (_foreign\_port_ ) only appears on connections from outside the Secure Firewall ASA. The local port value (_local\_port_ ) only appears on connections that were started on an internal interface.

**Recommended Action** None required.

### 302004

**Error Message-1** `%ASA-6-302004: Pre-allocate H323 {_TCP | UDP_} backconnection for faddr _foreign_ip_address_ to laddr _local_ip_address_/__local_port__`

**Error Message-2** `%ASA-6-302004: Pre-allocate H323 {_TCP | UDP_} backconnection for faddr _foreign_ip_address_/_foreign_port_ to laddr _local_ip_address_`

**Explanation** An H.323 UDP back connection has been preallocated to the foreign address (foreign\_ip\_address) from the local address (local\_ip\_address). The Secure Firewall ASA has detected the use of an Intel Internet Phone. The foreign port (foreign\_port) only appears on connections from outside the Secure Firewall ASA. The local port value (local\_port) only appears on connections that were started on an internal interface.

**Recommended Action** None required.

### 302010

**Error Message** `%ASA-6-302010: _connections_ in use, _connections_ most used`

**Explanation** Provides information on the number of connections that are in use and most used.

-   connections—The number of connections

**Recommended Action** None required.

### 302012

**Error Message-1** `%ASA-6-302012: Pre-allocate H225 Call Signalling Connection for faddr _foreign_ip_address_ to laddr _local_ip_address_/_local_port_`

**Error Message-2** `%ASA-6-302012: Pre-allocate H225 Call Signalling Connection for faddr _foreign_ip_address_/_foreign_port_ to laddr _local_ip_address_`

**Explanation** An H.225 secondary channel has been preallocated.

**Recommended Action** None required.

### 302013

**Error Message** `%ASA-6-302013: Built _{inbound | outbound}__[Probe]_ TCP connection _connection_id_ for _interface_:_real-address_/_real-port_ (_(mapped-address/mapped-port)_)_idfw_user_ to _interface_:_real-address_/_real-port_ (_mapped-address/mapped-port_)_inside_idfw_and_sg_info_ _id_port_num_ _rx_ring_num_ [(_user_)]`

**Explanation** A TCP connection slot between two hosts was created.

-   probe—Indicates the TCP connection is a probe connection
    
-   connection\_id —A unique identifier
-   interface, real-address, real-port—The actual sockets
-   mapped-address, mapped-port—The mapped sockets
-   user—The AAA name of the user
-   idfw\_user—The name of the identity firewall user
-   **id\_port\_num**—Internal port number
    
-   **rx\_ring\_num**—Internal RX ring number
    

If inbound is specified, the original control connection was initiated from the outside. For example, for FTP, all data transfer channels are inbound if the original control channel is inbound. If outbound is specified, the original control connection was initiated from the inside.

**Recommended Action** None required.

### 302014

**Error Message** `%ASA-6-302014: Teardown [_Probe_]TCP connection _connection_id_ for _interface_:_real_address_/_real_port__idfw_user_ to _interface_:_real_address_/_real_port__idfw_user_ duration _hh:mm:ss_ bytes _bytes_ _reason_string__teardown_initiator__initiator_ _id_port_num_ _rx_ring_num_ max-rate _conn_rate_/_max_permissible_rate_ (_user_)`

**Explanation** A TCP connection between two hosts was deleted. The following list describes the message values:

-   _probe_—Indicates the TCP connection is a probe connection
    
-   _id_—A unique identifier
    
-   _interface, real-address, real-port_—The actual socket
    
-   _duration_—The lifetime of the connection
    
-   _bytes_— The data transfer of the connection
    
-   _max-rate_—The maximum threshold for the number of new UDP connections established per second
    
-   _User_—The AAA name of the user
    
-   _idfw\_user_ —The name of the identity firewall user
    
-   _reason_—The action that causes the connection to terminate. Set the reason variable to one of the TCP termination reasons listed in the following table.
    
-   _teardown-initiator_—Interface name of the side that initiated the teardown.
    
-   _id\_port\_num_—Internal port number
    
-   _rx\_ring\_num_—Internal RX ring number
    

|                       Reason                        |                                                                                                                                                                                                                          Description                                                                                                                                                                                                                          |
|-----------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                    Conn-timeout                     |                                                                                                                                                                                 The connection ended when a flow is closed because of the expiration of its inactivity timer.                                                                                                                                                                                 |
|                   Deny Terminate                    |                                                                                                                                                                                                        Flow was terminated by application inspection.                                                                                                                                                                                                         |
|               Failover primary closed               |                                                                                                                                                                         The standby unit in a failover pair deleted a connection because of a message received from the active unit.                                                                                                                                                                          |
|                     FIN Timeout                     |                                                                                                                                                                                    Force termination after 10 minutes awaiting the last ACK or after half-closed timeout.                                                                                                                                                                                     |
|              Flow closed by inspection              |                                                                                                                                                                                                        Flow was terminated by the inspection feature.                                                                                                                                                                                                         |
|               Flow terminated by IPS                |                                                                                                                                                                                                                  Flow was terminated by IPS.                                                                                                                                                                                                                  |
|                  Flow reset by IPS                  |                                                                                                                                                                                                                    Flow was reset by IPS.                                                                                                                                                                                                                     |
|          Flow terminated by TCP Intercept           |                                                                                                                                                                                                             Flow was terminated by TCP Intercept.                                                                                                                                                                                                             |
|                   Flow timed out                    |                                                                                                                                                                                                                      Flow has timed out.                                                                                                                                                                                                                      |
|              Flow timed out with reset              |                                                                                                                                                                                                              Flow has timed out, but was reset.                                                                                                                                                                                                               |
|                 Flow is a loopback                  |                                                                                                                                                                                                                      Flow is a loopback.                                                                                                                                                                                                                      |
| Free the flow created as result of packet injection |                                                                                                                                                                      The connection was built because the packet tracer feature sent a simulated packet through the Secure Firewall ASA.                                                                                                                                                                      |
|                     Invalid SYN                     |                                                                                                                                                                                                                 The SYN packet was not valid.                                                                                                                                                                                                                 |
|                   IPS fail-close                    |                                                                                                                                                                                                       Flow was terminated because the IPS card is down.                                                                                                                                                                                                       |
|         No interfaces associated with zone          |                                                                                                                                                                            Flows were torn down after the “no nameif” or “no zone-member” leaves a zone with no interface members.                                                                                                                                                                            |
|                 No valid adjacency                  |                                                                                                                                              This counter is incremented when the Secure Firewall ASA tried to obtain an adjacency and could not obtain the MAC address for the next hop. The packet is dropped.                                                                                                                                              |
|                   Pinhole Timeout                   |                                                                    The counter is incremented to report that the Secure Firewall ASA opened a secondary flow, but no packets passed through this flow within the timeout interval, and so it was removed. An example of a secondary flow is the FTP data channel that is created after successful negotiation on the FTP control channel.                                                                     |
|  Probe maximum retries of retransmission exceeded   |                                                                                                                                                                             The connection was torn down because the TCP packet exceeded maximum probe retries of retransmission.                                                                                                                                                                             |
|      Probe maximum retransmission time elapsed      |                                                                                                                                                                                   The connection was torn down because the maximum probing time for TCP packet had elapsed.                                                                                                                                                                                   |
|                 Probe received RST                  |                                                                                                                                                                                        The connection was torn down because probe connection received RST from server.                                                                                                                                                                                        |
|                 Probe received FIN                  |                                                                                                                                                                The connection was torn down because probe connection received FIN from server and complete FIN closure process was completed.                                                                                                                                                                 |
|                   Probe completed                   |                                                                                                                                                                                                             The probe connection was successful.                                                                                                                                                                                                              |
|                    Route change                     | When the Secure Firewall ASA adds a lower cost (better metric) route, packets arriving that match the new route cause their existing connection to be torn down after the user-configured timeout (floating-conn) value. Subsequent packets rebuild the connection out of the interface with the better metric. To prevent the addition of lower cost routes from affecting active flows, you can set the floating-conn configuration timeout value to 0:0:0. |
|                     SYN Control                     |                                                                                                                                                                                                    A back channel initiation occurred from the wrong side.                                                                                                                                                                                                    |
|                     SYN Timeout                     |                                                                                                                                                                                         Force termination after 30 seconds, awaiting three-way handshake completion.                                                                                                                                                                                          |
|               TCP bad retransmission                |                                                                                                                                                                                              The connection was terminated because of a bad TCP retransmission.                                                                                                                                                                                               |
|                      TCP FINs                       |                                                                                                                                                                                                            A normal close-down sequence occurred.                                                                                                                                                                                                             |
|                   TCP Invalid SYN                   |                                                                                                                                                                                                                    Invalid TCP SYN packet.                                                                                                                                                                                                                    |
|                TCP Reset - APPLIANCE                |                                                                                                                                                                                         The flow is closed when a TCP reset is generated by the Secure Firewall ASA.                                                                                                                                                                                          |
|                    TCP Reset - I                    |                                                                                                                                                                                                                  Reset was from the inside.                                                                                                                                                                                                                   |
|                    TCP Reset - O                    |                                                                                                                                                                                                                  Reset was from the outside.                                                                                                                                                                                                                  |
|             TCP segment partial overlap             |                                                                                                                                                                                                         A partially overlapping segment was detected.                                                                                                                                                                                                         |
|        TCP unexpected window size variation         |                                                                                                                                                                                             A connection was terminated due to variation in the TCP window size.                                                                                                                                                                                              |
|              Tunnel has been torn down              |                                                                                                                                                                                                        Flow was terminated because the tunnel is down.                                                                                                                                                                                                        |
|                     Unauth Deny                     |                                                                                                                                                                                                         An authorization was denied by a URL filter.                                                                                                                                                                                                          |
|                       Unknown                       |                                                                                                                                                                                                                An unknown error has occurred.                                                                                                                                                                                                                 |
|                VPN reclassify failed                |                                                                                                                                                                                          When connections fail to be reclassified for passing through a VPN tunnel.                                                                                                                                                                                           |
|                     Xlate Clear                     |                                                                                                                                                                                                                  A command line was removed.                                                                                                                                                                                                                  |

**Recommended Action** None required.

### 302015

**Error Message** `%ASA-6-302015: Built {_inbound | outbound_} UDP connection _connection_id_ for _interface_:_real_address_/_real_port_ (_mapped_address_/_mapped_port_)_idfw_user_ to _interface_:_real_address_/_real_port_ (_mapped_address_/_mapped_port_)_idfw_user_ _id_port_num_ _rx_ring_num_ [(_user_)]`

**Explanation** A UDP connection slot between two hosts was created. The following list describes the message values:

-   _number_—A unique identifier
    
-   _interface, real\_address, real\_port_—The actual sockets
    
-   _mapped\_address and mapped\_port_—The mapped sockets
    
-   _user_—The AAA name of the user
    
-   _idfw\_user_ —The name of the identity firewall user
    
-   _id\_port\_num_—Internal port number
    
-   _rx\_ring\_num_—Internal RX ring number
    

If inbound is specified, then the original control connection is initiated from the outside. For example, for UDP, all data transfer channels are inbound if the original control channel is inbound. If outbound is specified, then the original control connection is initiated from the inside.

**Recommended Action** None required.

### 302016

**Error Message** `%ASA-6-302016: Teardown UDP connection _connection_id_ for _interface_:_real_address_/_real_port__idfw_user_ to _interface_:_real_address_/_real_port__idfw_user_ duration _hh:mm:ss_ bytes _bytes_ _id_port_num_ _rx_ring_num_ max-rate _conn_rate_/_max_permissible_rate_ Bps (_user_)`

**Explanation** A UDP connection slot between two hosts was deleted. The following list describes the message values:

-   _number_—A unique identifier
    
-   _interface, real\_address, real\_port_—The actual sockets
    
-   _time_—The lifetime of the connection
    
-   _bytes_—The data transfer of the connection
    
-   _id_— unique identifier
    
-   _interface, real-address, real-port_—The actual sockets
    
-   _duration_— The lifetime of the connection
    
-   _bytes_—The data transfer of the connection
    
-   _max-rate_—The maximum threshold for the number of new UDP connections established per second
    
-   _user_—The AAA name of the user
    
-   _idfw\_user_—The name of the identity firewall user
    
-   _id\_port\_num_—Internal port number
    
-   _rx\_ring\_num_—Internal RX ring number
    

**Recommended Action** None required.

### 302017

**Error Message** `%ASA-6-302017: Built {_inbound | outbound_} GRE connection _id_ from _interface_:_real_address_ (_translated_address_)_idfw_user_ to _interface_:_real_address_/_real_cid_ (_translated_address_/_translated_cid_)_idfw_user_ _id_port_num_ _rx_ring_num_ [(_user_)]`

**Explanation** A GRE connection slot between two hosts was created. The id is an unique identifier. The interface, real\_address, real\_cid tuple identifies the one of the two simplex PPTP GRE streams. The parenthetical translated\_address, translated\_cid tuple identifies the translated value with NAT. If inbound is indicated, then the connection can only be used inbound. If outbound is indicated, then the connection can only be used for outbound. The following list describes the message values:

-   _id_—Unique number identifying the connection
    
-   _inbound_—Control connection is for inbound PPTP GRE flow
    
-   _outbound_—Control connection is for outbound PPTP GRE flow
    
-   _interface\_name_—The interface name
    
-   _real\_address_—IP address of the actual host
    
-   _real\_cid_—Untranslated call ID for the connection
    
-   _translated\_address_—IP address after translation
    
-   _translated\_cid_—Translated call
    
-   _user_—AAA user name
    
-   _idfw\_user_—The name of the identity firewall user
    
-   _id\_port\_num_—Internal port number
    
-   _rx\_ring\_num_—Internal RX ring number
    

**Recommended Action** None required.

### 302018

**Error Message** `%ASA-6-302018: Teardown GRE connection _id_ from _interface_:_real_address__translated_address_ to _interface_:_real_address_/_real_cid__idfw_user_ duration _hh:mm:ss_ bytes _bytes_ _id_port_num_ _rx_ring_num_ [(_user_)]`

**Explanation** A GRE connection slot between two hosts was deleted. The interface, real\_address, real\_port tuples identify the actual sockets. Duration identifies the lifetime of the connection. The following list describes the message values:

-   _id_—Unique number identifying the connection
    
-   _interface_—The interface name
    
-   _real\_address_—IP address of the actual host
    
-   _real\_port_—Port number of the actual host
    
-   _hh:mm:ss_—Time in hour:minute:second format
    
-   _bytes_—Number of PPP bytes transferred in the GRE session
    
-   _reason_—Reason why the connection was terminated
    
-   _user_—AAA user name
    
-   _idfw\_user_—The name of the identity firewall user
    
-   _id\_port\_num_—Internal port number
    
-   _rx\_ring\_num_—Internal RX ring number
    

**Recommended Action** None required.

### 302019

**Error Message** `%ASA-3-302019: H.323 _library_name_ ASN Library failed to initialize, error code _number_`

**Explanation** The specified ASN librar y that the Secure Firewall ASA uses for decoding the H.323 messages failed to initialize; the Secure Firewall ASA cannot decode or inspect the arriving H.323 packet. The Secure Firewall ASA allows the H.323 packet to pass through without any modification. When the next H.323 message arrives, the Secure Firewall ASA tries to initialize the library again.

**Recommended Action** If this message is generated consistently for a particular library, contact the Cisco TAC and provide them with all log messages (preferably with timestamps).

### 302020

(Inbound) **Error Message** `%ASA-6-302020: Built _inbound_ ICMP connection for faddr _src_ip_address_/_src_port__outside_idfw_user_ gaddr _dest_ip_address_/_dest_port_ laddr _dest_ip_address_/_dest_port__inside_idfw_user_ [(_user_)] type _type_ code _code_ Internal-Data0/_id_port_num_:RX[_rx_ring_num_]`

(Outbound) **Error Message** `%ASA-6-302020: Built _outbound_ ICMP connection for faddr _dest_ip_address_/_dest_port__outside_idfw_user_ gaddr _src_ip_/_src_port_ laddr _src_ip_/_src_port__inside_idfw_user_[_(user)_] type _type_ code _code_ Internal-Data0/_id_port_num_:RX[rx_ring_num]`

**Explanation** This message is generated when an ICMP session was established in the fast-path. The following list describes the message values:

-   _faddr_ —Specifies the IP address of the foreign host
    
-   _gaddr_ —Specifies the IP address of the global host
    
-   _laddr_ —Specifies the IP address of the local host
    
-   _idfw\_user_ —The name of the identity firewall user
    
-   _user_ —The username associated with the host from where the connection was initiated
    
-   _type_ —Specifies the ICMP type
    
-   _code_ —Specifies the ICMP code
    
-   _Rx_ —Specifies the received data circular-buffer size, where the buffer is overwritten, starting from the beginning, when the buffer is full.
    
-   _id\_port\_num_—Internal port number
    
-   _rx\_ring\_num_—Internal RX ring number
    

**Recommended Action** None required.

### 302021

**Error Message** `%ASA-6-302021: Teardown ICMP connection for faddr _src_ip_address_/_src_port__outside_idfw_user_ gaddr _dest_ip_address_/_dest_port_ laddr _dest_ip_address_/_dest_port__inside_idfw_user_ [(_user_)] type _type_ code _code_ Internal-Data0/_id_port_num_:RX[_rx_ring_num_]`

**Explanation** This message is generated when an ICMP session is removed in the fast-path. The following list describes the message values:

-   _faddr_ —Specifies the IP address of the foreign host
    
-   _gaddr_ —Specifies the IP address of the global host
    
-   _laddr_ —Specifies the IP address of the local host
    
-   _idfw\_user_ —The name of the identity firewall user
    
-   _user_ —The username associated with the host from where the connection was initiated
    
-   _type_ —Specifies the ICMP type
    
-   _code_—Specifies the ICMP code
    
-   Rx—Specifies the received data circular-buffer size, where the buffer is overwritten, starting from the beginning, when the buffer is full.
    
-   _id\_port\_num_—Internal port number
    
-   _rx\_ring\_num_—Internal RX ring number
    

**Recommended Action** None required.

### 302022

**Error Message** `%ASA-6-302022: Built _role_ stub TCP connection for _interface_:_real-address_/_real-port_ (_mapped-address_/_mapped-port_) to _interface_:_real-address_/_real-port_ (_mapped-address_/_mapped-port)_)`

**Explanation** A TCP director/backup/forwarder flow has been created.

**Recommended Action** None required.

### 302023

**Error Message** `%ASA-6-302023: Teardown _stub_ TCP connection for _interface_:_real-address_/_real-port_ to _interface_:_real-address_/_real-port_ duration _hh:mm:ss_ forwarded bytes _bytes_ _reason_`

**Explanation** A TCP director/backup/forwarder flow has been torn down.

**Recommended Action** None required.

### 302024

**Error Message** `%ASA-6-302024: Built _role_ stub UDP connection for _interface_:_real-address_/_real-port_ (_mapped-address_/_mapped-port_) to _interface_:_real-address_/_real-port_ (_mapped-address_/_mapped-port_)`

**Explanation** A UDP director/backup/forwarder flow has been created.

**Recommended Action** None required.

### 302025

**Error Message** `%ASA-6-302025: Teardown _stub_ UDP connection for _interface_:_real-address_/_real-port_ to _interface_:_real-address_/_real-port_ duration _hh:mm:ss_ forwarded bytes _bytes_ _reason_`

**Explanation** A UDP director/backup/forwarder flow has been torn down.

**Recommended Action** None required.

### 302026

**Error Message** `%ASA-6-302026: Built _role_ stub ICMP connection for _interface_:_real-address_/_real-port_ (_mapped-address_) to _interface_:_real-address_/_real-port_ (_mapped-address_)`

**Explanation** An ICMP director/backup/forwarder flow has been created.

**Recommended Action** None required.

### 302027

**Error Message** `%ASA-6-302027: Teardown _stub_ ICMP connection for _interface_:_real-address_/_real-port_ to _interface_:_real-address_/_real-port_ duration _hh:mm:ss_ forwarded bytes _bytes_ _reason_`

**Explanation** An ICMP director/backup/forwarder flow has been torn down.

**Recommended Action** None required.

### 302033

**Error Message-1** `%ASA-6-302033: Pre-allocated H323 GUP Connection for faddr _interface_name_:_foreign_ip_address_ to laddr _interface_name_:_local_address_/_local_port_`

**Error Message-2** `%ASA-6-302033: Pre-allocated H323 GUP Connection for faddr _interface_name_:_foreign_ip_address_/_foreign_port_ to laddr _interface_name_:_local_address_`

**Explanation** A GUP connection was started from the foreign address to the local address. The foreign port (outside port) only appears on connections from outside the security device. The local port value (inside port) only appears on connections started on an internal interface.

-   _interface_—The interface name
    
-   _foreign-address_ —IP address of the foreign host
    
-   _foreign-port_ —Port number of the foreign host
    
-   _local-address_ —IP address of the local host
    
-   _local-port_ —Port number of the local host
    

**Recommended Action** None required.

### 302034

**Error Message-1** `%ASA-4-302034: Unable to Pre-allocate H323 GUP Connection for faddr _interface_name_:_foreign_ip_address_ to laddr _interface_name_:_local_ip_address_/_local_port_`

**Error Message-2** `%ASA-4-302034: Unable to Pre-allocate H323 GUP Connection for faddr _interface_name_:_foreign_ip_address_/_foreign_port_ to laddr _interface_name_:_local_ip_address_`

**Explanation** The module failed to allocate RAM system memory while starting a connection or has no more address translation slots available.

-   _interface_—The interface name
    
-   _foreign\_ip\_address_ —IP address of the foreign host
    
-   _foreign\_port_ —Port number of the foreign host
    
-   _local\_ip\_address_ —IP address of the local host
    
-   _local\_port_ —Port number of the local host
    

**Recommended Action** If this message occurs periodically, it can be ignored. If it repeats frequently, contact the Cisco TAC. You can check the size of the global pool compared to the number of inside network clients. Alternatively, shorten the timeout interval of translations and connections. This message may also be caused by insufficient memory; try reducing the amount of memory usage, or purchasing additional memory.

### 302035

**Error Message** `%ASA-6-302035: Built {_inbound | outbound_} SCTP connection _conn_id_ for _outside_interface_:_outside_ip_/_outside_port_ (_mapped_outside_ip_/_mapped_outside_port_)_outside_idfw_user_ to _inside_interface_:_inside_ip_/_inside_port_ (_mapped_inside_ip_/_mapped_inside_port_)_inside_idfw_user_ _port_num_ _rx_ring_num_ [(user)]`

**Explanation** SCTP flow creation is logged when SCTP-state-bypass is not configured.

-   _conn\_id_ —The unique connection ID
    
-   _outside\_interface_ —The interface with the lower security level
    
-   _outside\_ip_ —The IP address of the host on the lower security level side of the ASA
    
-   _outside\_port_ —The port number of the host on the lower security level side of the ASA
    
-   _mapped\_outside\_ip_ —The mapped IP address of the host on the lower security level side of the ASA
    
-   _mapped\_outside\_port_ —The mapped port number of the host on the lower security level side of the ASA
    
-   _outside\_idfw\_user_ —The IDFW username associated with the host on the lower security level side of the ASA
    
-   _outside\_sg\_info_ —The SGT and SG name associated with the host on the lower security level side of the ASA
    
-   _inside\_interface_ —The interface with the higher security level
    
-   _inside\_ip_ —The IP address of the host on the higher security level side of the ASA
    
-   _inside\_port_ —The port number of the host on the higher security level side of the ASA
    
-   _mapped\_inside\_ip_ —The mapped IP address of the host on the higher security level side of the ASA
    
-   _mapped\_inside\_port_ —The mapped port number of the host on the higher security level side of the ASA
    
-   _inside\_idfw\_user_ —The IDFW username associated with the host on the higher security level side of the ASA
    
-   _inside\_sg\_info_ —The SGT and SG name associated with the host on the higher security level side of the ASA
    
-   _user_ —The username associated with the host from where the connection was initiated
    

**Recommended Action** None required.

### 302036

**Error Message** `%ASA-6-302036: Teardown SCTP connection _conn_id_ for _inside_interface_:_inside_ip_address_/_inside_port__outside_idfw_user_ to _outside_interface_:_outside_ip_address_/_outside_port__inside_idfw_user_ duration _time_value_ bytes _bytes_ _reason_string_ _id_port_num_ _rx_ring_num_ [(_user_)]`

**Explanation** SCTP flow deletion is logged when SCTP-state-bypass is not configured.

-   _conn\_id_ —The unique connection ID
-   _outside\_interface_ —The interface with the lower security level
-   _outside\_ip\_address_ —The IP address of the host on the lower security level side of the ASA
-   _outside\_port_ —The port number of the host on the lower security level side of the ASA
-   _outside\_idfw\_user_ —The IDFW username associated with the host on the lower security level side of the ASA
-   _inside\_interface_ —The interface with the higher security level
-   _inside\_ip\_address_ —The IP address of the host on the higher security level side of the ASA
-   _inside\_port_ —The port number of the host on the higher security level side of the ASA
-   _inside\_idfw\_user_ —The IDFW username associated with the host on the higher security level side of the ASA
-   _user_ —The username associated with the host from where the connection was initiated
-   _time\_value_ —The amount of the flow stayed alive in hh:mm:ss
-   _bytes_ —The number of bytes passed on the flow
-   _reason\_string_ —The reason the connection was torn down

**Recommended Action** None required.

### 302037

**Error Message** `%ASA-6-302037: Built {inbound|outbound} IPINIP connection _conn_id_ from _outside_interface_:_outside_ip_/{_outside_mapped_ip|outside_port_} _outside_idfw_user_ to _inside_interface_name_:_inside_ip_/{_inside_mapped_ip|inside_port_} _inside_idfw_user_ [(_user_)]`

**Explanation** IPINIP flow has been created.

-   _conn\_id_ —The unique connection ID
-   _outside\_interface_ —The interface with the lower security level
-   _outside\_ip_ —The IP address of the host on the lower security level side of the ASA
-   _outside\_port_ —The port number of the host on the lower security level side of the ASA
-   _mapped\_outside\_ip_ —The mapped IP address of the host on the lower security level side of the ASA
-   _mapped\_outside\_port_ —The mapped port number of the host on the lower security level side of the ASA
-   _outside\_idfw\_user_ —The IDFW username associated with the host on the lower security level side of the ASA
-   _outside\_sg\_info_ —The SGT and SG name associated with the host on the lower security level side of the ASA
-   _inside\_interface_ —The interface with the higher security level
-   _inside\_ip_ —The IP address of the host on the higher security level side of the ASA
-   _inside\_port_ —The port number of the host on the higher security level side of the ASA
-   _mapped\_inside\_ip_ —The mapped IP address of the host on the higher security level side of the ASA
-   _mapped\_inside\_port_ —The mapped port number of the host on the higher security level side of the ASA
-   _inside\_idfw\_user_ —The IDFW username associated with the host on the higher security level side of the ASA
-   _inside\_sg\_info_ —The SGT and SG name associated with the host on the higher security level side of the ASA
-   _user_ —The username associated with the host from where the connection was initiated

**Recommended Action** None required.

### 302038

(Inbound flow)**Error Message 1** `%ASA-6-302038: Teardown IPINIP connection _conn_id_ for _inside_interface_:_inside_ip_/_inside_port__outside_idfw_user_ to _outside_interface_:_outside_ip_/_outside_port__inside_idfw_user_ duration _time_value_ bytes _bytes_ [(_user_)]`

(Outbound flow) **Error Message 2** `%ASA-6-302038: Teardown IPINIP connection _conn_id_ for _outside_interface_:_outside_ip_/_outside_port__outside_idfw_user_ to _inside_interface_:_inside_ip_/_inside_port__inside_idfw_user_ duration _time_value_ bytes _bytes_ [(_user_)]`

**Explanation** An IPINIP flow has been torn down.

-   _conn\_id_ —The unique connection ID
-   _outside\_interface_ —The interface with the lower security level
-   _outside\_ip_ —The IP address of the host on the lower security level side of the ASA
-   _outside\_port_ —The port number of the host on the lower security level side of the ASA
-   _outside\_idfw\_user_ —The IDFW username associated with the host on the lower security level side of the ASA
-   _outside\_sg\_info_ —The SGT and SG name associated with the host on the lower security level side of the ASA
-   _inside\_interface_ —The interface with the higher security level
-   _inside\_ip_ —The IP address of the host on the higher security level side of the ASA
-   _inside\_port_ —The port number of the host on the higher security level side of the ASA
-   _inside\_idfw\_user_ —The IDFW username associated with the host on the higher security level side of the ASA
-   _inside\_sg\_info_ —The SGT and SG name associated with the host on the higher security level side of the ASA
-   _user_ —The username associated with the host from where the connection was initiated
-   _time_ —The amount of the flow stayed alive in hh:mm:ss
-   _bytes_ —The number of bytes passed on the flow

**Recommended Action** None required.

### 302302

**Error Message** `%ASA-3-302302: _ACL=deny;no_sa_created_`

**Explanation** IPsec proxy mismatches have occurred. Proxy hosts for the negotiated SA correspond to a deny access-list command policy.

**Recommended Action** Check the access-list command statement in the configuration. Contact the administrator for the peer.

### 302303

**Error Message** `%ASA-6-302303: Built TCP state-bypass connection _conn_id_ from _initiator_interface_:_real_ip_/_real_port_ (_mapped_ip_/_mapped_port_) to _responder_interface_:_real_ip_/_real_port_ (_mapped_ip_/_mapped_port_)`

**Explanation** A new TCP connection has been created, and this connection is a TCP-state-bypass connection. This type of connection bypasses all the TCP state checks and additional security checks and inspections.

**Recommended Action** If you need to secure TCP traffic with all the normal TCP state checks as well as all other security checks and inspections, you can use the no set connection advanced-options tcp-state-bypass command to disable this feature for TCP traffic.

### 302304

**Error Message** `%ASA-6-302304: Teardown TCP state-bypass connection _conn_id_ from _initiator_interface_:_ip_/_port__user_ to _responder_interface_:_ip_/_port__user_ duration _duration_ bytes _bytes__teardown reason_` .

**Explanation** A new TCP connection has been torn down, and this connection is a TCP-state-bypass connection. This type of connection bypasses all the TCP state checks and additional security checks and inspections.

-   _duration_ —The duration of the TCP connection
-   _bytes_ —The total number of bytes transmitted over the TCP connection
-   _teardown reason_ —The reason for the teardown of the TCP connection

**Recommended Action** If you need to secure TCP traffic with all the normal TCP state checks as well as all other security checks and inspections, you can use the no set connection advanced-options tcp-state-bypass command to disable this feature for TCP traffic.

### 302305

**Error Message** `%ASA-6-302305: Built SCTP state-bypass connection _conn_id_ from _outside_interface_:_outside_ip_/_outside_port_ (_mapped_outside_ip_/_mapped_outside_port_)_outside_idfw_user_ to _outside_sg_info_:_inside_interface_/_inside_ip_ (_inside_port_ /_mapped_inside_ip_)_mapped_inside_port_ _inside_idfw_user_ _inside_sg_info_`

**Explanation** SCTP flow creation is logged when SCTP-state-bypass is configured.

-   _conn\_id_ —The unique connection ID
-   _outside\_interface_ —The interface with the lower security level
-   _outside\_ip_ —The IP address of the host on the lower security level side of the ASA
-   _outside\_port_ —The port number of the host on the lower security level side of the ASA
-   _mapped\_outside\_ip_ —The mapped IP address of the host on the lower security level side of the ASA
-   _mapped\_outside\_port_ —The mapped port number of the host on the lower security level side of the ASA
-   _outside\_idfw\_user_ —The IDFW username associated with the host on the lower security level side of the ASA
-   _outside\_sg\_info_ —The SGT and SG name associated with the host on the lower security level side of the ASA
-   _inside\_interface_ —The interface with the higher security level
-   _inside\_ip_ —The IP address of the host on the higher security level side of the ASA
-   _inside\_port_ —The port number of the host on the higher security level side of the ASA
-   _mapped\_inside\_ip_ —The mapped IP address of the host on the higher security level side of the ASA
-   _mapped\_inside\_port_ —The mapped port number of the host on the higher security level side of the ASA
-   _inside\_idfw\_user_ —The IDFW username associated with the host on the higher security level side of the ASA
-   _inside\_sg\_info_ —The SGT and SG name associated with the host on the higher security level side of the ASA

**Recommended Action** None required.

### 302306

**Error Message** `%ASA-6-302306: Teardown SCTP state-bypass connection _conn_id_ from _outside_interface_:_outside_ip_/_outside_port__outside_idfw_user_ to _outside_sg_info_:_inside_interface_/_inside_ip__inside_port_ duration _inside_idfw_user_ bytes _inside_sg_info_ _time_ _bytes_ _reason_`

**Explanation** SCTP flow deletion is logged when SCTP-state-bypass is configured.

-   _conn\_id_ —The unique connection ID
-   _outside\_interface_ —The interface with the lower security level
-   _outside\_ip_ —The IP address of the host on the lower security level side of the ASA
-   _outside\_port_ —The port number of the host on the lower security level side of the ASA
-   _outside\_idfw\_user_ —The IDFW username associated with the host on the lower security level side of the ASA
-   _outside\_sg\_info_ —The SGT and SG name associated with the host on the lower security level side of the ASA
-   _inside\_interface_ —The interface with the higher security level
-   _inside\_ip_ —The IP address of the host on the higher security level side of the ASA
-   _inside\_port_ —The port number of the host on the higher security level side of the ASA
-   _inside\_outside\_ip_ —The mapped IP address of the host on the higher security level side of the ASA
-   _inside\_idfw\_user_ —The IDFW username associated with the host on the higher security level side of the ASA
-   _inside\_sg\_info_ —The SGT and SG name associated with the host on the higher security level side of the ASA
-   _time_ —The amount of time that the flow stayed alive in hh:mm:ss
-   _bytes_ —The number of bytes passed on the flow
-   _reason_ —The reason the connection was torn down

**Recommended Action** None required.

### 4302310

**Error Message** `%ASA-4-302310: SCTP _packet_ received from _src_ifc_:_src_ip_/_src_port_ to _dst_ifc_:_dst_ip_/_dst_port_ contains unsupported Hostname Parameter.`

**Explanation** A init/init-ack packet is received with the hostname parameter.

-   packet init/init-ack—The message carrying the hostname parameter
-   src-ifc— Indicates the ingress interface
-   src-ip/src-port— Indicates the Source IP and Port in the packet
-   dst-ifc—Indicates the egress interface
-   dst\_ip/dst\_port—Indicates the Source IP and Port in the packet

**Recommended Action** Use the real IP addresses of endpoints rather than the hostname. Disable the hostname parameter.

### 302311

**Error Message** `%ASA-4-302311: Failed to create a new _protocol_ connection from _ingress_interface_:_source_ip_/_source_port_ to _egress_interface_:_destination_ip_/_destination_port_ due to application cache memory allocation failure. The app-cache memory threshold level is _threshold%_ and threshold check is _enabled/disabled_`

**Explanation** A new connection could not be created due to app-cache memory allocation failure. The failure could be due to system running out of memory or exceeding app-cache memory threshold.

-   protocol—The name of the protocol used to create the connection
-   ingress interface—The interface name
-   source IP—The source IP address
    
-   source port—The source port number
    
-   egress interface—The interface name
    
-   destination IP— The destination address
    
-   destination port—The destination port number
    
-   threshold%—The percentage value of memory threshold
    
-   enabled/disabled—app-cache memory threshold feature enabled/disabled
    

**Recommended Action** Disable memory intensive features on the device or reduce the number of through-the-box connections.

### 303002

**Error Message** `%ASA-6-303002: FTP connection from _src_ifc_:_src_ip_/_src_port_ to _dst_ifc_:_dst_ip_/_dst_port_, user_username_ _action_ file _filename_`

**Explanation** A client has uploaded or downloaded a file from the FTP server.

-   src\_ifc—The interface where the client resides.
-   src\_ip—The IP address of the client.
-   src\_port—The client port.
-   dst\_ifc—The interface where the server resides.
-   dst\_ip—The IP address of the FTP server.
-   dst\_port—The server port.
-   username—The FTP username.
-   action—The stored or retrieved actions.
-   filename—The file stored or retrieved.

**Recommended Action** None required.

### 303004

**Error Message** `%ASA-5-303004: FTP _cmd_string_ command unsupported - failed strict inspection, terminating connection from _source_interface_:_source_address_/_source_port_ to _dest_interface_:_dest_address_/_dest_interface_`

**Explanation** Strict FTP inspection on FTP traffic has been used, and an FTP request message contains a command that is not recognized by the device.

**Recommended Action** None required.

### 303005

**Error Message** `%ASA-5-303005: Strict FTP inspection matched _match_string_ in policy-map _policy-name_, _action_string_ from _src_ifc_:_sip_/_sport_ to _dest_ifc_:_dip_/_dport_`

**Explanation** When FTP inspection matches any of the following configured values: filename, file type, request command, server, or username, then the action specified by the _action\_string_ in this message occurs.

-   _match\_string_ —The match clause in the policy map
-   policy-name—The policy map that matched
-   action\_string—The action to take; for example, Reset Connection
-   src\_ifc—The source interface name
-   sip—The source IP address
-   sport—The source port
-   dest\_ifc—The destination interface name
-   dip—The destination IP address
-   dport—The destination port

**Recommended Action** None required.

### 304001

**Error Message** `%ASA-5-304001: _URL__user@source_address__idfw_user_ Accessed _URL_ _dest_address_:_url_`

**Explanation** The specified host tried to access the specified URL If you enable the HTTP inspection with custom HTTP policy map, the following possibilities are seen.When the packet of GET request does not have the hostname parameter, instead of printing the URI, it prints the following message:%ASA-5-304001: client IP Accessed URL server ip:Hostname not present URI: URIIf a large URI which cannot be printed in a single syslog, you can print partial wherever it is being chopped down.For instance, when the URL is to be divided into multiple chunks and logged, the following message is printed:%ASA-5-304001: client IP Accessed URL server ip: http(/ftp)://hostname/URI\_CHUNK1 partial%ASA-5-304001: client IP Accessed URL server ip: partial URI\_CHUNK1 partial............%ASA-5-304001: client IP Accessed URL server ip: partial URI\_CHUNKnThe limit for URI is 1024 bytes.If the current packet contains partial URI at the beginning or end, use the same logic as explained above.

**Recommended Action** None required.

### 304002

**Error Message** `%ASA-5-304002: Access denied URL _url_ SRC _(user)__(sip)__(user)_ DEST _dip_ on interface _int_name_`

**Explanation** Access from the source address to the specified URL or FTP site was denied.

**Recommended Action** None required.

### 304003

**Error Message** `%ASA-3-304003: URL Server _IP_address_ timed out URL _url_`

**Explanation** A URL server timed out.

**Recommended Action** None required.

### 304004

**Error Message** `%ASA-6-304004: URL Server _IP_address_ request failed URL _url_`

**Explanation** A Websense server request failed.

**Recommended Action** None required.

### 304005

**Error Message** `%ASA-7-304005: URL Server _IP_address_ request pending URL _url_`

**Explanation** A Websense server request is pending.

**Recommended Action** None required.

### 304006

**Error Message** `%ASA-3-304006: URL Server _IP_address_ not responding`

**Explanation** The Websense server is unavailable for access, and the ASA attempts to either try to access the same server if it is the only server installed, or another server if there is more than one.

**Recommended Action** None required.

### 304007

**Error Message** `%ASA-2-304007: URL Server not responding, ENTERING ALLOW mode`

**Explanation** You used the allow option of the filter command, and the Websense servers are not responding. The ASA allows all web requests to continue without filtering while the servers are not available.

**Recommended Action** None required.

### 304008

**Error Message** `%ASA-2-304008: LEAVING ALLOW mode, URL Server is up`

**Explanation** You used the allow option of the filter command, and the ASA receives a response message from a Websense server that previously was not responding. With this response message, the ASA exits the allow mode, which enables the URL filtering feature again.

**Recommended Action** None required.

### 304009

**Error Message** `%ASA-7-304009: Ran out of buffer blocks specified by url-block command`

**Explanation** The URL pending buffer block is running out of space.

**Recommended Action** Change the buffer block size by entering the url-block block block\_size command_._

### 305005

**Error Message** `%ASA-3-305005: No translation group found for _protocol_ src _interface_name_: _source_address_/_source_port_ [(_idfw_user_ )] dst _interface_name_: _dest_address_ /_dest_port_ [(_idfw_user_ )]`

**Explanation** A packet does not match any of the outbound nat command rules. If NAT is not configured for the specified source and destination systems, the message will be generated frequently.

**Recommended Action** This message indicates a configuration error. If dynamic NAT is desired for the source host, ensure that the nat command matches the source IP address. If static NAT is desired for the source host, ensure that the local IP address of the static command matches. If no NAT is desired for the source host, check the ACL bound to the NAT 0 ACL.

### 305006

**Error Message** `%ASA-3-305006: {outbound static|identity|portmap|regular) translation creation failed for _protocol_ src _interface_name_:_source_address_/_source_port_ [(_idfw_user_ )] dst _interface_name_:_dest_address_/_dest_port_ [(_idfw_user_ )]`

**Explanation** The ICMP error inspection was enabled and the following conditions were met:

-   There was a connection established through the device with forward and reverse flows having different protocols. For example, forward flow is UDP or TCP, reverse flow is ICMP. The switch in protocols occurs when either the receiver or any intermediary device in the path returns ICMP error messages, for example type 3 code 3.
    
-   There was a dynamic NAT/PAT statement that matched the packets of the reverse flow and failed to translate the outer header IP addresses because the device does not apply PAT to all ICMP message types; it only applies PAT ICMP echo and echo-reply packets (types 8 and 0).
    

**Recommended Action** None required.

### 305007

**Error Message** `%ASA-6-305007: _addrpool_free_(): Orphan IP _IP_address_ on interface _interface_number_`

**Explanation** The ASA has attempted to translate an address that it cannot find in any of its global pools. The ASA assumes that the address was deleted and drops the request.

**Recommended Action** None required.

### 305008

**Error Message** `%ASA-3-305008: Detecting free unallocated global IP _IP__address_ on interface _interface_name_`

**Explanation** The ASA kernel detected an inconsistency condition when trying to free an unallocated global IP address back to the address pool. This abnormal condition may occur if the ASA is running a Stateful Failover setup, and some of the internal states are momentarily out of sync between the active unit and the standby unit. This condition is not catastrophic, and the synchronization recovers automatically.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 305009

**Error Message** `%ASA-6-305009: Built _{dynamic|static}_ translation from _interface_name[(acl-name)]_:_real_address__idfw_user_ to _interface__name_:_mapped_address_`

**Explanation** An address translation slot was created. The slot translates the source address from the local side to the global side. In reverse, the slot translates the destination address from the global side to the local side.

**Recommended Action** None required.

### 305010

**Error Message** `%ASA-6-305010: Teardown _{dynamic|static}_ translation from _interface_name_:_real_address_ _idfw_user_ to _interface__name_:_mapped_address_ duration _time_`

**Explanation** The address translation slot was deleted.

**Recommended Action** None required.

### 305011

**Error Message** `%ASA-6-305011: Built _{dynamic|static}_ _{TCP|UDP|ICMP}_ translation from _interface_name_:_real_address_/_real_port__idfw_user_ to _interface__name_:_mapped_address_/_mapped_port_`

**Explanation** A TCP, UDP, or ICMP address translation slot was created. The slot translates the source socket from the local side to the global side. In reverse, the slot translates the destination socket from the global side to the local side.

**Recommended Action** None required.

### 305012

**Error Message** `%ASA-6-305012: Teardown _interface_name_ _acl-name_ translation from _real_address_:_real_port_/_real_ICMP_ID__idfw_user_ to _interface_name__mapped_address_:_mapped_port_/_mapped_ICMP_ID_ duration _time_`

**Explanation** The address translation slot was deleted.

**Recommended Action** None required.

### 305013

(ICMP) **Error Message** `%ASA-5-305013: Asymmetric NAT rules matched for forward and reverse flows; Connection for icmp src _interface_name_:_source_ip_address__source_user_ dst _interface_name_:_destination_ip_address__destination_user_ (type _type_, code _code_) denied due to NAT reverse path failure`

(TCP, UDP, SCTP) **Error Message** `%ASA-5-305013: Asymmetric NAT rules matched for forward and reverse flows; Connection for "protocol" src _interface_name_:_source_ip_address_/_source_port__source_user_ dst _interface_name_:_destination_ip_address_/_destination_port__destination_user_ denied due to NAT reverse path failure`

| ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)

**Note** | ___

Protocol in this error message can be TCP, UDP, or SCTP.

___ |
|--------|--------------------------------------------------------------|

(Any Protocol) **Error Message** `%ASA-5-305013: Asymmetric NAT rules matched for forward and reverse flows; Connection for protocol _protocol_name_ src _interface_name_:_source_ip_address__source_user_ dst _interface_name_:_destination_ip_address__destination_user_ denied due to NAT reverse path failure`

**Explanation** An attempt to connect to a mapped host using its actual address was rejected.

**Recommended Action** When not on the same interface as the host using NAT, use the mapped address instead of the actual address to connect to the host. In addition, enable the inspect command if the application embeds the IP address.

### 305014

**Error Message** `%ASA-6-305014: Allocated _num_of_blocks_ block of ports for translation from _real_interface_:_real_host_ip_ to _real_dest_interface_:_real_dest_ip_/_real_dest_port_start_-_real_dest_port_end_`

**Explanation** When CGNAT “block-allocation” is configured, this syslog will be generated on allocation of a new port block.

**Recommended Action** None.

### 305015

**Error Message** `%ASA-6-305015: Released _block_size_ block of ports for translation from _real_interface_:_real_host_ip_ to _real_destination_interface_:_real_dest_ip_/_port_start_-_port_end_`

**Explanation** When CGNAT “block-allocation” is configured, this syslog will be generated on release of an allocated port block.

**Recommended Action** None.

### 305016

**Error Message-1** `%ASA-3-305016: Unable to create _protocol_ connection from _source_interface_name_:_source_ip_address_/_source_port_ to _destination_interface_name_:_destination_ip_/_destination_port_ due to reaching per-host PAT port block limit of _threshold-limit_.`

**Error Message-2** `%ASA-3-305016: Unable to create _protocol_ connection from _source_interface_name_:_source_ip_address_/_source_port_ to _destination_interface_name_:_destination_ip_address_/_destination_port_ due to port block exhaustion in PAT pool '_pool_name_' IP _pool_ip_address_.`

**Error Message-3** `%ASA-3-305016: Port blocks exhausted in PAT pool '_pool_name_' IP _pool_address_. Unable to create connection.`

**Explanation** The maximum port blocks per host limit has been reached for a host or the port blocks have been exhausted.

-   _reason_ —May be one of the following:
    -   reaching per-host PAT port block limit of _value_
    -   port block exhaustion in PAT pool

**Recommended Action** For reaching the per-host PAT port block limit, review the maximum blocks per host limit by entering the following command:

```scss
xlate block-allocation maximum-per-host 4
```

For the port block exhaustion in the PAT pool, we recommend increasing the pool size. Also, review the block size by entering the following command:

```scss
xlate block-allocation size 512
```

### 305017

**Error Message** `%ASA-3-305017: Pba-interim-logging: Active _Active_ICMP_ block of ports for translation from _source_:_device_IP_ to _destination_:_device_IP_/_Active_Port_-_Block_`

**Explanation** When CGNAT interim logging feature is turned on. This syslog specifies the Active Port Block from a particular source IP address to a destination IP address at that time.

**Recommended Action**None.

### 305018

**Error Message** `%ASA-6-305018: MAP translation from _src_ifc_:_src_ip_/_src_port_-_dst_ifc_:_dst_ip_/_dst_port_ to _src_ifc_:_translated_src_ip_/_src_port_-_dst_ifc_:_translated_dst_ip_/_dst_port_`

**Explanation** MAP style address translation has been applied to a connection being established, their source and destination have been translated

Example:

```ruby
%ASA-6-305018: MAP translation from inside:2001:DB8:0000:0000:0000:0000:0000:0002/57964-outside:2001:DB8:FFFF:0000:0000:0000:0000:0001/22 to inside:192.168.101.210/57964-outside:192.168.100.203/22
```

**Recommended Action**None.

### 305019

**Error Message** `%ASA-3-305019: MAP node address _ip_/_port_ has inconsistent Port Set ID encoding`

**Explanation**A packet has an address that matches MAP basic mapping rules (meaning it is meant to be translated) but the Port Set ID encoded within the address is inconsistent (per RFC7599). This could be due to a software fault on the MAP node where this packet originates.

Example

```ruby
%ASA-3-305019: MAP node address 2001:DB8:0000:FFFF:0000:0000:0000:0002/57964 has inconsistent Port Set ID encoding
```

**Recommended Action**None.

### 305020

**Error Message** `%ASA-3-305020: MAP node with address _ip_ is not allowed to use port _port_`

**Explanation** A packet has an address that matches MAP basic mapping rules (meaning it is meant to be translated) but the associated port does not fall within the range allocated to that address. This likely means there is misconfiguration on the MAP node where this packet originates.

Example:

```vbnet
%ASA-3-305020: MAP node with address 2001:DB8:0000:0000:0000:0000:0000:0002 is not allowed to use port 37964\n
```

**Recommended Action**None.

### 305021

**Error Message** `%ASA-4-305021: Ports exhausted in pre-allocated PAT pool IP _mapped_ip_address_ for host _real_host_ip_. Allocating from new PAT pool IP _mapped_ip_address_`

**Explanation** This message is generated when all ports are exhausted in the sticky IP on a cluster node and allocation moves to the next available IP with free ports.

**Example:**

`%ASA-4-305021: Ports exhausted in pre-allocated PAT pool IP 174.0.1.1 for host 192.168.1.20. Allocating from new PAT pool IP 174.0.1.2.`

**Recommended Action** None.

### 305022

**Error Message** `%ASA-4-305022: Cluster unit _unit_name_ has been allocated _num_of_port_blocks_ port-blocks from _ip_address_ on interface _interface_name_ for PAT usage. All units should have at least _min_num_of_port_blocks_ port-blocks`

**Explanation** This message is generated on a node when it joins cluster and does not get any or unequal share of port blocks.

**Examples**

`%ASA-4-305022: Cluster unit ASA-4 has been allocated 0 port blocks for PAT usage. All units should have at least 32 port blocks.`

`%ASA-4-305022: Cluster unit ASA-4 has been allocated 12 port blocks for PAT usage. All units should have at least 32 port blocks.`

**Recommended Action** None.

### 305023

**Error Message** `%ASA-3-305023: Unable to create TCP connection from inside:_<ip/port>_ to outside:_<ip/port>_ due to IP port block exhaustion in PAT pool _pool_name_ IP _port_address_.`

**Explanation** This message is generated when the device could not create a new connection because the PAT pool was exhausted.

**Recommended Action** None.

### 308001

**Error Message** `%ASA-6-308001: Console enable password incorrect for _number_ tries (from _IP_address_)`

**Explanation** This is a Secure Firewall ASA management message. This message appears after the specified number of times a user incorrectly types the password to enter privileged mode. The maximum is three attempts.

**Recommended Action** Verify the password and try again.

### 308002

**Error Message** `%ASA-4-308002: static _global_address_ _inside_address_ netmask _netmask_ overlapped with _global_address_ _inside_address_ netmask _netmask_`

**Explanation** The IP addresses in one or more static command statements overlap. global\_address is the global address, which is the address on the lower security interface, and inside\_address is the local address, which is the address on the higher security-level interface.

**Recommended Action** Use the show static command to view the static command statements in your configuration and fix the commands that overlap. The most common overlap occurs if you specify a network address such as 10.1.1.0, and in another static command you specify a host within that range, such as 10.1.1.5.

### 308003

**Error Message** `%ASA-4-308003: WARNING: The enable password is not configured`

**Explanation** When entering enable mode (privilege level 2 or greater), you are forced to configure the enable password for privilege level 15 when the enable password is not already set.

**Recommended Action** Set the enable password. The permitted length of password is between 3 and 15.

### 308004

**Error Message** `%ASA-4-308004: The enable password has been configured by user _admin_`

**Explanation** You have configured the enable password for the first time. This message will not be displayed when you are modifying an existing enable password.

**Recommended Action** None.

### 311001

**Error Message** `%ASA-6-311001: LU loading standby start`

**Explanation** Stateful Failover update information was sent to the standby Secure Firewall ASA when the standby Secure Firewall ASA is first to be online.

**Recommended Action** None required.

### 311002

**Error Message** `%ASA-6-311002: LU loading standby end`

**Explanation** Stateful Failover update information stopped sending to the standby Secure Firewall ASA.

**Recommended Action** None required.

### 311003

**Error Message** `%ASA-6-311003: LU recv thread up`

**Explanation** An update acknowledgment was received from the standby Secure Firewall ASA.

**Recommended Action** None required.

### 311004

**Error Message** `%ASA-6-311004: LU xmit thread up`

**Explanation** A Stateful Failover update was transmitted to the standby Secure Firewall ASA.

**Recommended Action** None required.

### 312001

**Error Message** `%ASA-6-312001: RIP hdr failed from _IP_address_: cmd=_string_, version=_number_, domain=_string_ on interface _interface_name_`

**Explanation** The Secure Firewall ASA received a RIP message with an operation code other than reply, the message has a version number different from what is expected on this interface, and the routing domain entry was nonzero. Another RIP device may not be configured correctly to communicate with the Secure Firewall ASA.

**Recommended Action** None required.

### 313001

**Error Message** `%ASA-3-313001: Denied ICMP type=_number_, code=_code_ from _IP_address_ on interface _interface_name_`

**Explanation** When using the icmp command with an access list, if the first matched entry is a permit entry, the ICMP packet continues processing. If the first matched entry is a deny entry, or an entry is not matched, the Secure Firewall ASA discards the ICMP packet and generates this message. The icmp command enables or disables pinging to an interface. With pinging disabled, the Secure Firewall ASA cannot be detected on the network. This feature is also referred to as configurable proxy pinging.

**Recommended Action** Contact the administrator of the peer device.

### 313004

**Error Message-1** `%ASA-4-313004: Denied ICMP type=_icmp_type_, from laddr _source_ip_address_ on interface _interface_name_ to _destination_ip_address_: no matching session`

**Error Message-2** `%ASA-4-313004: Denied ICMP type=_icmp_type_, from laddr _source_ip_address_ on interface shared _physical_interface_name_ to _destination_ip_address_: no matching session`

**Explanation** ICMP packets were dropped by the Secure Firewall ASA because of security checks added by the stateful ICMP feature that are usually either ICMP echo replies without a valid echo request already passed across the Secure Firewall ASA or ICMP error messages not related to any TCP, UDP, or ICMP session already established in the Secure Firewall ASA.

**Recommended Action** None required.

### 313005

**Error Message** `%ASA-4-313005: No matching connection for ICMP error message: _icmp_msg_info_ on _interface_name_ interface. Original IP payload: _embedded_frame_info_icmp_msg_info=_.`

**Explanation** ICMP error packets were dropped by the Secure Firewall ASA because the ICMP error messages are not related to any session already established in the Secure Firewall ASA.

**Recommended Action** Review the Original IP Payload information embedded in the message. Inspect the original source and destination and verify if it is a valid packet in your network. If the packet is valid and as expected, you can ignore the message. If the cause is an attack, you can deny the host by using ACLs.

### 313008

**Error Message** `%ASA-3-313008: Denied IPv6-ICMP type=_number_, code=_code_ from _IP_address_ on interface _interface_name_`

**Explanation** When using the icmp command with an access list, if the first matched entry is a permit entry, the ICMPv6 packet continues processing. If the first matched entry is a deny entry, or an entry is not matched, the Secure Firewall ASA discards the ICMPv6 packet and generates this message.

The icmp command enables or disables pinging to an interface. When pinging is disabled, the Secure Firewall ASA is undetectable on the network. This feature is also referred to as “configurable proxy pinging.”

**Recommended Action** Contact the administrator of the peer device.

### 313009

**Error Message** `%ASA-4-313009: Denied invalid ICMP code _icmp_code_, for _src_ifc_:_src_address_/_src_port_ (_mapped_src_address_/_mapped_src_port_) to _dest_ifc_:_dest_address_/_dest_port_ (_mapped_dest_address_/_mapped_dest_port_) [(_user_)], ICMP id icmp_id, ICMP type _icmp_type_`

**Explanation** An ICMP echo request/reply packet was received with a malformed code(non-zero).

**Recommended Action** If it is an intermittent event, no action is required. If the cause is an attack, you can deny the host using the ACLs.

### 314001

**Error Message** `%ASA-6-314001: Pre-allocate RTSP UDP backconnection for _src_intf_:_src_IP_ to _dst_intf_:_dst_IP_/_dst_port._`

**Explanation** The Secure Firewall ASA opened a UDP media channel for the RTSP client that was receiving data from the server.

-   _src\_intf_ —Source interface name
-   _src\_IP_ —Source interface IP address
-   _dst\_intf_ —Destination interface name
-   _dst\_IP_ —Destination IP address
-   _dst\_port_ —Destination port

**Recommended Action** None required.

### 314002

**Error Message** `%ASA-6-314002: RTSP failed to allocate UDP media connection from _src_intf_:_src_IP_ to _dst_intf_:_dst_IP_/_dst_port_ reason: _reason_string._`

**Explanation** The Secure Firewall ASA cannot open a new pinhole for the media channel.

-   _src\_intf_ —Source interface name
-   _src\_IP_ —Source interface IP address
-   _dst\_intf_ —Destination interface name
-   _dst\_IP_ —Destination IP address
-   _dst\_port_ —Destination port
-   _reason\_string_ —Pinhole already exists/Unknown

**Recommended Action** If the reason is unknown, check the free memory available by running the show memory command, or the number of connections used by running the show conn command, because the Secure Firewall ASA is low on memory.

### 314003

**Error Message** `%ASA-6-314003: Dropped RTSP traffic from _src_intf_:_src_ip_, reason: _reason_`

**Explanation** The RTSP message violated the user-configured RTSP security policy, either because it contains a port from the reserve port range, or it contains a URL with a length greater than the maximum limit allowed.

-   _src\_intf_ —Source interface name
-   _src\_IP_ —Source interface IP address
-   _reason_ —The reasons may be one of the following:

\- Endpoint negotiating media ports in the reserved port range from 0 to 1024

\- URL length of _url length_ bytes exceeds the maximum _url length limit_ bytes

**Recommended Action** Investigate why the RTSP client sends messages that violate the security policy. If the requested URL is legitimate, you can relax the policy by specifying a longer URL length limit in the RTSP policy map.

### 314004

**Error Message** `%ASA-6-314004: RTSP client _src_intf_:_src_IP_ accessed RTSP URL _RTSP_URL_`

**Explanation** An RTSP client tried to access an RTSP server.

-   _src\_intf_ —Source interface name
-   _src\_IP_ —Source interface IP address
-   _RTSP URL_ —RTSP server URL

**Recommended Action** None required.

### 314005

**Error Message** `%ASA-6-314005: RTSP client _src_intf_:_src_IP_ denied access to RTSP URL _RTSP_URL._`

**Explanation** An RTSP client tried to access a prohibited site.

-   _src\_intf_ —Source interface name
-   _src\_IP_ —Source interface IP address
-   _RTSP\_URL_ —RTSP server URL

**Recommended Action** None required.

### 314006

**Error Message** `%ASA-6-314006: RTSP client _src_intf_:_src_IP_ exceeds configured rate limit of _rate_ for _request_method_ message`

**Explanation** A specific RTSP request message exceeded the configured rate limit of RTSP policy.

-   _src\_intf_ —Source interface name
-   _src\_IP_ —Source interface IP address
-   _rate_ —Configured rate limit
-   _request\_method_ —Type of request message

**Recommended Action** Investigate why the specific RTSP request message from the client exceeded the rate limit.

### 315004

**Error Message** `%ASA-3-315004: Fail to establish SSH session because RSA host key retrieval failed.`

**Explanation** The ASA cannot find the RSA host key, which is required for establishing an SSH session. The ASA host key may be absent because it was not generated or because the license for this ASA does not allow DES or 3DES encryption.

**Recommended Action** From the ASA console, enter the show crypto key mypubkey rsa command to verify that the RSA host key is present. If the host key is not present, enter the show version command to verify that DES or 3DES is allowed. If an RSA host key is present, restart the SSH session. To generate the RSA host key, enter the crypto key mypubkey rsa command.

### 315011

**Error Message-1** `%ASA-6-315011: SSH session from _remote_ip_address_ on interface _interface_name_ for user \'_user_name_\' terminated normally`

**Error Message-2** `%ASA-6-315011: SSH session from _remote_ip_address_ on interface _interface_name_ for user \'_user_name_\' terminated`

**Error Message-3** `%ASA-6-315011: SSH session from _remote_ip_address_ on interface _interface_name_ for user \'_user_name_\' disconnected by SSH server, reason: \'_reason_string_\' (_reason_state_)`

**Explanation** An SSH session has ended. If a user enters quit or exit, the terminated normally message appears. The username is hidden when invalid or unknown, but appears when valid or the no logging hide username command has been configured. If the session disconnected for another reason, the text describes the reason. The following table lists the possible reasons why a session is disconnected.

|      Text String       |                                                                 Explanation                                                                  |                                                                                                                                                                         Action                                                                                                                                                                          |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     Bad checkbytes     |                                    A mismatch was detected in the check bytes during an SSH key exchange.                                    |                                                                                                                                                                Restart the SSH session.                                                                                                                                                                 |
|    CRC check failed    |            The CRC value computed for a particular packet does not match the CRC value embedded in the packet; the packet is bad.            |                                                                                                                                                None required. If this message persists, call Cisco TAC.                                                                                                                                                 |
|   Decryption failure   |                                     Decryption of an SSH session key failed during an SSH key exchange.                                      |                                                                                                                                                          Check the RSA host key and try again.                                                                                                                                                          |
|      Format error      |                                  A nonprotocol version message was received during an SSH version exchange.                                  |                                                                                                                                               Check the SSH client, to ensure it is a supported version.                                                                                                                                                |
|     Internal error     | This message indicates either an error internal to SSH on the ASA or an RSA key may not have been entered on the ASA or cannot be retrieved. | From the ASA console, enter the show crypto key mypubkey rsa command to verify that the RSA host key is present. If the host key is not present, enter the show version command to verify that DES or 3DES is allowed. If an RSA host key is present, restart the SSH session. To generate the RSA host key, enter the crypto key mypubkey rsa command. |
|  Invalid cipher type   |                                               The SSH client requested an unsupported cipher.                                                |                                                                                                     Enter the show version command to determine which features your license supports, then reconfigure the SSH client to use the supported cipher.                                                                                                      |
| Invalid message length |        The length of SSH message arriving at the ASA exceeds 262,144 bytes or is shorter than 4096 bytes. The data may be corrupted.         |                                                                                                                                                                     None required.                                                                                                                                                                      |
|  Invalid message type  |                                The ASA received a non-SSH message, or an unsupported or unwanted SSH message.                                |                                                             Check whether the peer is an SSH client. If it is a client supporting SSHv1, and this message persists, from the ASA serial console enter the debug ssh command and capture the debugging messages. Then contact the Cisco TAC.                                                             |
|     Out of memory      |     This message appears when the ASA cannot allocate memory for use by the SSH server, probably when the ASA is busy with high traffic.     |                                                                                                                                                             Restart the SSH session later.                                                                                                                                                              |
|   Rejected by server   |                                                         User authentication failed.                                                          |                                                                                                                                                      Ask the user to verify username and password.                                                                                                                                                      |
|    Reset by client     |                                         An SSH client sent the SSH_MSG_DISCONNECT message to the ASA.                                          |                                                                                                                                                                     None required.                                                                                                                                                                      |
| status code: hex (hex) |                 Users closed the SSH client window (running on Windows) instead of entering quit or exit at the SSH console.                 |                                                                                                                                  None required. Encourage users to exit the client gracefully instead of just exiting.                                                                                                                                  |
| Terminated by operator |                          The SSH session was terminated by entering the ssh disconnect command at the ASA console.                           |                                                                                                                                                                     None required.                                                                                                                                                                      |
|   Time-out activated   |                      The SSH session timed out because the duration specified by the ssh timeout command was exceeded.                       |                                                                                                        Restart the SSH connection. You can use the ssh timeout command to increase the default value of 5 minutes up to 60 minutes if required.                                                                                                         |

**Recommended Action** None required.

### 315012

**Error Message** `%ASA-3-315012: Weak SSH _type_ (_alg_) provided from client '_IP_address_' on interface _Int_. Connection failed. Not FIPS 140-2 compliant`

**Explanation** As part of the FIPS 140-2 certification, when FIPS is enabled, SSH connections can only be brought up using aes128-cbc or aes256-cbc as the cipher and SHA1 as the MAC. This syslog is generated when an unacceptable cipher or MAC is used. This syslog will not be seen if FIPS mode is disabled.

-   _type_ —cipher or MAC
-   _alg_ —The name of the unacceptable cipher or MAC
-   _IP\_address_ —The IP address of the client
-   _int_ —The interface that the client is attempting to connect to

**Recommended Action** Provide an acceptable cipher or MAC

### 315013

**Error Message** `%ASA-6-315013: SSH session from _SSH_client_address_ on interface _interface_name_ for user "_user_name_" rekeyed successfully`

**Explanation** This syslog is needed to indicate that an SSH rekey has successfully completed. This is a Common Criteria certification requirement.

-   _SSH\_client\_address_ —The IP address of the client
-   _interface\_name_ —The interface that the client is attempting to connect to
-   user\_name—The user name associated with the session

**Recommended Action** None

### 316001

**Error Message** `%ASA-3-316001: Denied new tunnel to _IP_address_ . VPN peer limit (_platform_vpn_peer_limit)_ exceeded`

**Explanation** If more VPN tunnels (ISAKMP/IPsec) are concurrently trying to be established than are supported by the platform VPN peer limit, then the excess tunnels are aborted.

**Recommended Action** None required.

### 316002

**Error Message** `%ASA-3-316002: VPN Handle error: protocol=_protocol_, src _in_if_num_:_src_addr_, dst _out_if_num_:_dst_addr_.`

**Explanation** The Secure Firewall ASA cannot create a VPN handle, because the VPN handle already exists.

-   _protocol_ —The protocol of the VPN flow
-   _in\_if\_num_ —The ingress interface number of the VPN flow
-   _src\_addr_ —The source IP address of the VPN flow
-   _out\_if\_num_ —The egress interface number of the VPN flow
-   _dst\_addr_ —The destination IP address of the VPN flow

**Recommended Action** This message may occur during normal operation; however, if the message occurs repeatedly and a major malfunction of VPN-based applications occurs, a software defect may be the cause. Enter the following commands to collect more information and contact the Cisco TAC to investigate the issue further:

```sql
capture
 name
 type asp-drop vpn-handle-error
show asp table classify crypto detail
show asp table vpn-context
```

### 317001

**Error Message** `%ASA-3-317001: No memory available for _limit_slow_`

**Explanation** The requested operation failed because of a low-memory condition.

**Recommended Action** Reduce other system activity to ease memory demands. If conditions warrant, upgrade to a larger memory configuration.

### 317002

**Error Message** `%ASA-3-317002: Bad path pointer of _number_ for _IP_address_, _number_ max`

**Explanation** A software error occurred.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 317003

**Error Message** `%ASA-3-317003: IP routing table creation failure - _reason_`

**Explanation** An internal software error occurred, which prevented the creation of a new IP routing table.

**Recommended Action** Copy the message exactly as it appears, and report it to Cisco TAC.

### 317004

**Error Message** `%ASA-3-317004: IP routing table limit warning - _limit_context_`

**Explanation** The number of routes in the named IP routing table has reached the configured warning limit.

**Recommended Action** Reduce the number of routes in the table, or reconfigure the limit.

### 317005

**Error Message** `%ASA-3-317005: IP routing table limit exceeded - _reason_`

**Explanation** Additional routes will be added to the table.

**Recommended Action** Reduce the number of routes in the table, or reconfigure the limit.

### 317006

**Error Message** `%ASA-3-317006: Pdb index error %08x, %04x, _pdb_`

**Explanation** The index into the PDB is out of range.

-   pdb—Protocol Descriptor Block, the descriptor of the PDB index error
-   pdb\_index—The PDB index identifier
-   pdb\_type—The type of the PDB index error

**Recommended Action** If the problem persists, copy the error message exactly as it appears on the console or in the system log, contact the Cisco TAC, and provide the representative with the collected information.

### 317007

**Error Message** `%ASA-6-317007: Added _route_type_ route _dest_address_ _netmask_ via _gateway_address_ [_distance_ /_metric_ ] on _interface_name route_type_`

**Explanation** A new route has been added to the routing table.

Routing protocol type:

C – connected, S – static, I – IGRP, R – RIP, M – mobile

B – BGP, D – EIGRP, EX - EIGRP external, O - OSPF

IA - OSPF inter area, N1 - OSPF NSSA external type 1

N2 - OSPF NSSA external type 2, E1 - OSPF external type 1

E2 - OSPF external type 2, E – EGP, i - IS-IS, L1 - IS-IS level-1

L2 - IS-IS level-2, ia - IS-IS inter area

-   _dest\_address_ —The destination network for this route
-   _netmask_ —The netmask for the destination network
-   _gateway\_address_ —The address of the gateway by which the destination network is reached
-   _distance_ —Administrative distance for this route
-   _metric_ —Metric for this route
-   _interface\_name_ —Network interface name through which the traffic is routed

**Recommended Action** None required.

### 317008

**Error Message** `%ASA-6-317008: Community list check with bad list _list_number_`

**Explanation** When an out of range community list is identified, this message is generated along with the list number.

**Recommended Action** None required.

### 317012

**Error Message** `%ASA-3-317012: Interface IP route counter negative -  _nameif-string-value_` 

**Explanation** Indicates that the interface route count is negative.

-   nameif-string-value—The interface name as specified by the nameif command
    

**Recommended Action** None required.

### 317077

**Error Message** `%ASA-6-317077: Added _protocol_name_ route _destination_address_ _subnet-mask_ via _gateway-address_ [_admin_distance_/_metric_] on [_inf_name_] [_vrf_name_] tableid [_table_id_]`

**Explanation** This message is generated when a route is added successfully on the Secure Firewall Threat Defense device.

**Recommended Action** None required.

### 317078

**Error Message** `%ASA-6-317078: Deleted _protocol_name_ route _destination_address_ _subnet-mask_ via _gateway-address_ [_admin_distance_/_metric_] on [_inf_name_] [_vrf_name_] tableid [_table_id_]`

**Explanation** This message is generated when a route is deleted from the Secure Firewall Threat Defense device.

**Recommended Action** None required.

### 317079

**Error Message** `%ASA-6-317079: Added static route _destination_address_ [_admin_distance/metric_] via _inf_name_ tableid [_table_id_]`

**Explanation** This message is generated when a static route is added successfully.

**Recommended Action** None required.

### 317080

**Error Message** `%ASA-6-317080: Deleted static route _destination_address_ [_admin_distance/metric_] via _inf_name_ tableid [_table_id_]`

**Explanation** This message is generated when a static route is deleted.

**Recommended Action** None required.

### 317012

**Error Message** `%ASA-3-317012: Interface IP route counter negative -  _nameif-string-value_` 

**Explanation** Indicates that the interface route count is negative.

-   nameif-string-value—The interface name as specified by the nameif command
    

**Recommended Action** None required.

### 318001

**Error Message** `%ASA-3-318001: Internal error: _reason_`

**Explanation** An internal software error occurred. This message occurs at five-second intervals.

**Recommended Action** Copy the message exactly as it appears, and report it to the Cisco TAC.

### 318002

**Error Message** `%ASA-3-318002: Flagged as being an ABR without a backbone area`

**Explanation** The router was flagged as an area border router without a backbone area configured in the router. This message occurs at five-second intervals.

**Recommended Action** Restart the OSPF process.

### 318003

**Error Message** `%ASA-3-318003: Reached unknown state in neighbor state machine`

**Explanation** An internal software error occurred. This message occurs at five-second intervals.

**Recommended Action** Copy the message exactly as it appears, and report it to the Cisco TAC.

### 318004

**Error Message** `%ASA-3-318004: DB already exist : area _string_ lsid _IP_address_ adv _netmask_ type 0x_number_`

**Explanation** The OSPF process had a problem locating the link state advertisement, which might lead to a memory leak.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 318005

**Error Message** `%ASA-3-318005: No corresponding LSA in retransmission database for _ip_address_`

**Explanation** OSPF found an inconsistency between its database and the IP routing table.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 318006

**Error Message** `%ASA-3-318006: if _interface_name_ if_state _number_`

**Explanation** An internal error occurred.

**Recommended Action** Copy the message exactly as it appears, and report it to the Cisco TAC.

### 318008

**Error Message** `%ASA-3-318008: Reconfigure virtual link`

**Explanation** The OSPF process is being reset, and it is going to select a new router ID. This action will bring down all virtual links.

**Recommended Action** Change the virtual link configuration on all of the virtual link neighbors to reflect the new router ID.

### 318101

**Error Message** `%ASA-3-318101: Internal error: _REASON_`

**Explanation** An internal software error has occurred.

-   _REASON_ —The detailed cause of the event

**Recommended Action** None required.

### 318102

**Error Message** `%ASA-3-318102: Flagged as being an ABR without a backbone area`

**Explanation** The router was flagged as an Area Border Router (ABR) without a backbone area in the router.

**Recommended Action** Restart the OSPF process.

### 318103

**Error Message** `%ASA-3-318103: Reached unknown state in neighbor state machine`

**Explanation** An internal software error has occurred.

**Recommended Action** None required.

### 318104

**Error Message** `%ASA-3-318104: DB already exist : area _AREA_ID_STR_ lsid _i_ adv _i_ type 0x_x_`

**Explanation** OSPF has a problem locating the LSA, which could lead to a memory leak.

-   _AREA\_ID\_STR_ —A string representing the area
-   _i_ —An integer value
-   _x_ —A hexadecimal representation of an integer value

**Recommended Action** None required.

### 318105

**Error Message** `%ASA-3-318105: No corresponding LSA in retransmission database for _i_`

**Explanation** OSPF found an inconsistency between its database and the IP routing table.

-   _i_ —An integer value
-   _x_ —A hexadecimal representation of an integer value
-   _d_ —A number

**Recommended Action** None required.

### 318106

**Error Message** `%ASA-3-318106: if _IF_NAME_ if_state _d_`

**Explanation** An internal error has occurred.

-   _IF\_NAME—_ The name of the affected interface
-   _d_ —A number

**Recommended Action** None required.

### 318108

**Error Message** `%ASA-3-318108: OSPF process _d_ is changing router-id. Reconfigure virtual link neighbors with our new router-id`

**Explanation** The OSPF process is being reset, and it is going to select a new router ID, which brings down all virtual links. To make them work again, you need to change the virtual link configuration on all virtual link neighbors.

-   _d_ —A number representing the process ID

**Recommended Action** Change the virtual link configuration on all the virtual link neighbors to include the new router ID.

### 318109

**Error Message** `%ASA-3-318109: Received packet with wrong state _x_`

**Explanation** OSPFv3 has received an unexpected interprocess message.

-   _x_ —A hexadecimal representation of an integer value

**Recommended Action** None required.

### 318110

**Error Message** `%ASA-3-318110: Invalid encrypted key _key_string_.`

**Explanation** The specified encrypted key is not valid.

-   _key\_string_ —A string representing the encrypted key

**Recommended Action** Either specify a clear text key and enter the service password-encryption command for encryption, or ensure that the specified encrypted key is valid. If the specified encrypted key is not valid, an error message appears during system configuration.

### 318111

**Error Message** `%ASA-3-318111: IPSEC policy for area _u_ already exists`

**Explanation** An attempt was made to use a SPI that has already been used.

-   _u_ —A number representing the SPI
-   _d_ —A number representing the process ID

**Recommended Action** Choose a different SPI.

### 318112

**Error Message** `%ASA-3-318112: IPSEC SPI _u_ already in use for area _d_`

**Explanation** An attempt was made to use a SPI that has already been used.

-   _u_ —A number representing the SPI
-   _d_ —A number representing the process ID

**Recommended Action** Choose a different SPI. Enter the show crypto ipv6 ipsec sa command to view a list of SPIs that are already being used.

### 318113

**Error Message** `%ASA-3-318113: IPSEC SPI _s s_ reused for different policy on area _u_`

**Explanation** An attempt was made to use a SPI that has already been used.

-   _s—_ A string representing an interface
-   _u_ —A number representing the SPI

**Recommended Action** Unconfigure the SPI first, or choose a different one.

### 318114

**Error Message** `%ASA-3-318114: IPSEC invalid key length _spi_value_`

**Explanation** The key length was incorrect.

-   _u_ —A number representing the SPI

**Recommended Action** Choose a valid IPsec key. An IPsec authentication key must be 32 (MD5) or 40 (SHA-1) hexidecimal digits long.

### 318115

**Error Message** `%ASA-3-318115: IPSEC create policy error _s_ for area _u_`

**Explanation** An IPsec API (internal) error has occurred.

-   _s—_ A string representing the error
-   _u_ —A number representing the SPI

**Recommended Action** None required.

### 318116

**Error Message** `%ASA-3-318116: IPSEC policy does not exist for area _u_`

**Explanation** An attempt was made to unconfigure a SPI that is not being used with OSPFv3.

-   _u_ —A number representing the SPI
-   _d_ —A number representing the process ID

**Recommended Action** Enter a show command to see which SPIs are used by OSPFv3.

### 318117

**Error Message** `%ASA-3-318117: IPSEC policy still in use for area _u_`

**Explanation** An attempt was made to remove the policy for the indicated SPI, but the policy was still being used by a secure socket.

-   _u_ —A number representing the SPI

**Recommended Action** None required.

### 318118

**Error Message** `%ASA-3-318118: IPSEC remove policy error _s_ for area _u_`

**Explanation** An IPsec API (internal) error has occurred.

-   _s_ —A string representing the specified error
-   _u_ —A number representing the SPI

**Recommended Action** None required.

### 318119

**Error Message** `%ASA-3-318119: IPSEC close session error _u_ for area _s_`

**Explanation** An IPsec API (internal) error has occurred.

-   _u_ —A number representing the SPI
-   _s_ —A string representing the specified interface

**Recommended Action** None required.

### 318120

**Error Message** `%ASA-3-318120: OSPFv3 was unable to register with Ipsec`

**Explanation** An internal error has occurred.

**Recommended Action** None required.

### 318121

**Error Message** `%ASA-3-318121: IPSEC general error _s_ for area _d_`

**Explanation** An internal error has occurred.

-   _s_ —A string representing the specified message
-   _d_ —A number representing the total number of generated messages

**Recommended Action** None required.

### 318122

**Error Message**`%ASA-3-318122: IPSEC error message retry for area _s_`

**Explanation** An internal error has occurred. The system is trying to reopen the secure socket and to recover.

-   _s_ —A string representing the specified message and specified interface
-   _d_ —A number representing the total number of recovery attempts

**Recommended Action** None required.

### 318123

**Error Message** `%ASA-3-318123: IPSEC error message abort for area _s_`

**Explanation** An internal error has occurred. The maximum number of recovery attempts has been exceeded.

-   _s_ —A string representing the specified message
-   _IF\_NAME_ —The specified interface

**Recommended Action** None required.

### 318125

**Error Message** `%ASA-3-318125: Interface _IF_NAME_ initialization failed`

**Explanation** The interface initialization failed. Possible reasons include the following:

-   The area to which the interface is being attached is being deleted.
-   It was not possible to create the link scope database.
-   It was not possible to create a neighbor datablock for the local router.

**Recommended Action** Remove the configuration command that initializes the interface and then try it again.

### 318126

**Error Message** `%ASA-3-318126: Interface _IF_NAME_ attached to multiple areas`

**Explanation** The interface is on the interface list for an area other than the one to which the interface links.

-   _IF\_NAME_ —The specified interface

**Recommended Action** None required.

### 318127

**Error Message** `%ASA-3-318127: Could not allocate or find the neighbor`

**Explanation** An internal error has occurred.

**Recommended Action** None required.

### 319001

**Error Message** `%ASA-3-319001: Acknowledge for arp update for IP address _dest_address_ to NP_number_ not received.`

**Explanation** The ARP process in the ASA lost internal synchronization because the ASA was overloaded.

**Recommended Action** None required. The failure is only temporary. Check the average load of the ASA and make sure that it is not used beyond its capabilities.

### 319002

**Error Message** `%ASA-3-319002: Acknowledge for route update for IP address _dest_address_ to NP_number_ not received.`

**Explanation** The routing module in the ASA lost internal synchronization because the ASA was overloaded.

**Recommended Action** None required. The failure is only temporary. Check the average load of the ASA and make sure that it is not used beyond its capabilities.

### 319003

**Error Message** `%ASA-3-319003: Arp update for IP address _address_ to NP_n_ failed.`

**Explanation** When an ARP entry has to be updated, a message is sent to the network processor (NP) in order to update the internal ARP table. If the module is experiencing high utilization of memory or if the internal table is full, the message to the NP may be rejected and this message generated.

**Recommended Action** Verify if the ARP table is full. If it is not full, check the load of the module by reviewing the CPU utilization and connections per second. If CPU utilization is high and/or there is a large number of connections per second, normal operations will resume when the load returns to normal.

### 319004

**Error Message** `%ASA-3-319004: Route update for IP address _dest_address_ to NP_number_ failed.`

**Explanation** The routing module in the ASA lost internal synchronization because the system was overloaded.

**Recommended Action** None required. The failure is only temporary. Check the average load of the system and make sure that it is not used beyond its capabilities.

## Messages 320001 to 342008

This chapter includes messages from 320001 to 342008.

### 320001

**Error Message** `%ASA-3-320001: The subject name of the peer cert is not allowed for connection`

**Explanation** When the Secure Firewall ASA is an easy VPN remote device or server, the peer certificate includes asubject name that does not match the output of the ca verifycertdn command. A man-in-the-middle attack might be occurring, where a device spoofs the peer IP address and tries to intercept a VPN connection from the Secure Firewall ASA.

**Recommended Action** None required.

### 321001

**Error Message** `%ASA-5-321001: Resource _var1_ limit of _var2_ reached.`

**Explanation** A configured resource usage or rate limit for the indicated resource was reached.

**Recommended Action** If the platform maximum connections were reached, it takes some time to reallocate memory to free system memory, resulting in traffic failure. After memory space is released, you must reload the device. For further assistance, contact TAC team.

### 321002

**Error Message** `%ASA-5-321002: Resource _var1_ rate limit of _var2_ reached.`

**Explanation** A configured resource usage or rate limit for the indicated resource was reached.

**Recommended Action** If the platform maximum connections were reached, it takes some time to reallocate memory to free system memory, resulting in traffic failure. After memory space is released, you must reload the device. For further assistance, contact TAC team.

### 321003

**Error Message** `%ASA-6-321003: Resource _var1_ log level of _var2_ reached.`

**Explanation** A configured resource usage or rate logging level for the indicated resource was reached.

**Recommended Action** None required.

### 321004

**Error Message** `%ASA-6-321004: Resource _var1_ rate log level of _var2_ reached`

**Explanation** A configured resource usage or rate logging level for the indicated resource was reached.

**Recommended Action** None required.

### 321005

**Error Message** `%ASA-2-321005: System CPU utilization reached _utilization%_%%`

**Explanation** The system CPU utilization has reached 95 percent or more and remains at this level for five minutes.

-   _utilization %_ —The percentage of CPU being used

**Recommended Action** If this message occurs periodically, you can ignore it. If it repeats frequently, check the output of the show cpu command and verify the CPU usage. If it is high, contact the Cisco TAC.

### 321006

**Error Message** `%ASA-2-321006: System Memory usage reached _utilization%_%%`

**Explanation** The system memory usage has reached 80 percent or more and remains at this level for five minutes.

-   _utilization %_ —The percentage of memory being used

**Recommended Action** If this message occurs periodically, you can ignore it. If it repeats frequently, check the output of the show memory command and verify the memory usage. If it is high, contact the Cisco TAC.

### 321007

**Error Message** `%ASA-3-321007: System is low on free memory blocks of size _block_size_ (_free_blocks_ CNT out of _max_blocks_ MAX)`

**Explanation** The system is low on free blocks of memory. Running out of blocks may result in traffic disruption.

-   _block\_size_ —The block size of memory (for example, 4, 1550, 8192)
-   _free\_blocks_ —The number of free blocks, as shown in the CNT column after using the show blocks command
-   _max\_blocks_ —The maximum number of blocks that the system can allocate, as shown in the MAX column after using the show blocks command

**Recommended Action** Use the show blocks command to monitor the amount of free blocks in the CNT column of the output for the indicated block size. If the CNT column remains zero, or very close to it for an extended period of time, then the Secure Firewall ASA may be overloaded or running into another issue that needs additional investigation.

### 322001

**Error Message** `%ASA-3-322001: Deny MAC address _MAC_address_, possible spoof attempt on interface _interface_`

**Explanation** The Secure Firewall ASA received a packet from the offending MAC address on the specified interface, but the source MAC address in the packet is statically bound to another interface in the configuration. Either a MAC-spoofing attack or a misconfiguration may be the cause.

**Recommended Action** Check the configuration and take appropriate action by either finding the offending host or correcting the configuration.

### 322002

**Error Message** `%ASA-3-322002: ARP inspection check failed for arp _{request|response}_ received from host _MAC_address_ on interface _interface_. This host is advertising MAC Address _MAC_address_1_ for IP Address _IP_address_, which is _{statically|dynamically}_ bound to MAC Address _MAC_address_2_`

**Explanation** If the ARP inspection module is enabled, it checks whether a new ARP entry advertised in the packet conforms to the statically configured or dynamically learned IP-MAC address binding before forwarding ARP packets across the Secure Firewall ASA. If this check fails, the ARP inspection module drops the ARP packet and generates this message. This situation may be caused by either ARP spoofing attacks in the network or an invalid configuration (IP-MAC binding).

**Recommended Action** If the cause is an attack, you can deny the host using the ACLs. If the cause is an invalid configuration, correct the binding.

### 322003

**Error Message** `%ASA-3-322003: ARP inspection check failed for arp _{request|response}_ received from host _MAC_address_ on interface _interface_. This host is advertising MAC Address _MAC_address_1_ for IP Address _IP_address_, which is not bound to any MAC Address`

**Explanation** If the ARP inspection module is enabled, it checks whether a new ARP entry advertised in the packet conforms to the statically configured IP-MAC address binding before forwarding ARP packets across the Secure Firewall ASA. If this check fails, the ARP inspection module drops the ARP packet and generates this message. This situation may be caused by either ARP spoofing attacks in the network or an invalid configuration (IP-MAC binding).

**Recommended Action** If the cause is an attack, you can deny the host using the ACLs. If the cause is an invalid configuration, correct the binding.

### 322004

**Error Message** `%ASA-6-322004: No management IP address configured for transparent firewall. Dropping protocol _protocol_ packet from _interface_in_:_source_address_/_source_port_ to _interface_out_:_dest_address_/_dest_port_`

**Explanation** The Secure Firewall ASA dropped a packet because no management IP address was configured in the transparent mode.

-   protocol—Protocol string or value
-   interface\_in—Input interface name
-   source\_address—Source IP address of the packet
-   source\_port—Source port of the packet
-   interface\_out—Output interface name
-   dest\_address—Destination IP address of the packet
-   dest\_port—Destination port of the packet

**Recommended Action** Configure the device with the management IP address and mask values.

### 323001

**Error Message 1** `%ASA-3-323001: Module _module_id_ experienced a control channel communication failure.`

**Error Message 2** `%ASA-3-323001: Module in slot _slot_num_ experienced a control channel communications failure.`

**Explanation** The Secure Firewall ASA is unable to communicate via control channel with the module installed (in the specified slot).

-   module\_id—For a software services module, specifies the services module name.
-   slot\_num—For a hardware services module, specifies the slot in which the failure occurred. Slot 0 indicates the system main board, and slot 1 indicates the module installed in the expansion slot.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 323002

**Error Message** `%ASA-3-323002: Module _module_id_ is not able to shut down, shut down request not answered.`

`%ASA-3-323002: Module in slot _slot_num_ is not able to shut down, shut down request not answered.`

**Explanation** The module installed did not respond to a shutdown request.

-   module\_id—For a software services module, specifies the service module name.
-   slot\_num—For a hardware services module, specifies the slot in which the failure occurred. Slot 0 indicates the system main board, and slot 1 indicates the module installed in the expansion slot.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 323003

**Error Message 1** `%ASA-3-323003: Module _module_id_ is not able to reload, reload request not answered.`

**Error Message 2** `%ASA-3-323003: Module in slot _slotnum_ is not able to reload, reload request not answered.`

**Explanation** The module installed did not respond to a reload request.

-   module\_id—For a software services module, specifies the service module name.
-   slot\_num—For a hardware services module, specifies the slot in which the failure occurred. Slot 0 indicates the system main board, and slot 1 indicates the module installed in the expansion slot.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 323004

**Error Message** `%ASA-3-323004: Module in slot _string_one_ failed to write software v_newver_ (currently v_ver_), _reason_. hw-module reset is required before further use.`

**Explanation** The module failed to accept a software version, and will be transitioned to an UNRESPONSIVE state. The module is not usable until the software is updated.

-   string one—The text string that specifies the module
-   _\>newver_ —The new version number of software that was not successfully written to the module (for example, 1.0(1)0)
-   _\>ver_ —The current version number of the software on the module (for example, 1.0(1)0)
-   _\>reason_ —The reason the new version cannot be written to the module. The possible values for _\>reason_ include the following:

\- write failure

\- failed to create a thread to write the image

**Recommended Action** If the module software cannot be updated, it will not be usable. If the problem persists, contact the Cisco TAC.

### 323005

**Error Message-1** `%ASA-3-323005: Module _syslog_string_ can not be started completely.`

**Error Message-2** `%ASA-3-323005: Module _syslog_string_ powerfail recovery is in progress.`

**Explanation** This message indicates that the module cannot be started completely. The module will remain in the UNRESPONSIVE state until this condition is corrected. A module that is not fully seated in the slot is the most likely cause.

**Recommended Action** Verify that the module is fully seated and check to see if any status LEDs on the module are on. It may take a minute after fully reseating the module for the Secure Firewall ASA to recognize that it is powered up. If this message appears after verifying that the module is seated and after resetting the module using either the sw-module module _service-module-name_ reset command or the hw-module module _slotnum_ reset command, contact the Cisco TAC.

### 323006

**Error Message** `%ASA-1-323006: Module _ips_ experienced a data channel communication failure, data channel is DOWN.`

**Explanation** A data channel communication failure occurred and the Secure Firewall ASA was unable to forward traffic to the services module. This failure triggers a failover when the failure occurs on the active Secure Firewall ASA in an HA configuration. The failure also results in the configured fail open or fail closed policy being enforced on traffic that would normally be sent to the services module. This message is generated whenever a communication problem over the Secure Firewall ASA dataplane occurs between the system module and the services module, which can be caused when the services module stops, resets, is removed or disabled.

**Recommended Action** For software services modules such as IPS, recover the module using the sw-module module ips recover command. For hardware services modules, if this message is not the result of the SSM reloading or resetting and the corresponding syslog message 505010 is not seen after the SSM returns to an UP state, reset the module using the hw-module module 1 reset command.

### 323007

**Error Message** `%ASA-3-323007: Module in slot _slot_ experienced a firmware failure and the recovery is in progress.`

**Explanation** An Secure Firewall ASA with a 4GE-SSM installed experienced a short power surge, then rebooted. As a result, the 4GE-SSM may come online in an unresponsive state. The Secure Firewall ASA has detected that the 4GE-SSM is unresponsive, and automatically restarts the 4GE-SSM.

**Recommended Action** None required.

### 324000

**Error Message** `%ASA-3-324000: Drop GTP message _msg_type_ Flow:(_source_interface_:_source_address_/_source_port_ to _dest_interface_:_dest_address_/_dest_port_) Reason: _reason_`

**Explanation** The packet being processed did not meet the filtering requirements as described in the reason variable and is being dropped.

**Recommended Action** None required.

### 324001

**Error Message 1** `%ASA-3-324001: GTP_<version>_ packet parsing error from _source_interface_ :_source_address_ /_source_port_ to _dest_interface_ :_dest_address_ /_dest_port_ , TID: _tid_value_ , Reason: _reason_`

There was an error processing the GTP packet. The following are possible reasons:

-   Mandatory IE is missing
-   Mandatory IE incorrect
-   IE out of sequence
-   Invalid message format.
-   Optional IE incorrect
-   Invalid TEID
-   Unknown IE
-   Bad length field
-   Unknown GTP message.
-   Message too short
-   Unexpected message seen
-   Null TID
-   Version not supported

**Recommended Action** If the parser error message is seen periodically, it can be ignored. If it is seen frequently, then the endpoint may be sending out bad packets as part of an attack.

**Error Message 2** `%ASA-3-324001: GTP_<version>_ packet parse INFO:MsgType:_message type code_ (_message code value_) - TEID:_tid_value_ MCB INFO - Local-GSN:_IP address_, Remote-GSN:_IP address_. - Flow:(_source_interface_: _source_address_ /_source_port_ to gn:_dest_address_ /_dest_port_)`

The same log message ID is utilized for info level logs when parsing GTP packets:

**Example** `%ASA-3-324001: GTPv2 PKT Parse INFO:MsgType:34 (Modify Bearer Request) - TEID:0xaaaaaaaa MCB INFO - Local-GSN:192.168.1.224, Remote-GSN:192.168.2.20. - Flow:(outside:192.168.2.20/12035 to gn:192.168.1.224/2123)`

**Recommended Action** None.

### 324002

**Error Message** `%ASA-3-324002: No PDP[MCB] exists to process GTPv0 _msg_type_ from _source_interface_ :_source_address_ /_source_port_ to _dest_interface_ :_dest_address_ /_dest_port_ , TID: _tid_value_`

**Explanation** If this message was preceded by message 321100, memory allocation error, the message indicates that there were not enough resources to create the PDP context. If not, it was not preceded by message 321100. For version 0, it indicates that the corresponding PDP context cannot be found. For version 1, if this message was preceded by message 324001, then a packet processing error occurred, and the operation stopped.

**Recommended Action** If the problem persists, determine why the source is sending packets without a valid PDP context.

### 324003

**Error Message** `%ASA-3-324003: _msg_type_ - Flow:(_source_interface_:_source_address_/_source_port_ to _dest_interface_:_dest_address_/_dest_port_)`

**Explanation** The response received does not have a matching request in the request queue and should not be processed further.

**Recommended Action** If this message is seen periodically, it can be ignored. But if it is seen frequently, then the endpoint may be sending out bad packets as part of an attack.

### 324004

**Error Message** `%ASA-3-324004: GTP packet with version _Ver_number_ from _source_interface_:_source_address_/_source_port_ to _dest_interface_:_dest_address_/_dest_port_ not supported`

**Explanation** The packet being processed has a version other than the currently supported version, which is 0 or 1. If the version number printed out is an incorrect number and is seen frequently, then the endpoint may be sending out bad packets as part of an attack.

**Recommended Action** None required.

### 324005

**Error Message** `%ASA-3-324005: Unable to create tunnel from _source_interface_:_source_address_/_source_port_ to _dest_interface_:_dest_address_/_dest_port_`

**Explanation** An error occurred while trying to create the tunnel for the transport protocol data units.

**Recommended Action** If this message occurs periodically, it can be ignored. If it repeats frequently, contact the Cisco TAC.

### 324006

**Error Message** `%ASA-3-324006: GSN _IP_address_ tunnel limit _tunnel_limit_ exceeded, PDP Context TID _tid_ creation failed`

**Explanation** The GPRS support node sending the request has exceeded the maximum allowed tunnels created, so no tunnel will be created.

**Recommended Action** Check to see whether the tunnel limit should be increased or if there is a possible attack on the network.

### 324007

**Error Message** `%ASA-3-324007: Unable to create GTP connection for response from _source_address_/0 to _0_/_dest_address_`

**Explanation** An error occurred while trying to create the tunnel for the transport protocol data units for a differentsServicing GPRS support node or gateway GPRS support node.

**Recommended Action** Check debugging messages to see why the connection was not created correctly. If the problem persists, contact the Cisco TAC.

### 324008

**Error Message** `%ASA-3-324008: No PDP exists to update the data _sgsn[ggsn]_ PDPMCB Info,PDPMCB Info TEID: _teid_value_, PDP TID: _teid_value_, Local GSN: _IPaddress_ (_VPIfNum_), Remote GSN: _IPaddress_ (_VPIfNum_)`

**Explanation** When a GTP HA message is received on the standby unit to update the PDP with data sgsn/ggsn PDPMCB information, the PDP is not found because of a previous PDP update message that was not successfully delivered or successfully processed on the standby unit.

**Recommended Action** If this message occurs periodically, you can ignore it. If it occurs frequently, contact the Cisco TAC.

### 324010

**Error Message** `%ASA-5-324010: Subscriber _IMSI_ PDP Context activated on network _mcc_`

**Explanation**

This message appears when the PDP Context is activated. MCC is always 3 digits and MNC is 2 or 3 digits.

| ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)

**Note** | ___

The MCC, MNC, IE type, or Cell ID could be "Unknown" if the packet does not contain the location information IEs.

___ |
|--------|-----------------------------------------------------------------------------------------------------------------------|

Example:

```shell
%ASA-5-324010: Subscriber ID PDP Context activated on network MCC/MNC 11122 (v1 RAI/v1 ULI) CellID 1
```

```csharp
%ASA-5-324010: Subscriber ID PDP Context activated on network Unknown
```

**Recommended Action** None

### 324011

**Error Message** `%ASA-5-324011: Subscriber _IMSI_ location changed during _mcc_ from _mnc_ _IE_type_`

**Explanation**

A message appears when the location has changed. MCC is always 3 digits and MNC is 2 or 3 digits. This change could be triggered by handoff or a subsequent create request after the PDP is created and that the previous create request on ASA expired.

| ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)

**Note** | ___

The MCC, MNC, IE type, or Cell ID could be "Unknown" if the packet does not contain the location information IEs.

___ |
|--------|-----------------------------------------------------------------------------------------------------------------------|

Example:

```swift
%ASA-5-324011: Subscriber ID location changed during v1 handoff from MCC/MNC 11122 (v1 RAI/v1 ULI-CGI) CellID 1 to MCC/MNC 111222 (v1 RAI/v1 ULI-CGI) CellID 2
```

```sql
%ASA-5-324011: Subscriber ID location changed during v1 handoff from MCC/MNC 11122 (v2 ULI) CellID 1 to Unknown
```

```sql
%ASA-5-324011: Subscriber ID location changed during v1 handoff from Unknown to MCC/MNC 11122 (v1 RAI) CellID 1
```

**Recommended Action** None

### 324012

**Error Message** `%ASA-5-324012: GTP_PARSE: _GTP_IE_TYPE_[_GTP_IE_TYPE_NUMBER_]: Invalid Length Received Length: _Length_Received_, Minimum Expected Length: _Expected_Length_`

**Explanation**

When GTP IE length received is less than the minimum length, an error message appears with the following data:

-   _GTP IE TYPE_: Name Of GTP IE.
    
-   _GTP IE TYPE NUMBER_: Number Defined for GTP IE Type
    
-   _Invalid Length Received_: Invalid Length Received in the Packet.
    
-   _Minimum Expected Length_: Minimum Expected length for IE.
    

Example:

`%ASA-5-324012: GTP_PARSE: GTPV2_PARSE: Presence Reporting Area Action[177]: Invalid Length Received Length: 4, Minimum Expected Length: 11`

**Recommended Action** None

### 324300

**Error Message** `%ASA-3-324300: Radius Accounting Request from _from_addr_ has an incorrect request authenticator`

**Explanation** When a shared secret is configured for a host, the request authenticator is verified with that secret. If it fails, it is logged and packet processing stops.

-   _from\_addr_ —The IP address of the host sending the RADIUS accounting request

**Recommended Action** Check to see that the correct shared secret was configured. If it is, double-check the source of the packet to make sure that it was not spoofed.

### 324301

**Error Message** `%ASA-3-324301: Radius Accounting Request has a bad header length _hdr_len_, packet length _pkt_len_`

**Explanation** The accounting request message has a header length that is not the same as the actual packet length, so packet processing stops.

-   _hdr\_len_ —The length indicated in the request header
-   _pkt\_len_ —The actual packet length

**Recommended Action** Make sure the packet was not spoofed. If the packet is legitimate, then capture the packet and make sure the header length is incorrect, as indicated by the message. If the header length is correct, and if the problem persists, contact the Cisco TAC.

### 324302

**Error Message** `%ASA-4-324302: Server=_IPaddr_:_port_, ID=_id_: Rejecting the RADIUS response: _Reason_.`

**Explanation** This message is generated when RADIUS response is rejected either because the required message-authenticator payload is missing in the response or if the Message-Authenticator payload failed validation check.

-   **IPaddr:port**—RADIUS server IP address and port
    
-   **id**—RADIUS request ID
    
-   **Reason**—Reason why the RADIUS response is rejected:
    
    -   Required Message-Authenticator Payload Missing
        
    -   Message-Authenticator payload failed validation check
        

**Recommended Action** None.

### 324303

**Error Message** `%ASA-6-324303: Server=_IPaddr:port_ ID=_id_ The RADIUS server supports and included the Message-Authenticator payload in its response. To prevent Man-In-The-Middle attacks, consider enabling ‘ message-authenticator’ on the aaa-server-group configuration for this server as a security best practice.`

**Explanation**This message is generated to convey that the RADIUS server supports and included Message-authenticator payload in the RADIUS response. Also, provides best security practices that is configurable and could disable this syslog.

-   **IPaddr:port**—RADIUS server IP address and port
    
-   **id**—RADIUS request ID
    

In addition, this syslog is rate-limited to report not more than 10 syslog messages in a 5-minute interval window by default. You can configure custom rate-limit interval and count through CLI.

To view the existing rate limits, use:

```sql
show running-configuration all logging | grep 324303
```

To configure a custom value, use:

```
logging rate-limit 10 300 message 324303
```

**Recommended Action** Configure message-authenticator-required CLI under AAA server configuration.

### 325001

**Error Message** `%ASA-3-325001: Router _ipv6_address_ on _interface_ has conflicting ND (Neighbor Discovery) settings`

**Explanation** Another router on the link sent router advertisements with conflicting parameters.

-   ipv6\_address—IPv6 address of the other router
-   interface—Interface name of the link with the other router

**Recommended Action** Verify that all IPv6 routers on the link have the same parameters in the router advertisement for hop\_limit, managed\_config\_flag, other\_config\_flag, reachable\_time and ns\_interval, and that preferred and valid lifetimes for the same prefix, advertised by several routers, are the same. To list the parameters per interface, enter the show ipv6 interface command.

### 325002

**Error Message** `%ASA-4-325002: Duplicate address _ipv6_address_/_MAC_address_ on _interface_`

**Explanation** Another system is using your IPv6 address.

-   ipv6\_address—The IPv6 address of the other router
-   MAC\_address—The MAC address of the other system, if known; otherwise, it is considered unknown.
-   interface—The interface name of the link with the other system

**Recommended Action** Change the IPv6 address of one of the two systems.

### 325004

**Error Message** `%ASA-4-325004: IPv6 Extension Header _hdr_type_ _action_ by configuration. _protocol_ from _src_int_:_src_ipv6_addr_/_src_port_ to _dst_interface_:_dst_ipv6_addr_/_dst_port_`

**Explanation** A user has configured one or multiple actions over the specified IPv6 header extension.

-   _hdr\_type_ —Can be one of the following values:

ah—Configured action over the AH extension header

count—Configured action over the number of extension headers

destination-option—Configured action over the destination option extension header

esp—Configured action over the ESP extension header

fragment—Configured action over the fragment extension header

hop-by-hop—Configured action over the hop-by-hop extension header

routing-address count—Configured action over the number of addresses in the routing extension header

routing-type—Configured action over the routing type extension header

-   _action_ —Can be one of the following values:

denied—The packet is denied.

denied/logged—The packet is denied and logged.

logged—The packet is logged.

**Recommended Action** If the configured action is not expected, under the policy-map command, check the action in the match header extension\_header\_type command and the parameters command, and make the correct changes. For example:

```lua
ciscoasa (config)# policy-map type inspect ipv6 pname
ciscoasa (config-pmap)# parameters
ciscoasa (config-pmap-p)# no match header extension_header_type
 ! to remove the configuration
ciscoasa (config-pmap-p)# no drop ! so packets with the specified extension_header_type 
are not dropped
ciscoasa (config-pmap-p)# no log ! so packets with the specified extension_header_type 
are not logged
ciscoasa (config-pmap-p)# no drop log ! so packets with the specified extension_header_type 
are not dropped or logged
```

### 325005

**Error Message** `%ASA-4-325005: Invalid IPv6 Extension Header Content:_string_. _detail_regarding_protocol_ from _ingress_interface_:_IP_/_port_ to _egress_interface_:_IP_/_port_`

**Explanation** An IPv6 packet with a bad extension header has been detected.

-   _string_ —Can be one of the following values:

\- wrong extension header order

\- duplicate extension header

\- routing extension header

**Recommended Action** Configure the capture command to record the dropped packet, then analyze the cause of the dropped packet. If the validity check of the IPv6 extension header can be ignored, disable the validity check in the IPv6 policy map by entering the following commands:

```lua
ciscoasa (config)# policy-map type inspect ipv6 policy_name
ciscoasa (config-pmap)# parameters
ciscoasa (config-pmap-p)# no verify-header type
```

### 325006

**Error Message** `%ASA-4-325006: IPv6 Extension Header not in order: Type _hdr_type_ occurs after Type _hdr_type_. _prot_ from _src_int_:_src_ipv6_addr_/_src_port_ to _dst_interface_:_dst_ipv6_addr_/_dst_port_`

**Explanation** An IPv6 packet with out-of-order extension headers has been detected.

**Recommended Action** Configure the capture command to record the dropped packet, then analyze the extension header order of the dropped packet. If out-of-order header extensions are allowed, disable the out-of-order check in the IPv6 type policy map by entering the following commands:

```graphql
ciscoasa (config)# policy-map type inspect ipv6 policy_name
ciscoasa (config-pmap)# parameters
ciscoasa (config-pmap-p)# no verify-header order
```

### 325007

**Error Message** `%ASA-7-325007: IPv6 security check failed. Dropped packet from _interface_:_address_/_port_ to _address_/_port_ with source MAC address _MAC_address_ and hop limit _limit_value_`

**Explanation** Security check failed.

**Recommended Action** None.

### 326001

**Error Message** `%ASA-3-326001: Unexpected error in the timer library: _error_message_`

**Explanation** A managed timer event was received without a context or a correct type, or no handler exists. Alternatively, if the number of events queued exceeds a system limit, an attempt to process them will occur at a later time.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326002

**Error Message** `%ASA-3-326002: Error in _error_message_ : _error_message_`

**Explanation** The IGMP process failed to shut down upon request. Events that are performed in preparation for this shutdown may be out-of-sync.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326004

**Error Message** `%ASA-3-326004: An internal error occurred while processing a packet queue`

**Explanation** The IGMP packet queue received a signal without a packet.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326005

**Error Message** `%ASA-3-326005: Mrib notification failed for (_IP_address_, _IP_address_ )`

**Explanation** A packet triggering a data-driven event was received, and the attempt to notify the MRIB failed.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326006

**Error Message** `%ASA-3-326006: Entry-creation failed for (_IP_address_, _IP_address_ )`

**Explanation** The MFIB received an entry update from the MRIB, but failed to create the entry related to the addresses displayed. The probable cause is insufficient memory.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326007

**Error Message** `%ASA-3-326007: Entry-update failed for (_IP_address_, _IP_address_ )`

**Explanation** The MFIB received an interface update from the MRIB, but failed to create the interface related to the addresses displayed. The probable cause is insufficient memory.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326008

**Error Message** `%ASA-3-326008: MRIB registration failed`

**Explanation** The MFIB failed to register with the MRIB.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326009

**Error Message** `%ASA-3-326009: MRIB connection-open failed`

**Explanation** The MFIB failed to open a connection to the MRIB.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326010

**Error Message** `%ASA-3-326010: EIGRP-_ddb_name_ tableid as_id: Neighbor address (%interface) is event_msg: msg`

**Explanation** The MFIB failed to unbind from the MRIB.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326011

**Error Message** `%ASA-3-326011: MRIB table deletion failed`

**Explanation** The MFIB failed to retrieve the table that was supposed to be deleted.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326012

**Error Message** `%ASA-3-326012: Initialization of _string_ functionality failed`

**Explanation** The initialization of a specified functionality failed. This component might still operate without the functionality.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326013

**Error Message** `%ASA-3-326013: Internal error: _string_ in _string_ line _%d_ (_%s_ )`

**Explanation** A fundamental error occurred in the MRIB.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326014

**Error Message** `%ASA-3-326014: Initialization failed: error_message _error_message_`

**Explanation** The MRIB failed to initialize.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326015

**Error Message** `%ASA-3-326015: Communication error: error_message error_message`

**Explanation** The MRIB received a malformed update.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326016

**Error Message** `%ASA-3-326016: Failed to set un-numbered interface for _interface_name_ (_string_ )`

**Explanation** The PIM tunnel is not usable without a source address. This situation occurs because a numbered interface cannot be found, or because of an internal error.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326017

**Error Message** `%ASA-3-326017: Interface Manager error - _string_ in _string_ : _string_`

**Explanation** An error occurred while creating a PIM tunnel interface.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326019

**Error Message** `%ASA-3-326019: _string_ in _string_ : _string_`

**Explanation** An error occurred while creating a PIM RP tunnel interface.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326020

**Error Message** `%ASA-3-326020: List error in _string_ : _string_`

**Explanation** An error occurred while processing a PIM interface list.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326021

**Error Message** `%ASA-3-326021: Error in _string_ : _string_`

**Explanation** An error occurred while setting the SRC of a PIM tunnel interface.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326022

**Error Message** `%ASA-3-326022: Error in _string_ : _string_`

**Explanation** The PIM process failed to shut down upon request. Events that are performed in preparation for this shutdown may be out-of-sync.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326023

**Error Message** `%ASA-3-326023: _string_ - _IP_address_ : _string_`

**Explanation** An error occurred while processing a PIM group range.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326024

**Error Message** `%ASA-3-326024: An internal error occurred while processing a packet queue.`

**Explanation** The PIM packet queue received a signal without a packet.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326025

**Error Message** `%ASA-3-326025: _string_`

**Explanation** An internal error occurred while trying to send a message. Events scheduled to occur on the receipt of a message, such as deletion of the PIM tunnel IDB, may not occur.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326026

**Error Message** `%ASA-3-326026: Server unexpected error: _error_message_`

**Explanation**The MRIB failed to register a client.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326027

**Error Message** `%ASA-3-326027: Corrupted update: _error_message_`

**Explanation**The MRIB received a corrupt update.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 326028

**Error Message** `%ASA-3-326028: Asynchronous error: _error_message_`

**Explanation**An unhandled asynchronous error occurred in the MRIB API.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 327001

**Error Message** `%ASA-3-327001: IP SLA Monitor: Cannot create a new process`

**Explanation**The IP SLA monitor was unable to start a new process.

**Recommended Action** Check the system memory. If memory is low, then this is probably the cause. Try to reenter the commands when memory is available. If the problem persists, contact the Cisco TAC.

### 327002

**Error Message** `%ASA-3-327002: IP SLA Monitor: Failed to initialize, IP SLA Monitor functionality will not work`

**Explanation**The IP SLA monitor failed to initialize. This condition is caused by either the timer wheel function failing to initialize or a process not being created. Sufficient memory is probably not available to complete the task.

**Recommended Action** Check the system memory. If memory is low, then this is probably the cause. Try to reenter the commands when memory is available. If the problem persists, contact the Cisco TAC.

### 327003

**Error Message** `%ASA-3-327003: IP SLA Monitor: Generic Timer wheel timer functionality failed to initialize`

**Explanation**The IP SLA monitor cannot initialize the timer wheel.

**Recommended Action** Check the system memory. If memory is low, then the timer wheel function did not initialize. Try to reenter the commands when memory is available. If the problem persists, contact the Cisco TAC.

### 328001

**Error Message** `%ASA-3-328001: Attempt made to overwrite a set stub function in _string_ .`

**Explanation**A single function can be set as a callback for when a stub with a check registry is invoked. An attempt to set a new callback failed because a callback function has already been set.

-   string—The name of the function

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 328002

**Error Message** `%ASA-3-328002: Attempt made in _string_ to register with out of bounds key`

**Explanation** In the FASTCASE registry, the key has to be smaller than the size specified when the registry was created. An attempt was made to register with a key out-of-bounds.

**Recommended Action** Copy the error message exactly as it appears, and report it to the Cisco TAC.

### 329001

**Error Message** `%ASA-3-329001: The _string0_ subblock named _string1_ was not removed`

**Explanation**A software error has occurred. IDB subblocks cannot be removed.

-   _string0_ —SWIDB or HWIDB
-   _string1_ —The name of the subblock

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 331001

**Error Message** `%ASA-3-331001: Dynamic DNS Update for '_fqdn_name_' <=> _ip_address_ failed`

**Explanation**The dynamic DNS subsystem failed to update the resource records on the DNS server. This failure might occur if the Secure Firewall ASA is unable to contact the DNS server or the DNS service is not running on the destination system.

-   _fqdn\_name_ —The fully qualified domain name for which the DNS update was attempted
-   _ip\_address_ —The IP address of the DNS update

**Recommended Action** Make sure that a DNS server is configured and reachable by the Secure Firewall ASA. If the problem persists, contact the Cisco TAC.

### 331002

**Error Message** `%ASA-5-331002: Dynamic DNS _type_ RR for '_fqdn_name_' -> '_ip_address_ ' successfully updated in DNS server _ip_address_`

**Explanation** A dynamic DNS update succeeded in the DNS server.

-   _type_ —The type of resource record, which may be A or PTR
-   _fqdn\_name_ —The fully qualified domain name for which the DNS update was attempted
-   _ip\_address_ —The IP address of the DNS update
-   _dns\_server\_ip_ —The IP address of the DNS server

**Recommended Action** None required.

### 332001

**Error Message** `%ASA-3-332001: Unable to open cache discovery socket, WCCP V_2_ closing down`

**Explanation** An internal error that indicates the WCCP process was unable to open the UDP socket used to listen for protocol messages from caches.

**Recommended Action** Ensure that the IP configuration is correct and that at least one IP address has been configured.

### 332002

**Error Message** `%ASA-3-332002: Unable to allocate message buffer, WCCP V_2_ closing down`

**Explanation** An internal error that indicates the WCCP process was unable to allocate memory to hold incoming protocol messages.

**Recommended Action** Ensure that enough memory is available for all processes.

### 332003

**Error Message** `%ASA-5-332003: Web Cache _IP_address_/_service_ID_ acquired`

**Explanation** A service from the web cache of the Secure Firewall ASA was acquired.

-   IP\_address—The IP address of the web cache
-   service\_ID—The WCCP service identifier

**Recommended Action** None required.

### 332004

**Error Message** `%ASA-1-332004: Web Cache _IP_address_/_service_ID_ lost`

**Explanation** A service from the web cache of the Secure Firewall ASA was lost.

-   IP\_address—The IP address of the web cache
-   service\_ID—The WCCP service identifier

**Recommended Action** Verify operation of the specified web cache.

### 333001

**Error Message** `%ASA-6-333001: EAP association initiated - context: _EAP-context_`

**Explanation** An EAP association has been initiated with a remote host.

-   _EAP-context_ —A unique identifier for the EAP session, displayed as an eight-digit hexadecimal number (for example, 0x2D890AE0)

**Recommended Action** None required.

### 333002

**Error Message** `%ASA-5-333002: Timeout waiting for EAP response - context:_EAP-context_`

**Explanation** A timeout occurred while waiting for an EAP response.

-   _EAP-context_ —A unique identifier for the EAP session displayed as an eight-digit hexadecimal number (for example, 0x2D890AE0)

**Recommended Action** None required.

### 333003

**Error Message** `%ASA-6-333003: EAP association terminated - context:_EAP-context_`

**Explanation** The EAP association has been terminated with the remote host.

-   _EAP-context_ —A unique identifier for the EAP session displayed as an eight-digit hexadecimal number (for example, 0x2D890AE0)

**Recommended Action** None required.

### 333004

**Error Message** `%ASA-7-333004: EAP-SQ response invalid - context:_EAP-context_`

**Explanation** The EAP-Status Query response failed basic packet validation.

-   _EAP-context_ —A unique identifier for the EAP session displayed as an eight-digit hexadecimal number (for example, 0x2D890AE0)

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 333005

**Error Message** `%ASA-7-333005: EAP-SQ response contains invalid TLV(s) - context:_EAP-context_`

**Explanation** The EAP-Status Query response has one or more invalid TLVs.

-   _EAP-context_ —A unique identifier for the EAP session displayed as an eight-digit hexadecimal number (for example, 0x2D890AE0)

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 333006

**Error Message** `%ASA-7-333006: EAP-SQ response with missing TLV(s) - context:_EAP-context_`

**Explanation** The EAP-Status Query response is missing one or more mandatory TLVs.

-   _EAP-context_ —A unique identifier for the EAP session displayed as an eight-digit hexadecimal number (for example, 0x2D890AE0)

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 333007

**Error Message** `%ASA-7-333007: EAP-SQ response TLV has invalid length - context:_EAP-context_`

**Explanation** The EAP-Status Query response includes a TLV with an invalid length.

-   _EAP-context_ —A unique identifier for the EAP session displayed as an eight-digit hexadecimal number (for example, 0x2D890AE0)

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 333008

**Error Message** `%ASA-7-333008: EAP-SQ response has invalid nonce TLV - context:_EAP-context_`

**Explanation** The EAP-Status Query response includes an invalid nonce TLV.

-   _EAP-context_ —A unique identifier for the EAP session displayed as an eight-digit hexadecimal number (for example, 0x2D890AE0)

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 333009

**Error Message** `%ASA-6-333009: EAP-SQ response MAC TLV is invalid - context:_EAP-context_`

**Explanation** The EAP-Status Query response includes a MAC that does not match the calculated MAC.

-   _EAP-context_ —A unique identifier for the EAP session displayed as an eight-digit hexadecimal number (for example, 0x2D890AE0)

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 333010

**Error Message** `%ASA-5-333010: EAP-SQ response Validation Flags TLV indicates PV request - context:_EAP-context_`

**Explanation** The EAP-Status Query response includes a validation flags TLV, which indicates that the peer requested a full posture validation.

**Recommended Action** None required.

### 334001

**Error Message** `%ASA-6-334001: EAPoUDP association initiated - host-address`

**Explanation** An EAPoUDP association has been initiated with a remote host.

-   _host-address_ —The IP address of the host in dotted decimal format (for example, 10.86.7.101)

**Recommended Action** None required.

### 334002

**Error Message** `%ASA-5-334002: EAPoUDP association successfully established - _host-address_`

**Explanation** An EAPoUDP association has been successfully established with the host.

-   _host-address_ —The IP address of the host in dotted decimal format (for example, 10.86.7.101)

**Recommended Action** None required.

### 334003

**Error Message** `%ASA-5-334003: EAPoUDP association failed to establish - _host-address_`

**Explanation** An EAPoUDP association has failed to establish with the host.

-   _host-address_ —The IP address of the host in dotted decimal format (for example, 10.86.7.101)

**Recommended Action** Verify the configuration of the Cisco Secure Access Control Server.

### 334004

**Error Message** `%ASA-6-334004: Authentication request for NAC Clientless host - _host-address_`

**Explanation** An authentication request was made for a NAC clientless host.

-   _host-address_ —The IP address of the host in dotted decimal format (for example, 10.86.7.101)

**Recommended Action** None required.

### 334005

**Error Message** `%ASA-5-334005: Host put into NAC Hold state - _host-address_`

**Explanation** The NAC session for the host was put into the Hold state.

-   _host-address_ —The IP address of the host in dotted decimal format (for example, 10.86.7.101)

**Recommended Action** None required.

### 334006

**Error Message** `%ASA-5-334006: EAPoUDP failed to get a response from host - _host-address_`

**Explanation** An EAPoUDP response was not received from the host.

-   _host-address_ —The IP address of the host in dotted decimal format (for example, 10.86.7.101)

**Recommended Action** None required.

### 334007

**Error Message** `%ASA-6-334007: EAPoUDP association terminated - _host-address_`

**Explanation** An EAPoUDP association has terminated with the host.

-   _host-address_ —The IP address of the host in dotted decimal format (for example, 10.86.7.101)

**Recommended Action** None required.

### 334008

**Error Message** `%ASA-6-334008: NAC EAP association initiated - _host-address_ , EAP context: _EAP-context_`

**Explanation** EAPoUDP has initiated EAP with the host.

-   _host-address_ —The IP address of the host in dotted decimal format (for example, 10.86.7.101)
-   _EAP-context_ —A unique identifier for the EAP session displayed as an eight-digit, hexadecimal number (for example, 0x2D890AE0)

**Recommended Action** None required.

### 334009

**Error Message** `%ASA-6-334009: Audit request for NAC Clientless host - _Assigned_IP._`

**Explanation** An audit request is being sent for the specified assigned IP address.

-   _Assigned\_IP_ —The IP address assigned to the client

**Recommended Action** None required.

### 335001

**Error Message** `%ASA-6-335001: NAC session initialized - _host-address_`

**Explanation** A NAC session has started for a remote host.

-   _host-address_ —The IP address of the host in dotted decimal format (for example, 10.86.7.101)

**Recommended Action** None required.

### 335002

**Error Message** `%ASA-5-335002: Host is on the NAC Exception List - _host-address_ , OS: _oper-sys_`

**Explanation** The client is on the NAC Exception List and is therefore not subject to posture validation.

-   _host-address_ —The IP address of the host in dotted decimal format (for example, 10.1.1.1)
-   _oper-sys_ —The operating system (for example, Windows XP) of the host

**Recommended Action** None required.

### 335003

**Error Message** `%ASA-5-335003: NAC Default ACL applied, ACL:_ACL-name_ - _host-address_`

**Explanation** The NAC default ACL has been applied for the client.

-   _ACL-name_ —The name of the ACL being applied
-   _host-address_ —The IP address of the host in dotted decimal format (for example, 10.1.1.1)

**Recommended Action** None required.

### 335004

**Error Message** `%ASA-6-335004: NAC is disabled for host - _host-address_`

**Explanation** NAC is disabled for the remote host.

-   _host-address_ —The IP address of the host in dotted decimal format (for example, 10.1.1.1)

**Recommended Action** None required.

### 335005

**Error Message** `%ASA-4-335005: NAC Downloaded ACL parse failure - _host-address_`

**Explanation** Parsing of a downloaded ACL failed.

-   _host-address_ —The IP address of the host in dotted decimal format (for example, 10.1.1.1)

**Recommended Action** Verify the configuration of the Cisco Secure Access Control Server.

### 335006

**Error Message** `%ASA-6-335006: NAC Applying ACL: ACL-name - _host-address_`

**Explanation** The name of the ACL that is being applied as a result of NAC posture validation.

-   _ACL-name_ —The name of the ACL being applied
-   _host-address_ —The IP address of the host in dotted decimal format (for example, 10.1.1.1)

**Recommended Action** None required.

### 335007

**Error Message** `%ASA-7-335007: NAC Default ACL not configured - _host-address_`

**Explanation** A NAC default ACL has not been configured.

-   _host-address_ —The IP address of the host in dotted decimal format (for example, 10.1.1.1)

**Recommended Action** None required.

### 335008

**Error Message** `%ASA-5-335008: NAC IPsec terminate from dynamic ACL: _ACL-name_ - _host-address_`

**Explanation** A dynamic ACL obtained as a result of PV requires IPsec termination.

-   _ACL-name_ —The name of the ACL being applied
-   _host-address_ —The IP address of the host in dotted decimal format (for example, 10.1.1.1)

**Recommended Action** None required.

### 335009

**Error Message** `%ASA-6-335009: NAC Revalidate request by administrative action - _host-address_`

**Explanation** A NAC Revalidate action was requested by the administrator.

-   _host-address_ —The IP address of the host in dotted decimal format (for example, 10.1.1.1)

**Recommended Action** None required.

### 335010

**Error Message** `%ASA-6-335010: NAC Revalidate All request by administrative action - _num_ sessions`

**Explanation** A NAC Revalidate All action was requested by the administrator.

-   _num_ —A decimal integer that indicates the number of sessions to be revalidated

**Recommended Action** None required.

### 335011

**Error Message** `%ASA-6-335011: NAC Revalidate Group request by administrative action for _group-name_ group - _num_ sessions`

**Explanation** A NAC Revalidate Group action was requested by the administrator.

-   _group-name_ —The VPN group name
-   _num_ —A decimal integer that indicates the number of sessions to be revalidated

**Recommended Action** None required.

### 335012

**Error Message** `%ASA-6-335012: NAC Initialize request by administrative action - _host-address_`

**Explanation** A NAC Initialize action was requested by the administrator.

-   _host-address_ —The IP address of the host in dotted decimal format (for example, 10.1.1.1)

**Recommended Action** None required.

### 335013

**Error Message** `%ASA-6-335013: NAC Initialize All request by administrative action - _num_ sessions`

**Explanation** A NAC Initialize All action was requested by the administrator.

-   _num_ —A decimal integer that indicates the number of sessions to be revalidated

**Recommended Action** None required.

### 335014

**Error Message** `%ASA-6-335014: NAC Initialize Group request by administrative action for _group-name_ group - _num_ sessions`

**Explanation** A NAC Initialize Group action was requested by the administrator.

-   _group-name_ —The VPN group name
-   _num_ —A decimal integer that indicates the number of sessions to be revalidated

**Recommended Action** None required.

### 336001

**Error Message** `%ASA-3-336001: IP-EIGRP(AS _desination_network_): _ddb_name as_num_ stuck in active state`

**Explanation** The SIA state means that an EIGRP router has not received a reply to a query from one or more neighbors within the time allotted (approximately three minutes). When this happens, EIGRP clears the neighbors that did not send a reply and logs an error message for the route that became active.

-   _destination\_network_ —The route that became active
-   _ddb\_name_ —IPv4
-   _as\_num_ —The EIGRP router

**Recommended Action** Check to see why the router did not get a response from all of its neighbors and why the route disappeared.

### 336002

**Error Message** `%ASA-3-336002: Handle not allocated in pool`

**Explanation** The EIGRP router is unable to find the handle for the next hop.

-   _handle\_id_ —The identity of the missing handle

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 336003

**Error Message** `%ASA-3-336003: Unable to alloc pkt buffer`

**Explanation** The DUAL software was unable to allocate a packet buffer. The Secure Firewall ASA may be out of memory.

-   _bytes_ —Number of bytes in the packet

**Recommended Action** Check to see if the Secure Firewall ASA is out of memory by entering the show mem or show tech command. If the problem persists, contact the Cisco TAC.

### 336004

**Error Message** `%ASA-3-336004: Negative refcount in pakdesc`

**Explanation** The reference count packet count became negative.

-   _pakdesc_ —Packet identifier

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 336005

**Error Message** `%ASA-3-336005: Flow control error`

**Explanation** The interface is flow blocked for multicast. Qelm is the queue element, and in this case, the last multicast packet on the queue for this particular interface.

-   _error_ —Error statement: Qelm on flow ready
-   _interface\_name_ —Name of the interface on which the error occurred

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 336006

**Error Message** `%ASA-3-336006: Peers exist on IIDB`

**Explanation** Peers still exist on a particular interface during or after cleanup of the IDB of the EIGRP.

-   _num_ —The number of peers
-   _interface\_name_ —The interface name

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 336007

**Error Message** `%ASA-3-336007: Anchor Count negative`

**Explanation** An error occurred and the count of the anchor became negative when it was released.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 336008

**Error Message** `%ASA-3-336008: Lingering DRDB deleting IIDB`

**Explanation** An interface is being deleted and some lingering DRDB exists.

-   network—The destination network
-   address—The nexthop address
-   interface—The nexthop interface
-   origin\_str—String defining the origin

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 336009

**Error Message** `%ASA-3-336009: _ddb_name_ _as_id_: Internal error`

**Explanation** An internal error occurred.

-   _ddb\_name_ —PDM name (for example, IPv4 PDM)
-   _as\_id_ —Autonomous system ID

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 336010

**Error Message** `%ASA-5-336010: IP-EIGRP(AS _ddb_name_): Neighbor _neighbor_address_(_interface_name_) is _event_state_: _event_reason_`

**Explanation** A neighbor went up or down.

-   _ddb\_name_ —IPv4
-   _tableid_ — Internal ID for the RIB
-   _as\_id_ —Autonomous system ID
-   _address_ —IP address of the neighbor
-   _interface_ —Name of the interface
-   _event\_msg_ — Event that is occurring for the neighbor (that is, up or down)
-   _msg_ —Reason for the event. Possible _event\_msg_ and _msg_ value pairs include:

\- resync: peer graceful-restart

\- down: holding timer expired

\- up: new adjacency

\- down: Auth failure

\- down: Stuck in Active

\- down: Interface PEER-TERMINATION received

\- down: K-value mismatch

\- down: Peer Termination received

\- down: stuck in INIT state

\- down: peer info changed

\- down: summary configured

\- down: Max hopcount changed

\- down: metric changed

\- down: \[No reason\]

**Recommended Action** Check to see why the link on the neighbor is going down or is flapping. This may be a sign of a problem, or a problem may occur because of this.

### 336011

**Error Message** `%ASA-6-336011: hw or sw error occurred`

**Explanation** A dual event occurred. The events can be one of the following:

-   Redist rt change
-   SIA Query while Active

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 337000

**Error Message** `%ASA-6-337000: Session created, NeighAddr: _Created BFD session with local discriminator _id_, SrcAddr: _real_interface__`

**Explanation** This syslog message indicates that a BFD active session has been created.

-   id— A numerical field that denotes the local discriminator value for a particular BFD session
-   real\_interface— The interface nameif on which the BFD session is running
-   real\_host\_ip— The IP address of the neighbor with which the BFD session has come up

**Recommended Action** None.

### 337001

**Error Message** `%ASA-6-337001: Session destroyed, NeighAddr: _Terminated BFD session with local discriminator _id_, SrcAddr: _real_interface__`

**Explanation** This syslog message indicates that an active BFD session has been terminated.

-   id— A numerical field that denotes the local discriminator value for a particular BFD session
-   real\_interface— The interface nameif on which the BFD session is running
-   real\_host\_ip— The IP address of the neighbor with which the BFD session has come up
-   failure\_reason— One of the following failure reasons: BFD going down on peer’s side, BFD configuration removal on peer’s side, Detection timer expiration, Echo function failure, Path to peer going down, Local BFD configuration removal, BFD client configuration removal

**Recommended Action** None.

### 337005

**Error Message** `%ASA-4-337005: _Phone Proxy SRTP: Media session not found for media_term_ip/media_term_port for packet from in_ifc:src_ip/src_port to out_ifc:dest_ip/dest_port_`

**Explanation** The adaptive security appliance received an SRTP or RTP packet that was destined to go to the media termination IP address and port, but the corresponding media session to process this packet was not found.

-   in\_ifc—The input interface
-   src\_ip—The source IP address of the packet
-   src\_port—The source port of the packet
-   out\_ifc—The output interface
-   dest\_ip—The destination IP address of the packet
-   dest\_port—The destination port of the packet.

**Recommended Action** If this message occurs at the end of the call, it is considered normal because the signaling messages may have released the media session, but the endpoint is continuing to send a few SRTP or RTP packets. If this message occurs for an odd-numbered media termination port, the endpoint is sending RTCP, which must be disabled from the CUCM. If this message happens continuously for a call, debug the signaling message transaction either using phone proxy debug commands or capture commands to determine if the signaling messages are being modified with the media termination IP address and port..

### 338001

**Error Message** `%ASA-4-338001: Dynamic Filter _monitored_ blacklisted _protocol_ traffic from _in_interface_:_src_ip_addr_/_src_port_ (_mapped-ip_/_mapped-port)_) to _out_interface_:_dest_ip_addr_/_dest_port_ (_mapped-ip_/_mapped-port),_), source _malicious_address_ resolved from _local_or_dynamic_ list: _domain_name_, threat-level: _level_value_, category: _category_name_`

**Explanation** Traffic from a domain, which is on an block list in the dynamic filter database, has appeared. The threat level is a string that shows one of the following values: none, very-low, low, moderate, high, and very-high. The category is a string that shows the reason why a domain name is on a block list (for example, botnet, Trojan, and spyware).

**Recommended Action** Access to a malicious site has been logged. Use the internal IP address to trace the infected machine, or enter the dynamic-filter drop blacklist command to automatically drop such traffic.

### 338002

**Error Message** `%ASA-4-338002: Dynamic Filter _monitored_ blacklisted _protocol_ traffic from _in_interface_:_src_ip_addr_/_src_port_ (_mapped-ip_/_mapped-port_) to _out_interface_:_dest_ip_addr_/_dest_port_ (_mapped-ip_/_mapped-port_), destination _malicious_address_ resolved from _local_or_dynamic_ list: _domain_name_, threat-level: _level_value_, category: _category_name_`

**Explanation** Traffic to a domain, which is on an block list in the dynamic filter database, has appeared. The threat level is a string that shows one of the following values: none, very-low, low, moderate, high, and very-high. The category is a string that shows the reason why a domain name is on a block list (for example, botnet, Trojan, and spyware).

**Recommended Action** Access to a malicious site has been logged. Use the internal IP address to trace the infected machine, or enter the dynamic-filter drop blacklist command to automatically drop such traffic.

### 338003

**Error Message** `%ASA-4-338003: Dynamic Filter _monitored_ blacklisted _protocol_ traffic from _in_interface_:_src_ip_addr_/_src_port_ (_mapped-ip_/_mapped-port)_) to _out_interface_:_dest_ip_addr_/_dest_port_ (_mapped-ip_/_mapped-port)_), source _malicious_address_ resolved from _local_or_dynamic_ list: _ip_address_/_netmask_, threat-level: _level_value_, category: _category_name_`

**Explanation** Traffic from an IP address, which is on an block list in the dynamic filter database, has appeared. The threat level is a string that shows one of the following values: none, very-low, low, moderate, high, and very-high. The category is a string that shows the reason why a domain name is on a block list (for example, botnet, Trojan, and spyware).

**Recommended Action** Access to a malicious site has been logged. Use the internal IP address to trace the infected machine, or enter the dynamic-filter drop blacklist command to automatically drop such traffic.

### 338004

**Error Message** `%ASA-4-338004: Dynamic Filter _monitored_ blacklisted _protocol_ traffic from _in_interface_:_src_ip_addr_/_src_port_ (_mapped-ip_/_mapped-port_) to _out_interface_:_dest_ip_addr_/_dest_port_ (_mapped-ip_/_mapped-port_), destination _malicious_address_ resolved from _local_or_dynamic_ list: _ip_address_/_netmask_, threat-level: _level_value_, category: _category_name_`

**Explanation** Traffic to an IP address, which is on an block list in the dynamic filter database, has appeared. The threat level is a string that shows one of the following values: none, very-low, low, moderate, high, and very-high. The category is a string that shows the reason why a domain name is on a block list (for example, botnet, Trojan, and spyware).

**Recommended Action** Access to a malicious site has been logged. Use the internal IP address to trace the infected machine, or enter the dynamic-filter drop command to automatically drop such traffic.

### 338005

**Error Message** `%ASA-4-338005: Dynamic Filter _dropped_ blacklisted _protocol_ traffic from _in_interface_:_src_ip_addr_/_src_port_ (_mapped-ip_/_mapped-port_) to _out_interface_:_dest_ip_addr_/_dest_port_ (_mapped-ip_/_mapped-port_), source _malicious_address_ resolved from _local_or_dynamic_ list: _domain_name_, threat-level: _level_value_, category: _category_name_`

**Explanation** Traffic from a domain name, which is on an block list in the dynamic filter database, was denied. The threat level is a string that shows one of the following values: none, very-low, low, moderate, high, and very-high. The category is a string that shows the reason why a domain name is on a block list (for example, botnet, Trojan, and spyware).

**Recommended Action** None required.

### 338006

**Error Message** `%ASA-4-338006: Dynamic Filter _dropped_ blacklisted _protocol_ traffic from _in_interface_:_src_ip_addr_/_src_port_ (_mapped-ip_/_mapped-port_) to _out_interface_:_dest_ip_addr_/_dest_port_ (_mapped-ip_/_mapped-port_), destination _malicious_address_ resolved from _local_or_dynamic_ list: _domain_name_, threat-level: _level_value_, category: _category_name_`

**Explanation** Traffic to a domain, which is on an block list in the dynamic filter database, was denied. The threat level is a string that shows one of the following values: none, very-low, low, moderate, high, and very-high. The category is a string that shows the reason why a domain name is on a block list (for example, botnet, Trojan, and spyware).

**Recommended Action** None required.

### 338007

**Error Message** `%ASA-4-338007: Dynamic Filter _dropped_ blacklisted _protocol_ traffic from _in_interface_:_src_ip_addr_/_src_port_ (_mapped-ip_/_mapped-port_) to _out_interface_:_dest_ip_addr_/_dest_port_ (_mapped-ip_/_mapped-port_), source _malicious_address_ resolved from _local_or_dynamic_ list: _ip_address_/_netmask_, threat-level: _level_value_, category: _category_name_`

**Explanation** Traffic from an IP address, which is on an block list in the dynamic filter database, was denied. The threat level is a string that shows one of the following values: none, very-low, low, moderate, high, and very-high. The category is a string that shows the reason why a domain name is on a block list (for example, botnet, Trojan, and spyware).

**Recommended Action** None required.

### 338008

**Error Message** `%ASA-4-338008: Dynamic Filter _dropped_ blacklisted _protocol_ traffic from _in_interface_:_src_ip_addr_/_src_port_ (_mapped-ip_/_mapped-port_) to _out_interface_:_dest_ip_addr_/_dest_port_ (_mapped-ip_/_mapped-port_), destination _malicious_address_ resolved from _local_or_dynamic_ list: _ip_address_/_netmask_, threat-level: _level_value_, category: _category_name_`

**Explanation** Traffic to an IP address, which is on an block list in the dynamic filter database, was denied. The threat level is a string that shows one of the following values: none, very-low, low, moderate, high, and very-high. The category is a string that shows the reason why a domain name is on a block list (for example, botnet, Trojan, and spyware).

**Recommended Action** None required.

### 338101

**Error Message** `%ASA-4-338101: Dynamic Filter _action_ whitelisted _protocol_ traffic from _in_interface_:_src_ip_addr_/_src_port_ (_mapped-ip_/_mapped-port_) to _out_interface_:_dest_ip_addr_/_dest_port_ (_mapped-ip_/_mapped-port_), source _malicious_address_ resolved from _local_or_dynamic_ list: _domain_name_`

**Explanation** Traffic from a domain, which is on an allow list in the dynamic filter database, has appeared.

**Recommended Action** None required.

### 338102

**Error Message** `%ASA-4-338102: Dynamic Filter _action_ whitelisted _protocol_ traffic from _in_interface_:_src_ip_addr_/_src_port_ (_mapped-ip_/_mapped-port_) to _out_interface_:_dest_ip_addr_/_dest_port_ (_mapped-ip_/_mapped-port_), destination _malicious_address_ resolved from _local_or_dynamic_ list: _domain_name_`

**Explanation** Traffic to a domain name, which is on an allow list in the dynamic filter database, has appeared.

**Recommended Action** None required.

### 338103

**Error Message** `%ASA-4-338103: Dynamic Filter _action_ whitelisted _protocol_ traffic from _in_interface_:_src_ip_addr_/_src_port_ (_mapped-ip_/_mapped-port)_) to _out_interface_:_dest_ip_addr_/_dest_port_ (_mapped-ip_/_mapped-port_), source _malicious_address_ resolved from _local_or_dynamic_ list: _ip_address_/_netmask_`

**Explanation** Traffic from an IP address, which is on an allow list in the dynamic filter database, has appeared.

**Recommended Action** None required.

### 338104

**Error Message** `%ASA-4-338104: Dynamic Filter _action_ whitelisted _protocol_ traffic from _in_interface_:_src_ip_addr_/_src_port_ (_mapped-ip_/_mapped-port_) to _out_interface_:_dest_ip_addr_/_dest_port_ (_mapped-ip_/_mapped-port_), destination _malicious_address_ resolved from _local_or_dynamic_ list: _ip_address_/_netmask_`

**Explanation** Traffic to an IP address, which is on an allow list in the dynamic filter database, has appeared.

**Recommended Action** None required.

### 338201

**Error Message** `%ASA-4-338201: Dynamic Filter _monitored_ greylisted _protocol_ traffic from _in_interface_:_src_ip_addr_/_src_port_ (_mapped-ip_/_mapped-port)_) to _out_interface_:_dest_ip_addr_/_dest_port_ (_mapped-ip_/_mapped-port)_), source _malicious_address_ resolved from _local_or_dynamic_ list: _domain_name_, threat-level: _level_value_, category: _category_name_`

**Explanation** Traffic from a domain, which is on a greylist in the dynamic filter database, has appeared. The threat level is a string that shows one of the following values: none, very-low, low, moderate, high, and very-high. The category is a string that shows the reason why a domain name is on a block list (for example, botnet, Trojan, and spyware).

**Recommended Action** Access to a malicious site has been logged. Use the internal IP address to trace the infected machine, or enter the dynamic-filter drop blacklist command and the dynamic-filter ambiguous-is-black command to automatically drop such traffic.

### 338202

**Error Message** `%ASA-4-338202: Dynamic Filter _monitored_ greylisted _protocol_ traffic from _in_interface_:_src_ip_addr_/_src_port_ (_mapped-ip_/_mapped-port_) to _out_interface_:_dest_ip_addr_/_dest_port_ (_mapped-ip_/_mapped-port_), destination _malicious_address_ resolved from _local_or_dynamic_ list: _domain_name_, threat-level: _level_value_, category: _category_name_`

**Explanation** Traffic to a domain name, which is on a gerylist in the dynamic filter database, has appeared. The threat level is a string that shows one of the following values: none, very-low, low, moderate, high, and very-high. The category is a string that shows the reason why a domain name is on a block list (for example, botnet, Trojan, and spyware).

**Recommended Action** Access to a malicious site has been logged. Use the internal IP address to trace the infected machine, or enter the dynamic-filter drop blacklist command and the dynamic-filter ambiguous-is-black command to automatically drop such traffic.

### 338203

**Error Message** `%ASA-4-338203: Dynamic Filter _dropped_ greylisted _protocol_ traffic from _in_interface_:_src_ip_addr_/_src_port_ (_mapped-ip_/_mapped-port_) to _out_interface_:_dest_ip_addr_/_dest_port_ (_mapped-ip_/_mapped-port_), source _malicious_address_ resolved from _local_or_dynamic_ list: _domain_name_, threat-level: _level_value_, category: _category_name_`

**Explanation** Traffic from a greylisted domain name in the dynamic filter database was denied; however, the malicious IP address was also resolved to domain names that are unknown to the dynamic filter database. The threat level is a string that shows one of the following values: none, very-low, low, moderate, high, and very-high. The category is a string that shows the reason why a domain name is on a block list (for example, botnet, Trojan, and spyware).

**Recommended Action** Access to a malicious site was dropped. If you do not want to automatically drop greylisted traffic whose IP address matches both unknown domain names, and domain names, which are on a block list, disable the dynamic-filter ambiguous-is-black command.

### 338204

**Error Message** `%ASA-4-338204: Dynamic Filter _dropped_ greylisted _protocol_ traffic from _in_interface_:_src_ip_addr_/_src_port_ (_mapped-ip_/_mapped-port_) to _out_interface_:_dest_ip_addr_/_dest_port_ (_mapped-ip_/_mapped-port_), destination _malicious_address_ resolved from _local_or_dynamic_ list: _domain_name_, threat-level: _level_value_, category: _category_name_`

**Explanation** Traffic to a greylisted domain name in the dynamic filter database was denied; however, the malicious IP address was also resolved to domain names that are unknown to the dynamic filter database. The threat level is a string that shows one of the following values: none, very-low, low, moderate, high, and very-high. The category is a string that shows the reason why a domain name is on a block list (for example, botnet, Trojan, and spyware).

**Recommended Action** Access to a malicious site was dropped. If you do not want to automatically drop greylisted traffic whose IP address matches both unknown domain names, and domain names, which are on a block list, disable the dynamic-filter ambiguous-is-black command.

### 338301

**Error Message** `%ASA-4-338301: Intercepted DNS reply for name _name_ from _in_interface_:_src_ip_addr_/_src_port_ to _out_interface_:_dest_ip_addr_/_dest_port_, matched _list_`

**Explanation** A DNS reply that was present in an administrator's allow list, block list, or IronPort list was intercepted.

-   _name—_ The domain name
-   _list_ —The list that includes the domain name, administrator allow list, block list, or IronPort list

**Recommended Action** None required.

### 338302

**Error Message** `%ASA-5-338302: Address _ipaddr_ discovered for domain _name_ from _list_. Adding rule`

**Explanation** An IP address that was discovered from a DNS reply to the dynamic filter rule table was added.

-   _ipaddr—_ The IP address from the DNS reply
-   _name—_ The domain name
-   _list_ —The list that includes the domain name, administrator block list, or IronPort list

**Recommended Action** None required.

### 338303

**Error Message** `%ASA-5-338303: Address _ipaddr_ (_name)_) timed out. Removing rule`

**Explanation** An IP address that was discovered from the dynamic filter rule table was removed.

-   _ipaddr—_ The IP address from the DNS reply
-   _name—_ The domain name

**Recommended Action** None required.

### 338304

**Error Message** `%ASA-6-338304: Successfully downloaded dynamic filter data file from updater server _url_`

**Explanation** A new version of the data file has been downloaded.

-   _url_ —The URL of the updater server

**Recommended Action** None required.

### 338305

**Error Message** `%ASA-3-338305: Failed to download dynamic filter data file from updater server _url_`

**Explanation** The dynamic filter database has failed to download.

-   _url_ —The URL of the updater server

**Recommended Action** Make sure that you have a DNS configuration on the ASA so that the updater server URL can be resolved. If you cannot ping the server from the ASA, check with your network administrator for the correct network connection and routing configuration. If you are still having problems, contact the Cisco TAC.

### 338306

**Error Message** `%ASA-3-338306: Failed to authenticate with dynamic filter updater server _url_`

**Explanation** The ASA failed to authenticate with the dynamic filter updater server.

-   _url_ —The URL of the updater server

**Recommended Action** Contact the Cisco TAC.

### 338307

**Error Message** `%ASA-3-338307: Failed to decrypt downloaded dynamic filter data file`

**Explanation** The downloaded dynamic filter database file failed to decrypt.

**Recommended Action** Contact the Cisco TAC.

### 338308

**Error Message** `%ASA-5-338308: Dynamic Filter updater server dynamically changed from _old_server_host_:_old_server_port_ to _new_server_host_:_new_server_port_`

**Explanation** The ASA was directed to a new updater server host or port.

-   _old\_server\_host_ :_old\_server\_port_ —The previous updater server host and port
-   _new\_server\_host_ :_new\_server\_port_ —The new updater server host and port

**Recommended Action** None required.

### 338309

**Error Message** `%ASA-3-338309: The license on this _device_ does not support dynamic filter updater feature`

**Explanation** The dynamic filter updater is a licensed feature; however, the license on the ASA does not support this feature.

**Recommended Action** None required.

### 338310

**Error Message** `%ASA-3-338310: Failed to update from dynamic filter updater server _url,_, reason: _reason_string_`

**Explanation** The ASA failed to receive an update from the dynamic filter updater server.

-   _url—_ The URL of the updater server
-   _reason string_ —The reason for the failure, which can be one of the following:

\- Failed to connect to updater server

\- Received invalid server response

\- Received invalid server manifest

\- Error in stored update file information

\- Script error

\- Function call error

\- Out of memory

**Recommended Action** Check the network connection to the server. Try to ping the server URL, which is shown in the output of the show dynamic-filter updater-client command. Make sure that the port is allowed through your network. If the network connection is not the problem, contact your network administrator.

### 339001

**Error Message** `%ASA-3-339001: DNSCRYPT certificate update failed for _<num_tries>_ tries.`

**Explanation** The DNSCrypt failed to receive a certificate update.

-   _num\_tries—_ The number of times DNSCrypt failed to get a certificate update

**Recommended Action** Check for the following:

-   If the route is setup for the Umbrella server.
    
-   If the Umbrella server egress interface is up.
    
-   If the correct Provider public key is used.
    

### 339002

**Error Message** `%ASA-3-339002: Umbrella device registration failed with error code _<err_code>_`

**Explanation** The umbrella device registration failed.

-   _err\_code—_ The error code returned from the Umbrella Server.

**Recommended Action** If the error code is:

-   400 – There is a problem with the request format or content. The token is probably too short or corrupted. Verify if the token matches what is on the Umbrella Dashboard.
    
-   401 – The token is not authorized. If the token was refreshed on the Umbrella Dashboard, then the new token should be updated on ASA.
    
-   409 – The device id is conflicting with another organization. Contact the Umbrella Server Administrator.
    
-   500 – There is an internal server error. Contact the Umbrella Server Administrator.
    

### 339003

**Error Message** `%ASA-3-339003: Umbrella device registration was successful.`

**Explanation** Successful message for the umbrella device registration.

**Recommended Action** None.

### 339004

**Error Message** `%ASA-3-339004: Umbrella device registration failed due to missing token`

**Explanation** Umbrella device registration failed due to missing token.

**Recommended Action** Make sure the token is configured under the global “umbrella” submode.

### 339005

**Error Message** `%ASA-3-339005: Umbrella device registration failed after _<num_tries>_ retries`

**Explanation** Umbrella device registration failed.

-   _num\_tries—_ The number of times the device failed to register with the Umbrella Server.

**Recommended Action** Locate the error code in the syslog 339002 message. Refer the workaround for the 339002 syslog message and fix.

### 339006

**Error Message** `%ASA-3-339006: Umbrella resolver _current_resolver_ipv46_ is reachable. Resuming redirect`

**Explanation** Umbrella had failed to open, and the resolver was unreachable. The resolver is now reacheable and service is resumed.

**Recommended Action**None.

### 339007

**Error Message** `%ASA-3-339007: Umbrella resolver _current_resolver_ipv46_ is unreachable, moving to fail-open. Starting probe to resolver`

**Explanation** Umbrella fail-open has been configured and a resolver unreachabilty has been detected.

**Recommended Action**Check the network settings for reachability to the Umbrella resolvers.

### 339008

**Error Message** `%ASA-3-339008: Umbrella resolver _current_resolver_ipv46_ is unreachable, moving to fail-close`

**Explanation** Umbrella fail-open has NOT been configured and a resolver unreachabilty has been detected.

**Recommended Action**Check the network settings for reachability to the Umbrella resolvers.

### 339010

**Error Message** `%ASA-6-339010: Umbrella API token request was successful.`

**Explanation** This message appears when the request for umbrella API token was successful.

**Recommended Action** None.

### 339011

**Error Message** `%ASA-3-339011: Umbrella API token request received no responses.`

**Explanation** This message appears when the request for umbrella API token has not received any response from the server.

**Recommended Action** None.

### 339012

**Error Message** `%ASA-3-339012: Umbrella API token request failed with error code _error_code_.`

**Explanation** This message appears when the request for umbrella API token has failed.

**Recommended Action** None.

### 339013

**Error Message** `%ASA-3-339013: Umbrella API token request failed in response processing.`

**Explanation** This message appears when the request for umbrella API token has failed while processing the response.

**Recommended Action** None.

### 339014

**Error Message** `%ASA-3-339014: Umbrella API token request failed after _retry_number_ retries.`

**Explanation** This message appears when the request for umbrella API token has failed after retries.

**Recommended Action** None.

### 340001

**Error Message** `%ASA-3-340001: Vnet-proxy handshake error _error_string_ - _context_id_ (_version_)`

**Explanation** Loopback proxy allows third-party applications running on the Secure Firewall ASA to access the network. The loopback proxy encountered an error.

-   _context\_id—_ A unique, 32-bit context ID that is generated for each loopback client proxy request
-   _version_ —The protocol version
-   _request\_type_ —The type of request, which can be one of the following: TC (TCP connection), TB (TCP bind), or UA (UDP association)
-   _address\_type_ —The types of addresses, which can be one of the following: IP4 (IPv4), IP6 (IPv6), or DNS (domain name service)
-   _client\_address\_internal/server\_address\_internal—_ The addresses that the loopback client and the loopback server used for communication
-   _client\_port\_internal_ /_server\_port\_internal—_ The ports that the loopback client and the loopback server used for communication
-   _server\_address\_external_ /_remote\_address\_external_ —The addresses that the loopback server and the remote host used for communication
-   _server\_port\_external_ /_remote\_port\_external_ —The ports that the loopback server and the remote host used for communication
-   _error\_string_ —The error string that may help troubleshoot the problem

**Recommended Action** Copy the syslog message and contact the Cisco TAC.

### 340002

**Error Message** `%ASA-6-340002: Vnet-proxy data relay error _error_string_ from _context_id_/_version_ to _request_type_/_address_type_ - _client_address_internal_ (_client_port_internal_)`

**Explanation** Loopback proxy allows third-party applications running on the Secure Firewall ASA to access the network. The loopback proxy generated debugging information for use in troubleshooting.

-   _context\_id—_ A unique, 32-bit context ID that is generated for each loopback client proxy request
-   _version_ —The protocol version
-   _request\_type_ —The type of request, which can be one of the following: TC (TCP connection), TB (TCP bind), or UA (UDP association)
-   _address\_type_ —The types of addresses, which can be one of the following: IP4 (IPv4), IP6 (IPv6), or DNS (domain name service)
-   _client\_address\_internal/server\_address\_internal—_ The addresses that the loopback client and the loopback server used for communication
-   _client\_port\_internal_ /_server\_port\_internal—_ The ports that the loopback client and the loopback server used for communication
-   _server\_address\_external_ /_remote\_address\_external_ —The addresses that the loopback server and the remote host used for communication
-   _server\_port\_external_ /_remote\_port\_external_ —The ports that the loopback server and the remote host used for communication
-   _error\_string_ —The error string that may help troubleshoot the problem

**Recommended Action** Copy the syslog message and contact the Cisco TAC.

### 341001

**Error Message** `%ASA-6-341001: Policy Agent started successfully for VNMC _vnmc_ip_addr_`

**Explanation** The policy agent processes (DME, ducatiAG, and commonAG) started successfully.

-   _vnmc\_ip\_addr_ —-The IP address of the VNMC server

**Recommended Action** None.

### 341002

**Error Message** `%ASA-6-341002: Policy Agent stopped successfully for VNMC _vnmc_ip_addr_`

**Explanation** The policy agent processes (DME, ducatiAG, and commonAG) were stopped.

-   _vnmc\_ip\_addr_ —-The IP address of the VNMC server

**Recommended Action** None.

### 341003

**Error Message** `%ASA-3-341003: Policy Agent failed to start for VNMC _vnmc_ip_addr_`

**Explanation** The policy agent failed to start.

-   _vnmc\_ip\_addr_ —-The IP address of the VNMC server

**Recommended Action** Check for console history and the disk0:/pa/log/vnm\_pa\_error\_status for error messages. To retry starting the policy agent, issue the registration host command again.

### 341004

**Error Message** `%ASA-3-341004: Storage device not available. Attempt to shutdown module _module_name_ failed.`

**Explanation** All SSDs have failed or been removed with the system in Up state. The system has attempted to shut down the software module, but that attempt has failed.

-   _%s_ —The software module (for example, cxsc)

**Recommended Action** Replace the remved or failed drive and reload the Secure Firewall ASA.

### 341005

**Error Message** `%ASA-3-341005: Storage device not available. Shutdown issued for module _module_name_.`

**Explanation** All SSDs have failed or been removed with the system in Up state. The system is shutting down the software module.

-   _%s_ —The software module (for example, cxsc)

**Recommended Action** Replace the removed or failed drive and reload the software module.

### 341006

**Error Message** `%ASA-3-341006: Storage device not available. Failed to stop recovery of module _module_name_.`

**Explanation** All SSDs have failed or been removed with the system in recorvery state. The system attempted to stop the recover, but that attempt failed.

-   _%s_ —The software module (for example, cxsc)

**Recommended Action** Replace the removed or failed drive and reload the Secure Firewall ASA.

### 341007

**Error Message** `%ASA-3-341007: Storage device not available. Further recovery of module _module_name_ was stopped. This may take several minutes to complete.`

**Explanation** All SSDs have failed or been removed with the system in recovery state. The system is stopping the recovery of the softwaremodule.

-   _%s_ —The software module (for example, cxsc)

**Recommended Action** Replace the removed or failed drive and reload the software module.

### 341008

**Error Message** `%ASA-3-341008: Storage device not found. Auto-boot of module _module_name_ cancelled. Install drive and reload to try again.`

**Explanation** After getting the system into Up state, all SSDs have failed or been removed before reloading the system. Because the default action during boot is to auto-boot the software module, that action is blocked because there is no storage device available.

**Recommended Action** Replace the removed or failed drive and reload the software module.

### 341010

**Error Message** `%ASA-6-341010: Storage device with serial number _ser_no_ _[inserted_into|removed_from]_ bay _bay_no_`

**Explanation** The Secure Firewall ASA has detected insertion or removal events and generates this syslog message immediately.

**Recommended Action** None required.

### 341011

**Error Message** `%ASA-3-341011: Storage device with serial number _ser_no_ in bay _bay_no_ faulty`

**Explanation** The Secure Firewall ASA polls the hard disk drive (HDD) health status every 10 minutes and generates this syslog message if the HDD is in a failed state.

**Recommended Action** None required.

### 342001

**Error Message** `%ASA-7-342001: The REST API Agent was successfully started.`

**Explanation** The REST API Agent must be successfully started before a REST API Client can configure the ASA.

**Recommended Action** None.

### 342002

**Error Message** `%ASA-3-342002: REST API Agent failed, reason: _reason_.`

**Explanation** The REST API Agent could fail to start or crash for various reasons, and the reason is specified.

-   _reason_ —The cause for the REST API failure

**Recommended Action** The actions taken to resolve the issue vary depending on the reason logged. For example, the REST API Agent crashes when the Java process runs out of memory. If this occurs, you need to restart the REST API Agent. If the restart is not successful, contact the Cisco TAC to identify the root cause fix.

### 342003

**Error Message** `%ASA-3-342003: REST API Agent failure notification received. Agent will be restarted automatically.`

**Explanation** A failure notification from the REST API Agent has been received and a restart of the Agent is being attempted.

**Recommended Action** None.

### 342004

**Error Message** `%ASA-3-342004: Failed to automatically restart the REST API Agent after _num_ unsuccessful attempts. Use the 'no rest-api agent' and 'rest-api agent' commands to manually restart the Agent.`

**Explanation** The REST API Agent has failed to start after many attempts.

**Recommended Action** See syslog %ASA-3-342002 (if logged) to better understand the reason behind the failure. Try to disable the REST API Agent by entering the no rest-api agent command and re-enable the REST API Agent using the rest-api agent command.

### 342005

**Error Message** `%ASA-7-342005: REST API image has been successfully installed.`

**Explanation** The REST API image must be successfully installed before starting the REST API Agent.

**Recommended Action** None.

### 342006

**Error Message** `%ASA-3-342006: Failed to install REST API image, reason: _reason_.`

**Explanation** The REST API image installation may fail, for one of the following reasons: version check failed, image verification failed, image file not found, out of space on flash or mount failed.

**Recommended Action** The administrator should fix the failure and try to install the image again using ‘rest-api image <image>’.

### 342007

**Error Message** `%ASA-7-342007: REST API image has been successfully uninstalled.`

**Explanation** The old REST API image must be successfully uninstalled before a new one can be installed.

**Recommended Action** None.

### 342008

**Error Message** `%ASA-3-342008: Failed to uninstall REST API image, reason: _reason_.`

**Explanation** The REST API image could not be uninstalled for the following reasons- unmount failed or REST Agent is enabled.

**Recommended Action** The administrator should disable the REST Agent, before trying to uninstall the REST API image.