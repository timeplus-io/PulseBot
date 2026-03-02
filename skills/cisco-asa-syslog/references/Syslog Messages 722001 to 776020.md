## Messages 722001 to 722056

This section includes messages from 722001 to 722056.

### 722001

**Error Message** `%ASA-4-722001: IP _IP_address_ Error parsing SVC connect request.`

**Explanation** The request from the SVC was invalid.

**Recommended Action** Research as necessary to determine if this error was caused by a defect in the SVC, an incompatible SVC version, or an attack against the device.

### 722002

**Error Message** `%ASA-4-722002: IP _IP_address_ Error consolidating SVC connect request.`

**Explanation** There is not enough memory to perform the action.

**Recommended Action** Purchase more memory, upgrade the device, or reduce the load on the device.

### 722003

**Error Message** `%ASA-4-722003: IP _IP_address_ Error authenticating SVC connect request.`

**Explanation** The user took too long to download and connect.

**Recommended Action** Increase the timeouts for session idle and maximum connect time.

### 722004

**Error Message** `%ASA-4-722004: Group _group_ User _user-name_ IP _IP_address_ Error responding to SVC connect request.`

**Explanation** There is not enough memory to perform the action.

**Recommended Action** Purchase more memory, upgrade the device, or reduce the load on the device.

### 722005

**Error Message** `%ASA-5-722005: Group _group_ User _user-name_ IP _IP_address_ Unable to update session information for SVC connection.`

**Explanation** There is not enough memory to perform the action.

**Recommended Action** Purchase more memory, upgrade the device, or reduce the load on the device.

### 722006

**Error Message** `%ASA-5-722006: Group _group_ User _user-name_ IP _ip_address_ Invalid address _ip_address_ assigned to SVC connection.`

**Explanation** An invalid address was assigned to the user.

**Recommended Action** Verify and correct the address assignment, if possible. Otherwise, notify your network administrator or escalate this issue according to your security policy. For additional assistance, contact the Cisco TAC.

### 722007

**Error Message** `%ASA-3-722007: Group _group_ User _user-name_ IP _IP_address_ SVC Message: _type-num_/EMERGENCY: _message_.`

**Explanation** The SVC issued a message.

-   type-num— A number from 0 to 31 indicating a message type. Message types are as follows:

\- 0—Normal

\- 16—Logout

\- 17—Closed due to error

\- 18—Closed due to rekey

\- 1-15, 19-31—Reserved and unused

-   message—A text message from the SVC

**Recommended Action** None required.

### 722008

**Error Message** `%ASA-3-722008: Group _group_ User _user-name_ IP _IP_address_ SVC Message: _type-num_/ALERT: _message_.`

**Explanation** The SVC issued a message.

-   type-num— A number from 0 to 31 indicating a message type. Message types are as follows:

\- 0—Normal

\- 16—Logout

\- 17—Closed due to error

\- 18—Closed due to rekey

\- 1-15, 19-31—Reserved and unused

-   message—A text message from the SVC

**Recommended Action** None required.

### 722009

**Error Message** `%ASA-3-722009: Group _group_ User _user-name_ IP _IP_address_ SVC Message: _type-num_/CRITICAL: _message_.`

**Explanation** The SVC issued a message.

-   type-num— A number from 0 to 31 indicating a message type. Message types are as follows:

\- 0—Normal

\- 16—Logout

\- 17—Closed due to error

\- 18—Closed due to rekey

\- 1-15, 19-31—Reserved and unused

-   message—A text message from the SVC

**Recommended Action** None required.

### 722010

**Error Message** `%ASA-5-722010: Group _group_ User _user-name_ IP _IP_address_ SVC Message: _type-num_/ERROR: _message_.`

**Explanation** The SVC issued a message.

-   type-num— A number from 0 to 31 indicating a message type. Message types are as follows:

\- 0—Normal

\- 16—Logout

\- 17—Closed due to error

\- 18—Closed due to rekey

\- 1-15, 19-31—Reserved and unused

-   message—A text message from the SVC

**Recommended Action** None required.

### 722011

**Error Message** `%ASA-5-722011: Group _group_ User _user-name_ IP _IP_address_ SVC Message: _type-num_/WARNING: _message_.`

**Explanation** The SVC issued a message.

-   type-num— A number from 0 to 31 indicating a message type. Message types are as follows:

\- 0—Normal

\- 16—Logout

\- 17—Closed due to error

\- 18—Closed due to rekey

\- 1-15, 19-31—Reserved and unused

-   message—A text message from the SVC

**Recommended Action** None required.

### 722012

**Error Message** `%ASA-5-722012: Group _group_ User _user-name_ IP _IP_address_ SVC Message: _type-num_/NOTICE: _message_.`

**Explanation** The SVC issued a message.

-   type-num— A number from 0 to 31 indicating a message type. Message types are as follows:

\- 0—Normal

\- 16—Logout

\- 17—Closed due to error

\- 18—Closed due to rekey

\- 1-15, 19-31—Reserved and unused

-   message—A text message from the SVC

**Recommended Action** None required.

### 722013

**Error Message** `%ASA-6-722013: Group _group_ User _user-name_ IP _IP_address_ SVC Message: _type-num_/INFO: _message_.`

**Explanation** The SVC issued a message.

-   type-num— A number from 0 to 31 indicating a message type. Message types are as follows:

\- 0—Normal

\- 16—Logout

\- 17—Closed due to error

\- 18—Closed due to rekey

\- 1-15, 19-31—Reserved and unused

-   message—A text message from the SVC

**Recommended Action** None required.

### 722014

**Error Message** `%ASA-6-722014: Group _group_ User _user-name_ IP _IP_address_ SVC Message: _type-num_/DEBUG: _message_.`

**Explanation** The SVC issued a message.

-   type-num— A number from 0 to 31 indicating a message type. Message types are as follows:

\- 0—Normal.

\- 16—Logout

\- 17—Closed due to error

\- 18—Closed due to rekey

\- 1-15, 19-31—Reserved and unused

-   message—A text message from the SVC

**Recommended Action** None required.

### 722015

**Error Message** `%ASA-4-722015: Group _group_ User _user-name_ IP _IP_address_ Unknown SVC frame type: _type-num_`

**Explanation** The SVC sent an invalid frame type to the device, which might be caused by an SVC version incompatibility.

-   type-num—The number identifier of the frame type

**Recommended Action** Verify the SVC version.

### 722016

**Error Message** `%ASA-4-722016: Group _group_ User _user-name_ IP _IP_address_ Bad SVC frame length: _length_ expected: _expected-length_`

**Explanation** The expected amount of data was not available from the SVC, which might be caused by an SVC version incompatibility.

**Recommended Action** Verify the SVC version.

### 722017

**Error Message** `%ASA-4-722017: Group _group_ User _user-name_ IP _ip_address_ Bad SVC framing: _xx_.2X_xx_.2X_xx_.2X>, reserved: _xx_`

**Explanation** The SVC sent a badly framed datagram, which might be caused by an SVC version incompatibility.

**Recommended Action** Verify the SVC version.

### 722018

**Error Message** `%ASA-4-722018: Group _group_ User _user-name_ IP _IP_address_ Bad SVC protocol version: _version_, expected: _expected_`

**Explanation** The SVC sent a version unknown to the device, which might be caused by an SVC version incompatibility.

**Recommended Action** Verify the SVC version.

### 722019

**Error Message** `%ASA-4-722019: Group _group_ User _user-name_ IP _IP_address_ Not enough data for an SVC header: _length_`

**Explanation** The expected amount of data was not available from the SVC, which might be caused by an SVC version incompatibility.

**Recommended Action** Verify the SVC version.

### 722020

**Error Message** `%ASA-3-722020: TunnelGroup _tunnel_group_ GroupPolicy _group_policy_ User _user-name_ IP _IP_address_ No address available for SVC connection`

**Explanation** Address assignment failed for the AnyConnect session. No IP addresses are available.

-   tunnel\_group—The name of the tunnel group that the user was assigned to or used to log in
-   _group\_policy_ —The name of the group policy that the user was assigned to
-   _user-name_ —The name of the user with which this message is associated
-   _IP\_address_ —The public IP (Internet) address of the client machine

**Recommended Action** Check the configuration listed in the ip local ip command to see if enough addresses exist in the pools that have been assigned to the tunnel group and the group policy. Check the DHCP configuration and status. Check the address assignment configuration. Enable IPAA syslog messages to determine why the AnyConnect client cannot obtain an IP address.

### 722021

**Error Message** `%ASA-3-722021: Group _group_ User _user-name_ IP _IP_address_ Unable to start compression due to lack of memory resources`

**Explanation** There is not enough memory to perform the action.

**Recommended Action** Purchase more memory, upgrade the device, or reduce the load on the device.

### 722022

**Error Message** `%ASA-6-722022: Group _group-name_ User _user-name_ IP _addr_ _(TCP|UDP)_ SVC connection established _(with|without)_ compression`

**Explanation** The TCP or UDP connection was established with or without compression.

**Recommended Action** None required.

### 722023

**Error Message** `%ASA-6-722023: Group <_group_> User <_user_name_> IP <ip_address> _conn_type_ SVC connection terminated _with|without_ compression`

**Explanation** The SVC terminated either with or without compression.

**Recommended Action** None required.

### 722024

**Error Message** `%ASA-6-722024: SVC Global Compression Enabled`

**Explanation** Subsequent SVC connections will be allowed to perform tunnel compression if SVC compression is enabled in the corresponding user or group configuration.

**Recommended Action** None required.

### 722025

**Error Message** `%ASA-6-722025: SVC Global Compression Disabled`

**Explanation** Subsequent SVC connections will not be allowed to perform tunnel compression.

**Recommended Action** None required.

### 722026

**Error Message** `%ASA-6-722026: Group _group_ User _user-name_ IP _IP_address_ SVC compression history reset`

**Explanation** A compression error occurred. The SVC and the ASA corrected it.

**Recommended Action** None required.

### 722027

**Error Message** `%ASA-6-722027: Group _group_ User _user-name_ IP _IP_address_ SVC decompression history reset`

**Explanation** A decompression error occurred. The SVC and the ASA corrected it.

**Recommended Action** None required.

### 722028

**Error Message** `%ASA-5-722028: Group _group_ User _user-name_ IP _IP_address_ Stale SVC connection closed.`

**Explanation** An unused SVC connection was closed.

**Recommended Action** None required. However, the client may be having trouble connecting if multiple connections are established. The SVC log should be examined.

### 722029

**Error Message** `%ASA-7-722029: Group _group_ User _user-name_ IP _IP_address_ SVC Session Termination: Conns: _connections_, DPD Conns: _DPD_conns_, Comp resets: _compression_resets_, Dcmp resets: _decompression_resets_.`

**Explanation** The number of connections, reconnections, and resets that have occurred are reported. If connections is greater than 1 or the number of DPD\_conns, compression\_resets, or decompression\_resets is greater than 0, it may indicate network reliability problems, which may be beyond the control of the Secure Firewall ASA administrator. If there are many connections or DPD connections, the user may be having problems connecting and may experience poor performance.

-   connections—The total number of connections during this session (one is normal)
-   DPD\_conns—The number of reconnections due to DPD
-   compression\_resets—The number of compression history resets
-   decompression\_resets—The number of decompression history resets

**Recommended Action** The SVC log should be examined. You may want to research and take appropriate action to resolve possible network reliability problems.

### 722030

**Error Message** `%ASA-7-722030: Group _group_ User _user-name_ IP _IP_address_ SVC Session Termination: In: _data_bytes_ (+_ctrl_bytes_) bytes, _data_pkts_ (+_ctrl_pkts_) packets, _drop_pkts_ drops.`

**Explanation** End-of-session statistics are being recorded.

-   data\_bytes—The number of inbound (from SVC) data bytes
-   ctrl\_bytes—The number of inbound control bytes
-   data\_pkts—The number of inbound data packets
-   ctrl\_pkts—The number of inbound control packets
-   drop\_pkts—The number of inbound packets that were dropped

**Recommended Action** None required.

### 722031

**Error Message** `%ASA-7-722031: Group _group_ User _user-name_ IP _IP_address_ SVC Session Termination: Out: _data_bytes_ (+_ctrl_bytes_) bytes, _data_pkts_ (+_ctrl_pkts_) packets, _drop_pkts_ drops.`

**Explanation** End-of-session statistics are being recorded. The statistics include data bytes, control packet bytes, data packets, control packets, and dropped packets.

-   data\_bytes—The number of outbound (to SVC) data bytes
    
-   ctrl\_bytes—The number of outbound control bytes
    
-   data\_pkts—The number of outbound data packets
    
-   ctrl\_pkts—The number of outbound control packets
    
-   drop\_pkts—The number of outbound packets that were dropped
    

In some cases, the dropped packets count is more than the overall data and control packets because this syslog does not provide the break-down of the dropped packets. Few examples of such instances:

`2020-09-30T09:06:09.254798+00:00 local4.err pg122d-vpn116 %ASA-3-722031: Group <GP_1> User <xxxxxxxxxxxx.xxxxxxxxxx@intel.com> IP <x.x.x.x> SVC Session Termination: Out: 800808 (+32) bytes, 1957 (+4) packets, 3358 drops.`

`2020-09-30T08:53:11.359833+00:00 local4.err srr10c-vpn103 %ASA-3-722031: Group <GP_2> User <xxxxxxxxxxxx.xxxxxxxxxx@intel.com> IP <x.x.x.x> SVC Session Termination: Out: 413194 (+32) bytes, 1540 (+4) packets, 2059 drops.`

`2020-09-30T08:37:59.287415+00:00 local4.err srr10c-vpn115 %ASA-3-722031: Group <GP_3> User <xxxxxxxxxxxx.xxxxxxxxxx@intel.com> IP <x.x.x.x> SVC Session Termination: Out: 571473 (+48) bytes, 1283 (+6) packets, 1323 drops.`

`2020-09-30T08:31:48.105943+00:00 local4.err srr10c-vpn114 %ASA-3-722031: Group <GP_4> User <xxxxxxxxxxxx.xxxxxxxxxx@intel.com> IP <x.x.x.x> SVC Session Termination: Out: 131566 (+0) bytes, 283 (+0) packets, 320 drops.`

`2020-09-30T08:28:38.053003+00:00 local4.err pg122d-vpn117 %ASA-3-722031: Group <GP_5> User <xxxxxxxxxxxx.xxxxxxxxxx@intel.com> IP <x.x.x.x> SVC Session Termination: Out: 497446 (+23) bytes, 1048 (+1) packets, 1128 drops.`

`2020-09-30T07:45:43.044373+00:00 local4.err srr10c-vpn114 %ASA-3-722031: Group <GP_6> User <xxxxxxxxxxxx.xxxxxxxxxx@intel.com> IP <x.x.x.x> SVC Session Termination: Out: 153165 (+16) bytes, 398 (+2) packets, 1045 drops.`

**Recommended Action** None required.

### 722032

**Error Message** `%ASA-5-722032: Group <_group_> User <_user_name_> IP <_ip_address_> New _TCP|UDP_ SVC connection replacing old connection.`

**Explanation** A new SVC connection is replacing an existing one. You may be having trouble connecting.

**Recommended Action** Examine the SVC log.

### 722033

**Error Message** `%ASA-5-722033: Group <_group_> User <_user_name_> IP <_ip_address_> First _TCP|UDP_ SVC connection established for SVC session.`

**Explanation** The first SVC connection was established for the SVC session.

**Recommended Action** None required.

### 722034

**Error Message** `%ASA-5-722034: Group <_group_> User <_user_name_> IP <_ip_address_> New _TCP|UDP_ SVC connection, no existing connection.`

**Explanation** A reconnection attempt has occurred. An SVC connection is replacing a previously closed connection. There is no existing connection for this session because the connection was already dropped by the SVC or the Secure Firewall ASA. You may be having trouble connecting.

**Recommended Action** Examine the Secure Firewall ASA log and SVC log.

### 722035

**Error Message** `%ASA-3-722035: Group _group_ User _user-name_ IP _IP_address_ Received large packet _length_ (threshold _num_).`

**Explanation** A large packet was received from the client.

-   length—The length of the large packet
-   num—The threshold

**Recommended Action** Enter the anyconnect ssl df-bit-ignore enable command under the group policy to allow the Secure Firewall ASA to fragment the packets arriving with the DF bit set.

### 722036

**Error Message** `%ASA-6-722036: Group _group_ User _user-name_ IP _IP_address_ Transmitting large packet _length_ (threshold _num_).`

**Explanation** A large packet was sent to the client. The source of the packet may not be aware of the MTU of the client. This could also be due to compression of non-compressible data.

-   length—The length of the large packet
-   num—The threshold

**Recommended Action** Turn off SVC compression, otherwise, none required.

### 722037

**Error Message** `%ASA-5-722037: Group _group_ User _user-name_ IP _ip_address_ SVC closing connection: _reason_.`

**Explanation** An SVC connection was terminated for the given reason. This behavior may be normal, or you may be having trouble connecting.

-   reason—The reason that the SVC connection was terminated

**Recommended Action** Examine the SVC log.

### 722038

**Error Message** `%ASA-5-722038: Group _group_ User _name_ IP _user-name_ SVC terminating session: _reason_.`

**Explanation** An SVC session was terminated for the given reason. This behavior may be normal, or you may be having trouble connecting.

-   reason—The reason that the SVC session was terminated

**Recommended Action** Examine the SVC log if the reason for termination was unexpected.

### 722039

**Error Message** `%ASA-4-722039: Group _group_ User _user_ IP _ip_ SVC 'vpn-filter _acl_' is an IPv6 ACL; ACL not applied.`

**Explanation** The type of ACL to be applied is incorrect. An IPv6 ACL has been configured as an IPv4 ACL through the vpn-filter command.

-   _group_ —The group policy name of the user
-   _user_ —The username
-   _ip_ —The public (not assigned) IP address of the user
-   _acl_ —The name of the invalid ACL

**Recommended Action** Validate the VPN filter and IPv6 VPN filter configurations on the ASA, and the filter parameters on the AAA (RADIUS) server. Make sure that the correct type of ACL is specified.

### 722040

**Error Message** `%ASA-4-722040: Group _group_ User _user_ IP _ip_ SVC 'ipv6-vpn-filter _acl_' is an IPv4 ACL; ACL not applied.`

**Explanation** The type of ACL to be applied is incorrect. An IPv4 ACL has been configured as an IPv6 ACL through the ipv6-vpn-filter command.

-   _group_ —The group policy name of the user
-   _user_ —The username
-   _ip_ —The public (not assigned) IP address of the user
-   _acl_ —The name of the invalid ACL

**Recommended Action** Validate the VPN filter and IPv6 VPN filter configurations on the ASA and the filter parameters on the AAA (RADIUS) server. Make sure that the correct type of ACL is specified.

### 722041

**Error Message** `%ASA-4-722041: TunnelGroup _tunnel_group_ GroupPolicy _group_policy_ User _username_ IP _peer_address_ No IPv6 address available for SVC connection`

**Explanation** An IPv6 address was not available for assignment to the remote SVC client.

-   _n_ —The SVC connection identifier

**Recommended Action** Augment or create an IPv6 address pool, if desired.

### 722042

**Error Message** `%ASA-4-722042: Group _group_ User _user_ IP _ip_ Invalid _Cisco_ SSL Tunneling Protocol version`

**Explanation** An invalid SVC or AnyConnect client is trying to connect.

-   _group_ —The name of the group policy with which the user is trying to connect
-   _user_ —The name of the user who is trying to connect
-   _ip_ —The IP address of the user who is trying to connect

**Recommended Action** Validate that the SVC or AnyConnect client is compatible with the Secure Firewall ASA.

### 722043

**Error Message** `%ASA-5-722043: Group _group_ User _user_ IP _ip_ DTLS disabled: unable to negotiate cipher`

**Explanation** The DTLS (UDP transport) cannot be established. The SSL encryption configuration was probably changed.

-   _group_ —The name of the group policy with which the user is trying to connect
-   _user_ —The name of the user who is trying to connect
-   _ip_ —The IP address of the user who is trying to connect

**Recommended Action** Revert the SSL encryption configuration. Make sure there is at least one block cipher (AES, DES, or 3DES) in the SSL encryption configuration.

### 722044

**Error Message** `%ASA-5-722044: Group _group_ User _user_ IP _ip_ Unable to request IPv_ver_ address for SSL tunnel`

**Explanation** An IP address cannot be requested because of low memory on the Secure Firewall ASA.

-   _group_ —The name of the group policy with which the user is trying to connect
-   _user_ —The name of the user who is trying to connect
-   _ip_ —The IP address of the user who is trying to connect
-   _ver_ —Either IPv4 or IPv6, based on the IP address version being requested

**Recommended Action** Reduce the load on the Secure Firewall ASA or add more memory.

### 722045

**Error Message** `%ASA-3-722045: Connection terminated: no SSL tunnel initialization data`

**Explanation** Data to establish a connection is missing. This is a defect in the Secure Firewall ASA software.

**Recommended Action** Contact the Cisco TAC for assistance.

### 722046

**Error Message** `%ASA-3-722046: Group _group_ User _user_ IP _ip_ Session terminated: Unable to establish tunnel`

**Explanation** The Secure Firewall ASA cannot set up connection parameters. This is a defect in the Secure Firewall ASA software.

-   _group_ —The name of the group policy with which the user is trying to connect
-   _user_ —The name of the user who is trying to connect
-   _ip_ —The IP address of the user who is trying to connect

**Recommended Action** Contact the Cisco TAC for assistance.

### 722047

**Error Message** `%ASA-4-722047: Group _group_ User _user_ IP _ip_ Tunnel terminated: SVC not enabled or invalid SVC image on the _ASA_`

**Explanation** The user logged in via the web browser and tried to start the SVC or AnyConnect client. The SVC service is not enabled globally, or the SVC image is invalid or corrupted. The tunnel connection has been terminated, but the clientless connection remains.

-   _group_ —The name of the group policy with which the user is trying to connect
-   _user_ —The name of the user who is trying to connect
-   _ip_ —The IP address of the user who is trying to connect

**Recommended Action** Enable the SVC globally using the svc enable command. Validate the integrity of versions of the SVC images by reloading new images using the svc image command.

### 722048

**Error Message** `%ASA-4-722048: Group _group_ User _user_ IP _ip_ Tunnel terminated: SVC not enabled for the user`

**Explanation** The user logged in via the web browser, and tried to start the SVC or AnyConnect client. The SVC service is not enabled for this user. The tunnel connection has been terminated, but the clientless connection remains.

-   _group_ —The name of the group policy with which the user is trying to connect
-   _user_ —The name of the user who is trying to connect
-   _ip_ —The IP address of the user who is trying to connect

**Recommended Action** Enable the service for this user using the group-policy and username commands.

### 722049

**Error Message** `%ASA-4-722049: Group _group_ User _user_ IP _ip_ Session terminated: SVC not enabled or invalid SVC image on the _ASA_`

**Explanation** The user logged in via the AnyConnect client. The SVC service is not enabled globally, or the SVC image is invalid or corrupted. The session connection has been terminated.

-   _group_ —The name of the group policy with which the user is trying to connect
-   _user_ —The name of the user who is trying to connect
-   _ip_ —The IP address of the user who is trying to connect

**Recommended Action** Enable the SVC globally using the svc-enable command. Validate the integrity and versions of the SVC images by reloading new images using the svc image command.

### 722050

**Error Message** `%ASA-4-722050: Group _group_ User _user_ IP _ip_ Session terminated: SVC not enabled for the user`

**Explanation** The user logged in through the AnyConnect client. The SVC service is not enabled for this user. The session connection has been terminated.

-   _group_ —The name of the group policy with which the user is trying to connect
-   _user_ —The name of the user who is trying to connect
-   _ip_ —The IP address of the user who is trying to connect

**Recommended Action** Enable the service for this user using the group-policy and username commands.

### 722051

**Error Message** `%ASA-6-722051: Group _group-policy_ User _username_ IP _public-ip_ IPv4 Address _assigned-ip_ IPv6 address _assigned-ip_ assigned to session`

**Explanation** The specified address has been assigned to the given user.

-   _group-policy_ —The group policy that allowed the user to gain access
-   _username_ —The name of the user
-   _public-ip_ —The public IP address of the connected client
-   _assigned-ip_ —The IPv4 or IPv6 address that is assigned to the client

**Recommended Action** None required.

### 722053

**Error Message** `%ASA-6-722053: Group _g_ User _u_ IP _ip_ Unknown client _user-agent_ connection`

**Explanation** An unknown or unsupported SSL VPN client has connected to the Secure Firewall ASA. Older clients include the Cisco SVC and the Cisco AnyConnect client earlier than Version 2.3.1.

-   _g_ —The group policy under which the user logged in
-   _u_ —The name of the user
-   _ip_ —The IP address of the client
-   _user-agent_ —The user agent (usually includes the version) received from the client

**Recommended Action** Upgrade to a supported Cisco SSL VPN client.

### 722054

**Error Message** `%ASA-4-722054: Group _group_policy_ User _user_name_ IP _remote_IP_ SVC terminating connection: Failed to install Redirect URL: _redirect_URL_ Redirect ACL: _non_exist_ for _assigned_IP_.`

