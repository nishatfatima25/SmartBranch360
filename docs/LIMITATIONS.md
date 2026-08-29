# Limitations

1.  **Static Parsing:** The tool relies on standard string matching and regular expressions tailored to specific Cisco IOS versions present in Packet Tracer. Changes to command output formats may break the parser.
2.  **No Live SSH:** The tool currently processes text files offline. It does not actively SSH into devices to run commands (to remain simple and avoid Netmiko/Paramiko dependencies for this college project).
3.  **Limited ACL Checking:** The security validator checks for specific string matches rather than functionally evaluating the entire ACL logic tree.
4.  **No Packet Tracer API:** Packet Tracer does not offer a supported, headless CLI automation API. The tool cannot automatically fix the `.pkt` file.
