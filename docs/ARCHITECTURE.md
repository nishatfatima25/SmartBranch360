# SmartBranch 360 - Architecture Document

## Overview
SmartBranch 360 is a secure branch-office networking project integrating a practical network design built in Cisco Packet Tracer with a custom Python-based Network Assurance Tool.

## 1. Network Architecture (Packet Tracer)

### Topology
The physical network consists of:
*   **Router (R1):** Handles inter-VLAN routing (Router-on-a-stick), NAT, and internet connectivity.
*   **Switches (SW1, SW2):** Provide Layer 2 connectivity and VLAN segregation. SW1 connects directly to R1. SW2 connects to SW1.
*   **Wireless Access Point (AP1):** Provides Guest Wi-Fi access, connected to SW2.
*   **Internal Server:** Hosts internal services, connected to SW1.
*   **Endpoints:** PCs assigned to specific VLANs across both switches.
*   **Internet/Cloud:** Simulated external network.

### Logical Design
The network uses the following VLANs to segregate traffic:
*   **VLAN 10 (Employee):** Corporate users requiring access to internal server and internet.
*   **VLAN 20 (Guest):** Guest users requiring internet access only (isolated from internal networks).
*   **VLAN 30 (Server):** Internal server infrastructure.
*   **VLAN 99 (Management):** Dedicated VLAN for managing network devices via SSH.

### Core Services
*   **DHCP:** R1 provides dynamic IP addressing for Employee and Guest VLANs.
*   **Inter-VLAN Routing:** R1 performs routing between VLANs using subinterfaces.
*   **NAT:** R1 translates internal IP addresses to a public IP for internet access.
*   **Security (ACLs):** Standard and Extended ACLs on R1 enforce isolation (e.g., blocking Guests from Server and Management).

## 2. Software Architecture (Python Network Assurance Tool)

The Network Assurance Tool validates the actual state of the network against the intended design.

### Components
1.  **YAML Specification (`config/network_plan.yaml`):** The "source of truth". Defines expected VLANs, subnets, and security policies.
2.  **Cisco Output Parsers (`src/parser/`):** Reads text files containing outputs from `show` commands (e.g., `show vlan brief`, `show ip interface brief`) and extracts structured data.
3.  **Data Models (`src/models/`):** Represents network state using standard Python classes/dataclasses.
4.  **Validation Engine (`src/validators/`):** Compares parsed data against the YAML specification. Implements specific rules for VLANs, subnets, trunks, DHCP, and Security.
5.  **Reporting (`src/reports/`):** Generates human-readable summaries categorizing findings by severity (CRITICAL, HIGH, MEDIUM, LOW, INFO).

### Workflow
1.  User extracts `show` command outputs from Packet Tracer into `data/` folder text files.
2.  CLI tool is executed: `python src/main.py --plan config/network_plan.yaml --data data/ --report reports/output.txt`.
3.  Tool loads YAML plan.
4.  Tool parses Cisco output texts.
5.  Validators execute checks.
6.  Tool identifies PASS, FAIL, or INSUFFICIENT EVIDENCE.
7.  Report is generated.