**Explanation** An error occurred for an AnyConnect VPN connection when a redirect URL was installed, and the ACL was received from the ISE, but the redirect ACL does not exist on the Secure Firewall ASA.

-   _group policy_ —The group policy that allowed the user to gain access
-   _user name_ —Username of the requester for the remote access
-   _remote IP_ — Remote IP address that the connection request is coming from
-   _redirect URL_ —The URL for the HTTP traffic redirection
-   _assigned IP_ —The IP address that is assigned to the user

**Recommended Action** Configure the redirect ACL on the Secure Firewall ASA.

### 722055

**Error Message** `%ASA-6-722055: Group _group-policy_ User _username_ IP _public-ip_ Client Type: _user-agent_`

**Explanation** The indicated user is attempting to connect with the given user-agent.

-   _group-policy_ —The group policy that allowed the user to gain access
-   _username_ —The name of the user
-   _public-ip_ —The public IP address of the connected client
-   _user-agent_ —The user-agent string provided by the connecting client. Usually includes the AnyConnect version and host operating system for AnyConnect clients.

**Recommended Action** None required.

### 722056

**Error Message** `%ASA-4-722056: Unsupported AnyConnect client connection rejected from ip address. Client info: user-agent string. Reason: reason`

**Explanation** This syslog indicates that an AnyConnect client connection is rejected. The reason for this is provided in the syslog along with the client information.

-   _ip address_ —IP address from which a connection with the old client is attempted,
-   _user- agent string_ —User-Agent header in the client request. Usually includes the AnyConnect version and host operating system for AnyConnect clients
-   _reason_ —Reason for rejection

**Recommended Action** Use the client information and reason provided in the syslog to resolve the issue.

### 722057

**Error Message** `%ASA-4-722057: Group _group policy_ User _username_ IP _client IP_ SVC terminating connection: Failed to bind SGT _tag_ with assigned IP: _assigned IP_.`

**Explanation** When the device  fails to bind a Security Group Tag (SGT) to the assigned IP address during remote access VPN authentication, this message is generated. The syslog message provides information that helps to identify when an SGT binding error occurs, along with specific user, group, and IP information, making it much easier to diagnose and resolve related issues.

**Recommended Action** Use the client information and reason provided in the syslog to resolve the issue.

## Messages 723001 to 736001

This section includes messages from 723001 to 736001.

### 723001

**Error Message** `%ASA-6-723001: Group _group-name_ User _user-name_ IP _IP_address_ WebVPN Citrix ICA connection _connection_ is up.`

**Explanation** The Citrix connection is up.

-   group-name—The name of the Citrix group
-   user-name—The name of the Citrix user
-   IP\_address—The IP address of the Citrix user
-   connection—The Citrix connection identifier

**Recommended Action** None required.

### 723002

**Error Message** `%ASA-6-723002: Group _group-name_ User _user-name_ IP _IP_address_ WebVPN Citrix ICA connection _connection_ is down.`

**Explanation** The Citrix connection is down.

-   group-name—The name of the Citrix group
-   user-name—The name of the Citrix user
-   IP\_address—The IP address of the Citrix user
-   connection—The Citrix connection identifier

**Recommended Action** No action is required when the Citrix ICA connection is terminated intentionally by the client, the server, or the Secure Firewall ASA administrator. However, if this is not the case, verify that the WebVPN session in which the Citrix ICA connection is set up is still active. If it is inactive, then receiving this message is normal. If the WebVPN session is still active, verify that the ICA client and Citrix server both work correctly and that there is no error displayed. If not, bring either or both up or respond to any error. If this message is still received, contact the Cisco TAC and provide the following information:

-   Network topology
-   Delay and packet loss
-   Citrix server configuration
-   Citrix ICA client information
-   Steps to reproduce the problem
-   Complete text of all associated messages

### 723003

**Error Message** `%ASA-7-723003: No memory for WebVPN Citrix ICA connection _connection_.`

**Explanation** The Secure Firewall ASA is running out of memory. The Citrix connection was rejected.

-   connection—The Citrix connection identifier

**Recommended Action** Verify that the Secure Firewall ASA is working correctly. Pay special attention to memory and buffer usage. If the Secure Firewall ASA is under heavy load, buy more memory and upgrade the Secure Firewall ASA or reduce the load on the Secure Firewall ASA. If the problem persists, contact the Cisco TAC.

### 723004

**Error Message** `%ASA-7-723004: WebVPN Citrix encountered bad flow control _flow_.`

**Explanation** The Secure Firewall ASA encountered an internal flow control mismatch, which can be caused by massive data flow, such as might occur during stress testing or with a high volume of ICA connections.

**Recommended Action** Reduce ICA connectivity to the Secure Firewall ASA. If the problem persists, contact the Cisco TAC.

### 723005

**Error Message** `%ASA-7-723005: No channel to set up WebVPN Citrix ICA connection.`

**Explanation** The Secure Firewall ASA was unable to create a new channel for Citrix.

**Recommended Action** Verify that the Citrix ICA client and the Citrix server are still alive. If not, bring them back up and retest. Check the Secure Firewall ASA load, paying special attention to memory and buffer usage. If the Secure Firewall ASA is under heavy load, upgrade the Secure Firewall ASA, add memory, or reduce the load. If the problem persists, contact the Cisco TAC.

### 723006

**Error Message** `%ASA-7-723006: WebVPN Citrix SOCKS errors.`

**Explanation** An internal Citrix SOCKS error has occurred on the Secure Firewall ASA.

**Recommended Action** Verify that the Citrix ICA client is working correctly. In addition, check the network connection status between the Citrix ICA client and the Secure Firewall ASA, paying attention to packet loss. Resolve any abnormal network conditions. If the problem persists, contact the Cisco TAC.

### 723007

**Error Message** `%ASA-7-723007: WebVPN Citrix ICA connection _connection_ list is broken.`

**Explanation** The Secure Firewall ASA internal Citrix connection list is broken.

-   connection—The Citrix connection identifier

**Recommended Action** Verify that the Secure Firewall ASA is working correctly, paying special attention to memory and buffer usage. If the Secure Firewall ASA is under heavy load, upgrade the Secure Firewall ASA, add memory, or reduce the load. If the problem persists, contact the Cisco TAC.

### 723008

**Error Message** `%ASA-7-723008: WebVPN Citrix ICA SOCKS Server _server_ is invalid.`

**Explanation** An attempt was made to access a Citrix Socks server that does not exist.

-   server—The Citrix server identifier

**Recommended Action** Verify that the Secure Firewall ASA is working correctly. Note whether or not there is any memory or buffer leakage. If this issue occurs frequently, capture information about memory usage, network topology, and the conditions during which this message is received. Send this information to the Cisco TAC for review. Make sure that the WebVPN session is still up while this message is being received. If not, determine the reason that the WebVPN session is down. If the Secure Firewall ASA is under heavy load, upgrade the Secure Firewall ASA, add memory, or reduce the load. If the problem persists, contact the Cisco TAC.

### 723009

**Error Message** `%ASA-7-723009: Group _group-name_ User _user-name_ IP _IP_address_ WebVPN Citrix received data on invalid connection _connection_.`

**Explanation** Data was received on a Citrix connection that does not exist.

-   group-name—The name of the Citrix group
-   user-name—The name of the Citrix user
-   IP\_address—The IP address of the Citrix user
-   connection—The Citrix connection identifier

**Recommended Action** The original published Citrix application connection was probably terminated, and the remaining active published applications lost connectivity. Restart all published applications to generate a new Citrix ICA tunnel. If the Secure Firewall ASA is under heavy load, upgrade the Secure Firewall ASA, add memory, or reduce the load. If the problem persists, contact the Cisco TAC.

### 723010

**Error Message** `%ASA-7-723010: Group _group-name_ User _user-name_ IP _IP_address_ WebVPN Citrix received data on invalid connection _channel_.`

**Explanation** An abort was received on a nonexistent Citrix connection, which can be caused by massive data flow (such as stress testing) or a high volume of ICA connections, especially during network delay or packet loss.

-   group-name—The name of the Citrix group
-   user-name—The name of the Citrix user
-   IP\_address—The IP address of the Citrix user
-   channel—The Citrix channel identifier
-   connection—The Citrix connection identifier

**Recommended Action** Reduce the number of ICA connections to the Secure Firewall ASA, obtain more memory for the Secure Firewall ASA, or resolve the network problems.

### 723011

**Error Message** `%ASA-7-723011: Group _group-name_ User _user-name_ IP _IP_address_ WebVPN Citrix received bad SOCKS _socks_ message length _msg-length_. Expected length is _exp-msg-length_.`

**Explanation** The Citrix SOCKS message length is incorrect.

-   group-name—The name of the Citrix group
-   user-name—The name of the Citrix user
-   IP\_address—The IP address of the Citrix user

**Recommended Action** Verify that the Citrix ICA client is working correctly. In addition, check the network connection status between the ICA client and the Secure Firewall ASA, paying attention to packet loss. After resolving any abnormal network conditions, if the problem still exists, contact the Cisco TAC.

### 723012

**Error Message** `%ASA-7-723012: Group _group-name_ User _user-name_ IP _IP_address_ WebVPN Citrix received bad SOCKS _socks_ message format.`

**Explanation** The Citrix SOCKS message format is incorrect.

-   group-name—The name of the Citrix group
-   user-name—The name of the Citrix user
-   IP\_address—The IP address of the Citrix user

**Recommended Action** Verify that the Citrix ICA client is working correctly. In addition, check the network connection status between the ICA client and the Secure Firewall ASA, paying attention to packet loss. After resolving any abnormal network conditions, if the problem still exists, contact the Cisco TAC.

### 723013

**Error Message** `%ASA-7-723013: WebVPN Citrix encountered invalid connection _connection_ during periodic timeout.`

**Explanation** The Secure Firewall ASA internal Citrix timer has expired, and the Citrix connection is invalid.

-   connection—The Citrix connection identifier

**Recommended Action** Check the network connection between the Citrix ICA client and the Secure Firewall ASA, and between the Secure Firewall ASA and the Citrix server. Resolve any abnormal network conditions, especially delay and packet loss. Verify that the Secure Firewall ASA works correctly, paying special attention to memory or buffer problems. If the Secure Firewall ASA is under heavy load, obtain more memory, upgrade the Secure Firewall ASA, or reduce the load. If the problem persists, contact the Cisco TAC.

### 723014

**Error Message** `%ASA-7-723014: Group _group-name_ User _user-name_ IP _IP_address_ WebVPN Citrix TCP connection _connection_ to server _server_ on channel _channel_ initiated.`

**Explanation** The Secure Firewall ASA internal Citrix Secure Gateway is connected to the Citrix server.

-   group-name—The name of the Citrix group
-   user-name—The name of the Citrix user
-   IP\_address—The IP address of the Citrix user
-   connection—The connection name
-   server—The Citrix server identifier
-   channel—The Citrix channel identifier (hexadecimal)

**Recommended Action** None required.

### 724001

**Error Message** `%ASA-4-724001: Group _group-name_ User _user-name_ IP _IP_address_ WebVPN session not allowed. Unable to determine if Secure Desktop software was running on the client's workstation.`

**Explanation** The session was not allowed because an error occurred during processing of the CSD Host Integrity Check results on the Secure Firewall ASA.

-   group-name—The name of the group
-   user-name—The name of the user
-   IP\_address—The IP address

**Recommended Action** Determine whether the client firewall is truncating long URLs. Uninstall CSD from the client and reconnect to the Secure Firewall ASA.

### 724002

**Error Message** `%ASA-4-724002: Group _group-name_ User _user-name_ IP _IP_address_ WebVPN session not terminated. Secure Desktop was not running on the client's workstation.`

**Explanation** CSD is not running on the client machine.

-   group-name—The name of the group
-   user-name—The name of the user
-   IP\_address—The IP address

**Recommended Action** Verify that the end user can install and run CSD on the client machine.

### 725001

**Error Message** `%ASA-6-725001: Starting SSL handshake with _peer-type_ _interface_:_src-ip_/_src-port_ to _dst-ip_/_dst-port_ for _protocol_ session`

**Explanation** The SSL handshake has started with the remote device, which can be a client or server.

-   peer-type—Either the server or the client, depending on the device that initiated the connection
-   interface—The interface name that the SSL session is using
-   source-ip—The source IPv4 or IPv6 address
-   src-port—The source port number
-   dst-ip—The destination IP address
-   dst-port—The destination port number
-   protocol—The SSL version used for the SSL handshake

**Recommended Action** None required.

### 725002

**Error Message** `%ASA-6-725002: Device completed SSL handshake with _peer-type_ _interface_:_src-ip_/_src-port_ to _dst-ip_/_dst-port_ for _protocol-version_ session`

**Explanation** The SSL handshake has completed successfully with the remote device.

-   peer-type—Either the server or the client, depending on the device that initiated the connection
-   interface—The interface name that the SSL session is using
-   source-ip—The source IPv4 or IPv6 address
-   src-port—The source port number
-   _dst-ip_ —The destination IP address
-   _dst-port_ —The destination port number
-   _protocol-version_ —The version of the SSL protocol being used: SSLv3, TLSv1, DTLSv1, DTLSv1.2, TLSv1.1 or TLSv1.2

**Recommended Action** None required.

### 725003

**Error Message** `%ASA-6-725003: SSL client _peer-type_:_interface_/_src-ip_ to _src-port_/_dst-ip_ request to resume previous session`

**Explanation** The remote device is trying to resume a previous SSL session.

-   peer-type—Either the server or the client, depending on the device that initiated the connection
-   interface—The interface name that the SSL session is using
-   source-ip—The source IPv4 or IPv6 address
-   src-port—The source port number
-   _dst-ip_ —The destination IP address
-   _dst-port_ —The destination port number

**Recommended Action** None required.

### 725004

**Error Message** `%ASA-6-725004: Device requesting certificate from SSL client _peer-type_:_interface_/_src-ip_ to _src-port_/_dst-ip_ for authentication`

**Explanation** The Secure Firewall ASA has requested a client certificate for authentication.

-   peer-type—Either the server or the client, depending on the device that initiated the connection
-   interface—The interface name that the SSL session is using
-   source-ip—The source IPv4 or IPv6 address
-   src-port—The source port number
-   _dst-ip_ —The destination IP address
-   _dst-port_ —The destination port number

**Recommended Action** None required.

### 725005

**Error Message** `%ASA-6-725005: SSL server _peer-type_:_interface_/_src-ip_ to _src-port_/_dst-ip_ requesting our device certificate for authentication`

**Explanation** The server has requested the certificate of the Secure Firewall ASA for authentication.

-   peer-type—Either the server or the client, depending on the device that initiated the connection
-   interface—The interface name that the SSL session is using
-   source-ip—The source IPv4 or IPv6 address
-   src-port—The source port number
-   _dst-ip_ —The destination IP address
-   _dst-port_ —The destination port number

**Recommended Action** None required.

### 725006

**Error Message** `%ASA-6-725006: Device failed SSL handshake with _peer-type_ _interface_:_src-ip_/_src-port_ to _dst-ip_/_dst-port_`

**Explanation** The SSL handshake with the remote device has failed.

-   peer-type—Either the server or the client, depending on the device that initiated the connection
-   interface—The interface name that the SSL session is using
-   source-ip—The source IPv4 or IPv6 address
-   src-port—The source port number
-   _dst-ip_ —The destination IP address
-   _dst-port_ —The destination port number

**Recommended Action** Look for syslog message 725014, which indicates the reason for the failure.

### 725007

**Error Message** `%ASA-6-725007: SSL session with _peer-type_ _interface_:_src-ip_/_src-port_ to _dst-ip_/_dst-port_ terminated`

**Explanation** The SSL session has terminated.

-   peer-type—Either the server or the client, depending on the device that initiated the connection
-   interface—The interface name that the SSL session is using
-   source-ip—The source IPv4 or IPv6 address
-   src-port—The source port number
-   _dst-ip_ —The destination IP address
-   _dst-port_ —The destination port number

**Recommended Action** None required.

### 725008

**Error Message** `%ASA-7-725008: SSL client _peer-type_:_interface_/_src-ip_ to _src-port_/_dst-ip_ proposes the following _dst-port_ cipher(s)`

**Explanation** The number of ciphers proposed by the remote SSL device are listed.

-   peer-type—Either the server or the client, depending on the device that initiated the connection
-   interface—The interface name that the SSL session is using
-   source-ip—The source IPv4 or IPv6 address
-   src-port—The source port number
-   _dst-ip_ —The destination IP address
-   _dst-port_ —The destination port number
-   _n_ —The number of supported ciphers

**Recommended Action** None required.

### 725009

**Error Message** `%ASA-7-725009: Device proposes the following _n_ cipher(s) to server _interface_:_src-ip_/_src_port_ to _dst_ip_/_dst_port_`

**Explanation** The number of ciphers proposed to the SSL server are listed.

-   peer-type—Either the server or the client, depending on the device that initiated the connection
-   interface—The interface name that the SSL session is using
-   source-ip—The source IPv4 or IPv6 address
-   src-port—The source port number
-   _dst-ip_ —The destination IP address
-   _dst-port_ —The destination port number
-   _n_ —The number of supported ciphers

**Recommended Action** None required.

### 725010

**Error Message** `%ASA-7-725010: Device supports the following _n_ cipher(s)`

**Explanation** The number of ciphers supported by the Secure Firewall ASA for an SSL session are listed.

-   n—The number of supported ciphers

**Recommended Action** None required.

### 725011

**Error Message** `%ASA-7-725011: Cipher[_order_] : _cipher_name_`

**Explanation** Always following messages 725008, 725009, and 725010, this message indicates the cipher name and its order of preference.

-   order—The order of the cipher in the cipher list
-   cipher\_name—The name of the OpenSSL cipher from the cipher list

**Recommended Action** None required.

### 725012

**Error Message** `%ASA-7-725012: Device chooses cipher _cipher_ for the SSL session with client _peer-type_:_interface_/_src-ip_ to _src-port_/_dst-ip_`

**Explanation** The cipher that was chosen by the Cisco device for the SSL session is listed.

-   cipher—The name of the OpenSSL cipher from the cipher list
-   peer-type—Either the server or the client, depending on the device that initiated the connection
-   interface—The interface name that the SSL session is using
-   source-ip—The source IPv4 or IPv6 address
-   src-port—The source port number
-   _dst-ip_ —The destination IP address
-   _dst-port_ —The destination port number

**Recommended Action** None required.

### 725013

**Error Message** `%ASA-7-725013: SSL server _interface_:_src-ip_/_src-port_ to _dst-ip_/_dst-port_ chooses cipher _cipher_`

**Explanation** The cipher that was chosen by the server for the SSL session is identified.

-   peer-type—Either the server or the client, depending on the device that initiated the connection
-   interface—The interface name that the SSL session is using
-   source-ip—The source IPv4 or IPv6 address
-   src-port—The source port number
-   _dst-ip_ —The destination IP address
-   _dst-port_ —The destination port number
-   cipher—The name of the OpenSSL cipher from the cipher list

**Recommended Action** None required.

### 725014

**Error Message** `%ASA-7-725014: SSL lib error. Function: _function_ Reason: _reason_`

**Explanation** The reason for failure of the SSL handshake is indicated.

-   function—The function name where the failure is reported
-   reason—The description of the failure condition

**Recommended Action** Include this message when reporting any SSL-related issue to the Cisco TAC.

### 725015

**Error Message** `%ASA-3-725015: Error verifying client certificate. Public key size in client certificate (_actual_key_size_ bits) exceeds the maximum supported key size of _ideal_key_size_ bits`

**Explanation** The verification of an SSL client certificate failed because of an unsupported (large) key size.

**Recommended Action** Use client certificates with key sizes that are less than or equal to 4096 bits.

### 725016

**Error Message** `%ASA-6-725016: Device selects trust-point _trustpoint_ for _peer-type_ _interface_:_src-ip_/_src-port_ to _dst-ip_/_dst-port_`

**Explanation** With server-name indication (SNI), the certificate used for a given connection may not be the certificate configured on the interface. There is also no indication of which certificate trustpoint has been selected. This syslog gives an indication of the trustpoint used by the connection (given by _interface_ :_src-ip_ /_src-port_ ).

-   _trustpoint_ —The name of the configured trustpoint that is being used for the specified connection
-   _interface_ —The name of the interface on the Secure Firewall ASA
-   _src-ip_ —The IP address of the peer
-   _src-port_ —The port number of the peer
-   _dst-ip_ —The IP address of the destination
-   _dst-port_ —The port number of the destination

**Recommended Action** None required.

### 725017

**Error Message** `%ASA-7-725017: No certificates received during the handshake with _s_ _s_:_B_/_d_ to _B_/_d_ for _s_ session`

**Explanation** A remote client has not sent a valid certificate.

-   _remote\_device_ —Identifies whether a handshake is performed with the client or server
-   _ctm->interface_ —The interface name on which the handshake is sent
-   _ctm->src\_ip_ —The IP address of the SSL server, which will communicate with the client
-   _ctm->src\_port_ —The port of the SSL server, which will communicate with the client
-   _ctm->dst\_ip_ —The IP address of the client
-   _ctm->dst\_port_ —The port of the client through which it responds
-   _s->method->version_ —The protocol version involved in the transaction (SSLv3, TLSv1, or DTLSv1)

**Recommended Action** None required.

### 725021

**Error Message** `%ASA-7-725021: Device preferring _cipher-suite_ cipher(s). Connection info: _interface_ :_src-ip_ /_src-port_ to _dst-ip_ /_dst-port_`

**Explanation** The cipher suites being preferred when negotiating the handshake is listed in this message.

-   **cipher-suite**—Preferred cipher suite string
    
-   **interface**—The interface name that the SSL session is using
    
-   **src-ip**—The source IPv4 or IPv6 address
    
-   **src-port**—The source port number
    
-   **dst-ip**—The destination IPv4 or IPv6 address
    
-   **dst-port**—The destination port number
    

Following is a list of prefered cipher suite strings that are used when negotiating the handshake:

-   server
    
-   SUITE-B
    
-   ChaCha20
    
-   client
    
-   SHA-256 hash
    

**Recommended Action** None required.

### 725022

**Error Message** `%ASA-7-725022: Device skipping cipher : _cipher_ - _reason_. Connection info: _interface_ :_src-ip_ /_src-port_ to _dst-ip_ /_dst-port_`

**Explanation** This syslog displays the reason for skipping a particular cipher in a list of cipher suites when negotiating the handshake.

-   **cipher-suite**—Preferred cipher suite string
    
-   **reason**—Reason for skipping a cipher.
    
-   **interface**—The interface name that the SSL session is using
    
-   **src-ip**—The source IPv4 or IPv6 address
    
-   **src-port**—The source port number
    
-   **dst-ip**—The destination IPv4 or IPv6 address
    
-   **dst-port**—The destination port number
    

Following list provides few example reason for skipping a particular cipher:

-   Ephemeral EC key is not compatible with trust-point <trust point>
    
-   Not supported by protocol version
    
-   PSK server callback is not set
    
-   Not permitted by security callbacks
    
-   ECDHE-ECDSA is broken on Safari
    
-   Cipher suite does not use SHA256
    
-   Unknown cipher
    
-   Wrong cipher
    
-   Message digest changed
    
-   Ciphersuite from previous session not selected
    

**Recommended Action** None required.

### 725025

**Error Message** `%ASA-6-725025: SSL Pre-auth connection rate limit hit _s_ watermark`

**Explanation** When the device reaches the rate-limit threshold for the number of pre-authenticated SSL connections. This message appears when the number of pre-authenticated SSL connections is high (90% of the limit) or when it is low (70% of the limit). The syslog is rate-limited to one syslog for every 10 seconds. In this message, s denotes high or low of the threshold limit.

**Recommended Action** Contact Cisco TAC.

### 726001

**Error Message** `%ASA-6-726001: Inspected _im_protocol_ _im_service_ Session between Client _im_client_1_ Packet flow from _im_client_2_:/_src_ifc_/_sip_ to _sport_:/_dest_ifc_/_dip_ Action: _dport_ _action_`

**Explanation** An IM inspection was performed on an IM message and the specified criteria were satisfied. The configured action is taken.

-   _im\_protocol_ —MSN IM or Yahoo IM
-   _im\_service_ —The IM services, such as chat, conference, file transfer, voice, video, games, or unknown
-   _im\_client\_1_ , _im\_client\_2_ —The client peers that are using the IM service in the session: _client\_login\_name_ or “?”
-   _src\_ifc_ —The source interface name
-   _sip_ —The source IP address
-   _sport_ —The source port
-   _dest\_ifc_ —The destination interface name
-   _dip_ —The destination IP address
-   _dport_ —The destination port
-   _action_ —The action taken: reset connection, dropped connection, or received
-   _class\_map\_id_ —The matched class-map ID
-   _class\_map\_name_ —The matched class-map name

**Recommended Action** None required.

### 730001

**Error Message** `%ASA-7-730001: Group <_groupname_> User <_username_> IP <_ipaddr_> VLAN Mapping to VLAN <_vlanid_>.`

**Explanation** VLAN mapping succeeded.

