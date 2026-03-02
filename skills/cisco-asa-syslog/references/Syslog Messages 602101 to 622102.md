## Messages 602101 to 609002

This section includes messages from 602101 to 609002.

### 602101

**Error Message** `%ASA-6-602101: PMTU-D packet _number_ bytes greater than effective mtu _number_, dest_addr=_dest_address_, src_addr=_source_address_, prot=_protocol_`

**Explanation** The Secure Firewall ASA sent an ICMP destination unreachable message and fragmentation is needed.

**Recommended Action** Make sure that the data is sent correctly.

### 602103

**Error Message** `%ASA-6-602103: IPSEC: Received an ICMP Destination Unreachable from _src_addr_ with suggested PMTU of _rcvd_mtu_; PMTU updated for SA with peer _peer_addr_, SPI _spi_, tunnel name _username_, old PMTU _old_mtu_, new PMTU _new_mtu_`

**Explanation** The MTU of an SA was changed. When a packet is received for an IPsec tunnel, the corresponding SA is located and the MTU is updated based on the MTU suggested in the ICMP packet. If the suggested MTU is greater than 0 but less than 256, then the new MTU is set to 256. If the suggested MTU is 0, the old MTU is reduced by 256 or it is set to 256—whichever value is greater. If the suggested MTU is greater than 256, then the new MTU is set to the suggested value.

-   src\_addr—IP address of the PMTU sender
-   rcvd\_mtu—Suggested MTU received in the PMTU message
-   peer\_addr—IP address of the IPsec peer
-   spi—IPsec Security Parameter Index
-   username—Username associated with the IPsec tunnel
-   old\_mtu—Previous MTU associated with the IPsec tunnel
-   new\_mtu—New MTU associated with the IPsec tunnel

**Recommended Action** None required.

### 602104

**Error Message** `%ASA-6-602104: IPSEC: Received an ICMP Destination Unreachable from _src_addr_, PMTU is unchanged because suggested PMTU of _rcvd_mtu_ is equal to or greater than the current PMTU of _curr_mtu_, for SA with peer _peer_addr_, SPI _spi_, tunnel name _username_`

**Explanation** An ICMP message was received indicating that a packet sent over an IPsec tunnel exceeded the path MTU, and the suggested MTU was greater than or equal to the current MTU. Because the MTU value is already correct, no MTU adjustment is made. This may happen when multiple PMTU messages are received from different intermediate stations, and the MTU is adjusted before the current PMTU message is processed.

-   src\_addr—IP address of the PMTU sender
-   rcvd\_mtu—Suggested MTU received in the PMTU message
-   curr\_mtu—Current MTU associated with the IPsec tunnel
-   peer\_addr—IP address of the IPsec peer
-   spi—IPsec Security Parameter Index
-   _username_ —Username associated with the IPsec tunnel

**Recommended Action** None required.

### 602303

**Error Message** `%ASA-6-602303: IPSEC: An _direction_ _tunnel_type_ SA (SPI= _spi_) between _local_IP_ and _remote_IP_ (user= _username_) has been created.`

**Explanation** A new SA was created.

-   direction—SA direction (inbound or outbound)
-   tunnel\_type—SA type (remote access or L2L)
-   spi—IPsec Security Parameter Index
-   local\_IP—IP address of the tunnel local endpoint
-   remote\_IP—IP address of the tunnel remote endpoint
-   _\>username_ —Username associated with the IPsec tunnel

**Recommended Action** None required.

### 602304

**Error Message** `%ASA-6-602304: IPSEC: An _direction_ _tunnel_type_ SA (SPI= _spi_) between _local_IP_ and _remote_IP_ (user= _username_) has been deleted.`

**Explanation** An SA was deleted.

-   direction—SA direction (inbound or outbound)
-   tunnel\_type—SA type (remote access or L2L)
-   spi—IPsec Security Parameter Index
-   local\_IP—IP address of the tunnel local endpoint
-   remote\_IP—IP address of the tunnel remote endpoint
-   _\>username_ —Username associated with the IPsec tunnel

**Recommended Action** None required.

### 602305

**Error Message** `%ASA-3-602305: IPSEC: SA creation error, source _source_address_, destination _destination_address_, reason _error_string_.`

**Explanation** An error has occurred while creating an IPsec security association.

**Recommended Action** This is typically a transient error condition. If this message occurs consistently, contact the Cisco TAC.

### 602306

**Error Message** `%ASA-3-602306: IPSEC: SA change peer IP error, SPI: _IPsec_SPI_, (src _original_src_IP_address_/_original_src_port_, dest _original_dest_IP_address_/_original_dest_port_ => src _new_src_IP_address_/_new_src_port_, dest: _new_dest_IP_address_/_new_dest_port_), reason _failure_reason_.`

**Explanation** An error has occurred while updating an IPsec tunnel’s peer address for Mobile IKE and the peer address could not be changed.

**Recommended Action** This is typically a transient error condition. If this message occurs consistently, contact the Cisco TAC.

### 603101

**Error Message** `%ASA-6-603101: PPTP received out of seq or duplicate pkt, tnl_id=_number_, sess_id=_number_, seq=_number_`

**Explanation** The ASA received a PPTP packet that was out of sequence or duplicated.

**Recommended Action** If the packet count is high, contact the peer administrator to check the client PPTP configuration.

### 603102

**Error Message** `%ASA-6-603102: PPP virtual interface _interface_name_ - user: _user_ aaa authentication started`

**Explanation** The ASA sent an authentication request to the AAA server.

**Recommended Action** None required.

### 603103

**Error Message** `%ASA-6-603103: PPP virtual interface _interface_name_ - user: _user_ aaa authentication _status_`

**Explanation** The ASA received an authentication response from the AAA server.

**Recommended Action** None required.

### 603104

**Error Message** `%ASA-6-603104: PPTP Tunnel created, tunnel_id is _number_, remote_peer_ip is _remote_address_, ppp_virtual_interface_id is _number_, client_dynamic_ip is _IP_address_, username is _user_, MPPE_key_strength is _string_`

**Explanation** A PPTP tunnel was created.

**Recommended Action** None required.

### 603105

**Error Message** `%ASA-6-603105: PPTP Tunnel deleted, tunnel_id = _number_, remote_peer_ip = _remote_address_`

**Explanation** A PPTP tunnel was deleted.

**Recommended Action** None required.

### 603106

**Error Message** `%ASA-6-603106: L2TP Tunnel created, tunnel_id is _number_, remote_peer_ip is _remote_address_, ppp_virtual_interface_id is _number_, client_dynamic_ip is _IP_address_, username is _user_`

**Explanation** An L2TP tunnel was created. The username is hidden when invalid or unknown, but appears when valid or the no logging hide username command has been configured.

**Recommended Action** None required.

### 603107

**Error Message** `%ASA-6-603107: L2TP Tunnel deleted, tunnel_id = _number_, remote_peer_ip = _remote_address_`

**Explanation** An L2TP tunnel was deleted.

**Recommended Action** None required.

### 603108

**Error Message** `%ASA-6-603108: Built PPPOE Tunnel, tunnel_id = _interface_name_, remote_peer_ip = _number_, ppp_virtual_interface_id = _IP_address_, client_dynamic_ip = _number_, username = _IP_address_`

**Explanation** A new PPPoE tunnel was created.

**Recommended Action** None required.

### 603109

**Error Message** `%ASA-6-603109: Teardown PPPOE Tunnel, tunnel_id = _interface_name_, remote_peer_ip = _number_`

**Explanation** A new PPPoE tunnel was deleted.

