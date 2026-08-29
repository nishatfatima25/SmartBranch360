# Security Policy

## Traffic Flow Matrix

| Source       | Destination    | Expected | Implementation Details                                        |
|--------------|----------------|----------|---------------------------------------------------------------|
| Employee     | Server         | ALLOW    | Default inter-VLAN routing (permitted by default).            |
| Employee     | Internet       | ALLOW    | Permitted and translated via NAT overload (PAT).              |
| Guest        | Internet       | ALLOW    | Permitted and translated via NAT overload (PAT).              |
| Guest        | Server         | DENY     | ACL applied on R1 to drop traffic from 10.10.20.0 to 10.10.30.0.|
| Guest        | Management     | DENY     | ACL applied on R1 to drop traffic from 10.10.20.0 to 10.10.99.0.|
| Employee     | Network SSH    | DENY     | VTY Access-Class restricts SSH to source VLAN 99 only.        |
| Guest        | Network SSH    | DENY     | VTY Access-Class restricts SSH to source VLAN 99 only.        |
| Management   | Network SSH    | ALLOW    | Permitted explicitly by VTY Access-Class ACL.                 |

## Device Hardening Policies
1.  **SSH Management Only:** SSH Management Only: Telnet is disabled and SSH is used for remote management.
2.  **Management VLAN:** A dedicated VLAN (99) is used for network management. In-band management interfaces (SVI) are placed in this VLAN.
3.  **Local Authentication:** Usernames and secure (secret) passwords are required for device access.
4.  **Trunking Security:** Trunk ports are explicitly configured (switchport mode trunk).