-   _groupname_ —The group name
-   _username_ —The username
-   _ipaddr_ —The IP address of this session
-   _vlanid_ — The VLAN ID that is used for the VLAN mapping session

**Recommended Action** None required.

### 730002

**Error Message** `%ASA-6-730002: Group <_groupname_> User <_username_> IP <_ipaddr_> VLAN Mapping to VLAN <_vlanid_> failed.`

**Explanation** VLAN mapping failed.

-   _groupname_ —The group name
-   _username_ —The username
-   _ipaddr_ —The IP address of this session
-   _vlanid_ — The VLAN ID that is used for the VLAN mapping session

**Recommended Action** Verify that all the VLAN mapping-related configurations are correct, and that the VLAN ID is valid.

### 730003

**Error Message** `%ASA-7-730003: IP _ipaddr_ egress VLAN ID is set to _vlanid_.`

**Explanation** ASA receives an SNMP set message from NACApp to set the new VLAN ID for the session.

-   _ipaddr_ —The IP address of this session
-   _vlanid_ — The VLAN ID that is used for the VLAN mapping session

**Recommended Action** None required

### 730004

**Error Message** `%ASA-6-730004: Group _groupname_ User _username_ IP _ipaddr_ VLAN ID _vlanid_ from AAA ignored.`

**Explanation** The VLAN ID received from AAA is different from the current one in use, and it is ignored for the current session.

-   _groupname_ —The group name
-   _username_ —The username
-   _ipaddr_ —The IP address of this session
-   _vlanid_ — The VLAN ID that is used for the VLAN mapping session

**Recommended Action** If the newly received VLAN ID must be used, then the current session needs to be torn down. Otherwise, no action is required.

### 730005

**Error Message** `%ASA-3-730005: Group _DfltGrpPolicy_ User _username_ IP _IP_ VLAN ID _vlan_id_ from AAA is invalid.`

**Explanation** A VLAN mapping error has occurred. A VLAN may be out of range, unassigned to any interfaces, or assigned to multiple interfaces.

**Recommended Action** Verify the VLAN ID configurations on the AAA server and ASA are both correct.

### 730006

**Error Message** `%ASA-7-730006: Group _groupname_ , User _username_ , IP _ipaddr_ : is on NACApp AUTH VLAN _vlanid_ .`

**Explanation** The session is under NACApp posture assessment.

-   _groupname_ —The group name
-   _username_ —The username
-   _ipaddr_ —The IP address of this session
-   _vlanid_ — The VLAN ID that is used for the VLAN mapping session

**Recommended Action** None required.

### 730007

**Error Message** `%ASA-7-730007: Group _groupname_ User _username_ IP _ipaddr_ changed VLAN to _vlan_ ID _vlanid_.`

**Explanation** NACApp (Cisco NAC appliance) posture assessment is done with the session, the VLAN is changed from AUTH VLAN to a new VLAN.

-   _groupname_ —The group name
-   _username_ —The username
-   _ipaddr_ —The IP address of this session
-   _%s_ —A string
-   _vlanid_ — The VLAN ID that is used for the VLAN mapping session

**Recommended Action** None required.

### 730008

**Error Message** `%ASA-6-730008: Group _groupname,_ User _username,_ IP ipaddr, VLAN MAPPING timeout waiting NACApp.`

**Explanation** NACApp (Cisco NAC appliance) posture assessment takes longer than the timeout value configured.

-   _groupname_ —The group name
-   _username_ —The username
-   _ipaddr_ —The IP address of this session

**Recommended Action** Check the status of the NACApp setup.

### 730009

**Error Message** `%ASA-5-730009: Group _groupname_ , User _username,_ IP _ipaddr_ , CAS _casaddr_ , capacity exceeded, terminating connection.`

**Explanation** The load capacity of the NACApp (Cisco NAC appliance) CAS is execeeded, the new incoming session that uses it is terminating.

-   _groupname_ —The group name
-   _username_ —The username
-   _ipaddr_ —The IP address of this session
-   _casaddr_ —The IP Address of CAS (Clean Access Server)

**Recommended Action** Review and revise planning for how many groups, and which groups, are associated with the CAS to ensure that its load capacity is not exceeded.

### 730010

**Error Message** `%ASA-7-730010: Group _groupname_ User _username,_ IP _ipaddr_ VLAN Mapping is enabled on VLAN _vlanid_.`

**Explanation** VLAN mapping is enabled in the session.

-   _groupname_ —The group name
-   _username_ —The username
-   _ipaddr_ —The IP address of this session
-   _vlanid_ —The VLAN ID that is used for the VLAN mapping session

**Recommended Action** None required.

### 731001

**Error Message** `%ASA-6-731001: NAC policy added: name: _policyname_ Type: _policytype_ .`

**Explanation** A new NAC-policy has been added to the ASA.

-   policyname—The NAC policy name
-   policytype—The type of NAC policy

**Recommended Action** None required.

### 731002

**Error Message** `%ASA-6-731002: NAC policy deleted: name: _policyname_ Type: _policytype_ .`

**Explanation** A NAC policy has been removed from the ASA.

-   policyname—The NAC policy name
-   policytype—The type of NAC policy

**Recommended Action** None required.

### 731003

**Error Message** `%ASA-6-731003: nac-policy unused: name: _policyname_ Type: _policytype_ .`

**Explanation** The NAC policy is unused because there is an existing NAC policy with the same name, but a different type.

-   policyname—The NAC policy name
-   policytype—The type of NAC policy

**Recommended Action** If the new NAC policy must be used, the existing NAC policy must be removed first. Otherwise, no action is required.

### 732001

**Error Message** `%ASA-6-732001: Group _groupname,_ User _username,_ IP _ipaddr,_ Fail to parse NAC-SETTINGS _nac-settings-id_ , terminating connection.`

**Explanation** The ASA cannot apply the NAC settings because no memory is available.

-   _groupname_ —The group name
-   _username_ —The username
-   _ipaddr_ —The IP address of this session
-   _nac-settings-id_ — The ID that is used for the NAC filter

**Recommended Action** Upgrade the ASA memory. Resolve any errors in the log before this problem occurs. If the problem persists, contact the Cisco TAC.

### 732002

**Error Message** `%ASA-6-732002: Group _groupname,_ User _username,_ IP _ipaddr,_ NAC-SETTINGS _settingsid_ from AAA ignored, existing NAC-SETTINGS _settingsid_inuse_ used instead.`

**Explanation** The NAC settings ID cannot be applied because there is a different one for the session.

-   _groupname_ —The group name
-   _username_ —The username
-   _ipaddr_ —The IP address of this session
-   _settingsid_ — The settings ID, which should be a NAC policy name
-   _settingsid\_inuse_ — The NAC settings ID that is currently in use

**Recommended Action** If the new NAC settings ID must be applied, then all the active sessions that use it must be torn down first. Otherwise, no action is required.

### 732003

**Error Message** `%ASA-6-732003: Group _groupname,_ User _username,_ IP _ipaddr,_ NAC-SETTINGS _nac-settings-id_ from AAA is invalid, terminating connection.`

**Explanation** The NAC settings received from AAA are invalid.

-   _groupname_ —The group name
-   _username_ —The username
-   _ipaddr_ —The IP address of this session
-   _nac-settings-id_ — The ID that is used for the NAC filter

**Recommended Action** Verify that the NAC settings configurations on the AAA server and ASA are both correct.

### 733100

**Error Message** `%ASA-4-733100: [_Object_] drop rate-_rate_ID_ exceeded. Current burst rate is _rate_val_ per second, max configured rate is _rate_val_; Current average rate is _rate_val_ per second, max configured rate is _rate_val_; Cumulative total count is _total_cnt_`

**Explanation** The specified object in the message has exceeded the specified burst threshold rate or average threshold rate. The object can be a drop activity of a host, TCP/UDP port, IP protocol, or various drops caused by potential attacks. The Secure Firewall ASA may be under attack.

-   _Object_ —The general or particular source of a drop rate count, which might include the following:

\- Firewall

\- Bad pkts

\- Rate limit

\- DoS attck

\- ACL drop

\- Conn limit

\- ICMP attk

\- Scanning

\- SYN attck

\- Inspect

\- Interface

(A citation of a particular interface object might take a number of forms. For example, you might see 80/HTTP, which would signify port 80, with the well-known protocol HTTP.)

-   _rate\_ID_ —The configured rate that is being exceeded. Most objects can be configured with up to three different rates for different intervals.
-   _rate\_val_ —A particular rate value.
-   _total\_cnt_ —The total count since the object was created or cleared.

The following three examples show how these variables occur:

-   For an interface drop caused by a CPU or bus limitation:

```python
%ASA-4-733100: [Interface] drop rate 1 exceeded. Current burst rate is 1 per second, max configured rate is 8000; Current average rate is 2030 per second, max configured rate is 2000; Cumulative total count is 3930654.”
```

-   For a scanning drop caused by potential attacks:

```csharp
%ASA-4-733100: [Scanning] drop rate-1 exceeded. Current burst rate is 10 per second_max configured rate is 10; Current average rate is 245 per second_max configured rate is 5; Cumulative total count is 147409 (35 instances received)
```

-   For bad packets caused by potential attacks:

```python
%ASA-4-733100: [Bad pkts] drop rate 1 exceeded. Current burst rate is 0 per second, max configured rate is 400; Current average rate is 760 per second, max configured rate is 100; Cumulative total count is 1938933
```

-   Because of the scanning rate configured and the threat-detection rate scanning-rate 3600 average-rate 15 command:

```python
%ASA-4-733100: [144.60.88.2] drop rate-2 exceeded. Current burst rate is 0 per second, max configured rate is 8; Current average rate is 5 per second, max configured rate is 4; Cumulative total count is 38086
```

Perform the following steps according to the specified object type that appears in the message:

1.  If the object in the message is one of the following:
    -   Firewall
    -   Bad pkts
    -   Rate limit
    -   DoS attck
    -   ACL drop
    -   Conn limit
    -   ICMP attck
    -   Scanning
    -   SYN attck
    -   Inspect
    -   Interface

**Recommended Action** Check whether the drop rate is acceptable for the running environment.

1.  Adjust the threshold rate of the particular drop to an appropriate value by using the threat-detection rate xxx command, where _xxx_ is one of the following:
    -   acl-drop
    -   bad-packet-drop
    -   conn-limit-drop
    -   dos-drop
    -   fw-drop
    -   icmp-drop
    -   inspect-drop
    -   interface-drop
    -   scanning-threat
    -   syn-attack
2.  If the object in the message is a TCP or UDP port, an IP address, or a host drop, check whether or not the drop rate is acceptable for the running environment.
3.  Adjust the threshold rate of the particular drop to an appropriate value by using the threat-detection rate bad-packet-drop command.

| ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)

**Note** | ___

If you do not want the drop rate exceed warning to appear, you can disable it by using the no threat-detection basic-threat command.

___ |
|--------|------------------------------------------------------------------------------------------------------------------------------------------|

### 733101

**Error Message** `%ASA-4-733101: _Object_objectIP_. Current burst rate is _rate_val_ per second, max configured rate is _rate_val_; Current average rate is _rate_val_ per second, max configured rate is _rate_val_; Cumulative total count is _total_cnt._`

**Explanation** The Secure Firewall ASA detected that a specific host (or several hosts in the same 1024-node subnet) is either scanning the network (attacking), or is being scanned (targeted).

-   _object_ —Attacker or target (a specific host or several hosts in the same 1024-node subnet)
-   _objectIP_ —The IP address of the scanning attacker or scanned target
-   _rate\_val_ —A particular rate value
-   _total\_cnt_ —The total count

The following two examples show how these variables occur:

```sql
%ASA-4-733101: Subnet 100.0.0.0 is targeted. Current burst rate is 200 per second, max configured rate is 0; Current average rate is 0 per second, max configured rate is 0; Cumulative total count is 2028.
%ASA-4-733101: Host 175.0.0.1 is attacking. Current burst rate is 200 per second, max configured rate is 0; Current average rate is 0 per second, max configured rate is 0; Cumulative total count is 2024
```

**Recommended Action** For the specific host or subnet, use the show threat-detection statistics host ip-address ip-mask command to check the overall situation and then adjust the threshold rate of the scanning threat to the appropriate value. After the appropriate value is determined, an optional action can be taken to shun those host attackers (not subnet attacker) by configuring the threat-detection scanning-threat shun-host command. You may specify certain hosts or object groups in the shun-host except list. For more information, see the CLI configuration guide. If scanning detection is not desirable, you can disable this feature by using the no threat-detection scanning command.

### 733102

**Error Message** `%ASA-4-733102: Threat-detection adds host _host_ to shun list`

**Explanation** A host has been shunned by the threat detection engine. When the threat-detection scanning-threat shun command is configured, the attacking hosts will be shunned by the threat detection engine.

-   _%I_ —A particular hostname

The following message shows how this command was implemented:

```csharp
%ASA-4-733102: Threat-detection add host 11.1.1.40 to shun list
```

**Recommended Action** To investigate whether the shunned host is an actual attacker, use the threat-detection statistics host ip-address command. If the shunned host is not an attacker, you can remove the shunned host from the threat detection engine by using the clear threat-detection shun ip address command. To remove all shunned hosts from the threat detection engine, use the clear shun command.

If you receive this message because an inappropriate threshold rate has been set to trigger the threat detection engine, then adjust the threshold rate by using the threat-detection rate scanning-threat rate-interval x average-rate y burst-rate z command.

### 733103

**Error Message** `%ASA-4-733103: Threat-detection removes host _host_ from shun list`

**Explanation** A host has been shunned by the threat detection engine. When you use the clear-threat-detection shun command, the specified host will be removed from the shunned list.

-   _%I_ —A particular hostname

The following message shows how this command is implemented:

```csharp
%ASA-4-733103: Threat-detection removes host 11.1.1.40 from shun list
```

**Recommended Action** None required.

### 733104

**Error Message** `%ASA-4-733104: TCP Intercept SYN flood attack detected to _host_ip_/_host_port_ (_real_ip_/_real_port_). Average rate of _avg_rate_ SYNs/sec exceeded the threshold of _threshold_rate_.`

**Explanation** The Secure Firewall ASA is under Syn flood attack and protected by the TCP intercept mechanism, if the average rate for intercepted attacks exceeds the configured threshold. The message is showing which server is under attack and where the attacks are coming from.

**Recommended Action** Write an ACL to filter out the attacks.

### 733105

**Error Message** `%ASA-4-733105: TCP Intercept SYN flood attack detected to _host_ip_/_host_port_ (_real_ip_/_real_port_). Burst rate of _burst_rate_ SYNs/sec exceeded the threshold of _threshold_rate_.`

**Explanation** The Secure Firewall ASA is under Syn flood attack and protected by the TCP intercept mechanism, if the burst rate for intercepted attacks exceeds the configured threshold. The message is showing which server is under attack and where the attacks are coming from.

**Recommended Action** Write an ACL to filter out the attacks.

### 733201

(For IKEv2 connection requests) **Error Message 1** `%ASA-4-733201: Threat-detection: Service[_remote-access-client-initiations_] Peer[_peer-ip_]: failure threshold of _threshold-value_ exceeded: adding shun to interface _interface_. _IKEv2:RA_excessive_client_initiation_requests_`

(For SSL connection requests) **Error Message 2** `%ASA-4-733201: Threat-detection: Service[remote-access-client-initiations] Peer[_peer_-_ip_]: failure threshold of _value_ exceeded: adding shun to interface _interface_. _SSL: RA excessive client initiation requests_.`

**Explanation** This message appears when the threat-detection service shunned an IP address due to excessive number of remote access client initiation requests to the headend from that host.

**Recommended Action** An IP address is shunned because it met the configured service threshold for mischievous activity. If this IP address should not be blocked, remove the shun manually using the shun CLI

.

### 734001

**Error Message** `%ASA-6-734001: DAP: User _user_, Addr _ipaddr_, Connection _connection_: The following DAP records were selected for this connection: _string_`

**Explanation** The DAP records that were selected for the connection are listed.

-   _user_ —The authenticated username
-   _ipaddr_ —The IP address of the remote client
-   _connection_ —The type of client connection, which can be one of the following:

\- IPsec

\- AnyConnect

\- Clientless (web browser)

\- Cut-Through-Proxy

\- L2TP

-   _DAP record names_ —The comma-separated list of the DAP record names

**Recommended Action** None required.

### 734002

**Error Message** `%ASA-5-734002: DAP: User _user_, Addr _ipaddr_: Connection terminated by the following DAP records: _string_`

**Explanation** The DAP records that terminated the connection are listed.

-   _user_ —The authenticated username
-   _ipaddr_ —The IP address of the remote client
-   _DAP record names_ —The comma-separated list of the DAP record names

**Recommended Action** None required.

### 734003

**Error Message** `%ASA-7-734003: DAP: User _name_, Addr _ipaddr_: Session Attribute _attr_name/value_`

**Explanation** The AAA and endpoint session attributes that are associated with the connection are listed.

-   _user_ —The authenticated username
-   _ipaddr_ —The IP address of the remote client
-   _attr/value_ —The AAA or endpoint attribute name and value

**Recommended Action** None required.

### 734004

**Error Message** `%ASA-3-734004: DAP: Processing error: Code _internal_`

**Explanation** A DAP processing error occurred.

-   _internal error code_ —The internal error string

**Recommended Action** Enable the debug dap errors command and re-run DAP processing for further debugging information. If this does not resolve the issue, contact the Cisco TAC and provide the internal error code and any information about the conditions that generated the error.

### 735001

**Error Message** `%ASA-1-735001: Cooling Fan _var1_: OK`

**Explanation** A cooling fan has been restored to normal operation.

-   _var1_ —The device number markings

**Recommended Action** None required.

### 735002

**Error Message** `%ASA-1-735002: Cooling Fan _var1_: Failure Detected`

**Explanation** A cooling fan has failed.

-   _var1_ —The device number markings

**Recommended Action** Perform the following steps:

1.  Check for obstructions that would prevent the fan from rotating.
2.  Replace the cooling fan.
3.  If the problem persists, record the message as it appears and contact the Cisco TAC.

### 735003

**Error Message** `%ASA-1-735003: Power Supply _var1_: OK`

**Explanation** A power supply has been restored to normal operation.

-   _var1_ —The device number markings

**Recommended Action** None required.

### 735004

**Error Message** `%ASA-1-735004: Power Supply _var1_: Failure Detected`

**Explanation** AC power has been lost, or the power supply has failed.

-   _var1_ —The device number markings

**Recommended Action** Perform the following steps:

1.  Check for AC power failure.
2.  Replace the power supply.
3.  If the problem persists, record the message as it appears and contact the Cisco TAC.

### 735005

**Error Message** `%ASA-1-735005: Power Supply Unit Redundancy OK`

**Explanation** Power supply unit redundancy has been restored.

**Recommended Action** None required.

### 735006

**Error Message** `%ASA-1-735006: Power Supply Unit Redundancy Lost`

**Explanation** A power supply failure occurred. Power supply unit redundancy has been lost, but the Secure Firewall ASA is functioning normally with minimum resources. Any further failures will result in an Secure Firewall ASA shutdown.

**Recommended Action** To regain full redundancy, perform the following steps:

1.  Check for AC power failure.
2.  Replace the power supply.
3.  If the problem persists, record the message as it appears and contact the Cisco TAC.

### 735007

**Error Message** `%ASA-1-735007: CPU _var1_: Temp: _var2_ _var3_, Critical`

**Explanation** The CPU has reached a critical temperature.

-   _var1_ —The device number markings
-   _var2_ —The temperature value
-   _var3_ —Temperature value units (C, F)

**Recommended Action** Record the message as it appears and contact the Cisco TAC.

### 735008

**Error Message** `%ASA-1-735008: Chassis Ambient _var1_: Temp: _var2_ _var3_, Critical`

**Explanation** A chassis ambient temperature sensor has reached a critical level.

-   _var1_ —The device number markings
-   _var2_ —The temperature value
-   _var3_ —Temperature value units (C, F)

**Recommended Action** Record the message as it appears and contact the Cisco TAC.

### 735009

**Error Message** `%ASA-2-735009: Environment Monitoring has failed initialization and configuration. Environment Monitoring is not running.`

**Explanation** Environment monitoring has experienced a fatal error during initialization and was unable to continue.

**Recommended Action** Collect the output of the show environment and debug ipmi commands. Record the message as it appears and contact the Cisco TAC.

### 735010

**Error Message** `%ASA-3-735010: Environment Monitoring has failed to update one or more of its records.`

**Explanation** Environment monitoring has experienced an error that temporarily prevented it from updating one or more of its records.

**Recommended Action** If this message appears repeatedly, collect the output from the show environment driver and debug ipmi commands. Record the message as it appears and contact the Cisco TAC.

### 735011

**Error Message** `%ASA-1-735011: Power Supply _var1_: Fan OK`

**Explanation** The power supply fan has returned to a working operating state.

-   _var1_ — Fan number

**Recommended Action** None required.

### 735012

**Error Message** `%ASA-1-735012: Power Supply _var1_: Fan Failure Detected`

**Explanation** The power supply fan has failed.

-   _var1_ — Fan number

**Recommended Action** Contact Cisco TAC to troubleshoot the failure. Power down the unit until this failure is resolved.

### 735013

**Error Message** `%ASA-1-735013: Voltage Channel _var1_: Voltage OK`

**Explanation** A voltage channel has returned to a normal operating level.

-   _var1_ — Voltage channel number

**Recommended Action** None required.

### 735014

**Error Message** `%ASA-1-735014: Voltage Channel _var1_: Voltage Critical`

**Explanation** A voltage channel has changed to a critical level.

-   _var1_ — Voltage channel number

**Recommended Action** Contact Cisco TAC to troubleshoot the failure. Power down the unit until this failure is resolved.

### 735015

**Error Message** `%ASA-4-735015: CPU _var1_: Temp: _var2_ _var3_, Warm`

**Explanation** The CPU temperature is warmer than the normal operating range.

-   _var1_ —CPU Number
-   _var2_ —Temperature Value
-   _var3_ —Units

**Recommended Action** Continue to monitor this component to ensure that it does not reach a critical temperature.

### 735016

**Error Message** `%ASA-4-735016: Chassis Ambient _var1_: Temp: _var2_ _var3_, Warm`

**Explanation** The chassis temperature is warmer than the normal operating range.

-   _var1_ —Chassis Sensor Number
-   _var2_ —Temperature Value
-   _var3_ —Units

**Recommended Action** Continue to monitor this component to ensure that it does not reach a critical temperature.

### 735017

**Error Message** `%ASA-1-735017: Power Supply _var1_: Temp: _var2_ _var3_, OK`

**Explanation** The power supply temperature has returned to a normal operating temperature.

-   _var1_ —Power Supply Number
-   _var2_ —Temperature Value
-   _var3_ —Units

**Recommended Action** None required.

### 735018

**Error Message** `%ASA-4-735018: Power Supply _var1_: Temp: _var2_ _var3_, Critical`

**Explanation** The power supply has reached a critical operating temperature.

-   _var1_ —Power Supply Number
-   _var2_ —Temperature Value
-   _var3_ —Units

**Recommended Action** Contact Cisco TAC to troubleshoot the failure. Power down the unit until this failure is resolved.

### 735019

**Error Message** `%ASA-4-735019: Power Supply _var1_: Temp: _var2_ _var3_, Warm`

**Explanation** The power supply temperature is warmer than the normal operating range.

-   _var1_ —Power Supply Number
-   _var2_ —Temperature Value
-   _var3_ —Units

**Recommended Action** Continue to monitor this component to ensure that it does not reach a critical temperature.

### 735020

**Error Message** `%ASA-1-735020: CPU _var1_: Temp: _var2_ _var3_, OK`

**Explanation** The CPU temperature has returned to the normal operating temperature.

-   _var1_ —CPU Number
-   _var2_ —Temperature Value
-   _var3_ —Units

**Recommended Action** None required.

### 735021

**Error Message** `%ASA-1-735021: Chassis Ambient _var1_: Temp: _var2_ _var3_, OK`

**Explanation** The chassis temperature has returned to the normal operating temperature.

-   _var1_ —Chassis Sensor Number
-   _var2_ —Temperature Value
-   _var3_ —Units

**Recommended Action** None required.

### 735022

**Error Message** `%ASA-1-735022: CPU_num_ is running beyond the max thermal operating temperature and the device will be shutting down immediately to prevent permanent damage to the CPU`

**Explanation** The Secure Firewall ASA has detected a CPU running beyond the maximum thermal operating temperature, and will shut down immediately after detection.

**Recommended Action** The chassis and CPU need to be inspected immediately for ventilation issues.

### 735023

**Error Message** `%ASA-2-735023: _device_ was previously shutdown due to the CPU complex running beyond the max thermal operating temperature. The chassis needs to be inspected immediately for ventilation issues`

**Explanation** At boot time, the Secure Firewall ASA detected a shutdown that occurred because a CPU was running beyond the maximum safe operating temperature. Using the show environment command will indicate that this event has occurred.

**Recommended Action** The chassis need to be inspected immediately for ventilation issues.

### 735024

