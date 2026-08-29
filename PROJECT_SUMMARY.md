# Project Summary: SmartBranch 360

**Project Title:** SmartBranch 360 – Secure Branch Office Network & Automated Assurance

**Domain:** Networking, Network Security, and Network Automation

**Technologies:** Cisco IOS, Cisco Packet Tracer, Python 3, YAML

---

## 1. Executive Summary and Objective

Modern branch-office networks need reliable connectivity, logical segmentation, controlled access, and efficient troubleshooting. The objective of **SmartBranch 360** is to design and validate a secure branch-office network while demonstrating how Python-based automation can assist with network configuration verification.

The project combines a Cisco Packet Tracer network topology with a custom **Network Assurance Tool** developed in Python. The network is designed using VLANs, inter-VLAN routing, ACL-based traffic restrictions, NAT, DHCP, and SSH-based device management.

The Python tool uses a YAML network plan as the expected configuration and compares it with collected Cisco IOS command outputs. It identifies configuration discrepancies and generates a human-readable report containing the status, severity, expected state, actual state, and suggested corrective action.

---

## 2. Problem Statement

Branch-office network deployments commonly involve multiple user groups with different access requirements. Employees may require access to internal servers and the Internet, while guest users should be restricted from sensitive internal networks.

Manual network configuration and troubleshooting can introduce errors such as:

1. **Configuration Errors:** Incorrect VLAN assignments, trunk configurations, or gateway addresses can cause connectivity problems.

2. **Security Misconfiguration:** Incorrect or missing ACL rules can allow guest users to access protected server or management networks.

3. **Time-Consuming Troubleshooting:** Administrators may need to manually inspect multiple Cisco IOS command outputs to identify configuration problems.

SmartBranch 360 addresses these issues by combining a structured network design with an automated validation tool.

---

## 3. Proposed Solution and Architecture

SmartBranch 360 consists of two main parts:

### Part A: Secure Network Infrastructure

The network is implemented in Cisco Packet Tracer using a router, two Layer-2 switches, a server, a wireless access point, and client devices.

### Logical Segmentation

The network is divided into four VLANs:

* **VLAN 10 – Employee:** Used by employee endpoints.
* **VLAN 20 – Guest:** Used by wireless guest users.
* **VLAN 30 – Server:** Used for internal server resources.
* **VLAN 99 – Management:** Dedicated to network administration and device management.

### Inter-VLAN Routing

Inter-VLAN communication is implemented using a **Router-on-a-Stick** design. Router subinterfaces use IEEE 802.1Q encapsulation and provide the default gateway for the corresponding VLANs.

The configured gateways are:

* VLAN 10 → `10.10.10.1`
* VLAN 20 → `10.10.20.1`
* VLAN 30 → `10.10.30.1`
* VLAN 99 → `10.10.99.1`

### Access Control

An extended ACL is applied to the Guest VLAN interface on R1. It prevents Guest VLAN traffic from reaching:

* Server VLAN `10.10.30.0/24`
* Management VLAN `10.10.99.0/24`

Other permitted traffic can continue according to the router configuration.

### DHCP

R1 provides DHCP services for the Employee and Guest networks. Employee and Guest endpoints can therefore obtain their IP configuration automatically.

### Network Address Translation

NAT overload (PAT) is configured on R1 to translate private internal addresses when traffic is sent toward the simulated external network.

### Device Management

Network-device remote management is configured using SSH with local authentication. VTY access is restricted using an access-class so that remote management is permitted from the Management network.

---

## Part B: Automated Network Assurance Tool

The second part of SmartBranch 360 is a Python-based validation system.

### Network Configuration Blueprint

The expected network design is stored in:

`config/network_plan.yaml`

The YAML file defines the expected VLANs, gateway addresses, trunk requirements, and other validation information.

It acts as the reference configuration against which collected network data is checked.

### Cisco Output Parser

The custom Cisco parser processes text output collected from Cisco IOS commands.

The parser currently handles information from commands including:

* `show vlan brief`
* `show interfaces trunk`
* `show ip interface brief`
* `show access-lists`