**Recommended Action** None required.

### 603110

**Error Message** `%ASA-4-603110: Failed to establish L2TP session, tunnel_id = _tunnel_id_, remote_peer_ip = _peer_ip_, user = _username_. Multiple sessions per tunnel are not supported`

**Explanation** An attempt to establish a second session was detected and denied. Cisco does not support multiple L2TP sessions per tunnel.

-   _tunnel\_id_ —The L2TP tunnel ID
-   _peer\_ip_ —The peer IP address
-   _username_ —The name of the authenticated user

**Recommended Action** None required.

### 604101

**Error Message** `%ASA-6-604101: DHCP client interface _interface_name_: Allocated ip = _IP_address_, mask = _netmask_, gw = _gateway_address_`

**Explanation** The Secure Firewall ASA DHCP client successfully obtained an IP address from a DHCP server. The dhcpc command statement allows the Secure Firewall ASA to obtain an IP address and network mask for a network interface from a DHCP server, as well as a default route. The default route statement uses the gateway address as the address of the default router.

**Recommended Action** None required.

### 604102

**Error Message** `%ASA-6-604102: DHCP client interface _interface_name_: address released`

**Explanation** The Secure Firewall ASA DHCP client released an allocated IP address back to the DHCP server.

**Recommended Action** None required.

### 604103

**Error Message** `%ASA-6-604103: DHCP daemon interface _interface_name_: address granted _MAC_address_ (_IP_address_)`

**Explanation** The Secure Firewall ASA DHCP server granted an IP address to an external client.

**Recommended Action** None required.

### 604104

**Error Message** `%ASA-6-604104: DHCP daemon interface _interface_name_: address released _build_number_ (_IP_address_)`

**Explanation** An external client released an IP address back to the Secure Firewall ASA DHCP server.

**Recommended Action** None required.

### 604105

**Error Message** `%ASA-4-604105: Unable to send DHCP reply to client _hardware_address_ on interface _interface_name_. Reply exceeds options field size (_options_field_size_) by _number_of_octets_ octets.`

**Explanation** An administrator can configure the DHCP options to return to the DHCP client. Depending on the options that the DHCP client requests, the DHCP options for the offer could exceed the message length limits. A DHCP offer cannot be sent, because it will not fit within the message limits.

-   _hardware\_address_ —The hardware address of the requesting client.
-   _interface\_name—_ The interface to which server messages are being sent and received
-   _options\_field\_size_ —The maximum options field length. The default is 312 octets, which includes 4 octets to terminate.
-   _number\_of\_octets_ —The number of exceeded octets.

**Recommended Action** Reduce the size or number of configured DHCP options.

### 604201

**Error Message** `%ASA-6-604201: DHCPv6 PD client on interface _pd-client-iface_ received delegated prefix _prefix_/_prefix_ from DHCPv6 PD server _server-address_ with preferred lifetime _in-seconds_ seconds and valid lifetime _in-seconds_ seconds`

**Explanation** This syslog is displayed whenever DHCPv6 PD client is received with delegated prefix from PD server as part of initial 4-way exchange. In the case of multiple prefixes, the syslog is displayed for each prefix.

-   _pd-client-iface_—The interface name on which the DHCPv6 PD client is enabled.
-   _prefix_—Prefix received from DHCPv6 PD server.
-   _server-address_—DHCPv6 PD server address.
-   _in-seconds_—Associated preferred and valid lifetime in seconds for delegated prefixes.

**Recommended Action** None.

### 604202

**Error Message** `%ASA-6-604202: DHCPv6 PD client on interface _pd-client-iface_ releasing delegated prefix _prefix_/_prefix_ received from DHCPv6 PD server _server-address_`

**Explanation** This syslog is displayed whenever DHCPv6 PD Client is releasing delegated prefix(s) received from PD Server upon no configuration. In the case of multiple prefixes, the syslog is displayed for each prefix.

-   _pd-client-iface_—The interface name on which the DHCPv6 PD client is enabled.
-   _prefix_—Prefix received from DHCPv6 PD server.
-   _server-address_—DHCPv6 PD server address.

**Recommended Action** None.

### 604203

**Error Message** `%ASA-6-604203: DHCPv6 PD client on interface _pd-client-iface_ renewed delegated prefix _prefix_/_prefix_ from DHCPv6 PD server _server-address_ with preferred lifetime _in-seconds_ seconds and valid lifetime _in-seconds_ seconds`

**Explanation** This syslog is displayed whenever DHCPv6 PD Client initiate renewal of previously allocated delegated prefix from PD Server and upon successful. In the case of multiple prefixes, the syslog is displayed for each prefix.

-   _pd-client-iface_—The interface name on which the DHCPv6 PD client is enabled.
-   _prefix_—Prefix received from DHCPv6 PD server.
-   _server-address_—DHCPv6 PD server address.
-   _in-seconds_—Associated preferred and valid lifetime in seconds for delegated prefixes.

**Recommended Action** None.

### 604204

**Error Message** `%ASA-6-604204: DHCPv6 delegated prefix _delegated_prefix_/_prefix_ got expired on interface _pd-client-iface_, received from DHCPv6 PD server _server-address_`

**Explanation** This syslog is displayed whenever DHCPv6 PD Client received delegated prefix is getting expired.

-   _pd-client-iface_—The interface name on which the DHCPv6 PD client is enabled.
-   _prefix_—Prefix received from DHCPv6 PD server.
-   _delegated prefix_—The delegated prefix received from DHCPv6 PD server.

**Recommended Action** None.

### 604205

**Error Message** `%ASA-6-604205: DHCPv6 client on interface _client-iface_ allocated address _ipv6-address_ from DHCPv6 server _server-address_ with preferred lifetime _in-seconds_ seconds and valid lifetime _in-seconds_ seconds`

**Explanation** This syslog is displayed whenever DHCPv6 Client address is received from DHCPv6 Server as part of initial 4-way exchange and is valid. In the case of multiple addresses, the syslog is displayed for each received address.

-   _client-iface_—The interface name on which the DHCPv6 client address is enabled.
-   _ipv6-address_—IPv6 Address received from DHCPv6 server.
-   _server-address_—DHCPv6 server address.
-   _in-seconds_—Associated preferred and valid lifetime in seconds for client address.

**Recommended Action** None.

### 604206

**Error Message** `%ASA-6-604206: DHCPv6 client on interface _client-iface_ releasing address _ipv6-address_ received from DHCPv6 server _server-address_`

**Explanation** DHCPv6 Client is releasing received client address whenever no configuration of DHCPv6 client address is performed. In the case of multiple addresses release, the syslog is displayed for each address.

-   _client-iface_—The interface name on which the DHCPv6 client address is enabled.
-   _ipv6-address_—IPv6 address received from DHCPv6 server.
-   _server-address_—DHCPv6 server address.

**Recommended Action** None.

### 604207

**Error Message** `%ASA-6-604207: DHCPv6 client on interface _client-iface_ renewed address _ipv6-address_ from DHCPv6 server _server-address_ with preferred lifetime _in-seconds_ seconds and valid lifetime _in-seconds_ seconds`

**Explanation** This syslog is displayed whenever DHCPv6 client initiates renewal of previously allocated address from DHCPv6 server. In the case of multiple addresses, the syslog is displayed for each renewed address.

-   _client-iface_—The interface name on which the DHCPv6 client address is enabled.
-   _ipv6-address_—IPv6 Address received from DHCPv6 server.
-   _server-address_—DHCPv6 server address.
-   _in-seconds_—Associated preferred and valid lifetime in seconds for client address.

