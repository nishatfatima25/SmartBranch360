from dataclasses import dataclass
from typing import Optional

@dataclass
class Finding:
    category: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW, INFO
    status: str    # PASS, FAIL, INSUFFICIENT EVIDENCE
    expected: str
    actual: str
    impact: str
    evidence: str
    device: Optional[str] = None
    interface: Optional[str] = None
    vlan: Optional[str] = None
    suggested_fix: Optional[str] = None

    def __str__(self):
        return f"[{self.status}] {self.category} - {self.severity}\n" \
               f"Expected: {self.expected}\n" \
               f"Actual: {self.actual}"