**Error Message** `%ASA-1-735024: CPU_var1_ Voltage Regulator is running beyond the max thermal operating temperature and the device will be shutting down immediately. The chassis and CPU need to be inspected immediately for ventilation issues`

**Explanation** The IO hub temperature has returned to the normal operating temperature.

-   _ar1_ - IO hub number
-   _var2_ - Temperature value
-   _var3_ – Units

**Recommended Action** None required.

### 735025

**Error Message** `%ASA-1-735025: _var1_ was previously shutdown due to a CPU Voltage Regulator running beyond the max thermal operating temperature. The chassis and CPU need to be inspected immediately for ventilation issues`

**Explanation** The IO hub temperature has a critical temperature.

-   _ar1_ - IO hub number
-   _var2_ - Temperature value
-   _var3_ – Units

**Recommended Action** Record the message as it appears and contact the Cisco TAC.

### 735026

**Error Message** `%ASA-4-735026: IO Hub _var1_: Temp: _var2_ _var3_, OK`

**Explanation** The IO hub temperature is warmer than the normal operating range.

-   _ar1_ - IO hub number
-   _var2_ - Temperature value
-   _var3_ – Units

**Recommended Action** Continue to monitor this component to ensure that it does not reach a critical temperature.

### 735027

**Error Message** `%ASA-1-735027: CPU _cpu_num_ Voltage Regulator is running beyond the max thermal operating temperature and the device will be shutting down immediately. The chassis and CPU need to be inspected immediately for ventilation issues.`

**Explanation** The Secure Firewall ASA has detected a CPU voltage regulator running beyond the maximum thermal operating temperature, and shuts down immediately after detection.

-   _cpu\_num_ —The number to identify which CPU voltage regulator experienced the thermal event

**Recommended Action** The chassis and CPU need to be inspected immediately for ventilation issues.

### 735028

**Error Message** `%ASA-2-735028: ASA was previously shutdown due to a CPU Voltage Regulator running beyond the max thermal operating temperature. The chassis and CPU need to be inspected immediately for ventilation issues.`

**Explanation** At boot time, the Secure Firewall ASA detected a shutdown that occurred because of a CPU voltage regulator running beyond the maximum safe operating temperature. Enter the show environment command to indicate that this event has occurred.

**Recommended Action** The chassis and CPU need to be inspected immediately for ventilation issues.

### 735029

**Error Message** `%ASA-1-735029: IO Hub is running beyond the max thermal operating temperature and the device will be shutting down immediately to prevent permanent damage to the circuit`

**Explanation** The Secure Firewall ASA has detected that the IO hub is running beyond the maximum thermal operating temperature, and will shut down immediately after detection.

**Recommended Action** The chassis and IO hub need to be inspected immediately for ventilation issues.

### 736001

**Error Message** `%ASA-2-736001: Unable to allocate enough memory at boot for jumbo-frame reservation. Jumbo-frame support has been disabled.`

**Explanation** Insufficient memory has been detected when jumbo frame support was being configured. As a result, jumbo-frame support was disabled.

**Recommended Action** Try reenabling jumbo frame support using the jumbo-frame reservation command. Save the running configuration and reboot the Secure Firewall ASA. If the problem persists, contact the Cisco TAC.

## Messages 737001 to 776254

This section includes messages from 737001 to 776254.

### 737001

**Error Message** `%ASA-7-737001: IPAA: Session=_session_, Received message '_message-type_'`

**Explanation** The IP address assignment process received a message.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _message-type_ —The message received by the IP address assignment process

**Recommended Action** None required.

### 737002

**Error Message** `%ASA-3-737002: IPAA: Session=_session_, Received unknown message '_num_'`

**Explanation** The IP address assignment process received a message.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _num_ —The identifier of the message received by the IP address assignment process

**Recommended Action** None required.

### 737003

**Error Message** `%ASA-5-737003: IPAA: Session=_session_, DHCP configured, no viable servers found for tunnel-group '_tunnel-group_'`

**Explanation** The DHCP server configuration for the given tunnel group is not valid.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _tunnel-group_ —The tunnel group that IP address assignment is using for configuration

**Recommended Action** Validate the DHCP configuration for the tunnel group. Make sure that the DHCP server is online.

### 737004

**Error Message** `%ASA-5-737004: IPAA: Session=_session_, DHCP configured, request failed for tunnel-group '_'tunnel-group'_'`

**Explanation** The DHCP server configuration for the given tunnel group is not valid.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _tunnel-group_ —The tunnel group that IP address assignment is using for configuration

**Recommended Action** Validate the DHCP configuration for the tunnel group. Make sure that the DHCP server is online.

### 737005

**Error Message** `%ASA-6-737005: IPAA: Session=_session_, DHCP configured, request succeeded for tunnel-group '_tunnel-group_'`

**Explanation** The DHCP server request has succeeded.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _tunnel-group_ —The tunnel group that IP address assignment is using for configuration

**Recommended Action** None required.

### 737006

**Error Message** `%ASA-6-737006: IPAA: Session=_session_, Local pool request succeeded for tunnel-group '_tunnel-group_'`

**Explanation** The local pool request has succeeded.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _tunnel-group_ —The tunnel group that IP address assignment is using for configuration

**Recommended Action** None required.

### 737007

**Error Message** `%ASA-5-737007: IPAA: Session=_session_, Local pool request failed for tunnel-group '_tunnel-group_'`

**Explanation** The local pool request has failed. The pool assigned to the tunnel group may be exhausted.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _tunnel-group_ —The tunnel group that IP address assignment is using for configuration

**Recommended Action** Validate the IP local pool configuration by using the show ip local pool command.

### 737008

**Error Message** `%ASA-5-737008: IPAA: Session=_session_, tunnel-group '_'tunnel-group'_' not found`

**Explanation** The tunnel group was not found when trying to acquire an IP address for configuration. A software defect may cause this message to be generated.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _tunnel-group_ —The tunnel group that IP address assignment is using for configuration

**Recommended Action** Check the tunnel group configuration. Contact the Cisco TAC and report the issue.

### 737009

**Error Message** `%ASA-6-737009: IPAA: Session=_session_, AAA assigned address _ip-address_, request failed`

**Explanation** The remote access client software requested the use of a particular address. The request to the AAA server to use this address failed. The address may be in use.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _ip-address_ —The IPv4 or IPv6 address that the client requested

**Recommended Action** Check the AAA server status and the status of IP local pools.

### 737010

**Error Message** `%ASA-6-737010: IPAA: Session=_session_, AAA assigned address _ip-address_, succeeded`

**Explanation** The remote access client software requested the use of a particular address and successfully received this address.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _ip-address_ —The IPv4 or IPv6 address that the client requested

**Recommended Action** None required.

### 737011

**Error Message** `%ASA-5-737011: IPAA: Session=_session_, AAA assigned address _ip-address_, not permitted, retrying`

**Explanation** The remote access client software requested the use of a particular address. The vpn-addr-assign aaa command is not configured. An alternatively configured address assignment method will be used.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _ip-address_ —The IPv4 or IPv6 address that the client requested

**Recommended Action** If you want to permit clients to specify their own address, enable the vpn-addr-assign aaa command.

### 737012

**Error Message** `%ASA-4-737012: IPAA: Session=_session_, Address assignment failed`

**Explanation** The remote access client software request of a particular address failed.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _ip-address_ —The IP address that the client requested

**Recommended Action** If using IP local pools, validate the local pool configuration. If using AAA, validate the configuration and status of the AAA server. If using DHCP, validate the configuration and status of the DHCP server. Increase the logging level (use notification or informational) to obtain additional messages to identify the reason for the failure.

### 737013

**Error Message** `%ASA-4-737013: IPAA: Session=_session_, Error freeing address _ip-address_, not found`

**Explanation** The Secure Firewall ASA tried to free an address, but it was not on the allocated list because of a recent configuration change.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _ip-address_ —The IPv4 or IPv6 address to be released

**Recommended Action** Validate your address assignment configuration. If this message recurs, it might be due to a software defect. Contact the Cisco TAC and report the issue.

### 737014

**Error Message** `%ASA-6-737014: IPAA: Session=_session_, Freeing AAA address _ip-address_`

**Explanation** The Secure Firewall ASA successfully released the IP address assigned through AAA.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _ip-address_ —The IPv4 or IPv6 address to be released

**Recommended Action** None required.

### 737015

**Error Message** `%ASA-6-737015: IPAA: Session=_session_, Freeing DHCP address _ip-address_`

**Explanation** The Secure Firewall ASA successfully released the IP address assigned through DHCP.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _ip-address_ —The IP address to be released

**Recommended Action** None required.

### 737016

**Error Message** `%ASA-6-737016: IPAA: Session=_session_, Freeing local pool _pool-name_ address _ip-address_`

**Explanation** The Secure Firewall ASA successfully released the IP address assigned through local pools.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _ip-address_ —The IPv4 or IPv6 address to be released
-   _pool-name_ —The pool to which the address is being returned to

**Recommended Action** None required.

### 737017

**Error Message** `%ASA-6-737017: IPAA: Session=_session_, DHCP request attempt _num_ succeeded`

**Explanation** The Secure Firewall ASA successfully sent a request to a DHCP server.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _num_ —The attempt number

**Recommended Action** None required.

### 737018

**Error Message** `%ASA-5-737018: IPAA: Session=_session_, DHCP request attempt _num_ failed`

**Explanation** The Secure Firewall ASA failed to send a request to a DHCP server.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _num_ —The attempt number

**Recommended Action** Validate the DHCP configuration and connectivity to the DHCP server.

### 737019

**Error Message** `%ASA-4-737019: IPAA: Session=_session_, Unable to get address from group-policy or tunnel-group local pools`

**Explanation** The Secure Firewall ASA failed to acquire an address from the local pools configured on the group policy or tunnel group. The local pools may be exhausted.

-   _session_ —The session is the VPN session ID in hexadecimal.
    

**Recommended Action** Validate the local pool configuration and status. Validate the group policy and tunnel group configuration of local pools.

### 737023

**Error Message** `%ASA-5-737023: IPAA: Session=_session_, Unable to allocate memory to store local pool address _ip-address_`

**Explanation** The Secure Firewall ASA is low on memory.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _ip-address_ —The IP address that was acquired

**Recommended Action** The Secure Firewall ASA may be overloaded and need more memory, or there may be a memory leak caused by a software defect. Contact the Cisco TAC and report the issue.

### 737024

**Error Message** `%ASA-5-737024: IPAA: Session= , Client requested address _:_ , already in use, retrying`

**Explanation** The client requested an IP address that is already in use. The request will be tried using a new IP address.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _ip-address_ —The IP address that the client requested

**Recommended Action** None required.

### 737025

**Error Message** `%ASA-5-737025: IPAA:Session=_session_, Duplicate local pool address found, {_ip-address|(ipv6-address)_} in quarantine`

**Explanation** The IP address that was to be given to the client is already in use. The IP address has been removed from the pool and will not be reused.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _ip-address_ —The IP address that was acquired

**Recommended Action** Validate the local pool configuration; there may be an overlap caused by a software defect. Contact the Cisco TAC and report the issue.

### 737026

**Error Message** `%ASA-6-737026: IPAA: Session= , Client assigned _session_ from local pool _ip-address_`

**Explanation** The client has assigned the given address from a local pool.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _ip-address_ —The IP address that was assigned to the client
-   _pool-name_—The pool from which the address was allocated
    

**Recommended Action** None required.

### 737027

**Error Message** `%ASA-3-737027: IPAA: Session= , No data for address request`

**Explanation** A software defect has been found.

-   _session_ —The session is the VPN session ID in hexadecimal.
    

**Recommended Action** Contact the Cisco TAC and report the issue.

### 737028

**Error Message** `%ASA-4-737028: IPAA: Session= , Unable to send _session_ to standby: communication failure`

**Explanation** The active Secure Firewall ASA was unable to communicate with the standby Secure Firewall ASA. The failover pair may be out-of-sync.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _ip-address_ —The IP address that was assigned to the client

**Recommended Action** Validate the failover configuration and status.

### 737029

**Error Message** `%ASA-6-737029: IPAA: Session=_session_, Added {_ip_address | ipv6_address_} to standby`

**Explanation** The standby Secure Firewall ASA accepted the IP address assignment.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _ip\_address_ —The IP address that was assigned to the client

**Recommended Action** None required.

### 737030

**Error Message** `%ASA-4-737030: IPAA: Session=_session_, Unable to send {_ip_address | ipv6_address_} to standby: address in use`

**Explanation** The standby Secure Firewall ASA has the given address already in use when the active Secure Firewall ASA attempted to acquire it. The failover pair may be out-of-sync.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _ip-address_ —The IP address (IPv4 or IPv6) that was assigned to the client.

**Recommended Action** Validate the failover configuration and status.

### 737031

**Error Message** `%ASA-6-737031: IPAA: Session= , Removed _session_ from standby`

**Explanation** The standby Secure Firewall ASA cleared the IP address assignment.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _ip-address_ —The IP address that was assigned to the client

**Recommended Action** None required.

### 737032

**Error Message** `%ASA-4-737032: IPAA: Session= , Unable to remove _session_ from standby: address not found`

**Explanation** The standby Secure Firewall ASA did not have an IP address in use when the active Secure Firewall ASA attempted to release it. The failover pair may be out-of-sync.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _ip-address_ —The IP address that was assigned to the client

**Recommended Action** Validate the failover configuration and status.

### 737033

**Error Message** `%ASA-4-737033: IPAA: Session=_session_ , Unable to assign _session_ provided IP address (_addr_allocator_) to Client. This IP address has already been assigned by _ip_addr_`

**Explanation** The address assigned by the AAA/DHCP/local pool is already in use.

-   _session_ —The session is the VPN session ID in hexadecimal.
    
-   _addr\_allocator_ —The DHCP/AAA/local pool
-   _ip\_addr_ —The IP address allocated by the DHCP/AAA/local pool
-   _previous\_ addr\_allocator_ —The address allocater that already assigned the IP address (local pool, AAA, or DHCP)

**Recommended Action** Validate the AAA/DHCP/local pool address configurations. Overlap may occur.

### 737034

**Error Message 1**`%ASA-4-737030: IPAA:Session=_session_, IPv4 address: _ip-address_`

**Error Message 2**`%ASA-4-737030: IPAA:Session=_session_, IPv6 address: _ipv6-address_`

**Explanation** The IP address assignment process is unable to provide an address.

-   _session_ —The session is the VPN session ID in hexadecimal.
    

**Recommended Action** Action will be based on explanation for the failure.

### 737035

**Error Message** `%ASA-7-737035: IPAA: Session=_session_, '_'message_type'_' message queued`

**Explanation** A message is queued to the IP address assignment. This corresponds with syslog 737001. This message is not rate limited.

-   _session_ —The session is the VPN session ID in hexadecimal.
    

**Recommended Action** No action required.

### 737036

**Error Message** `%ASA-6-737035: IPAA: Session=_session_, '_<address>_' message queued`

**Explanation** IP address assignment process has provided a DHCP provisioned address back to the VPN client. This message is not rate limited.

-   _session_ —The session is the VPN session ID in hexadecimal.
    

**Recommended Action** No action required.

### 737038

**Error Message** `%ASA7-737038: IPAA: Session=_session_, specified address _ip_address_ was in-use, trying to get another.`

**Explanation** This log occurs when the AAA server (internal or external) has specified an address to assign to the user; but this address already in-use. The request is being re-queued without a specified address to fall back to DHCP or local pools.

-   _session_ —The VPN session ID of the requesting session.
    
-   _ip-address_ —The IPv4 or IPv6 address specified by AAA

**Recommended Action** None required

### 737200

**Error Message** `%ASA-7-737200: VPNFIP: Pool=_pool_, Allocated _ip-address_ from pool`

**Explanation** This log occurs an address is allocated from a local pool.

-   _pool_ —The local pool name.
    
-   _ip-address_ —The IPv4 or IPv6 address specified by AAA

**Recommended Action** None required

### 737201

**Error Message** `%ASA-7-737201: VPNFIP: Pool=_pool_, Returned _ip-address_ to pool (recycle=_recycle_)`

**Explanation** This log occurs when an address returned to a local pool. The recycle flag indicates whether this address should be re-used for the next request. For rare situation, the recycle flag will be FALSE. For example, when there is an address collision , the address has been assigned to a VPN session by other means such as by AAA or DHCP. In this case, we will not immediately try to reuse that address for the next request.

-   _pool_ —The local pool name.
    
-   _ip-address_ —The IPv4 or IPv6 address specified by AAA

**Recommended Action** None required

### 737202

**Error Message** `%ASA-3-737202: VPNFIP: Pool=_pool_, ERROR: _message_`

**Explanation** This log is generated when an error event is detected related to the VPN FIP database.

-   _pool_ —The local pool name.
    
-   _message_ —The details for the event.

**Recommended Action** If error is persistent, contact Cisco TAC.

### 737203

**Error Message** `%ASA-4-737203: VPNFIP: Pool=_pool_, WARN: _message_`

**Explanation** This log is generated to warn of an event related to the VPN FIP database.

-   _pool_ —The local pool name.
    
-   _message_ —The details for the event.
    

**Recommended Action** If warning is persistent, contact Cisco TAC.

### 737204

**Error Message** `%ASA-5-737204: VPNFIP: Pool=_pool_, NOTIFY: _message_`

**Explanation** This log is generated to notify of an event related to the VPN FIP database.

-   _pool_ —The local pool name.
    
-   _message_ —The details for the event.
    

**Recommended Action** None required

### 737205

**Error Message** `%ASA-6-737205: VPNFIP: Pool=_pool_, INFO: _message_`

**Explanation** This log is generated to inform of an event related to the VPN FIP database.

-   _pool_ —The local pool name.
    
-   _message_ —The details for the event.
    

**Recommended Action** None required

### 737206

**Error Message** `%ASA-7-737206: VPNFIP: Pool=_pool_, DEBUG: _message_`

**Explanation** This log is generated to debug an event related to the VPN FIP database.

-   _pool_ —The local pool name.
    
-   _message_ —The details for the event.
    

**Recommended Action** None required

### 737400

**Error Message** `%ASA-7-737400: POOLIP: Pool=_pool_, Allocated _ip-address_ from pool`

**Explanation** This log occurs an address is allocated from a local pool.

-   _pool_ —The local pool name
    
-   _ip-address_ —The IPv4 or IPv6 address specified by AAA

**Recommended Action** None required

### 737401

**Error Message** `%ASA-7-737401: POOLIP: Pool=_pool_, Returned _ip-address_ to pool (recycle=_recycle_)`

**Explanation** This log occurs an address returned to a local pool. The recycle flag indicates whether this address should be re-used for the next request. For rare situation, the recycle flag will be FALSE. For example, when there is an address collision—the address has been assigned to a VPN session by other means such as by AAA or DHCP. In this case, we will not immediately try to reuse that address for the next request.

-   _pool_ —The local pool name
    
-   _ip-address_ —The IPv4 or IPv6 address specified by AAA

**Recommended Action** None required

### 737402

**Error Message** `%ASA-4-737402: POOLIP: Pool=_pool_, Failed to return _ip-address_ to pool (recycle=_recycle_). Reason: _message_`

**Explanation** This log occurs unable to return an address to an address pool.

-   _pool_ —The local pool name
    
-   _ip-address_ —The IPv4 or IPv6 address specified by AAA
-   _message_—The details of the failure. (For example, address not in pool range)
    

**Recommended Action** None required

### 737403

**Error Message** `%ASA-3-737403: POOLIP: Pool=_pool_, ERROR: _message_`

**Explanation** This log is generated when an error event is detected related to an IP local pool database.

-   _pool_ —The local pool name
    
-   _message_ —The details for the event.
    

**Recommended Action** If error is persistent, contact Cisco TAC.

### 737404

**Error Message** `%ASA-4-737404: POOLIP: Pool=_pool_, WARN: _message_`

**Explanation** This log is generated to warn of an event related to an IP local pool database.

-   _pool_ —The local pool name
    
-   _message_ —The details for the event.
    

**Recommended Action** If warning is persistent, contact Cisco TAC.

### 737405

**Error Message** `%ASA-5-737405: POOLIP: Pool=_pool_, NOTIFY: _message_`

**Explanation** This log is generated to notify of an event related to an IP local pool database.

-   _pool_ —The local pool name
    
-   _message_ —The details for the event.
    

**Recommended Action** None required

### 737406

**Error Message** `%ASA-6-737406: POOLIP: Pool=_pool_, INFO: _message_`

**Explanation** This log is generated to inform of an event related to an IP local pool database.

-   _pool_ —The local pool name
    
-   _message_ —The details for the event.
    

**Recommended Action** None required

### 737407

**Error Message** `%ASA-7-737407: POOLIP: Pool=_pool_, DEBUG: _message_`

**Explanation** This log is generated to debug an event related to an IP local pool database.

-   _pool_ —The local pool name
    
-   _message_ —The details for the event.
    

**Recommended Action** None required

### 741000

**Error Message** `%ASA-6-741000: Coredump filesystem image created on _variable_1_ - size _variable_2_ MB`

**Explanation** A core dump file system was successfully created. The file system is used to manage core dumps by capping the amount of disk space that core dumps may use.

-   _variable 1_ —The file system on which the core dumps are placed (for example, disk0:, disk1:, and flash:)
-   _variable 2_ —The size of the created core dump file system in MB

**Recommended Action** Make sure that you save your configuration after creating the core dump file system.

### 741001

**Error Message** `%ASA-6-741001: Coredump filesystem image on _variable_ - resized from _variable_ MB to _variable_ MB`

**Explanation** The core dump file system has been successfully resized.

-   _variable 1_ —The file system on which the core dumps are placed
-   _variable 2_ —The size of the previous core dump file system in MB
-   _variable 3_ —The size of the current, newly resized core dump file system in MB

**Recommended Action** Make sure that you save your configuration after resizing the core dump file system. Resizing the core dump file system deletes the contents of the existing core dump file system. As a result, make sure that you archive any information before you resize the core dump file system.

### 741002

**Error Message** `%ASA-6-741002: Coredump log and filesystem contents cleared on _variable_1_`

**Explanation** All core dumps have been deleted from the core dump file system, and the core dump log has been cleared. The core dump file system and coredump log are always synchronized with each other.

-   _variable 1_ —The file system on which the core dumps are placed (for example, disk0:, disk1:,and flash:)

**Recommended Action** None required. You can clear the core dump file system to reset it to a known state using the clear coredump command.

### 741003

**Error Message** `%ASA-6-741003: Coredump filesystem and it's contents removed on _variable_1_`

**Explanation** The core dump file system and its contents have been removed, and the core dump feature has been disabled.

-   _variable 1_ —The file system on which the core dumps are placed (for example, disk0:, disk1:,and flash:)

**Recommended Action** Make sure that you save your configuration after the core dump feature has been disabled.

### 741004

**Error Message** `%ASA-6-741004: Coredump configuration reset to default values`

**Explanation** The core dump configuration has been reset to its default value, which is disabled.

**Recommended Action** Make sure that you save your configuration after the core dump feature has been disabled.

### 741005

**Error Message** `%ASA-4-741005: Coredump operation '_variable_1_' failed with error _variable_2_variable_3_`

**Explanation** An error occurred during the performance of a core dump-related operation.

-   _variable 1_ —This variable may have the following values:

\- CREATE\_FSYS—An error occurred when creating the core dump file system.

\- CLEAR\_LOG—An error occurred when clearing the core dump log.

\- DELETE\_FSYS—An error occurred when deleting the core dump file system.

\- CLEAR\_FSYS—An error occurred when removing the contents of the core dump file system.

\- MOUNT\_FSYS—An error occurred when mounting the core dump file system.

-   _variable 2_ —The decimal number that provides additional information about the cause of the error specified in _variable 1_ .
-   _variable 3_ —The descriptive ASCII string associated with _variable 2._ The ASCII string can have the following values:

\- coredump files already exist

\- unable to create coredump filesystem

\- unable to create loopback device

\- filesystem type not supported

\- unable to delete the coredump filesystem

\- unable to delete loopback device

\- unable to unmount coredump filesystem

\- unable to mount coredump filesystem

\- unable to mount loopback device

\- unable to clear coredump filesystem

\- coredump filesystem not found

\- requested coredump filesystem too big

\- coredump operation aborted by administrator

\- coredump command execution failed

\- coredump IFS error encountered

\- coredump, unidentified error encountered

**Recommended Action** Make sure that the core dump feature is disabled in the configuration, and send the message to the Cisco TAC for further analysis.

### 741006

**Error Message** `%ASA-4-741006: Unable to write Coredump Helper configuration, reason _variable_1_`

**Explanation** An error occurred when writing to the coredump helper configuration file. This error occurs only if disk0: is full. The configuration file is located in disk0:.coredumpinfo/coredump.cfg.

-   _variable 1_ —This variable includes a basic file system-related string that indicates why the writing of the core dump helper configuration file failed.

**Recommended Action** Disable the core dump feature, remove unneeded items from disk0:, and then reenable core dumps, if desired.

### 742001

**Error Message** `%ASA-3-742001: failed to read master key for password encryption from persistent store`

**Explanation** An attempt to read the primary password encryption key from the nonvolatile memory after bootup failed. Encrypted passwords in the configuration are not decrypted unless the primary key is set to the correct value using the key config-key password encryption command.

