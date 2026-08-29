# Fault Scenarios

## FAULT 1: Missing VLAN 20 on SW1 Trunk
*   **Fault Injection:** Remove VLAN 20 from SW1 G0/1 trunk (`switchport trunk allowed vlan 10,30,99`).
*   **Symptom:** Guest users connected to AP1 via SW2 cannot get DHCP or access the internet.
*   **Root Cause:** SW1 drops VLAN 20 traffic from SW2 before it reaches the router.
*   **Python Diagnosis:** Detects missing VLAN 20 in `show interfaces trunk`.
*   **Suggested Fix:** Add VLAN 20 back to the allowed list.

## FAULT 2: Incorrect Employee Gateway
*   **Fault Injection:** Change R1 G0/0.10 IP to `10.10.11.1`.
*   **Symptom:** Employee PCs get DHCP (if DHCP pool matches) but cannot ping Server or Internet.
*   **Root Cause:** Subinterface IP doesn't match the network plan gateway.
*   **Python Diagnosis:** Detects wrong IP on interface.
*   **Suggested Fix:** Change subinterface IP back to `10.10.10.1`.

## FAULT 3: DHCP Configuration Broken (Conceptual)
*   **Fault Injection:** Remove the `default-router` command from the GUEST_POOL.
*   **Symptom:** Guest gets an IP but no gateway, cannot ping internet.
*   **Root Cause:** DHCP missing option.
*   **Python Diagnosis:** INSUFFICIENT EVIDENCE (unless `show ip dhcp pool` is implemented).
*   **Suggested Fix:** Add `default-router 10.10.20.1` to DHCP pool.

## FAULT 4: ACL Incorrectly Allows Guest to Management
*   **Fault Injection:** Remove `deny ip 10.10.20.0 0.0.0.255 10.10.99.0 0.0.0.255` from ACL 100.
*   **Symptom:** Guest can ping Management PC.
*   **Root Cause:** Missing security rule.
*   **Python Diagnosis:** Detects missing ACL entry in `show access-lists`.
*   **Suggested Fix:** Re-add the deny statement to ACL 100 on R1.

## FAULT 5: NAT Misconfigured (Conceptual)
*   **Fault Injection:** Remove `ip nat inside` from G0/0.10.
*   **Symptom:** Employee PC can ping Server but not Internet.
*   **Root Cause:** Interface not participating in NAT.
*   **Python Diagnosis:** (Requires parsing `show running-config`).
*   **Suggested Fix:** Re-apply `ip nat inside` to the interface.
