## Messages 400000 to 409023

This chapter includes messages from 400000 to 409023.

### 4000nn

**Error Message** `%ASA-4-4000nn: IPS:_number string_ from _IP_address_ to _IP_address_ on interface _interface_name_`

**Explanation** Messages 400000 through 400051 are Cisco Intrusion Prevention Service signature messages.

**Recommended Action** See the Cisco Intrusion Prevention Service User Guide on Cisco.com.

Not all signature messages are supported by the ASA in this release. IPS messages all start with 4-4000nn and have the following format:

|     number     | The signature number. For more information, see the Cisco Intrusion Prevention Service User Guide on Cisco.com. |
|----------------|-----------------------------------------------------------------------------------------------------------------|
|     string     |                The signature message—approximately the same as the NetRanger signature message.                 |
|   IP_address   |                           The local to remote address to which the signature applies.                           |
| interface_name |                          The name of the interface on which the signature originated.                           |

For example:

```vbnet
%ASA-4-400013 IPS:2003 ICMP redirect from 10.4.1.2 to 10.2.1.1 on interface dmz
%ASA-4-400032 IPS:4051 UDP Snork attack from 10.1.1.1 to 192.168.1.1 on interface outside
```

The following table lists the supported signature messages.

| Message Number | Signature ID |                Signature Title                 | Signature Type |
|----------------|--------------|------------------------------------------------|----------------|
|     400000     |     1000     |           IP options-Bad Option List           | Informational  |
|     400001     |     1001     |         IP options-Record Packet Route         | Informational  |
|     400002     |     1002     |              IP options-Timestamp              | Informational  |
|     400003     |     1003     |              IP options-Security               | Informational  |
|     400004     |     1004     |         IP options-Loose Source Route          | Informational  |
|     400005     |     1005     |              IP options-SATNET ID              | Informational  |
|     400006     |     1006     |         IP options-Strict Source Route         | Informational  |
|     400007     |     1100     |               IP Fragment Attack               |     Attack     |
|     400008     |     1102     |              IP Impossible Packet              |     Attack     |
|     400009     |     1103     |              IP Fragments Overlap              |     Attack     |
|     400010     |     2000     |                ICMP Echo Reply                 | Informational  |
|     400011     |     2001     |             ICMP Host Unreachable              | Informational  |
|     400012     |     2002     |               ICMP Source Quench               | Informational  |
|     400013     |     2003     |                 ICMP Redirect                  | Informational  |
|     400014     |     2004     |               ICMP Echo Request                | Informational  |
|     400015     |     2005     |       ICMP Time Exceeded for a Datagram        | Informational  |
|     400016     |     2006     |       ICMP Parameter Problem on Datagram       | Informational  |
|     400017     |     2007     |             ICMP Timestamp Request             | Informational  |
|     400018     |     2008     |              ICMP Timestamp Reply              | Informational  |
|     400019     |     2009     |            ICMP Information Request            | Informational  |
|     400020     |     2010     |             ICMP Information Reply             | Informational  |
|     400021     |     2011     |           ICMP Address Mask Request            | Informational  |
|     400022     |     2012     |            ICMP Address Mask Reply             | Informational  |
|     400023     |     2150     |            Fragmented ICMP Traffic             |     Attack     |
|     400024     |     2151     |               Large ICMP Traffic               |     Attack     |
|     400025     |     2154     |              Ping of Death Attack              |     Attack     |
|     400026     |     3040     |                 TCP NULL flags                 |     Attack     |
|     400027     |     3041     |               TCP SYN+FIN flags                |     Attack     |
|     400028     |     3042     |               TCP FIN only flags               |     Attack     |
|     400029     |     3153     |         FTP Improper Address Specified         |     Attack     |
|     400030     |     3154     |          FTP Improper Port Specified           |     Attack     |
|     400031     |     4050     |                UDP Bomb attack                 |     Attack     |
|     400032     |     4051     |                UDP Snork attack                |     Attack     |
|     400033     |     4052     |             UDP Chargen DoS attack             |     Attack     |
|     400034     |     6050     |               DNS HINFO Request                | Informational  |
|     400035     |     6051     |               DNS Zone Transfer                | Informational  |
|     400036     |     6052     |        DNS Zone Transfer from High Port        | Informational  |
|     400037     |     6053     |          DNS Request for All Records           | Informational  |
|     400038     |     6100     |             RPC Port Registration              | Informational  |
|     400039     |     6101     |            RPC Port Unregistration             | Informational  |
|     400040     |     6102     |                    RPC Dump                    | Informational  |
|     400041     |     6103     |              Proxied RPC Request               |     Attack     |
|     400042     |     6150     |   ypserv (YP server daemon) Portmap Request    | Informational  |
|     400043     |     6151     |    ypbind (YP bind daemon) Portmap Request     | Informational  |
|     400044     |     6152     | yppasswdd (YP password daemon) Portmap Request | Informational  |
|     400045     |     6153     |  ypupdated (YP update daemon) Portmap Request  | Informational  |
|     400046     |     6154     |  ypxfrd (YP transfer daemon) Portmap Request   | Informational  |
|     400047     |     6155     |     mountd (mount daemon) Portmap Request      | Informational  |
|     400048     |     6175     | rexd (remote execution daemon) Portmap Request | Informational  |
|     400049     |     6180     |     rexd (remote execution daemon) Attempt     | Informational  |
|     400050     |     6190     |             statd Buffer Overflow              |     Attack     |

### 401001

**Error Message** `%ASA-4-401001: Shuns cleared`

**Explanation** The clear shun command was entered to remove existing shuns from memory. An institution to keep a record of shunning activity was allowed.

**Recommended Action** None required.

### 401002

**Error Message** `%ASA-4-401002: Shun added: _IP_address_ _IP_address_ _port_ _port_`

**Explanation** A shun command was entered, where the first IP address is the shunned host. The other addresses and ports are optional and are used to terminate the connection if available. An institution to keep a record of shunning activity was allowed.

**Recommended Action** None required.

### 401003

**Error Message** `%ASA-4-401003: Shun deleted: _IP_address_`

**Explanation**A single shunned host was removed from the shun database. An institution to keep a record of shunning activity was allowed.

**Recommended Action** None required.

### 401004

**Error Message** `%ASA-4-401004: Shunned packet: _IP_address_ ==> _IP_address_ on interface _interface_name_`

**Explanation**A packet was dropped because the host defined by IP SRC is a host in the shun database. A shunned host cannot pass traffic on the interface on which it is shunned. For example, an external host on the Internet can be shunned on the outside interface. A record of the activity of shunned hosts was provided. This message and message %ASA\-4-401005 can be used to evaluate further risk concerning this host.

**Recommended Action** None required.

### 401005

**Error Message** `%ASA-4-401005: Shun add failed: unable to allocate resources for _IP_address_ _IP_address_ _port_ _port_`

**Explanation** The Secure Firewall ASA is out of memory; a shun cannot be applied.

**Recommended Action** The Cisco IPS should continue to attempt to apply this rule. Try to reclaim memory and reapply a shun manually, or wait for the Cisco IPS to do this.

### 402114

**Error Message** `%ASA-4-402114: IPSEC: Received an _protocol_ packet (SPI= _spi_, sequence number= _seq_num_) from _remote_IP_ to _local_IP_ with an invalid SPI.`

-   _\>protocol—_ IPsec protocol
-   _\>spi—_ IPsec Security Parameter Index
-   seq\_num_\>—_ IPsec sequence number
-   remote\_IP_\>—_ IP address of the remote endpoint of the tunnel
-   _\>username—_ Username associated with the IPsec tunnel
-   local\_IP_\>—_ IP address of the local endpoint of the tunnel

**Explanation**An IPsec packet was received that specifies an SPI that does not exist in the SA database. This may be a temporary condition caused by slight differences in aging of SAs between the IPsec peers, or it may be because the local SAs have been cleared. It may also indicate incorrect packets sent by the IPsec peer, which may be part of an attack. This message is rate limited to no more than one message every five seconds.

**Recommended Action**The peer may not acknowledge that the local SAs have been cleared. If a new connection is established from the local router, the two peers may then reestablish connection successfully. Otherwise, if the problem occurs for more than a brief period, either attempt to establish a new connection or contact the peer administrator.

### 402115

**Error Message** `%ASA-4-402115: IPSEC: Received a packet from _remote_IP_ to _local_IP_ containing _act_prot_ data instead of _exp_prot_ data.`

**Explanation** An IPsec packet was received that is missing the expected ESP header. The peer is sending packets that do not match the negotiated security policy, which may indicate an attack. This message is rate limited to no more than one message every five seconds.

-   remote\_IP_\>—_ IP address of the remote endpoint of the tunnel
-   local\_IP_\>—_ IP address of the local endpoint of the tunnel
-   _\>act\_prot—_ Received IPsec protocol
-   _\>exp\_prot—_ Expected IPsec protocol

**Recommended Action** Contact the administrator of the peer.

### 402116

**Error Message** `%ASA-4-402116: IPSEC: Received an _protocol_ packet (SPI= _spi_, sequence number= _seq_num_) from _remote_ip_ (user= _username_) to _local_ip_. The decapsulated inner packet doesn't match the negotiated policy in the SA. The packet specifies its destination as _pkt_daddr_, its source as _pkt_saddr_, and its protocol as _pkt_prot_. The SA specifies its local proxy as _id_daddr_/_id_dmask_/_id_dprot_/_id_dport_ and its remote_proxy as _id_saddr_/_id_smask_/_id_sprot_/_id_sport_.`

**Explanation**: A decapsulated IPsec packet does not match the negotiated identity. The peer is sending other traffic through this security association, which may be caused by a security association selection error by the peer, or it may be part of an attack. This message is rate limited to no more than one message every five seconds.

-   _\>protocol—_ IPsec protocol
-   _\>spi—_ IPsec Security Parameter Index
-   seq\_num_\>—_ IPsec sequence number
-   remote\_ip_\>—_ IP address of the remote endpoint of the tunnel
-   _\>username—_ Username associated with the IPsec tunnel
-   local\_ip_\>—_ IP address of the local endpoint of the tunnel
-   pkt\_daddr_\>—_ Destination address from the decapsulated packet
-   pkt\_saddr_\>—_ Source address from the decapsulated packet
-   pkt\_prot_\>—_ Transport protocol from the decapsulated packet
-   id\_daddr_\>—_ Local proxy IP address
-   id\_dmask_\>—_ Local proxy IP subnet mask
-   id\_dprot_\>—_ Local proxy transport protocol
-   id\_dport_\>—_ Local proxy port
-   id\_saddr_\>—_ Remote proxy IP address
-   id\_smask_\>—_ Remote proxy IP subnet mask
-   id\_sprot_\>—_ Remote proxy transport protocol
-   id\_sport_\>—_ Remote proxy port

**Recommended Action**Contact the administrator of the peer and compare policy settings.

### 402117

**Error Message** `%ASA-4-402117: IPSEC: Received a non-IPSec packet (protocol= _protocol_) from _remote_IP_ to _local_IP_.`

**Explanation**The received packet matched the crypto map ACL, but it is not IPsec-encapsulated. The IPsec peer is sending unencapsulated packets. This error can occur because of a policy setup error on the peer. For example, the firewall may be configured to only accept encrypted Telnet traffic to the outside interface port 23. If you attempt to use Telnet without IPsec encryption to access the outside interface on port 23, this message appears, but not with Telnet or traffic to the outside interface on ports other than 23. This error can also indicate an attack. This message is not generated except under these conditions (for example, it is not generated for traffic to the Secure Firewall ASA interfaces themselves). See messages 710001, 710002, and 710003, which track TCP and UDP requests. This message is rate limited to no more than one message every five seconds.

-   _\>protocol—_ IPsec protocol
-   remote\_IP_\>—_ IP address of the remote endpoint of the tunnel
-   local\_IP_\>—_ IP address of the local endpoint of the tunnel

**Recommended Action**Contact the administrator of the peer to compare policy settings.

### 402118

**Error Message** `%ASA-4-402118: IPSEC: Received an _protocol_ packet (SPI= _spi_, sequence number= _seq_num_) from _remote_IP_ (user= _username_) to _local_IP_ containing an illegal IP fragment of length _frag_len_ with offset _frag_offset_.`

**Explanation** A decapsulatd IPsec packet included an IP fragment with an offset less than or equal to 128 bytes. The latest version of the security architecture for IP RFC recommends 128 bytes as the minimum IP fragment offset to prevent reassembly attacks. This may be part of an attack. This message is rate limited to no more than one message every five seconds.

-   _\>protocol—_ IPsec protocol
-   _\>spi—_ IPsec Security Parameter Index
-   seq\_num_\>—_ IPsec sequence number
-   remote\_IP_\>—_ IP address of the remote endpoint of the tunnel
-   _\>username—_ Username associated with the IPsec tunnel
-   local\_IP_\>—_ IP address of the local endpoint of the tunnel
-   frag\_len_\>—_ IP fragment length
-   frag\_offset_\>—_ IP fragment offset in bytes

**Recommended Action** Contact the administrator of the remote peer to compare policy settings.

### 402119

**Error Message** `%ASA-4-402119: IPSEC: Received an _protocol_ packet (SPI= _spi_, sequence number= _seq_num_) from _remote_IP_ (user= _username_) to _local_IP_ that failed anti-replay checking.`

**Explanation**An IPsec packet was received with an invalid sequence number. The peer is sending packets including sequence numbers that may have been previously used. This message indicates that an IPsec packet has been received with a sequence number outside of the acceptable window. This packet will be dropped by IPsec as part of a possible attack. This message is rate limited to no more than one message every five seconds.

-   _\>protocol—_ IPsec protocol
-   _\>spi—_ IPsec Security Parameter Index
-   seq\_num_\>—_ IPsec sequence number
-   remote\_IP_\>—_ IP address of the remote endpoint of the tunnel
-   _\>username—_ Username associated with the IPsec tunnel
-   local\_IP_\>—_ IP address of the local endpoint of the tunnel

**Recommended Action**Contact the administrator of the peer.

### 402120

**Error Message** `%ASA-4-402120: IPSEC: Received an _protocol_ packet (SPI= _spi_, sequence number= _seq_num_) from _remote_IP_ (user= _username_) to _local_IP_ that failed authentication.`

**Explanation** An IPsec packet was received and failed authentication. The packet is dropped. The packet may have been corrupted in transit, or the peer may be sending invalid IPsec packets, which may indicate an attack if many of these packets were received from the same peer. This message is rate limited to no more than one message every five seconds.

-   _\>protocol—_ IPsec protocol
-   _\>spi—_ IPsec Security Parameter Index
-   seq\_num_\>—_ IPsec sequence number
-   remote\_IP_\>—_ IP address of the remote endpoint of the tunnel
-   _\>username—_ Username associated with the IPsec tunnel
-   local\_IP_\>—_ IP address of the local endpoint of the tunnel

**Recommended Action** Contact the administrator of the remote peer if many failed packets were received.

### 402121

**Error Message** `%ASA-4-402121: IPSEC: Received an _protocol_ packet (SPI= _spi_, sequence number= _seq_num_) from _peer_addr_ (user= _username_) to _lcl_addr_ that was dropped by IPSec (_drop_reason_).`

**Explanation** An IPsec packet to be decapsulated was received and subsequently dropped by the IPsec subsystem. This may indicate a problem with the Secure Firewall ASA configuration or with the Secure Firewall ASA itself.

-   _\>protocol—_ IPsec protocol
-   _\>spi—_ IPsec Security Parameter Index
-   seq\_num_\>—_ IPsec sequence number
-   peer\_addr_\>—_ IP address of the remote endpoint of the tunnel
-   _\>username—_ Username associated with the IPsec tunnel
-   lcl\_addr_\>—_ IP address of the local endpoint of the tunnel
-   drop\_reason_\>—_ Reason that the packet was dropped

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 402122

**Error Message** `%ASA-4-402122: IPSEC: Received a cleartext packet from _src_addr_ to _dest_addr_ that was to be encapsulated in IPSec that was dropped by IPSec (_drop_reason_).`

**Explanation** A packet to be encapsulated in IPsec was received and subsequently dropped by the IPsec subsystem. This may indicate a problem with the Secure Firewall ASA configuration or with the Secure Firewall ASA itself.

-   _src\_addr_ _\>—_ Source IP address
-   _dest\_addr_ _\>—_ Destination_\>_ IP address
-   drop\_reason_\>—_ Reason that the packet was dropped

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 402123

**Error Message** `%ASA-4-402123: CRYPTO: The _accel_type_ hardware accelerator encountered an error (_eror_type_, code= _error_string_) while executing the command _command_name_ (_command_).`

**Explanation** An error was detected while running a crypto command with a hardware accelerator, which may indicate a problem with the accelerator. This type of error may occur for a variety of reasons, and this message supplements the crypto accelerator counters to help determine the cause.

-   accel\_type—Hardware accelerator type
-   _\>error\_string—_ Code indicating the type of error
-   command—Crypto command that generated the error

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 402124

**Error Message-1** `%ASA-4-402124: CRYPTO: The _platform_ hardware accelerator encountered an error (HWErrAddr= 0x_error_address_, Core= _error_core_, HwErrCode= _error_code_, IstatReg= 0x_Istat_, PciErrReg= 0x_PCI_, CoreErrStat= 0x_core_error_stat_, CoreErrAddr= 0x_core_err_address_, Doorbell Size[0]= _size_, DoorBell Outstanding[0]= _outstanding_, Doorbell Size[1]= _size_, DoorBell Outstanding[1]= _outstanding_, SWReset= _Reset_code_)`