**Recommended Action** None.

### 604208

**Error Message** `%ASA-6-604208: DHCPv6 client address _ipv6-address_ got expired on interface _client-iface_, received from DHCPv6 server _server-address_`

**Explanation** This syslog is displayed whenever DHCPv6 client received address is getting expired.

-   _client-iface_—The interface name on which the DHCPv6 client address is enabled.
-   _ipv6-address_—IPv6 Address received from DHCPv6 server.
-   _server-address_—DHCPv6 server address.

**Recommended Action** None.

### 605004

**Error Message-1** `%ASA-6-605004: Login denied from _source_ip_address_/_source_port_ to _interface_:_destination_ip_address_/_service_name_ for user \'_username_\'`

**Error Message-2** `%ASA-6-605004: Login denied from _serial_ to _console_ for user \'_username_\'`

**Explanation** The following form of the message appears when the user attempts to log in to the console:

```css
Login denied from serial to console for user “username”
```

An incorrect login attempt or a failed login to the Secure Firewall ASA occurred. For all logins, three attempts are allowed per session, and the session is terminated after three incorrect attempts. For SSH and Telnet logins, this message is generated after the third failed attempt or if the TCP session is terminated after one or more failed attempts. For other types of management sessions, this message is generated after every failed attempt. The username is hidden when invalid or unknown, but appears when valid or the no logging hide username command has been configured.

-   _source-address—_ Source address of the login attempt
-   _source-port—_ Source port of the login attempt
-   _interface—_ Destination management interface
-   _destination—_ Destination IP address
-   _service—_ Destination service
-   _username_ _—_ Destination management interface

**Recommended Action** If this message appears infrequently, no action is required. If this message appears frequently, it may indicate an attack. Communicate with the user to verify the username and password.

### 605005

**Error Message 1** `%ASA-6-605005: Login permitted from _source_ip_address_/_source_port_ to _interface_:_destination_ip_address_/_service_name_ for user '_username_'`

**Error Message 2** `%ASA-6-605005: Login permitted from _serial_ to _console_ for user '_username_'`

The following form of the message appears when the user logs in to the console:

```css
Login permitted from serial to console for user “username”
```

**Explanation** A user was authenticated successfully, and a management session started.

-   _source\_ip\_address—_ Source address of the login attempt
-   _source\_port—_ Source port of the login attempt
-   _interface—_ Destination management interface
-   _destination\_ip\_address—_ Destination IP address
-   _service—_ Destination service
-   _username—_ Destination management interface

**Recommended Action** None required.

### 606001

**Error Message** `%ASA-6-606001: ASDM session number _number_ from _IP_address_ started`

**Explanation** An administrator has been authenticated successfully, and an ASDM session started.

**Recommended Action** None required.

### 606002

**Error Message** `%ASA-6-606002: ASDM session number _number_ from _IP_address_ ended`

**Explanation** An ASDM session ended.

**Recommended Action** None required.

### 606003

**Error Message** `%ASA-6-606003: ASDM logging session number _id_ from _IP_address_ started`

**Explanation** An ASDM logging connection was started by a remote management client.

-   IP\_address—IP address of the remote management client

**Recommended Action** None required.

### 606004

**Error Message** `%ASA-6-606004: ASDM logging session number _id_ from _IP_address_ ended`

**Explanation** An ASDM logging connection was terminated.

-   id—Session ID assigned
-   IP\_address—IP address of remote management client

**Recommended Action** None required.

### 607001

**Error Message-1** `%ASA-6-607001: Pre-allocate SIP _connection_type_ secondary channel for _interface_name_:_ip_address_ to _interface_name_:_ip_address_/_port_ from _message_string_ message`

**Error Message-2** `%ASA-6-607001: Pre-allocate SIP _connection_type_ secondary channel for _interface_name_:_ip_address_/_port_ to _interface_name_:_ip_address_ from _message_string_ message`

**Explanation** The fixup sip command preallocated a SIP connection after inspecting a SIP message . The connection\_type is one of the following strings:

-   SIGNALLING UDP
-   SIGNALLING TCP
-   SUBSCRIBE UDP
-   SUBSCRIBE TCP
-   Via UDP
-   Route
-   RTP
-   RTCP

**Recommended Action** None required.

### 607002

**Error Message** `%ASA-4-607002: _action_class_ SIP _action_ _req_resp_ from _req_resp_info_:_src_ifc_/_sip_ to _sport_:_dest_ifc_/_dip_; _dport_`

**Explanation** A SIP classification was performed on a SIP message, and the specified criteria were satisfied. As a result, the configured action occurs.

-   _action\_class_ —The class of the action: SIP Classification for SIP match commands or SIP Parameter for parameter commands
-   _action_ —The action taken: Dropped, Dropped connection for, Reset connection for, or Masked header flags for
-   _req\_resp_ —Request or Response
-   _req\_resp\_info_ —The SIP method name if the type is Request: INVITE or CANCEL. The SIP response code if the type is Response: 100, 183, 200.
-   _src\_ifc_ —The source interface name
-   _sip_ —The source IP address
-   _sport_ —The source port
-   _dest\_ifc_ —The destination interface name
-   _dip_ —The destination IP address
-   _dport_ —The destination port
-   _further\_info_ —More information appears for SIP match and SIP parameter commands, as follows:

For SIP match commands:

matched Class id: class-name

For example:

```vbnet
matched Class 1234: my_class
```

For SIP parameter commands:

parameter-command: descriptive-message

For example:

```vbnet
strict-header-validation: Mandatory header field Via is missing
state-checking: Message CANCEL is not permitted to create a Dialog.
```

**Recommended Action** None required.

### 607003

**Error Message** `%ASA-6-607003: _action_class_ SIP _req_resp_ _req_resp_info_ from _src_ifc_:_sip_/_sport_ to _dest_ifc_:_dip_/_dport_; _further_info_`

**Explanation** A SIP classification was performed on a SIP message, and the specified criteria were satisfied. As a result, the standalone log action occurs.

-   _action\_class_ —SIP classification for SIP match commands or SIP parameter for parameter commands
-   _req\_resp_ —Request or Response
-   _req\_resp\_info_ —The SIP method name if the type is Request: INVITE or CANCEL. The SIP response code if the type is Response: 100, 183, 200.
-   _src\_ifc_ —The source interface name
-   _sip_ —The source IP address
-   _sport_ —The source port
-   _dest\_ifc_ —The destination interface name
-   _dip_ —The destination IP address.
-   _dport_ —The destination port.
-   _further\_info_ —More information appears for SIP match and SIP parameter commands, as follows:

For SIP match commands:

matched Class id: class-name

For example:

```vbnet
matched Class 1234: my_class
```

For SIP parameter commands:

parameter-command: descriptive-message

For example:

```vbnet
strict-header-validation: Mandatory header field Via is missing
state-checking: Message CANCEL is not permitted to create a Dialog.
```

**Recommended Action** None required.

### 607004

**Error Message** `%ASA-4-607004: Phone Proxy: Dropping SIP message from _src_if_:_src_ip_/_src_port_ to _dest_if_:_dest_ip_/_dest_port_ with source MAC _mac_address_ due to secure phone database mismatch`

**Explanation** The MAC address in the SIP message is compared with the secure database entries in addition to the IP address and interface. If they do not match, then the particular message is dropped.

**Recommended Action** None required.

### 608001

**Error Message** `%ASA-6-608001: Pre-allocate Skinny _connection_type_ secondary channel for _interface_name:IP_address_ to _interface_name:IP_address_ from _string_ message`

