from typing import List
from src.models.findings import Finding

class ReportGenerator:
    def __init__(self, findings: List[Finding]):
        self.findings = findings

    def generate(self, output_path: str):
        passed = [f for f in self.findings if f.status == "PASS"]
        failed = [f for f in self.findings if f.status == "FAIL"]
        insufficient = [f for f in self.findings if f.status == "INSUFFICIENT EVIDENCE"]
        
        crit_count = len([f for f in failed if f.severity == "CRITICAL"])
        high_count = len([f for f in failed if f.severity == "HIGH"])
        med_count = len([f for f in failed if f.severity == "MEDIUM"])
        low_count = len([f for f in failed if f.severity == "LOW"])
        
        overall_status = "FAILED" if failed else "PASSED"
        if not failed and not passed and insufficient:
            overall_status = "INCONCLUSIVE"
            
        report_lines = [
            "SMARTBRANCH 360",
            "NETWORK ASSURANCE REPORT",
            "",
            f"Overall Status: {overall_status}",
            "",
            f"CRITICAL: {crit_count}",
            f"HIGH: {high_count}",
            f"MEDIUM: {med_count}",
            f"LOW: {low_count}",
            "\n" + "-"*32 + "\n"
        ]
        
        for f in failed:
            report_lines.append(f"[FAIL] {f.category}")
            report_lines.append(f"Severity: {f.severity}")
            if f.device: report_lines.append(f"Device: {f.device}")
            if f.vlan: report_lines.append(f"VLAN: {f.vlan}")
            report_lines.append(f"Expected:\n{f.expected}")
            report_lines.append(f"Actual:\n{f.actual}")
            report_lines.append(f"Impact:\n{f.impact}")
            report_lines.append(f"Suggested Fix:\n{f.suggested_fix}")
            report_lines.append(f"Evidence:\n{f.evidence}")
            report_lines.append("-" * 32)
            
        for f in insufficient:
            report_lines.append(f"[INSUFFICIENT EVIDENCE] {f.category}")
            report_lines.append(f"Missing File: {f.actual}")
            report_lines.append("-" * 32)
            
        for f in passed:
            report_lines.append(f"[PASS] {f.category} - {f.expected}")
            
        report_lines.append("\n" + "="*32)
        report_lines.append("SUMMARY")
        report_lines.append(f"{len(passed)} checks passed")
        report_lines.append(f"{len(failed)} checks failed")
        report_lines.append(f"{len(insufficient)} insufficient evidence")
        
        if failed:
            report_lines.append("\nRecommended Actions:")
            for i, f in enumerate(failed, 1):
                report_lines.append(f"{i}. {f.suggested_fix}")
                
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_lines))
        
        return "\n".join(report_lines)
