## What’s New in Each Release

This section provides the following new or changed logging information for ASA.

-   **Timestamp Logging:** Beginning with version 9.10(1), ASA provides the option to enable timestamp as per RFC 5424 in eventing syslogs. When this option is enabled, all timestamp of syslog messages would be displaying the time, in UTC, as per RFC 5424 format. Following is a sample output with RFC 5424 format:
    
    ```vbnet
    <166>2018-06-27T12:17:46Z asa : %ASA-6-110002: Failed to locate egress interface for protocol from src interface :src IP/src port to dest IP/dest port
    ```
    

## About ASA Syslog Messages

This section provides information about the ASA syslog messages; lists the message classes and their ID ranges.

-   The valid range for message IDs is between 100000 and 999999.
    
    | ![](https://www.cisco.com/content/dam/en/us/td/i/templates/note.gif)
    
    **Note** | ___
    
    When a number is skipped in a sequence, the message is no longer in the ASA code.
    
    ___ |
    |--------|---------------------------------------------------------------------------------------|
    
-   For information about how to configure logging, SNMP, and NetFlow, see the _CLI configuration guide_.
    

-   Most of the ISAKMP messages have a common set of prepended objects to help identify the tunnel. These objects precede the descriptive text of a message when available. If the object is not known at the time the message is generated, the specific heading = value combination will not be displayed.
    
    The objects will be prepended as follows:
    
    Group = groupname, Username = user, IP = IP\_address,...
    
    Where the Group identifies the tunnel group, the Username is the username from the local database or AAA server, and the IP address is the public IP address of the remote access client or L2L peer.
    

-   Typically, a traffic session displays the connection numbers/IDs for each flow in the syslog messages. However, for some of the connections, though the connection ID is incremented, the syslog messages does not display the ID. Thus, you may find missing sequence numbers in the connection IDs of the subsequent messages.
    
    For example, during a TCP traffic flow, the syslog messages display the connection IDs as 201, 202, 203, and 204 for each flow. When an ICMP flow begins, though the connection ID is internally incremented to 205 and 206, the syslog messages does not display the numbers. When another TCP flow follows, its connection numbers are now displayed as 207, 208, and so on, giving an impression of skipping sequence.
    

The following table lists the message classes and the ranges of message IDs that are associated with each class.

| Logging Class |                  Definition                  |                                          Syslog Message ID Numbers                                           |
|---------------|----------------------------------------------|--------------------------------------------------------------------------------------------------------------|
|     auth      |             User Authentication              |                                                   109, 113                                                   |
|       —       |                 Access Lists                 |                                                     106                                                      |
|       —       |             Application Firewall             |                                                     415                                                      |
|    bridge     |             Transparent Firewall             |                                                   110, 220                                                   |
|      ca       |         PKI Certification Authority          |                                                     717                                                      |
|    citrix     |                Citrix Client                 |                                                     723                                                      |
|       —       |                  Clustering                  |                                                     747                                                      |
|       —       |               Card Management                |                                                     323                                                      |
|    config     |              Command Interface               |                                              111, 112, 208, 308                                              |
|      csd      |                Secure Desktop                |                                                     724                                                      |
|      cts      |                Cisco TrustSec                |                                                     776                                                      |
|      dap      |           Dynamic Access Policies            |                                                     734                                                      |
| eap, eapoudp  | EAP or EAPoUDP for Network Admission Control |                                                   333, 334                                                   |
|     eigrp     |                EIGRP Routing                 |                                                     336                                                      |
|     email     |                 E-mail Proxy                 |                                                     719                                                      |
|       —       |            Environment Monitoring            |                                                     735                                                      |
|      ha       |                   Failover                   |                                    101, 102, 103, 104, 105, 210, 311, 709                                    |
|       —       |           Identity-based Firewall            |                                                     746                                                      |
|      ids      |          Intrusion Detection System          |                                                   400, 733                                                   |
|       —       |                IKEv2 Toolkit                 |                                                750, 751, 752                                                 |
|      ip       |                   IP Stack                   |                                           209, 215, 313, 317, 408                                            |
|     ipaa      |            IP Address Assignment             |                                                     735                                                      |
|      ips      |         Intrusion Protection System          |                                                400, 401, 420                                                 |
|       —       |                     IPv6                     |                                                     325                                                      |
|       —       |   Block lists, Allow lists, and Graylists    |                                                     338                                                      |
|       —       |                  Licensing                   |                                                     444                                                      |
|   mdm-proxy   |                  MDM Proxy                   |                                                     802                                                      |
|      nac      |          Network Admission Control           |                                                   731, 732                                                   |
|   nacpolicy   |                  NAC Policy                  |                                                     731                                                      |
|  nacsettings  |       NAC Settings to apply NAC Policy       |                                                     732                                                      |
|       —       |             Network Access Point             |                                                     713                                                      |
|      np       |              Network Processor               |                                                     319                                                      |
|       —       |                    NP SSL                    |                                                     725                                                      |
|     ospf      |                 OSPF Routing                 |                                              318, 409, 503, 613                                              |
|       —       |             Password Encryption              |                                                     742                                                      |
|       —       |                 Phone Proxy                  |                                                     337                                                      |
|      rip      |                 RIP Routing                  |                                                   107, 312                                                   |
|      rm       |               Resource Manager               |                                                     321                                                      |
|       —       |               Smart Call Home                |                                                     120                                                      |
|    session    |                 User Session                 | 106, 108, 201, 202, 204, 302, 303, 304, 305, 314, 405, 406, 407, 500, 502, 607, 608, 609, 616, 620, 703, 710 |
|     snmp      |                     SNMP                     |                                                     212                                                      |
|       —       |                   ScanSafe                   |                                                     775                                                      |
|      ssl      |                  SSL Stack                   |                                                     725                                                      |
|      svc      |                SSL VPN Client                |                                                     722                                                      |
|      sys      |                    System                    |           199, 211, 214, 216, 306, 307, 315, 414, 604, 605, 606, 610, 612, 614, 615,701, 711, 741            |
|       —       |               Threat Detection               |                                                     733                                                      |
|      tre      |          Transactional Rule Engine           |                                                     780                                                      |
|       —       |                    UC-IME                    |                                                     339                                                      |
| tag-switching |            Service Tag Switching             |                                                     779                                                      |
|      vm       |                 VLAN Mapping                 |                                                     730                                                      |
|     vpdn      |            PPTP and L2TP Sessions            |                                                213, 403, 603                                                 |
|      vpn      |                IKE and IPsec                 |                               316, 320, 402, 404, 501, 602, 702, 713, 714, 715                               |
|     vpnc      |                  VPN Client                  |                                                     611                                                      |
|     vpnfo     |                 VPN Failover                 |                                                     720                                                      |
|     vpnlb     |              VPN Load Balancing              |                                                     718                                                      |
|       —       |                    VXLAN                     |                                                     778                                                      |
|     webfo     |               WebVPN Failover                |                                                     721                                                      |
|    webvpn     |         WebVPN and AnyConnect Client         |                                                     716                                                      |
|       —       |                 NAT and PAT                  |                                                     305                                                      |

### Syslog Message Format

Syslog messages are structured as follows:

`[_<PRI>_]: [_Timestamp_] [_Device-ID_] : %ASA-_Level_-_Message_number_: _Message_text_`

Field descriptions are as follows:

|     _<PRI>_      |                                            Priority value. When the logging EMBLEM is enabled, this value is displayed in the syslog message. Logging EMBLEM is compatible with UDP and not with TCP.                                             |
|----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|   _Timestamp_    | Date and time of the event is displayed. When logging of timestamps is enabled, and if the timestamp is configured to be in the RFC 5424 format, all timestamp in syslog messages display the time in UTC, as indicated by the RFC 5424 standard. |
|   _Device-ID_    |                      The device identifier string that was configured while enabling the logging device-id option through the user interface. If enabled, the device ID does not appear in EMBLEM-formatted syslog messages.                      |
|      ASA       |                                                                      The syslog message facility code for messages that are generated by the ASA. This value is always `ASA`.                                                                       |
|     _Level_      |                                                0 through 7. The level reflects the severity of the condition described by the syslog message—the lower the number, the more severe the condition.                                                 |
| _Message_number_ |                                                                                           A unique six-digit number that identifies the syslog message.                                                                                           |
|  _Message_text_  |                                                    A text string that describes the condition. This portion of the syslog message sometimes includes IP addresses, port numbers, or usernames.                                                    |

All syslog messages that are generated by the device are documented in this guide.

The EMBLEM syslog format is a Cisco-specific convention that is built upon the RFC 3164 and RFC 5424 standards. Hence, when EMBLEM is enabled, the syslog message prints colon (:) after <PRI> field.

Example of a syslog message with logging EMBLEM, logging timestamp rfc5424, and device-id enabled. Note the colon (:) after the <PRI> field (<166>).

`<166>:2018-06-27T12:17:46Z: %ASA-6-110002: Failed to locate egress interface for _protocol_ from _src interface :src IP/src port to dest IP/dest port_`

Example of a syslog message with logging timestamp rfc5424 and device-id enabled. No colon (:) is present before the timestamp.

`2018-06-27T12:17:46Z asa : %ASA-6-110002: Failed to locate egress interface for _protocol_ from _src interface :src IP/src port to dest IP/dest port_`