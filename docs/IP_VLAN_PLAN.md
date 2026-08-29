# IP and VLAN Plan

## VLAN Scheme

| VLAN ID | Name       | Subnet          | Default Gateway | Purpose                                   |
|---------|------------|-----------------|-----------------|-------------------------------------------|
| 10      | Employee   | 10.10.10.0 /24  | 10.10.10.1      | Corporate users, requires internal/internet access |
| 20      | Guest      | 10.10.20.0 /24  | 10.10.20.1      | Guest Wi-Fi users, internet access only   |
| 30      | Server     | 10.10.30.0 /24  | 10.10.30.1      | Internal servers, isolated from guests    |
| 99      | Management | 10.10.99.0 /24  | 10.10.99.1      | Dedicated for network management (SSH)    |

## IP Addressing Plan

| Device      | Interface     | VLAN | IP Address      | Subnet Mask     | Gateway       | Note                         |
|-------------|---------------|------|-----------------|-----------------|---------------|------------------------------|
| **R1**      | G0/0.10       | 10   | 10.10.10.1      | 255.255.255.0   | N/A           | Router-on-a-stick Employee   |
| **R1**      | G0/0.20       | 20   | 10.10.20.1      | 255.255.255.0   | N/A           | Router-on-a-stick Guest      |
| **R1**      | G0/0.30       | 30   | 10.10.30.1      | 255.255.255.0   | N/A           | Router-on-a-stick Server     |
| **R1**      | G0/0.99       | 99   | 10.10.99.1      | 255.255.255.0   | N/A           | Router-on-a-stick Management |
| **R1**      | G0/1          | N/A  | DHCP / External | External Mask   | External      | Connection to Internet/Cloud |
| **SW1**     | VLAN 99       | 99   | 10.10.99.11     | 255.255.255.0   | 10.10.99.1    | Switch 1 Management          |
| **SW2**     | VLAN 99       | 99   | 10.10.99.12     | 255.255.255.0   | 10.10.99.1    | Switch 2 Management          |
| **Server1** | NIC           | 30   | 10.10.30.10     | 255.255.255.0   | 10.10.30.1    | Internal Server              |
| **AP1**     | Port 0        | 20   | DHCP            | 255.255.255.0   | 10.10.20.1    | Access Point for Guests      |
| **PC-Emp1** | NIC           | 10   | DHCP            | 255.255.255.0   | 10.10.10.1    | Employee Endpoint 1          |
| **PC-Emp2** | NIC           | 10   | DHCP            | 255.255.255.0   | 10.10.10.1    | Employee Endpoint 2          |
| **PC-Mgt1** | NIC           | 99   | 10.10.99.50     | 255.255.255.0   | 10.10.99.1    | Management Endpoint          |
| **Wireless**| Wi-Fi         | 20   | DHCP            | 255.255.255.0   | 10.10.20.1    | Guest Endpoints (Smartphones)|

## DHCP Pools (configured on R1)

*   **EMPLOYEE_POOL:** Network `10.10.10.0 /24`, Default Router `10.10.10.1`, DNS `8.8.8.8`, Exclude `10.10.10.1-10.10.10.10`
*   **GUEST_POOL:** Network `10.10.20.0 /24`, Default Router `10.10.20.1`, DNS `8.8.8.8`, Exclude `10.10.20.1-10.10.20.10`
