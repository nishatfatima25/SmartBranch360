# Cisco Verification Commands

Run these commands on the respective devices in Packet Tracer to gather evidence for the Network Assurance Tool.

## Switch Verification (Run on SW1 and SW2)

1.  **VLANs:** `show vlan brief`
    *   *Proves:* VLANs exist, are named correctly, and access ports are assigned.
2.  **Trunks:** `show interfaces trunk`
    *   *Proves:* Trunk links are active, encapsulation is 802.1q, and correct VLANs are allowed.
3.  **Running Config (Partial):** `show running-config`
    *   *Proves:* Spanning-tree, interface configs, default gateways.

## Router Verification (Run on R1)

1.  **Interface IP and Status:** `show ip interface brief`
    *   *Proves:* Subinterfaces are up, IPs are assigned correctly.
2.  **Routing Table:** `show ip route`
    *   *Proves:* Directly connected routes (VLANs) and default route exist.
3.  **Access Control Lists:** `show access-lists`
    *   *Proves:* ACLs are configured with correct ACEs (Access Control Entries) and counters.
4.  **NAT Translations:** `show ip nat translations`
    *   *Proves:* Inside addresses are successfully being translated to outside addresses (after generating traffic).
5.  **DHCP Binding:** `show ip dhcp binding`
    *   *Proves:* IP addresses are successfully leased to Employee and Guest PCs.
6.  **Running Config (Partial):** `show running-config`
    *   *Proves:* NAT inside/outside placement, subinterface encapsulation, SSH configuration.
