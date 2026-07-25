import subprocess
import json

def collect():
    """Collects PnP signed driver details using PowerShell."""
    try:
        # Note: Get-WmiObject can be slow, but it's reliable for this info
        cmd = "powershell -Command \"Get-WmiObject Win32_PnPSignedDriver | Select-Object -Property DeviceName, Manufacturer, DriverVersion, IsSigned | ConvertTo-Json\""
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, encoding='utf-8', errors='replace')
        if result.returncode == 0:
            drivers = json.loads(result.stdout)
            return {"status": "success", "data": {"drivers": drivers}}
        return {"status": "error", "message": "Failed to collect drivers"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