**Recommended Action** If there are encrypted passwords in the configuration that must be used, set the primary key to the previous value used to encrypt the password using the key config-key password encryption command. If there are no encrypted passwords or they can be discarded, set a new primary key. If password encryption is not used, no action is required.

### 742002

**Error Message** `%ASA-3-742002: failed to set master key for password encryption`

**Explanation** An attempt to read the key config-key password encryption command failed. The error may be caused by the following reasons:

-   Configuration from a nonsecure terminal (for example, over a Telnet connection) was made.
-   Failover is enabled, but it does not use an encrypted link.
-   Another user is setting the key at the same time.
-   When trying to change the key, the old key is incorrect.
-   The key is too small to be secure.

Other reasons for the error may be valid. In these cases, the actual error is printed in response to the command.

**Recommended Action** Correct the problem indicated in the command response.

### 742003

**Error Message** `%ASA-3-742003: failed to save master key for password encryption, reason=_reason_text_`

**Explanation** An attempt to save the primary key to nonvolatile memory failed. The actual reason is specified by the _reason\_text_ parameter. The reason can be an out-of-memory condition, or the nonvolatile store can be inconsistent.

**Recommended Action** If the problem persists, reformat the nonvolatile store that is used to save the key by using the write erase command. Before performing this step, make sure that you back up the out-of-the-box configuration. Then reenter the write erase command.

### 742004

**Error Message** `%ASA-3-742004: failed to sync master key for password encryption, reason=_reason_text_`

**Explanation** An attempt to synchronize the primary key to the peer failed. The actual reason is specified by the _reason\_text_ parameter.

**Recommended Action** Try to correct the problem specified in the _reason\_text_ parameter.

### 742005

**Error Message** `%ASA-3-742005: cipher text _enc_pass_ is not compatible with the configured master key or the cipher text has been tampered`

**Explanation** An attempt to decrypt a password failed. The password may have been encrypted using a primary key that is different from the current primary key, or the encrypted password has been changed from its original form.

**Recommended Action** If the correct primary key is not being used, correct the problem. If the encrypted password has been modified, reapply the configuration in question with a new password.

### 742006

**Error Message** `%ASA-3-742006: password decryption failed due to unavailable memory`

**Explanation** An attempt to decrypt a password failed because no memory was available. Features using this password will not work as desired.

**Recommended Action** Correct the memory problem.

### 742007

**Error Message** `%ASA-3-742007: password encryption failed due to unavailable memory`

**Explanation** An attempt to encrypt a password failed because no memory was available. Passwords may be left in clear text form in the configuration.

**Recommended Action** Correct the memory problem, and reapply the configuration that failed password encryption.

### 742008

**Error Message** `%ASA-3-742008: password _enc_pass_ decryption failed due to decoding error`

**Explanation** Password decryption failed because of decoding errors, which may occur if the encrypted password has been modified after being encrypted.

**Recommended Action** Reapply the configuration in question with a clear text password.

### 742009

**Error Message** `%ASA-3-742009: password encryption failed due to encoding error`

**Explanation** Password encryption failed because of decoding errors, which may be an internal software error.

**Recommended Action** Reapply the configuration in question with a clear text password. If the problem persists, contact the Cisco TAC.

### 742010

**Error Message** `%ASA-3-742010: encrypted password _enc_pass_ is not well formed`

**Explanation** The encrypted password provided in the command is not well formed. The password may not be a valid, encrypted password, or it may have been modified since it was encrypted.

-   _reason\_text_ —A string that represents the actual cause of the failure
-   _enc\_pass_ —The encrypted password that is related to the issue

**Recommended Action** Reapply the configuration in question with a clear text password.

### 743000

**Error Message** `%ASA-1-743000: The PCI device with vendor ID: _vendor_id_ device ID: _device_id_ located at bus:device.function (hex) _bus_num_:_dev_num_._func_num_ has a link _link_attr_name_ of _actual_link_attr_val_ when it should have a link _link_attr_name_ of _expected_link_attr_val_`

**Explanation** A PCI device in the system is not configured correctly, which may result in the system not performing at its optimum level.

**Recommended Action** Collect the output of the show controller pci detail command, and contact the Cisco TAC.

### 743001

**Error Message** `%ASA-1-743001: Backplane health monitoring detected link failure`

**Explanation** A hardware failure has probably occurred and has been detected on one of the links between the Secure Firewall ASA Services Module and the switch chassis.

**Recommended Action** Contact the Cisco TAC.

### 743002

**Error Message** `%ASA-1-743002: Backplane health monitoring detected link OK`

**Explanation** A link has been restored between the Secure Firewall ASA Services Module and the switch chassis. However, the failure and subsequent recovery probably indicates a hardware failure.

**Recommended Action** Contact the Cisco TAC.

### 743004

**Error Message** `%ASA-1-743004: System is not fully operational - The PCI device with vendor ID: _vendor_id_ (_vendor_name_) device ID: _device_id_ (_device_name_) could not be found in the system.`

**Explanation** A PCI device in the system that is needed for it to be fully operational was not found.

-   _vendor\_id_ —Hexadecimal value that identifies the device vendor
-   _vendor\_name_ —Text string that identifies the vendor name
-   _device\_id_ —Hexadecimal value that identifies the vendor device
-   _device\_name_ —Text string that identifies the device name

**Recommended Action** Collect the output of the show controller pci detail command and contact the Cisco TAC.

### 743010

**Error Message** `%ASA-3-743010: EOBC RPC server failed to start for client module _client_name_.`

**Explanation** The service failed to start for a particular client of the EOBC RPC service on the server.

**Recommended Action** Call the Cisco TAC.

### 743011

**Error Message** `%ASA-3-743011: EOBC RPC call failed, return code _code_.`

**Explanation** The EOBC RPC client failed to make an RPC to the intended server.

**Recommended Action** Call the Cisco TAC.

### 746001

**Error Message** `%ASA-6-746001: user-identity: _user-to-IP_address_databases_ started`

**Explanation** A database (user groups, hostnames, or IP addresses) download has started.

**Recommended Action** None required.

### 746002

**Error Message** `%ASA-6-746002: user-identity: _user-to-IP_address_databases_ complete`

**Explanation** A database (user groups, hostnames, or IP addresses) download has completed.

**Recommended Action** None required.

### 746003

**Error Message** `%ASA-3-746003: user-identity: _user-to-IP_address_databases_ failed - _reason_`

**Explanation** A database (user groups, hostnames, or IP addresses) download has failed because of a timeout.

**Recommended Action** Check the off-box AD agent status. If the AD agent is down, resolve that issue first. If the AD agent is up and running, try to download the database again. If the problem persists, contact the Cisco TAC.

### 746004

**Error Message** `%ASA-4-746004: user-identity: Total number of activated user groups exceeds the maximum number of _max_groups_ groups for this platform`

**Explanation** The total number of activated user groups exceeds the maximum number of 256 user groups for this platform.

**Recommended Action** Too many user groups have been configured and activated. Reduce the number of configured user groups. Run the clear user-identity user no-policy-activated command to release user records that have not been activated in any policy. Run the show user-identity user all command to check the total number of users in the database.

### 746005

**Error Message** `%ASA-3-746005: user-identity: The AD Agent _AD_agent_IP_address_ cannot be reached - _reason__action_`

**Explanation** The ASA cannot reach the AD agent. There has been no response from the AD agent, or the RADIUS registration failed because the buffer was too small.

**Recommended Action** Check the network connection between the AD agent and the ASA. Try to reach another AD agent, if one is configured and available. If the problem persists, contact the Cisco TAC.

### 746006

**Error Message** `%ASA-4-746006: user-identity: Out of sync with AD Agent, start bulk download`

**Explanation** The AD agent cannot update the IP-user mapping events on the ASA and the AD agent event log overflows, which causes inconsistency between the AD agent and the ASA IP-user database.

**Recommended Action** None required. If this message persists, check the connection between the AD agent and the ASA.

### 746007

**Error Message** `%ASA-5-746007: user-identity: NetBIOS response failed from User _user_name_ at _user_ip_`

**Explanation** No NetBIOS response was received for the number of retries made.

**Recommended Action** None required.

### 746008

**Error Message** `%ASA-6-746008: user-identity: NetBIOS Logout Probe Process started`

**Explanation** The NetBIOS process has started.

**Recommended Action** None required.

### 746009

**Error Message** `%ASA-6-746009: user-identity: NetBIOS Logout Probe Process stopped`

**Explanation** The NetBIOS process has stopped.

**Recommended Action** None required.

### 746010

**Error Message** `%ASA-3-746010: user-identity: Update import-user _domain_name_ - Import Failed _group_name_`

**Explanation** Entering the user-identity update import-user username command failed to update a user element. Reasons for failure include the following: timeout, partial update, import aborted, group does not exist, or no reason given.

**Recommended Action** If the reason for failure does not exist, verify that the group name is correct in the policy. Otherwise, check the connectivity between the ASA and the AD server.

### 746011

**Error Message** `%ASA-4-746011: user-identity: Total number of users created exceeds the maximum number of _max_users_ for this platform`

**Explanation** The AD group has more than the hard-coded maximum number (64000) of levels. Too many users have been configured in the activated policy.

**Recommended Action** Change your policies so that the number of configured users and users under configured groups does not exceed the limit.

### 746012

**Error Message** `%ASA-7-746012: user-identity: Add IP-User mapping _ip_address_ - _domain_name_\_user_name_ _result_ - _reason_`

**Explanation** A new user-IP mapping has been added to the user-to-IP address mapping database. The status of the operation (success or failure) is indicated. The success reason is VPN user. The failure reasons include the following: Maximum user limit reached and Duplicated address.

**Recommended Action** None required.

### 746013

**Error Message** `%ASA-7-746013: user-identity: Delete IP-User mapping _ip_address_ - _domain_name_\_user_ _name_ - _result_ _reason_`

**Explanation** A change has been made to the user-to-IP address mapping database. The status of the operation (success or failure) is indicated. The success reasons include the following: Inactive timeout, NetBIOS probing failed, PIP notification, VPN user logout, Cut-through-proxy user logout, and MAC address mismatch. The failure reason is PIP notification.

**Recommended Action** None required.

### 746014

**Error Message** `%ASA-5-746014: user-identity: [FQDN] _fqdn_ address _IP_Address_ obsolete`

**Explanation** A fully qualified domain name has become obsolete.

**Recommended Action** None required.

### 746015

**Error Message** `%ASA-5-746015: user-identity: [FQDN] _fqdn_ resolved _IP_address_`

**Explanation** A fully qualified domain name lookup has succeeded.

**Recommended Action** None required.

### 746016

**Error Message** `%ASA-3-746016: user-identity: DNS lookup for _ip_ failed, reason:_reason_`

**Explanation** A DNS lookup has failed. Failure reasons include timeout, unresolvable, and no memory.

**Recommended Action** Verify that the FQDN is valid, and that the DNS server is reachable from the ASA. If the problem persists, contact the Cisco TAC.

### 746017

**Error Message** `%ASA-6-746017: user-identity: Update import-user _domain_name_ issued`

**Explanation** The user-identity update import-user command has been issued.

**Recommended Action** None required.

### 746018

**Error Message** `%ASA-6-746018: user-identity: Update import-user _domain_name_ done`

**Explanation** The user-identity update import-user command has been issued, and the import has been completed successfully.

**Recommended Action** None requried.

### 746019

**Error Message** `%ASA-3-746019: user-identity: _Update_ AD Agent _Remove_ IP-user mapping _AD_agent_IP_Address_ - _user_IP_\_domain_name_ failed`

**Explanation** The ASA failed to update or remove an IP-user mapping on the AD agent.

**Recommended Action** Check the status of the AD agent and the connectivity between the ASA and the AD agent. If the problem persists, contact the Cisco TAC.

### 747001

**Error Message** `%ASA-3-747001: Clustering: Recovered from state machine event queue depleted. Event (_event-id_ , _ptr-in-hex_ , _ptr-in-hex_ ) dropped. Current state _state-name_ , stack _ptr-in-hex_ , _ptr-in-hex_ , _ptr-in-hex_ , _ptr-in-hex_ , _ptr-in-hex_ , _ptr-in-hex_`

**Explanation** The cluster FSM event queue is full, and a new event has been dropped.

**Recommended Action** None.

### 747002

**Error Message** `%ASA-5-747002: Clustering: Recovered from state machine dropped event (_event-id_ , _ptr-in-hex_ , _ptr-in-hex_ ). Intended state: _state-name_ . Current state: _state-name_ .`

**Explanation** The cluster FSM received an event that is incompatible with the current state.

**Recommended Action** None.

### 747003

**Error Message** `%ASA-5-747003: Clustering: Recovered from state machine failure to process event (_event-id_ , _ptr-in-hex_ , _ptr-in-hex_ ) at state _state-name_ .`

**Explanation** The cluster FSM failed to process an event for all reasons given.

**Recommended Action** None.

### 747004

**Error Message** `%ASA-6-747004: Clustering: state machine changed from state _state-name_ to _state-name_ .`

**Explanation** The cluster FSM has progressed to a new state.

**Recommended Action** None.

### 747005

**Error Message** `%ASA-7-747005: Clustering: State machine notify event _event-name_ (_event-id_ , _ptr-in-hex_ , _ptr-in-hex_ )`

**Explanation** The cluster FSM has notified clients about an event.

**Recommended Action** None.

### 747006

**Error Message** `%ASA-7-747006: Clustering: State machine is at state _state-name_`

**Explanation** The cluster FSM moved to a stable state; that is, Disabled, Slave, or Master.

**Recommended Action** None.

### 747007

**Error Message** `%ASA-5-747007: Clustering: Recovered from finding stray config sync thread, stack _ptr-in-hex_ , _ptr-in-hex_ , _ptr-in-hex_ , _ptr-in-hex_ , _ptr-in-hex_ , _ptr-in-hex_ .`

**Explanation** Astray configuration sync thread has been detected.

**Recommended Action** None.

### 747008

**Error Message** `%ASA-4-747008: Clustering: New cluster member _name_ with serial number _serial-number-A_ rejected due to name conflict with existing unit with serial number _serial-number-B_ .`

**Explanation** The same unit name has been configured on multiple units.

**Recommended Action** None.

### 747009

**Error Message** `%ASA-2-747009: Clustering: Fatal error due to failure to create RPC server for module _module name_ .`

**Explanation** The Secure Firewall ASA failed to create an RPC server.

**Recommended Action** Disable clustering on this unit and try to re-enable it. Contact the Cisco TAC if the problem persists.

### 747010

**Error Message** `%ASA-3-747010: Clustering: RPC call failed, message _message-name_ , return code _code-value_ .`

**Explanation** An RPC call failure has occurred. The system tries to recover from the failure.

**Recommended Action** None.

### 747011

**Error Message** `%ASA-2-747011: Clustering: Memory allocation error.`

**Explanation** A memory allocation failure occurred in clustering.

**Recommended Action** Disable clustering on this unit and try to re-enable it. If the problem persists, check the memory usage on the Secure Firewall ASA.

### 747012

**Error Message** `%ASA-3-747012: Clustering: Failed to replicate global object id _hex-id-value_ in domain _domain-name_ to peer _unit-name_ , continuing operation.`

**Explanation** A global object ID replication failure has occurred.

**Recommended Action** None.

### 747013

**Error Message** `%ASA-3-747013: Clustering: Failed to remove global object id _hex-id-value_ in domain _domain-name_ from peer _unit-name_ , continuing operation.`

**Explanation** A global object ID removal failure has occurred.

**Recommended Action** None.

### 747014

**Error Message** `%ASA-3-747014: Clustering: Failed to install global object id _hex-id-value_ in domain _domain-name_ , continuing operation.`

**Explanation** A global object ID installation failure has occurred.

**Recommended Action** None.

### 747015

**Error Message** `%ASA-4-747015: Clustering: Forcing stray member _unit-name_ to leave the cluster.`

**Explanation** A stray cluster member has been found.

**Recommended Action** None.

### 747016

**Error Message** `%ASA-4-747016: Clustering: Found a split cluster with both _unit-name-A_ and _unit-name-B_ as master units. Master role retained by _unit-name-A_ , _unit-name-B_ will leave, then join as a slave.`

**Explanation** A split cluster has been found.

**Recommended Action** None.

### 747017

**Error Message** `%ASA-4-747017: Clustering: Failed to enroll unit _unit-name_ due to maximum member limit _limit-value_ reached.`

**Explanation** The Secure Firewall ASA failed to enroll a new unit because the maximum member limit has been reached.

**Recommended Action** None.

### 747018

**Error Message** `%ASA-3-747018: Clustering: State progression failed due to timeout in module _module-name_ .`

**Explanation** The cluster FSM progression has timed out.

**Recommended Action** None.

### 747019

**Error Message** `%ASA-4-747019: Clustering: New cluster member _name_ rejected due to Cluster Control Link IP subnet mismatch (_ip-address_ /_ip-mask_ on new unit, _ip-address_ /_ip-mask_ on local unit).`

**Explanation** The control unit found that a new joining unit has an incompatible cluster interface IP address.

**Recommended Action** None.

### 747020

**Error Message** `%ASA-4-747020: Clustering: New cluster member _unit-name_ rejected due to encryption license mismatch.`

**Explanation** The control unit found that a new joining unit has an incompatible encryption license.

**Recommended Action** None.

### 747021

**Error Message** `%ASA-3-747021: Clustering: Master unit _unit-name_ is quitting due to interface health check failure on _interface-name_ .`

**Explanation** The control unit has disabled clustering because of an interface health check failure.

**Recommended Action** None.

### 747022

**Error Message** `%ASA-3-747022: Clustering: Asking slave unit _unit-name_ to quit because it failed interface health check _x_ times, rejoin will be attempted after _y_ min. Failed interface: _interface-name_ .`

**Explanation** This syslog message occurs when the maximum number of rejoin attempts has not been exceeded. A data unit has disabled clustering because of an interface health check failure for the specified amount of time. This unit will re-enable itself automatically after the specified amount of time (ms).

**Recommended Action** None.

### 747023

**Error Message** `%ASA-3-747023: Master unit %s[unit name] is quitting due to Security Service Module health check failure, and master's Security Service Module state is %s[SSM state, which can be UP/DOWN/INIT]. Rejoin will be attempted after %d[rejoin delay time] minutes.`

**Explanation** SSM health check failure on data unit; control unit asks data unit to quit with rejoin.

**Recommended Action** None.

### 747024

**Error Message** `%ASA-3-747024: Asking slave unit %s[unit name] to quit due to its Security Service Module health check failure, and its Security Service Module state is %s[SSM state]. The slave will decide whether to rejoin based on the configurations.`

**Explanation** SSM health check failure on data unit; control unit asks data unit to quit. The data unit would decide whether to rejoin or not.

**Recommended Action** None.

### 747025

**Error Message** `%ASA-4-747025: Clustering: New cluster member _unit-name_ rejected due to firewall mode mismatch.`

**Explanation** A control unit found a joining unit that has an incompatible firewall mode.

**Recommended Action** None.

### 747026

**Error Message** `%ASA-4-747026: Clustering: New cluster member _unit-name_ rejected due to cluster interface name mismatch (_ifc-name_ on new unit, _ifc-name_ on local unit).`

**Explanation** A control unit found a joining unit that has an incompatible cluster control link interface name.

**Recommended Action** None.

### 747027

**Error Message** `%ASA-4-747027: Clustering: Failed to enroll unit _unit-name_ due to insufficient size of cluster pool _pool-name_ in _context-name_ .`

**Explanation** A control unit could not enroll a joining unit because of the size limit of the minimal cluster pool configured.

**Recommended Action** None.

### 747028

**Error Message** `%ASA-4-747028: Clustering: New cluster member _unit-name_ rejected due to interface mode mismatch (_mode-name_ on new unit, _mode-name_ on local unit).`

**Explanation** A control unit found a joining unit that has an incompatible interface-mode, either spanned or individual.

**Recommended Action** None.

### 747029

**Error Message** `%ASA-4-747029: Clustering: Unit _unit-name_ is quitting due to Cluster Control Link down.`

**Explanation** A unit disabled clustering because of a cluster interface failure.

**Recommended Action** None.

### 747030

**Error Message** `%ASA-3-747030: Clustering: Asking slave unit _unit-name_ to quit because it failed interface health check _x_ times (last failure on _interface-name_ ), Clustering must be manually enabled on the unit to re-join.`

**Explanation** An interface health check has failed and the maximum number of rejoin attempts has been exceeded. A data unit has disabled clustering because of an interface health check failure.

**Recommended Action** None.

### 747031

**Error Message** `%ASA-3-747031: Clustering: Platform mismatch between cluster master (_platform-type_ ) and joining unit _unit-name_ (_platform-type_ ). _unit-name_ aborting cluster join.`

**Explanation** The joining unit's platform type does not match with that of the cluster control unit.

-   _unit-name_ —Name of the unit in the cluster bootstrap
-   _platform-type_ —Type of Secure Firewall ASA platform

**Recommended Action** Make sure that the joining unit has the same platform type as that of the cluster control unit.

### 747032

**Error Message** `%ASA-3-747032: Clustering: Service module mismatch between cluster master (_module-name_ ) and joining unit _unit-name_ (_module-name_ )in slot _slot-number_ . _unit-name_ aborting cluster join.`

**Explanation** The joining unit's external modules are not consistent (module type and order in which they are installed) with those on the cluster control unit.

-   _module-name—_ Name of the external module
-   _unit-name_ —Name of the unit in the cluster bootstrap
-   _slot-number_ —The number of the slot in which the mismatch occurred

**Recommended Action** Make sure that the modules installed on the joining unit are of the same type and are in the same order as they are in the cluster control unit.

### 747033

**Error Message** `%ASA-3-747033: Clustering: Interface mismatch between cluster master and joining unit _unit-name_ . _unit-name_ aborting cluster join.`

**Explanation** The joining unit's interfaces are not the same as those on the cluster control unit.

-   _unit-name_ —Name of the unit in the cluster bootstrap

**Recommended Action** Make sure that the interfaces available on the joining unit are the same as those on the cluster control unit.

### 747034

**Error Message** `%ASA-4-747034: Unit %s is quitting due to Cluster Control Link down (%d times after last rejoin). Rejoin will be attempted after %d minutes.`

**Explanation** Cluster Control Link down and the unit is kicked out with rejoin.

**Recommended Action** Wait for the unit to rejoin.

### 747035

**Error Message** `%ASA-4-747035: Unit %s is quitting due to Cluster Control Link down. Clustering must be manually enabled on the unit to rejoin.`

**Explanation** Cluster Control Link down and the unit is kicked out without rejoin.

**Recommended Action** Rejoin the unit manually.

### 747036

**Error Message** `%ASA-3-747036: Application software mismatch between cluster master %s[Master unit name] (%s[Master application software name]) and joining unit (%s[Joining unit application software name]). %s[Joining member name] aborting cluster join.`

**Explanation** The applications on control unit and the joining data unit are not the same. Data unit will be kicked out.

**Recommended Action** Make sure that the data unit run the same applications/services, and manually rejoin the unit.

### 747037

**Error Message** `%ASA-3-747037: Asking slave unit %s to quit due to its Security Service Module health check failure %d times, and its Security Service Module state is %s. Rejoin will be attempted after %d minutes.`

**Explanation** SSM health check failure on data unit; control unit asks data unit to quit with rejoin.

**Recommended Action** None.

### 747038

**Error Message** `%ASA-3-747038: Asking slave unit %s to quit due to Security Service Module health check failure %d times, and its Security Service Card Module is %s. Clustering must be manually enabled on this unit to rejoin.`

**Explanation** SSM health check failure on data; control unit asks data unit to quit with rejoin.

**Recommended Action** Manually rejoin the unit.

### 747039

**Error Message** `%ASA-3-747039: Unit %s is quitting due to system failure for %d time(s) (last failure is %s[cluster system failure reason]). Rejoin will be attempted after %d minutes.`

**Explanation** Clustering system failure, and the unit kicks itself out with rejoin

**Recommended Action** None required.

### 747040

**Error Message** `%ASA-3-747040: Unit %s is quitting due to system failure for %d time(s) (last failure is %s[cluster system failure reason]). Clustering must be manually enabled on the unit to rejoin.`

**Explanation** Clustering system failure and the unit kicks itself out without rejoin

**Recommended Action** Manually rejoin the unit.

### 747041

**Error Message** `%ASA-3-747041: Master unit %s is quitting due to interface health check failure on %s[interface name], %d times. Clustering must be manually enabled on the unit to rejoin.`

**Explanation** Interface health check failure on control unit; control unit kicks itself out with rejoin.

**Recommended Action** Manually rejoin the unit.

### 747042

**Error Message** `%ASA-3-747042: Clustering: Master received the config hash string request message from an unknown member with id _cluster-member-id_`

**Explanation** Control unit received the config hash string request event.

**Recommended Action** Verify requestor member is still in OnCall state.

### 747043

**Error Message** `%ASA-3-747043: Clustering: Get config hash string from master error: ret_code _ret_code_, string_len _string_len_`

**Explanation** Failed to get config hash string from control unit.

