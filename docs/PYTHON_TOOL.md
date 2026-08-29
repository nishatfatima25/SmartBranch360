# Python Tool Documentation

## Overview
The Network Assurance Tool reads a YAML specification (the intended design) and parses Cisco `show` command outputs (the actual state) to identify discrepancies.

## Components
*  `src/parser/cisco_parser.py`: Extracts information from Cisco show command outputs using regex and string splitting. It parses VLANs, trunk      interfaces, IP interface information, and access-control lists.
*   `src/validators/engine.py`: Compares parsed data against the `network_plan.yaml`. Identifies PASS/FAIL/INSUFFICIENT EVIDENCE.
*   `src/reports/generator.py`: Formats findings into a clean text report.
*   `src/models/findings.py`: Dataclass defining a single issue.

## Adding New Validators
To add a new validator (e.g., for NAT):
1.  Add a parser method in `cisco_parser.py` (e.g., `parse_ip_nat_translations`).
2.  Add a validation method in `engine.py` (e.g., `validate_nat()`).
3.  Add the call to `self.validate_nat()` inside `run_all()`.