**Error Message-2** `%ASA-4-402124: CRYPTO: The _platform_ hardware accelerator encountered an error (HWErrAddr= 0x_error_address_, Core= _error_core_, HwErrCode= _error_code_, Queue= _queue_string_ (_0_), IstatReg= 0x_Istat_, Station= _core_station_, CoreRptr= 0x_core_pointer_, CoreConfig= 0x_core_config_pointer_, SWReset= _Reset_code_)`

**Explanation** The crypto hardware chip has reported a fatal error, indicating that the chip is inoperable. The information from this message captures the details to allow further analysis of the problem. The crypto chip is reset when this condition is detected to unobtrusively allow the Secure Firewall ASA to continue functioning. Also, the crypto environment at the time this issue is detected is written to a crypto archive directory on flash to provide further debugging information. Various parameters related to the crypto hardware are included in this message, as follows:

-   HWErrAddr_\>—_ Hardware address (set by crypto chip)
-   Core_\>—_ Crypto core experiencing the error
-   HwErrCode_\>—_ Hardware error code (set by crypto chip)
-   IstatReg_\>—_ Interrupt status register (set by crypto chip)
-   PciErrReg_\>—_ PCI error register (set by crypto chip)
-   CoreErrStat_\>—_ Core error status (set by crypto chip)
-   CoreErrAddr_\>—_ Core error address (set by crypto chip)
-   Doorbell Size_\>—_ Maximum crypto commands allowed
-   DoorBell Outstanding_\>—_ Crypto commands outstanding
-   SWReset_\>—_ Number of crypto chip resets since boot

| ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)

**Note** | ___

The %ASA-vpn-4-402124: CRYPTO: The ASA hardware accelerator encountered an error (HWErrAddr= 0x40EE9800, Core= 0, HwErrCode= 23, IstatReg= 0x8, PciErrReg= 0x0, CoreErrStat= 0x41, CoreErrAddr= 0x844E9800, Doorbell Size[0]= 2048, DoorBell Outstanding[0]= 0, Doorbell Size[1]= 0, DoorBell Outstanding[1]= 0, SWReset= 99) error message indicates a AnyConnect problem and the workaround for this to upgrade to AnyConnect 3.1.x.

___ |
|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

**Recommended Action** Forward the message information to the Cisco TAC for further analysis.

### 402125

**Error Message-1** `%ASA-4-402125: CRYPTO: The _platform_ hardware accelerator _ring_string_ ring timed out (Desc= 0x_descriptor_address_, CtrlStat= 0x_control_or_status value_, ResultP= 0x_success_pointer_, ResultVal= _success_value_, Cmd= 0x_crypto_command_, CmdSize= _command_size_, Param= 0x_command_parameters_, Dlen= _Data_length_, DataP= 0x_Data_pointer_, CtxtP= 0x_VPN_context_pointer_, SWReset= _reset_number_)`

**Explanation** The crypto driver has detected that either the IPSEC descriptor ring or SSL/Admin descriptor ring is no longer progressing, meaning the crypto chip no longer appears to be functioning. The crypto chip is reset when this condition is detected to unobtrusively allow the Secure Firewall ASA to continue functioning. Also, the crypto environment at the time this issue was detected was written to a crypto archive directory on flash to provide further debugging information.

-   _\>ring—_ IPSEC or Admin ring
-   _parameters_ _\>—_ Include the following:

\- Desc_\>—_ Descriptor address

\- CtrlStat_\>—_ Control/status value

\- ResultP_\>—_ Success pointer

\- ResultVal_\>—_ Success value

\- Cmd_\>—_ Crypto command

\- CmdSize_\>—_ Command size

\- Param_\>—_ Command parameters

\- Dlen_\>—_ Data length

\- DataP_\>—_ Data pointer

\- CtxtP_\>—_ VPN context pointer

\- SWReset_\>—_ Number of crypto chip resets since boot

**Recommended Action** Forward the message information to the Cisco TAC for further analysis.

### 402126

**Error Message** `%ASA-4-402126: CRYPTO: The _platform_ created Crypto Archive File <_Archive_Filename_> as a Soft Reset was necessary. Please forward this archived information to _Cisco_`

**Explanation** A functional problem with the hardware crypto chip was detected (see syslog messages 402124 and 402125). To further debug the crypto problem, a crypto archive file was generated that included the current crypto hardware environment (hardware registers and crypto description entries). At boot time, a crypto\_archive directory was automatically created on the flash file system (if it did not exist previously). A maximum of two crypto archive files are allowed to exist in this directory.

-   _\>Archive Filename—_ The name of the crypto archive file name. The crypto archive file names are of the form, crypto\_arch\_x.bin, where x = (1 or 2).

**Recommended Action** Forward the crypto archive files to the Cisco TAC for further analysis.

### 402127

**Error Message** `%ASA-4-402127: CRYPTO: The _platform_ is skipping the writing of latest Crypto Archive File as the maximum # of files ( _max_number_ ) allowed have been written to <_archive_directory_>. Please archive remove files from < _Archive Directory_ > if you want more Crypto Archive Files saved`

**Explanation** A functional problem with the hardware crypto chip was detected (see messages 4402124 and 4402125). This message indicates a crypto archive file was not written, because the maximum number of crypto archive files already existed.

-   _max\_number_ _\>—_ Maximum number of files allowed in the archive directory; currently set to two
-   _\>archive\_directory—_ Name of the archive directory

**Recommended Action** Forward previously generated crypto archive files to the Cisco TAC. Remove the previously generated archive file(s) so that more can be written (if deemed necessary).

### 402128

**Error Message** `%ASA-5-402128: CRYPTO: An attempt to allocate a large memory block failed, size: _size_, limit: _limit_.`

**Explanation** An SSL connection is attempting to use more memory than allowed. The request has been denied.

-   _size_ —The size of the memory block being allocated
-   _limit_ —The maximum size of allocated memory permitted

**Recommended Action** If this message persists, an SSL denial of service attack may be in progress. Contact the remote peer administrator or upstream provider.

### 402129

**Error Message** `%ASA-6-402129: CRYPTO: An attempt to release a DMA memory block failed, location: _address_.`

**Explanation** An internal software error has occurred.

-   _address_ —The address being freed

**Recommended Action** Contact the Cisco TAC for assistance.

### 402130

**Error Message** `%ASA-6-402130: CRYPTO: Received an ESP packet (SPI = xxxxxxxxxx, sequence number=xxxx) from 172.16.0.1 (user=user) to 192.168.0.2 with incorrect IPsec padding.`

**Explanation** The Secure Firewall ASA crypto hardware accelerator detected an IPsec packet with invalid padding. The ATT VPN client sometimes pads IPsec packets incorrectly.

-   _SPI_ —The SPI associated with the packet
    
-   _sequence number_ —The sequence number associated with the packet
    
-   _user_ —Username string
    
-   _padding_ —Padding data from the packet
    

**Recommended Action** While this message is None required and does not indicate a problem with the Secure Firewall ASA, customers using the ATT VPN client may wish to upgrade their VPN client software.

### 402131

**Error Message** `%ASA-4-402131: CRYPTO: _status_ changing the _accel_instance_ hardware accelerator's configuration bias from _old_config_bias_ to _new_config_bias_.`

**Explanation** The hardware accelerator configuration has been changed on the Secure Firewall ASA. Some Secure Firewall ASA platforms have multiple hardware accelerators. One syslog message is generated for each hardware accelerator change.

-   _status_ —Indicates success or failure
-   _accel\_instance_ —The instance of the hardware accelerator
-   _old\_config\_bias_ —The old configuration
-   _new\_config\_bias_ —The new configuration

**Recommended Action** If any of the accelerators fails when attempting to change its configuration, collect logging information and contact the Cisco TAC. If a failure occurs, the software will retry the configuration change multiple times. The software will fall back to the original configuration bias if the retry attempts fail. If multiple attempts to reconfigure the hardware accelerator fail, it may indicate a hardware failure.

### 402140

**Error Message** `%ASA-3-402140: CRYPTO: _RSA_ key generation error: modulus len _len_`

**Explanation** An error occurred during an RSA public key pair generation.

-   _len_ —The prime modulus length in bits

**Recommended Action** Contact the Cisco TAC for assistance.

### 402141

**Error Message** `%ASA-3-402141: CRYPTO: Key zeroization error: key set '_type_', reason '_reason_'`

**Explanation** An error occurred during an RSA public key pair generation.

-   _type_ —The key set type, which can be any of the following: DH, RSA, DSA, or unknown
-   _reason_ —The unexpected crypto session type

**Recommended Action** Contact the Cisco TAC for assistance.

### 402142

**Error Message** `%ASA-3-402142: CRYPTO: Bulk data _op_ error: algorithm '_alg_', mode '_mode_'`

**Explanation** An error occurred during a symmetric key operation.

-   _op_ —The operation, which can be either encryption or decryption
-   _alg_ —The encryption algorithm, which can be any of the following: DES, 3DES, AES, or RC4
-   _mode_ —The mode, which can be any of the following: CBC, CTR, CFB, ECB, stateful-RC4, or stateless-RC4

**Recommended Action** Contact the Cisco TAC for assistance.

### 402143

**Error Message** `%ASA-3-402143: CRYPTO: _alg_ _type_ key _op_ error`

**Explanation** An error occurred during an asymmetric key operation.

-   _alg_ —The encryption algorithm, which can be either RSA or DSA
-   _type_ —The key type, which can be either public or private
-   _op_ —The operation, which can be either encryption or decryption

**Recommended Action** Contact the Cisco TAC for assistance.

### 402144

**Error Message** `%ASA-3-402144: CRYPTO: Digital signature error: signature algorithm '_sig_', hash algorithm '_hash_'`

**Explanation** An error occurred during digital signature generation.

-   _sig_ —The signature algorithm, which can be either RSA or DSA
-   _hash_ —The hash algorithm, which can be any of the following: MD5, SHA1, SHA256, SHA384, or SHA512

**Recommended Action** Contact the Cisco TAC for assistance.

### 402145

**Error Message** `%ASA-3-402145: CRYPTO: Hash generation error: algorithm '_hash_'`

**Explanation** A hash generation error occurred.

-   _hash_ —The hash algorithm, which can be any of the following: MD5, SHA1, SHA256, SHA384, or SHA512

**Recommended Action** Contact the Cisco TAC for assistance.

### 402146

**Error Message** `%ASA-3-402146: CRYPTO: Keyed hash generation error: algorithm '_hash_', key len _len_`

**Explanation** A keyed hash generation error occurred.

-   _hash_ —The hash algorithm, which can be any of the following: MD5, SHA1, SHA256, SHA384, or SHA512
-   _len_ —The key length in bits

**Recommended Action** Contact the Cisco TAC for assistance.

### 402147

**Error Message** `%ASA-3-402147: CRYPTO: HMAC generation error: algorithm '_alg_'`

**Explanation** An HMAC generation error occurred.

-   _alg_ —The HMAC algorithm, which can be any of the following: HMAC-MD5, HMAC-SHA1, HMAC-SHA2, or AES-XCBC

**Recommended Action** Contact the Cisco TAC for assistance.

### 402148

**Error Message** `%ASA-3-402148: CRYPTO: Random Number Generator error`

**Explanation** A random number generator error occurred.

**Recommended Action** Contact the Cisco TAC for assistance.

### 402149

**Error Message** `%ASA-3-402149: CRYPTO: Weak _encryption_type_ (_length_) provided. Operation disallowed. Not FIPS 140-2 compliant`

**Explanation** The Secure Firewall ASA tried to use an RSA key that is less than 2048 bits or DH groups 1, 2, or 5.

-   _encryption type_ —The encryption type
-   _length_ —The RSA key length or DH group number

**Recommended Action** Configure the Secure Firewall ASA or external application to use an RSA key that is at least 2048 bits, or to configure a DH group that is not 1, 2, or 5.

### 402150

**Error Message** `%ASA-3-402150: CRYPTO: Deprecated hash algorithm used for RSA _operation_ (_hash_alg_). Operation disallowed. Not FIPS 140-2 compliant`

**Explanation** An unacceptable hashing algorithm has been used for digital certificate signing or verification for FIPS 140-2 certification.

-   _operation_ —Sign or verify
-   _hash alg_ —The name of the unacceptable hashing algorithm

**Recommended Action** Make sure that you use the minimum acceptable hashing algorithm for digital certificate signing or verification for FIPS 140-2 certification. These include SHA-256, SHA-384, and SHA-512.

### 403101

**Error Message** `%ASA-4-403101: PPTP session state not established, but received an XGRE packet, tunnel_id=_number_, session_id=_number_`

**Explanation** The ASA received a PPTP XGRE packet without a corresponding control connection session.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 403102

**Error Message** `%ASA-4-403102: PPP virtual interface _interface_name_ rcvd pkt with invalid protocol: _protocol_, reason: _reason_`

**Explanation** The module received an XGRE encapsulated PPP packet with an invalid protocol field.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 403103

**Error Message** `%ASA-4-403103: PPP virtual interface max connections reached`

**Explanation** The module cannot accept additional PPTP connections.Connections are allocated as soon as they are available.

**Recommended Action** None required.

### 403104

**Error Message** `%ASA-4-403104: PPP virtual interface _interface_name_ requires mschap for MPPE`

**Explanation** The MPPE was configured, but MS-CHAP authentication was not.

**Recommended Action** Add MS-CHAP authentication with the vpdn group group\_name ppp authentication command.

### 403106

**Error Message** `%ASA-4-403106: PPP virtual interface _interface_name_ requires RADIUS aaa server for MPPE`

**Explanation** The MPPE was configured, but RADIUS authentication was not.

**Recommended Action** Add RADIUS authentication with the vpdn group group\_name ppp authentication command.

### 403107

**Error Message** `%ASA-4-403107: PPP virtual interface _interface_name_ missing aaa server group info`

**Explanation** The AAA server configuration information cannot be found.

**Recommended Action** Add the AAA server information with the vpdn group group\_name client authentication aaa aaa\_server\_group command.

### 403108

**Error Message** `%ASA-4-403108: PPP virtual interface _interface_name_ missing client ip address option`

**Explanation** The client IP address pool information is missing.

**Recommended Action** Add IP address pool information with the vpdn group group\_name client configuration address local address\_pool\_name command.

### 403109

**Error Message** `%ASA-4-403109: Rec'd packet not a PPTP packet. (ip) dest_addr= _ip_, src_addr= _dest_address_, data: _source_address_`

**Explanation** The module received a spoofed PPTP packet, which may indicate a hostile event.

**Recommended Action** Contact the administrator of the peer to check the PPTP configuration settings.

### 403110

**Error Message** `%ASA-4-403110: PPP virtual interface _interface_name_, user: _user_ missing MPPE key from aaa server`

**Explanation** The AAA server was not returning the MPPE key attributes required to set up the MPPE encryption policy.

**Recommended Action** Check the AAA server configuration. If the AAA server cannot return MPPE key attributes, use local authentication instead by entering the vpdn group group\_name client authentication local command.

### 403500

**Error Message** `%ASA-6-403500: PPPoE - Service name 'any' not received in _interface_name_. AC:_ac_name_.`

**Explanation** The Secure Firewall ASA requested the PPPoE service _any_ from the access controller at the Internet service provider. The response from the service provider includes other services, but does not include the service _any_ . This is a discrepancy in the implementation of the protocol. The PADO packet is processed normally, and connection negotiations continue.

**Recommended Action** None required.

### 403501

**Error Message** `%ASA-3-403501: PPPoE - Bad host-unique in PADO - packet dropped. AC:_interface_name_.`

**Explanation** The Secure Firewall ASA sent an identifier called the host-unique value to the access controller. The access controller responded with a different host-unique value. The Secure Firewall ASA was unable to identify the corresponding connection request for this response. The packet was dropped, and connection negotiations were discontinued.

**Recommended Action** Contact the Internet service provider. Either the access controller at the service provider is mishandling the host-unique value, or the PADO packet is being forged.

### 403502

**Error Message** `%ASA-3-403502: PPPoE - Bad host-unique in PADS - packet dropped. AC:_interface_name_.`

**Explanation** The Secure Firewall ASA sent an identifier called the host-unique value to the access controller. The access controller responded with a different host-unique value. The Secure Firewall ASA was unable to identify the corresponding connection request for this response. The packet was dropped, and connection negotiations were discontinued.

**Recommended Action** Contact the Internet service provider. Either the access controller at the service provider is mishandling the host-unique value, or the PADO packet is being forged.

### 403503

**Error Message** `%ASA-3-403503: _Header_string_:PPP link down[:_reason string_]`

**Explanation** The PPP link has gone down. There are many reasons why this can happen. The first format will display a reason if PPP provides one.

**Recommended Action** Check the network link to ensure that the link is connected. The access concentrator may be down. Make sure that your authentication protocol matches the access concentrator and that your name and password are correct. Verify this information with your ISP or network support person.

### 403504

**Error Message** `%ASA-3-403504: _group_name_:No 'vpdn group' for PPPoE has been created!`

**Explanation** PPPoE requires a dial-out configuration before starting a PPPoE session. In general, the configuration should specify a dialing policy, the PPP authentication, the username, and a password. The following example configures the Secure Firewall ASA for PPPoE dialout. The my-username and my-password commands are used to authenticate the access concentrator, using PAP if necessary.

For example:

```graphql
ciscoasa# vpdn group my-pppoe request dialout pppoe
ciscoasa# vpdn group my-pppoe ppp authentication pap
ciscoasa# vpdn group my-pppoe localname my-username
ciscoasa# vpdn username my-username password my-password
ciscoasa# ip address outside pppoe setroute
```