-   ret\_code⏤The error return code; 0 indicates OK, and 1 indicates Failed
    
-   string\_len⏤The hash\_str length
    

**Recommended Action** Contact technical support to troubleshoot the issue on control unit. Ensure to turn on 'debug cluster ccp’ to identify the root cause.

### 747044

**Error Message** `%ASA-6-747044: Configuration Hash string verification _result_`

**Explanation** The result of configuration hash string comparison..

-   result⏤This result can be PASSED or FAILED
    

**Recommended Action** None required.

### 748001

**Error Message** `%ASA-5-748001: Module _slot_number_ in chassis _chassis_number_ is leaving the cluster due to a chassis configuration change`

**Explanation** A cluster control link has changed in the MIO, a cluster group has been removed in the MIO, or a blade module has been removed in the MIO configuration.

-   _slot\_number_ —The blade slot ID within the chassis
-   _chassis\_number_ —The chassis ID, which is unique for each chassis

**Recommended Action** None required.

### 748002

**Error Message** `%ASA-4-748002: Clustering configuration on the chassis is missing or incomplete; clustering is disabled`

**Explanation** Configurations are missing or incomplete in the MIO (for example, a cluster group is not configured, or a cluster control link is not configured).

-   _slot\_number_ —The blade slot ID within the chassis
-   _chassis\_number_ —The chassis ID, which is unique for each chassis

**Recommended Action** Go to the MIO console and configure the cluster service type, add the module to the service type, and define the cluster control link accordingly.

### 748003

**Error Message** `%ASA-4-748003: Module _slot_number_ in chassis _chassis_number_ is leaving the cluster due to a chassis health check failure`

**Explanation** The blade cannot talk to the MIO, so it relies on the MIO to detect this communication problem and de-bundle the data ports. If data ports are de-bundled, the Secure Firewall ASA will be kicked out by an interface health check.

-   _slot\_number_ —The blade slot ID within the chassis
-   _chassis\_number_ —The chassis ID, which is unique for each chassis

**Recommended Action** Check if the MIO card is up or if the communication between the MIO and the blade is still up.

### 748004

**Error Message** `%ASA-5-748004: Module _slot_number_ in chassis _chassis_number_ is re-joining the cluster due to a chassis health check recovery`

**Explanation** The MIO blade health check has recovered, and the Secure Firewall ASA tries to rejoin the cluster.

-   _slot\_number_ —The blade slot ID within the chassis
-   _chassis\_number_ —The chassis ID, which is unique for each chassis

**Recommended Action** Check if the MIO card is up or if the communication between the MIO and the blade is still up

### 748005

**Error Message** `%ASA-3-748005: Failed to bundle the ports for module _slot_number_ in chassis _chassis_number_ ; clustering is disabled`

**Explanation** The MIO failed to bundle the ports for itself.

-   _slot\_number_ —The blade slot ID within the chassis
-   _chassis\_number_ —The chassis ID, which is unique for each chassis

**Recommended Action** Check if the MIO is operating correctly.

### 748006

**Error Message** `%ASA-3-748006: Asking module _slot_number_ in chassis _chassis_number_ to leave the cluster due to a port bundling failure`

**Explanation** The MIO failed to bundle ports for a blade, so the blade has been kicked out.

-   _slot\_number_ —The blade slot ID within the chassis
-   _chassis\_number_ —The chassis ID, which is unique for each chassis

**Recommended Action** Check if the MIO is operating correctly.

### 748007

**Error Message** `%ASA-2-748007: Failed to de-bundle the ports for module _slot_number_ in chassis _chassis_number_ ; traffic may be black holed`

**Explanation** The MIO failed to de-bundle the ports.

-   _slot\_number_ —The blade slot ID within the chassis
-   _chassis\_number_ —The chassis ID, which is unique for each chassis

**Recommended Action** Check if the MIO is operating correctly.

### 748008

**Error Message** `%ASA-6-748008: [CPU load _percentage_ | memory load _percentage_ ] of module _slot_number_ in chassis _chassis_number_ (_member-name_ ) exceeds overflow protection threshold [CPU _percentage_ | memory _percentage_ ]. System may be oversubscribed on member failure.`

**Explanation** The CPU load has exceeded (N-1)/N, where N is the total number of active cluster members, or the memory load has exceeded (100 – x) \* (N – 1) / N + x, where N is the number of cluster members, and x is the baseline memory usage of the last joining member.

-   _percentage_ —The CPU load or memory load percentile data
-   _slot\_number_ —The blade slot ID within the chassis
-   _chassis\_number_ —The chassis ID, which is unique for each chassis

**Recommended Action** Re-plan the network and clustering deployment. Either reduce the amount of traffic or add more blades/chassis.

### 748009

**Error Message** `%ASA-6-748009: [CPU load _percentage_ | memory load _percentage_ ] of chassis _chassis_number_ exceeds overflow protection threshold [CPU _percentage_ | memory _percentage_ }. System may be oversubscribed on chassis failure.`

**Explanation** The chassis traffic load exceeded a certain threshold.

-   _percentage_ —The CPU load or memory load percentile data
-   _chassis\_number_ —The chassis ID, which is unique for each chassis

**Recommended Action** Re-plan the network and clustering deployment. Either reduce the amount of traffic or add more blades/chassis.

### 748100

**Error Message** `%ASA-3-748100: <application_name> application status is changed from <status> to <status>.`

**Explanation** Detect the application status change from one state to another. Application status change will trigger application health check mechanism.

-   application name—snort or disk\_full
    
-   status—init, up, down
    

**Recommended Action** Verify the status of the application.

### 748101

**Error Message** `%ASA-3-748101: Peer unit <unit_id> reported its <application_name> application status is <status>.`

**Explanation** Peer unit reported application status change that will trigger application health check mechanism.

-   unit id—the unit id
    
-   application name—snort or disk\_full
    
-   status—init, up, down
    

**Recommended Action** Verify the status of the application.

### 748102

**Error Message** `%ASA-3-748102: Master unit <unit_id> is quitting due to <application_name> Application health check failure, and master's application state is <status>.`

**Explanation** Application health check detects that the control unit is not healthy. The control unit will leave the cluster group.

-   unit id—the unit id
    
-   application name—snort or disk\_full
    
-   status—init, up, down
    

**Recommended Action** Verify the status of the application. When the application (snort) is up again, the unit will rejoin automatically.

### 748103

**Error Message** `%ASA-3-748103: Asking slave unit <unit_id> to quit due to <application_name> Application health check failure, and slave's application state is <status>.`

**Explanation** Application health check detects that the data unit is not healthy. Control unit will evict the data node.

-   unit id—the unit id
    
-   application name—snort or disk\_full
    
-   status—init, up, down
    

**Recommended Action** Verify the status of the application. When the application (snort) is up again, the unit will rejoin automatically.

### 748201

**Error Message** `%ASA-4-748201: <Application name> application on module <module id> in chassis <chassis id> is <status>.`

**Explanation** Status of the application in the service chain gets changed.

-   status—up, down
    

**Recommended Action** Verify the status of the application in the service chain.

### 748202

**Error Message** `%ASA-3-748202: Module <module_id> in chassis <chassis id> is leaving the cluster due to <application name> application failure\n.`

**Explanation** Unit will be kicked out of cluster if the application such as vDP, fails.

**Recommended Action** Verify the status of the application in the service chain.

### 748203

**Error Message** `%ASA-5-748203: Module <module_id> in chassis <chassis id> is re-joining the cluster due to a service chain application recovery\n.`

**Explanation** Unit automatically rejoins the cluster if the service chain application such as vDP, recovers.

**Recommended Action** Verify the status of the application in the service chain.

### 750001

**Error Message** `%ASA-5-750001: Local:_local IP_ :_local port_ Remote:_remote IP_ : _remote port_ Username: _username_ Received request to _request_ an IPsec tunnel; local traffic selector = _local selectors: range, protocol, port range_ ; remote traffic selector = _remote selectors: range, protocol, port range_`

**Explanation** A request is being made for an operation on the IPsec tunnel such as a rekey, a request to establish a connection, and so on.

-   _local IP:local port_ — Local IP address for this request. The Secure Firewall ASA IP address and port number used for this connection
-   _remote IP:remote port_ — Remote IP address for this request. Peer IP address and port number that the connection is coming from
-   _username_ —Username of the requester for remote access, if known, or the tunnel group
-   _local selectors_ —Locally configured traffic selectors or proxies that are being used for this IPsec tunnel
-   _remote selectors_ —Remote peers requested traffic selectors or proxies for this IPsec tunnel

**Recommended Action** None required.

### 750002

**Error Message** `%ASA-5-750002: Local:_local IP_ :_local port_ Remote: _remote IP_ : _remote port_ Username: _username_ Received a IKE_INIT_SA request`

**Explanation** An incoming tunnel or SA initiation request (IKE\_INIT\_SA request) has been received.

-   _local IP:local port_ — Local IP address for this request. The Secure Firewall ASA IP address and port number used for this connection
-   _remote IP:remote port_ — Remote IP address for this request. Peer IP address and port number that the connection is coming from
-   _username_ —Username of the requester for remote access, if known, or the tunnel group

**Recommended Action** None required.

### 750003

**Error Message** `%ASA-4-750003: Local: _local IP:local port_ Remote: _remote IP:remote port_ Username: _username_ Negotiation aborted due to ERROR: _error_`

**Explanation** The negotiation of an SA was aborted because of the provided error reason.

-   _local IP:local port_ — Local IP address for this request. The Secure Firewall ASA IP address and port number used for this connection
-   _remote IP:remote port_ — Remote IP address for this request. Peer IP address and port number that the connection is coming from
-   _username_ —Username of the requester for remote access, if known yet
-   _error_ —Error reason for aborting the negotiation. Errors include the following:

\- Failed to send data on the network

\- Asynchronous request queued

\- Failed to enqueue packet

\- A supplied parameter is incorrect

\- Failed to allocate memory

\- Failed the cookie negotiation

\- Failed to find a matching policy

\- Failed to locate an item in the database

\- Failed to initialize the policy database

\- Failed to insert a policy into the database

\- The peer's proposal is invalid

\- Failed to compute the DH value

\- Failed to construct a NONCE

\- An expected payload is missing from the packet

\- Failed to compute the SKEYSEED

\- Failed to create child SA keys

\- The peer's KE payload contained the wrong DH group

\- Received invalid KE notify, yet we've tried all configured DH groups

\- Failed to compute a hash value

\- Failed to authenticate the IKE SA

\- Failed to compute or verify a signature

\- Failed to validate the certificate

\- The certificate has been revoked and is consequently invalid

\- Failed to build or process a certificate request

\- We requested a certificate, but the peer supplied none

\- While sending the certificate chain, peer did not send its certificate as the first in the chain

\- Detected an unsupported ID type

\- Failed to construct an encrypted payload

\- Failed to decrypt an encrypted payload

\- Detected an invalid value in the packet

\- The initiator bit is asserted in packet from original responder

\- The initiator bit isn't asserted in packet from original initiator

\- The message response bit is asserted in a packet from the exchange initiator

\- The message response bit isn't asserted in a packet from the exchange responder

\- Detected an invalid IKE SPI

\- Packet is a retransmission

\- Detected an invalid protocol ID

\- Detected unsupported critical payload

\- Detected an invalid traffic selector type

\- Failed to create new SA

\- Failed to delete SA

\- Failed to add new SA into session DB

\- Failed to add session to PSH

\- Failed to delete session from osal

\- Failed to delete a session from the database

\- Failed to add request to SA

\- Throttling request queue exceeds reasonable limit, increase the window size on peer

\- Received an IKE msg id outside supported window

\- Detected unsupported version number

\- Received no proposal chosen notify

\- Detected an error notify payload

\- Detected NAT-d hash doesn't match

\- Initialize sadb failed

\- Initialize session db failed

\- Failed to get PSH

\- Negotiation context locked currently in use

\- Negotiation context was not freed!

\- Invalid data state found

\- Failed to open PKI session

\- Failed to insert public keys

\- No certificate found

\- Unsupported cert encoding found or Peer requested HTTP URL but never sent HTTP\_LOOKUP\_SUPPORTED Notification

\- Sending BUNDLE URL is not supported at least for now. However, processing a BUNDLE URL is supported

\- Local certificate has expired

\- Failed to construct State Machine

\- Error encountered while navigating State Machine

\- SM Validation failed

\- Could not find neg context

\- Failed to add work request to SM Q

\- Nonce payload is missing

\- Traffic selector payload is missing

\- Unsupported DH group

\- Expected keypair is unavailable

\- Packet isn't encrypted

\- Packet is missing KE payload

\- Packet is missing SA payload

\- Invalid SA

\- Invalid negotiation context

\- Remote or local ID isn't defined

\- Invalid connection id

\- Unsupported auth method

\- Ipsec policy not found

\- Failed to initialize the event priority queue

\- Failed to enqueue an item to a list

\- Failed to remove an item from list

\- Data in the event priority queue is NULL or corrupt

\- No local IKE policy found

\- Can't delete IKE SA due to in-progress task

\- Expected Cookie Notify not received

\- Failed to generate auth data: My auth info missing

\- Failed to generate auth data: Failed to sign data

\- Failed to generate auth data: Signature operation successful but unable to locate generated auth material

\- Failed to receive the AUTH msg before the timer expired

\- Maximum number of retransmissions reached

\- Initial exchange failed

\- Auth exchange failed

\- Create child exchange failed

\- Platform errors

\- Failed to log a message

\- Unwanted debug level turned on

\- There are additional TS possible

\- A single pairs of addresses is required

\- Invalid session

\- There was no IPSEC policy found for received TS

\- Cannot remove request from window

\- There was no proposal found in configured policy

\- Nat-t test failure

\- No pskey found

\- Invalid compression algorithm

\- Failed to get profile name from platform service handle

\- Failed to find profile

\- Initiator failed to match profile sent by IPSEC with profile found by peer id or certificate

\- Failed to get peer id from platform service handle

\- The transform attribute is invalid

\- Extensible Authentication Protocol failed

\- Authenticator sent NULL EAP message

\- The config attribute is invalid

\- Failed to calculate packet hash

\- The AAA context is deleted

\- Cannot alloc AAA ID

\- Cannot alloc AAA request

\- Cannot init AAA request

\- The Authen list is not configured

\- Fail to send AAA request

\- Fail to alloc IP addr

\- Invalid message context

\- Key Auth memory failure

\- EAP method does not generate MSK

\- Failed to register new SA with platform

\- Failed to async process session register, error: %d

\- Failed to insert SA due to ipsec rekey collision

\- Failed while handling a ipsec rekey collision

\- Failed to accept rekey on SA that caused a rekey collision

\- Failed to start timer to ensure IPsec collision SA SPI %s/%s will be deleted by the peer

\- Error/Debug codes and strings are not matched

\- Failed to initialize SA lifetime

\- Failed to find rekey SA

\- Failed to generate DH shared secret

\- Failed to retrieve issuer public key hash list

\- Failed to build certificate payload

\- Unable to initialize the timer

\- Failed to generate DH shared secret

\- Failed to initialized authorization request

\- Incorrect author record received from AAA

\-Failed to fetch the keys from AAA

\-Failed to add attribute to AAA request

\-Failed to send tunnel password request to AAA

\- Failed to allocate AAA context

\- Insertion to policy AVL tree failed

\- Deletion from policy AVL tree failed

\- No Matching node found in policy AVL tree

\- No Matching policy found

\- No Matching proposal found

\- Proposal is incomplete to be attached to the policy

\- Proposal is in use

\- Peer authentication method configured is mismatching with the method proposed by peer

\- Failed to find the session in osal

\- Failed to allocate event

\- Failed to create accounting record

\- Accounting not required

\- Accounting not started for this session

\- NAT-T disabled via cli

\-Negotiating limit reached, deny SA request

\- SA is already in negotiation, hence not negotiating again

\- AAA group authorization failed

\- AAA user authorization failed

\- %% Dropping received fragment, as fragmentation is not negotiated for this SA!

\- Maximum number of received fragments reached for the SA

\- Number of fragments exceeds maximum allowed

\- Assembled packet length %d is greater than maximum ikev2 packet size %d

\- Received fragment numbers were NOT continuous or IKEV2\_FRAG\_FLAG\_LAST\_FRAGMENT flag was set on the wrong packet

\- Received fragment is not valid, hence being dropped

\- AAA group authorization failed

\- AAA user authorization failed

\- AAA author not configured in IKEv2 profile

\- Failed to extract the skeyid

\- Failed to send a failover msg to the standby unit

\- Detected unsupported failover version

\- Request was received but failover is not enabled

\- Received an active unit request but the negotiated role is %s

\- Received a standby unit request but the negotiated role is %s

\- Invalid IP Version

\- GDOI is not yet supported in IKEv2

\- Failed to allocate PSH from platform

\- Redirect the session to another gateway

\- Redirect check failed

\- Accept the session on this gateway after Redirect check

\- Detected unsupported Redirect gateway ID type

\- Redirect accepted, initiate new request

\- Redirect accepted, clean-up IKEv2 SA, platform will initiate new request

\- SA got redirected, it should not do any CREATE\_CHILD\_SA exchange

\- DH public key computation failed

\- DH secret computation failed

\- IN-NEG IKEv2 Rekey SA got deleted

\- Number of cert req exceeds the reasonable limit (%d)

\- The negotiation context has been freed

\- Assembled packet length %d is greater than maximum ikev2 packet size %d

\- Received fragment numbers were NOT continuous or IKEV2\_FRAG\_FLAG\_LAST\_FRAGMENT flag was set on the wrong packet

\- AAA author not configured in IKEv2 profile

\- Assembled packet is not valid, hence being dropped

\- Invalid VCID context

**Recommended Action** Review the syslog and follow the flow of the logs to determine if this syslog is the final in the exchange and if it is the cause of a potential failure or a transient error that was renegotiated through. For example, a peer may suggest a DH group via the KE payload that is not configured that causes an initial request to fail, but the correct DH group is communicated so that the peer can come back with the correct group in a new request.

### 750004

**Error Message** `%ASA-5-750004: Local: _local IP: local port_ Remote: _remote IP: remote port_ Username: _username_ Sending COOKIE challenge to throttle possible DoS`

**Explanation** An incoming connection request was challenged with a cookie based on the cookie challenge thresholds that are configured to prevent a possible DoS attack.

-   _local IP:local port_ — Local IP address for this request. The Secure Firewall ASA IP address and port number used for this connection
-   _remote IP:remote port_ — Remote IP address for this request. Peer IP address and port number that the connection is coming from
-   _username_ —Username of the requester for remote access, if known yet

**Recommended Action** None required.

### 750005

**Error Message** `%ASA-5-750005: Local: _local IP: local port_ Remote: _remote IP: remote port_ Username: _username_ IPsec rekey collision detected. I am lowest nonce initiator, deleting SA with inbound SPI _SPI_`

**Explanation** A rekey collision was detected (both peers trying to initiate a rekey at the same time), and it was resolved by keeping the one initiated by this Secure Firewall ASA because it had the lowest nonce. This action caused the indicated SA referenced by the SPI to be deleted.

-   _local IP:local port_ — Local IP address for this request. The Secure Firewall ASA IP address and port number used for this connection
-   _remote IP:remote port_ — Remote IP address for this request. Peer IP address and port number that the connection is coming from
-   _username_ —Username of the requester for remote access, if known yet
-   _SPI_ —SPI handle of the SA being deleted by resolving the rekey collision that was detected

**Recommended Action** None required.

### 750006

**Error Message** `%ASA-5-750006: Local: _local IP: local port_ Remote: _remote IP: remote port_ Username: _username_ SA UP. Reason: _reason_`

**Explanation** An SA came up for the given reason, such as for a newly established connection or a rekey.

-   _local IP:local port_ — Local IP address for this request. The Secure Firewall ASA IP address and port number used for this connection
-   _remote IP:remote port_ — Remote IP address for this request. Peer IP address and port number that the connection is coming from
-   _username_ —Username of the requester for remote access, if known yet
-   _reason_ —Reason that the SA came into the UP state

**Recommended Action** None required.

### 750007

**Error Message** `%ASA-5-750007: Local: _local IP: local port_ Remote: r_emote IP: remote port_ Username: _username_ SA DOWN. Reason: _reason_`

**Explanation** An SA was torn down or deleted for the given reason, such as a request by the peer, operator request (via an administrator action), rekey, and so on.

-   _local IP:local port_ — Local IP address for this request. The Secure Firewall ASA IP address and port number used for this connection
-   _remote IP:remote port_ — Remote IP address for this request. Peer IP address and port number that the connection is coming from
-   _username_ —Username of the requester for remote access, if known yet
-   _reason_ —Reason that the SA came into the DOWN state

**Recommended Action** None required.

### 750008

**Error Message** `%ASA-5-750008: Local: _local IP: local port_ Remote: _remote IP: remote port_ Username: _username_ SA rejected due to system resource low`

**Explanation** An SA request was rejected to alleviate a low system resource condition.

-   _local IP:local port_ — Local IP address for this request. The Secure Firewall ASA IP address and port number used for this connection
-   _remote IP:remote port_ — Remote IP address for this request. Peer IP address and port number that the connection is coming from
-   _username_ —Username of the requester for remote access, if known yet

**Recommended Action** Check CAC settings for IKEv2 to determine if this is expected behavior based on configured thresholds; otherwise, if the condition persists, investigate further to alleviate the issue.

### 750009

**Error Message** `%ASA-5-750009: Local: _local IP: local port_ Remote: _remote IP: remote port_ Username: _username_ SA request rejected due to CAC limit reached: Rejection reason: _reason_`

**Explanation** A Connection Admission Control (CAC) limiting threshold was reached, which caused the SA request to be rejected.

-   _local IP:local port_ — Local IP address for this request. The Secure Firewall ASA IP address and port number used for this connection
-   _remote IP:remote port_ — Remote IP address for this request. Peer IP address and port number that the connection is coming from
-   _username_ —Username of the requester for remote access, if known yet
-   _reason_ —Reason that the SA was rejected

**Recommended Action** Check CAC settings for IKEv2 to determine if this is expected behavior based on configured thresholds; otherwise, if the condition persists, investigate further to alleviate the issue.

### 750010

**Error Message** `%ASA-5-750010: Local: _local-ip_ Remote: _remote-ip_ Username:_username_ IKEv2 local throttle-request queue depth threshold of _threshold_ reached; increase the window size on peer _peer_ for better performance`

-   _local-ip_ —Local peer IP address
-   _remote-ip_ —Remote peer IP address
-   _username_ —Username of the requester for remote access or tunnel group name for L2L, if known yet
-   _threshold_ —Queue depth threshold of the local throttle-request queue reached
-   _peer_ —Remote peer IP address

**Explanation** The Secure Firewall ASA overflowed its throttle request queue to the specified peer, indicating that the peer is slow. The throttle request queue holds requests destined for the peer, which cannot be sent immediately because the maximum number of requests allowed to be in-flight based on the IKEv2 window size were already in-flight. As in-flight requests are completed, requests are pulled off of the throttle request queue and sent to the peer. If the peer is not processing these requests quickly, the throttle queue backs up.

**Recommended Action** If possible, increase the IKEv2 window size on the remote peer to allow more concurrent requests to be in-flight, which may improve performance.

| ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)

**Note** | ___

The Secure Firewall ASA does not currently support an increased IKEv2 window size setting.

___ |
|--------|------------------------------------------------------------------------------------------------|

### 750011

**Error Message** `%ASA-3-750011: Tunnel Rejected: Selected IKEv2 encryption algorithm (_IKEV2 encry algo_ ) is not strong enough to secure proposed IPSEC encryption algorithm (_IPSEC encry algo_ ).`

**Explanation** The tunnel was rejected because the selected IKEv2 encryption algorithm is not strong enough to secure the proposed IPSEC encryption algorithm.

**Recommended Action** Configure a stronger IKEv2 encryption algorithm to match or exceed the strength of the IPsec child SA encryption algorithm.

### 750012

**Error Message** `%ASA-4-750012: Selected IKEv2 encryption algorithm (_IKEV2 encry algo_ ) is not strong enough to secure proposed IPSEC encryption algorithm (_IPSEC encry algo_ ).`

**Explanation** The selected IKEv2 encryption algorithm is not strong enough to secure the proposed IPSEC encryption algorithm.

**Recommended Action** Configure a stronger IKEv2 encryption algorithm to match or exceed the strength of the IPsec child SA encryption algorithm.

### 750013

**Error Message** `%ASA-5-750013: IKEv2 SA (iSPI ISPI rRSP rSPI) Peer Moved: Previous prev_remote_ip:prev_remote_port/prev_local_ip:prev_local_port. Updated new_remote_ip:new_remote_port/new_local_ip:new_local_port`

**Explanation** The new mobike feature allows peer IP to be changed without tearing down the tunnel. For example, a mobile device (smartphone) acquires new IP after connecting to a different network.The following list describes the message values:

-   _ip_ —Specifies the previous, the new local, and remote IP addresses
-   _port_ —Specifies the previous, the new local, and remote port information
-   _SPI_ —Indicates the Initiator and Responder SPI
-   _iSPI_ —Specifies the Initiator SPI
-   _rSPI_ —Specifies the Responder SPI

