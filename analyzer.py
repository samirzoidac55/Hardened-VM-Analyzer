from collectors import system_info, registry, services, drivers, network, hardware_sensors

# Collection Phase (as per architecture diagram)
class Analyzer:
    def collect_all(self):
        return {
            "system": system_info.collect(),
            "registry": registry.collect(),
            "services": services.collect(),
            "drivers": drivers.collect(),
            "network": network.collect(),
            "hardware": hardware_sensors.collect()
        }

# Detection Phase (as per architecture diagram)
class DetectionEngine:
    def __init__(self, data):
        self.data = data
        self.findings = []

    def run(self):
        """Runs security and evasion checks on collected data."""
        self._check_uac()
        self._check_defender()
        self._check_services()
        self._check_drivers()
        self._check_evasion_artifacts()
        self._check_hardware_sensors()
            
        return self.findings

    def _check_evasion_artifacts(self):
        """Detects signs of VM hardening (anti-anti-VM)."""
        reg_data = self.data.get("registry", {}).get("data", {})
        net_data = self.data.get("network", {}).get("data", {}).get("adapters", [])

        # Check for spoofed/missing BIOS info
        bios_version = reg_data.get("SystemBiosVersion", "")
        if "VirtualBox" in bios_version or "VMware" in bios_version:
            self.findings.append({"check": "VM BIOS Artifacts Found", "status": "PASS", "severity": "LOW", "detail": "VM signature detected (not hardened)"})
        elif bios_version == "Not Found" or bios_version == "":
             self.findings.append({"check": "Missing BIOS Information", "status": "WARN", "severity": "MEDIUM", "detail": "Potential hardening: BIOS strings tampered or removed"})

        # Check for common VM MAC OUIs (e.g., VirtualBox 08:00:27)
        vm_ouis = ["08:00:27", "00:05:69", "00:0C:29"]
        found_vm_mac = False
        for adapter in net_data:
            mac = adapter.get("MacAddress", "")
            if any(oui in mac for oui in vm_ouis):
                found_vm_mac = True
                break
        
        if not found_vm_mac:
             self.findings.append({"check": "No VM-specific MAC OUI detected", "status": "WARN", "severity": "MEDIUM", "detail": "Potential hardening: MAC address spoofed or customized"})

    def _check_hardware_sensors(self):
        """Detects absence of physical hardware sensors."""
        hw_data = self.data.get("hardware", {}).get("data", {})
        thermal_zones = hw_data.get("thermal_zones", [])
        
        if not thermal_zones:
             self.findings.append({"check": "Physical Hardware Sensors", "status": "WARN", "severity": "MEDIUM", "detail": "No thermal sensor data detected: likely virtual environment"})
        else:
             self.findings.append({"check": "Physical Hardware Sensors", "status": "PASS", "severity": "LOW"})

    def _check_uac(self):
        reg_data = self.data.get("registry", {}).get("data", {})
        if reg_data.get("uac_enabled") is False:
            self.findings.append({"check": "UAC Enabled", "status": "FAIL", "severity": "HIGH"})
        else:
            self.findings.append({"check": "UAC Enabled", "status": "PASS", "severity": "LOW"})

    def _check_defender(self):
        # Simplified placeholder check for Defender presence
        # Real-world would involve checking specific registry keys/services
        self.findings.append({"check": "Windows Defender Check", "status": "INFO", "severity": "LOW", "detail": "Verify active status in Security Center"})

    def _check_services(self):
        # Check for risky services like 'RemoteRegistry'
        services = self.data.get("services", {}).get("data", {}).get("services", [])
        if isinstance(services, list):
            for service in services:
                if service.get("Name") == "RemoteRegistry" and service.get("Status") == "Running":
                    self.findings.append({"check": "Risky Service Running: RemoteRegistry", "status": "FAIL", "severity": "HIGH"})
        
    def _check_drivers(self):
        # Simple check for unsigned drivers
        drivers = self.data.get("drivers", {}).get("data", {}).get("drivers", [])
        if isinstance(drivers, list):
            unsigned = [d for d in drivers if d.get("IsSigned") is False]
            if unsigned:
                self.findings.append({"check": "Unsigned Drivers Detected", "status": "WARN", "severity": "MEDIUM", "detail": f"Found {len(unsigned)} unsigned drivers"})
            else:
                self.findings.append({"check": "Driver Signatures", "status": "PASS", "severity": "LOW"})