**Recommended Action** Configure a VPDN group for PPPoE.

### 403505

**Error Message** `%ASA-4-403505: _PPPoE_:PPP - Unable to set default route to _IP_address_ at _interface_name_. _interface_`

**Explanation** This message is usually followed by the message, default route already exists.

**Recommended Action** Remove the current default route or remove the _setroute_ parameter so that there is no conflict between PPPoE and the manually configured route.

### 403506

**Error Message** `%ASA-4-403506: _PPPoE_: failed to assign PPP address _IP_address_ netmask _netmask_ at _interface_ _interface_name_`

**Explanation** This message is followed by one of the followings messages: subnet is the same as interface, or on failover channel.

**Recommended Action** In the first case, change the address causing the conflict. In the second case, configure the PPPoE on an interface other than the failover interface.

### 403507

**Error Message** `%ASA-3-403507: _PPPoE_:PPPoE client on interface _interface_ failed to locate PPPoE vpdn group _group_name_`

**Explanation** You can configure the PPPoE client on an interface to use a particular VPDN group by entering the pppoe client vpdn group group\_name command. If a PPPoE VPDN group of the configured name was not located during system startup, this message is generated.

-   _interface_ —The interface on which the PPPoE client failed
-   _group\_name_ —The VPDN group name of the PPPoe client on the interface

**Recommended Action** Perform the following steps:

1.  Add the required VPDN group by entering the vpdn group group\_name command. Request dialout PPPoE in global configuration mode, and add all the group properties.
2.  Remove the pppoe client vpdn group _group\_name_ command from the interface indicated. In this case, the PPPoE client will attempt to use the first PPPoE VPDN group defined.

| ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)

**Note** | ___

All changes take effect only after the PPPoE client on the interface is restarted by entering the ip address pppoe command.

___ |
|--------|---------------------------------------------------------------------------------------------------------------------------------|

### 405001

**Error Message** `%ASA-4-405001: Received ARP _{request | response}_ collision from _ip_address_/_MAC_address_ on interface _interface_name_ with existing ARP entry _ip_address_/_MAC_address_`

**Explanation** The Secure Firewall ASA received an ARP packet, and the MAC address in the packet differs from the ARP cache entry.

**Recommended Action** This traffic might be legitimate, or it might indicate that an ARP poisoning attack is in progress. Check the source MAC address to determine where the packets are coming from and to see if they belong to a valid host.

### 405002

**Error Message** `%ASA-4-405002: Received mac mismatch packet from _IP_address_/{_MAC_bytes|MAC_address_} for authenticated host`

**Explanation** This packet appears for one of the following conditions:

-   The Secure Firewall ASA received a packet with the same IP address, but a different MAC address from one of its uauth entries.
-   You configured the vpnclient mac-exempt command on the Secure Firewall ASA, and the Secure Firewall ASA received a packet with an exempt MAC address, but a different IP address from the corresponding uauth entry.

**Recommended Action** This traffic might be legitimate, or it might indicate that a spoofing attack is in progress. Check the source MAC address and IP address to determine where the packets are coming from and if they belong to a valid host.

### 405003

**Error Message** `%ASA-4-405003: IP address collision detected between host _ip_address_ at _MAC_address_ and interface _interface_name_, _MAC_address_`

**Explanation** A client IP address in the network is the same as the Secure Firewall ASA interface IP address.

**Recommended Action** Change the IP address of the client.

### 405101

**Error Message-1** `%ASA-4-405101: Unable to Pre-allocate H225 Call Signalling Connection for faddr _foreign_ip_address_ to laddr _local_ip_address_/_local_port_`

**Error Message-2** `%ASA-4-405101: Unable to Pre-allocate H225 Call Signalling Connection for faddr _foreign_ip_address_/_foreign_port_ to laddr _local_ip_address_`

**Explanation** The module failed to allocate RAM system memory while starting a connection or has no more address translation slots available.

**Recommended Action** If this message occurs periodically, it can be ignored. You can check the size of the global pool compared to the number of inside network clients. A PAT address may be necessary. Alternatively, shorten the timeout interval of translates and connections. This error message may also be caused by insufficient memory; try reducing the amount of memory usage, or purchasing additional memory. If the problem persists, contact the Cisco TAC.

### 405102

**Error Message-1** `%ASA-4-405102: Unable to Pre-allocate H245 Connection for faddr _foreign_ip_address_ to laddr _local_ip_address_/_local_port_`

**Error Message-2** `%ASA-4-405102: Unable to Pre-allocate H245 Connection for faddr _foreign_ip_address_/_foreign_port_ to laddr _local_ip_address_`

**Explanation** The Secure Firewall ASA failed to allocate RAM system memory while starting a connection or has no more address translation slots available.

**Recommended Action** Check the size of the global pool compared to the number of inside network clients. A PAT address may be necessary. Alternatively, shorten the timeout interval of translations and connections. In addition, reduce the amount of memory usage, or purchase additional memory. If this message occurs periodically, it can be ignored. If the problem persists, contact the Cisco TAC.

### 405103

**Error Message** `%ASA-4-405103: H225 message from _source_address_/_source_port_ to _dest_address_/_dest_port_ contains bad protocol discriminator _hex_`

**Explanation** The Secure Firewall ASA is expecting the protocol discriminator, 0x08, but it received something other than 0x08. The endpoint may be sending a bad packet, or received a message segment other than the first segment. The packet is allowed through.

**Recommended Action** None required.

### 405104

**Error Message** `%ASA-4-405104: H225 message _string_ received from _outside_address_/_outside_port_ to _inside_address_/_inside_port_ before SETUP`

**Explanation** An H.225 message was received out of order, before the initial SETUP message, which is not allowed. The Secure Firewall ASA must receive an initial SETUP message for that H.225 call signalling channel before accepting any other H.225 messages.

**Recommended Action** None required.

### 405105

**Error Message** `%ASA-4-405105: H323 RAS message AdmissionConfirm received from _source_address_/_source_port_ to _dest_address_/_dest_port_ without an AdmissionRequest`

**Explanation** A gatekeeper has sent an ACF, but the Secure Firewall ASA did not send an ARQ to the gatekeeper.

**Recommended Action** Check the gatekeeper with the specified source\_address to determine why it sent an ACF without receiving an ARQ from the Secure Firewall ASA.

### 405106

**Error Message** `%ASA-4-405106: H323 _num_ channel is not created from %I/%d to %I/%d %s`

**Explanation** The ASA tried to create a match condition on the H.323 media-type channel. See the match media-type command for more information.

**Recommended Action** None required.

### 405107

**Error Message** `%ASA-4-405107: H245 Tunnel is detected and connection dropped from %I/%d to %I/%d %s`

**Explanation** An H.323 connection has been dropped because of an attempted H.245 tunnel control during call setup. See the h245-tunnel-block command for more information.

**Recommended Action** None required.

### 405201

**Error Message** `%ASA-4-405201: ILS _ILS_message_type_ from _inside_interface_:_source_IP_address_/_port_ to _outside_interface_:_destination_IP_address_/_port_ has wrong embedded address _embedded_IP_address_`

**Explanation** The embedded address in the ILS packet payload was not the same as the source IP address of the IP packet header.

**Recommended Action** Check the host specified with the source\_IP\_address to determine why it sent an ILS packet with an incorrect embedded IP address.

### 405300

**Error Message** `%ASA-4-405300: Radius Accounting Request received from _from_addr_ is not allowed`

**Explanation** The accounting request came from a host that was not configured in the policy map. The message is logged and processing stops.

-   _from\_addr_ —The IP address of the host sending the request

**Recommended Action** If the host was configured to send RADIUS accounting messages to the ASA, make sure that it was configured in the correct policy map that was applied to the service policy. If the host was not configured to send RADIUS accounting messages to the ASA, then check to see why the messages are being sent. If the messages are illegitimate, then create the proper ACLs to drop the packets.

### 405301

**Error Message** `%ASA-4-405301: Attribute _attribute_number_ does not match for user _user_ip_`

**Explanation** When the validate-attribute command was entered, the attribute values stored in the accounting request start received do not match those stored in the entry, if it exists.

-   _attribute\_number_ —The RADIUS attribute to be validated with RADIUS accounting. Values range from 1 to 191. Vendor-specific attributes are not supported.
-   _user\_ip_ —The IP address (framed IP attribute) of the user.

**Recommended Action** None required.

### 406001

**Error Message** `%ASA-4-406001: FTP port command low port: _IP_address_/_port_ to _IP_address_ on interface _interface_name_`

**Explanation** A client entered an FTP port command and supplied a port less than 1024 (in the well-known port range usually devoted to server ports). This is indicative of an attempt to avert the site security policy. The Secure Firewall ASA drops the packet, terminates the connection, and logs the event.

**Recommended Action** None required.

### 406002

**Error Message** `%ASA-4-406002: FTP port command different address: _IP_address_(_IP_address_) to _IP_address_ on interface _interface_name_`

**Explanation** A client entered an FTP port command and supplied an address other than the address used in the connection. An attempt to avert the site security policy occurred. For example, an attacker might attempt to hijack an FTP session by changing the packet on the way, and putting different source information instead of the correct source information. The Secure Firewall ASA drops the packet, terminates the connection, and logs the event. The address in parentheses is the address from the port command.

**Recommended Action** None required.

### 407001

**Error Message** `%ASA-4-407001: Deny traffic for local-host _interface_name_:_inside_address_, license limit of _number_ exceeded`

**Explanation** The host limit was exceeded. An inside host is counted toward the limit when one of the following conditions is true:

-   The inside host has forwarded traffic through the Secure Firewall ASA within the last five minutes.
-   The inside host has reserved an xlate connection or user authentication at the Secure Firewall ASA.

**Recommended Action** The host limit is enforced on the low-end platforms. Use the show version command to view the host limit. Use the show local-host command to view the current active hosts and the inside users that have sessions at the Secure Firewall ASA. To forcefully disconnect one or more users, use the clear local-host command. To expire the inside users more quickly from the limit, set the xlate, connection, and uauth timeouts to the recommended values or lower as given in the table below:

| Timeout |    Recommended Value    |
|---------|-------------------------|
|  xlate  | 00:05:00 (five minutes) |
|  conn   |   00:01:00 (one hour)   |
|  uauth  | 00:05:00 (five minutes) |

### 407002

**Error Message** `%ASA-4-407002: Embryonic limit for through connections exceeded _nconns_/_elimit_. _outside_address_/_outside_port_ to _global_address_(_inside_address_)/_inside_port_ on interface _interface_name_`

**Explanation** The number of connections from a specified foreign address over a specified global address to the specified local address exceeded the maximum embryonic limit for that static. The Secure Firewall ASA tries to accept the connection if it can allocate memory for that connection. It proxies on behalf of the local host and sends a SYN\_ACK packet to the foreign host. The Secure Firewall ASA retains pertinent state information, drops the packet, and waits for the acknowledgment from the client. The message might indicate legitimate traffic or that a DoS attack is in progress.

**Recommended Action** Check the source address to determine where the packets are coming from and whether or not a valid host is sending them.

### 407003

**Error Message** `%ASA-4-407003: Established limit for RPC services exceeded`

**Explanation** The Secure Firewall ASA tried to open a new hole for a pair of RPC servers or services that have already been configured after the maximum number of holes has been met.

**Recommended Action** Wait for other holes to be closed (through associated timeout expiration), or limit the number of active pairs of servers or services.

### 408001

**Error Message** `%ASA-4-408001: IP route counter negative`

**Explanation** An attempt to decrement the IP route counter into a negative value failed.

**Recommended Action** Enter the clear ip route command to reset the route counter. If the problem persists, contact the Cisco TAC.

### 408101

**Error Message** `%ASA-4-408101: KEYMAN : Type _encrption_type_ encryption unknown. Interpreting keystring as literal.`

**Explanation** The format type was not recognized by the system. A keystring format type value of 0 (unencrypted keystring) or 7 (hidden keystring), followed by a space, can precede the actual keystring to indicate its format. An unknown type value will be accepted, but the system will consider the keystring as being unencrypted.

**Recommended Action** Use the correct format for the value type or remove the space following the value type.

### 408102

**Error Message** `%ASA-4-408102: KEYMAN : Bad encrypted keystring for key id _key_id_.`

**Explanation** The system could not successfully decrypt an encrypted keystring. The keystring may have been corrupted during system configuration.

**Recommended Action** Re-enter the key-string command, and reconfigure the key string.

### 409014

**Error Message** `%ASA-4-409014: No valid authentication _send_ key is available on interface _nameif_.`

**Explanation** The authentication key configured on the interface is not valid.

**Recommended Action** Configure a new key.

### 409015

**Error Message** `%ASA-4-409015: Key ID _key-id_ _received_ on interface _nameif_.`

**Explanation** The ID is not found in the configured key chain.

**Recommended Action** Configure a new security association with the Key ID.

### 409016

**Error Message** `%ASA-4-409016: Key chain name _key-chain-name_ on _nameif_ is invalid.`

**Explanation** The key-chain name configured under OSPF interface does not match global key chain configuration.

**Recommended Action**Fix configuration. Either remove OSPF authentication command or configure key chain in global configuration mode.

### 409017

**Error Message** `%ASA-4-409017: Key ID _key-id_ in key chain _key-chain-name_ is invalid.`

**Explanation** The Key ID configured in the key chain is out of range for OSPF. This may happen because the key chain allows Key ID values of the range which is not acceptable for OSPF.

**Recommended Action** Configure a new security association with a Key ID that is in the range 1-255.

### 409023

**Error Message** `%ASA-4-409023: Attempting AAA Fallback method _method_name_ for _request_type_ request for user _user_ : Auth-server group _Auth-server_ unreachable`

**Explanation** An authentication or authorization attempt to an external server has failed and will be performed using the local user database.

-   aaa\_operation—Either authentication or authorization
-   username—The user associated with the connection
-   server\_group—The name of the AAA server whose servers were unreachable

**Recommended Action** Investigate any connectivity problems with the AAA servers configured in the first method. Ping the authentication servers from the Secure Firewall ASA. Make sure that the daemons are running on the AAA server.

## Messages 410001 to 450002

This chapter includes messages from 410001 to 450002.

### 410001

**Error Message** `%ASA-4-410001: Dropped UDP DNS _request_ from _source_interface_:_source_address_/_source_port_ to _dest_interface_:_dest_address_/_dest_port_; _label|domain-name_ length _number_ bytes exceeds _remaining_packet_length_ limit of _number_ bytes`

**Explanation** The label length exceeds bytes in a UDP DNS packet. See RFC 1035, section 2.3.4 for more information. .

**Recommended Action** Create the policy-map and add a custom DNS class-map to match traffic and exclude it from inspection to allow packets exceeding the label length.

### 410002

**Error Message** `%ASA-2-410002: Dropped _num_ DNS responses with mis-matched id in the past _sec_ second(s): from _src_ifc_:_sip_/_sport_ to _dest_ifc_:_dip_/_dport_`

**Explanation** The ASA detects an excess number of DNS responses with a mismatched DNS identifier. A high rate of mismatched DNS identifiers might indicate an attack on the cache. The threshold is set by the id-mismatch DNS policy-map parameter submode command.

-   _num_ —The number of ID mismatch instances as configured by the id-mismatch command
-   _sec_ —The duration in seconds as configured by the id-mismatch command
-   _src\_ifc_ —The source interface name at which the DNS message is received with a mismatched DNS identifier
-   _sip_ —The source IP address
-   _sport_ —The source port
-   _dest\_ifc_ —The destination interface name
-   _dip_ —The destination IP address
-   _dport_ —The destination port

**Recommended Action** Check the IP address and port in the message to trace the source of the attack. You can configure ACLs to block traffic permanently from the source.

### 410003

**Error Message** `%ASA-4-410003: _action_class_ DNS _action_ from _query_response_:_src_ifc_/_sip_ to _sport_:_dest_ifc_/_dip_; _dport_`

**Explanation** A DNS classification was performed on a DNS message and the specified criteria were satisfied. As a result, the configured action occurs.

-   _action\_class_ —The DNS Classification action class
-   _action_ —The action taken: Dropped, Dropped (no TSIG), or Masked header flags for
-   _query\_response_ —Either query or response
-   _src\_ifc_ —The source interface name
-   _sip_ —The source IP address
-   _sport_ —The source port
-   _dest\_ifc_ —The destination interface name
-   _dip_ —The destination IP address
-   _dport_ —The destination port
-   _further\_info_ —One of the following: matched Class id: _class\_name_ , matched Class id: _match\_command_ (for a standalone match command), or TSIG resource record not present (for messages generated by the tsig enforced command)

**Recommended Action** None required.

### 410004

**Error Message** `%ASA-6-410004: _action_class_ DNS _action_ from _query_response_:_src_ifc_/_sip_ to _sport_:_dest_ifc_/_dip_; _dport_`

**Explanation** A DNS classification was performed on a DNS message and the specified criteria were satisfied.

-   _action\_class_ —The DNS Classification action class
-   _action_ —The action taken: Received or Received (no TSIG)
-   _query\_response_ —Either query or response
-   _src\_ifc_ —The source interface name
-   _sip_ —The source IP address
-   _sport_ —The source port
-   _dest\_ifc_ —The destination interface name
-   _dip_ —The destination IP address
-   _dport_ —The destination port
-   _further\_info_ —One of the following: matched Class id: _class\_name_ , matched Class id: _match\_command_ (for a standalone match command), or TSIG resource record not present (for messages generated by the tsig enforced command)