**Recommended Action** Contact the Development engineers.

### 750014

**Error Message** `%ASA-4-750014: Local:_self ip_:_self port_ Remote:_peer ip_:_peer port_ Username:_TG or Username_ IKEv2 Session aborted. Reason: Initial Contact received for Local ID: _self ID_, Remote ID: _peer ID_ from remote peer:_peer ip_:_peer port_ to _self ip_:_self port_`

**Explanation**

For ASA IKEv2, the initial contact (IC) processing is done based on peer IP/Port and ASA IP/Port pairs and the stale sessions get deleted based on these IP/Port pairs. This could be a problem with NAT as IP/Port of peer may change for connections and the stale sessions would not get cleaned up based on IP/Port pairs. As per the IKEv2 RFC , the Initial Contact processing will be switched to use Identity pairs so that the stale sessions can be identified based on peer and ASA identities and clear them. The identities can be IPs, hostnames, Certificate DNs, and so on. This syslog displays the exact reason for clearing the stale sessions. This syslog will be generated on ASA after clearing a stale session from a peer while negotiating a new IKEv2 session with the same peer. This syslog is applicable only for standalone and clustering site-to-site VPNs and not for RA.

**Recommended Action** IKEv2 session Initial Contact processing is done to reset state between peers and clear the stale sessions. If sessions are getting cleared unexpectedly due to Initial Contact processing, ensure that all peers are configured with unique identities.

### 750015

**Error Message** `%ASA-4-750015: Local:_self ip_:_self port_ Remote:_peer ip_:_peer port_ Username:_TG or Username_ deleting IPSec SA. Reason: invalid SPI notification received for SPI 0x_SPI_; local traffic selector = Address Range: _start address_-_end address_ Protocol: _protocol number_ Port Range: _start port_-_end port_ ; remote traffic selector = Address Range: _start address_-_end address_ Protocol: _protocol number_ Port Range: _start port_-_end port_`

**Explanation**

When an ESP packet gets dropped due to invalid SPI, an INFORMATIONAL exchange with the peer has been added. When peer receives this notification, the child SA causing INVALID\_SPI scenario will be cleared, thereby sync the child SAs sooner and reducing the traffic loss. This IKEv2 syslog is introduced when the child SA gets cleared due to INVALID\_SPI INFORMATIONAL exchange. The following describes the message values:

-   _SPI_—SPI in hex for which INVALID\_SPI notification was received.
    

**Recommended Action** An out-of-sync IKEv2 child condition was detected and handled. No action is required.

### 750016

**Error Message** `%ASA-7-750016: Local: _localIP:port_ Remote:_remoteIP:port_ Username:_username_ Need to send a DPD message to peer`

**Explanation**

The device may have terminated a connection to the peer. Dead peer detection needs to be performed for the specified peer to determine if it is still alive. The following describes the message values:

-   _localIP:port_ —The local IP address and port number
    
-   _remoteIP:port_ —The remote IP address and port number
    
-   _username_ —The username associated with this connection attempt
    

**Recommended Action** No action is required.

### 751001

**Error Message** `%ASA-3-751001: Failed to complete Diffie-Hellman operation. Error: _error_.`

**Explanation** A failure to complete a Diffie-Hellman operation occurred, as indicated by the error.

-   _error_ —The error string that indicates the specific error

**Recommended Action** A low memory issue or other internal error that should be resolved has occurred. If it persists, use the memory tracking tool to isolate the issue.

### 751002

**Error Message** `%ASA-3-751002: No pre-shared key or trustpoint configured for self in tunnel group _group_`

**Explanation** The Secure Firewall ASA was unable to find any type of authentication information in the tunnel group that it could use to authenticate itself to the peer.

-   _group_ —The name of the tunnel group

**Recommended Action** Check the tunnel group configuration, and configure a preshared key or certificate for self-authentication in the indicated tunnel group.

### 751003

**Error Message** `%ASA-7-751003: Need to send a DPD message to peer`

**Explanation** Dead peer detection needs to be performed for the specified peer to determine if it is still alive. The Secure Firewall ASA may have terminated a connection to the peer.

**Recommended Action** None required.

### 751004

**Error Message** `%ASA-3-751004: No remote authentication method configured for peer in tunnel group _group_`

**Explanation** A method to authenticate the remote peer was not found in the configuration to allow the connection.

-   _group_ —The name of the tunnel group

**Recommended Action** Check the configuration to make sure that a valid remote peer authentication setting is present.

### 751005

**Error Message** `%ASA-3-751005: AnyConnect client reconnect authentication failed. Session ID: _session_id_, Error: _error_`

**Explanation** A failure occurred during an AnyConnect client reconnection attempt using the session token.

-   _session\_id_ —The session ID used to try to reconnect
-   _error_ —The error string to indicate the specific error that occurred during the reconnection attempt

**Recommended Action** Take action according to the error specified, if necessary. The error may indicate that a session was removed instead of remaining in resume state because a client disconnect was detected or sessions were cleared on the Secure Firewall ASA. If necessary, also compare this message to the event logs on the Anyconnect client.

### 751006

**Error Message** `%ASA-3-751006: Certificate authentication failed. Error: _error_`

**Explanation** A failure related to certificate authentication occurred.

-   _error_ —The error string to indicate the specific certificate authentication failure

**Recommended Action** Take action according to the error specified, if necessary. Check the certificate trustpoint configuration and make sure that the necessary CA certificate exists to be able to correctly verify client certificate chains. Use the debug crypto ca commands to isolate the failure.

### 751007

**Error Message** `%ASA-5-751007: Configured attribute not supported for IKEv2. Attribute: _attribute_`

**Explanation** A configured attribute could not be applied to the IKE version 2 connection because it is not supported for IKE version 2 connections.

-   _attribute_ —The attribute that is configured to be applied

**Recommended Action** None required, To eliminate this message from being generated, you can remove the IKE version 2 configuration setting.

### 751008

**Error Message** `%ASA-3-751008: Group=_group_, Tunnel rejected: IKEv2 not enabled in group policy`

**Explanation** IKE version 2 is not allowed based on the enabled protocols for the indicated group to which a connection attempt was mapped, and the connection was rejected.

-   _group_ —The tunnel group used for connection

**Recommended Action** Check the group policy VPN tunnel protocol setting and enable IKE version 2, if desired.

### 751009

**Error Message** `%ASA-3-751009: Unable to find tunnel group for peer.`

**Explanation** A tunnel group could not be found for the peer.

**Recommended Action** Check the configuration and tunnel group mapping rules, then configure them to allow the peer to land on a configured group.

### 751010

**Error Message** `%ASA-3-751010: Local: _localIP:port_ Remote:_remoteIP:port_ Username: _username/group_ Unable to determine self-authentication method. No crypto map setting or tunnel group found.`

**Explanation** A method for authenticating the Secure Firewall ASA to the peer could not be found in either the tunnel group or crypto map.

-   _localIP:port_ —The local IP address and port number
-   _remoteIP:port_ —The remote IP address and port number
-   _username/group_ —The username or group associated with this connection attempt

**Recommended Action** Check the configuration, and configure a self-authentication method in the crypto map for the initiator L2L or in the applicable tunnel group.

### 751011

**Error Message** `%ASA-3-751011: Failed user authentication. Error: _error_`

**Explanation** A failure occurred during user authentication within EAP for an IKE version 2 remote access connection.

-   _error_ —The error string that indicates the specific error

**Recommended Action** Make sure that the correct authentication credentials were provided and debug further to determine the exact cause of failure, if necessary.

### 751012

**Error Message** `%ASA-3-751012: Failure occurred during Configuration Mode processing. Error: _error_`

**Explanation** A failure occurred during configuration mode processing while settings were being applied to the connection.

-   _error_ —The error string that indicates the specific error

**Recommended Action** Take action based on the indicated error. Use the debug crypto ikev2 commands to determine the cause of the failure, or debug the indicated subsystem that is specified by the error, if necessary.

### 751013

**Error Message** `%ASA-3-751013: Failed to process Configuration Payload request for attribute _attribute_id_. Error: _error_`

**Explanation** The Configuration Payload request failed to process and generate a Configuration Payload response for an attribute that was requested by the peer.

-   _attribute\_id_ — The attribute ID on which the failure occurred
-   _error_ —The error string that indicates the specific error

**Recommended Action** A memory error, configuration error, or another type of error has occurred. Use the debug crypto ikev2 commands to help isolate the cause of the failure.

### 751014

**Error Message** `%ASA-4-751014: Warning Configuration Payload request for attribute _attribute_id_ could not be processed. Error: _error_`

**Explanation** A warning occurred while processing a CP request to generate a CP response for a requested attribute.

-   _attribute\_id_ — The attribute ID on which the failure occurred
-   _error_ —The error string that indicates the specific error

**Recommended Action** Take action based on the attribute indicated in the warning and the indicated warning message. For example, a newer client is being used with an older Secure Firewall ASA image, which does not understand a new attribute that has been added to the client. An upgrade of the Secure Firewall ASA image may be necessary to allow the attribute to be processed.

### 751015

**Error Message** `%ASA-4-751015: SA request rejected by CAC. Reason: _reason_`

**Explanation** The connection was rejected by the call admission control to protect the Secure Firewall ASA based on configured thresholds or conditions indicated by the reason listed.

-   _reason_ —The reason that the SA request was rejected

**Recommended Action** Check the reason and resolve the condition if a new connection should have been accepted or change the configured thresholds.

### 751016

**Error Message** `%ASA-4-751016: Remote L2L Peer initiated a tunnel with same outer and inner addresses. Peer could be Originate Only - Possible misconfiguration!`

**Explanation** The peer may be configured for originate-only connections based on the received outer and inner IP addresses for the tunnel.

**Recommended Action** Check the L2L peer configuration.

### 751017

**Error Message** `%ASA-3-751017: Configuration Error: _error_description_.`

**Explanation** An error in the configuration that prevented the connection has been detected.

-   _error description_ —A brief description of the configuration error

**Recommended Action** Correct the configuration based on the indicated error.

### 751018

**Error Message** `%ASA-3-751018: Terminating the VPN connection attempt from _attempted group_.`

**Explanation** The tunnel group over which the connection is attempted is not the same as the tunnel group set in the group lock.

-   _attempted group_ —The tunnel group over which the connection came in

**Recommended Action** Check the group-lock value in the group policy or the user attributes.

### 751019

**Error Message** `%ASA-4-751019: Failed to obtain an _licenseType_ license. Maximum license limit _limit_ exceeded.`

**Explanation** A session creation failed because the maximum license limit was exceeded, which caused a failure to either initiate or respond to a tunnel request.

-   _licenseType_ — License type that was exceeded (other VPN or AnyConnect Premium/Essentials)
-   _limit_ —Number of licenses allowed and was exceeded

**Recommended Action** Make sure that enough licenses are available for all allowed users and/or obtain more licenses to allow the rejected connections. For multiple context mode, allow more licenses for the context that reported the failure, if necessary.

### 751020

**Error Message** `%ASA-3-751020: Local:%A:%u Remote:%A:%u Username:%s An %s remote access connection failed. Attempting to use an NSA Suite B crypto algorithm (%s) without an AnyConnect Premium license.`

**Explanation** An IKEv2 remote access tunnel could not be created because the AnyConnect Premium license was applied but explicitly disabled with the anyconnect-essentials command in the webvpn configuration mode.

**Recommended Action** Make sure that an AnyConnect Premium license is installed on the Secure Firewall ASA is configured in the remote access IKEv2 policies or IPsec proposals.

### 751021

**Error Message** `%ASA-4-751021: _variable_1 variable_2_ with _variable_3_ encryption is not supported with this version of the AnyConnect Client. Please upgrade to the latest Anyconnect Client.`

**Explanation** An out-of-date AnyConnect client tried to connect to an Secure Firewall ASA that has IKEv2 with AES-GCM encryption policy configured.

-   _variable\_1_ —Username of the AnyConnect client (may be unknown because this occurs before the user enters a username)
-   _variable\_2_ —Connection protocol type (IKEv1, IKEv2)
-   _variable\_3_ —Combined mode encryption type (AES-GCM, AES-GCM 256)

**Recommended Action** Upgrade the AnyConnect client to the latest version to use IKEv2 with AES-GCM encryption.

### 751022

**Error Message** `%ASA-3-751022: Tunnel rejected: Crypto Map Policy not found for remote traffic selector _rem-ts-start_/_rem-ts-end_/_rem-ts.startport_/_rem-ts.endport_/_rem-ts.protocol_ local traffic selector _local-ts-start_/_local-ts-end_/_local-ts.startport_/_local-ts.endport_/_local-ts.protocol_!`

**Explanation** The Secure Firewall ASA was not able to find security policy information for the private networks or hosts indicated in the message. These networks or hosts were sent by the initiator and do not match any crypto ACLs at the Secure Firewall ASA. This is most likely a misconfiguration.

-   _rem-ts-start_ —Remote traffic selector start address
-   _rem-ts-end_ —Remote traffic selector end address
-   _rem-ts.startport_ —Remote traffic selector start port
-   _rem-ts.endport_ —Remote traffic selector end port
-   _rem-ts.protocol_ —Remote traffic selector protocol
-   _local-ts-start_ —Local traffic selector start address
-   _local-ts-end_ —Local traffic selector end address
-   _local-ts.startport_ —Local traffic selector start port
-   _local-ts.endport_ —Local traffic selector end port
-   _local-ts.protocol_ —Local traffic selector protocol

**Recommended Action** Check the protected network configuration in the crypto ACLs on both sides and make sure that the local network on the initiator is the remote network on the responder and vice-versa. Pay special attention to wildcard masks and host addresses as compared to network addresses. Non-Cisco implementations may have the private addresses labeled as proxy addresses or “red” networks.

### 751023

**Error Message** `%ASA-6-751023: Unknown client connection.`

**Explanation** An unknown non-Cisco IKEv2 client has connected to the Secure Firewall ASA.

**Recommended Action** Upgrade to a Cisco-supported IKEv2 client.

### 751024

**Error Message** `%ASA-3-751024: IPv6 User Filter _tempipv6_ configured. This setting has been deprecated, terminating connection`

**Explanation** The IPv6 VPN filter has been deprecated and if it is configured instead of a unified filter for IPv6 traffic access control, the connection will be terminated.

**Recommended Action** Configure a unified filter with IPv6 entries to control IPv6 traffic for the user.

### 751025

**Error Message** `%ASA-5-751025: Group:_group-policy_ IPv4 Address=_assigned_IPv4_addr_ IPv6 address=_assigned_IPv6_addr_ assigned to session`

**Explanation** This message displays the assigned IP address information for the AnyConnect IKEv2 connection of the specified user.

-   _group-policy_ —The group policy that allowed the user to gain access
-   _assigned\_IPv4\_addr_ —The IPv4 address that is assigned to the client
-   _assigned\_IPv6\_addr_ —The IPv6 address that is assigned to the client

**Recommended Action** None required.

### 751026

**Error Message** `%ASA-6-751026: Client OS: _client-os_ Client: _client-name_ _client-version_`

**Explanation** The indicated user is attempting to connect with the shown operating system and client version.

-   _client-os_ —The operating system reported by the client
-   _client-name_ —The client name reported by the client (usually AnyConnect)
-   _client-version_ —The client version reported by the client

**Recommended Action** None required.

### 751027

**Error Message** `%ASA-4-751027: Received INVALID_SELECTORS Notification. Peer received a packet (SPI= _spi_). The decapsulated inner packet didn't match the negotiated policy in the SA. Packet destination _pkt_daddr_, port _pkt_dest_port_, source _pkt_saddr_, port _pkt_src_port_, protocol _pkt_prot_.`

**Explanation** A peer received a packet on an IPsec security association (SA) that did not match the negotiated traffic descriptors for that SA. The peer sent an INVALID\_SELECTORS notification containing the SPI and packet data for the offending packet.

-   _spi_ —SPI of the IPsec SA for the packet
-   _pkt\_daddr_ —Packet destination IP address
-   _pkt\_dest\_port_ —Packet destination port
-   _pkt\_saddr_ —Packet source IP address
-   _pkt\_src\_port_ —Packet source port
-   _pkt\_prot_ —Packet protocol

**Recommended Action** Copy the error message, the configuration, and any details about the events leading up to this error, then submit them to Cisco TAC.

### 751028

**Error Message** `%ASA-5-751028: Overriding configured keepalive values of threshold:_config_threshold_/retry:_config_retry_ to threshold:_applied_threshold_/retry:_applied_retry_.`

**Explanation** When configured for distributed-site to site with clustering, the keepalive threshold and retry intervals should be increased to prevent overloading the system. If the configured values are below these required values, the required values will be applied. The following list describes the message values:

-   _config\_threshold_ — The configured keepalive threshold for tunnel-group
    
-   _config\_retry_ — The configured keepalive retry for tunnel-group
    
-   _applied\_threshold_ — The keepalive threshold being applied
    
-   _applied\_retry_ — The keepalive retry being applied
    

**Recommended Action** Configure to at least the required minimum values.

### 752001

**Error Message** `%ASA-2-752001: Tunnel Manager received invalid parameter to remove record`

**Explanation** A failure to remove a record from the tunnel manager that might prevent future tunnels to the same peer from initiating has occurred.

**Recommended Action** Reloading the device will remove the record, but if the error persists or recurs, perform additional debugging of the specific tunnel attempt.

### 752002

**Error Message** `%ASA-7-752002: Tunnel Manager Removed entry. Map Tag = _mapTag_ . Map Sequence Number = _mapSeq_ .`

**Explanation** An entry to initiate a tunnel was successfully removed.

-   _mapTag_ —Name of the crypto map for which the initiation entry was removed
-   _mapSeq_ —Sequence number of the crypto map for which the initiation entry was removed

**Recommended Action** None required.

### 752003

**Error Message** `%ASA-5-752003: Tunnel Manager dispatching a KEY_ACQUIRE message to IKEv2. Map Tag = _mapTag_ . Map Sequence Number = _mapSeq_`

**Explanation** An attempt is being made to initiate an IKEv2 tunnel that was based on the crypto map indicated.

-   _mapTag_ —Name of the crypto map for which the initiation entry was removed
-   _mapSeq_ —Sequence number of the crypto map for which the initiation entry was removed

**Recommended Action** None required.

### 752004

**Error Message** `%ASA-5-752004: Tunnel Manager dispatching a KEY_ACQUIRE message to IKEv1. Map Tag = _mapTag_ . Map Sequence Number = _mapSeq_`

**Explanation** An attempt is being made to initiate an IKEv1 tunnel that was based on the crypto map indicated.

-   _mapTag_ —Name of the crypto map for which the initiation entry was removed
-   _mapSeq_ —Sequence number of the crypto map for which the initiation entry was removed

**Recommended Action** None required.

### 752005

**Error Message** `%ASA-2-752005: Tunnel Manager failed to dispatch a KEY_ACQUIRE message. Memory may be low. Map Tag = _mapTag_ . Map Sequence Number = _mapSeq._`

**Explanation** An attempt to dispatch a tunnel initiation attempt failed because of an internal error, such as a memory allocation failure.

-   _mapTag_ —Name of the crypto map for which the initiation entry was removed
-   _mapSeq_ —Sequence number of the crypto map for which the initiation entry was removed

**Recommended Action** Use the memory tracking tools and additional debugging to isolate the issue.

### 752006

**Error Message** `%ASA-3-752006: Tunnel Manager failed to dispatch a KEY_ACQUIRE message. Probable mis-configuration of the crypto map or tunnel-group. Map Tag = _Tag_ . Map Sequence Number = _num,_ SRC Addr: _address_ port_: port_ Dst Addr: _address_ port: _port_ .`

**Explanation** An attempt to dispatch a tunnel initiation attempt failed because of a configuration error of the indicated crypto map or associated tunnel group.

-   _Tag_ —Name of the crypto map for which the initiation entry was removed
-   _num_ —Sequence number of the crypto map for which the initiation entry was removed
-   _address_ —The source IP address or destination IP address
-   _port_ —The source port number or destination port number

**Recommended Action** Check the configuration of the tunnel group and crypto map indicated to make sure that it is complete.

### 752007

**Error Message** `%ASA-3-752007: Tunnel Manager failed to dispatch a KEY_ACQUIRE message. Entry already in Tunnel Manager. Map Tag = _mapTag_ . Map Sequence Number = _mapSeq_`

**Explanation** An attempt was made to re-add an existing entry into the tunnel manager.

-   _mapTag_ —Name of the crypto map for which the initiation entry was removed
-   _mapSeq_ —Sequence number of the crypto map for which the initiation entry was removed

**Recommended Action** If the issue persists, make sure that the configuration of the peer will allow the tunnel, and debug further to make sure that the tunnel manager entries are being added and removed correctly during tunnel initiation and successful or failed initiation attempts. Debug IKE version 2 or IKE version 1 connections further, because they may still be in the process of creating the tunnel.

### 752008

**Error Message** `%ASA-7-752008: Duplicate entry already in Tunnel Manager`

**Explanation** A duplicate request to initiate a tunnel was made, and the tunnel manager is already attempting to initiate the tunnel.

**Recommended Action** None required. If the issue persists, either IKE version 1 or IKE version 2 may have attempted a tunnel initiation and not have timed out yet. Debug further using the applicable commands to make sure that the tunnel manager entry is removed after successful or failed initiation attempts.

### 752009

**Error Message** `%ASA-4-752009: IKEv2 Doesn't support Multiple Peers`

**Explanation** An attempt to initiate a tunnel with IKE version 2 failed because the crypto map is configured with multiple peers, which is not supported for IKE version 2. Only IKE version 1 supports multiple peers.

**Recommended Action** Check the configuration to make sure that multiple peers are not expected for IKE version 2 site-to-site initiation.

### 752010

**Error Message** `%ASA-4-752010: IKEv2 Doesn't have a proposal specified`

**Explanation** No IPsec proposal was found to be able to initiate an IKE version 2 tunnel .

**Recommended Action** Check the configuration, then configure an IKE version 2 proposal that can be used to initiate the tunnel, if necessary.

### 752011

**Error Message** `%ASA-4-752011: IKEv1 Doesn't have a transform set specified`

**Explanation** No IKE version 1 transform set was found to be able to initiate an IKE version 2 tunnel.

**Recommended Action** Check the configuration, then configure an IKE version 2 transform set that can be used to initiate the tunnel, if necessary.

### 752012

**Error Message** `%ASA-4-752012: IKEv _protocol_ was unsuccessful at setting up a tunnel. Map Tag = _mapTag_ . Map Sequence Number = _mapSeq_ .`

**Explanation** The indicated protocol failed to initiate a tunnel using the configured crypto map.

-   _protocol—_ IKE version number 1 or 2 for IKEv1 or IKEv2
-   _mapTag_ —Name of the crypto map for which the initiation entry was removed
-   _mapSeq_ —Sequence number of the crypto map for which the initiation entry was removed

**Recommended Action** Check the configuration, then debug further within the indicated protocol to determine the cause of the failed tunnel attempt.

### 752013

**Error Message** `%ASA-4-752013: Tunnel Manager dispatching a KEY_ACQUIRE message to IKEv2 after a failed attempt. Map Tag = _mapTag_ . Map Sequence Number = _mapSeq_ .`

**Explanation** The tunnel manager is attempting to initiate the tunnel again after it failed.

-   _mapTag_ —Name of the crypto map for which the initiation entry was removed
-   _mapSeq_ —Sequence number of the crypto map for which the initiation entry was removed

**Recommended Action** Check the configuration, and make sure that the crypto maps are correctly configured. Then determine if the tunnel is successfully created on the second attempt.

### 752014

**Error Message** `%ASA-4-752014: Tunnel Manager dispatching a KEY_ACQUIRE message to IKEv1 after a failed attempt. Map Tag = _mapTag_ . Map Sequence Number = _mapSeq_ .`

**Explanation** The tunnel manager is falling back and attempting to initiate the tunnel using IKE version 1 after the tunnel failed.

-   _mapTag_ —Name of the crypto map for which the initiation entry was removed
-   _mapSeq_ —Sequence number of the crypto map for which the initiation entry was removed

**Recommended Action** Check the configuration, and make sure that the crypto maps are correctly configured. Then determine if the tunnel is successfully created on the second attempt.

### 752015

**Error Message** `%ASA-3-752015: Tunnel Manager has failed to establish an L2L SA. All configured IKE versions failed to establish the tunnel. Map Tag = _mapTag_ . Map Sequence Number = _mapSeq_ .`

**Explanation** An attempt to bring up an L2L tunnel to a peer failed after trying with all configured protocols.

-   _mapTag_ —Name of the crypto map for which the initiation entry was removed
-   _mapSeq_ —Sequence number of the crypto map for which the initiation entry was removed

**Recommended Action** Check the configuration, and make sure that the crypto maps are correctly configured. Debug the individual protocols to isolate the cause of the failure.

### 752016

**Error Message** `%ASA-5-752016: IKEv _protocol_ was successful at setting up a tunnel. Map Tag = _mapTag_ . Map Sequence Number = _mapSeq._`

**Explanation** The indicated protocol (IKE version 1 or IKE version 2) successfully created an L2L tunnel.

