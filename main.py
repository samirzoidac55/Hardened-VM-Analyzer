import argparse
import json
import os
from analyzer import Analyzer, DetectionEngine
from report import generate_text_report

def compare_with_baseline(current, baseline_path):
    if not os.path.exists(baseline_path):
        return "Baseline not found."
    with open(baseline_path, 'r') as f:
        baseline = json.load(f)
    
    # Simple registry comparison example
    current_reg = current.get("registry", {}).get("data", {})
    baseline_reg = baseline.get("registry", {}).get("data", {})
    
    if current_reg != baseline_reg:
        return "Changes detected in registry configuration!"
    return "No changes detected."

def main():
    parser = argparse.ArgumentParser(description="Windows VM Assessment Tool")
    subparsers = parser.add_subparsers(dest="command")
    
    collect_parser = subparsers.add_parser("collect", help="Collect system data and analyze")
    
    args = parser.parse_args()
    
    if args.command == "collect":
        # 1. Collection Phase
        analyzer = Analyzer()
        data = analyzer.collect_all()
        
        # Save results
        with open("results.json", "w") as f:
            json.dump(data, f, indent=4)
            
        # 2. Detection Phase
        detection_engine = DetectionEngine(data)
        findings = detection_engine.run()
        
        print(generate_text_report(findings))
        
        # Baseline check
        if os.path.exists("baseline.json"):
            print("\nBaseline Comparison:")
            print(compare_with_baseline(data, "baseline.json"))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