**Recommended Action** None required.

### 411001

**Error Message** `%ASA-4-411001: Line protocol on Interface _interface_name_, changed state to up`

**Explanation** The status of the line protocol has changed from down to up . If interface\_name is a logical interface name such as inside and outside, this message indicates that the logical interface line protocol has changed from down to up . If interface\_name is a physical interface name such as Ethernet0 and GigabitEthernet0/1, this message indicates that the physical interface line protocol has changed from down to up .

**Recommended Action** None required.

### 411002

**Error Message** `%ASA-4-411002: Line protocol on Interface _interface_name_, changed state to down`

**Explanation** The status of the line protocol has changed from up to down. If interface\_name is a logical interface name such as inside and outside, this message indicates that the logical interface line protocol has changed from up to down. In this case, the physical interface line protocol status is not affected. If interface\_name is a physical interface name such as Ethernet0 and GigabitEthernet0/1, this message indicates that the physical interface line protocol has changed from up to down.

**Recommended Action** If this is an unexpected event on the interface, check the physical line.

### 411003

**Error Message** `%ASA-4-411003: Interface _interface_name_, changed state to administratively up`

**Explanation** The configuration status of the interface has changed from down to up.

**Recommended Action** If this is an unexpected event, check the physical line.

### 411004

**Error Message** `%ASA-4-411004: Interface _interface_name_, changed state to administratively down`

**Explanation** The configuration status of the interface has changed from down to up.

**Recommended Action** None required.

### 411005

**Error Message** `%ASA-4-411005: Interface _variable_1_ experienced a hardware transmit hang. A software reset has been performed.`

**Explanation** The interface experienced a hardware transmit freeze that required a reset of the Ethernet controller to restore the interface to full operation.

-   _variable 1_ —The interface name, such as GigabitEthernet0/0

**Recommended Action** None required.

### 412001

**Error Message** `%ASA-4-412001: MAC _MAC_address_ moved from _interface_1_ to _interface_2_`

**Explanation** A host move was detected from one module interface to another. In a transparent Secure Firewall ASA, mapping between the host (MAC) and Secure Firewall ASA port is maintained in a Layer 2 forwarding table. The table dynamically binds packet source MAC addresses to an Secure Firewall ASA port. In this process, whenever movement of a host from one interface to another interface is detected, this message is generated.

**Recommended Action** The host move might be valid or might be an attempt to spoof host MACs on other interfaces. If it is a MAC spoof attempt, you can either locate vulnerable hosts on your network and remove them or configure static MAC entries, which will not allow MAC address and port binding to change. If it is a genuine host move, no action is required.

### 412002

**Error Message** `%ASA-4-412002: Detected bridge table full while inserting MAC _MAC_address_ on interface _interface_. Number of entries = _num_`

**Explanation** The bridge table was full and an attempt was made to add one more entry. The Secure Firewall ASA maintains a separate Layer 2 forwarding table per context and the message is generated whenever a context exceeds its size limit. The MAC address will be added, but it will replace the oldest existing dynamic entry (if available) in the table. This might be an attempted attack.

**Recommended Action** Make sure that the new bridge table entries are valid. In case of attack, use EtherType ACLs to control access to vulnerable hosts.

### 413001

**Error Message** `%ASA-4-413001: Module _module_id_ is not able to shut down. Module Error: _errnum_ _message_`

**Explanation** The module identified by _module\_id_ was not able to comply with a request from the Secure Firewall ASA system module to shut down. It may be performing a task that cannot be interrupted, such as a software upgrade. The errnum and message text describes the reason why the module cannot shut down, and the recommended corrective action.

**Recommended Action** Wait for the task on the module to complete before shutting down the module, or use the session command to access the CLI on the module, and stop the task that is preventing the module from shutting down.

### 413002

**Error Message** `%ASA-4-413002: Module _module_id_ is not able to reload. Module Error: _errnum_ _message_`

**Explanation** The module identified by _module\_id_ was not able to comply with a request from the Secure Firewall ASA module to reload. It may be performing a task that cannot be interrupted, such as a software upgrade. The errnum and message text describes the reason why the module cannot reload, and the recommended corrective action.

**Recommended Action** Wait for the task on the module to complete before reloading the module, or use the session command to access the CLI on the module and stop the task that is preventing the module from reloading.

### 413003

**Error Message** `%ASA-4-413003: Module _string_one_ is not a recognized type.`

**Explanation** A module was detected that is not recognized as a valid module type.

**Recommended Action** Upgrade to a version of Secure Firewall ASA software that supports the module type installed.

### 413004

**Error Message** `%ASA-4-413004: Module in slot _string_one_ failed to write software v_newver_ (currently v_ver_), _reason_. Trying again.`

**Explanation** The module failed to accept a software version, and will be transitioned to an UNRESPONSIVE state. Another attempt will be made to update the module software.

-   _\>string one—_ The text string that specifies the module
-   _\>newver_ —The new version number of software that was not successfully written to the module (for example, 1.0(1)0)
-   _\>ver_ —The current version number of the software on the module (for example, 1.0(1)0)
-   _\>reason_ —The reason the new version cannot be written to the module. The possible values for _\>reason_ include the following:

\- write failure

\- failed to create a thread to write the image

**Recommended Action** None required. Subsequent attempts will either generate a message indicating a successful update or failure. You may verify the module transitions to UP after a subsequent update attempt by using the show module command.

### 413005

**Error Message** `%ASA-4-413005: Module _module_id_, application is not supported "_app_name_" version "_app_vers_" type _app_type_.`

**Error Message** `%ASA-4-413005: Module _prod_id_ in slot _slot_num_ , application is not supported _app_name_ version _app_vers_ type _app_type_`

**Explanation** The module installed in slot _slot\_num_ was running an unsupported application version or type.

-   _module\_id—_ The name of the software services module
-   _prod\_id_ —Product ID string
-   _slot\_num_ —The slot number in which the module is installed. Slot 0 indicates the system main board, and slot 1 indicates the module installed in the expansion slot.
-   _app\_name_ —Application name (string)
-   _app\_vers_ —Application version (string)
-   _app\_type_ —Application type (decimal)

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 413006

**Error Message** `%ASA-4-413006: _prod-id_ Module software version mismatch; slot _slot_ is "_prod-id_" version "_running-vers_". Slot _slot_ "_prod-id_" requires version "_required-vers_"`

**Explanation** The version of software running on the module in slot _slot_ was not the version required by another module.

-   _slot_ —Slot 0 indicates the system main board. Slot 1 indicates the module installed in the expansion slot.
-   _prod\_id_ —Product ID string for the device installed in slot _slot_
-   _running\_vers_ —Version of software currently running on the module installed in slot _slot_
-   _required\_vers_ —Version of software required by the module in slot _slot_

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 413007

**Error Message** `%ASA-1-413007: An unsupported configuration is detected. The combination of an _mpc_description_ with _ips_description_ is not supported.`

**Explanation** An unsupported Secure Firewall ASA and IPS configuration has been detected during IPS SSP setup for slot 1. The Secure Firewall ASA should continue to function normally with an unsupported configuration.

-   _mpc\_description_ —A description string for the ASA model, which can be one of the following: ASA5585-SSP-10, ASA5585-SSP-20, ASA5585-SSP-40, ASA5585-SSP-60, ASA5585-SSP-10-K7, ASA5585-SSP-20-K7, ASA5585-SSP-40-K7, ASA5585-SSP-60-K7.
-   _ips\_description_ —A description string for the IPS SSP model, which can be one of the following: ASA5585-SSP-IPS10, ASA5585-SSP-IPS20, ASA5585-SSP-IPS40, ASA5585-SSP-IPS60, ASA5585-SSP-P10K7, ASA5585-SSP-P20K7, ASA5585-SSP-P40K7, ASA5585-SSP-P60K7.

**Recommended Action** None required.

### 413008

**Error Message** `%ASA-1-413008: An unsupported configuration is detected.`

**Explanation** Only one power supply and one fan module are inserted when an ASA 10G SSP and IPS 10G SSP are present.

**Recommended Action** When using an ASA 10G SSP and IPS 10G SSP, insert two power supplies instead of one fan module and one power supply module.

### 413009

**Error Message** `%ASA-4-413009: _internal_interface_ =_current value_`

**Explanation** The firewall checks the current value of an internal interface or a data ring every one minute. When the current value of the ring falls below 10, this message is generated.

```makefile
%ASA-4-413009: Internal-Data0/1:RX[1]=[2]
```

In the above example, Internal-Data0/1 RX1 value went to 2, which is less than 10.

**Recommended Action** None.

### 414001

**Error Message** `%ASA-3-414001: Failed to save logging buffer to FTP server _filename_ using filename _ftp_server_address_ on interface _interface_name_: _fail_reason_`

**Explanation** The logging module failed to save the logging buffer to an external FTP server.

**Recommended Action** Take applicable actions based on the failed reason:

-   Protocol error—Make sure no connectivity issue exists between the FTP server and Secure Firewall ASA, and that the FTP sever can accept the FTP port command and PUT requests.
-   Invalid username or password—Make sure that the configured FTP client username and password are correct.
-   All other errors—If the problem persists, contact the Cisco TAC.

### 414002

**Error Message** `%ASA-3-414002: Failed to save logging buffer to _flash:/syslog_ directory using filename _filename_: _fail_reason_`

**Explanation** The logging module failed to save the logging buffer to system flash.

**Recommended Action** If the failed reason is caused by insufficient space, check the flash free space, and make sure that the configured limits of the logging flash-size command are set correctly. If the error is a flash file system I/O error, then contact the Cisco TAC for assistance.

### 414003

**Error Message** `%ASA-3-414003: TCP Syslog Server _intf_:_IP_Address_/_port_ not responding, New connections are _[permitted|denied]_ based on logging permit-hostdown policy`

**Explanation** The TCP syslog server for remote host logging was successful, is connected to the server, and new connections are permitted or denied based on the logging permit-hostdown policy. If the logging permit-hostdown policy is configured, a new connection is permitted. If not configured, a new connection is denied.

-   _intf_ —Interface of the Secure Firewall ASA to which the server is connected
-   _IP\_Address_ —IP address of the remote TCP syslog server
-   _port_ —Port of the remote TCP syslog server

**Recommended Action** Validate that the configured TCP syslog server is up. To permit new connections, configure the logging permit-hostdown policy. To deny new connections, do not configure the logging permit-hostdown policy.

### 414004

**Error Message** `%ASA-6-414004: TCP Syslog Server _intf_:_IP_Address_/_port_ - Connection restored`

**Explanation** The TCP syslog setup involves 4 channels connecting to the server. This message is generated only when one of the TCP syslog server channels become unreachable and the server is restored. This message is the first to reach the syslog server after a successful connection. This message is generated only on TCP syslog server.

| ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)

**Note** | ___

This message does not appear every time when the TCP syslog server is restored. It appears only when the server is restored after one of its channels became unreachable.

___ |
|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

-   _intf_ —Interface of the ASA to which the server is connected
    
-   _IP\_Address_ —IP address of the remote TCP syslog server
    
-   _port_ —Port of the remote TCP syslog server
    

**Recommended Action** None required.

### 414005

**Error Message** `%ASA-3-414005: TCP Syslog Server _intf_ : _IP_Address_ /_port_ connected, New connections are permitted based on logging permit-hostdown policy`

**Explanation** The TCP syslog server for remote host logging was successful, is connected to the server, and new connections are permitted based on the logging permit-hostdown policy. If the logging permit-hostdown policy is configured, a new connection is permitted.

-   _intf_ —Interface of the Secure Firewall ASA to which the server is connected
-   _IP\_Address_ —IP address of the remote TCP syslog server
-   _port_ —Port of the remote TCP syslog server

**Recommended Action** None required.

### 414006

**Error Message** `%ASA-3-414006: TCP syslog server configured and logging queue is full. New connections denied based on logging permit-hostdown policy.`

**Explanation** The logging queue is close to reaching the configured limit, so there is a risk that syslog messages will be discarded.

**Recommended Action** See the "Configuring the Logging Queue" section in the CLI configuration guide for information about how to tune the queue size to avoid this situation. If you want to deny new connections in this case, use the no logging permit-hostdown command. If you want to allow new connections in this case, use the logging permit-hostdown command.

### 414007

**Error Message** `%ASA-6-414007: TCP syslog server connection restored. New connections allowed.`

**Explanation** The TCP syslog server for remote host logging was successfully connected and new connections are permitted.

**Recommended Action** None required.

### 414008

**Error Message** `%ASA-6-414008: New connections are now allowed due to change of logging permit-hostdown policy.`

**Explanation** An administrator changed the logging permit-hostdown policy by entering the logging permit-hostdown command at a time when new connections are being denied. Due to this change of policy, new connections will be allowed.

**Recommended Action** None required.

### 414009

**Error Message** `%ASA-6-414009: TCP syslog server connection removed. New connections allowed.`

**Explanation** The system successfully removed the TCP syslog server for remote host logging. New connections are permitted.

**Recommended Action** None required.

### 415001

**Error Message** `%ASA-6-415001: HTTP - matched _matched_string_ in policy-map _map_name_, header field count exceeded _connection_action_ _int_type_:_IP_address_/_port_num_ to _int_type_:_IP_address_/_port_num_`

**Explanation** This message is generated when one of the following occurs:

-   The total number of fields in the HTTP header exceeds the user-configured number of header fields. The relevant command is: match {request | response} header count num.
-   The appearance of a specified field in the HTTP header exceeds the user-configured number for this header field. The relevant command is: match {request | response} header header-name count num.
-   matched\_string—The matched string is one of the following:

\- The class map ID, followed by the name of the class map. This string appears when the class map is user configured.

\- The actual match command that initiated the message. This string appears when the class map is internal.

-   _map\_name_ —The name of the policy map
-   _connection\_action_ —Dropping the connection or resetting the connection
-   _interface\_type_ —The type of interface (for example, DMZ or outside)
-   _IP\_address_ —The IP address of the interface
-   _port\_num_ —The port number

**Recommended Action** Enter the match {request | response} header command to reconfigure the HTTP header field value.

### 415002

**Error Message** `%ASA-6-415002: HTTP - matched _matched_string_ in policy-map _map_name_, header field length exceeded _connection_action_ _int_type_:_IP_address_/_port_num_ to _int_type_:_IP_address_/_port_num_`

**Explanation** The specified HTTP header field length exceeded the user-configured length.

-   matched\_string—The matched string is one of the following:

\- The class map ID, followed by the name of the class map. This string appears when the class map is user configured.

\- The actual match command that initiated the message. This string appears when the class map is internal.

-   _map\_name_ —The name of the policy map
-   _connection\_action_ —Dropping connection or Resetting connection
-   _interface\_type_ —The type of interface (for example, DMZ or outside)
-   _IP\_address_ —The IP address of the interface
-   _port\_num_ —The port number

**Recommended Action** Enter the match {request | response} header header\_name length gt num command to change the HTTP header field length.

### 415003

**Error Message** `%ASA-6-415003: HTTP - matched _matched_string_ in policy-map _map_name_, body length exceeded _connection_action_ _int_type_:_IP_address_/_port_num_ to _int_type_:_IP_address_/_port_num_`

**Explanation** The length of the message body exceeded the user-configured length.

-   matched\_string—The matched string is one of the following:

\- The class map ID, followed by the name of the class map. This string appears when the class map is user configured.

\- The actual match command that initiated the message. This string appears when the class map is internal.

-   _map\_name_ —The name of the policy map
-   _connection\_action_ —Dropping the connection or resetting the connection
-   _interface\_type_ —The type of interface (for example, DMZ or outside)
-   _IP\_address_ —The IP address of the interface
-   _port\_num_ —The port number

**Recommended Action** Enter the match {request | response} body length gt num command to change the length of the message body.

### 415004

**Error Message** `%ASA-5-415004: HTTP - matched _matched_string_ in policy-map _map_name_, content-type verification failed _connection_action_ _int_type_:_IP_address_/_port_num_ to _int_type_:_IP_address_/_port_num_`

**Explanation** The magic number in the body of the HTTP message is not the correct magic number for the MIME-type specified in the content-type field in the HTTP message header.

-   matched\_string—The matched string is one of the following:

\- The class map ID, followed by the name of the class map. This string appears when the class map is user configured.

\- The actual match command that initiated the message. This string appears when the class map is internal.

-   _map\_name_ —The name of the policy map
-   _connection\_action_ —Dropping the connection or resetting the connection
-   _interface\_type_ —The type of interface (for example, DMZ or outside)
-   _IP\_address_ —The IP address of the interface
-   _port\_num_ —The port number

**Recommended Action** Enter the match {request | response} header content-type violation command to correct the error.

### 415005

**Error Message** `%ASA-5-415005: HTTP - matched _matched_string_ in policy-map _map_name_, URI length exceeded _connection_action_ _int_type_:_IP_address_/_port_num_ to _int_type_:_IP_address_/_port_num_`

**Explanation** The length of the URI exceeded the user-configured length.

-   matched\_string—The matched string is one of the following:

\- The class map ID, followed by the name of the class map. This string appears when the class map is user configured.

\- The actual match command that initiated the message. This string appears when the class map is internal.

-   _map\_name_ —The name of the policy map
-   _connection\_action_ —Dropping the connection or resetting the connection
-   _interface\_type_ —The type of interface (for example, DMZ or outside)
-   _IP\_address_ —The IP address of the interface
-   _port\_num_ —The port number

**Recommended Action** Enter the match request uri length gt num command to change the length of the URI.

