import re
from typing import Dict, List, Optional

class CiscoParser:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        
    def read_file(self, filename: str) -> Optional[str]:
        import os
        path = os.path.join(self.data_dir, filename)
        if not os.path.exists(path):
            return None
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def parse_vlan_brief(self, device: str) -> Optional[Dict[str, Dict]]:
        """Parses 'show vlan brief' for a specific device. Assuming filename: <device>_show_vlan.txt"""
        content = self.read_file(f"{device}_show_vlan.txt")
        if not content:
            return None
            
        vlans = {}
        # Simple regex to match VLAN lines: "10   Employee   active   Fa0/1, Fa0/2"
        for line in content.splitlines():
            match = re.match(r'^(\d+)\s+(\S+)\s+(active|suspended)\s*(.*)', line)
            if match:
                vid, name, status, ports = match.groups()
                vlans[vid] = {
                    "name": name,
                    "status": status,
                    "ports": [p.strip() for p in ports.split(',')] if ports else []
                }
        return vlans

    def parse_interfaces_trunk(self, device: str) -> Optional[Dict[str, List[str]]]:
        """Parses 'show interfaces trunk'. Assuming filename: <device>_show_interfaces_trunk.txt"""
        content = self.read_file(f"{device}_show_interfaces_trunk.txt")
        if not content:
            return None
            
        trunks = {}
        # Simple parsing for allowed vlans
        # Find line: Port        Vlans allowed on trunk
        #            Gi0/1       10,20,30,99
        lines = content.splitlines()
        parsing_allowed = False
        for line in lines:
            if "Vlans allowed on trunk" in line:
                parsing_allowed = True
                continue
            if parsing_allowed and line.strip():
                parts = line.strip().split()
                if len(parts) >= 2 and ('/' in parts[0] or 'Fa' in parts[0] or 'Gi' in parts[0]):
                    port = parts[0]
                    vlans_str = parts[1]
                    vlans = []
                    for v in vlans_str.split(','):
                        if '-' in v:
                            start, end = v.split('-')
                            vlans.extend([str(i) for i in range(int(start), int(end)+1)])
                        else:
                            vlans.append(v)
                    trunks[port] = vlans
        return trunks

    def parse_ip_int_brief(self, device: str) -> Optional[Dict[str, Dict]]:
        """Parses 'show ip interface brief'. Assuming filename: <device>_show_ip_interface_brief.txt"""
        content = self.read_file(f"{device}_show_ip_interface_brief.txt")
        if not content:
            return None
            
        interfaces = {}
        for line in content.splitlines():
            # Interface  IP-Address  OK? Method Status  Protocol
            # GigabitEthernet0/0.10  10.10.10.1  YES manual up up
            parts = line.split()
            if len(parts) >= 6 and ('Ethernet' in parts[0] or 'Vlan' in parts[0]):
                interfaces[parts[0]] = {
                    "ip": parts[1],
                    "status": parts[4],
                    "protocol": parts[5]
                }
        return interfaces

    def parse_access_lists(self, device: str) -> Optional[List[str]]:
        """Parses 'show access-lists'. Assuming filename: <device>_show_access_lists.txt"""
        content = self.read_file(f"{device}_show_access_lists.txt")
        if not content:
            return None
        return content.splitlines()