**Explanation** The inspect skinny command preallocated a Skinny connection after inspecting a Skinny message . The connection\_type is one of the following strings:

-   SIGNALLING UDP
-   SIGNALLING TCP
-   SUBSCRIBE UDP
-   SUBSCRIBE TCP
-   Via UDP
-   Route
-   RTP
-   RTCP

**Recommended Action** None required.

### 608002

**Error Message** `%ASA-4-608002: Dropping Skinny message for _in_ifc_:_src_ip_/_src_port_ to _out_ifc_:_dest_ip_/_dest_port_, SCCPPrefix length _value_ too small`

**Explanation** A Skinny (SSCP) message was received with an SCCP prefix length less than the minimum length configured.

-   _in\_ifc_ —The input interface
-   _src\_ip_ —The source IP address of the packet
-   _src\_port_ —The source port of the packet
-   _out\_ifc_ —The output interface
-   _dest\_ip_ —The destination IP address of the packet
-   _dest\_port_ —The destination port of the packet
-   _value_ —The SCCP prefix length of the packet

**Recommended Action** If the SCCP message is valid, then customize the Skinny policy map to increase the minimum length value of the SSCP prefix.

### 608003

**Error Message** `%ASA-4-608003: Dropping Skinny message for _in_ifc_:_src_ip_/_src_port_ to _out_ifc_:_dest_ip_/_dest_port_, SCCPPrefix length _value_ too large`

**Explanation** A Skinny (SSCP) message was received with an SCCP prefix length greater than the maximum length configured.

-   _in\_ifc_ —The input interface
-   _src\_ip_ —The source IP address of the packet
-   _src\_port_ —The source port of the packet
-   _out\_ifc_ —The output interface
-   _dest\_ip_ —The destination IP address of the packet
-   _dest\_port_ —The destination port of the packet
-   _value_ —The SCCP prefix length of the packet

**Recommended Action** If the SCCP message is valid, then customize the Skinny policy map to increase the maximum length value of the SCCP prefix.

### 608004

**Error Message** `%ASA-4-608004: Dropping Skinny message for _in_ifc_:_src_ip_/_src_port_ to _out_ifc_:_dest_ip_/_dest_port_, message id _value_ not allowed`

**Explanation** This SCCP message ID is not allowed.

-   _in\_ifc_ —The input interface
-   _src\_ip_ —The source IP address of the packet
-   _src\_port_ —The source port of the packet
-   _out\_ifc_ —The output interface
-   _dest\_ip_ —The destination IP address of the packet
-   _dest\_port_ —The destination port of the packet
-   _value_ —The SCCP prefix length of the packet

**Recommended Action** If the SCCP messages should be allowed, then customize the Skinny policy map to allow them.

### 608005

**Error Message** `%ASA-4-608005: Dropping Skinny message for _in_ifc_:_src_ip_/_src_port_ to _out_ifc_:_dest_ip_/_dest_port_, message id _value_ registration not complete`

**Explanation** This SCCP message ID is not allowed, because the endpoint did not complete registration.

-   _in\_ifc_ —The input interface
-   _src\_ip_ —The source IP address of the packet
-   _src\_port_ —The source port of the packet
-   _out\_ifc_ —The output interface
-   _dest\_ip_ —The destination IP address of the packet
-   _dest\_port_ —The destination port of the packet
-   _value_ —The SCCP prefix length of the packet

**Recommended Action** If the SCCP messages that are being dropped are valid, then customize the Skinny policy map to disable registration enforcement.

### 609001

**Error Message** `%ASA-7-609001: Built local_host _zone_name_:_ip_address_`

**Explanation** A network state container was reserved for host ip\_address connected to zone _zone\_name_. The zone\_name/\* parameter is used if the interface on which the host is created is part of a zone. The asterisk symbolizes all interfaces because hosts do not belong to any one interface.

**Recommended Action** None required.

### 609002

**Error Message** `%ASA-7-609002: Teardown local-host _zone_name_:_ip_address_ duration _time_`

**Explanation** A network state container for host ip\_address connected to zone zone\_name was removed. The zone\_name/\* parameter is used if the interface on which the host is created is part of a zone. The asterisk symbolizes all interfaces because hosts do not belong to any one interface.

**Recommended Action** None required.

## Messages 610001 to 622102

This section includes messages from 610001 to 622102.

### 610001

**Error Message** `%ASA-3-610001: NTP daemon interface _interface_name_: Packet denied from _IP_address_`

**Explanation** An NTP packet was received from a host that does not match one of the configured NTP servers. The ASA is only an NTP client; it is not a time server and does not respond to NTP requests.

**Recommended Action** None required.

### 610002

**Error Message** `%ASA-3-610002: NTP daemon interface _interface_name_: Authentication failed for packet from _IP_address_`

**Explanation** The received NTP packet failed the authentication check.

**Recommended Action** Make sure that both the ASA and the NTP server are set to use authentication, and the same key number and value.

### 610101

**Error Message** `%ASA-6-610101: Authorization failed: Cmd: _command_ Cmdtype: _command_modifier_`

**Explanation** Command authorization failed for the specified command. The command\_modifier is one of the following strings:

-   -   cmd (this string means the command has no modifier)
    -   clear
    -   no
    -   show

If the ASA encounters any other value other than the four command types listed, the message “ unknown command type ” appears.

**Recommended Action** None required.

### 611101

**Error Message** `%ASA-6-611101: User authentication succeeded: IP address: _IP_address_, Uname: _user_`

**Explanation** User authentication succeeded when accessing the Secure Firewall ASA. The username is hidden when invalid or unknown, but appears when valid or the no logging hide username command has been configured.

-   _IP address_ —The IP address of the client that succeeded user authentication
-   _user_ —The user that authenticated

**Recommended Action** None required.

### 611102

**Error Message** `%ASA-6-611102: User authentication failed: IP address: _IP_address,_, Uname: _user_`

**Explanation** User authentication failed when attempting to access the Secure Firewall ASA. The username is hidden when invalid or unknown, but appears when valid or the no logging hide username command has been configured.

-   _IP address_ —The IP address of the client that failed user authentication
-   _user_ —The user that authenticated

**Recommended Action** None required.

### 611103

**Error Message** `%ASA-5-611103: User logged out: Uname: _user_`

**Explanation** The specified user logged out.

**Recommended Action** None required.

### 611104

**Error Message** `%ASA-5-611104: Serial console idle timeout exceeded`

**Explanation** The configured idle timeout for the Secure Firewall ASA serial console was exceeded because of no user activity.

**Recommended Action** None required.

### 611301

**Error Message** `%ASA-6-611301: VPNClient: NAT configured for Client Mode with no split tunneling: NAT addr: _mapped_address_`

**Explanation** The VPN client policy for client mode with no split tunneling was installed.

**Recommended Action** None required.

### 611302

**Error Message** `%ASA-6-611302: VPNClient: NAT exemption configured for Network Extension Mode with no split tunneling`

**Explanation** The VPN client policy for network extension mode with no split tunneling was installed.

**Recommended Action** None required.

### 611303

**Error Message** `%ASA-6-611303: VPNClient: NAT configured for Client Mode with split tunneling: NAT addr: _mapped_address_ Split Tunnel Networks: _IP_address_`

**Explanation** The VPN client policy for client mode with split tunneling was installed.

**Recommended Action** None required.

### 611304

**Error Message** `%ASA-6-611304: VPNClient: NAT exemption configured for Network Extension Mode with split tunneling: Split Tunnel Networks: _IP_address_`