### 415006

**Error Message** `%ASA-5-415006: HTTP - matched _matched_string_ in policy-map _map_name_, URI matched _connection_action_ _int_type_:_IP_address_/_port_num_ to _int_type_:_IP_address_/_port_num_`

**Explanation** The URI matched the regular expression that the user configured. See the match request uri regex {regex-name | class class-name} command for more information.

-   matched\_string—The matched string is one of the following:

\- The class map ID, followed by the name of the class map. This string appears when the class map is user configured.

\- The actual match command that initiated the message. This string appears when the class map is internal.

-   _map\_name_ —The name of the policy map
-   _connection\_action_ —Dropping the connection or resetting the connection
-   _interface\_type_ —The type of interface (for example, DMZ or outside)
-   _IP\_address_ —The IP address of the interface
-   _port\_num_ —The port number

**Recommended Action** None required.

### 415007

**Error Message** `%ASA-5-415007: HTTP - matched _matched_string_ in policy-map _map_name_, Body matched _connection_action_ _int_type_:_IP_address_/_port_num_ to _int_type_:_IP_address_/_port_num_`

**Explanation** The message body matched the regular expression that the user configured. See the match {request | response} body regex {regex-name | class class-name} command for more information.

-   matched\_string—The matched string is one of the following:

\- The class map ID, followed by the name of the class map. This string appears when the class map is user configured.

\- The actual match command that initiated the message. This string appears when the class map is internal.

-   _map\_name_ —The name of the policy map
-   _connection\_action_ —Dropping the connection or resetting the connection
-   _interface\_type_ —The type of interface (for example, DMZ or outside)
-   _IP\_address_ —The IP address of the interface
-   _port\_num_ —The port number

**Recommended Action** None required.

### 415008

**Error Message** `%ASA-5-415008: HTTP - matched _matched_string_ in policy-map _map_name_, header matched _connection_action_ _int_type_:_IP_address_/_port_num_ to _int_type_: _IP_address_/_port_num_`

**Explanation** A value in a user-specified field in the message header matched the regular expression that the user configured. See the match {request | response } header header-field-name {regex-name | class class-name} command for more information.

-   matched\_string—The matched string is one of the following:

\- The class map ID, followed by the name of the class map. This string appears when the class map is user configured.

\- The actual match command that initiated the message. This string appears when the class map is internal.

-   _map\_name_ —The name of the policy map
-   _connection\_action_ —Dropping the connection or resetting the connection
-   _interface\_type_ —The type of interface (for example, DMZ or outside)
-   _IP\_address_ —The IP address of the interface
-   _port\_num_ —The port number

**Recommended Action** None required.

### 415009

**Error Message** `%ASA-5-415009: HTTP - matched _matched_string_ in policy-map _map_name_, method matched _connection_action_ _int_type_:_IP_address_/_port_num_ to _int_type_:_IP_address_/_port_num_`

**Explanation** The HTTP method matched the user-configured regular expression. See the match request method {regex-name | class class-name} command for more information.

-   matched\_string—The matched string is one of the following:

\- The class map ID, followed by the name of the class map. This string appears when the class map is user configured.

\- The actual match command that initiated the message. This string appears when the class map is internal.

-   _map\_name_ —The name of the policy map
-   _connection\_action_ —Dropping the connection or resetting the connection
-   _interface\_type_ —The type of interface (for example, DMZ or outside)
-   _IP\_address_ —The IP address of the interface
-   _port\_num_ —The port number

**Recommended Action** None required.

### 415010

**Error Message** `%ASA-5-415010: matched _matched_string_ in policy-map _map_name_ , transfer encoding matched _connection_action_ from _int_type_ :_IP_address_ /_port_num_ to _int_type_ :_IP_address_ /_port_num_`

**Explanation** The value in the transfer encoding field matched the user-configured regular expression or keyword. See the match {request | response} header transfer-encoding {{regex-name | class class-name} | keyword} command for more information.

-   matched\_string—The matched string is one of the following:

\- The class map ID, followed by the name of the class map. This string appears when the class map is user configured.

\- The actual match command that initiated the message. This string appears when the class map is internal.

-   _map\_name_ —The name of the policy map
-   _connection\_action_ —Dropping the connection or resetting the connection
-   _interface\_type_ —The type of interface (for example, DMZ or outside)
-   _IP\_address_ —The IP address of the interface
-   _port\_num_ —The port number

**Recommended Action** None required.

### 415011

**Error Message** `%ASA-5-415011: HTTP - policy-map _map_name_:Protocol violation _connection_action_ _int_type_:_IP_address_/_port_num_ to _int_type_:_IP_address_/_port_num_`

**Explanation** The HTTP parser cannot detect a valid HTTP message in the first few bytes of an HTTP message.

-   _map\_name_ —The name of the policy map
-   _connection\_action_ —Dropping the connection or resetting the connection
-   _interface\_type_ —The type of interface (for example, DMZ or outside)
-   _IP\_address_ —The IP address of the interface
-   _port\_num_ —The port number

**Recommended Action** Enter the protocol-violation action {drop | reset} log command to correct the problem.

### 415012

**Error Message** `%ASA-5-415012: HTTP - matched _matched_string_ in policy-map _map_name_, content-type unknown _connection_action_ _int_type_:_IP_address_/_port_num_ to _int_type_:_IP_address_/_port_num_`

**Explanation** The content-type field did not contain a MIME type that matches a built-in MIME type.

-   matched\_string—The matched string is one of the following:

\- The class map ID, followed by the name of the class map. This string appears when the class map is user configured.

\- The actual match command that initiated the message. This string appears when the class map is internal.

-   _map\_name_ —The name of the policy map
-   _connection\_action_ —Dropping the connection or resetting the connection
-   _interface\_type_ —The type of interface (for example, DMZ or outside)
-   _IP\_address_ —The IP address of the interface
-   _port\_num_ —The port number

**Recommended Action** Enter the match {request | response} header content-type unknown command to correct the problem.

### 415013

**Error Message** `%ASA-5-415013: HTTP - policy-map _map-name_:Malformed chunked encoding _connection_action_ _int_type_:_IP_address_/_port_num_ to _int_type_:_IP_address_/_port_num_`

**Explanation** A chunked encoding was malformed, and the HTTP message cannot be parsed. In addition, logging for the protocol-violation command was configured.

-   map-name— The name of the policy map
-   _connection\_action_ —Dropping the connection or resetting the connection
-   _interface\_type_ —The type of interface (for example, DMZ or outside)
-   _IP\_address_ —The IP address of the interface
-   _port\_num_ —The port number

**Recommended Action** Enter the protocol-violation action {drop | reset} log command to correct the problem.

### 415014

**Error Message** `%ASA-5-415014: HTTP - matched _matched_string_ in policy-map _map_name_, Mime-type in response wasn't found in the accept-types of the request _connection_action_ _int_type_:_IP_address_/_port_num_ to _int_type_:_IP_address_/_port_num_`

**Explanation** The MIME type in an HTTP response was not in the accept field of the request.

-   matched\_string—The matched string is one of the following:

\- The class map ID, followed by the name of the class map. This string appears when the class map is user configured.

\- The actual match command that initiated the message. This string appears when the class map is internal.

-   _map\_name_ —The name of the policy map
-   _connection\_action_ —Dropping the connection or resetting the connection
-   _interface\_type_ —The type of interface (for example, DMZ or outside)
-   _IP\_address_ —The IP address of the interface
-   _port\_num_ —The port number

**Recommended Action** Enter the match req-resp content-type mismatch command to correct the problem.

### 415015

**Error Message** `%ASA-5-415015: HTTP - matched _matched_string_ in policy-map _map_name_, transfer-encoding unknown _connection_action_ _int_type_:_IP_address_/_port_num_ to _int_type_:_IP_address_/_port_num_`

**Explanation** An empty transfer encoding occurred.

-   matched\_string—The matched string is one of the following:

\- The class map ID, followed by the name of the class map. This string appears when the class map is user configured.

\- The actual match command that initiated the message. This string appears when the class map is internal.

-   _map\_name_ —The name of the policy map
-   _connection\_action_ —Dropping the connection or resetting the connection
-   _interface\_type_ —The type of interface (for example, DMZ or outside)
-   _IP\_address_ —The IP address of the interface
-   _port\_num_ —The port number

**Recommended Action** Enter the match {request | response} header transfer-encoding empty command to correct the problem.

### 415016

**Error Message** `%ASA-4-415016: policy-map _map_name_:Maximum number of unanswered HTTP requests exceeded _connection_action_ _int_type_:_IP_address_/_port_num_ to _int_type_:_IP_address_/_port_num_`

**Explanation** The number of unanswered HTTP requests exceeded the internal number of requests allowed.

-   _map\_name_ —The name of the policy map
-   _connection\_action_ —Dropping the connection or resetting the connection
-   _interface\_type_ —The type of interface (for example, DMZ or outside)
-   _IP\_address_ —The IP address of the interface
-   _port\_num_ —The port number

**Recommended Action** Enter the protocol-violation action {drop | reset} log command to correct the problem.

### 415017

**Error Message** `%ASA-6-415017: HTTP - matched _matched_string_ in policy-map _map_name_, arguments matched _connection_action__int_type_:_IP_address_/_port_num_ to _int_type_:_IP_address_/_port_num_`

**Explanation** A pattern in the arguments matches the user-configured regular expression or keyword. See the match request args regex {regex-name | class class-name} command for more information.

-   matched\_string—The matched string is one of the following:

\- The class map ID, followed by the name of the class map. This string appears when the class map is user configured.

\- The actual match command that initiated the message. This string appears when the class map is internal.

-   _map\_name_ —The name of the policy map
-   _connection\_action_ —Dropping the connection or resetting the connection
-   _interface\_type_ —The type of interface (for example, DMZ or outside)
-   _IP\_address_ —The IP address of the interface
-   _port\_num_ —The port number

**Recommended Action** None required.

### 415018

**Error Message** `%ASA-5-415018: HTTP - matched _matched_string_ in policy-map _map_name_, Header length exceeded _connection_action_ _int_type_:_IP_address_/_port_num_ to _int_type_:_IP_address_/_port_num_`

**Explanation** The total header length exceeded the user-configured length for the header.

-   matched\_string—The matched string is one of the following:

\- The class map ID, followed by the name of the class map. This string appears when the class map is user configured.

\- The actual match command that initiated the message. This string appears when the class map is internal.

-   _map\_name_ —The name of the policy map
-   _connection\_action_ —Dropping the connection or resetting the connection
-   _interface\_type_ —The type of interface (for example, DMZ or outside)
-   _IP\_address_ —The IP address of the interface
-   _port\_num_ —The port number

**Recommended Action** Enter the match {request | response} header length gt num command to reduce the length of the header.

### 415019

**Error Message** `%ASA-5-415019: HTTP - matched _matched_string_ in policy-map _map_name_, status line matched _connection_action_ _int_type_:_IP_address_/_port_num_ to _int_type_:_IP_address_/_port_num_`

**Explanation** The status line in a response matched a user-configured regular expression. See the match response status-line regex {regex-name | class class-name } command for more information.

-   matched\_string—The matched string is one of the following:

\- The class map ID, followed by the name of the class map. This string appears when the class map is user configured.

\- The actual match command that initiated the message. This string appears when the class map is internal.

-   _map\_name_ —The name of the policy map
-   _connection\_action_ —Dropping the connection or resetting the connection
-   _interface\_type_ —The type of interface (for example, DMZ or outside)
-   _IP\_address_ —The IP address of the interface
-   _port\_num_ —The port number

**Recommended Action** None required.

### 415020

**Error Message** `%ASA-5-415020: HTTP - matched _matched_string_ in policy-map _map_name_, a non-ASCII character was matched _connection_action_ _int_type_:_IP_address_/_port_num_ to _int_type_:_IP_address_/_port_num_`

**Explanation** A non-ASCII character was found.

-   matched\_string—The matched string is one of the following:

\- The class map ID, followed by the name of the class map. This string appears when the class map is user configured.

\- The actual match command that initiated the message. This string appears when the class map is internal.

-   _map\_name_ —The name of the policy map
-   _connection\_action_ —Dropping the connection or resetting the connection
-   _interface\_type_ —The type of interface (for example, DMZ or outside)
-   _IP\_address_ —The IP address of the interface
-   _port\_num_ —The port number

**Recommended Action** Enter the match {request | response} header non-ascii command to correct the problem.

### 416001

**Error Message** `%ASA-4-416001: Dropped UDP SNMP packet from _source_interface_:_source_IP_/_source_port_ to _dest_interface_:_dest_address_/_dest_port_; _prot_version_`

**Explanation** An SNMP packet was denied passage through the ASA because of a bad packet format or because the prot\_version is not allowed through the ASA. The prot\_version parameter can be one of the following values: 1, 2, 2c, or 3.

**Recommended Action** Change the settings for SNMP inspection using the snmp-map command, which allows the user to permit or deny specific protocol versions.

### 417001

**Error Message** `%ASA-4-417001: Unexpected event received: _number_`

**Explanation** A process received a signal, but no handler was found for the event.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 417004

**Error Message** `%ASA-4-417004: Filter violation error: conn _number_ (_string_:_string_) in _string_`

**Explanation** A client tried to modify a route attribute that the client does not own.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 417006

**Error Message** `%ASA-4-417006: No memory for _string_ in _string_ (warning)`

**Explanation** An operation failed because of low memory, but will be handled with another mechanism.

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 418001

**Error Message** `%ASA-4-418001: Through-the-device packet to/from management-only network is denied: _protocol_string_`

**Explanation** A packet from the specified source to the destination was dropped because it is traversing the Secure Firewall ASA to and from the management-only network.

-   protocol\_string—TCP, UDP, ICMP, or protocol ID as a number in decimal
-   interface\_name— Interface name
-   IP\_address—IP address
-   port—Port number
-   _sg\_info_ —Security group name or tag for the specified IP address

**Recommended Action** Determine who is generating this packet and why.

### 418018

**Error Message** `%ASA-3-418018: neighbor _IP_Address__vrf_identifie__topology_identifier__address_family__state_change_` OR `%ASA-3-418018: neighbor _IP_Address_ IPv4 Unicast topology base removed from session User reset` OR `%ASA-3-418018: neighbor _IP_Address_ Up` OR `%ASA-3-418018: neighbor _IP_Address_ IPv4 Unicast topology base removed from session BGP Notification sent`

**Explanation** The different states of BGP peering and notification of changes on the topology DB as a result of the peering state transitions.

**Recommended Action** None required.

### 418019

**Error Message** `%ASA-3-418019: received from _IP_Address_ error_code/_error_subcode_(_error_text_) _data_bytes_bytes _hex_data_`

**Explanation** An indication of why BGP peering was terminated.

-   Reason—Reason for termination. The reason could be invalid or corrupt AS path, or expiry of hold time, and so on.
    
-   Bytes—Number of bytes transmitted
    

**Recommended Action** None required.

### 418040

**Error Message** `%ASA-3-418040: Unsupported or malformed message: _IP_Address_`

**Explanation** Indication of unsupported or mal-formed messages received during the BGP handshake, not necessarily only related to Graceful restart specifically.

**Recommended Action** None required.

### 418044

**Error Message** `%ASA-3-418044: Connection closed remotely by _IP_Address_`

**Explanation** Indication of hold time for a BGP neighbor has expired.

-   IP\_Address—IPv4 or IPv6 address of the BGP neighbor.
    
-   hold\_time—The hold time in milliseconds.
    

**Recommended Action** None required.

### 419001

**Error Message** `%ASA-4-419001: Dropping TCP packet from _src_ifc_:_src_IP_/_src_port_ to _dest_ifc_:_dest_IP_/_dest_port_, reason: _reason_, MSS _size_, data _size_`

**Explanation** The length of the TCP packet exceeded the MSS advertised in the three-way handshake.

-   _\>src\_ifc—_ Input interface name
-   _\>src\_IP—_ The source IP address of the packet
-   _\>src\_port—_ The source port of the packet
-   _\>dest\_ifc—_ The output interface name
-   _\>dest\_IP—_ The destination IP address of the packet
-   _\>dest\_port—_ The destination port of the packet

**Recommended Action** If there is a need to allow packets that exceed the MSS, create a TCP map using the exceed-mss command, as in the following example:

```graphql
ciscoasa# access-list http-list permit tcp any host server_ip eq 80
ciscoasa# class-map http
 ciscoasa# match access-list http-list
 ciscoasa# tcp-map tmap
ciscoasa# exceed-mss allow
ciscoasa# policy-map global_policy
ciscoasa# class http
ciscoasa# set connection advanced-options tmap
```

### 419002

**Error Message** `%ASA-4-419002: Duplicate TCP SYN from _in_interface_:_src_address_/_src_port_ to _out_interface_:_dest_address_/_dest_port_ with different initial sequence number`

**Explanation** A duplicate TCP SYN was received during the three-way-handshake that has a different initial sequence number from the SYN that opened the embryonic connection. This may indicate that SYNs are being spoofed. This message occurs in Release 7.0.4.1 and later.

-   in\_interface—The input interface
-   src\_address—The source IP address of the packet
-   src\_port—The source port of the packet
-   out\_interface—The output interface
-   dest\_address—The destination IP address of the packet
-   dest\_port—The destination port of the packet

**Recommended Action** None required.

### 419003

**Error Message** `%ASA-4-419003: Cleared TCP urgent flag from _out_ifc_:_src_ip_/_src_port_ to _in_ifc_:_dest_ip_/_dest_port_`

