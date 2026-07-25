def generate_text_report(findings):
    """Formats findings into a readable text report."""
    report = "VM Assessment Report\n"
    report += "====================\n\n"
    if not findings:
        report += "No findings.\n"
        return report
        
    for finding in findings:
        line = f"[{finding['status']}] {finding['check']} (Severity: {finding['severity']})"
        if "detail" in finding:
            line += f" - {finding['detail']}"
        report += line + "\n"
    return report
