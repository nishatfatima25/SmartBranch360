# SmartBranch 360

## Secure Branch Office Network & Automated Network Assurance

SmartBranch 360 is a network engineering and automation project that combines a secure Cisco Packet Tracer branch-office network with a Python-based Network Assurance Tool.

The project demonstrates VLAN segmentation, inter-VLAN routing, trunking, ACL-based security, SSH management, and automated validation of Cisco network state against a predefined network design.

---

## Project Objectives

* Design a secure branch-office network using Cisco Packet Tracer.
* Separate employees, guests, servers, and management traffic using VLANs.
* Implement inter-VLAN routing using Router-on-a-Stick.
* Restrict Guest access to internal Server and Management networks.
* Provide secure device management using SSH.
* Simulate Internet connectivity and NAT/PAT.
* Develop a Python tool to automatically validate network configuration.
* Detect configuration errors and generate a human-readable assurance report.

---

## Network Design

The network simulates a branch office containing a router, two Layer 2 switches, an internal server, wireless access point, employee devices, a management workstation, and a guest wireless device.

### VLANs

| VLAN | Name       | Network       | Purpose            |
| ---- | ---------- | ------------- | ------------------ |
| 10   | Employee   | 10.10.10.0/24 | Employee users     |
| 20   | Guest      | 10.10.20.0/24 | Guest users        |
| 30   | Server     | 10.10.30.0/24 | Internal server    |
| 99   | Management | 10.10.99.0/24 | Network management |

### Default Gateways

| VLAN    | Gateway    |
| ------- | ---------- |
| VLAN 10 | 10.10.10.1 |
| VLAN 20 | 10.10.20.1 |
| VLAN 30 | 10.10.30.1 |
| VLAN 99 | 10.10.99.1 |

---

## Network Features

### VLAN Segmentation

The network is divided into four VLANs to separate employee, guest, server, and management traffic.

### Inter-VLAN Routing

Router-on-a-Stick is implemented on R1 using 802.1Q subinterfaces to provide gateway and routing functionality for the VLANs.

### Trunking

802.1Q trunk links are configured between the router and switches and between the switches, carrying the required VLANs.

### Network Security

Extended ACLs are configured on R1 to prevent Guest traffic from reaching the internal Server and Management networks.

### NAT/PAT

NAT overload is used to allow internal private network addresses to access the simulated external Internet.

### Secure Management

SSH is used for network-device management, with access restricted to the Management VLAN.

---

## Security Policy

The intended traffic policy is:

| Source     | Destination | Expected |
| ---------- | ----------- | -------- |
| Employee   | Server      | ALLOW    |
| Employee   | Internet    | ALLOW    |
| Guest      | Internet    | ALLOW    |
| Guest      | Server      | DENY     |
| Guest      | Management  | DENY     |
| Employee   | Network SSH | DENY     |
| Guest      | Network SSH | DENY     |
| Management | Network SSH | ALLOW    |

---

## Network Assurance Tool

The Python component of SmartBranch 360 validates the actual network state against the intended network design.

The intended configuration is defined in:

```text
config/network_plan.yaml
```

The tool processes exported Cisco IOS command outputs such as:

```text
show vlan brief
show interfaces trunk
show ip interface brief
show access-lists
```

The parsed information is compared against the expected network configuration.

### Validation Checks

The assurance engine currently validates:

* VLAN existence and naming
* Trunk configuration
* Required VLANs allowed on trunks
* Router sub-interface gateway IP addresses
* Guest-to-Server security policy
* Guest-to-Management security policy

---

## Automated Reporting

The tool generates a human-readable network assurance report containing:

* Overall network status
* Number of critical, high, medium, and low findings
* PASS/FAIL results
* Expected configuration
* Actual configuration
* Impact of detected issues
* Suggested remediation
* Evidence used for validation

The current validated network produced:

```text
Overall Status: PASSED

17 checks passed
0 checks failed
0 insufficient evidence
```

---

## Fault Scenario Testing

To demonstrate the effectiveness of the assurance engine, multiple intentional fault scenarios are included in the project.

These scenarios cover configuration problems such as:

* Incorrect or incomplete trunk configuration
* Missing VLANs
* Incorrect router gateway configuration
* Missing security ACL rules

The Python tool compares each faulty configuration against the expected network plan and reports the detected discrepancies.

---

## Testing

Automated unit tests are included using `pytest`.

Run:

```bash
pytest
```

The Packet Tracer network can also be manually verified using the test procedures documented in:

```text
docs/TEST_PLAN.md
```

---

## Running the Network Assurance Tool

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

Run the assurance tool with the collected network data:

```bash
python src/main.py --plan config/network_plan.yaml --data data/real_network --report reports/real_network_report.txt
```

The generated report is saved to:

```text
reports/real_network_report.txt
```

---

## Technologies Used

* Cisco Packet Tracer
* Cisco IOS
* Python 3
* YAML
* PyYAML
* pytest
* Git & GitHub

---

## Limitations

The current version processes exported Cisco command outputs as text files rather than connecting directly to physical Cisco devices.

The parser is designed around Cisco IOS output formats used in the Packet Tracer environment, so significant changes in command-output formatting may require parser updates.

ACL validation focuses on the specific security policies defined for this project rather than evaluating arbitrary ACL logic.

The Python tool validates the network state but does not automatically modify the Cisco Packet Tracer `.pkt` file.

---

## Future Scope

The project can be extended to:

* Collect device information automatically through SSH.
* Integrate network automation libraries such as Netmiko or NAPALM.
* Add additional configuration validators.
* Provide a web-based network health dashboard.
* Support larger enterprise network topologies.
* Detect additional forms of configuration drift.

---

## Project Status

**Completed**

The SmartBranch 360 network has been successfully configured and validated.

**Latest Network Assurance Result:**

**17 checks passed — 0 failures — 0 insufficient evidence.**