**Explanation** The VPN client policy for network extension mode with split tunneling was installed.

**Recommended Action** None required.

### 611305

**Error Message** `%ASA-6-611305: VPNClient: DHCP Policy installed: _IP_address_`

**Explanation** The VPN client policy for DHCP was installed.

**Recommended Action** None required.

### 611306

**Error Message** `%ASA-6-611306: VPNClient: Perfect Forward Secrecy Policy installed`

**Explanation** Perfect forward secrecy was configured as part of the VPN client download policy.

**Recommended Action** None required.

### 611307

**Error Message** `%ASA-6-611307: VPNClient: Head end : _IP_address_`

**Explanation** The VPN client is connected to the specified headend.

**Recommended Action** None required.

### 611308

**Error Message** `%ASA-6-611308: VPNClient: Split DNS Policy installed: List of domains: _string_string_`

**Explanation** A split DNS policy was installed as part of the VPN client downloaded policy.

**Recommended Action** None required.

### 611309

**Error Message** `%ASA-6-611309: VPNClient: Disconnecting from head end and uninstalling previously downloaded policy: Head End : _IP_address_`

**Explanation** A VPN client is disconnecting and uninstalling a previously installed policy.

**Recommended Action** None required.

### 611310

**Error Message** `%ASA-6-611310: VPNClient: XAUTH Succeeded: Peer: _IP_address_`

**Explanation** The VPN client Xauth succeeded with the specified headend.

**Recommended Action** None required.

### 611311

**Error Message** `%ASA-6-611311: VPNClient: XAUTH Failed: Peer: _IP_address_`

**Explanation** The VPN client Xauth failed with the specified headend.

**Recommended Action** None required.

### 611312

**Error Message** `%ASA-6-611312: VPNClient: Backup Server List: _reason_`

**Explanation** When the Secure Firewall ASA is an Easy VPN remote device, the Easy VPN server downloaded a list of backup servers to the Secure Firewall ASA. This list overrides any backup servers that you have configured locally. If the downloaded list is empty, then the Secure Firewall ASA uses no backup servers. The reason is one of the following messages:

-   A list of backup server IP addresses
-   Received NULL list. Deleting current backup servers

**Recommended Action** None required.

### 611313

**Error Message** `%ASA-3-611313: VPNClient: Backup Server List Error: _reason_`

**Explanation** When the Secure Firewall ASA is an Easy VPN remote device, and the Easy VPN server downloads a backup server list to the Secure Firewall ASA, the list includes an invalid IP address or a hostname. The Secure Firewall ASA does not support DNS, and therefore does not support hostnames for servers, unless you manually map a name to an IP address using the name command.

**Recommended Action** On the Easy VPN server, make sure that the server IP addresses are correct, and configure the servers as IP addresses instead of hostnames. If you must use hostnames on the server, use the name command on the Easy VPN remote device to map the IP addresses to names.

### 611314

**Error Message** `%ASA-6-611314: VPNClient: Load Balancing Cluster with Virtual IP: _IP_address_ has redirected firewall to server _IP_address_`

**Explanation** When the Secure Firewall ASA is an Easy VPN remote device, the director server of the load balancing group redirected the Secure Firewall ASA to connect to a particular server.

**Recommended Action** None required.

### 611315

**Error Message** `%ASA-6-611315: VPNClient: Disconnecting from Load Balancing Cluster member _IP_address_.`

**Explanation** When the Secure Firewall ASA is an Easy VPN remote device, it disconnected from a load balancing cluster server.

**Recommended Action** None required.

### 611316

**Error Message** `%ASA-6-611316: VPNClient: Secure Unit Authentication Enabled`

**Explanation** When the Secure Firewall ASA is an Easy VPN remote device, the downloaded VPN policy enabled SUA.

**Recommended Action** None required.

### 611317

**Error Message** `%ASA-6-611317: VPNClient: Secure Unit Authentication Disabled`

**Explanation** When the Secure Firewall ASA is an Easy VPN remote device, the downloaded VPN policy disabled SUA.

**Recommended Action** None required.

### 611318

**Error Message** `%ASA-6-611318: VPNClient: User Authentication Enabled: Auth Server IP: _IP_address_ Auth Server Port: _port_ Idle Timeout: _time_`

**Explanation** When the Secure Firewall ASA is an Easy VPN remote device, the downloaded VPN policy enabled IUA for users on the Secure Firewall ASA inside network.

-   IP\_address—The server IP address to which the Secure Firewall ASA sends authentication requests.
-   port—The server port to which the Secure Firewall ASA sends authentication requests
-   time—The idle timeout value for authentication credentials

**Recommended Action** None required.

### 611319

**Error Message** `%ASA-6-611319: VPNClient: User Authentication Disabled`

**Explanation** When the Secure Firewall ASA is an Easy VPN remote device, the downloaded VPN policy disabled IUA for users on the Secure Firewall ASA inside network.

**Recommended Action** None required.

### 611320

**Error Message** `%ASA-6-611320: VPNClient: Device Pass Through Enabled`

**Explanation** When the Secure Firewall ASA is an Easy VPN remote device, the downloaded VPN policy enabled device pass-through. The device pass-through feature allows devices that cannot perform authentication (such as an IP phone) to be exempt from authentication when IUA is enabled. If the Easy VPN server enabled this feature, you can specify the devices that should be exempt from authentication (IUA) using the vpnclient mac-exempt command on the Secure Firewall ASA.

**Recommended Action** None required.

### 611321

**Error Message** `%ASA-6-611321: VPNClient: Device Pass Through Disabled`

**Explanation** When the Secure Firewall ASA is an Easy VPN remote device, the downloaded VPN policy disabled device pass-through.

**Recommended Action** None required.

### 611322

**Error Message** `%ASA-6-611322: VPNClient: Extended XAUTH conversation initiated when SUA disabled`

**Explanation** When the Secure Firewall ASA is an Easy VPN remote device and the downloaded VPN policy disabled SUA, the Easy VPN server uses two-factor/SecurID/cryptocard-based authentication mechansims to authenticate the Secure Firewall ASA using XAUTH.

**Recommended Action** If you want the Easy VPN remote device to be authenticated using two-factor/SecureID/cryptocard-based authentication mechanisms, enable SUA on the server.

### 611323

**Error Message** `%ASA-6-611323: VPNClient: Ignoring duplicate split network entry _network_address_/_network_mask_`

**Explanation** When the Secure Firewall ASA is an Easy VPN remote device, the downloaded VPN policy included duplicate split network entries. An entry is considered a duplicate if it matches both the network address and the network mask.

**Recommended Action** Remove duplicate split network entries from the VPN policy on the Easy VPN server.

### 612001

**Error Message** `%ASA-5-612001: Auto Update succeeded: _filename_, version: _number_`

**Explanation** An update from an Auto Update server was successful. The filename variable is image, ASDM file, or configuration. The version number variable is the version number of the update.

**Recommended Action** None required.

### 612002

**Error Message** `%ASA-4-612002: Auto Update failed: _filename_, version: _number_, reason: _reason_`

**Explanation** An update from an Auto Update server failed.

-   filename—Either an image file, an ASDM file, or a configuration file.
-   number—The version number of the update.
-   reason—The failure reason, which may be one of the following:

\- Failover module failed to open stream buffer

\- Failover module failed to write data to stream buffer

\- Failover module failed to perform control operation on stream buffer

\- Failover module failed to open flash file

\- Failover module failed to write data to flash

\- Failover module operation timeout