**Explanation** A duplicate TCP SYN was received during the three-way-handshake that has a different initial sequence number from the SYN that opened the embryonic connection. This may indicate that SYNs are being spoofed. This message occurs in Release 7.0.4.1 and later.

-   in\_ifc—The input interface
-   src\_ip—The source IP address of the packet
-   src\_port—The source port of the packet
-   out\_ifc—The output interface
-   dest\_ip—The destination IP address of the packet
-   dest\_port—The destination port of the packet

**Recommended Action** If you need to keep the urgent flag in TCP headers, use the urgent-flag allow command in TCP map configuration mode.

**Error Message** `%ASA-7-419003: Cleared TCP urgent flag.`

**Explanation** This syslog is displayed when urgent flag or urgent pointer of tcp packet is cleared. This could be due to user configuration (tcp-map) or having some value for the urgent pointer in a tcp packet but the urgent flag is not set.

**Recommended Action** Verify if the tcp-map configurations whether the urget flag is set to clear.

### 419004

**Error Message** `%ASA-6-419004: TCP connection _ID_ from _src_ifc_:_src_ip_/_src_port_ (_src_ip_/_src_port_) to _dst_ifc_:_dst_ip_/_dst_port_ (_dst_ip_/_dst_port_) is probed by DCD`

**Explanation**

A TCP connection was probed by Dead Connection Detection (DCD) to determine if connection was still valid.

**Recommended Action** None.

### 419005

**Error Message** `%ASA-6-419005: TCP connection _ID_ from _src_ifc_:_src_ip_/_src_port_ (_src_ip_/_src_port_) to _dest_ifc_:_des_ip_/_des_port_ (_des_ip_/_des_port_) duration _hh:mm:ss_ data _bytes_, is kept open by DCD as valid connection`

**Explanation**

A TCP connection was kept open by Dead Connection Detection (DCD) as a valid connection.

**Recommended Action** None.

### 419006

**Error Message** `%ASA-6-419006: Teardown TCP connection _ID_ from _src_ifc_:_src_ip_/_src_port_ (_src_ip_/_src_port_) to _dst_ifc_:_dst_ip_/_dst_port_ (_dst_ip_/_dst_port_) duration _hh:mm:ss_ data _bytes_, DCD probe was not responded from _client/server_ interface _ifc_name_`

**Explanation**

A TCP connection was closed by Dead Connection Detection (DCD) as it is no longer required.

**Recommended Action** None.

### 420001

**Error Message** `%ASA-3-420001: IPS card not up and fail-close mode used, dropping _ICMP_ packet from _ifc_in_:_SIP_/_port_ to _ifc_out_:_DIP_/_port_`

For example:

```ruby
%ASA-3-420001: IPS card not up and fail-close mode used, dropping TCP packet from >ifc_in
:>SIP
/>SPORT
 to >ifc_out
:>DIP
/>DPORT
%ASA-3-420001: IPS card not up and fail-close mode used, dropping UDP packet from >ifc_in
:>SIP
/>SPORT
 to >ifc_out
:>DIP
/>DPORT
%ASA-3-420001: IPS card not up and fail-close mode used, dropping protocol >protocol
 packet from >ifc_in
:>SIP
 to >ifc_out
:>DIP
```

**Explanation** Packets are dropped when the IPS fail-close mode is used, and the IPS card is not up. This message is rate limited.

-   _ifc\_in_ —Input interface name
-   _ifc\_out_ —Output interface name
-   _SIP_ —Source IP of the packet
-   _SPORT_ —Source port of the packet
-   _DIP_ —Destination IP of the packet
-   _DPORT_ —Destination port of the packet
-   _ICMP\_TYPE_ —Type of the ICMP packet
-   _ICMP\_CODE_ —Code of the ICMP packet

**Recommended Action** Bring up the IPS card.

### 420002

**Error Message** `%ASA-4-420002: IPS requested to drop _ICMP_ packet from _ifc_in_:_SIP_/_port_ to _ifc_out_:_DIP_/_port_`

For example:

```vbnet
%ASA-4-420002: IPS requested to drop TCP packet from ifc_in:SIP/SPORT to ifc_out:DIP/DPORT
%ASA-4-420002: IPS requested to drop UDP packet from ifc_in:SIP/SPORT to ifc_out:DIP/DPORT
%ASA-4-420002: IPS requested to drop protocol packet from ifc_in:SIP to ifc_out:DIP
```

**Explanation** IPS requested that the packet be dropped.

-   _ifc\_in_ —Input interface name
-   _ifc\_out_ —Output interface name
-   _SIP_ —Source IP of the packet
-   _SPORT_ —Source port of the packet
-   _DIP_ —Destination IP of the packet
-   _DPORT_ —Destination port of the packet
-   _ICMP\_TYPE_ —Type of the ICMP packet
-   _ICMP\_CODE_ —Code of the ICMP packet

**Recommended Action** None required.

### 420003

**Error Message** `%ASA-4-420003: IPS requested to reset TCP connection from _ifc_in_:_SIP_/_SPORT_ to _ifc_out_:_DIP_/_DPORT_`

**Explanation** IPS requested a reset of a TCP connection.

-   _ifc\_in_ —Input interface name
-   _ifc\_out_ —Output interface name
-   _SIP_ —Source IP of the packet
-   _SPORT_ —Source port of the packet
-   _DIP_ —Destination IP of the packet
-   _DPORT_ —Destination port of the packet

**Recommended Action** None required.

### 420004

**Error Message** `%ASA-6-420004: Virtual Sensor _sensor_name_ was added on the AIP SSM`

**Explanation** A virtual sensor was added on the AIP SSM card.

-   _n_ —Card number

**Recommended Action** None required.

### 420005

**Error Message** `%ASA-6-420005: Virtual Sensor _sensor_name_ was deleted from the AIP SSM`

**Explanation** A virtual sensor was deleted from the AIP SSM card.

-   _n_ —Card number

**Recommended Action** None required.

### 420006

**Error Message** `%ASA-3-420006: Virtual sensor not present and fail-close mode used, dropping _protocol_ packet from _ifc_in_:_SIP_/_SPORT_ to _ifc_out_:_DIP_/_DPORT_`

**Explanation** Packets are dropped when the IPS fail-close mode is used, and the virtual sensor used for the packet is not present.

-   _protocol—_ Protocol used to send the packet
-   _ifc\_in_ —Input interface name
-   _ifc\_out_ —Output interface name
-   _SIP_ —Source IP address of the packet
-   _SPORT_ —Source port of the packet
-   _DIP_ —Destination IP address of the packet
-   _DPORT_ —Destination port of the packet

**Recommended Action** Add the virtual sensor.

### 420007

**Error Message** `%ASA-4-420007: _application-string_ cannot be enabled for the Module in slot _slot_id_. The module's current software version does not support this feature. Please upgrade the software on the module in slot _slot_id_ to support this feature.`

**Explanation** This message is generated by any new feature in the ASA that needs a corresponding software version in the SSM or SSC hardware module. The message is sent each time that the ASA module manager detects state changes in the SSM or SSC hardware module.

-   _application-string_ —The name of the application (for example, Promiscuous IDS)
-   _slot\_id_ —The module identifier, which is 1 for the current ASA
-   _version\_number_ —The version number of the message header between the ASA and the IPS application

**Recommended Action** Load the SSM or SSC hardware module with the correct software images that support the designated application.

### 420008

**Error Message** `%ASA-3-420008: IPS module license disabled and fail-close mode used, dropping packet.`

**Explanation** The IPS module license has been disabled and when the fail-close mode is configured, all traffic destined for the IPS module will be dropped. You can check the status of the license by using the show activation-key command.

**Recommended Action** Use the activation-key command to apply an activation key that has the IPS license enabled.

### 421001

**Error Message 1** `%ASA-3-421001: {TCP|UDP} flow from _interface_name_:_IP_address_/_port_ to _interface_name_:_IP_address_/_port_ is dropped because _application_id_ has failed.`

**Error Message 2** `%ASA-3-421001: {TCP|UDP} flow from _interface_name_:_IP_address_/_port_ to _interface_name_:_IP_address_/_port_ is skipped because _application_id_ has failed.`

**Explanation** A packet was dropped (Error Message 1) or skipped (Error Message 2) because the CSC SSM application failed. By default, this message is rate limited to 1 message every 10 seconds.

-   interface\_name—The interface name
-   IP\_address—The IP address
-   port—The port number
-   application—The CSC SSM is the only application supported in the current release

**Recommended Action** Determine the problem with the service module.

### 421002

**Error Message** `%ASA-6-421002: TCP|UDP flow from _interface_name_ :_IP_address_ /_port_ to _interface_name_ :_IP_address_ /_port_ bypassed _application_ checking because the protocol is not supported.`

**Explanation** The connection bypassed service module security checking because the protocol that it is using cannot be scanned by the service module. For example, the CSC SSM is not capable of scanning Telnet traffic. If the user configures Telnet traffic to be scanned, the traffic will bypass the scanning service. By default, this message is rate limited to 1 message every 10 seconds.

-   IP\_address—The IP address
-   port—The port number
-   interface\_name—The name of the interface on which the policy is applied
-   application—The CSC SSM is the only application supported in the current release

**Recommended Action** The configuration should be modified to only include protocols that are supported by the service module.

### 421003

**Error Message** `%ASA-3-421003: Invalid data plane encapsulation`

**Explanation** A packet injected by the service module did not have the correct data plane header. Packets exchanged on the data backplane adhere to a Cisco proprietary protocol called ASDP. Any packet that does not have the proper ASDP header is dropped.

**Recommended Action** Use the capture name type asp-drop \[ssm-asdp-invalid-encap\] command to capture the offending packets and contact the Cisco TAC.

### 421004

**Error Message** `%ASA-7-421004: Failed to inject _{TCP|UDP}_ packet from _IP_address_/_port_ to _IP_address_/_port_`

**Explanation** The ASA has failed to inject a packet as instructed by the service module. This may happen if the ASA tries to inject a packet into a flow that has already been released or when the ASA maintains its connection table independently from the service module. Normally it will not cause any problem.

-   IP\_address—The IP address
-   port—The port number

**Recommended Action** If ASA performance is affected, or if the problem persists, contact the Cisco TAC.

### 421005

**Error Message** `%ASA-6-421005: _interface_name_:_IP_address_ is counted as a user for _application_`

**Explanation** A host has been counted toward the license limit. The specified host was counted as a user of application. The total number of users in 24 hours is calculated at midnight for license validation.

-   interface\_name—The interface name
-   IP\_address—The IP address
-   application—The CSC SSM

**Recommended Action** None required. However, if the overall count exceeds the user license that you have purchased, contact the Cisco TAC to upgrade your license.

### 421006

**Error Message** `%ASA-6-421006: There are _number_ users of _application_ accounted during the past 24 hours`

**Explanation** The total number of users who have used an application for the past 24 hours have been identified. This message is generated every 24 hours to give the total number of hosts that have used services provided by the service module.

-   application—The CSC SSM

**Recommended Action** None required. However, if the overall count exceeds the user license that you have purchased, contact the Cisco TAC to upgrade your license.

### 421007

**Error Message** `%ASA-3-421007: TCP|UDP flow from _interface_name_ :_IP_address_ /_port_ to _interface_name_ :_IP_address_ /_port_ is skipped because _application_ has failed.`

**Explanation** A flow was skipped because the service module application has failed. By default, this message is rate limited to 1 message every 10 seconds.

-   IP\_address—The IP address
-   port—The port number
-   interface\_name—The name of the interface on which the policy is applied
-   application—The CSC SSM

**Recommended Action** Determine the problem with the service module.

### 422004

**Error Message** `%ASA-4-422004: IP SLA Monitor _number0_ : Duplicate event received. Event number _number1_`

**Explanation** The IP SLA monitor process has received a duplicate event. Currently, this message applies to destroy events. Only one destroy request will be applied. This is only a warning message.

-   _number0_ —The SLA operation number
-   _number1_ —The SLA operation event ID

**Recommended Action** If this recurs, enter the show sla monitor configuration SLA\_operation\_id command and copy the output of the command. Copy the message as it appears on the console or in the system log. Then contact the Cisco TAC and provide the representative with the information that you have, along with information about the application that is configuring and polling the SLA probes.

### 422005

**Error Message** `%ASA-4-422005: IP SLA Monitor Probe(s) could not be scheduled because clock is not set.`

**Explanation** One or more IP SLA monitor probes cannot be scheduled because the system clock was not set.

**Recommended Action** Make sure that the system clock is functional by using NTP or another mechanism.

### 422006

**Error Message** `%ASA-4-422006: IP SLA Monitor Probe _number_ : _string_`

**Explanation** The IP SLA monitor probe cannot be scheduled. Either the configured starting time has already occurred or the starting time is invalid.

-   _number_ —The SLA operation ID
-   _string_ —A string describing the error

**Recommended Action** Reschedule the failed probe with a valid start time.

### 423001

**Error Message** `%ASA-4-423001: _{Allowed|Dropped}_ invalid NBNS _pkt_type_name_ with _error_reason_str_ from _ifc_name_:_ip_address_/_port_ to _ifc_name_:_ip_address_/_port_.`

**Explanation** The NBNS packet format is incorrect.

**Recommended Action** None required.

### 423002

**Error Message** `%ASA-4-423002: _{Allowed|Dropped}_ mismatched NBNS _pkt_type_name_ with _error_reason_str_ from _ifc_name_:_ip_address_/_port_ to _ifc_name_:_ip_address_/_port_`

**Explanation** An NBNS ID mismatch occurred.

**Recommended Action** None required.

### 423003

**Error Message** `%ASA-4-423003: _{Allowed|Dropped}_ invalid NBDGM _pkt_type_name_ with _error_reason_str_ from _ifc_name_:_ip_address_/_port_ to _ifc_name_:_ip_address_/_port_.`

**Explanation** The NBDGM packet format is incorrect.

**Recommended Action** None required.

### 423004

**Error Message** `%ASA-4-423004: _{Allowed|Dropped}_ mismatched NBDGM _pkt_type_name_ with _error_reason_str_ from _ifc_name_:_ip_address_/_port_ to _ifc_name_:_ip_address_/_port_`

**Explanation** An NBDGM ID mismatch occurred.

**Recommended Action** None required.

### 423005

**Error Message** `%ASA-4-423005: _{Allowed|Dropped}_ NBDGM _pkt_type_name_ fragment with _error_reason_str_ from _ifc_name_:_ip_address_/_port_ to _ifc_name_:_ip_address_/_port_.`

**Explanation** The NBDGM fragment format is incorrect.

**Recommended Action** None required.

### 424001

**Error Message** `%ASA-4-424001: Packet denied: _protocol_string_. _intf_in_ interface is in a backup state`

**Explanation** A packet was dropped because it was traversing the Secure Firewall ASA to or from a redundant interface. Interface functionality is limited on low-end platforms. The interface specified by the backup interface command can only be a backup for the primary interface configured. If the default route to the primary interface is up, any traffic through the Secure Firewall ASA from the backup interface will be denied. Conversely, if the default route to the primary interface is down, traffic through the Secure Firewall ASA from the primary interface will be denied.

-   _protocol\_string_ —The protocol string; for example, TCP or protocol ID (a decimal number)
-   _intf\_in_ —The input interface name
-   _src\_ip_ —The source IP address of the packet
-   _src\_port_ —The source port of the packet
-   _intf\_out_ —The output interface name
-   _dst\_ip_ —The destination IP address of the packet
-   _dst\_port_ —The destination port of the packet
-   _sg\_info_ —The security group name or tag for the specified IP address

**Recommended Action** Determine the source of the denied packet.

### 424002

**Error Message** `%ASA-4-424002: Connection to the backup interface is denied: _protocol_string_`

**Explanation** A connection was dropped because it is in a backup state. Interface functionality is limited on low-end platforms. The backup interface can only be a backup for the primary interface specified by the backup interface command. If the default route to the primary interface is up, any connection to the Secure Firewall ASA through the backup interface will be denied. Conversely, if the default route to the primary interface is down, connections to the Secure Firewall ASA through the primary interface will be denied.

-   _protocol\_string_ —The protocol string; for example, TCP or protocol ID (a decimal number)
-   _intf\_in_ —The input interface name
-   _src\_ip_ —The source IP address of the packet
-   _src\_port_ —The source port of the packet
-   _intf\_out_ —The output interface name
-   _dst\_ip_ —The destination IP address of the packet
-   _dst\_port_ —The destination port of the packet

**Recommended Action** Determine the source of the denied packet.

### 425001

**Error Message** `%ASA-6-425001: Redundant interface _redundant_interface_name_ created.`

**Explanation** The specified redundant interface was created in the configuration.

-   _redundant\_interface\_name_ —Redundant interface name

**Recommended Action** None required.

### 425002

**Error Message** `%ASA-6-425002: Redundant interface _redundant_interface_name_ removed.`

**Explanation** The specified redundant interface was removed from the configuration.

-   _redundant\_interface\_name_ —Redundant interface name

**Recommended Action** None required.

### 425003

**Error Message** `%ASA-6-425003: Interface _interface_name_ added into redundant interface _redundant_interface_name_`

**Explanation** The specified physical interface was added to the specified redundant interface as a member interface.

-   _interface\_name_ —An interface name
-   _redundant\_interface\_name_ —Redundant interface name

**Recommended Action** None required.

### 425004

**Error Message** `%ASA-6-425004: Interface _interface_name_ removed from redundant interface _redundant_interface_name_`

**Explanation** The specified redundant interface was removed from the specified redundant interface.

