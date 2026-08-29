import yaml
import os
from src.parser.cisco_parser import CiscoParser
from src.models.findings import Finding

class ValidationEngine:
    def __init__(self, plan_path: str, data_dir: str):
        self.plan_path = plan_path
        self.data_dir = data_dir
        self.parser = CiscoParser(data_dir)
        self.plan = self._load_plan()
        self.findings = []

    def _load_plan(self) -> dict:
        if not os.path.exists(self.plan_path):
            raise FileNotFoundError(f"Plan file not found: {self.plan_path}")
        with open(self.plan_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def run_all(self):
        self.validate_vlans()
        self.validate_trunks()
        self.validate_gateways()
        self.validate_security()

    def validate_vlans(self):
        # We expect VLANs on switches SW1, SW2
        expected_vlans = {str(v['id']): v['name'] for v in self.plan.get('vlans', [])}
        
        for switch in ["SW1", "SW2"]:
            actual_vlans = self.parser.parse_vlan_brief(switch)
            if actual_vlans is None:
                self.findings.append(Finding(
                    category="VLAN", severity="HIGH", status="INSUFFICIENT EVIDENCE",
                    expected=f"VLANs {list(expected_vlans.keys())} should exist on {switch}.",
                    actual=f"Missing {switch}_show_vlan.txt",
                    impact="Cannot verify VLAN configuration.", evidence="show vlan brief", device=switch
                ))
                continue
            
            for vid, vname in expected_vlans.items():
                if vid not in actual_vlans:
                    self.findings.append(Finding(
                        category="VLAN", severity="HIGH", status="FAIL",
                        expected=f"VLAN {vid} ({vname}) must exist.",
                        actual=f"VLAN {vid} is missing.",
                        impact="Connectivity for this VLAN will fail.",
                        suggested_fix=f"Create VLAN {vid} on {switch}.",
                        evidence="show vlan brief", device=switch, vlan=vid
                    ))
                elif actual_vlans[vid]['name'].lower() != vname.lower():
                    self.findings.append(Finding(
                        category="VLAN", severity="LOW", status="FAIL",
                        expected=f"VLAN {vid} name should be {vname}.",
                        actual=f"VLAN {vid} name is {actual_vlans[vid]['name']}.",
                        impact="Naming inconsistency.",
                        suggested_fix=f"Rename VLAN {vid} to {vname}.",
                        evidence="show vlan brief", device=switch, vlan=vid
                    ))
                else:
                    self.findings.append(Finding(
                        category="VLAN", severity="INFO", status="PASS",
                        expected=f"VLAN {vid} ({vname}) exists.",
                        actual=f"VLAN {vid} exists.",
                        impact="None", evidence="show vlan brief", device=switch, vlan=vid
                    ))

    def validate_trunks(self):
        trunks = self.plan.get('trunks', [])
        for trunk in trunks:
            dev = trunk['device']
            intf = trunk['interface']
            # allow short names Gi0/1, Gig0/1 vs GigabitEthernet0/1
            short_intf_gi = intf.replace('GigabitEthernet', 'Gi')
            short_intf_gig = intf.replace('GigabitEthernet', 'Gig')
            short_intf_fa = intf.replace('FastEthernet', 'Fa')
            expected_vlans = [str(v) for v in trunk['allowed_vlans']]
            
            actual_trunks = self.parser.parse_interfaces_trunk(dev)
            if actual_trunks is None:
                self.findings.append(Finding(
                    category="TRUNK", severity="HIGH", status="INSUFFICIENT EVIDENCE",
                    expected=f"Trunk {intf} on {dev} should allow VLANs {expected_vlans}.",
                    actual=f"Missing {dev}_show_interfaces_trunk.txt",
                    impact="Cannot verify trunk allowed VLANs.", evidence="show interfaces trunk", device=dev, interface=intf
                ))
                continue
            
            # check if trunk interface exists in parsed data
            found = False
            for act_intf, act_vlans in actual_trunks.items():
                if act_intf in (intf, short_intf_gi, short_intf_gig, short_intf_fa):
                    found = True
                    missing_vlans = set(expected_vlans) - set(act_vlans)
                    if missing_vlans:
                        self.findings.append(Finding(
                            category="TRUNK", severity="HIGH", status="FAIL",
                            expected=f"Trunk {intf} must allow VLANs {expected_vlans}.",
                            actual=f"VLANs {list(missing_vlans)} are missing from allowed list.",
                            impact="Traffic for missing VLANs will be dropped across switches.",
                            suggested_fix=f"Add VLANs to allowed list on {intf}.",
                            evidence="show interfaces trunk", device=dev, interface=intf
                        ))
                    else:
                        self.findings.append(Finding(
                            category="TRUNK", severity="INFO", status="PASS",
                            expected=f"Trunk {intf} allows required VLANs.",
                            actual="All required VLANs are allowed.",
                            impact="None", evidence="show interfaces trunk", device=dev, interface=intf
                        ))
            if not found:
                self.findings.append(Finding(
                    category="TRUNK", severity="HIGH", status="FAIL",
                    expected=f"Interface {intf} should be a trunk.",
                    actual=f"Interface {intf} is not operating as a trunk.",
                    impact="Inter-switch or router connectivity will fail.",
                    suggested_fix=f"Configure 'switchport mode trunk' on {intf}.",
                    evidence="show interfaces trunk", device=dev, interface=intf
                ))

    def validate_gateways(self):
        # Validate IPs on R1 match the planned gateways
        expected_gws = {str(v['id']): v['gateway'] for v in self.plan.get('vlans', []) if v['gateway']}
        actual_ints = self.parser.parse_ip_int_brief("R1")
        if actual_ints is None:
            self.findings.append(Finding(
                category="ROUTING", severity="HIGH", status="INSUFFICIENT EVIDENCE",
                expected="Router subinterfaces should have gateway IPs.",
                actual="Missing R1_show_ip_interface_brief.txt",
                impact="Cannot verify inter-VLAN routing IPs.", evidence="show ip int brief", device="R1"
            ))
            return
            
        for vid, gw in expected_gws.items():
            # e.g., GigabitEthernet0/0.10
            intf_name = f"GigabitEthernet0/0.{vid}"
            if intf_name not in actual_ints:
                self.findings.append(Finding(
                    category="ROUTING", severity="HIGH", status="FAIL",
                    expected=f"Interface {intf_name} should have IP {gw}.",
                    actual=f"Interface {intf_name} does not exist.",
                    impact=f"VLAN {vid} will not have a default gateway.",
                    suggested_fix=f"Create subinterface {intf_name} and assign IP {gw}.",
                    evidence="show ip int brief", device="R1", vlan=vid
                ))
            elif actual_ints[intf_name]['ip'] != gw:
                self.findings.append(Finding(
                    category="ROUTING", severity="HIGH", status="FAIL",
                    expected=f"Interface {intf_name} IP should be {gw}.",
                    actual=f"Interface {intf_name} IP is {actual_ints[intf_name]['ip']}.",
                    impact=f"VLAN {vid} clients will fail to route traffic if they expect {gw}.",
                    suggested_fix=f"Change IP on {intf_name} to {gw}.",
                    evidence="show ip int brief", device="R1", interface=intf_name
                ))
            else:
                self.findings.append(Finding(
                    category="ROUTING", severity="INFO", status="PASS",
                    expected=f"Interface {intf_name} IP is {gw}.",
                    actual=f"Interface {intf_name} IP is correct.",
                    impact="None", evidence="show ip int brief", device="R1", interface=intf_name
                ))

    def validate_security(self):
        acls = self.parser.parse_access_lists("R1")
        if acls is None:
            self.findings.append(Finding(
                category="SECURITY", severity="CRITICAL", status="INSUFFICIENT EVIDENCE",
                expected="Security ACLs should be configured.",
                actual="Missing R1_show_access_lists.txt",
                impact="Cannot verify security policies.", evidence="show access-lists", device="R1"
            ))
            return
        
        # Very simple validation: check if 'deny ip 10.10.20.0 0.0.0.255 10.10.30.0 0.0.0.255' exists
        guest_server_deny = False
        guest_mgmt_deny = False
        
        for line in acls:
            if "deny ip 10.10.20.0 0.0.0.255 10.10.30.0 0.0.0.255" in line:
                guest_server_deny = True
            if "deny ip 10.10.20.0 0.0.0.255 10.10.99.0 0.0.0.255" in line:
                guest_mgmt_deny = True
                
        if not guest_server_deny:
            self.findings.append(Finding(
                category="SECURITY", severity="CRITICAL", status="FAIL",
                expected="Guest VLAN (10.10.20.0) must be denied access to Server VLAN (10.10.30.0).",
                actual="No ACL entry found denying this traffic.",
                impact="Guests can access internal servers.",
                suggested_fix="Add an ACE denying 10.10.20.0 to 10.10.30.0.",
                evidence="show access-lists", device="R1"
            ))
        else:
            self.findings.append(Finding(
                category="SECURITY", severity="INFO", status="PASS",
                expected="Guest to Server traffic is denied.",
                actual="ACL entry exists.",
                impact="None", evidence="show access-lists", device="R1"
            ))
            
        if not guest_mgmt_deny:
             self.findings.append(Finding(
                category="SECURITY", severity="CRITICAL", status="FAIL",
                expected="Guest VLAN (10.10.20.0) must be denied access to Management VLAN (10.10.99.0).",
                actual="No ACL entry found denying this traffic.",
                impact="Guests can access management network.",
                suggested_fix="Add an ACE denying 10.10.20.0 to 10.10.99.0.",
                evidence="show access-lists", device="R1"
            ))
        else:
            self.findings.append(Finding(
                category="SECURITY", severity="INFO", status="PASS",
                expected="Guest to Management traffic is denied.",
                actual="ACL entry exists.",
                impact="None", evidence="show access-lists", device="R1"
            ))
