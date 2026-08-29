import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.validators.engine import ValidationEngine

PLAN_PATH = "config/network_plan.yaml"

def test_good_data():
    engine = ValidationEngine(PLAN_PATH, "data/good")
    engine.run_all()
    failed = [f for f in engine.findings if f.status == "FAIL"]
    assert len(failed) == 0, "Good data should not have FAIL findings"

def test_fault_01():
    engine = ValidationEngine(PLAN_PATH, "data/fault_01")
    engine.run_all()
    failed = [f for f in engine.findings if f.status == "FAIL" and f.category == "TRUNK"]
    assert len(failed) > 0, "Fault 01 should detect missing VLAN on trunk"
    assert "missing" in failed[0].actual.lower()

def test_fault_02():
    engine = ValidationEngine(PLAN_PATH, "data/fault_02")
    engine.run_all()
    failed = [f for f in engine.findings if f.status == "FAIL" and f.category == "ROUTING"]
    assert len(failed) > 0, "Fault 02 should detect incorrect gateway IP"

def test_fault_04():
    engine = ValidationEngine(PLAN_PATH, "data/fault_04")
    engine.run_all()
    failed = [f for f in engine.findings if f.status == "FAIL" and f.category == "SECURITY"]
    assert len(failed) > 0, "Fault 04 should detect missing security ACL"
