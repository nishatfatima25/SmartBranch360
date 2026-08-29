# PACKET TRACER BUILD GUIDE

This guide provides exact instructions for building and configuring the SmartBranch 360 network in Cisco Packet Tracer.



## 1. Devices Required

Add the following devices to the logical workspace:

* **1x Router:** Cisco 2911 or 4331

  * Rename to `R1`

* **2x Switch:** Cisco 2960

  * Rename to `SW1`
  * Rename to `SW2`

* **1x Server:** Generic Server

  * Rename to `Server1`

* **1x Access Point:** Access Point-PT

  * Rename to `AP1`

* **3x PC:** Generic PC

  * Rename to `PC-Emp1`
  * Rename to `PC-Emp2`
  * Rename to `PC-Mgt1`

* **1x Wireless End Device:** Laptop or Smart Device with wireless capability

  * Rename to `Wireless-Guest`

* **1x Internet Simulation Device:** Generic Server or PT Cloud

  * Rename to `Internet`

---

## 2. Network Addressing and VLAN Plan

| VLAN | Name       | Network       | Gateway    |
| ---- | ---------- | ------------- | ---------- |
| 10   | Employee   | 10.10.10.0/24 | 10.10.10.1 |
| 20   | Guest      | 10.10.20.0/24 | 10.10.20.1 |
| 30   | Server     | 10.10.30.0/24 | 10.10.30.1 |
| 99   | Management | 10.10.99.0/24 | 10.10.99.1 |

### Static Addresses

| Device      | IP Address  | Subnet Mask   | Gateway    |
| ----------- | ----------- | ------------- | ---------- |
| Server1     | 10.10.30.10 | 255.255.255.0 | 10.10.30.1 |
| PC-Mgt1     | 10.10.99.50 | 255.255.255.0 | 10.10.99.1 |
| SW1 VLAN 99 | 10.10.99.11 | 255.255.255.0 | 10.10.99.1 |
| SW2 VLAN 99 | 10.10.99.12 | 255.255.255.0 | 10.10.99.1 |
| R1 G0/1     | 8.8.8.1     | 255.255.255.0 | —          |

Employee and Guest endpoints receive their addresses automatically from the DHCP pools configured on R1.

---

## 3. Connections and Cabling

Connect the devices as follows.

| Source Device | Source Port        | Destination Device | Destination Port           | Cable Type                        |
| ------------- | ------------------ | ------------------ | -------------------------- | --------------------------------- |
| R1            | GigabitEthernet0/0 | SW1                | GigabitEthernet0/1         | Copper Straight-Through           |
| R1            | GigabitEthernet0/1 | Internet           | FastEthernet0 (or similar) | Copper Straight-Through           |
| SW1           | GigabitEthernet0/2 | SW2                | GigabitEthernet0/1         | Copper Cross-Over or Auto-Connect |
| SW1           | FastEthernet0/1    | Server1            | FastEthernet0              | Copper Straight-Through           |
| SW1           | FastEthernet0/2    | PC-Emp1            | FastEthernet0              | Copper Straight-Through           |
| SW1           | FastEthernet0/24   | PC-Mgt1            | FastEthernet0              | Copper Straight-Through           |
| SW2           | FastEthernet0/1    | PC-Emp2            | FastEthernet0              | Copper Straight-Through           |
| SW2           | FastEthernet0/2    | AP1                | Port 0                     | Copper Straight-Through           |

### Important Trunk Ports

The following interfaces must operate as trunks:

* SW1 `GigabitEthernet0/1`
* SW1 `GigabitEthernet0/2`
* SW2 `GigabitEthernet0/1`

Allowed VLANs:

```text
10,20,30,99
```

---

## 4. Switch Port Assignment

### SW1