\- Failover command link is down

\- Failover resource is not available

\- Invalid failover state on mate

\- Failover module encountered file transfer data corruption

\- Failover active state change

\- Failover command EXEC failed

\- The image cannot run on current system

\- Unsupported file type

**Recommended Action** Check the configuration of the Auto Update server. Check to see if the standby unit is in the failed state. If the Auto Update server is configured correctly, and the standby unit is not in the failed state, contact the Cisco TAC.

### 612003

**Error Message** `%ASA-4-612003: Auto Update failed to contact: _url_, reason: _reason_`

**Explanation** The Auto Update daemon was unable to contact the specified URL url, which can be the URL of the Auto Update server or one of the file server URLs returned by the Auto Update server. The reason field describes why the contact failed. Possible reasons for the failure include no response from the server, authentication failed, or a file was not found.

**Recommended Action** Check the configuration of the Auto Update server.

### 613001

**Error Message** `%ASA-6-613001: Bad checksum _string_ from _IP_address_ on _number_`

**Explanation** OSPF has detected a checksum error in the database because of memory corruption.

**Recommended Action** Restart the OSPF process.

### 613002

**Error Message** `%ASA-6-613002: Interface _interface_name_ has zero bandwidth configuration`

**Explanation** The interface reported its bandwidth as zero.

**Recommended Action** Copy the message exactly as it appears, and report it to the Cisco TAC.

### 613003

**Error Message** `%ASA-6-613003: Network range _IP_address netmask_ changed from area _string_ to _string_`

**Explanation** An OSPF configuration change has caused a network range to change areas.

**Recommended Action** Reconfigure OSPF with the correct network range.

### 613004

**Error Message** `%ASA-3-613004: Internal error: memory allocation failure`

**Explanation** An internal software error occurred.

**Recommended Action** Copy the error message exactly as it appears, and report it to Cisco TAC.

### 613005

**Error Message** `%ASA-3-613005: Flagged as being an ABR without a backbone area`

**Explanation** The router was flagged as an Area Border Router (ABR) without a backbone area in the router.

**Recommended Action** Restart the OSPF process.

### 613006

**Error Message** `%ASA-3-613006: Reached unknown state in neighbor state machine`

**Explanation** An internal software error in this router has resulted in an invalid neighbor state during database exchange.

**Recommended Action** Copy the error message, the configuration and any details about the events leading up to this error and submit them to Cisco TAC.

### 613007

**Error Message** `%ASA-3-613007: area string lsid IP_address mask netmask type number`

**Explanation** OSPF is trying to add an existing LSA to the database.

**Recommended Action** Copy the error message, the configuration and any details about the events leading up to this error and submit them to Cisco TAC.

### 613008

**Error Message** `%ASA-3-613008: if inside if_state number`

**Explanation** An internal error occurred.

**Recommended Action** Copy the error message, the configuration and any details about the events leading up to this error and submit them to Cisco TAC.

### 613011

**Error Message** `%ASA-3-613011: OSPF process number is changing router-id. Reconfigure virtual link neighbors with our new router-id`

**Explanation** An OSPF process is being reset, and it is going to select a new router ID. This action brings down all virtual links. To make them work again, the virtual link configuration needs to be changed on all virtual link neighbors.

**Recommended Action** Change the virtual link configuration on all the virtual link neighbors to reflect the new router ID.

### 613013

**Error Message** `%ASA-3-613013: OSPF LSID IP_address adv IP_address type number gateway IP_address metric number forwarding addr route IP_address/mask type number has no corresponding LSA`

**Explanation** OSPF found inconsistency between its database and the IP routing table.

**Recommended Action** Copy the error message, the configuration and any details about the events leading up to this error, and submit them to Cisco TAC.

### 613014

**Error Message** `%ASA-6-613014: Base topology enabled on interface string attached to MTR compatible mode area string`

**Explanation** OSPF interfaces attached to MTR-compatible OSPF areas require the base topology to be enabled.

**Recommended Action** None.

### 613015

**Error Message** `%ASA-4-613015: Process 1 flushes LSA ID IP_address type-number adv-rtr IP_address in area mask`

**Explanation** A router is extensively re-originating or flushing the LSA reported by this error message.

**Recommended Action** If this router is flushing the network LSA, it means the router received a network LSA whose LSA ID conflicts with the IP address of one of the router's interfaces and flushed the LSA out of the network. For OSPF to function correctly, the IP addresses of transit networks must be unique. Conflicting routers are the router reporting this error message and the router with the OSPF router ID reported as adv-rtr in this message. If this router is re-originating an LSA, it is highly probable that some other router is flushing this LSA out of the network. Find that router and avoid the conflict. The conflict for a Type-2 LSA may be due to a duplicate LSA ID. For a Type-5 LSA, it may be a duplicate router ID on the router reporting this error message and on the routers connected to a different area. In an unstable network, this message may also warn of extensive re-origination of the LSA for some other reason. Contact Cisco TAC to investigate this type of case.

### 613016

**Error Message** `%ASA-3-613016: Area string router-LSA of length number bytes plus update overhead bytes is too large to flood.`

**Explanation** The router tried to build a router-LSA that is larger than the huge system buffer size or the OSPF protocol imposed maximum.

**Recommended Action** If the reported total length (LSA size plus overhead) is larger than the huge system buffer size but less than 65535 bytes (the OSPF protocol imposed maximum), you may increase the huge system buffer size. If the reported total length is greater than 65535, you need to decrease the number of OSPF interfaces in the reported area.

### 613017

**Error Message** `%ASA-4-613017: Bad LSA mask: Type number, LSID IP_address Mask _mask_ from IP_address`

**Explanation** The router received an LSA with an invalid LSA mask because of an incorrect configuration from the LSA originator. As a result, this route is not installed in the routing table.

**Recommended Action** Find the originating router of the LSA with the bad mask, then correct any misconfiguration of this LSA's network. For further debugging, call Cisco TAC for assistance.

### 613018

**Error Message** `%ASA-4-613018: Maximum number of non self-generated LSA has been exceeded “OSPF number” - number LSAs`

**Explanation** The maximum number of non self-generated LSAs has been exceeded.

**Recommended Action** Check whether or not a router in the network is generating a large number of LSAs as a result of a misconfiguration.

### 613019

**Error Message** `%ASA-4-613019: Threshold for maximum number of non self-generated LSA has been reached "OSPF number" - number LSAs`

**Explanation** The threshold for the maximum number of non self-generated LSAs has been reached.

**Recommended Action** Check whether or not a router in the network is generating a large number of LSAs as a result of a misconfiguration.

### 613021

**Error Message** `%ASA-4-613021: Packet not written to the output queue`

**Explanation** An internal error occurred.

**Recommended Action** Copy the error message, the configuration and any details about the events leading up to this error, and submit them to Cisco TAC.

### 613022

**Error Message** `%ASA-4-613022: Doubly linked list linkage is NULL`

**Explanation** An internal error occurred.

**Recommended Action** Copy the error message, the configuration and any details about the events leading up to this error, and submit them to Cisco TAC.

### 613023

**Error Message** `%ASA-4-613023: Doubly linked list prev linkage is NULL number`

**Explanation** An internal error occurred.

**Recommended Action** Copy the error message, the configuration and any details about the events leading up to this error, and submit them to Cisco TAC.

### 613024

**Error Message** `%ASA-4-613024: Unrecognized timer number in OSPF string`

**Explanation** An internal error occurred.

**Recommended Action** Copy the error message, the configuration and any details about the events leading up to this error, and submit them to Cisco TAC.