The extracted information is converted into structured Python data for validation.

### Validation Engine

The validation engine compares the parsed network state with the expected configuration defined in the YAML plan.

The current validation checks include:

* Required VLAN existence
* VLAN names
* Required trunk interfaces
* Allowed VLANs on trunks
* Router gateway IP addresses
* Guest-to-Server security restriction
* Guest-to-Management security restriction

Each validation produces a result such as **PASS**, **FAIL**, or **INSUFFICIENT EVIDENCE**.

### Automated Reporting

The tool generates a text-based network assurance report.

The report includes:

* Overall status
* Number of critical, high, medium, and low findings
* Passed checks
* Failed checks
* Expected configuration
* Actual configuration
* Impact
* Suggested corrective action
* Evidence command used for the check

For example, a trunk configuration problem can produce a suggested action such as:

`Configure 'switchport mode trunk' on GigabitEthernet0/1`

---

## 4. Validation and Testing

The project includes prepared network data and test scenarios to demonstrate that the assurance engine can detect configuration discrepancies.

The validation process includes checks for:

### VLAN Configuration

The tool verifies that VLANs 10, 20, 30, and 99 exist on the required switches.

### Trunk Configuration

The tool verifies that the expected trunk interfaces exist and allow the required VLANs.

### Routing Configuration

The tool verifies that R1's VLAN subinterfaces contain the expected gateway addresses.

### Security Configuration

The tool verifies the presence of ACL entries that deny Guest VLAN traffic to the Server and Management VLANs.

### Automated Test Suite

The Python project also includes automated unit tests for the validation engine.

The current test suite successfully completes with all configured tests passing.

### Real Packet Tracer Validation

The project also supports collecting actual Cisco IOS command outputs from the Packet Tracer topology and storing them under the project's data directory.

These outputs can be supplied to the Python assurance engine to validate the actual configured network.

The current real-network validation successfully reports:

**Overall Status: PASSED**

with:

* **17 checks passed**
* **0 checks failed**
* **0 insufficient evidence**

---

## 5. Limitations

The current implementation has several limitations:

1. **Static Input:** The Python tool reads previously collected Cisco command outputs from text files rather than directly connecting to network devices.

2. **Cisco Output Dependency:** The parser is designed around the Cisco IOS output formats used in the project and may require changes if command-output formats differ significantly.

3. **Limited ACL Analysis:** The security validator checks for the presence of specific ACL entries rather than performing complete packet-by-packet ACL logic analysis.

4. **No Automatic Configuration Changes:** The tool reports configuration issues but does not automatically modify Cisco devices or Packet Tracer files.

5. **Packet Tracer Environment:** The network is a simulation created in Cisco Packet Tracer rather than a deployment on physical enterprise networking equipment.

---

## 6. Future Scope

The project can be extended in several ways:

### Live Device Integration

The current file-based input system could be extended using tools such as **Netmiko** or **NAPALM** to collect command outputs directly from supported network devices.

### Expanded Validation

Additional validators could be implemented for:

* NAT translations
* DHCP bindings
* Interface status
* Routing tables
* SSH configuration
* Additional security policies

### Improved Reporting

The text-based report could be extended into a web-based dashboard showing network health, detected issues, severity levels, and historical validation results.

### Larger Network Support

The validation framework could be extended to support additional Cisco devices and larger branch-office topologies.

---

## 7. Conclusion

SmartBranch 360 demonstrates how traditional network engineering concepts can be combined with Python-based automation to improve network validation and troubleshooting.

The Cisco Packet Tracer implementation provides VLAN segmentation, Router-on-a-Stick inter-VLAN routing, DHCP, NAT, ACL-based security restrictions, and SSH-based management.

The accompanying Python Network Assurance Tool compares the intended network design with collected Cisco IOS command outputs and automatically identifies configuration discrepancies.

The successful validation of the configured real-network data, together with the automated test suite, demonstrates that the project can provide a structured and repeatable approach to checking network configuration correctness.

Overall, SmartBranch 360 provides a practical demonstration of **secure network design, configuration validation, and network automation** within a simulated branch-office environment.