-   _interface\_name_ —An interface name
-   _redundant\_interface\_name_ —Redundant interface name

**Recommended Action** None required.

### 425005

**Error Message** `%ASA-5-425005: Interface _interface_name_ become active in redundant interface _redundant_interface_name_`

**Explanation** Within a redundant interface, one member interface is the active member. Traffic only passes through the active member interface. The specified physical interface became the active member of the specified redundant interface. Member interface switchover occurs when one of the following is true:

-   The redundant-interface interface-name active-member interface-name command was executed.
-   The active member interface is down, while the standby member interface is up.
-   The standby member interface comes up (from down), while the active member interface remains down.

-   _interface\_name_ —An interface name
-   _redundant\_interface\_name_ —Redundant interface name

**Recommended Action** Check the status of the member interfaces.

### 425006

**Error Message** `%ASA-3-425006: Redundant interface _redundant_interface_name_ switch active member to _interface_name_ failed`

**Explanation** An error occurred when member interface switchover was attempted.

-   _redundant\_interface\_name_ —Redundant interface name
-   _interface\_name_ —An interface name

**Recommended Action** If the problem persists, contact the Cisco TAC.

### 426001

**Error Message** `%ASA-6-426001: PORT-CHANNEL:Interface _ifc_name_ bundled into EtherChannel interface _num_`

**Explanation** The interface port-channel _num_ or the channel-group _num_ mode _mode_ command has been used on a nonexistent port channel.

-   _ifc\_name_ —The EtherChannel interface name
-   _num_ —The port channel number

**Recommended Action** None required.

### 426002

**Error Message** `%ASA-6-426002: PORT-CHANNEL:Interface _ifc_name_ unbundled from EtherChannel interface _num_`

**Explanation** The no interface port-channel _num_ command has been used.

-   _ifc\_name_ —The EtherChannel interface name
-   _num—_ The port channel number

**Recommended Action** None required.

### 426003

**Error Message** `%ASA-6-426003: PORT-CHANNEL:Interface _ifc_name1_ has become standby in EtherChannel interface _num_`

**Explanation** The channel-group _num_ mode _mode_ command has been used.

-   _ifc\_name1_ —The EtherChannel interface name
-   _num_ —The port channel number

**Recommended Action** None required.

### 426004

**Error Message 1** `%ASA-4-426004: PORT-CHANNEL:Interface _ifc_name1_ is not compatible with _ifc_name_ and will be suspended (_speed_of_ _ifc_name1_ is _X_Mbps_, _Y_ is _1000_Mbps_)`

**Error Message 2** `%ASA-4-426004: Interface _ifc_name1_ is not compatible with _ifc_name1_ and will be suspended (_ifc_name1_ is _Full-duplex_, _ifc_name1_ is _Half-duplex_)`

**Explanation** The channel-group _num_ mode _mode_ command is executed on a physical interface and there is a speed or duplex mismatch of this physical interface with that of the port channel.

-   _ifc\_name_ —The interface that is being added to the port channel
-   _ifc\_name1_ —The interface that is already in the port channel and in a bundled state

**Recommended Action** Do one of the following:

-   Change the speed of the physical interface to that of the port channel and execute the channel-group _num_ mode _mode_ command again.
-   Leave the member interface in a suspended state. When the last active member is removed, then that member will try to reestablish LACP on the suspended member.

### 426101

**Error Message** `%ASA-6-426101: PORT-CHANNEL:Interface _ifc_name_ is allowed to bundle into EtherChannel interface _port-channel_id_ by CLACP.`

**Explanation** A port has been bundled in a span-cluster channel group.

**Recommended Action** None required.

### 426102

**Error Message** `%ASA-6-426102: PORT-CHANNEL:Interface _ifc_name_ is moved to standby in EtherChannel interface _port-channel_id_ by CLACP.`

**Explanation** A port has been moved to hot-standby state in a span-cluster channel group.

**Recommended Action** None required.

### 426103

**Error Message** `%ASA-6-426103: PORT-CHANNEL:Interface _ifc_name_ is selected to move from standby to bundle in EtherChannel interface _port-channel_id_ by CLACP.`

**Explanation** A standby port has been selected to move to bundled state in a span-cluster channel group.

**Recommended Action** None required.

### 426104

**Error Message** `%ASA-6-426104: PORT-CHANNEL:Interface _ifc_name_ is unselected in EtherChannel interface _port-channel_id_ by CLACP.`

**Explanation** A bundled port has been unbundled in a span-cluster channel group to obtain space for other ports to be bundled.

**Recommended Action** None required.

### 428002

**Error Message** `%ASA-6-428002: WAAS confirmed from _in_interface_ :_src_ip_addr/src_port_ to _out_interface_ :_dest_ip_addr/dest_port_ , inspection services bypassed on this connection.`

**Explanation** WAAS optimization was detected on a connection. All layer 7 inspection services, including IPS, are bypassed on WAAS-optimized connections.

**Recommended Action** No action is required if the network includes WAE devices; otherwise, the network administrator should investigate the use of the WAAS option on this connection.

### 429001

**Error Message** `%ASA-3-429001: CX card not up and fail-close mode used, dropping _protocol_ packet from _interface_name_:_ip_address_/_port_ to _interface_name_:_ip_address_/_port_`

**Explanation** Data has been dropped because an SSP is down and a fail-close policy exists.

**Recommended Action** Check the status of the service module and contact the Cisco TAC for assistance, if necessary.

### 429002

**Error Message** `%ASA-4-429002: CX requested to drop _protocol_ packet from _interface_name_:_ip_address_/_port_ to _interface_name_:_ip_address_/_port_`

**Explanation** The CXSC SSP requested that the ASA drop a packet of a connection.

**Recommended Action** None.

### 429003

**Error Message** `%ASA-4-429003: CX requested to reset TCP connection from _interface_name_:_ip_addr_/_port_ to _interface_name_:_ip_addr_/_port_`

**Explanation** The CXSC SSP requested that the ASA reset a TCP connection.

**Recommended Action** None required.

### 429004

**Error Message** `%ASA-3-429004: Unable to set up _rule_name_ authentication-proxy rule for the cxsc action on interface _interface_name_ for _policy_type_ service-policy.`

**Explanation** The ASA could not set up to-the-box rules for authentication proxy with the CXSC action because of some internal errors, such as insufficient memory.

**Recommended Action** This error should not occur. Contact the Cisco TAC.for assistance.

### 429005

**Error Message** `%ASA-6-429005: Set up _protocol_type_ authentication-proxy rule for the cxsc action on interface _interface_name_ for traffic destined to _ip_address_/_port_ for _policy_type_ service-policy`

**Explanation** The ASA successfully set up to-the-box rules for authentication proxy with the CXSC action.

**Recommended Action** None.

### 429006

**Error Message** `%ASA-6-429006: Cleaned up authentication-proxy rule for the cxsc action on interface _interface_name_ for traffic destined to _ip_address_ for _policy_type_ service-policy`

**Explanation** The ASA successfully cleaned up to-the-box rules for authentication proxy with the CXSC action.

**Recommended Action** None.

### 429007

**Error Message** `%ASA-4-429007: CXSC redirect will override Scansafe redirect for flow from _interface_name_:_ip_address_/_port_ to _interface_name_:_ip_address_/_port_ [(_username_)]`

**Explanation** A flow matches both CXSC and Scansafe redirects. The message indicates that the CXSC redirect overrides the Scansafe redirect for the displayed flow.

**Recommended Action** If this is unwanted behavior, then reconfigure the policy to ensure that no overlap of CXSC and Scansafe redirection occurs for the same flow.

### 429008

**Error Message** `%ASA-4-429008: Unable to respond to VPN query from CX for session _0x%x_ . Reason _%s_`

**Explanation** The CX sent a VPN session query to the Secure Firewall ASA, but it did not respond either because of an invalid session ID or another reason. Valid reasons can be any of the following:

-   TLV length is invalid
-   TLV memory allocation failed
-   VPN session query message enqueue failed
-   VPN session ID is invalid

**Recommended Action** None required.

### 431001

**Error Message** `%ASA-4-431001: RTP conformance: Dropping RTP packet from _in_ifc_:_src_ip_/_src_port_ to _out_ifc_:_dest_ip_/_dest_port_, Drop reason: _drop_reason_ _value_`

**Explanation** The RTP packet was dropped.

-   in\_ifc—The input interface
-   src\_ip—The source IP address of the packet
-   src\_port—The source port of the packet
-   out\_ifc—The output interface
-   _dest\_ip_ —The destination IP address of the packet
-   dest\_port—The destination port of the packet
-   drop\_reason—One of the following drop reasons:

\- Incorrect version _value_ —The version number from the packet is incorrect.

\- Invalid payload-type _value_ —The payload type from the packet is invalid.

\- Incorrect SSRC _value_ —The SSRC from the packet is incorrect.

\- Out-of-range sequence number _value_ sequence number from the packet.

\- Out of sequence in packet in probation _value_ sequence number from the packet.

**Recommended Action** Examine the dropped RTP packets to determine which field the RTP source is setting incorrectly. Also examine the source to verify that it is legitimate and not an attacker trying to misuse an opening in the ASA.

### 431002

**Error Message** `%ASA-4-431002: RTCP conformance: Dropping RTCP packet from _in_ifc_:_src_ip_/_src_port_ to _out_ifc_:_dest_ip_/_dest_port_, Drop reason: _drop_reason_ _value_`

**Explanation** The RTCP packet was dropped.

-   in\_ifc—The input interface
-   src\_ip—The source IP address of the packet
-   src\_port—The source port of the packet
-   out\_ifc—The output interface
-   dest\_ip—The destination IP address of the packet
-   dest\_port—The destination port of the packet
-   drop\_reason—One of the following drop reasons:

\- Incorrect version value—The version number from the packet is incorrect.

\- Invalid payload-type value—The payload type from the packet is incorrect.

**Recommended Action** Examine the dropped RTP packets to determine which field the RTP source is setting incorrectly. Also examine the source to verify that it is legitimate and not an attacker trying to misuse an opening in the ASA.

### 434001

**Error Message** `%ASA-4-434001: SFR card not up and fail-close mode used, dropping _protocol_ packet from _ingress_:_source_/_IP_address_ to _source_port_:_egress_interface_/_destination_IP_address_`

**Explanation** A packet has been dropped because of a fail-close configuration for the module. Your loss of connectivity for all the flows is caused by redirecting them to the module, because the fail-close configuration is designed to drop all the flows if the module is down.

**Recommended Action** Try to understand the reason for failure and restore services. Alternatively, you can use the fail-open option even if the card does not recover immediately. Note that in the fail-open configuration, all packets to the module are bypassed if the card status is down.

### 434002

**Error Message** `%ASA-4-434002: SFR requested to drop _protocol_ packet from _ingress_interface_:_source_IP_address_/_source_port_ to _egress_interface_:_destination_IP_address_/_destination_port_`

**Explanation** A packet has been denied by the module. Your connection is not successful for a certain flow has been redirected to the module.

**Recommended Action** Try to identify the module policy that caused this flow or packet to be denied.

### 434003

**Error Message** `%ASA-4-434003: SFR requested to reset TCP connection from _ingress_interface_:_source_IP_address_/_source_port_ to _egress_:_interface_/_destination_IP_address_`

**Explanation** A TCP flow has been reset by the ASA, as requested by the module. Your TCP connection is not successful for a certain flow because it was redirected to the module.

**Recommended Action** Try to identify the module policy that caused this flow or packet to be denied.

### 434004

**Error Message** `%ASA-5-434004: SFR requested device to bypass further packet redirection and process _protocol_ flow from _inside_ifc_name_:_src_ip_/_src_port_ to _outside_ifc_name_:_dst_ip_/_dst_port_ locally`

**Explanation** SourceFire (SFR) has determined not to inspect more traffic of a flow and requests the Secure Firewall ASA to stop redirecting the flow of traffic to SFR.

**Recommended Action** None Required.

### 434007

**Error Message** `%ASA-4-434007: SFR redirect will override Scansafe redirect for flow from _inside_interface_:_source_ip_address_/_source_port_ to _outside_interface_:_destination_IP_address_/_destination_port_ [(_user_)]`

**Explanation** A flow that was inspected by Scansafe is now inspected by SourceFire (SFR) only. Scansafe and SFR cannot inspect a flow simultaneously.

**Recommended Action** Reconfigure the ASA inspect policy that caused this flow or packet to be inspected by either Scansafe or SFR.

### 444004

**Error Message** `%ASA-2-444004: Timebased activation key _xxx_ _xxx_ _xxx_ _xxx_ _xxx_ has expired. Applying _permanent_license_ activation key _xxx_ _xxx_ _xxx_ _xxx_ _xxx_.`

**Explanation** The temporary license that was installed has expired. The features that the license provided are no longer available.

-   _key_ —The temporary activation key
-   _permkey_ —The permanent activation key

**Recommended Action** A permanent license should be purchased and installed.

### 444005

**Error Message** `%ASA-4-444005: Timebased license key _xxx_ _xxx_ _xxx_ _xxx_ _xxx_ will expire in _num_ days.`

**Explanation** This message is generated every 24 hours, indicating that the temporary license will expire in the number of days specified. After that date, the features that the license provided will no longer be available.

-   _activation-key_ —The temporary activation key
-   _num_ —The number of days left until expiration

**Recommended Action** If the amount of time remaining is less than 30 days, you should purchase another time-based activation key before the temporary license runs out.

### 444007

**Error Message** `%ASA-2-444007: Timebased activation key _xxx_ _xxx_ _xxx_ _xxx_ _xxx_ has expired.`

**Explanation** The time-based activation key has expired. The specified features that the license provided are no longer available.

-   _activation-key_ —The temporary activation key
-   _feature_ —The name of the licensed feature being affected

**Recommended Action** You must purchase another time-based activation key as soon as possible to prevent service disruption for the features specified.

### 444008

**Error Message** `%ASA-4-444008: _license-type_ license has expired, and the system is scheduled to reload in _number_ days. Apply a new activation key to enable _license-type_ license and prevent the automatic reload.`

**Explanation** The specific license has expired, which will cause the system to reload in x days. Apply a new activation key to enable the specific license and prevent automatic reload.

**Recommended Action** Apply a new activation key to enable the specific license and prevent automatic reload.

### 444009

**Error Message** `%ASA-2-444009: _license-type_ license has expired 30 days ago. The system will now reload.`

**Explanation** The specific license expired 30 days ago. The system will reload.

**Recommended Action** None required.

### 444100

**Error Message** `%ASA-5-444100: Shared license _request_ request failed, Reason: _reason_.`

**Explanation** A shared license client request was unsuccessfully sent or processed by the server.

-   _request_ —Valid requests are:

\- get AnyConnect Premium

\- release AnyConnect Premium

\- transfer AnyConnect Premium

-   _reason_ —The reason that the request failed. Valid reasons are:

\- connection failed to server

\- version not supported by server

\- message signature invalid

\- client ID unknown by server

\- server is not active

\- license capacity reached

**Recommended Action** None required.

### 444101

**Error Message** `%ASA-5-444101: Shared license service is active. License server address: _address_`

**Explanation** The shared license server has become active.

-   _address_ —The license server IPv4 or IPv6 address

**Recommended Action** None required.

### 444102

**Error Message** `%ASA-2-444102: Shared license service inactive. License server is not responding.`

**Explanation** The shared license service was inactive because the license server was not responding. The ASA failed to register with the shared license server.

**Recommended Action** Verify that the license server address, secret, and port are configured correctly.

### 444103

**Error Message** `%ASA-6-444103: Shared _licensetype_ license usage is over 90% capacity.`

**Explanation** The shared license usage on the network is over 90 percent capacity.

-   _licensetype_ —AnyConnect Premium

**Recommended Action** None required.

### 444104

**Error Message** `%ASA-6-444104: Shared _licensetype_ license availability: _value_.`

**Explanation** The shared license availability on the network appeared.

-   _licensetype_ —AnyConnect Premium
-   _value_ —The license availability

**Recommended Action** None required.

### 444105

**Error Message** `%ASA-2-444105: Released _value_ shared _licensetype_ license(s). License server has been unreachable for 24 hours.`

**Explanation** The shared license server has been unreachable for 24 hours, and all shared licenses that have been acquired by the ASA have been released. The ASA failed to register with the license server.

-   _licensetype_ —AnyConnect Premium
-   _value_ —The license availability

**Recommended Action** Verify the connectivity to the license server, and that the configuration has not been changed on the license server.

### 444106

**Error Message** `%ASA-4-444106: Shared license backup server _address_ is not available`

**Explanation** The shared license backup server is not reachable. License server information is not synchronized with the backup device.

-   _address_ —The IPv4 or IPv6 address of the backup license server

**Recommended Action** None required.

### 444107

**Error Message** `%ASA-6-444107: Shared license service _status_ on interface _ifname_.`

**Explanation** The shared license service has been enabled or disabled on the specified interface.

-   _ifname_ —The interface name.
-   _status_ —The status of the license server. Valid values are enabled or disabled.

**Recommended Action** None required.

### 444108

**Error Message** `%ASA-6-444108: Shared license _state_ client id _id_.`

**Explanation** The multi-site license client ID has registered or expired with the server.

-   _id_ —The ID of the client
-   _state_ —The state of the license server. Valid values are registered or expired.

**Recommended Action** None required.

### 444109

**Error Message** `%ASA-4-444109: Shared license backup server role change to _state_.`.

**Explanation** The shared backup license server role has changed.

-   _state_ —The state of the license server. Valid values are active or inactive.

