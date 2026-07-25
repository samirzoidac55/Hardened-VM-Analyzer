# Hardened-VM-Analyzer

**Detect and analyze VM-hardening evasion techniques.**

## Description
Hardened-VM-Analyzer is a security tool designed to detect artifacts and discrepancies indicative of a "hardened" virtual machine—essentially detecting the techniques used to hide a virtualized environment from analysis tools. By analyzing system-level identifiers (BIOS, MAC addresses) and comparing them against expected virtual machine signatures, this tool identifies when a VM has been deliberately modified to masquerade as a physical host.

## Features
- **System Hardening Detection**: Uncovers signs of VM-hardening scripts (anti-anti-VM).
- **Artifact Analysis**: Validates BIOS signatures and inspects network interface MAC OUI patterns.
- **Security Baseline**: Checks for common security misconfigurations (UAC status, risky services, driver signatures).
- **Extensible**: Modular architecture allows for easy addition of new evasion detection heuristics.

## Installation
Ensure you have Python installed. Clone the repository and run the tool directly.

```bash
git clone https://github.com/samirzoidac55/Hardened-VM-Analyzer.git
cd Hardened-VM-Analyzer
```

## Usage
Run the tool using the following command to collect system data and perform analysis:

```bash
python main.py collect
```

The output will provide a summary of security and evasion findings:
- `[PASS]`: Expected VM/Security state found.
- `[WARN]`: Potential hardening detected.
- `[FAIL]`: Security misconfiguration (e.g., UAC disabled).

## Testing Detection
1. **Standard VM**: Run on a default, non-hardened VM. It will report `[PASS]` for VM BIOS signatures.
2. **Hardened VM**: Apply hardening (e.g., modifying BIOS strings) and run the tool. It will detect the absence of expected VM signatures and flag `[WARN]` for potential hardening.
3. **Physical Machine**: Run on a host. It will naturally show `[WARN]` due to the absence of virtual hardware identifiers, validating the scanner's baseline.