| Port   | Connected Device | VLAN        | Mode   |
| ------ | ---------------- | ----------- | ------ |
| Fa0/1  | Server1          | 30          | Access |
| Fa0/2  | PC-Emp1          | 10          | Access |
| Fa0/24 | PC-Mgt1          | 99          | Access |
| Gi0/1  | R1               | 10,20,30,99 | Trunk  |
| Gi0/2  | SW2              | 10,20,30,99 | Trunk  |

### SW2

| Port  | Connected Device | VLAN        | Mode   |
| ----- | ---------------- | ----------- | ------ |
| Fa0/1 | PC-Emp2          | 10          | Access |
| Fa0/2 | AP1              | 20          | Access |
| Gi0/1 | SW1              | 10,20,30,99 | Trunk  |

---

## 5. GUI Configurations

The following devices are configured through the Packet Tracer GUI rather than the CLI.

### 5.1 Server1

Click:

`Server1 → Desktop → IP Configuration`

Select **Static**.

Set:

```text
IP Address:       10.10.30.10
Subnet Mask:      255.255.255.0
Default Gateway:  10.10.30.1
DNS Server:       8.8.8.8
```

---

### 5.2 AP1

Click:

`AP1 → Config → Port 1`

Configure the wireless settings:

```text
SSID:              SmartBranch_Guest
Authentication:    WPA2-PSK
Passphrase:        guestpass123
Encryption:        AES
```

The Access Point is used as a Layer-2 wireless access device. Guest addressing is provided by the DHCP service on R1.

---

### 5.3 PC-Emp1

Click:

`PC-Emp1 → Desktop → IP Configuration`

Select:

```text
DHCP
```

The PC should receive an address from the Employee DHCP pool:

```text
Network:       10.10.10.0/24
Gateway:       10.10.10.1
```

---

### 5.4 PC-Emp2

Click:

`PC-Emp2 → Desktop → IP Configuration`

Select:

```text
DHCP
```

The PC should receive an address from the Employee DHCP pool.

---

### 5.5 Wireless-Guest

Connect the wireless device to:

```text
SSID: SmartBranch_Guest
Password: guestpass123
```

Then go to:

`Desktop → IP Configuration`

Select:

```text
DHCP
```

The Guest device should receive an address from the Guest DHCP pool:

```text
Network:       10.10.20.0/24
Gateway:       10.10.20.1
```

---

### 5.6 PC-Mgt1

Click:

`PC-Mgt1 → Desktop → IP Configuration`

Select **Static**.

Set:

```text
IP Address:       10.10.99.50
Subnet Mask:      255.255.255.0
Default Gateway:  10.10.99.1
```

---

## 6. CLI Configurations

Open the CLI tab of each router/switch.

Enter:

```text
enable
configure terminal
```

Then apply the corresponding configuration file:

```text
docs/configs/R1.txt
docs/configs/SW1.txt
docs/configs/SW2.txt
```

### R1

The router provides:

* Inter-VLAN routing
* DHCP
* NAT
* Default route
* Guest security ACL
* SSH management

R1 subinterfaces:

```text
G0/0.10 → 10.10.10.1/24
G0/0.20 → 10.10.20.1/24
G0/0.30 → 10.10.30.1/24
G0/0.99 → 10.10.99.1/24
```

R1 Internet-facing interface:

```text
G0/1 → 8.8.8.1/24
```

---

## 7. DHCP Configuration

R1 provides DHCP for Employee and Guest networks.

### Employee DHCP Pool

```text
Network:        10.10.10.0/24
Default Router: 10.10.10.1
DNS Server:     8.8.8.8
```

### Guest DHCP Pool

```text
Network:        10.10.20.0/24
Default Router: 10.10.20.1
DNS Server:     8.8.8.8
```

The first addresses in each subnet are excluded from DHCP:

```text
10.10.10.1 - 10.10.10.10
10.10.20.1 - 10.10.20.10
```

---

## 8. Security Configuration

Guest VLAN 20 is restricted from accessing:

```text
Server VLAN 30
10.10.30.0/24
```

and:

```text
Management VLAN 99
10.10.99.0/24
```

The ACL configured on R1 denies:

```text
10.10.20.0/24 → 10.10.30.0/24
10.10.20.0/24 → 10.10.99.0/24
```

Other permitted traffic is allowed according to the configured ACL.

---

## 9. SSH Management

R1, SW1, and SW2 are configured for SSH management.

The domain is:

```text
smartbranch.local
```

The configured administrative username is:

```text
admin
```

SSH is enabled using RSA keys.

Management access is restricted to the Management network where configured.

---

## 10. Internet Device Simulation

The Packet Tracer Internet device is simulated using a Generic Server or PT Cloud.

For the current project configuration, R1's Internet-facing interface is **statically configured**, not DHCP:

```text
R1 G0/1
IP Address: 8.8.8.1
Subnet Mask: 255.255.255.0
```

The simulated Internet device uses:

```text
IP Address: 8.8.8.8
Subnet Mask: 255.255.255.0
```

R1 uses a default route through `GigabitEthernet0/1`.

NAT overload is configured on R1 so internal networks can access the simulated external network.

---

## 11. Verification Commands

After configuration, verify the network using the following commands.

### SW1 and SW2

Check VLANs:

```text
show vlan brief
```

Check trunks:

```text
show interfaces trunk
```

Check configuration:

```text
show running-config
```

### R1

Check interfaces:

```text
show ip interface brief
```

Check routing:

```text
show ip route
```

Check ACLs:

```text
show access-lists
```

Check NAT translations:

```text
show ip nat translations
```

Check DHCP leases:

```text
show ip dhcp binding
```

Check configuration:

```text
show running-config
```

---

## 12. Basic Connectivity Tests

From an Employee PC, verify the gateway:

```text
ping 10.10.10.1
```

Verify Server connectivity:

```text
ping 10.10.30.10
```

Verify Internet connectivity:

```text
ping 8.8.8.8
```

From a Guest device, Guest-to-Server traffic should be blocked:

```text
ping 10.10.30.10
```

Guest-to-Management traffic should also be blocked:

```text
ping 10.10.99.50
```

---

## 13. Collecting Data for the Network Assurance Tool

The Python Network Assurance Tool works with saved Cisco command outputs.

Create:

```text
data/real_network/
```

Save the relevant command outputs there using these filenames:

```text
SW1_show_vlan.txt
SW1_show_interfaces_trunk.txt

SW2_show_vlan.txt
SW2_show_interfaces_trunk.txt

R1_show_ip_interface_brief.txt
R1_show_access_lists.txt
```

These files provide the real Packet Tracer evidence used by the Python validation engine.

---

## 14. Running the Network Assurance Tool

From the project root:

```text
C:\CISCO\smartbranch360
```

run:

```powershell
python src/main.py --plan config/network_plan.yaml --data data/real_network --report reports/real_network_report.txt
```

A successful analysis should report:

```text
Analysis complete.
Found 0 issues.
```

The generated report should show:

```text
Overall Status: PASSED

CRITICAL: 0
HIGH: 0
MEDIUM: 0
LOW: 0
```

The current verified network produced:

```text
17 checks passed
0 checks failed
0 insufficient evidence
```

---

## 15. Automated Python Tests

The Python implementation can also be tested using:

```powershell
pytest
```

A successful test run should show:

```text
4 passed
```

---

## 16. Expected Final Status

When the topology, configurations, and evidence files are correct:

### Packet Tracer

* VLANs operational
* Trunks operational
* Inter-VLAN routing operational
* DHCP operational
* NAT operational
* SSH configured
* Guest security ACL operational
* Internet simulation reachable

### Network Assurance Tool

```text
Overall Status: PASSED
17 checks passed
0 checks failed
0 insufficient evidence
```

### Python Tests

```text
4 passed
```

This indicates that the SmartBranch 360 network configuration and the Network Assurance validation tool are functioning as intended.