**Recommended Action** None required.

### 444110

**Error Message** `%ASA-4-444110: Shared license server backup has _days_ day(s) remaining as active license server.`

**Explanation** The shared backup license server is in an active role and remains active for a specified number of days. The ASA failed to register with the license server, and needs to register with the primary license server soon.

-   _days_ —The number of days left as the active license server

**Recommended Action** Verify that the license server is online and reachable by the ASA.

### 444111

**Error Message** `%ASA-2-444111: Shared license backup service has been terminated due to the primary license server _address_ being unavailable for more than _days_ days. The License server needs to be brought back on-line to continue using shared licensing.`

**Explanation** The shared backup license server active time has expired. The primary server needs to go online in order for the shared license service to continue.

-   _address_ —The IPv4 or IPv6 address of the license server
-   _days_ —The number of days that the license server has been unavailable

**Recommended Action** Register with the primary license server in order to continue using the shared license service.

### 444302

**Error Message** `%ASA-2-444302: %SMART_LIC-2-PLATFORM_ERROR: Platform error.`

**Explanation** Smart Licensing Agent has encountered a platform problem. This indicates that the platform team did not properly implement smart licensing on the device.

**Recommended Action** The platform team needs to address this problem before release.

### 444303

**Error Message** `%ASA-3-444303: %SMART_LIC-3-AGENT_REG_FAILED: Smart Agent for licensing registration with Cisco licensing cloud failed.`

**Explanation** Smart Licensing registration failed. This may have been caused due to an invalid ID token used during the registration or network connection failure to cisco.com.

**Recommended Action** Please check the Smart Agent syslog messages for additional information. Turn on the smart agent debug mode (CLI command: ‘debug license agent all’) and retry for more detailed information. Check your Smart Call Home configuration, your network connection with Cisco, and if the Identity token you used for registration is valid.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-AGENT_DEREG_FAILED: Smart Agent for licensing deregistration with CSSM failed.`

**Explanation** Smart Licensing deregistration failed. This may have been caused due to a network connection failure to CSSM. The local registration information has been removed from the device.

**Recommended Action** Please check the Smart Agent syslog messages for additional information. Turn on the smart agent debug mode (CLI command: ‘debug license agent all’) and retry for more detailed information. Check your Smart Call Home configuration and your network connection with CSSM.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-OUT_OF_COMPLIANCE: One or more entitlements are out of compliance.`

**Explanation** One or more requested entitlements from the customer are out of compliance.

**Recommended Action** Customer needs to go to the smart licensing portal to view their entitlements to understand the non-compliance.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-EVAL_EXPIRED: Evaluation period expired`.

**Explanation** Your evaluation period has expired. Please obtain a new identity token from the smart agent portal and re-register the device.

**Recommended Action** Customer needs to obtain a new identity token from the smart agent portal and re-register the device with the Cisco licensing service.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-BAD_MODE: An unknown mode was specified.`

**Explanation** An invalid entitlement enforcement mode was received by the smart agent in the process of logging a syslog message.

**Recommended Action** This is a smart call home internal error. Please report this to Cisco.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-BAD_NOTIF: A bad notification type was specified.`

**Explanation** An invalid notification type was received by the smart agent in the process of logging a syslog message.

**Recommended Action** This is a smart call home internal error. Please report this to Cisco.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-ID_CERT_EXPIRED: Identity certificate expired. Agent will transition to the unidentified (not registered) state.`

**Explanation** The device has not communicated with Cisco for an extended period of time and the device has not automatically renewed the device registration with Cisco.

**Recommended Action** Please check the smart call home settings and network connectivity to cisco.com.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-ID_CERT_RENEW_NOT_STARTED: Identity certificate start date not reached yet.`

**Explanation** The device registration failed. The Identity certificate start date is later than the device current time.

**Recommended Action** Please adjust your device clock to be up-to-date and retry the registration again.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-ID_CERT_RENEW_FAILED: Identity certificate renewal failed.`

**Explanation** The device has not communicated with Cisco for an extended period of time and the device has failed to automatically renew the device registration with Cisco.

**Recommended Action** Please check the smart call home settings and network connectivity to cisco.com.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-ENTITLEMENT_RENEW_FAILED: Entitlement authorization with Cisco licensing cloud failed.`

**Explanation** The device has failed to communicate with Cisco to renew the entitlement authorization.

**Recommended Action** Please check the smart agent syslog messages for further information. Additionally, check for smart call home settings and network connectivity to cisco.com.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-COMM_FAILED: Communications failure with Cisco licensing cloud.`

**Explanation** The device communication with the Cisco licensing service failed.

**Recommended Action** Please check the smart call home settings and network connectivity to cisco.com.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-CERTIFICATE_VALIDATION: Certificate validation failed by smart agent.`

**Explanation** The identity certificate validation failed.

**Recommended Action** Please check the smart agent syslog file for more information. Turn on the smart agent debug mode (CLI command: license smart debug enable) and retry again for additional information. Additionally, check if the identity certificate expiration date has been reached.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-AUTH_RENEW_FAILED: Authorization renewal with Cisco licensing cloud failed.`

**Explanation** The authorization renew request failed. This may have been caused due to wrong smart call home settings or network connectivity failure to cisco.com.

**Recommended Action** Please check the smart agent syslog file for more information. Turn on the smart agent debug mode and retry again for additional information. Additionally, check the smart call home settings and network connectivity to cisco.com.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-INVALID_TAG: The entitlement tag is invalid.`

**Explanation** The tag is not defined in the Cisco Smart Software Manager.

**Recommended Action** Report this error to Cisco.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-INVALID_ROLE_STATE: The current role is not allowed to move to the new role.`

**Explanation** From the last role event, we can only move to certain roles. The device has moved to a role to which the smart agent cannot follow.

**Recommended Action** Please check the smart agent syslog file for more information. Turn on the smart agent debug mode and retry again for additional information.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-EVAL_WILL_EXPIRE_WARNING: Evaluation period will expire in time.`

**Explanation** The device is using the evaluation period which will expire in the specified time.

**Recommended Action** Use the ‘license smart register ID token’ CLI to register this device before the evaluation period expires.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-EVAL_EXPIRED_WARNING: Evaluation period expired on time.`

**Explanation** The device evaluation period has expired.

**Recommended Action** Use the ‘license smart register ID token’ CLI to register this device.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-ID_CERT_EXPIRED_WARNING: This device's registration will expire in time.`

**Explanation** The registration for this device will expire at the specified time. This usually indicates a communications failure with the Cisco licensing authority.

**Recommended Action** Please check the smart call home settings and network connectivity to cisco.com. Additionally, check if the identity certificate need to be renewed.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-CONFIG_OUT_OF_SYNC: Trusted Store Enable flag not in sync with System Configuration, TS flag Config flag.`

**Explanation** Smart licensing configuration does not match the value of the enable flag in persistent storage. This can happen if a configuration is copied onto the system and a reload occurs. If the new configuration does not contain the Smart Licensing Enable command, the value in persistent storage will not match.

**Recommended Action** Apply the desired Smart Licensing Configuration Command and persist the configuration.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-REG_EXPIRED_CLOCK_CHANGE: Smart Licensing registration has expired because the system time was changed outside the validity period of the registration period. The agent will transition to the un-registered state in 60 minutes.`

**Explanation** The system clock has been changed so that it is now outside the valid registration period. If the clock is reset to a value inside the registration validity period within one hour smart licensing will continue function normally. If the clock is not reset the device will become un-registered and a new identity token will need to be obtained to re-register the device. The registration validity period is defined by the start and end date in the identity certificate. Use 'show tech license' to get the id certificate information.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-ROOT_CERT_MISMATCH_PROD: Certificate type mismatch.`

**Explanation** Smart Agent received incorrect certificate for validation. Please contact your product support team.

**Error Message** `%ASA-3-444303: %SMART_LIC-3-HOT_STANDBY_OUT_OF_SYNC: Smart Licensing agent on hot standby is out of sync with active Smart Licensing agent.`

**Explanation** Smart Licensing Agent on the hot standby failed to process the data necessary to stay in sync with the active agent. If a switchover occurs the new active agent will not be in the same state as the current active agent configuration does not match the value of the enable flag in persistent storage. This can happen if a configuration is copied onto the system and a reload occurs. If the new configuration does not contain the Smart Licensing Enable command, the value in persistent storage will not match.

### 444304

**Error Message** `%ASA-4-444304: %SMART_LIC-4-IN_OVERAGE: One or more entitlements are in overage.`

**Explanation** This is for information only. The customer is still in compliance and within the overage amount as specified in their contract.

**Error Message** `%ASA-4-444304: %SMART_LIC-4-CONFIG_NOT_SAVED: Smart Licensing configuration has not been saved.`

This is for information only. The customer remains in IN/OUT\_OF compliance state.

**Recommended Action** None.

### 444305

**Error Message** %ASA-5-444305: %SMART\_LIC-5-SYSTEM\_CLOCK\_CHANGED: Smart Agent for Licensing System clock has been changed.

**Explanation** System clock was manually reset.

**Error Message** `%ASA-5-444305: %SMART_LIC-5-IN_COMPLIANCE: All entitlements are authorized.`

**Explanation** All customer requested entitlements are authorized by Cisco licensing service.

**Error Message** `%ASA-5-444305: %SMART_LIC-5-EVAL_START: Entering evaluation period.`

**Explanation** Either customer allocate entitlement prior to registration or customer registration has expired. The device is now de-registered and is in evaluation mode.

**Error Message** `%ASA-5-444305: %SMART_LIC-5-AUTHORIZATION_EXPIRED: Authorization expired.`

**Explanation** The device has not communicated with Cisco for an extended period of time and the device has not automatically renewed the entitlement authorizations.

**Error Message** `%ASA-5-444305: %SMART_LIC-5-COMM_RESTORED: Communications with Cisco licensing cloud restored.`

**Explanation** Smart Agent communication with the Cisco licensing service is restored.

**Error Message** `%ASA-5-444305: %SMART_LIC-5-COMM_INIT_FAILED: Failed to initialize communications with the Cisco Licensing Cloud.`

**Explanation** Smart Agent could not initialize communication with the Cisco licensing service.

**Recommended Action** None.

### 444306

**Error Message** `%ASA-6-444306: %SMART_LIC-6-AGENT_READY: Smart Agent for Licensing is initialized.`

**Explanation** Smart Agent is initialized and ready for use.

**Error Message** `%ASA-6-444306: %SMART_LIC-6-AGENT_ENABLED: Smart Agent for Licensing is enabled.`

**Explanation** Smart Agent is enabled and ready for use.

**Error Message** `%ASA-6-444306: %SMART_LIC-6-AGENT_REG_SUCCESS: Smart Agent for Licensing Registration with Cisco licensing cloud successful.`

**Explanation** Smart Licensing registration was successful.

**Error Message** `%ASA-6-444306: %SMART_LIC-6-AGENT_DEREG_SUCCESS: Smart Agent for Licensing De-registration with Cisco licensing cloud successful.`

**Explanation** Smart Licensing deregistration was successful.

**Error Message** `%ASA-6-444306: %SMART_LIC-6-DISABLED: Smart Agent for Licensing disabled.`

**Explanation** Smart Agent has been disabled.

**Error Message** `%ASA-6-444306: %SMART_LIC-6-ID_CERT_RENEW_SUCCESS: Identity certificate renewal successful.`

**Explanation** Customer identity certificate has been renewed successfully and can continue to use the device.

**Error Message** `%ASA-6-444306: %SMART_LIC-6-ENTITLEMENT_RENEW_SUCCESS: Entitlement authorization renewal with Cisco licensing cloud successful.`

**Explanation** Authorization renewal request is successful.

**Error Message** `%ASA-6-444306: %SMART_LIC-6-AUTH_RENEW_SUCCESS: Authorization renewal with Cisco licensing cloud successful.`

**Explanation** Authorization of customer requested entitlements are successfully renewed.

**Error Message** `%ASA-6-444306: %SMART_LIC-6-HA_ROLE_CHANGED: Smart Agent HA role changed to role.`

**Explanation** Smart Agent role on HA RP has been changed to either active or standby.

**Error Message** `%ASA-6-444306: %SMART_LIC-6-HA_CHASSIS_ROLE_CHANGED: Smart Agent HA chassis role changed to role.`

**Explanation** Smart Agent chassis role on HA has been changed to either active or standby.

**Error Message** `%ASA-6-444306: %SMART_LIC-6-AGENT_ALREADY_REGISTER: Smart Agent is already registered with the Cisco licensing cloud.`

**Explanation** Smart Licensing has already registered with Cisco. Use the force option to register again.

**Error Message** `%ASA-6-444306: %SMART_LIC-6-AGENT_ALREADY_DEREGISTER: Smart Agent is already Deregistered with the CSSM.`

**Explanation** Smart Licensing has already de-registered with Cisco, use the force option to register again.

**Error Message** `%ASA-6-444306: %SMART_LIC-6-EXPORT_CONTROLLED: Usage of export controlled features is status.`

**Explanation** Notification of whether the usage of export controlled features is allowed or not allowed. This message is generated following the registration with Cisco licensing cloud.

**Recommended Action** None.

### 444307

**Error Message** `%ASA-7-444307: %SMART_LIC-7-DAILY_JOB_TIMER_RESET: Daily job timer reset.`

**Explanation** This message is only used for testing purposes and does not indicate an error.

**Recommended Action** None.

### 446001

**Error Message** `%ASA-4-446001: Maximum TLS Proxy session limit of _max_sess_ reached`

**Explanation** A configured maximum session limit for TLS proxy was reached. New sessions beyond the limit were denied.

-   _max\_sess_ —The currently effective maximum session limit

**Recommended Action** If more TLS sessions are needed, use the tls-proxy maximum-sessions max\_sess command to increase the limit. Alternatively, you can use the tls-proxy proxy\_name and tls-proxy maximum-sessions max\_sess commands, and then reboot for the commands to take effect.

### 446003

**Error Message** `%ASA-4-446003: Denied TLS Proxy session from _src_int_ :_src_ip_ /_src_port_ to _dst_int_ :_dst_ip_ /_dst_port_ , UC-IME license is disabled.`

**Explanation** The UC-IME license is either on or off. Once enabled, UC-IME can use any number of available TLS sessions, according to the Secure Firewall ASA limit and the K8 export limit.

-   _src\_int_ —The source interface name (inside or outside)
-   _src\_ip_ —The source IP address
-   _src\_port_ —The source port
-   _dst\_int_ —The destination interface name (inside or outside)
-   _dst\_ip_ —The destination IP address
-   _dst\_port_ —The destination port

**Recommended Action** Check to see if UC-IME is disabled. If so, activate it.

### 447001

**Error Message** `%ASA-4-447001: ASP DP to CP _queue_name_ was full. Queue length _length_, limit _limit_`

**Explanation** This message indicates a particular data path (DP) to control point (CP) event queue is full, and one or more multiple enqueue actions have failed. If the event contains a packet block, such as for CP application inspection, the packet will be dropped by the DP, and a counter from the show asp drop command will increment. If the event is for punt to CP, a typical counter is the Punt no memory ASP-drop counter.

-   _queue_ —The name of the DP-CP event queue.
-   _length_ —The current number of events on the queue.
-   _limit_ —The maximum number of events that are allowed on the queue.

**Recommended Action** The queue-full condition reflects the fact that the load on the CP has exceeded the CP processing ability, which may or may not be a temporary condition. You should consider reducing the feature load on the CP if this message appears repeatedly. Use the show asp event dp-cp command to identify the features that contribute the most load on the event queue.

### 448001

**Error Message** `%ASA-4-448001: Denied SRTP crypto session setup on flow from _src_int_:_src_ip_/_src_port_ to _dst_int_:_dst_ip_/_dst_port_, licensed K8 SRTP crypto session limit of _limit_ exceeded`

**Explanation** For a K8 platform, the limit of 250 SRTP crypto sessions is enforced. Each pair of SRTP encrypt or decrypt sessions is counted as one SRTP crypto session. A call is counted toward this limit only when encryption or decryption is required for a medium, which means that if the pass-through is set for the call, even if both legs use SRTP, they are not counted toward this limit.

-   _src\_int_ —The source interface name (inside or outside)
-   _src\_ip_ —The source IP address
-   _src\_port_ —The source port
-   _dst\_int_ —The destination interface name (inside or outside)
-   _dst\_ip_ —The destination IP address
-   _dst\_port_ —The destination port
-   _limit_ —The K8 limit of SRTP crypto sessions (250)

**Recommended Action** None required. You can set up new SRTP crypto sessions only when existing SRTP crypto sessions have been released.

### 450001

**Error Message** `ASA-4-450001: Deny traffic for protocol _protocol_id_ src _interface_name_ :_IP_address_ /_port_ dst _interface_name_ :_IP_address_ /_port_ , licensed host limit of _num_ exceeded.`

**Explanation** The licensed host limit was exceeded. This message applies to the ASA 5505 ASA only.

-   _protocol\_id_ —The protocol ID number
-   _interface\_name_ —The interface associated with the sender or receiver of the packet
-   _IP\_address_ —The IP address of the sender/receiver of the packet
-   _port_ —The port number of the packet transmitted
-   _num_ —The maximum host limit value

**Recommended Action** None required.

### 450002

**Error Message** `%ASA-4-450002: Teardown _string_ connection _connection_ for _interface_:_address_/_port_ to _interface_:_address_/_port_ duration _hh:mm:ss_ bytes _bytes_ reason _reason_string_`

**Explanation** Drop due to vPath license failure.

**Recommended Action** None required.