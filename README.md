# Hardened-VM-Analyzer

A Windows-oriented tool designed to detect artifacts and discrepancies indicative of a "hardened" virtual machine—essentially detecting techniques used to hide a VM from malware (anti-anti-VM).

## Overview
This tool performs security and evasion detection checks on a Windows system. It identifies potential signs of VM hardening, such as spoofed BIOS strings, missing virtualized hardware identifiers, or tampered network configuration.

## Features
- **System Hardening Detection**: Detects signs of VM-hardening scripts (anti-anti-VM).
- **Artifact Analysis**: Checks for known VM BIOS signatures and MAC address OUI patterns.
- **Security Baseline**: Includes checks for UAC status, risky services (e.g., RemoteRegistry), and driver signatures.
- **Extensible**: Modular collector architecture for easy addition of new evasion detection heuristics.

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
To test the tool's effectiveness:
1. **Standard VM**: Run the tool on a default, non-hardened VM. It will report `[PASS]` for VM BIOS signatures.
2. **Hardened VM**: Apply hardening (e.g., modifying BIOS strings in VirtualBox) and run the tool again. It will detect the absence of expected VM signatures and flag `[WARN]` for potential hardening.
3. **Physical Machine**: Run the tool on a host. It will naturally show `[WARN]` due to the absence of virtual hardware identifiers, validating the scanner's baseline.
