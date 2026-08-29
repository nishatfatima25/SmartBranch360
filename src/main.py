import argparse
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.validators.engine import ValidationEngine
from src.reports.generator import ReportGenerator

def main():
    parser = argparse.ArgumentParser(description="SmartBranch 360 Network Assurance Tool")
    parser.add_argument("--plan", required=True, help="Path to YAML network plan")
    parser.add_argument("--data", required=True, help="Path to folder with show-command outputs")
    parser.add_argument("--report", required=True, help="Path to output report file")
    
    args = parser.parse_args()
    
    print(f"Loading plan from {args.plan}...")
    try:
        engine = ValidationEngine(args.plan, args.data)
        engine.run_all()
        
        print(f"Generating report...")
        generator = ReportGenerator(engine.findings)
        report_content = generator.generate(args.report)
        
        failed = [f for f in engine.findings if f.status == "FAIL"]
        print(f"\nAnalysis complete. Report saved to {args.report}")
        print(f"Found {len(failed)} issues.")
        
        if failed:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(2)

if __name__ == "__main__":
    main()