### 613025

**Error Message** `%ASA-4-613025: Invalid build flag number for LSA IP_address, type number`

**Explanation** An internal error occurred.

**Recommended Action** Copy the error message, the configuration and any details about the events leading up to this error, and submit them to Cisco TAC.

### 613026

**Error Message** `%ASA-4-613026: Can not allocate memory for area structure`

**Explanation** An internal error occurred.

**Recommended Action** Copy the error message, the configuration and any details about the events leading up to this error, and submit them to Cisco TAC.

### 613027

**Error Message** `%ASA-6-613027: OSPF process number removed from interface interface_name`

**Explanation** The OSPF process was removed from the interface because of an IP VRF.

**Recommended Action** None.

### 613028

**Error Message** `%ASA-6-613028: Unrecognized virtual interface intetface_name. Treat it as loopback stub route`

**Explanation** The virtual interface type was not recognized by OSPF, so it is treated as a loopback interface stub route.

**Recommended Action** None.

### 613029

**Error Message** `%ASA-3-613029: Router-ID IP_address is in use by ospf process number`

**Explanation** The Secure Firewall ASA attempted to assign a router ID that is in use by another process.

**Recommended Action** Configure another router ID for one of the processes.

### 613030

**Error Message** `%ASA-4-613030: Router is currently an ASBR while having only one area which is a stub area`

**Explanation** An ASBR must be attached to an area that can carry AS external or NSSA LSAs.

**Recommended Action** Make the area to which the router is attached into an NSSA or regular area.

### 613031

**Error Message** `%ASA-4-613031: No IP address for interface inside`

**Explanation** The interface is not point-to-point and is unnumbered.

**Recommended Action** Change the interface type or give the interface an IP address.

### 613032

**Error Message** `%ASA-3-613032: Init failed for interface inside, area is being deleted. Try again.`

**Explanation** The interface initialization failed. The possible reasons include the following:

-   The area to which the interface is being attached is being deleted.
-   It was not possible to create a neighbor datablock for the local router.

**Recommended Action** Remove the configuration command that covers the interface and then try it again.

### 613033

**Error Message** `%ASA-3-613033: Interface inside is attached to more than one area`

**Explanation** The interface is on the interface list for an area other than the one to which the interface links.

**Recommended Action** Copy the error message, the configuration and any details about the events leading up to this error, and submit them to Cisco TAC.

### 613034

**Error Message** `%ASA-3-613034: Neighbor IP_address not configured`

**Explanation** The configured neighbor options are not valid.

**Recommended Action** Check the configuration options for the neighbor command and correct the options or the network type for the neighbor's interface.

### 613035

**Error Message** `%ASA-3-613035: Could not allocate or find neighbor IP_address`

**Explanation** An internal error occurred.

**Recommended Action** Copy the error message exactly as it appears, and report it to Cisco TAC.

### 613036

**Error Message** `%ASA-4-613036: Can not use configured neighbor: cost and database-filter options are allowed only for a point-to-multipoint network`

**Explanation** The configured neighbor was found on an NBMA network and either the cost or database-filter option was configured. These options are only allowed on point-to-multipoint type networks.

**Recommended Action** Check the configuration options for the neighbor command and correct the options or the network type for the neighbor's interface.

### 613037

**Error Message** `%ASA-4-613037: Can not use configured neighbor: poll and priority options are allowed only for a NBMA network`

**Explanation** The configured neighbor was found on a point-to-multipoint network and either the poll or priority option was configured. These options are only allowed on NBMA-type networks.

**Recommended Action** Check the configuration options for the neighbor command and correct the options or the network type for the neighbor's interface.

### 613038

**Error Message** `%ASA-4-613038: Can not use configured neighbor: cost or database-filter option is required for point-to-multipoint broadcast network`

**Explanation** The configured neighbor was found on a point-to-multipoint broadcast network. Either the cost or database-filter option needs to be configured.

**Recommended Action** Check the configuration options for the neighbor command and correct the options or the network type for the neighbor's interface.

### 613039

**Error Message** `%ASA-4-613039: Can not use configured neighbor: neighbor command is allowed only on NBMA and point-to-multipoint networks`

**Explanation** The configured neighbor was found on a network for which the network type was neither NBMA nor point-to-multipoint.

**Recommended Action** None.

### 613040

**Error Message** `%ASA-4-613040: OSPF-1 Area string: Router IP_address originating invalid type number LSA, ID IP_address, Metric number on Link ID IP_address Link Type number`

**Explanation** The router indicated in this message has originated an LSA with an invalid metric. If this is a router LSA and the link metric is zero, a risk of routing loops and traffic loss in the network exists.

**Recommended Action** Configure a valid metric for the given LSA type and link type on the router originating on the reported LSA.

### 613041

**Error Message** `%ASA-6-613041: OSPF-100 Areav string: LSA ID IP_address, Type number, Adv-rtr IP_address, LSA counter DoNotAge`

**Explanation** An internal error has corrected itself. There is no operational effect related to this error message.

**Recommended Action** Check the system memory. If memory is low, then the timer wheel functionality did not initialize. Try to reenter the commands when memory is available. If there is sufficient memory, then contact the Cisco TAC and provide output from the show memory, show processes, and show tech-support ospf commands.

### 613042

**Error Message** `%ASA-4-613042: OSPF process number lacks forwarding address for type 7 LSA IP_address in NSSA string - P-bit cleared`

**Explanation** There is no viable forwarding address in the NSSA area. As a result, the P-bit must be cleared and the Type 7 LSA is not translated into a Type 5 LSA by the NSSA translator. See RFC 3101.

**Recommended Action** Configure at least one interface in the NSSA with an advertised IP address. A loopback is preferable because an advertisement does not depend on the underlying layer 2 state.

### 613043

**Error Message** `%ASA-6-613043:`

**Explanation** A negative database reference count occurred.

**Recommended Action** Check the system memory. If memory is low, then the timer wheel functionality did not initialize. Try to reenter the commands when memory is available. If there is sufficient memory, then contact the Cisco TAC and provide output from the show memory, show processes, and show tech-support ospf commands.

### 613104

**Error Message** `%ASA-6-613104: Unrecognized virtual interface _IF_NAME_ .`

**Explanation** The virtual interface type was not recognized by OSPFv3, so it is treated as a loopback interface stub route.

**Recommended Action** None required.

### 614001

**Error Message** `%ASA-6-614001: Split DNS: request patched from server: _IP_address_ to server: _IP_address_`

**Explanation** Split DNS is redirecting DNS queries from the original destination server to the primary enterprise DNS server.

**Recommended Action** None required.

### 614002

**Error Message** `%ASA-6-614002: Split DNS: reply from server: _IP_address_ reverse patched back to original server: _IP_address_`

**Explanation** Split DNS is redirecting DNS queries from the enterprise DNS server to the original destination server.

**Recommended Action** None required.

### 615001

**Error Message** `%ASA-6-615001: vlan _number_ not available for firewall interface`

**Explanation** The switch removed the VLAN from the Secure Firewall ASA.

**Recommended Action** None required.

### 615002

**Error Message** `%ASA-6-615002: vlan _number_ available for firewall interface`

**Explanation** The switch added the VLAN to the Secure Firewall ASA.

**Recommended Action** None required.

### 616001

**Error Message** `%ASA-6-616001: Pre-allocate MGCP _data_channel_ connection for _inside_interface_:_inside_address_ to _outside_interface_:_outside_address_/_port_ from _message_type_message_ message`