-   _protocol—_ IKE version number 1 or 2 for IKEv1 or IKEv2
-   _mapTag_ —Name of the crypto map for which the initiation entry was removed
-   _mapSeq_ —Sequence number of the crypto map for which the initiation entry was removed

**Recommended Action** None required.

### 752017

**Error Message** `%ASA-4-752017: IKEv2 Backup L2L tunnel initiation denied on interface _interface_ matching crypto map _name_, sequence number _number_ . Unsupported configuration.`

**Explanation** The Secure Firewall ASA uses IKEv1 to initiate the connection because IKEv2 does not support the backup L2L feature.

**Recommended Action** None required if IKEv1 is enabled. You must enable IKEv1 to use the backup L2L feature.

### 753001

**Error Message** `%ASA-4-753001: Unexpected IKEv2 packet received from _ip_address_:_port_. Error: _reason_`

**Explanation** This syslog is generated when an IKEv2 packet is received when the cluster is operating in Distributed VPN clustering mode and fails early consistency and/or error checks performed on it in the datapath.

-   _ip\_address_—source IP address from where the packet was received
    
-   _port_—source port from where the packet was received
    
-   _reason_—Reason why the packet is considered invalid. This value could be _Corrupted SPI detected_ or _Expired SPI received_.
    

**Recommended Action** None required if IKEv1 is enabled. You must enable IKEv1 to use the backup L2L feature.

### 767001

**Error Message** `%ASA-6-767001: _Inspect-name_ : Dropping an unsupported IPv6/IP46/IP64 packet from _interface_ :_IP Addr_ to _interface_ :_IP Addr_ (fail-close)`

**Explanation** A fail-close option was set for a service policy, and a particular inspect received an IPv6, IP64, or IP46 packet. Based on the fail-close option setting, this syslog message is generated and the packet is dropped.

**Recommended Action** None required.

### 768001

**Error Message** `%ASA-3-768001: QUOTA: _resource_ utilization is high: requested _req_, current _curr_, warning level _level_`

**Explanation** A system resource allocation level has reached its warning threshold. In the case of a management session, the resource is simultaneous administrative sessions.

-   _resource—_ The name of the system resource; in this case, it is a management session.
-   _req_ —The number requested; for a management session, it is always 1.
-   _curr_ —The current number allocated; equals _level_ for a management session
-   _level_ —The warning threshold, which is 90 percent of the configured limit

**Recommended Action** None required.

### 768002

**Error Message** `%ASA-3-768002: QUOTA: _resource_ quota exceeded: requested _req_, current _curr_, limit _limit_`

**Explanation** A request for a system resource would have exceeded its configured limit and was denied. In the case of a management session, the maximum number of simultaneous administrative sessions on the system has been reached.

-   _resource—_ The name of the system resource; in this case, it is a management session.
-   _req_ —The number requested; for a management session, it is always 1.
-   _curr_ —The current number allocated; equals _level_ for a management session
-   _limit_ —The configured resource limit

**Recommended Action** None required.

### 768003

**Error Message** `%ASA-3-768003: QUOTA: _management_session_ quota exceeded for user _user_name_: current _3_,user limit _3_`

**Explanation** The current management session exceeded the configured limits for the user.

-   _current_ —The current number allocated for management session for the user
-   _limit_ —The configured management session limit. The default value being 15.

**Recommended Action** None required.

### 768004

**Error Message** `%ASA-3-768004: QUOTA: _management_session_ quota exceeded for _ssh/telnet/http_ protocol: current _2_, protocol limit _2_`

**Explanation** The maximum number of management sessions for the protocol - ssh, telnet, or http exceeded the configured limit.

-   _current_ —The current number allocated for a management session
-   _limit_ —The configured resource limit per protocol. The default values being 5.

**Recommended Action** None required.

### 769001

**Error Message** `%ASA-5-769001: UPDATE: _ASA_ image '_src_' was added to system boot list`

**Explanation** The system image has been updated. The name of a file previously downloaded onto the system has been added to the system boot list.

-   _src—_ The name or URL of the source image file

**Recommended Action** None required.

### 769002

**Error Message** `%ASA-5-769002: UPDATE: _ASA_ image '_src_' was copied to '_dest_'`

**Explanation** The system image has been updated. An image file has been copied onto the system.

-   _src—_ The name or URL of the source image file
-   _dest_ —The name of the destination image file

**Recommended Action** None required.

### 769003

**Error Message** `%ASA-5-769003: UPDATE: _ASA_ image '_src_' was renamed to '_dest_'`

**Explanation** The system image has been updated. An existing image file has been renamed to an image file name in the system boot list.

-   _src—_ The name or URL of the source image file
-   _dest_ —The name of the destination image file

**Recommended Action** None required.

### 769004

**Error Message** `%ASA-2-769004: UPDATE: _ASA_ image '_src_file_' failed verification, reason: _failure_reason_`

**Explanation** The image failed verification from either the copy command or verify command.

-   _src\_file —_ The file name or URL of the source image file
-   _failure\_reason_ —The file name of the destination image file

**Recommended Action** Possible failure reasons are: insufficient system memory, no image found in file, checksum failed, signature not found in file, signature invalid, signature algorithm not supported, signature processing issue

### 769005

**Error Message** `%ASA-5-769005: UPDATE: _ASA_ image '_image_name_' passed verification`

**Explanation** This is a notification message indicating that the image passed verification.

-   _image\_name —_ The file name of the Secure Firewall ASA image file

**Recommended Action** None Required.

### 769006

**Error Message** `%ASA-3-769006: UPDATE: _ASA_ boot system image '_image_name_' was not found on disk`

**Explanation** This is an error message indicating that the file configured in the boot system list could not be located on disk.

-   _image\_name —_ The file name of the Secure Firewall ASA image file

**Recommended Action** If the device fails to boot, change the boot system command to point to a valid file or install the missing file to the disk before rebooting the device.

### 769007

**Error Message** `%ASA-6-769007: UPDATE: Image version is _version_number_`

**Explanation** This message appears when the device is upgraded.

-   _version\_number —_ The version number of the Secure Firewall ASA image file

**Recommended Action** None required.

### 769009

**Error Message** `%ASA-4-769009: UPDATE: Image booted _image_name_ is different from boot images`

**Explanation** This is an error message appears after upgrading the device indicating that the file configured is different from the existing list of boot images.

-   _image\_name —_ The file name of the Secure Firewall ASA image file

**Recommended Action** None required.

### 770001

**Error Message** `%ASA-4-770001: _Resource_ resource allocation is more than the permitted limit of _limit_. If this condition persists, the _ASA_ will be rebooted`

**Explanation** The CPU or memory resource allocation for the Secure Firewall ASA virtual machine has exceeded the allowed limit for this platform. This condition does not occur unless the setting for the Secure Firewall ASA virtual machine has been changed from that specified in the software downloaded from Cisco.com.

**Recommended Action** To continue Secure Firewall ASA operation, change the CPU or memory resource allocation of the virtual machine to what was specified with the software downloaded from Cisco.com.or to the resource limits specified in the _Cisco ASA 1000V CLI Configuration Guide_ for this platform.

### 770002

**Error Message** `%ASA-1-770002: _Resource_ resource allocation is more than the permitted limit of _limit_, _Device_ will be rebooted`

**Explanation** The CPU or memory resource allocation for the Secure Firewall ASA virtual machine has exceeded the allowed limit for this platform. This condition does not occur unless the setting for the Secure Firewall ASA virtual machine has been changed from that specified in the software downloaded from Cisco.com. The Secure Firewall ASA will continue to reboot if the resource allocation is not changed.

**Recommended Action** Change the CPU or memory reosurce allocation to the virtual machine to what was specified with the software downloaded from Cisco.com.or to the resource limits specified in the _Cisco ASA 1000V CLI Configuration Guide_ for this platform.

### 770003

**Error Message** `%ASA-4-770003: _Resource_ resource allocation is less than the minimum requirement of _value_.`

**Explanation** The CPU or memory resource allocation to the Secure Firewall ASA virtual machine is less than the minimum requirement for this platform. If this condition persists, performance will be lower than normal.

**Recommended Action** To continue Secure Firewall ASA operation, change the CPU or memory reosurce allocation of the virtual machine to what was specified with the software downloaded from Cisco.

### 771001

**Error Message** `%ASA-5-771001: CLOCK: System clock set, source: _src_, before: _time_, after: _time_`

**Explanation** The system clock was set from a local source.

-   _src—_ The time protocol, which can be any of the following: NTP, SNTP, VINES, or the RFC-868 time protocol
-   _ip_ —The IP address of the time server
-   _time_ —The time string in the form, “Sun Apr 1 12:34:56.789 EDT 2012”

**Recommended Action** None required.

### 771002

**Error Message** `%ASA-5-771002: CLOCK: System clock set, source: _src_, IP: _ip_, before: _time_, after: _time_`

**Explanation** The system clock was set from a remote source.

-   _src—_ The time source, which can be either manual or hardware calendar
-   _ip_ —The IP address of the time server
-   _time_ —The time string in the form, “Sun Apr 1 12:34:56.789 EDT 2012”

**Recommended Action** None required.

### 771003

**Error Message** `%ASA-3-771003: CLOCK: Hardware clock UIP bit is set to 1, for _duration_ secs, start time _duration_ secs, end time _duration_ secs. Read clock time from linux system clock`

**Explanation** Rate-limited.

**Recommended Action** None required.

### 772002

**Error Message** `%ASA-3-772002: PASSWORD: _console_ login warning, user _username_, cause: password expired`

**Explanation** A user logged into the system console with an expired password, which is permitted to avoid system lockout.

-   _username—_ The name of the user
    

**Recommended Action** The user should change the login password.

### 772003

**Error Message** `%ASA-2-772003: PASSWORD: _session_ login failed, user _username_, IP _ip_, cause: password expired`

**Explanation** A user logged tried to log into the system with an expired password and was denied access.

-   _session—_ The session type, which can be SSH or Telnet
-   _username—_ The name of the user
-   _ip_ —The IP address of the user

**Recommended Action** If the user has authorized access, an administrator must change the password for the user. Unauthorized access attempts should trigger an appropriate response, for example. traffic from that IP address can be blocked.

### 772004

**Error Message** `%ASA-3-772004: PASSWORD: _session_ login failed, user _username_, IP _ip_, cause: password expired`

**Explanation** A user logged tried to log into the system with an expired password and was denied access.

-   _session—_ The session type, which is ASDM
-   _username—_ The name of the user
-   _ip_ —The IP address of the user

**Recommended Action** If the user has authorized access, an administrator must change the password for the user. Unauthorized access attempts should trigger an appropriate response, for example. traffic from that IP address can be blocked.

### 772005

**Error Message** `%ASA-6-772005: REAUTH: user '_username_' passed authentication`

**Explanation** The user authenticated successfully after changing the password.

-   _username—_ The name of the user

**Recommended Action** None required.

### 772006

**Error Message** `%ASA-2-772006: REAUTH: user '_username_' failed authentication`

**Explanation** The user entered the wrong password while trying to change it. As a result, the password was not changed.

-   _username—_ The name of the user

**Recommended Action** The user should retry changing the password using the change-password command.

### 774001

**Error Message** `%ASA-2-774001: POST: unspecified error`

**Explanation** The crypto service provider failed the power on self-test.

**Recommended Action** Contact the Cisco TAC.

### 774002

**Error Message** `%ASA-2-774002: POST: error '_err_', func '_func_', engine _eng_, algorithm _alg_, mode _mode_, dir _dir_, key len _len_`

**Explanation** The crypto service provider failed the power on self-test.

-   _err_ —The failure cause
-   _func_ —The function
-   _eng_ —The engine, which can be NPX, Nlite, or software
-   _alg_ —The algorithm, which can be any of the following: RSA, DSA, DES, 3DES, AES, RC4, MD5, SHA1, SHA256, SHA386, SHA512, HMAC-MD5, HMAC-SHA1, HMAC-SHA2, or AES-XCBC
-   _mode_ —The mode, which can be any of the following: none, CBC, CTR, CFB, ECB, stateful-RC4, or stateless-RC4
-   _dir_ —Either encryption or decryption
-   _len_ —The key length in bits

**Recommended Action** Contact the Cisco TAC.

### 775001

**Error Message** `%ASA-6-775001: Scansafe: _protocol_ connection _conn_id_ from _interface_name_:_real_address_/_real_port_ (_idfw_user_) to _interface_name_:_real_address_/_real_port_ redirected to _server_interface_name_:_server_ip_address_`

**Explanation** A ScanSafe server is configured, and traffic matches a policy that has been configured to redirect the connection to the ScanSafe server for content scanning and other malware protection services.

**Recommended Action** None required.

### 775002

**Error Message** `%ASA-4-775002: Scansafe: _Reason_ - _protocol_ connection _conn_id_ from _interface_name_:_real_address_/_real_port_ (_idfw_user_) to _interface_name_:_real_address_/_real_port_ is _action_ locally`

**Explanation** If the source IP address and port of the new ScanSafe redirected connection matches the existing connection, then the ASA drops the new connection and this syslog message is generated.

-   _Reason_ —Duplicate connection with same source _address_ and port _port_

**Recommended Action** Make sure of all of the following:

-   The ScanSafe license key is configured.
-   The public key is configured.
-   The ScanSafe server is reachable by the ASA.
-   The maximum number of connections has not been reached.

| ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)

**Note** | ___

Configuring PAT and ScanSafe on a single connection are not recommended.

___ |
|--------|------------------------------------------------------------------------------|

### 775003

**Error Message** `%ASA-6-775003: Scansafe: _protocol_ connection _conn_id_ from _interface_name_:_real_address_/_real_port_ (_idfw_user_) to _interface_name_:_real_address_/_real_port_ is whitelisted`

**Explanation** The traffic has been matched and does not need to be redirected to the ScanSafe server for content scanning, but can be sent directly to the intended web server.

**Recommended Action** None required.

### 775004

**Error Message** `%ASA-4-775004: Scansafe: Primary server _server-name_:_ip_address_ is unreachable`

**Explanation** The primary ScanSafe server is not reachable on either of the configured HTTP or HTTPS ports.

**Recommended Action** None required.

### 775005

**Error Message** `%ASA-6-775005: Scansafe: Primary server _server-name_:_ip_address_ is now reachable`

**Explanation** The primary ScanSafe server is reachable on both of the configured HTTP and HTTPS ports.

**Recommended Action** None required.

### 775006

**Error Message** `%ASA-6-775006: Scansafe: Reachable backup server _interface_:_ip_address_ is now active`

**Explanation** If the primary ScanSafe server becomes unreachable, the ASA checks the connectivity to the configured backup ScanSafe server; if the backup server is reachable, it becomes the active server.

**Recommended Action** None required.

### 775007

**Error Message** `%ASA-2-775007: Scansafe: No reachable servers found`

**Explanation** Neither the primary nor backup ScanSafe server is reachable. Based on the configured default action( fail\_close or fail\_open), traffic is getting dropped or sent to the web server without being redirected.

**Recommended Action** If both the ScanSafe servers are not reachable, you can change the ScanSafe configuration to fail\_open to send traffic to the web server without having it redirected to the ScanSafe server. This configuration changes the default action to permit.

### 776001

**Error Message** `%ASA-3-776001: CTS SXP: Configured source IP _source ip error_`

**Explanation** An error occurred while using this configured source IP address to set up an SXP connection.

-   _source ip_ —IPv4 or IPv6 source address
-   _error_ —Detailed message regarding what type of error occurs while using the configured address to set up the SXP connection, which can be one of the following:

\- Does not belong to this device.

\- Does not match outbound interface IP address.

**Recommended Action** Reconfigure the SXP connection to have a valid source IP address. Alternatively, unconfigure the source IP address and let the device select the correct source IP address based on a route lookup.

### 776002

**Error Message** `%ASA-3-776002: CTS SXP: Invalid message from peer _peer IP_ : _error_`

**Explanation** An error occurred while parsing an SXP message.

-   _peer IP_ —IPv4 or IPv6 peer address
-   _error_ — Description of message parsing problem

**Recommended Action** Contact the Cisco TAC for assistance.

### 776003

**Error Message** `%ASA-3-776003: CTS SXP: Connection with peer _peer IP_ failed: _error_`

**Explanation** An SXP configuration error occurred. The connection cannot be set up correctly.

-   _peer IP_ —IPv4 or IPv6 peer address
-   _error_ — Description of SXP configuration problem. The error can be one of the following values:

\- Mode mismatch with received one.

\- Does not exist.

\- With the same peer, but different source IP address exists.

\- Version mismatch with received one.

\- Received binding update while in speaker mode.

**Recommended Action** Make sure that the connection configurations on both ends have the correct mode and IP addresses.

### 776004

**Error Message** `%ASA-3-776004: CTS SXP: Fail to start listening socket after TCP process restart.`

**Explanation** The SXP on this device cannot accept SXP connection setup requests from remote devices, because it cannot update the binding manager.

**Recommended Action** Disable and reenable the SXP feature to see if the listening socket can be restarted.

### 776005

**Error Message** `%ASA-3-776005: CTS SXP: Binding _Binding IP - SGname_ (_SGT_ ) from _peer IP_ _instance connection instance_ _num error_ .`

**Explanation** An SXP binding update error has occurred.

-   _Binding IP_ —IPv4 or IPv6 binding address
-   _SGname_ (_SGT_ )—Binding SGT information. Has the following format if SGname is available: _SGname_ (_SGT_ ) and the following format if SGname is unavailable: _SGT_ .
-   _peer IP_ —IPv4 or IPv6 peer address that sent the binding
-   _connection instance num_ —Instance number of the SXP connection from which the binding came
-   _error_ —Detailed message about the binding error

**Recommended Action** Contact the Cisco TAC for assistance.

### 776006

**Error Message** `%ASA-3-776006: CTS SXP: Internal error: _error_`

**Explanation** The CTS SXP system encountered an internal failure.

-   _error_ —Detailed message about the SXP internal error, which can be one of the following:

\- Source IP address of existing SXP connection cannot change.

\- Password type of existing connection cannot change.

\- Connection mode is the same as the existing configuration.

\- IP address does not exist.

**Recommended Action** Contact the Cisco TAC for assistance.

### 776007

**Error Message** `%ASA-3-776007: CTS SXP: Connection with peer _peer IP_ (_instance connection instance num_ ) state changed from _original state_ to Off.`

**Explanation** The CTS SXP system encountered an internal failure, because the SXP connection with the specified instance number changed its state to off.

-   _peer IP_ —IPv4 or IPv6 peer address
-   _connection instance num_ —SXP connection instance number
-   _original state_ —Original connection state

**Recommended Action** None required.

### 776008

**Error Message** `%ASA-6-776008: CTS SXP: Connection with _peer IP_ (instance _connection instance num_ ) state changed from _original state_ to _final state_ .`

**Explanation** The SXP connection with the specified instance number changed state.

-   _peer IP_ —IPv4 or IPv6 peer address
-   _source IP_ —IPv4 or IPv6 source address
-   _connection instance num_ —SXP connection instance number
-   _original state_ —Original connection state
-   _final state_ —Final connection state, which can be any state except the Off state.

**Recommended Action** None required.

### 776009

**Error Message** `%ASA-5-776009: CTS SXP: password changed.`

**Explanation** The SXP system password has been changed.

**Recommended Action** None required.

### 776010

**Error Message** `%ASA-5-776010: CTS SXP: SXP default source IP is changed _original source IP final source IP_ .`

**Explanation** The SXP default source IP address has been changed on this device.

-   _original source_ _IP_ —IPv4 or IPv6 original default source IP address
-   _final source IP_ —IPv4 or IPv6 final default source IP address

**Recommended Action** None required.

### 776011

**Error Message** `%ASA-5-776011: CTS SXP: _operational state_ .`

**Explanation** The SXP feature has changed operational state and works only when the feature is enabled.

-   _operational state_ —Flags the state whether CTS SXP is enabled or disabled.

**Recommended Action** None required.

### 776012

**Error Message** `%ASA-7-776012: CTS SXP: _timer name_ timer started for connection with peer _peer IP_ .`

**Explanation** The specified SXP timer started.

-   _peer IP_ —IPv4 or IPv6 peer address. For timers that are not triggered by connection-based events, that is, the retry open timer, a default IP address of 0.0.0.0 is used.
-   _timer name_ —Timer name

**Recommended Action** None required.

### 776013

**Error Message** `%ASA-7-776013: CTS SXP: _timer name_ timer stopped for connection with peer _peer IP_ .`

**Explanation** The specified SXP timer stopped.

-   _peer IP_ —IPv4 or IPv6 peer address. For timers that are not triggered by connection-based events, that is, the retry open timer, a default IP address of 0.0.0.0 is used.
-   _timer name_ —Timer name

**Recommended Action** None required.

### 776014

**Error Message** `%ASA-7-776014: CTS SXP: SXP received binding forwarding request (_action_ ) binding _binding IP - SGname_ (_SGT_ ).`

**Explanation** The SXP received a binding forwarding request. The request comes from the binding manager when it wants SXP to broadcast the latest net binding changes within the binding manager.

-   _action_ —Add or delete operation
-   _binding IP_ —IPv4 or IPv6 binding address
-   _SGname_ (_SGT_ )—Binding SGT information. Has the following format if SGname is available: _SGname_ (_SGT_ ) and the following format if SGname is unavailable: _SGT_ .

**Recommended Action** None required.

### 776015

**Error Message** `%ASA-7-776015: CTS SXP: Binding _binding IP_ - _SGname_ (_SGT_ ) is forwarded to peer _peer IP_ (instance _connection instance num_ ).`

**Explanation** The SXP forwarded binding to the peer.

-   _binding IP_ —IPv4 or IPv6 binding address
-   _SGname_ (_SGT_ )—Binding SGT information. Has the following format if SGname is available: _SGname_ (_SGT_ ) and the following format if SGname is unavailable: _SGT_ .
-   _peer IP_ —IPv4 or IPv6 peer address
-   _connection instance num_ —SXP connection instance number

**Recommended Action** None required.

### 776016

**Error Message** `%ASA-7-776016: CTS SXP: Binding _binding IP_ - _SGName_ (_SGT_ ) from peer _peer IP_ (instance _binding's connection instance num_ ) changed from old instance: _old instance num_ , old sgt: _old SGName_ (_SGT_ ).`

**Explanation** Binding changed in the SXP database.

-   _binding IP_ —IPv4 or IPv6 binding address
-   _SGname_ (_SGT_ )—Binding SGT information. Has the following format if SGname is available: _SGname_ (_SGT_ ) and the following format if SGname is unavailable: _SGT_ .
-   _peer IP_ —Binding source IPv4 or IPv6 address
-   _binding’s connection instance num_ —SXP connection instance number
-   _old instance num_ —Old connection instance number on which the binding was learned
-   _old SGName_ (_SGT_ )—Binding old SGT information. Has the following format if SGname is available: _SGname_ (_SGT_ ) and the following format if SGname is unavailable: _SGT_ .

**Recommended Action** None required.

### 776017

**Error Message** `%ASA-7-776017: CTS SXP: Binding _binding IP_ - _SGname_ (SGT) from peer _peer IP_ (instance _connection instance num_ ) deleted in SXP database.`

**Explanation** Binding was deleted in the SXP database.

-   _binding IP_ —IPv4 or IPv6 binding address
-   _SGname_ (_SGT_ )—Binding SGT information. Has the following format if SGname is available: _SGname_ (_SGT_ ) and the following format if SGname is unavailable: _SGT_ .
-   _peer IP_ —Binding source IPv4 or IPv6 peer address
-   _connection instance num_ —SXP connection instance number

**Recommended Action** None required.

### 776018

**Error Message** `%ASA-7-776018: CTS SXP: Binding _binding IP_ - _SGname_ (SGT) from peer _peer IP_ (instance _connection instance num_ ) added in SXP database.`

**Explanation** Binding was aded in the SXP database.

-   _binding IP_ —IPv4 or IPv6 binding address
-   _SGname_ (_SGT_ )—Binding SGT information. Has the following format if SGname is available: _SGname_ (_SGT_ ) and the following format if SGname is unavailable: _SGT_ .
-   _peer IP_ —Binding source IPv4 or IPv6 peer address
-   _connection instance num_ —SXP connection instance number

**Recommended Action** None required.

### 776019

**Error Message** `%ASA-7-776019: CTS SXP: Binding _binding IP_ - _SGname_ (_SGT_ ) _action taken_ . Update binding manager.`

**Explanation** The SXP updated the binding manager with the binding change.

-   _binding IP_ —IPv4 or IPv6 binding address
-   _SGname_ (_SGT_ )—Binding SGT information. Has the following format if SGname is available: _SGname_ (_SGT_ ) and the following format if SGname is unavailable: _SGT_ .
-   _action taken_ —Action taken, which can be one of the following: added, deleted, or changed.

**Recommended Action** None required.

### 776020

**Error Message** `%ASA-3-776020: CTS SXP: Unable to locate egress interface to peer _peer IP_ .`

**Explanation** The ASA cannot locate the egress interface to the SXP peer.

-   _binding IP_ —IPv4 or IPv6 address

**Recommended Action** Make sure that the SXP peer is routable from the device.