**Explanation** An MGCP data channel connection, RTP, or RTCP was preallocated. The message text also specifies which message has triggered the connection preallocation.

**Recommended Action** None required.

### 617001

**Error Message** `%ASA-6-617001: GTPv_(version)_ _msg_type_ from _dest_interface_:_dest_address_/_dest_port_ not accepted by _source_interface_:_source_address_/_source_port_, Cause: value _cause_info_ (_cause_string_)`

**Explanation** A request was not accepted by the peer, which is usually seen with a Create PDP Context request.

**Recommended Action** None required.

### 617002

**Error Message 1** `%ASA-6-617002: Removing v0 PDP Context with TID _tid_ from GGSN _ip_address_ and SGSN _ip_address_, Cause: value _error_code_ (_string_), Reason: _reason_`

**Error Message 2** `%ASA-6-617002: Removing v1 {_primary | secondary_} PDP Context with TID _tid_ from GGSN _ip_address_ and SGSN _ip_address_, Cause: value _error_code_ (_string_), Reason: _reason_`

**Error Message 3** `%ASA-6-617002: Removing v2 {_primary | secondary_} PDP Context with TID _tid_ from PGW _ip_address_ and SGW _ip_address_, Cause: value _error_code_ (_string_), Reason: _reason_`

**Explanation** A PDP context was removed from the database either because it expired, a Delete PDP Context Request/Response was exchanged, or a user removed it using the CLI.

**Recommended Action** None required.

### 617003

**Error Message** `%ASA-6-617003: GTP Tunnel created from _source_interface_:_source_address_/0 to _source_port_:_source_interface_/_dest_address_`

**Explanation** A GTP tunnel was created after receiving a Create PDP Context Response that accepted the request.

**Recommended Action** None required.

### 617004

**Error Message** `%ASA-6-617004: GTP connection created for response from _source_interface_:_source_address_/0 to _0_:_source_interface_/_dest_address_`

**Explanation** The SGSN or GGSN signaling address in the Create PDP Context Request or Response, respectively, was different from the SGSN/GGSN sending it.

**Recommended Action** None required.

### 617100

**Error Message** `%ASA-6-617100: Teardown _num_conns_ connection(s) for user _user_ip_`

**Explanation** The connections for this user were torn down because either a RADIUS accounting stop or RADIUS accounting start was received, which includes attributes that were configured in the policy map for a match. The attributes did not match those stored for the user entry, if the user entry exists.

-   num\_conns—The number of connections torn down
-   user\_ip—The IP address (framed IP attribute) of the user

**Recommended Action** None required.

### 618001

**Error Message 1** `%ASA-6-618001: Denied STUN packet _msg_type_ from _inside_ifc_:_source_addr_/_source_port_ to _outside_ifc_:_destination_addr_/_destination_port_ for connection _conn_id_, malformed message header`

**Error Message 2** `%ASA-6-618001: Denied STUN packet _msg_type_ from _inside_ifc_:_source_addr_/_source_port_ to _outside_ifc_:_destination_addr_/_destination_port_ for connection _conn_id_, translation id doesn't match previous entry`

**Explanation** This syslog is modeled after 4313009. This message is rate limited to 25 logs per second.

-   msg\_type—The STUN message type value.
-   ingress\_ifc—The interface on which the packet arrived.
-   source\_addr—The IP address of the host which sent the packet.
-   source\_port—The port number of the host which sent the packet.
-   egress\_ifc—The interface on which the packet will leave.
-   destination\_addr—The IP address of the host which will receive the packet
-   destination\_port—The port number of the host which will receive the packet.
-   conn\_id—The unique connection ID
-   drop\_reason—The reason why the STUN packet was dropped.

**Recommended Action** None required.

### 620001

**Error Message 1** `%ASA-6-620001: Pre-allocate CTIQBE {_RTP | RTCP_} channel for _interface_name_:_outside_address_ to _interface_name_:_inside_address_/_inside_port_ from _message_name_ message`

**Error Message 2** `%ASA-6-620001: Pre-allocate CTIQBE {_RTP | RTCP_} channel for _interface_name_:_outside_address_/_outside_port_ to _interface_name_:_inside_address_ from _message_name_ message`

**Explanation** The ASA preallocated a connection object for the specified CTIQBE media traffic. This message is rate limited to one message every 10 seconds.

**Recommended Action** None required.

### 620002

**Error Message** %ASA-4-620002: Drop CTIQBE packet from _interface\_name_:_ip\_address_/_port_ to _interface\_name_:_ip\_address_/_port_ Reason: _reason\_string_

**Explanation** The ASA received a CTIQBE message with an unsupported version number, and dropped the packet. This message is rate limited to one message every 10 seconds.

**Recommended Action** If the version number captured in the log message is unreasonably large (greater than 10), the packet may be malformed, a non-CTIQBE packet, or corrupted before it arrives at the ASA. We recommend that you determine the source of the packets. If the version number is reasonably small (less than or equal to 10), then contact the Cisco TAC to see if a new ASA image that supports this CTIQBE version is available.

### 621001

**Error Message** `%ASA-6-621001: Interface` _interface\_name_ does not support multicast, not enabled

**Explanation** An attempt was made to enable PIM on an interface that does not support multicast.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 621002

**Error Message** `%ASA-6-621002: Interface` _interface\_name_ does not support multicast, not enabled

**Explanation** An attempt was made to enable IGMP on an interface that does not support multicast.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 621003

**Error Message** `%ASA-6-621003: The event queue size has exceeded` _number_

**Explanation** The number of event managers created has exceeded the expected amount.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 621006

**Error Message** `%ASA-6-621006: Mrib disconnected`, (_IP\_address_ ,_IP\_address_ ) event cancelled

**Explanation** A packet triggering a data-driven event was received, but the connection to the MRIB was down. The notification was canceled.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 621007

**Error Message** `%ASA-6-621007: Bad register from` _interface\_name_ :_IP\_address_ to _IP\_address_ for (_IP\_address_ , _IP\_address_ )

**Explanation** A PIM router configured as a rendezvous point or with NAT has received a PIM register packet from another PIM router. The data encapsulated in this packet is invalid.

**Recommended Action** The sending router is erroneously sending non-RFC registers. Upgrade the sending router.

### 622001

**Error Message** `%ASA-6-622001: _action_ tracked route _destination_network_ _netmask_ _nexthop_address_, distance _admin_distance_, table _routing_table_name_, on interface _interface_name_`_string_ tracked route _network mask address_ , distance _number_ , table _string_ , on interface _interface-name_

**Explanation** A tracked route has been added to or removed from a routing table, which means that the state of the tracked object has changed from up or down.

-   _string_ —Adding or Removing
-   _network_ —The network address
-   _mask_ —The network mask
-   _address_ —The gateway address
-   _number_ —The route administrative distance
-   _string_ —The routing table name
-   _interface-name_ —The interface name as specified by the nameif command

**Recommended Action** None required.

### 622101

**Error Message** `%ASA-6-622101: Starting regex table compilation for _match_command_, table entries = _regex_num_ entries`

**Explanation** Information on the background activities of regex compilation appear.

-   _match\_command_ —The match command to which the regex table is associated
-   _regex\_num_ —The number of regex entries to be compiled

**Recommended Action** None required.

### 622102

**Error Message** `%ASA-6-622102: Completed regex table compilation for _match_command_, table size = _num_ bytes`

**Explanation** Information on the background activities of the regex compilation appear.

-   _match\_command_ —The match command to which the regex table is associated
-   _num_ —The size, in bytes, of the compiled table

**Recommended Action** None required.